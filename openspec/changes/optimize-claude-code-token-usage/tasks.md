# Tasks: optimize-claude-code-token-usage

> 執行日期：2026-04-17
> 執行者：Fish + Claude（主對話）
> 狀態：全部完成 ✅

## 1. Session 啟動機制恢復

- [x] 1.1 加 `ENABLE_TOOL_SEARCH=false` 到 `~/.claude/settings.json` env
  - 結果：TaskUpdate/WebSearch/Kimi MCP 等常用工具不再 defer
- [x] 1.2 刪除 Cache Keepalive SessionStart hook（已有 cron 在跑，不需要每次提醒）

## 2. 背景服務清理（launchd）

- [x] 2.1 刪除 `com.fishtv.healthcheck.plist`（每週一燒 token 的健檢，改手動）
- [x] 2.2 刪除 `com.buygo.archive.plist`（已用 GitHub 同步取代）
- [x] 2.3 刪除 `com.fishtv.fish-knowledge-pipeline.plist`（專案從未建成）
- [x] 2.4 新增 `com.fishtv.token-report.plist`（每週一 9:07 跑，電腦沒開會補跑）
  - 測試：`launchctl start com.fishtv.token-report` 驗證成功

## 3. Rules 觸發表改造（最大 token 省下處）

- [x] 3.1 備份舊檔到 `~/.claude/backups/2026-04-17-optimization/`
- [x] 3.2 搬 `routing.md` → `rules/detail/routing-full.md`（on-demand 載入）
- [x] 3.3 搬 `spectra-agent-routing.md` → `rules/detail/spectra-agent-routing-full.md`
- [x] 3.4 寫新版精簡 `routing.md`（254 行 → 45 行速查表）
- [x] 3.5 寫新版精簡 `spectra-agent-routing.md`（322 行 → 60 行速查表）
- [x] 3.6 量測：自動載入從 10,285 → 7,232 tokens（-30%）

## 4. Session Hook 索引瘦身

- [x] 4.1 備份 `session-start.js` 到 backups/
- [x] 4.2 改 `MAX_AGE_DAYS`：7 → 3
- [x] 4.3 改上次 session 摘要載入：全文 → 前 25 行（超出標註 full path）
- [x] 4.4 改 Smart Context：載所有檔 → 只載 1 個（其餘標名待命）
- [x] 4.5 測試：`node session-start.js` 實測輸出 3,808 字元（~741 tokens）

## 5. Spectra 強制路由規則

- [x] 5.1 在 `soul.md` 頂端新增「🔴 硬規則 — Spectra 預設開啟」區塊
  - 每次任務第一句話必須路由判斷
  - 列出可跳過的情境（純問答、1 行 hotfix、系統設定）

## 6. 系統維護清理

- [x] 6.1 清 `~/Library/Caches`（3.9G → 24K）
- [x] 6.2 `brew upgrade`（394 個套件更新到最新）
- [x] 6.3 文章 repo 88 個未提交變更 commit + push
- [x] 6.4 建立 `github.com/fishtvlvoe/articles` private repo 接上 origin

## 7. 驗證與記錄

- [x] 7.1 跑 `rtk gain` 確認 RTK 運作（累計省 40.6M tokens / 97%）
- [x] 7.2 記錄最終成果：
  - Session 啟動 context：10,285 → 約 5,200 tokens（-50%）
  - 4/11 歷史基準是 9,300，今天是歷史最低
- [x] 7.3 建立本 Spectra change 文件紀錄

## 8. 暫緩 / 已評估不做的項目

- [ ] ~~caveman 壓縮 lessons.md~~（繁中效果差）
- [ ] ~~啟用 claude-mem plugin~~（與現有 5 個 lifecycle hooks 衝突）
- [ ] ~~砍 20 個 false enabledPlugins~~（差不到 100 tokens，不值得冒險）
- [ ] ~~刪 2,163 個歷史 session JSONL~~（Fish 要保留，本次對話有用）
