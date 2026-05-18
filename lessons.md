# lessons.md — 被糾正的規則（核心 / 跨專案）

> 每次被 Fish 糾正 → 當場更新這裡。
> session 開始時讀這個，避免重複犯同樣的錯。
> 領域別 lessons 不在這裡，按需 Read：
> - `~/.claude/lessons-spectra.md` — Spectra / SDD 工作流
> - `~/.claude/lessons-web-deploy.md` — CSS / Vercel / Supabase / rsync / Postgres
> - `~/.claude/lessons-frontend.md` — React / Next / iOS / Chrome / Vite
> - `~/.claude/lessons-products.md` — BuyGo / huashu / three-ai 等專案專屬

## 規則速查表（核心通用）

| # | 規則 | 觸發情境 |
|---|------|---------|
| L016 | 說「X 不能用」前必須先 `which X` 確認。已知：copilot/gemini/cursor/kimi/codex 都可用 | 工具可用性 |
| L018 | 遇阻靜默試 B/C/D，全部失敗才回報，禁止中途打斷用戶 | 工具失敗 |
| L019 | UI 按鈕/圖示一律用 SVG icon（Heroicons/Lucide），禁止 Emoji | UI 設計 |
| L020 | 不確定的事自己查完再說話，禁止叫用戶「試試看」代勞驗證 | Debug |
| L021 | Bug 流程：蒐集線索→列原因→工具逐一排除→確定根因→一次修復→自驗→才告知 | Debug |
| L023 | 任何「需要重複改同一件事」的操作，必須自動化完成，不問用戶 | 自動化原則 |
| L031 | 大檔案（>100 行）用 Grep 定位行號，再用 Read offset/limit 只讀需要的段落，不要整個讀進來 | 讀檔效率 |
| L032 | 自動化腳本失敗後 MUST 先記錄實際狀態（期望找到什麼 vs 實際找到什麼）到 log，才決定是否重試，不得用同樣邏輯盲目 retry | 自動化 debug |
| L034 | 任何擴展點（include/hook/slot）用前 MUST 先查文件確認正確名稱，不猜檔名 | 平台整合 |
| L035 | 建 repo 後第一件事：.gitignore、LICENSE、README；依賴管理檔 MUST 固定版本，不要先寫內容再補基礎設施 | 專案初始化 |
| L036 | 加任何平台設定前先確認目標平台版本和限制（如 GitHub Pages 用 Jekyll 3.10 不是 Jekyll 4），不確定就查官方文件 | 平台版本確認 |
| L039 | 每個階段完成後，MUST 主動告知下一步是什麼、需要用戶做什麼決定，不能做完就停在那裡等問。格式：「下一步是 X，需要你 Y，我的判斷是 Z，你要繼續嗎？」 | 任何任務完成後 |
| L040 | SDD 任務執行中，不需要用戶判斷的步驟（測試通過、build 通過、commit、下一個 Wave）MUST 自動往下走，不等指令。只有以下情況才停下來等用戶：重大架構決策、需要外部資料（客戶提供）、代理全部失敗無法繼續。每個 Wave 完成後主動回報進度摘要（做了什麼、結果如何、下一步是什麼）。 | SDD 執行期間 |
| L041 | 禁止叫 Fish 開瀏覽器操作任何事情。瀏覽器操作一律用 agent-browser MCP 或 gh CLI 自己完成。唯一例外：需要 Fish 親自授權的事（貼 API Key、2FA、付費操作、手動 Webhook 授權）。違反 = 白工。 | 任何需要瀏覽器的操作 |
| L045 | UI 任務（HTML 原型、React 元件、CSS 改動）commit 前 MUST 跑視覺驗證：用 playwright/chrome MCP 截圖每個畫面或狀態 → 主對話 Read 截圖確認渲染對 → 錯誤就退回 Agent 改。**禁止**「Agent 回報完成 + grep 字串存在」就 commit。理由：字面驗證 ≠ 行為驗證，HTML 結構正確不代表瀏覽器渲染對。 | 任何 UI 任務 commit 前 |
| L046 | 派工給 cursor-agent / Sonnet 子代理做 UI 時，prompt 結尾 MUST 加：「完成後用 playwright 截圖每個畫面/狀態存到 /tmp/，把路徑列出，不要說『完成』，說『截圖在 X 請主對話驗證』」。沒附截圖證據 = 退回重做。 | 派工 UI 任務時 |
| L049 | 派工給 Copilot CLI（`copilot --yolo`）時，MUST 加 `--add-dir src/` 限制只能動 src 目錄。`--yolo` 模式下 Copilot 有完整寫/刪權限，會動到 openspec/、.claude/、.agent/ 等非代碼目錄。正確呼叫：`copilot --yolo --add-dir src/ --model gpt-5.2 -p @prompt.txt` | Copilot CLI 派工 |
| L050 | 派任何外部代理（Copilot CLI / Sonnet 子代理）前，MUST 跑 `git status` 檢查 untracked 的重要檔案；有則先 `git add openspec/ .claude/ docs/ && git commit -m "wip: pre-dispatch checkpoint"` 才派工。`--add-dir src/` 只限制「主動編輯」範圍，不限制 bash 指令；Copilot --yolo 會跑 `git restore` / `git clean -fd` 把 untracked 檔案永久刪除（unlink，git reflog 也救不回）。prompt MUST 用白名單：「只允許跑 npm test、git status、git diff，禁止任何其他 git 指令（特別是 clean、restore、reset、checkout）」。 | 派工外部代理前 |
| L053 | L050 補強：Copilot CLI 即使加 `--add-dir`，看到 `git diff --stat` 出現「跟我這個任務無關的檔案」就會自作主張 restore 它們。真正的防護：每個 Wave 結束就 `git add -A && git commit -m "wip: ..."`，不留 untracked / modified 給下個 Wave；prompt 結尾明文「只允許 `git diff --stat` `git diff` `git status`，禁止 `git restore` `git checkout` `git clean` `git reset`」。 | Copilot CLI 派工 |
| L069 | 派 Kimi CLI 寫碼前 MUST 防護 SDD 檔案。Kimi CLI 沒有排除目錄的 flag，`-w` 設工作目錄 = 它能動的全部範圍。SOP：(1) 派工前 `git add openspec/ .claude/ && git commit -m "wip: pre-kimi checkpoint"`；(2) `-w` 只指向程式碼目錄（如 `-w src/`），不指向專案根目錄；(3) prompt 結尾加禁令：「只修改程式碼檔案，禁止動 openspec/、.claude/、docs/」；(4) 派工後 `git diff --stat` 檢查。**`--add-dir` 是「擴展」scope 不是「限制」**。 | Kimi CLI 派工 |
| L071 | 派外部代理做 SDD apply 前，MUST 先確認 SDD 路徑與工作 git repo 對齊：(1) `cd` 到目標目錄；(2) `git remote -v` 確認 origin 是 Fish 自己的 repo，不是上游 fork；(3) 確認 `git rev-parse --show-superproject-working-tree` 無輸出（不在 submodule 內）；任一檢查失敗 = 停下、改路徑或重 propose。 | 派代理跑 SDD apply 前 |
| L074 | **SDD 是程式設計版的 Popper 證偽主義，不是蓋房子瀑布式**。動工順序：propose（提出假說）→ 逆推失敗點 → 寫紅燈測試把每個失敗點具體化（Phase 2 — TDD，不可跳）→ 紅燈成立 → 才派 Copilot / Sonnet 寫實作讓紅變綠 → 紅燈不過時 ingest 改 propose（Quine-Duhem 理論修正循環）。禁止「先 apply 看實物再回頭修圖」（waterfall 反模式）。禁止用「蓋房子」比喻 SDD。 | 任何 SDD 動工前 |
| L075 | 派工 CLI 代理前 MUST 用正確模型參數。已驗證預設：Copilot CLI → `gpt-5.2`、Codex CLI → `gpt-5.3-codex`（ChatGPT 帳號不支援 `o4-mini`/`o4`）、Kimi CLI → 內建預設。錯誤模型名會導致 CLI 直接報錯退出，非互動模式下看起來像「靜默失敗」。 | CLI 代理派工 |
| L076 | Agent tool call 的 XML 參數值內禁止插入任何描述文字。錯誤：`<parameter name="subagent_type">general-purpose</parameter>(讀截圖...)\n<parameter name="model">haiku`。parser 會把 `</parameter>` 之後的文字全吞進前一個參數值。派工說明只能寫在 tool call 之外的文字輸出裡，不能夾在 XML 標籤之間。 | Agent tool call XML 格式 |
| L077 | **程式碼風格衝突時必須明說選哪一種**，不要「兩邊都用、混在一起」。觸發：同個 codebase 看到兩種風格（例：camelCase vs snake_case、tab vs space、early-return vs nested-if）→ 必須先看哪種佔多數或先看 .editorconfig/prettier 設定，跟著佔多數的走；無法決定時直接問用戶「A 還是 B？」。禁止：「為了相容性兩個都保留」、「這檔案用 A 那檔案用 B」式的悄悄混用。理由：Karpathy 規則 7，模型平均化策略會讓 codebase 風格腐爛。 | 任何寫碼任務開始前 |
| L078 | **長任務每完成一個邏輯子步驟 MUST 建存檔點**（`git add -A && git commit -m "wip: <子步驟>"`），不依賴對話 history 當備份。觸發：超過 3 個子步驟的任務、跨 Wave 的 SDD、需要派多次外部代理的工作。理由：(1) 對話被 compact 或 session 換手時，未 commit 的工作會丟；(2) 派外部代理踩 L050/L053 坑會把 untracked 工作 git clean 掉；(3) 用戶中途要看「目前做到哪」可以 `git log --oneline` 看。一個子步驟做完不 commit 就不算開始下一步。 | 多步任務每個子步驟結束 |
| L080 | Fish 說「sr」= Spectra SDD 專案（sr = spectra 的縮寫） | 任何對話 |
| L081 | **驗證 = 實際跑出結果，不是 build 通過**。任何功能完成後 MUST 自己做行為驗證：(1) 寫 Node 腳本用假資料呼叫函式 → 產出實際檔案（PDF/JSON/圖片）存 `/tmp/`；(2) 或 `cargo tauri dev` / `npm run dev` 跑起來 → Chrome MCP 操作 UI → 截圖每個畫面；(3) 或 curl/fetch 打 API 確認回傳格式正確。**build 通過 ≠ 功能正確**。禁止只跑 build 就回報「完成」；禁止說「需要你自己跑一次確認」把驗證丟回 Fish — 那是我做得到的事。截圖/輸出檔存 `/tmp/` 供 Fish 檢視。違反 = 白工 + 信任歸零。 | 任何功能完成回報前 |
| L082 | **理解 UI 結構用 DOM/HTML，不用截圖**。截圖 = 圖片 token（每張 ~1500 tokens）+ 「看圖說話」再產文字 = 雙倍浪費。讀 HTML/DOM（`read_page`、`get_page_text`、`javascript_tool` 抓 computed style）= 純文字 token，直接得到 class、px、hex、font-size、佈局，一次到位且精確度更高。鐵律：**給人看的是圖形介面，給 AI 看的是 0 與 1 的介面**。截圖只用於最終視覺驗證（L045），分析結構階段一律讀代碼。 | 任何 UI 偵察/spec 撰寫 |
| L079 | **寫代碼前 / spectra-apply 前 MUST 跑 cross-impact 分析（A 壞 B 預檢）**。Fish 多次反映：以前修 A 常常把 B 弄壞。觸發：spectra-propose 完成、spectra-apply 開跑前、或直接動程式碼前。動作：派 Sonnet/Haiku 子代理 grep 所有受影響 API/function/DB 表/欄位的 caller 與 consumer，輸出 ABCDEFG 分類報告，每段標 ✅ 無影響 / ⚠️ 需注意 / 🔴 高風險。報告寫到 `/tmp/cross-impact-<change>.md` 給用戶 review。發現 🔴 → STOP，回頭擴大 change 範圍或補對策進 design.md，**禁止硬上**；發現 ⚠️ → 把細節補進 tasks.md 寫成明文步驟（例：「合併邏輯第一次見 product 怎麼建、已存在怎麼累加、subItems 內 variation 怎麼分組」這種步驟級規範），不是嘴上講一下就跳過。實際應用範例：fix-shipment-details-expand-variations 預檢抓到 `mergeItemsByProduct` 的 `{...item}` spread 會讓 parent 欄位被最後一筆覆蓋，補進任務 3.1。**補強規則（2026-05-16 hotfix 1.7.12 踩坑後加）：改任何 REST API 行為前 MUST 先從前端往後 trace — `grep "fetch.*<endpoint>" `、`grep "/<resource>/"` 在 `includes/views/`、`admin/js/`、`admin/partials/` 找實際被打的 URL → 對應後端 handler → 改對 handler**。光看 service method caller 不夠，可能 service method 根本沒被 REST endpoint 用到（例如 fix-shipment-details-expand-variations 改了 `/shipments/{id}` 用的 `get_shipment_items`，但前端打的是 `/shipments/{id}/detail` 用 `get_shipment_detail` 獨立 SQL → 部署後子列不顯示 → 開 hotfix v1.7.12 補修 detail endpoint）。 | spectra-apply 前 / 任何寫代碼前 |

