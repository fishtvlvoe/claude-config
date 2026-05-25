# lessons-spectra.md — Spectra / SDD 工作流踩坑

> 載入時機：執行任何 `/spectra-*` skill 前、SDD apply、ingest、archive。
> 核心通則見 `~/.claude/lessons.md`。

| # | 規則 | 觸發情境 |
|---|------|---------|
| L026 | Spectra Propose 第 8 步（Inline Self-Review）時檢查 Consistency：每個 design.md 的決策都要在 tasks.md 中被引用，當場修正，不等分析器發現 | Spectra propose 工作流 |
| L027 | Spectra Apply 開始前，必須先做任務分工分析（哪些任務給哪個代理：Codex CLI / Sonnet 子代理 / Kimi MCP），給用戶確認後才開始執行。禁止擅自用自己的 token 跑多任務。 | Spectra apply 工作流 |
| L028 | 所有開發任務必須建立 Spectra Change（propose/debug），不允許只存在對話紀錄。執行完才標 [x]，流程：propose→analyze→apply（分配 Agent）→結果回 Sonnet 審核→需 debug 再開新 Change。這是標準 SDD Loop，無例外。 | 工作流程 |
| L037 | 「取消訂單」需求必須先問清楚：是取消整筆訂單（父訂單 status→cancelled）還是取消訂單內的某個商品行（對應子訂單 cancelChildOrder）。兩者完全不同，不可憑字面假設。 | Spectra propose 需求釐清 |
| L059 | 任何 Spectra 工作流（propose / ingest / debug）寫完或更新 artifacts 後，MUST 自動跑 `spectra analyze` 並修復全部四個維度（Coverage/Consistency/Ambiguity/Gaps）到 0 findings 才能進 validate。所有等級（Critical/Warning/Suggestion）都要修，不分類跳過。**本規則覆蓋 spectra-propose skill 第 9 步**（skill 寫「只修 Critical/Warning、2 次後放棄」— 不適用，以本規則為準）。不限迭代次數，直到 Total: 0。禁止：(1) 任何 finding 殘留就說「完成」；(2) 不跑 analyze 就直接 validate；(3) 自行判斷「這個可以跳過」；(4) 以「skill 指示」為由跳過 Suggestion。 | 任何 Spectra 工作流完成後 |
| L066 | Spectra skill 一律用 dash 格式 `spectra-propose`，禁止用 colon 格式 `spectra:propose`。Skills 列表同時有兩組（dash = 實體 skill 檔案，colon = plugin namespace 自動註冊），colon 版會報 Unknown skill 錯誤。 | Spectra skill 呼叫 |
| L067 | Spectra 工作流開始前 MUST 先檢查 `openspec/config.yaml` 是否有 `context:` + `rules:` 且內容非空。空模板（只有註解）= 不合格。缺任一 → 先讀專案 CLAUDE.md / package.json / README 取得產品定位和 Tech Stack，rules 段落以 22-AIRE 為範本再依專案特性調整。範本位置：`/Users/fishtv/Development/22-AIRE/openspec/config.yaml`。 | Spectra 工作流前置 |
| L070 | OPCOS 底下所有產品的 SDD 計畫 MUST 自動納入「UI + UX 統一規格」，不用 Fish 提醒。寫 OPCOS 系產品的 propose 時自動加：**(A) UI 視覺統一** — capability `ui-design-system`（共用 design tokens、各自寫元件、icon 統一 lucide-react、字型 Noto Sans TC + Inter）；**(B) UX 互動統一** — capability `ux-interaction-patterns`（表單草稿自動儲存、錯誤訊息語氣、loading/empty/error 三態、確認對話框、鍵盤快捷鍵、Toast 行為、空狀態提示）；**(C) tasks** 加 6 個：抽 token + 設定字型/icon + 寫 atomic 元件 + 視覺對齊驗收 + UX pattern 文件化（`docs/ux-patterns.md`）+ UX 互動驗收。例外：純後端服務（無 UI）不適用。 | OPCOS 系產品 SDD propose |
| L040 | SDD 任務執行中，不需要用戶判斷的步驟（測試通過、build 通過、commit、下一個 Wave）MUST 自動往下走，不等指令。只有以下情況才停下來等用戶：重大架構決策、需要外部資料（客戶提供）、代理全部失敗無法繼續。每個 Wave 完成後主動回報進度摘要（做了什麼、結果如何、下一步是什麼）。 | SDD 執行期間 |
| L071 | 派外部代理做 SDD apply 前，MUST 先確認 SDD 路徑與工作 git repo 對齊：(1) `cd` 到目標目錄；(2) `git remote -v` 確認 origin 是 Fish 自己的 repo，不是上游 fork；(3) 確認 `git rev-parse --show-superproject-working-tree` 無輸出（不在 submodule 內）；任一檢查失敗 = 停下、改路徑或重 propose。 | 派代理跑 SDD apply 前 |
| L074 | **SDD 是程式設計版的 Popper 證偽主義，不是蓋房子瀑布式**。動工順序：propose（提出假說）→ 逆推失敗點 → 寫紅燈測試把每個失敗點具體化（Phase 2 — TDD，不可跳）→ 紅燈成立 → 才派 Sonnet 子代理 / Codex CLI 寫實作讓紅變綠 → 紅燈不過時 ingest 改 propose（Quine-Duhem 理論修正循環）。禁止「先 apply 看實物再回頭修圖」（waterfall 反模式）。禁止用「蓋房子」比喻 SDD。 | 任何 SDD 動工前 |
| L079 | **寫代碼前 / spectra-apply 前 MUST 跑 cross-impact 分析（A 壞 B 預檢）**。Fish 多次反映：以前修 A 常常把 B 弄壞。觸發：spectra-propose 完成、spectra-apply 開跑前、或直接動程式碼前。動作：派 Sonnet/Haiku 子代理 grep 所有受影響 API/function/DB 表/欄位的 caller 與 consumer，輸出 ABCDEFG 分類報告，每段標 ✅ 無影響 / ⚠️ 需注意 / 🔴 高風險。報告寫到 `/tmp/cross-impact-<change>.md` 給用戶 review。發現 🔴 → STOP，回頭擴大 change 範圍或補對策進 design.md，**禁止硬上**；發現 ⚠️ → 把細節補進 tasks.md 寫成明文步驟，不是嘴上講過去。**補強規則（2026-05-16）**：改任何 REST API 行為前 MUST 先從前端往後 trace — `grep "fetch.*<endpoint>"`、`grep "/<resource>/"` 在 `includes/views/`、`admin/js/`、`admin/partials/` 找實際被打的 URL → 對應後端 handler → 改對 handler。光看 service method caller 不夠。 | spectra-apply 前 / 任何寫代碼前 |

## 變更歷程

- 2026-05-19: 從 lessons.md 收 L040 / L071 / L074 / L079（SDD 執行 / 路徑檢查 / Popper 哲學 / cross-impact 預檢）
