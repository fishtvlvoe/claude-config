# lessons-spectra.md — Spectra / SDD 工作流踩坑

> 載入時機：執行任何 `/spectra-*` skill 前、SDD apply、ingest、archive。
> 核心通則見 `~/.claude/lessons.md`。

| # | 規則 | 觸發情境 |
|---|------|---------|
| L026 | Spectra Propose 第 8 步（Inline Self-Review）時檢查 Consistency：每個 design.md 的決策都要在 tasks.md 中被引用，當場修正，不等分析器發現 | Spectra propose 工作流 |
| L027 | Spectra Apply 開始前，必須先做任務分工分析（哪些任務給哪個工具：Copilot/Kimi/Codex/Sonnet），給用戶確認後才開始執行。禁止擅自用自己的 token 跑多任務。 | Spectra apply 工作流 |
| L028 | 所有開發任務必須建立 Spectra Change（propose/debug），不允許只存在對話紀錄。執行完才標 [x]，流程：propose→analyze→apply（分配 Agent）→結果回 Sonnet 審核→需 debug 再開新 Change。這是標準 SDD Loop，無例外。 | 工作流程 |
| L037 | 「取消訂單」需求必須先問清楚：是取消整筆訂單（父訂單 status→cancelled）還是取消訂單內的某個商品行（對應子訂單 cancelChildOrder）。兩者完全不同，不可憑字面假設。 | Spectra propose 需求釐清 |
| L059 | 任何 Spectra 工作流（propose / ingest / debug）寫完或更新 artifacts 後，MUST 自動跑 `spectra analyze` 並修復全部四個維度（Coverage/Consistency/Ambiguity/Gaps）到 0 findings 才能進 validate。所有等級（Critical/Warning/Suggestion）都要修，不分類跳過。**本規則覆蓋 spectra-propose skill 第 9 步**（skill 寫「只修 Critical/Warning、2 次後放棄」— 不適用，以本規則為準）。不限迭代次數，直到 Total: 0。禁止：(1) 任何 finding 殘留就說「完成」；(2) 不跑 analyze 就直接 validate；(3) 自行判斷「這個可以跳過」；(4) 以「skill 指示」為由跳過 Suggestion。 | 任何 Spectra 工作流完成後 |
| L066 | Spectra skill 一律用 dash 格式 `spectra-propose`，禁止用 colon 格式 `spectra:propose`。Skills 列表同時有兩組（dash = 實體 skill 檔案，colon = plugin namespace 自動註冊），colon 版會報 Unknown skill 錯誤。 | Spectra skill 呼叫 |
| L067 | Spectra 工作流開始前 MUST 先檢查 `openspec/config.yaml` 是否有 `context:` + `rules:` 且內容非空。空模板（只有註解）= 不合格。缺任一 → 先讀專案 CLAUDE.md / package.json / README 取得產品定位和 Tech Stack，rules 段落以 22-AIRE 為範本再依專案特性調整。範本位置：`/Users/fishtv/Development/22-AIRE/openspec/config.yaml`。 | Spectra 工作流前置 |
| L070 | OPCOS 底下所有產品的 SDD 計畫 MUST 自動納入「UI + UX 統一規格」，不用 Fish 提醒。寫 OPCOS 系產品的 propose 時自動加：**(A) UI 視覺統一** — capability `ui-design-system`（共用 design tokens、各自寫元件、icon 統一 lucide-react、字型 Noto Sans TC + Inter）；**(B) UX 互動統一** — capability `ux-interaction-patterns`（表單草稿自動儲存、錯誤訊息語氣、loading/empty/error 三態、確認對話框、鍵盤快捷鍵、Toast 行為、空狀態提示）；**(C) tasks** 加 6 個：抽 token + 設定字型/icon + 寫 atomic 元件 + 視覺對齊驗收 + UX pattern 文件化（`docs/ux-patterns.md`）+ UX 互動驗收。例外：純後端服務（無 UI）不適用。 | OPCOS 系產品 SDD propose |