| L083 | **supastarter-first（先查底盤，無例外）**。收到任何 SR/SDD 任務，寫代碼前強制前置步驟：(1) 查 `supastarter-nextjs/` 有沒有現成頁面/元件；(2) 查 supastarter.dev 開發文件；(3) 查 `packages/` 12 個共用套件有沒有可用的；(4) 產出「可用資源清單」給 Fish：直接用 / 改一點 / 需新寫；(5) Fish 確認後才動手。**禁止**：跳過查詢直接設計方案。supastarter 是成品底盤，不是參考資料。anismile-bugfix-round2 的 14 個 bug 中 40% 來自沒用底盤現成功能。 | 任何 SR/SDD 動工前 |
| L084 | **reuse-first（先考古再動手，無例外）**。寫任何代碼前強制前置步驟：(1) grep 現有 `apps/` 找類似 pattern；(2) 查同產品或其他產品的 archived changes（已解過的問題）；(3) 確認 API procedure 是否已存在（禁止只做 UI 外殼不接 API）；(4) 主動告訴 Fish：「這些不用做、這些直接用、只有這些要新寫」。**禁止**：從頭寫已有的東西、只做靜態 UI 沒接 API 就標「完成」。 | 任何寫碼任務開始前 |
| L085 | **完整派工 + 自己驗收（不丟球給 Fish，無例外）**。派工時：prompt 必須附 `ui-reference/` 路徑 + spec 路徑 + HTML demo 路徑，明確寫「按照這三份文件實作，不可自由發揮」。測試時：自己用 Chrome MCP 跑完所有頁面 + 讀 console + 截圖，一次跑完、一次報告全部問題 + 建議解法。對話中：重要資訊立刻寫進 spec/design.md，不靠對話記憶。**禁止**：叫 Fish 開瀏覽器/截圖/貼報錯、問 Fish 已回答過的問題。 | 派工/測試/對話中 |

