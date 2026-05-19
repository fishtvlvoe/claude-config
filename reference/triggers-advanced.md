# 自動觸發規則（低頻 / 按需 Read）

> 高頻硬規則 → `~/.claude/rules/triggers.md`
> 本檔放：UI 工具、Compact 提醒、日誌、Session 管理、Skills 同步

## 設計（Pencil）
trigger: 多頁面設計完成或修改後
action: 強制截圖驗證一致性；主動檢查排版、重疊、壓到問題。

## 離開前 Compact 提醒
trigger: 用戶說要離開、休息、等一下回來、或對話明顯暫停
action: 提醒「prompt cache TTL：Max 訂閱 1 小時、其他 5 分鐘。超過 TTL 回來後全額重建（125%）。長時間離開建議先 /compact 或 /clear」。只提醒一次。

## today.md 輕量日誌
trigger: session 開始 → Read memory/today.md，日期不是今天則清空並更新日期標題。
trigger: 任務完成 | git commit | session 結束 → 追加一行摘要（格式：`- 做了什麼`）。today.md 只記當天，歷史靠 claude-mem。

## Session 長度提醒
trigger: assistant turns 超過 30 次（目測對話已經很長）
action: 提醒用戶「這個 session 已經很長了，建議 /交接 + /clear 開新 session，避免 context 膨脹推高 Opus 成本」。只提醒一次。

## 核心 Skills 同步提醒
trigger: 修改了以下任一 skill 並 commit：分配、dp、debug-buygo、deploy、token-report、ssc、tdd
action: 提醒「💡 核心 skill 已更新，要同步到 claude-config/skills-snapshot/ 嗎？」。用戶說好 → 執行 `cp -r Development/.claude/skills/<skill名> ~/.claude/skills-snapshot/` → commit + push claude-config repo。

## 主動記錄（中頻）
trigger: 解決 bug | 踩坑（環境/版本/邏輯）| 架構或流程決策 | 發現環境特殊限制
action: 主動問「💡 這個值得記錄（[一句話描述]），要寫進 lessons.md 嗎？」。用戶說好 → 寫進 `~/.claude/lessons.md`（格式：問題→根因→解法→教訓→來源）。
