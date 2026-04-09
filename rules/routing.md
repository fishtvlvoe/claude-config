# 模型路由 — 誰做什麼

## 角色分工（核心心智模型）

```
Fish（架構師）→ 定方向、定邊界、最終裁決
Claude（專案經理）→ 企劃、規劃、拆任務、驗證、整合結果
外部模型（實習生）→ 照單全收、執行具體小任務、回報結果
```

**實習生原則（派出去的任務必須符合）：**
- 輸入清楚：任務描述明確，不需要來回詢問
- 輸出格式定義好：告訴他回傳什麼、多少字
- 粒度夠小：一個任務只做一件事
- 不需推理判斷：模糊、複雜、需討論的部分，專案經理先釐清再派出

**禁止派給實習生的工作：**計畫制定、方向討論、Debug 根因分析、架構決策、需要來回確認的任務 → 這些留在大腦。

---

## ⛔ 動手前強制自問（每次，不允許跳過）

收到任務後，**寫任何程式碼或工具呼叫之前**，必須先在腦中過這四題：

1. **超過 5 行程式碼？** → YES → 派 cursor-agent Skill 或 Sonnet 子代理，我不寫
2. **需要讀 3+ 個檔案？** → YES → 派 Kimi MCP，我只看摘要
3. **需要查外部技術/API/文件？** → YES → `gemini -p "..."` CLI，不用 Claude
4. **寫文件/HTML/scaffold？** → YES → cursor-agent Skill，零 Anthropic token

全部 NO → 才允許主對話直接執行。

5. **串接外部 API（fal.ai / OpenAI / ElevenLabs...）？** → YES → 先用 `gemini -p` 查最新端點格式，再派 Sonnet 實作。禁止憑記憶假設 URL / payload 格式。

---

## WBS 拆任務原則（強制）

收到任務後，大腦（Opus/Sonnet）必須：
1. **由上而下拆解**：目標 → 工作包 → 可執行子任務（WBS）
2. **MECE 檢查**：子任務之間不重疊（ME）、合起來完整覆蓋目標（CE）
3. **並行評估**：哪些子任務無依賴關係 → 同一 Sprint 並行派出
4. **派完才等**：全部 Agent 派出後統一等結果，不串行等待

## 多 Agent 分工架構

```
大腦（Opus/Sonnet）
  WBS 拆解 + MECE 驗證
       ↓
  ┌────┴──────────────────────┐
  │   Sprint N（並行波次）     │
  ├──────┬──────┬──────┬──────┤
  ▼      ▼      ▼      ▼      ▼
Copilot Copilot Kimi  Gemini cursor
不同    不同    分析   研究   偵察
模型    任務   codebase 外部  文件
  └────────────────────────────┘
       Sprint N 結束 → 整合
       ↓
  Sprint N+1（下一波）
```

## 模型分工表

<!-- 呼叫方式：Opus=主對話 / Sonnet/Haiku=Agent / Kimi=`kimi --yolo --print` / Gemini=`gemini -p` / Codex=`codex exec` / cursor-agent=`cursor-agent -f --print` / Copilot=`copilot -p --allow-all-tools --model <id>` -->

| 層級 | 模型 | 用於 |
|------|------|------|
| **大腦** | Opus / Sonnet | 規劃、WBS 拆解、決策、整合結果（唯一消耗 Anthropic token 的層） |
| **Primary 執行** | Copilot (gpt-5.2-codex) | 寫程式碼、重構、測試撰寫（零 Anthropic token） |
| **Primary 執行** | Copilot (claude-opus-4.6) | 複雜邏輯實作、需要高推理的任務（零 Anthropic token） |
| **Primary 執行** | Copilot (gpt-5.4 / gpt-4.1) | 文件撰寫、scaffold、輕量任務（零 Anthropic token） |
| **Primary 執行** | Kimi | 3+ 檔案分析、架構理解、大量 diff review |
| **Primary 執行** | Gemini | 研究外部 API/技術、搜尋網路資料 |
| **Primary 執行** | cursor-agent | 本機偵察、HTML UI 原型（零 Anthropic token） |
| **Primary 執行** | Codex | 安全驗證、交叉 review |
| **Fallback 執行** | Sonnet 子代理 | Primary 額度滿 / 失敗時，接手程式碼撰寫 |
| **Fallback 執行** | Haiku 子代理 | Primary 額度滿 / 失敗時，接手雜務、格式、讀檔 |