| L090 | **API key / token / endpoint 先查 `.env`，禁止問 Fish**。任何「這個 API 的 key 是什麼？」「你有這個服務的 token 嗎？」問題，MUST 先 `cat .env`（或 `cat .env.local`、`cat .env.production`）自己找答案。找不到才問，且問的時候說明「已查 .env，沒有 X」。這是 L020「不確定的事自己查完再說話」的具體化 — API 憑證永遠先在 .env 找。 | 需要外部 API key 時 |
| L086 | **底層先修，新功能後加（foundation-first，無例外）**。發現 ST 底盤元件與 anismile 自寫版本重疊時，**必須先替換底層元件，才能繼續加新功能**。原因：新功能如果建在自寫版元件上，之後替換底層時會做 A 壞 B——舊自寫版的行為、props 介面、型別定義可能跟 ST 版不同，改了底層新功能就跟著爛。順序：(1) 讀 `docs/st-overlap-analysis.md` 確認所有 ✅ 可直接換掉的項目；(2) 先做全部替換並通過測試；(3) build 乾淨才進新功能。**禁止**：「先快速加新功能，回頭再換底層」。新功能建在錯誤底層 = 雙倍工。 | 有 ST 元件重疊存在時，任何新功能動工前 |

## 變更歷程

- 2026-05-15: 從 61 條拆分為核心 + 4 領域檔案，本檔保留 26 條（24 原 + L077 風格衝突 + L078 存檔點）
- 2026-05-15: 新增 L079 cross-impact 預檢（A 壞 B 預防）
- 2026-05-16: 新增 L080 sr 縮寫
- 2026-05-17: 新增 L081 驗證必須實跑（build≠功能正確，禁止丟回 Fish）
- 2026-05-18: 新增 L083 supastarter-first、L084 reuse-first、L085 完整派工+自己驗收（opcOS 願景討論產出）
- 2026-05-18: 新增 L090 API key/token 先查 .env
