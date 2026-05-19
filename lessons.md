# lessons.md — 被糾正的規則（核心 / 跨專案）

> 每次被 Fish 糾正 → 當場更新這裡。
> session 開始時讀這個，避免重複犯同樣的錯。
> 領域別 lessons 不在這裡，按需 Read：
> - `~/.claude/lessons-spectra.md` — Spectra / SDD 工作流（L040 / L071 / L074 / L079）
> - `~/.claude/lessons-dev.md` — 派工 / CLI SOP（L049 / L050 / L053 / L069 / L075 / L076 / L078）
> - `~/.claude/lessons-frontend.md` — React / UI 驗證 / Chrome MCP（L019 / L045 / L046 / L082 / L089）
> - `~/.claude/lessons-web-deploy.md` — CSS / Vercel / Supabase / rsync / Postgres
> - `~/.claude/lessons-products.md` — BuyGo / anismile / supastarter / three-ai（L083 / L086）

## 規則速查表（核心通用）

| # | 規則 | 觸發情境 |
|---|------|---------|
| L016 | 說「X 不能用」前必須先 `which X` 確認。已知：copilot/gemini/cursor/kimi/codex 都可用 | 工具可用性 |
| L018 | 遇阻靜默試 B/C/D，全部失敗才回報，禁止中途打斷用戶 | 工具失敗 |
| L020 | 不確定的事自己查完再說話，禁止叫用戶「試試看」代勞驗證 | Debug |
| L021 | Bug 流程：蒐集線索→列原因→工具逐一排除→確定根因→一次修復→自驗→才告知 | Debug |
| L023 | 任何「需要重複改同一件事」的操作，必須自動化完成，不問用戶 | 自動化原則 |
| L031 | 大檔案（>100 行）用 Grep 定位行號，再用 Read offset/limit 只讀需要的段落，不要整個讀進來 | 讀檔效率 |
| L032 | 自動化腳本失敗後 MUST 先記錄實際狀態（期望找到什麼 vs 實際找到什麼）到 log，才決定是否重試，不得用同樣邏輯盲目 retry | 自動化 debug |
| L034 | 任何擴展點（include/hook/slot）用前 MUST 先查文件確認正確名稱，不猜檔名 | 平台整合 |
| L035 | 建 repo 後第一件事：.gitignore、LICENSE、README；依賴管理檔 MUST 固定版本，不要先寫內容再補基礎設施 | 專案初始化 |
| L036 | 加任何平台設定前先確認目標平台版本和限制（如 GitHub Pages 用 Jekyll 3.10 不是 Jekyll 4），不確定就查官方文件 | 平台版本確認 |
| L039 | 每個階段完成後，MUST 主動告知下一步是什麼、需要用戶做什麼決定，不能做完就停在那裡等問。格式：「下一步是 X，需要你 Y，我的判斷是 Z，你要繼續嗎？」 | 任何任務完成後 |
| L041 | 禁止叫 Fish 開瀏覽器操作任何事情。瀏覽器操作一律用 agent-browser MCP 或 gh CLI 自己完成。唯一例外：需要 Fish 親自授權的事（貼 API Key、2FA、付費操作、手動 Webhook 授權）。違反 = 白工。 | 任何需要瀏覽器的操作 |
| L077 | **程式碼風格衝突時必須明說選哪一種**，不要「兩邊都用、混在一起」。觸發：同個 codebase 看到兩種風格（例：camelCase vs snake_case、tab vs space、early-return vs nested-if）→ 必須先看哪種佔多數或先看 .editorconfig/prettier 設定，跟著佔多數的走；無法決定時直接問用戶「A 還是 B？」。禁止：「為了相容性兩個都保留」、「這檔案用 A 那檔案用 B」式的悄悄混用。 | 任何寫碼任務開始前 |
| L080 | Fish 說「sr」= Spectra SDD 專案（sr = spectra 的縮寫） | 任何對話 |
| L081 | **驗證 = 實際跑出結果，不是 build 通過**。任何功能完成後 MUST 自己做行為驗證：(1) 寫腳本用假資料呼叫函式 → 產出實際檔案（PDF/JSON/圖片）存 `/tmp/`；(2) 或啟動 dev server → Chrome MCP 操作 UI → 截圖每個畫面；(3) 或 curl/fetch 打 API 確認回傳格式正確。**build 通過 ≠ 功能正確**。禁止只跑 build 就回報「完成」；禁止說「需要你自己跑一次確認」把驗證丟回 Fish。違反 = 白工 + 信任歸零。 | 任何功能完成回報前 |
| L084 | **reuse-first（先考古再動手，無例外）**。寫任何代碼前強制前置步驟：(1) grep 現有 `apps/` 找類似 pattern；(2) 查同產品或其他產品的 archived changes；(3) 確認 API procedure 是否已存在（禁止只做 UI 外殼不接 API）；(4) 主動告訴 Fish：「這些不用做、這些直接用、只有這些要新寫」。**禁止**：從頭寫已有的東西、只做靜態 UI 沒接 API 就標「完成」。 | 任何寫碼任務開始前 |
| L085 | **完整派工 + 自己驗收（不丟球給 Fish，無例外）**。派工時：prompt 必須附 `ui-reference/` 路徑 + spec 路徑 + HTML demo 路徑，明確寫「按照這三份文件實作，不可自由發揮」。測試時：自己用 Chrome MCP 跑完所有頁面 + 讀 console + 截圖，一次跑完、一次報告全部問題 + 建議解法。對話中：重要資訊立刻寫進 spec/design.md，不靠對話記憶。**禁止**：叫 Fish 開瀏覽器/截圖/貼報錯、問 Fish 已回答過的問題。 | 派工/測試/對話中 |
| L090 | **API key / token / endpoint 先查 `.env`，禁止問 Fish**。任何「這個 API 的 key 是什麼？」「你有這個服務的 token 嗎？」問題，MUST 先 `cat .env`（或 `cat .env.local`、`cat .env.production`）自己找答案。找不到才問，且問的時候說明「已查 .env，沒有 X」。這是 L020 的具體化。 | 需要外部 API key 時 |

## 變更歷程

- 2026-05-15: 從 61 條拆分為核心 + 4 領域檔案，本檔保留 26 條
- 2026-05-15: 新增 L079 cross-impact 預檢
- 2026-05-16: 新增 L080 sr 縮寫
- 2026-05-17: 新增 L081 驗證必須實跑
- 2026-05-18: 新增 L083 supastarter-first、L084 reuse-first、L085 完整派工+自己驗收
- 2026-05-18: 新增 L090 API key 先查 .env
- 2026-05-19: 二次拆檔。主檔縮為 18 條核心跨領域規則：
  - L040 / L071 / L074 / L079 → `lessons-spectra.md`
  - L019 / L045 / L046 / L082 → `lessons-frontend.md`
  - L049 / L050 / L053 / L069 / L075 / L076 / L078 → `lessons-dev.md`（新建）
  - L083 / L086 → `lessons-products.md`
