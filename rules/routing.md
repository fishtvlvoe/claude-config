# 路由速查表

> 2026-08-17 更新：拆掉「任務類型→固定模型」死板對照表，改成判斷原則。
> 依據：Boris Cherny（Claude Code 創辦人，2026 YC Startup School 訪談）——Opus 5 上線後 Anthropic 自己砍了 Claude Code 80% 的 system prompt，模型反而變準。方法叫 ablation study：整段刪掉、拿去用、模型真的卡在同一個問題才補一行回去。「這種任務一定要 Sonnet」「超過 5 行一定要派子代理」這類規則，就是他說的「舊模型才需要的逐步指令」，對現在的模型是拖累不是幫助。
> 但他也明講：verification（驗證/驗收機制）要加碼投資，不能減。所以這次只拆「派給誰」的機制，不動 Spectra 流程、TDD、Wave 驗收清單、deny-list 安全紅線。

## 硬規則（不可違反，只剩流程/事實，不含「派給誰」）

1. **Spectra 強制入口**：執行類任務 → `/spectra-*`，禁用 TaskCreate/TodoList 替代（哪個 Phase 誰來做 → 見下方「派工判斷」，自己判斷，不查表）
2. **說工具「不能用」前 → 先 `which <tool>` 確認**（這是驗證習慣，不是派工機制，留）

## 派工判斷（原則，不是表格）

派給誰（自己 / Sonnet 子代理 / Haiku 子代理 / Codex）、要不要派，自己判斷。判斷依據：

- **划不划算**：這任務獨立跑、平行跑會不會明顯省時間/省 context
- **能不能自己驗證**：派出去的工作，回來後我能不能一眼看出對不對（能 → 放心派；不能 → 自己做或緊盯著）
- **值不值得**：幾行代碼、簡單查詢、當下做更快 → 直接做，不為了「派工」而派工；複雜、可拆解、需要獨立 context 的 → 才考慮派出去

不用每次先宣告「派工：X，因為Y」，也不用先產分配表等 Fish 拍板才動——除非任務本身方向不確定、風險大，那種情況本來就該問，不是因為規則要求。

## 派工給外部 CLI 的方式（orca CLI）

Fish 說「派 Codex/Kimi/Cursor」等外部 CLI 時，MUST 用 orca CLI 開真正獨立的互動式 terminal session：

```bash
orca worktree create --name "<task-name>" --repo name:<repo-name> --json
orca terminal create --worktree path:<回傳的 path> --command "codex"   # 或 kimi/cursor-agent/agy
```

已確認可用：`codex`、`cursor-agent`、`kimi`、`agy`（Antigravity，執行檔名不是 antigravity）。`--worktree` 一定填明確 path，不要用 `active`（那是 UI 焦點中的 worktree，不是新建的）。`--command` 禁止填 `claude`（等於自己分身寫代碼，不是外部交叉驗證）。

**禁止**：`codex exec "..."` / `kimi -p "..."` 這類背景一次性 headless 呼叫冒充派工，沒有 session、沒有多輪記憶。

新開 worktree 第一次啟動 MUST 驗證真的開始做了（可能卡 onboarding 選單或吃掉第一則訊息），不能送出指令就假設成功。worker 完成（`worker_done`）→ 立即主動驗收+回報，不等 Fish 來問。

**完整 SOP**（要不要委派派工師、orchestration 監督流程、worktree 收尾流程、每個坑的起因與指令範例）→ 動工前 Read `~/.claude/reference/orca-worktree-sop.md`

## 自訂全域 Agent 命名對照表（可以叫用的專門子代理，不是必須叫）

> SSOT：全域 agent 定義唯一放 `~/.claude/agents/*.md`（frontmatter `name:` 欄位＝檔名＝呼叫用的 subagent_type）。這裡只列速查表，改名/加新 agent 時同步更新這裡。

