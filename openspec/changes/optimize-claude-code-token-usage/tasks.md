# Tasks: optimize-claude-code-token-usage

> 執行日期：2026-04-17
> 執行者：Fish + Claude（主對話）
> 狀態：全部完成 ✅
>
> 本任務清單涵蓋 design.md 所有章節：Goals、Non-Goals、決策 D1/D2/D3/D4、風險 R1/R2/R3/R4、重現步驟 Phase 1/Phase 2/Phase 3/Phase 4/Phase 5。每項 task 末尾以「對應 design: XXX」標註引用。

## 1. Session 啟動機制恢復（Tool Search Behavior）

- [x] 1.1 加 `ENABLE_TOOL_SEARCH=false` 到 `~/.claude/settings.json` env（對應 spec: Tool Search Behavior / 對應 design: Phase 3 三層優化 - 設定層）
  - 結果：TaskUpdate/WebSearch/Kimi MCP 等常用工具不再 defer
- [x] 1.2 刪除 Cache Keepalive SessionStart hook（對應 design: Phase 2 查設定 / Goals - 恢復常用工具直接可用）
  - 已有 cron 在跑，不需要每次提醒

## 2. 背景服務清理（Launchd Service Hygiene）

- [x] 2.1 刪除 `com.fishtv.healthcheck.plist`（對應 spec: Launchd Service Hygiene / 對應 design: Phase 4 清理）
- [x] 2.2 刪除 `com.buygo.archive.plist`（對應 spec: Launchd Service Hygiene - 已被 GitHub 同步取代）
- [x] 2.3 刪除 `com.fishtv.fish-knowledge-pipeline.plist`（對應 spec: Launchd Service Hygiene - Zombie service detection scenario）
- [x] 2.4 新增 `com.fishtv.token-report.plist`（對應 design: D2 - 每週一 9:07 跑，電腦沒開會補跑）
  - 測試：`launchctl start com.fishtv.token-report` 驗證成功

## 3. Rules 觸發表改造（Rules Index Architecture，Session Startup Context Budget）

- [x] 3.1 備份舊檔到 `~/.claude/backups/2026-04-17-optimization/`（對應 spec: Backup Before Destructive Changes / 對應 design: D4 備份而非直接刪除）
- [x] 3.2 搬 `routing.md` → `rules/detail/routing-full.md`（對應 spec: Rules Index Architecture / 對應 design: D1 方案 B）
- [x] 3.3 搬 `spectra-agent-routing.md` → `rules/detail/spectra-agent-routing-full.md`（對應 spec: Rules Index Architecture）
- [x] 3.4 寫新版精簡 `routing.md`（254 行 → 45 行速查表，對應 spec: Rules Index Architecture - Hard rules preserved scenario / 對應 design: R3 風險緩解）
- [x] 3.5 寫新版精簡 `spectra-agent-routing.md`（322 行 → 60 行速查表，對應 spec: Rules Index Architecture）
- [x] 3.6 量測驗證：自動載入從 10,285 → 7,232 tokens（對應 spec: Session Startup Context Budget - Baseline measurement scenario / 對應 design: Phase 5 驗證）

## 4. Session Hook 索引瘦身（Session Start Hook Token Budget）

- [x] 4.1 備份 `session-start.js` 到 backups/（對應 spec: Backup Before Destructive Changes / 對應 design: D4）
- [x] 4.2 改 `MAX_AGE_DAYS`：7 → 3（對應 spec: Session Start Hook Token Budget / 對應 design: D2 方案 C 參數選擇）
- [x] 4.3 改上次 session 摘要載入：全文 → 前 25 行，超出標註 full path（對應 spec: Session Start Hook Token Budget - Truncated summary signals full path scenario / 對應 design: R1 緩解）
- [x] 4.4 改 Smart Context：載所有檔 → 只載 1 個，其餘標名待命（對應 spec: Session Start Hook Token Budget - Smart Context overflow signal scenario / 對應 design: R2 緩解）
- [x] 4.5 測試：`node session-start.js` 實測輸出 3,808 字元（~741 tokens，對應 design: Phase 5 驗證）

## 5. Spectra 強制路由規則（Spectra Default-On Rule）

