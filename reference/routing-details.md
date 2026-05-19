# 路由細節（按需 Read）

> 主檔速查表 → `~/.claude/rules/routing.md`
> 本檔放：CLI 寫碼用法備忘、CR 三層細節、Fallback 觸發條件

---

## Kimi CLI 寫碼用法備忘

```bash
# 標準寫碼派工（-w 只指程式碼目錄，不指專案根）
kimi --print -w src/ -p "重構 X 模組... 只修改 src/ 下的檔案，禁止動 openspec/、.claude/、docs/"

# 複雜任務先規劃再執行
kimi --print --plan -w src/ -p "..."

# 限制步數防失控（預設由 config 決定）
kimi --print --max-steps-per-turn 20 -w src/ -p "..."

# 只拿最終結果（省 log 噪音，適合串接腳本）
kimi --quiet -w src/ -p "..."

# 需要讀額外目錄但不改（如讀 types/ 參考但只改 src/）
kimi --print -w src/ --add-dir types/ -p "..."
```

**防護 SDD 檔案**（L069）：派工前先 `git add openspec/ .claude/ && git commit`；`-w` 只指程式碼目錄；prompt 結尾加禁令；派工後 `git diff --stat` 檢查。

---

## Codex CLI 寫碼用法備忘

```bash
# 標準非互動派工（workspace-write = 只能改工作目錄）
codex exec -C src/ -s workspace-write "重構 X 模組..."

# 完全繞過確認（等同 --yolo，在 CI / 全自動流程用）
codex exec -C src/ --dangerously-bypass-approvals-and-sandbox "..."

# 指定模型（預設 gpt-5.3-codex，ChatGPT 帳號不支援 o4-mini）
codex exec -C src/ -s workspace-write -m gpt-5.3-codex "..."

# 從 stdin 讀 prompt（適合 prompt 很長）
cat prompt.txt | codex exec -C src/ -s workspace-write

# 多工並行：不同目錄可同時跑（shell 背景執行）
codex exec -C apps/web -s workspace-write "改 UI" &
codex exec -C apps/api -s workspace-write "改 API" &
wait
```

**Codex × Claude Code 多工串接模式**：
- Claude（PM）把任務拆成「不同目錄/不同檔案」的工作包
- 同一訊息用多個 Bash tool call 並行 dispatch `codex exec &`
- 所有 Codex 任務完成後 Claude 統一 `git diff --stat` 驗收 → CR → commit

**防護 SDD 檔案**：同 L069/L050 — 派工前先 `git add openspec/ .claude/ && git commit`；`-C` 只指程式碼目錄；prompt 結尾加「禁止動 openspec/、.claude/、docs/」。

---

## 代碼審核三層（任何 diff > 10 行，強制）

### Layer 1 — CR 並行矩陣

**同一訊息並行派 3 個 subagent**（每個戴不同濾鏡全讀 diff）：

- `correctness-auditor` — 只看邏輯錯誤、邊界條件、型別誤用
- `security-lens` — 只看 OWASP / 注入 / 權限 / WP nonce
- `performance-auditor` — 只看 N+1 / 迴圈 IO / 記憶體 / 缺快取

三份報告回來後主對話整合，派 Copilot 一次修。

**備用**：跨檔（3+ 檔案）改用 Kimi CLI `kimi -p --print -w <dir>`

### Layer 2 — Debug

- 觸發：CR 發現問題 OR 測試跑不過
- 流程：讀 error → 找根因 → 派對應代理修 → 重跑測試
- 禁止：連續 retry 同一個錯誤超過 2 次不換策略
- 派給：Sonnet 子代理或主對話

### Layer 3 — Coverage

- 觸發：每個 Phase 完成後
- 工作：確認新增的函數都有對應測試，執行 `npx jest --coverage` 或 `composer test`
- 標準：核心業務邏輯覆蓋率 > 80%
- 派給：Copilot CLI 跑 `--coverage`

---

## 派工後自動驗證（強制，每次派工必跑）

```
派工完成 → git diff --stat
         → 檢查三項：
           1. 有改檔案？（diff 非空）
           2. 只改該改的？（沒動 openspec/ .claude/ docs/）
           3. build/test 通過？（npm run build 或對應指令）
         → 三項全過 = 繼續
         → 任一不過 = 觸發 fallback
```

## 自動 Fallback 觸發條件（不問 Fish，靜默切換 + 告知結果）

| 觸發條件 | 動作 |
|---------|------|
| CLI exit code ≠ 0（指令本身失敗） | 直接換下一個 |
| `git diff` 空（執行了但沒改任何檔案） | 換下一個 |
| 改了不該改的檔案（openspec/ .claude/ docs/） | `git restore .` → 換下一個 + prompt 加強禁令 |
| 改了檔案但 build/test 失敗 | `git restore .` → 換下一個 |
| CLI 超時（60 秒無輸出） | kill → 換下一個 |

切換時一行告知：「⚠️ [Copilot] build 失敗，切換 [Kimi] 重做」。不解釋細節、不等確認。

---

## 並行 vs 單派決策表（細節）

| 任務 | 並行？ | 條件 |
|------|-------|------|
| 審查 | ✅ | 同檔多濾鏡（correctness / security-lens / performance） |
| 寫碼 | ⚠️ | 只有「不同檔案」才並行（同檔會打架） |
| 研究 | ⚠️ | 只有「不同主題」才並行（同主題合併一次問） |
| 設計 | ❌ | 單一 Copilot 或 Sonnet 子代理（一致性優先） |
| 搜檔 | ❌ | 單一 Explore 或 Grep（並行無意義） |

原則：**任務之間無交互依賴 → 才並行**。

---

## 實習生任務原則（派外部 Agent 的鐵律）

派出去的任務必須符合：
- 輸入清楚：任務描述明確，不需要來回詢問
- 輸出格式定義好：告訴他回傳什麼、多少字
- 粒度夠小：一個任務只做一件事
- 不需推理判斷：模糊、複雜、需討論的部分，PM 先釐清再派出

**禁止派給實習生的工作**：計畫制定、方向討論、Debug 根因分析、架構決策、需要來回確認的任務 → 這些留在 PM。