| 中文名 | 原英文名 | 用途 | 正式規格（若非全域檔） |
|---|---|---|---|
| 後端工程師 | backend-specialist | API、伺服器邏輯、資料庫串接、auth | — |
| 前端工程師 | frontend-specialist | React/Next.js、UI 元件、樣式、狀態管理 | — |
| 資料庫工程師 | database-architect | Schema 設計、migration、查詢優化 | — |
| debug師 | debugger | 抓 bug、crash、效能問題根因分析 | — |
| 測試師 | test-engineer | 寫測試、TDD、補覆蓋率 | — |
| 資安稽核師 | security-auditor | 資安稽核、OWASP、注入/加密檢查 | — |
| 文件師 | documentation-writer | README/API文件/changelog（僅明確要求才叫） | — |
| 專案規劃師 | project-planner | 新專案/大功能拆任務、分工圖 | — |
| 簡報師 | presentation-manager | 簡報：想法/文案整理成中繼稿→Kimi 提詞或 ppt-master pptx | `/Users/fishtv/Development/PM專案師/.claude/agents/簡報師.md` |
| 開課師 | course-builder | 開課六階段：討論→定位收斂→簡報大綱（委派簡報師）→內容→出檔 | `/Users/fishtv/Development/PM專案師/.claude/agents/開課師.md` |
| 課程社群架構師 | （純中文新建，無舊英文名） | 課程/社群學習系統設計：Discovery→六維度逐題確認（分級/自評/任務過關/分組/角色/共編工具）→收斂成正式 Spectra SR，止步於 SR，不寫程式碼 | `~/.claude/agents/課程社群架構師.md` |
| 網頁設計師 | （純中文新建，無舊英文名） | 網頁企劃+部署：從想法/SR 討論需求→抓風格（21st.dev/motionsites.ai/Pinterest，3D 捲動效果走 scroll-world skill）→產出 HTML mockup 確認→靜態網站自己部署，或 App 需求交接前端工程師；也可直接吃已寫好的 HTML 跳過討論直接部署。預設直接 public 部署，使用者當次請求明確要求才走 private | `~/.claude/agents/網頁設計師.md` |
| 派工師 | worktree-agent skill（2026-08-17 升格為子代理） | 用 Orca CLI 開隔離 Git Worktree，把 Spectra tasks.md 依檔案範圍拆組，平行派給多個外部 CLI（Codex/Kimi/Cursor/Antigravity）或 Claude Code 執行 SR/實作/驗證；自己盯啟動狀態、送達確認、輪詢完成度，用 git diff 驗證實際改動再回報，不相信代理自報「做完了」。取代主對話自己跑 worktree-agent skill 的雜訊——啟動/輪詢/git diff 這些留在派工師自己的紀錄裡，回報給主對話只有精簡結果 | `~/.claude/agents/派工師.md` |
| 蓋神 | （純中文新建，無舊英文名，2026-08-19） | 一鍵全自動跑完 Spectra SDD 全流程（discuss→propose→apply→review→archive）。**只在 Fish 明講「用蓋神做 X」時觸發**，平常開發任務仍由 PM 主對話親自帶，不取代預設模式。三個硬停點不可跳：①propose 完成等 Fish 確認方向 ②TDD 紅燈矩陣表確認（L074）③cross-impact 🔴（L079） | `~/.claude/agents/蓋神.md` |

呼叫：`Agent(subagent_type="簡報師")`、`Agent(subagent_type="派工師")`、`Agent(subagent_type="蓋神")`。「課程社群架構師」「網頁設計師」為銜接關係：架構師產出 SR 後交棒給網頁設計師，網頁設計師自己涵蓋討論→mockup→部署（或判定為 App 再轉交前端工程師）。

不在此表的舊 spec pipeline agent（product-planner、spec-initializer、spec-shaper、spec-verifier、spec-writer、task-list-creator、implementer、implementation-verifier、codex-development-worker，位於 `~/.claude/agents/agent-os/`）刻意不改名，Fish 確認過沒在用。

## 工作流層級（參考圖，不是強制路徑）

```
Fish（架構師）→ 定方向、邊界、裁決
Claude Opus（PM）→ 企劃、拆任務、驗證、整合
Sonnet 子代理（執行者）→ 寫碼、CR、研究
Haiku 子代理（助手）→ 讀檔摘要、輕量分析
```

## 代碼審核（diff > 10 行仍要做，這是品質關卡不是派工機制）

