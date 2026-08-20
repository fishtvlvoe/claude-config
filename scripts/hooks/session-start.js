#!/usr/bin/env node
/**
 * SessionStart Hook — Memory Engine
 * 1. 載入上次 session 摘要
 * 2. Smart Context：根據 CWD 自動載入對應記憶檔
 * 3. 載入最近的踩坑紀錄
 * stdout 的內容會被 Claude 看到（注入 context）
 */

const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || process.env.USERPROFILE;
const SESSIONS_DIR = path.join(HOME, '.claude', 'sessions');
// Auto-detect project memory directory from CWD
// Claude Code stores project memory in ~/.claude/projects/{project-id}/memory/
// You may need to adjust this path for your setup
const MEMORY_DIR = path.join(HOME, '.claude', 'projects', getProjectId(), 'memory');

function getProjectId() {
  const cwd = process.cwd().replace(/\\/g, '/');
  const parts = cwd.split('/').filter(Boolean);
  if (parts.length === 0) return 'default';
  const drive = parts[0].replace(':', '');
  const rest = parts.slice(1).join('-');
  return `${drive}--${rest}`;
}
const LEARNED_DIR = path.join(HOME, '.claude', 'skills', 'learned');
const MAX_AGE_DAYS = 3; // 從 7 降為 3，只看最近 session
const SUMMARY_HEAD_LINES = 15; // 上次 session 摘要只取前 15 行（2026-05-19 從 25 降）
const SMART_CONTEXT_MAX_FILES = 1; // Smart Context 每專案只載 1 個檔
const SMART_CONTEXT_HEAD_LINES = 20; // Smart Context 每檔只讀前 20 行（2026-05-19 從 50 降，砍 Recent Activity 表格 9.8KB → 4KB）

// === Smart Context: auto-scan all project memory directories ===
function autoDetectProjectContext() {
  const projectsDir = path.join(HOME, '.claude', 'projects');
  if (!fs.existsSync(projectsDir)) return null;

  const cwd = process.cwd().replace(/\\/g, '/').toLowerCase();

  // 掃描所有專案目錄，找出有 memory/ 的
  const entries = fs.readdirSync(projectsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;

    const memDir = path.join(projectsDir, entry.name, 'memory');
    if (!fs.existsSync(memDir)) continue;

    // 從 project-id 還原路徑片段來比對 CWD
    // project-id 格式：drive--path-segments（例如 C--Users-kaoru-my-project）
    const segments = entry.name.split('--').join('/').split('-');
    const projectHint = segments.filter(s => s.length > 1).join('/').toLowerCase();

    // 檢查 CWD 是否包含這個專案的路徑片段
    const keyParts = entry.name.replace(/^[a-zA-Z]--/, '').split('-').filter(s => s.length > 2);
    const isMatch = keyParts.length > 0 && keyParts.every(part => cwd.includes(part.toLowerCase()));

    if (isMatch) {
      // 載入該專案 memory/ 下所有 .md 檔案
      const mdFiles = fs.readdirSync(memDir).filter(f => f.endsWith('.md'));
      const loaded = [];
      for (const filename of mdFiles) {
        const filepath = path.join(memDir, filename);
        const content = fs.readFileSync(filepath, 'utf-8').trim();
        // 只載入前 SMART_CONTEXT_HEAD_LINES 行，避免 context 爆炸
        const lines = content.split('\n').slice(0, SMART_CONTEXT_HEAD_LINES);
        loaded.push({ name: filename, content: lines.join('\n') });
      }
      return { project: entry.name, files: loaded };
    }
  }
  return null;
}

// === 找最近的 session 摘要 ===
function findLatestSession() {
  if (!fs.existsSync(SESSIONS_DIR)) return null;

  const now = Date.now();
  const maxAge = MAX_AGE_DAYS * 24 * 60 * 60 * 1000;

  const files = fs.readdirSync(SESSIONS_DIR)
    .filter(f => f.endsWith('-session.md'))
    .map(f => ({
      name: f,
      path: path.join(SESSIONS_DIR, f),
      mtime: fs.statSync(path.join(SESSIONS_DIR, f)).mtimeMs
    }))
    .filter(f => (now - f.mtime) < maxAge)
    .sort((a, b) => b.mtime - a.mtime);

  return files.length > 0 ? files[0] : null;
}

// === Smart Context：自動偵測 CWD 對應的專案記憶 ===
function loadSmartContext() {
  return autoDetectProjectContext();
}

// === 找最近的踩坑紀錄 ===
function findRecentPitfalls() {
  if (!fs.existsSync(LEARNED_DIR)) return null;

  const now = Date.now();
  const maxAge = 3 * 24 * 60 * 60 * 1000; // 3 天內

  const files = fs.readdirSync(LEARNED_DIR)
    .filter(f => f.startsWith('auto-pitfall-') && f.endsWith('.md'))
    .map(f => ({
      name: f,
      path: path.join(LEARNED_DIR, f),
      mtime: fs.statSync(path.join(LEARNED_DIR, f)).mtimeMs
    }))
    .filter(f => (now - f.mtime) < maxAge)
    .sort((a, b) => b.mtime - a.mtime);

  return files.length > 0 ? files[0] : null;
}

