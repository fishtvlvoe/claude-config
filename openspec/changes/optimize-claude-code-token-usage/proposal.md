# Change: optimize-claude-code-token-usage

## Why

Claude Code 4.7 改版引入 deferred tools 機制，加上長期使用累積的多層設定（hooks、rules/、memory/、plugins），導致每次 session 啟動的 context 量膨脹到 10,285 tokens，配合 Opus 主對話使用成本高，7 天用量達 $146.39（Opus 佔 40%）。

用戶痛點：
1. TaskUpdate 等常用工具被 defer，每次要 ToolSearch 打斷流暢度
2. Session 啟動塞入過多自動載入內容（routing/spectra 規則全文、上次 session 整段摘要、多個 memory 檔）
3. 不用的 launchd 背景服務持續運作（含一個永遠跑不起來的 fish-knowledge-pipeline）
4. Homebrew / caches 長期未清理

## What Changes

### 設定層
- **ENABLE_TOOL_SEARCH=false**：關閉 deferred tools，常用工具一次載入
- **刪除 Cache Keepalive SessionStart hook**：已有 cron 在跑，重複提醒每 session 浪費 60 tokens

### 背景服務層
- **刪除 healthcheck launchd**：每週一下午燒 token 的記憶系統健檢，改手動 `/大健檢`
- **刪除 buygo.archive launchd**：已改用 GitHub 同步
- **刪除 fish-knowledge-pipeline launchd**：專案從未完成，每次開機噴錯
- **新增 token-report launchd**：每週一 9:07 自動產報告（電腦沒開會補跑）

### Rules 架構層
- **routing.md：254 行 → 45 行**（觸發表 + on-demand）
- **spectra-agent-routing.md：322 行 → 60 行**
- 詳細規則移到 `~/.claude/rules/detail/*.md`，需要時 `Read` 載入

### Hook 層
- **session-start.js 參數調整**：
  - `MAX_AGE_DAYS`：7 → 3
  - 上次 session 摘要：全文 → 前 25 行
  - Smart Context：所有檔 → 只載 1 個
- **soul.md 加硬規則**：Spectra 預設開啟，每次任務第一句話必須路由判斷

### 一次性清理
- 清 `~/Library/Caches`（3.9G → 24K）
- `brew upgrade`（394 個套件更新）
- 文章 repo 88 個 Spectra archive 檔 commit + push，建立 GitHub private repo

## Non-Goals

- **不處理 claude-mem plugin 啟用**：會與現有 5 lifecycle hooks 衝突，暫緩
- **不處理 caveman 壓縮**：對繁體中文效果差（本身已精簡），跳過
- **不砍 `enabledPlugins` 20 個 false 條目**：token 差不到 100，不值得冒險
- **不動 `~/.claude/projects/` 歷史 session**：2,163 個 JSONL（587MB），Fish 要保留
- **不改 MCP 設定**：linear-server、kimi-code、pencil、stitch 運作正常

## Capabilities

### Modified Capabilities

- `claude-code-config`：Claude Code 環境配置標準，涵蓋 settings/hooks/rules/memory 的 token 優化架構

## Impact

### Affected code
- `~/.claude/settings.json`（env + hooks）
- `~/.claude/rules/routing.md`（重寫為速查表）
- `~/.claude/rules/spectra-agent-routing.md`（重寫為速查表）
- `~/.claude/rules/detail/routing-full.md`（新增，原 routing 全文）
- `~/.claude/rules/detail/spectra-agent-routing-full.md`（新增，原 spectra 全文）
- `~/.claude/soul.md`（加 Spectra 硬規則區塊）
- `~/.claude/scripts/hooks/session-start.js`（3 處參數調整）

### Affected launchd plists（`~/Library/LaunchAgents/`）
- 刪除：`com.fishtv.healthcheck.plist`
- 刪除：`com.buygo.archive.plist`
- 刪除：`com.fishtv.fish-knowledge-pipeline.plist`
- 新增：`com.fishtv.token-report.plist`

### Results
- **Session 啟動 context：10,285 → 約 5,200 tokens（省 50%）**
- **RTK 歷史累計：已省 40.6M tokens（97%）**
- 磁碟：Library/Caches 釋放 3.9G
- 套件：394 個 brew 套件升到最新

## Backup Location

所有被改/刪的檔案備份：`~/.claude/backups/2026-04-17-optimization/`