CR 本身不可跳；要幾個角度看（correctness / security / performance）、要不要拆多個子代理平行跑，自己判斷任務規模再決定。3+ 子代理平行回報時，過 Reducer 層（見下）再整合，不要直接讀原始輸出。

## 並行原則

任務之間無交互依賴 → 才並行。
- 審查 ✅ 同檔多濾鏡
- 寫碼 ⚠️ 只有不同檔案
- 研究 ⚠️ 只有不同主題
- 設計 / 搜檔 ❌

### 🔴 Reducer 層（3+ 子代理彙整前強制，2026-08-16）

3 個以上子代理平行回報後，PM 禁止直接讀取全部原始輸出去整合。先過一層純邏輯 reducer（不用模型）：

1. 丟掉格式壞掉/欄位缺失的回報
2. 依內容正規化後分組，同組只留最高信心/最完整那份
3. 多個子代理獨立得出同結論 → 標記「已交叉確認」
4. 多個子代理結論矛盾 → 標記「矛盾」，明列給 Fish，不自行取捨

理由：原始輸出直接倒給整合層 = 濫竽充數，重複佔位、矛盾被淹沒、context 爆量。來源案例（40 Haiku worker → 1 Sonnet 合成）加 reducer 後成本降 86%、延遲降 78%，且多抓到原本被淹沒的矛盾。
適用：CR 平行審查、cross-impact 預檢分類表、Wave 多子代理回報彙整。
不適用：只有 1-2 個子代理回報時（沒有去重/分組的必要）。

## SDD Phase（流程不變，模型不再指定）

**原則**：這是「做什麼」的品質流程，不是「誰做」的派工表。各 Phase 該做什麼、驗收標準是什麼寫死；誰來做（自己/Sonnet子代理/Haiku子代理）當下判斷。

| Phase | 用途 |
|-------|------|
| 1（規劃） | Discuss / Propose |
| 2（TDD） | 紅燈測試（強制，見下方 Phase 2 說明） |
| 3（實作） | 代碼撰寫 |
| 4（Review） | CR 驗證（並行多角度） |
| 5（驗收） | E2E 測試 + 部署 |

**工作包合併原則**：不要拆太碎（例：「修 API / 寫測試 / 再修 API」分三份）；合併成一包或拆兩包平行，用判斷不用死規則。

## Wave SOP（驗收清單不變，執行方式自己判斷）

### Wave 前
1. 前一 Wave 所有任務 `[x]`
2. `git status` 乾淨
3. `npm run build` 通過

### Wave 執行
同 Wave 任務能不能平行、派不派子代理，自己判斷 → CR（diff > 10 行，品質關卡不可跳）→ build + test → git add + commit（conventional）→ 下一 Wave

### Wave 完成驗收（缺一不過，這是 verification，不可鬆）
- `npm run build` 0 錯誤
- CR 無 Critical
- git commit 存在
- tasks.md `[x]` 已更新

## 開發 Phase 職責

**Phase 1 — 規劃**：與用戶討論決策；產出 spec.md + tasks.md + HTML UI mockup。

**Phase 2 — TDD 測試（強制不可跳）**：逆推失敗點 → 產出「失敗矩陣表」（每個失敗點對應紅燈測試名稱 + 預期錯誤訊息）→ Fish 確認 → 只寫紅燈測試（不寫實作）→ 跑測試確認全紅燈 → 紅燈清單再給 Fish 確認後才進 Phase 3。

**Phase 3 — 實作**：核心架構、UI 元件、代碼、文案等多層級執行。不同檔案可平行，同檔案必須串行。

**Phase 4 — Review**：多角度 CR（correctness / security / performance），品質關卡不可跳。

**Phase 5 — 驗收**：測試全綠、UI 驗證、用戶確認。

**原則**：
- **Review 即修**：Review 發現的小改善（5 分鐘內完成）當下直接修，不記 todo；涉及其他 Wave 的檔案或設計決策才延後。
- **並行安全**：不同檔案可平行處理，同一檔案必須串行執行。

## 參考

詳細案例、失敗分類處置、Token 預算、完整並行策略：
→ `~/.claude/reference/spectra-agent-routing-full.md`（部分內容為舊版死板表格，讀取時以本檔的「派工判斷」原則為準）

