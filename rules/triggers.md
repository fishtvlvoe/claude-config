# 自動觸發規則（高頻硬規則）

> 低頻 trigger（Pencil / Compact 提醒 / today.md / Session 提醒 / Skills 同步） → `Read ~/.claude/rules/triggers-advanced.md`

## 🔴 SDD 動工前強制 TDD 紅燈規劃（L074）
trigger: 任何 `/spectra-apply` 或 SDD 推進至「開始寫實作」前
action: **不可直接派寫程式碼**。Phase 2 TDD：讀 design.md Risks + spec.md acceptance criteria → 產出失敗矩陣表（失敗點 → 紅燈測試名 → 預期錯誤訊息）→ Fish 確認 → 派代理只寫紅燈測試（不寫實作）→ 跑測試全紅燈 → 才進 Phase 3 寫實作。SDD 是 Popper 證偽主義，不是蓋房子瀑布式。

## 🔴 Cross-impact 預檢（A 壞 B 預防，L079）
trigger: 任何 `/spectra-apply` 開跑前 | 直接動程式碼前 | 修改既有 service / API / DB query 前
action: 不可直接動代碼。先派 Sonnet/Haiku 子代理跑 cross-impact 分析：grep 受影響 API/function/DB 表/欄位所有 caller → 分類 ABCDEFG 列表，每段標 ✅ / ⚠️ / 🔴 → 寫到 `/tmp/cross-impact-<change>.md`。🔴 → STOP；⚠️ → 補進 tasks.md 明文步驟。報告給 Fish review 後才進 apply。

## 🔴 功能完成行為驗證（L081）
trigger: 任何 Wave 完成 | spectra-apply 全部 task done | 回報「完成」前
action: 禁止只 build 通過就回報。MUST 實跑：(1) 腳本用假資料產出實際檔案 → `/tmp/`；(2) 或啟動 dev server → Chrome MCP 操作 → 截圖；(3) 或 curl 打 API。沒有實際輸出物 = 沒完成。禁止說「請你手動跑一次」。

## 🔴 supastarter-first 前置檢查（L083）
trigger: 任何 `/spectra-propose` | `/spectra-apply` | 直接寫 SR 代碼前
action: 跑 checklist：(1) 查 `supastarter-nextjs/` 現成功能；(2) 查 supastarter.dev；(3) 查 `packages/` 12 套件；(4) grep `apps/` 既有 pattern + archived changes；(5) 產出「可用資源清單」（直接用 / 改一點 / 需新寫）給 Fish 確認。沒產出清單不准動手。

## Spectra config.yaml 前置檢查
trigger: 執行 `/spectra-propose` | `/spectra-discuss` | `/spectra-ingest` 前
action: 先讀 `openspec/config.yaml`，缺 `context:` 或 `rules:` → 補齊（讀專案 CLAUDE.md / package.json / README），rules 段落複製 22-AIRE 範本（`/Users/fishtv/Development/22-AIRE/openspec/config.yaml`）。

## 開新專案自動化
trigger: 用戶說「開新專案」|「建新專案」|「建 repo」| 新專案情境
action: 立即執行 /new-project，不問確認。自動萃取名稱描述，缺什麼才問。完成後回報 GitHub URL。同時：建 Private GitHub repo，產出寫 .md → commit → push。

## 60% 主動 Compact
trigger: context 用量達 60%（約 600K tokens）
action: 主動建議執行 /compact，附上應保留的關鍵上下文摘要。不等 auto-compact（95% 觸發時品質已劣化）。

## Context 耗盡警告
trigger: 收到 CONTEXT MONITOR WARNING（35%）或 CRITICAL（25%）
action: 告知 context 用量 → 列出本次對話重要事項 → 問是否記錄 → 用戶說好則寫進 lessons.md。
