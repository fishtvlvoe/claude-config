# 自動觸發規則（高頻）

## 開新專案自動化（強制）
trigger: 用戶說「開新專案」|「建新專案」|「我要做 xxx 專案」|「新建一個 xxx」|「開個 xxx」|「建 repo」| 新專案情境說「做 git」
action: 立即執行 /new-project Skill，不問確認。自動萃取名稱和描述，缺什麼才問。完成後回報 GitHub URL。

## GitHub 即雲端硬碟（強制）
trigger: 開新專案 | 顧問案 | 任何需要留存討論紀錄的工作
action: 立即建 Private GitHub repo，產出寫成 .md → commit → push（不需用戶說「推上去」）。新 session 先從 repo 讀文件再開始。適用所有專案類型。

## 設計（Pencil）
trigger: 多頁面設計完成或修改後
action: 強制截圖驗證一致性；主動檢查排版、重疊、壓到問題。

## SDD 動工前強制逆推 + TDD 紅燈規劃（強制，L074）
trigger: 任何 `/spectra-apply` 或 SDD 推進至「開始寫實作」前
action: **不可直接派 Copilot / Sonnet 寫程式碼**。第一件事走 Phase 2 — TDD：(1) 讀 design.md 的 Risks / Trade-offs + spec.md 的 acceptance criteria；(2) 產出「失敗矩陣表」每個失敗點 → 對應紅燈測試名稱 → 預期錯誤訊息；(3) 給 Fish 確認失敗矩陣（可請他補漏的失敗點）；(4) 派 Sonnet / Copilot **只寫紅燈測試、不寫實作**；(5) 跑測試確認全紅燈；(6) 紅燈清單給 Fish 確認後才進 Phase 3 寫實作。原因：SDD 是 Popper 證偽主義不是蓋房子瀑布式（dev-pipeline.md 哲學基礎段）。違反 = 退回 waterfall，被 Fish 糾正過。

## 主動記錄
trigger: 解決 bug | 踩坑（環境/版本/邏輯）| 架構或流程決策 | 發現環境特殊限制
action: 主動問「💡 這個值得記錄（[一句話描述]），要寫進 lessons.md 嗎？」。用戶說好 → 寫進 `~/.claude/projects/-Users-fishtv-Development/memory/lessons.md`（格式：問題→根因→解法→教訓→來源）。

## 60% 主動 Compact
trigger: context 用量達 60%（約 600K tokens）
action: 主動建議執行 /compact，附上應保留的關鍵上下文摘要。不等 auto-compact（95% 觸發時品質已劣化）。

## 離開前 Compact 提醒
trigger: 用戶說要離開、休息、等一下回來、或對話明顯暫停
action: 提醒「prompt cache TTL：Max 訂閱 1 小時、其他 5 分鐘。超過 TTL 回來後全額重建（125%）。長時間離開建議先 /compact 或 /clear」。只提醒一次。

## Context 耗盡警告
trigger: 收到 CONTEXT MONITOR WARNING（35%）或 CONTEXT MONITOR CRITICAL（25%）
action: 告知 context 用量 → 列出本次對話重要事項 → 問是否記錄 → 用戶說好則寫進 lessons.md。

## today.md 輕量日誌
trigger: session 開始 → Read memory/today.md，日期不是今天則清空並更新日期標題。
trigger: 任務完成 | git commit | session 結束 → 追加一行摘要（格式：`- 做了什麼`）。today.md 只記當天，歷史靠 claude-mem。

## Session 長度提醒
trigger: assistant turns 超過 30 次（目測對話已經很長）
action: 提醒用戶「這個 session 已經很長了，建議 /交接 + /clear 開新 session，避免 context 膨脹推高 Opus 成本」。只提醒一次。

## Spectra config.yaml 前置檢查（強制）
trigger: 執行 `/spectra-propose` | `/spectra-discuss` | `/spectra-ingest` | 任何 Spectra 工作流開始前
action: 先讀 `openspec/config.yaml`，檢查是否同時有 `context:` 和 `rules:` 且內容非空（非註解模板）。缺任一 → 先補齊 config.yaml 再繼續 Spectra 流程。補齊方式：讀專案的 CLAUDE.md / package.json / README 取得產品定位和 Tech Stack，rules 段落複製 22-AIRE 範本（`/Users/fishtv/Development/22-AIRE/openspec/config.yaml`）再依專案特性調整。完成後告知用戶「config.yaml 已補齊」再進 Spectra。

## 核心 Skills 同步提醒
trigger: 修改了以下任一 skill 並 commit：分配、dp、debug-buygo、deploy、token-report、ssc、tdd
action: 提醒「💡 核心 skill 已更新，要同步到 claude-config/skills-snapshot/ 嗎？」。用戶說好 → 執行 `cp -r Development/.claude/skills/<skill名> ~/.claude/skills-snapshot/` → commit + push claude-config repo。