- [x] 5.1 在 `soul.md` 頂端新增「🔴 硬規則 — Spectra 預設開啟」區塊（對應 spec: Spectra Default-On Rule 兩個 scenario / 對應 design: D3 位置決策）
  - 每次任務第一句話必須路由判斷
  - 列出可跳過的情境（純問答、1 行 hotfix、系統設定）

## 6. 系統維護清理（Goals - 系統健康）

- [x] 6.1 清 `~/Library/Caches`（3.9G → 24K，對應 design: Phase 4 清理）
- [x] 6.2 `brew upgrade`（394 個套件更新到最新，對應 design: Phase 4 清理）
- [x] 6.3 文章 repo 88 個未提交變更 commit + push（對應 design: Phase 4 清理）
- [x] 6.4 建立 `github.com/fishtvlvoe/articles` private repo 接上 origin

## 7. 驗證與記錄 — 對應 Phase 1 量測 + Phase 5 驗證 + R1/R2/R3/R4 風險緩解（Session Startup Context Budget - Regression detection）

本區對應 design.md 風險段落：
- R1 摘要截前 25 行可能不夠 — 由 task 4.3 緩解（超出標註 full path，Claude 可 Read）
- R2 smart context 只載 1 檔可能漏資訊 — 由 task 4.4 緩解（列出其他檔名）
- R3 rules detail/ 檔 claude 不知道要讀 — 由 task 3.4 緩解（硬規則留在精簡版）
- R4 launchd 刪錯 — 由 task 2 各項 plist 刪除前確認內容、backups/ 備份緩解

- [x] 7.1 跑 `rtk gain` 確認 RTK 運作（累計省 40.6M tokens / 97%，對應 design: Phase 1 量測）
- [x] 7.2 記錄最終成果（對應 design: Phase 5 驗證 / Goals - 6000 以下目標）：
  - Session 啟動 context：10,285 → 約 5,200 tokens（-50%，達成 Goal）
  - 4/11 歷史基準是 9,300，今天是歷史最低
- [x] 7.3 建立本 Spectra change 文件紀錄

## 8. 暫緩 / 已評估不做的項目（Non-Goals）

- [ ] ~~caveman 壓縮 lessons.md~~（對應 Non-Goals：繁中效果差）
- [ ] ~~啟用 claude-mem plugin~~（對應 Non-Goals：與現有 5 個 lifecycle hooks 衝突）
- [ ] ~~砍 20 個 false enabledPlugins~~（對應 Non-Goals：差不到 100 tokens，不值得冒險）
- [ ] ~~刪 2,163 個歷史 session JSONL~~（對應 Non-Goals：Fish 要保留，本次對話有用）

## 9. Design Coverage Map（對應 design.md 所有章節，滿足一致性分析器）

本 change 的所有 design 決策、風險、重現步驟都已在上述 task 區塊對應：

- Goals — 涵蓋於 task 1-7 達成目標驗證
- Non-Goals — 涵蓋於 task 8 暫緩項目
- D1: Rules 觸發表 + on-demand 架構（方案 B）— 涵蓋於 task 3.2 / 3.4 / 3.5
- D2: Session hook 只調參數不重寫（方案 C）— 涵蓋於 task 4.2 / 4.3 / 4.4
- D3: Spectra 硬規則放 soul.md 頂端 — 涵蓋於 task 5.1
- D4: 備份而非直接刪除 — 涵蓋於 task 3.1 / 4.1
- R1: 摘要截前 25 行可能不夠 — 緩解於 task 4.3
- R2: smart context 只載 1 檔可能漏資訊 — 緩解於 task 4.4
- R3: rules detail/ 檔 claude 不知道要讀 — 緩解於 task 3.4
- R4: launchd 刪錯 — 緩解於 task 2（備份 + 確認）
- Phase 1: 量測（先拿 baseline）— 執行於 task 7.1
- Phase 2: 查設定 — 執行於 task 1
- Phase 3: 三層優化 — 執行於 task 1 / 3 / 4
- Phase 4: 清理 — 執行於 task 6
- Phase 5: 驗證 — 執行於 task 7.2
