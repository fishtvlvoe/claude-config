---
name: 分配
description: "把任務分派給背景 AI worker 執行，主對話只做編排。說 'dispatch sonnet 做這個'、'dispatch gemini 查這個'、'dispatch kimi 分析這個' 都可以觸發。"
user-invocable: true
---

# Dispatch v2 — 背景 AI Worker 調度器

把任務交給背景 worker 執行，主對話不阻塞，只負責規劃、追蹤、回報。

> 完整 dispatch 引擎邏輯參考：`~/.claude/skills/dispatch/skills/dispatch/SKILL.md`
> Config 範例：`~/.dispatch/config.yaml`

## GATE（強制對焦，不可跳過）

收到 `/dispatch-v2` 後：

a. 判斷意圖類型（下方三種之一）
b. 說「我打算用 [模型] 處理 [任務]，方向對嗎？」→ 確認才執行

## 三種意圖

| 意圖 | 判斷條件 | 處理方式 |
|------|---------|---------|
| **暖機** | 沒有任務描述 | 讀 `~/.dispatch/config.yaml`，確認載入，停止 |
| **Config 修改** | 提到「加模型」「改預設」「新增 alias」 | 修改 config，停止 |
| **任務分派** | 其他所有情況 | 走下方流程 |

**核心原則：永遠不要自己做任務。主對話只寫計畫、派 worker、追蹤進度。**

## 模型路由（Primary 優先，Fallback 備用）

> 原則：外部訂閱模型優先（零 Anthropic token），Claude 子代理為 Fallback。

| 你說的 | 對應 backend | 適合任務 | 層級 |
|--------|-------------|---------|------|
| `copilot-codex` | copilot `--model gpt-5.2-codex` | 寫程式碼、重構、測試 | Primary |
| `copilot-opus` | copilot `--model claude-opus-4.6` | 複雜邏輯實作 | Primary |
| `copilot-fast` | copilot `--model gpt-4.1` | 文件、scaffold、輕量任務 | Primary |
| `copilot-haiku` | copilot `--model claude-haiku-4.5` | 格式雜務、讀檔紀錄 | Primary |
| `gemini` / `research` | gemini | 網路研究、API 文件、市場調查 | Primary |
| `kimi` / `analyze` | kimi | 3+ 檔案分析、大量數據 | Primary |
| `cursor` / `scout` | cursor | 本機偵察、簡單查找（< 300 字） | Primary |
| `codex` / `review` | codex | Code review、安全驗證 | Primary |
| `sonnet` / `code` | claude | 寫程式碼（Fallback，Primary 失敗時） | Fallback |
| `haiku` | claude | 瑣事、格式調整（Fallback） | Fallback |
| `opus` | claude | 規劃、架構決策（謹慎使用） | 大腦 |

> **Copilot backend 指令**：`/Users/fishtv/.superset/bin/copilot -p --allow-all-tools --model <model-id>`
> **Sonnet / Opus / Haiku 用 claude backend，不加 `--model` 參數。**

## 執行流程

### Step 1 — 選模型

掃描 prompt 中的模型名或 alias（見上表）。沒有指定 → 用 config 的 `default`，告知用戶確認。

### Step 2 — 建計畫檔

寫入 `.dispatch/tasks/<task-id>/plan.md`：

```markdown
# <任務標題>

- [ ] 第一個具體步驟
- [ ] 第二個具體步驟
- [ ] 把結果寫入 .dispatch/tasks/<task-id>/output.md
```

規則：每項要可驗證、不寫廢話、複雜任務 5-8 項、簡單任務 1-2 項。

### Step 3 — 一次 Bash 建全部 scaffolding

```bash
mkdir -p .dispatch/tasks/<task-id>/ipc
cat > /tmp/dispatch-<task-id>-prompt.txt << 'PROMPT'
<worker prompt>
PROMPT
cat > /tmp/worker--<task-id>.sh << 'WORKER'
#!/bin/bash
<backend 指令> "$(cat /tmp/dispatch-<task-id>-prompt.txt)" 2>&1
WORKER
cat > /tmp/monitor--<task-id>.sh << 'MONITOR'
#!/bin/bash
IPC_DIR=".dispatch/tasks/<task-id>/ipc"
TIMEOUT=1800
START=$(date +%s)
shopt -s nullglob
while true; do
  [ -f "$IPC_DIR/.done" ] && exit 0
  for q in "$IPC_DIR"/*.question; do
    seq=$(basename "$q" .question)
    [ ! -f "$IPC_DIR/${seq}.answer" ] && exit 0
  done
  ELAPSED=$(( $(date +%s) - START ))
  [ "$ELAPSED" -ge "$TIMEOUT" ] && exit 1
  sleep 3
done
MONITOR
chmod +x /tmp/worker--<task-id>.sh /tmp/monitor--<task-id>.sh
```

**Backend 指令對照：**

```
claude backend:   env -u CLAUDE_CODE_ENTRYPOINT -u CLAUDECODE claude -p --dangerously-skip-permissions
copilot backend:  /Users/fishtv/.superset/bin/copilot -p --allow-all-tools --model <model-id>
cursor backend:   cursor-agent -f --print --model <model-id>
codex backend:    codex exec --full-auto -C "$(pwd)" --model <model-id>
gemini backend:   /Users/fishtv/.superset/bin/gemini -p
kimi backend:     kimi --yolo --print
```

**Copilot 可用 model-id：**
```
gpt-5.2-codex    → 寫程式碼（Primary 預設）
claude-opus-4.6  → 複雜邏輯
gpt-5.4          → 標準任務
gpt-4.1          → 輕量/快速
claude-haiku-4.5 → 雜務兜底
```

**同一任務可開多個 Copilot worker 用不同模型並行執行。**

### Step 4 — 背景執行

```bash
# run_in_background: true
bash /tmp/worker--<task-id>.sh

# run_in_background: true
bash /tmp/monitor--<task-id>.sh
```

### Step 5 — 回報給用戶

只說：task-id、用哪個模型、計畫摘要。不回報 script 路徑或內部細節。

## Worker Prompt 模板

```
你有一份計畫檔在 .dispatch/tasks/{task-id}/plan.md。
從上到下逐項執行，完成後把 [ ] 改成 [x]。

遇到問題需要詢問，寫到 .dispatch/tasks/{task-id}/ipc/<NNN>.question（原子寫入）。
等待 .answer。3 分鐘無回應 → 把上下文存到 context.md，標記 [?]，停止。

全部完成後執行：touch .dispatch/tasks/{task-id}/ipc/.done

Context:
{任務背景、需要讀的檔案、限制條件}
```

## 追蹤進度

- 收到 `<task-notification>` → 讀 `plan.md` 回報狀態
- 用戶問「怎麼了」→ `cat .dispatch/tasks/<task-id>/plan.md`
- Worker 問問題（monitor 通知）→ 讀 `.question` 檔 → 問用戶 → 寫 `.answer` → 重啟 monitor

## 完成條件

- [ ] 計畫檔已建立並給用戶確認
- [ ] Worker 已背景執行
- [ ] 用戶已收到 task-id 和計畫摘要