// === 設定衛兵：檢查關鍵優化是否還在 ===
function checkOptimizationHealth() {
  const warnings = [];
  const settingsPath = path.join(HOME, '.claude', 'settings.json');

  try {
    const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf-8'));
    const allow = settings?.permissions?.allow || [];

    // 1. Edit/Write Development 白名單（跳過 Auto Mode 分類器）
    const hasEditDev = allow.some(r => r.includes('Edit(/Users/fishtv/Development'));
    const hasWriteDev = allow.some(r => r.includes('Write(/Users/fishtv/Development'));
    if (!hasEditDev || !hasWriteDev) {
      warnings.push('Edit/Write Development 白名單遺失 → 每次編輯都觸發 Opus 分類器（+15-28% token）');
    }

    // 2. 不該有的 MCP（dfs-mcp 已移除）
    const mcpServers = settings?.mcpServers || {};
    if (mcpServers['dfs-mcp']) {
      warnings.push('dfs-mcp 已復活（應該移除）');
    }

    // 3. disable-model-invocation 抽檢（隨機 5 個 skill）
    // 已被 settings.json 覆蓋（skillOverrides: off 或 skills.disable-model-invocation）的
    // skill 不算缺失 —— 模型本來就看不到/叫不到它，SKILL.md 裡沒寫這行不影響行為。
    const skillsDir = path.join(HOME, '.claude', 'skills');
    if (fs.existsSync(skillsDir)) {
      const overriddenOff = new Set(
        Object.entries(settings?.skillOverrides || {})
          .filter(([, v]) => v === 'off')
          .map(([k]) => k)
      );
      const dmiCovered = new Set(
        Object.entries(settings?.skills || {})
          .filter(([, v]) => v?.['disable-model-invocation'])
          .map(([k]) => k)
      );
      const skills = fs.readdirSync(skillsDir).filter(d => {
        const sp = path.join(skillsDir, d, 'SKILL.md');
        return fs.existsSync(sp) && !overriddenOff.has(d) && !dmiCovered.has(d);
      });
      // 抽 5 個檢查
      const sample = skills.sort(() => Math.random() - 0.5).slice(0, 5);
      const missing = sample.filter(s => {
        const content = fs.readFileSync(path.join(skillsDir, s, 'SKILL.md'), 'utf-8');
        return !content.includes('disable-model-invocation: true');
      });
      if (missing.length > 0) {
        warnings.push(`Skill 缺少 disable-model-invocation: ${missing.join(', ')}`);
      }
    }
  } catch (err) {
    // 靜默失敗，不阻塞 session
  }

  return warnings;
}

// === 主程式 ===
function main() {
  const output = [];

  try {
    // 1. 載入上次 session 摘要（只取前 SUMMARY_HEAD_LINES 行）
    const latest = findLatestSession();
    if (latest) {
      const content = fs.readFileSync(latest.path, 'utf-8').trim();
      if (content && content.length >= 20) {
        const date = latest.name.split('-session.md')[0];
        const lines = content.split('\n').slice(0, SUMMARY_HEAD_LINES);
        const truncated = content.split('\n').length > SUMMARY_HEAD_LINES ? `\n... (完整摘要見 ${latest.path})` : '';
        output.push(`[Memory Engine] 上次工作摘要（${date}）：\n${lines.join('\n')}${truncated}`);
      }
    }

    if (output.length === 0) {
      output.push('[Memory Engine] 沒有找到最近的工作紀錄，這是全新的開始！');
    }

    // 2. Smart Context（只載前 SMART_CONTEXT_MAX_FILES 個檔）
    const context = loadSmartContext();
    if (context) {
      output.push(`\n[Memory Engine] 偵測到專案：${context.project}`);
      const filesToLoad = context.files.slice(0, SMART_CONTEXT_MAX_FILES);
      for (const file of filesToLoad) {
        output.push(`--- ${file.name} ---\n${file.content}`);
      }
      if (context.files.length > SMART_CONTEXT_MAX_FILES) {
        const remaining = context.files.slice(SMART_CONTEXT_MAX_FILES).map(f => f.name).join(', ');
        output.push(`（其他記憶檔待命，Read 即可載入：${remaining}）`);
      }
    }

    // 3. 最近踩坑（已關閉：auto-pitfall 品質差，真正教訓在 lessons.md）

    // 4. 設定衛兵
    const optWarnings = checkOptimizationHealth();
    if (optWarnings.length > 0) {
      output.push(`\n⚠️ [設定衛兵] 偵測到優化設定異常：`);
      optWarnings.forEach(w => output.push(`  - ${w}`));
      output.push('  → 執行 /健檢 或手動修復');
    }
  } catch (err) {
    output.push('[Memory Engine] 載入記憶時發生問題，但不影響正常使用');
  }

  process.stdout.write(output.join('\n') + '\n');
}

main();