## 核心路由

- 任務拆解、方案選擇、風險評估 → 主對話（Opus），用 WBS + MECE
- 3+ 檔案分析 / 架構 / review / 50+ 行 diff → Kimi（Primary）
- 寫程式碼（有規格）→ Copilot gpt-5.2-codex（Primary）→ Sonnet（Fallback）
- 研究外部技術 / API 文件 / 網路資料 → `gemini -p "prompt"`（Primary）
- 關鍵邏輯驗證 / 安全 review → `codex exec "prompt"`
- 文件撰寫 / HTML UI / 本機偵察 → cursor-agent 或 Copilot gpt-4.1（零 token）
- 搜尋、讀檔、紀錄、格式調整 → Copilot claude-haiku（Primary）→ Haiku（Fallback）
- 小改動（1-2 行 hotfix）→ 主對話直接做（唯一例外）
- PR 建立後 → GitHub Copilot 自動 review（訂閱內，不消耗 Claude token）
- 正式開發 → /sla:develop 或 /sla:plan；專案啟動 → /gsd:plan-phase

## Fallback 觸發條件

Primary 出現以下任一情況 → 靜默切換 Fallback，並告知用戶：
- 模型回傳錯誤 / 超時
- 用戶明確說「X 用量滿了」
- 任務需要 Anthropic context（本地 codebase 深度整合）

## 研究類任務 Gate（強制）

禁止 Claude 子代理執行網路研究（沒有上網能力）。預設用 Gemini CLI；不可用時降級順序：Kimi MCP → Haiku（必須告知用戶原因並取得同意，禁止靜默換代理）。

## 外顯化路由判斷（硬規則）

每次收到任務，回應**第一句話**必須是路由判斷：「路由：這是 [工作類型]，派 [代理名稱]」或「路由：1-2 行 hotfix，我直接做」或「路由：需要方向判斷，我來處理」。禁止跳過直接執行。

## Opus 自律 Checklist

**只做**：規劃、決策、方向討論、審核結果、跟用戶對話、1-2 行 hotfix。

**禁止做**（違反 = 白工）：
- ❌ 親自讀大量檔案（50+ 行）→ 交 Haiku / cursor-agent
- ❌ 親自做研究或技術調查 → 交 Gemini / Kimi
- ❌ 親自寫超過 5 行代碼 → 交 Sonnet
- ❌ 親自寫文件/spec/tasks → 交 cursor-agent / Gemini / Haiku
- ❌ 靜默執行工具不告知用戶

**Opus 可直接做**（不需派子代理）：
- ✅ 預期輸出 < 10 行的 Bash（如 `tail -5`、`wc -l`、`git status`）
- ✅ 讀短檔案（< 50 行）或讀檔案的特定片段（offset + limit）
- ✅ 1-2 行 hotfix（同一檔案內，不跨檔）
- 判斷基準：原始輸出會不會大量佔用主對話 context？不會 → 直接做；會 → 派 Haiku

**透明度 + 子代理 prompt 規則**：
- 每次呼叫工具或子代理前，一句話告知用戶「派 X 去做 Y」
- 子代理 prompt 必須含回傳字數上限或格式要求；只要路徑 + 方法清單 + 關鍵摘要，不要求完整原始碼
- 回傳結果超過預期 → 先摘要再給用戶
- 子代理任務完成後，若中間派工對話已超過 10 輪，主動建議 /compact 壓縮中間過程只留結果摘要

**委派優先順序（寫文件/spec/tasks）**：cursor-agent → Gemini CLI → Haiku → Sonnet（Sonnet 只寫程式碼）

**委派優先順序（研究/分析）**：Kimi MCP（codebase） → Gemini CLI（外部技術/市場） → Codex（交叉驗證） → cursor-agent（本機偵察 < 300 字）→ Haiku（最後手段，必須告知降級原因）
