# SSC 產出模板

## 模板 A：Skill（世代 3 完整結構）

### SKILL.md 模板

```markdown
---
name: {{skill-name}}
description: "{{一行描述，要包含觸發詞}}"
disable-model-invocation: true
user-invocable: true
---

# {{Skill 標題}}

## GATE：強制對焦（不可跳過）

收到任務後，第一步必須：
1. 一句話複述「我理解你要 ___」
2. {{依 Skill 類型補充確認項}}
3. 問「方向對嗎？」→ 用戶說 OK 才往下

---

## 流程

### 步驟 1：{{第一步名稱}}

{{步驟說明}}

{{如果有參考資料：Read knowledge/xxx.md 執行 ___。}}

> **強制停止點：{{什麼完成後}}，必須等用戶確認才能繼續。**

### 步驟 2：{{第二步名稱}}

{{步驟說明}}

### 步驟 3：{{第三步名稱}}

{{步驟說明}}

### 步驟 N：品質檢查（必須執行）

{{依品質檢查類型填入，見 quality-check.md}}

---

## 完成條件（全部達到才算完成）

- [ ] GATE 已通過
- [ ] {{關鍵停止點}}已確認
- [ ] 品質檢查已通過
- [ ] 用戶已確認結果
```

### 資料夾結構

```
skill-name/
├── SKILL.md              ← 流程骨架（< 100 行）
├── knowledge/            ← 參考資料（按需 Read）
│   └── {{topic}}.md
└── TEMPLATES.md          ← 輸出模板（如有固定格式）
```

### SKILL.md 撰寫原則

1. **< 100 行**：超過就拆到 knowledge/
2. **用 Read 指令引用**：`Read knowledge/xxx.md 執行 ___`
3. **每個步驟一段話**：不要寫成說明書
4. **強制停止點標記清晰**：用 blockquote + 粗體
5. **完成條件用 checkbox**：方便對照

---

## 模板 B：Agent

### agents/*.md 模板

```markdown
# {{Agent 名稱}} — {{一句話角色}}

{{2-3 句話說明職責。由 {{誰}} 呼叫，也可直接使用。}}

## 執行流程

1. {{讀取輸入}}
2. {{依 checklist 逐項掃描}}
3. {{按嚴重程度分類輸出}}
4. {{CRITICAL 未清零 → 禁止繼續}}

## Checklist

### {{類別 1}}

**CRITICAL（信心閾值 95%）**
- [ ] {{檢查項}}
- [ ] {{檢查項}}

**HIGH（信心閾值 85%）**
- [ ] {{檢查項}}

**MEDIUM（信心閾值 75%）**
- [ ] {{檢查項}}

## 輸出格式

{{Agent 的結構化輸出格式}}
```

### Agent 撰寫原則

1. **不需要 GATE**：Agent 收到任務直接做
2. **職責單一**：一個 Agent 只做一件事
3. **Checklist 導向**：用信心閾值分級
4. **輸出結構化**：方便呼叫者解析

---

## 模板 C：Hook

### settings.json hook 設定模板

```json
{
  "hooks": {
    "{{事件名稱}}": [
      {
        "command": "{{Shell 指令}}",
        "timeout": {{毫秒數}}
      }
    ]
  }
}
```

### 可用事件

| 事件 | 觸發時機 | 典型用途 |
|------|---------|---------|
| `SessionStart` | Session 開始 | 載入記憶、日誌初始化 |
| `SessionEnd` | Session 結束 | 備份、同步 |
| `UserPromptSubmit` | 用戶送出訊息 | 訊息前處理 |
| `PreCompact` | Context 壓縮前 | 保存重要資訊 |
| `PreToolUse` | 工具執行前 | 攔截危險操作 |
| `PostToolUse` | 工具執行後 | 日誌記錄 |
| `Stop` | 回應完成後 | 自動學習、記憶更新 |
| `PostToolUseFailure` | 工具執行失敗 | 錯誤記錄 |
| `PermissionRequest` | 權限請求時 | 自動審核 |

### Hook 撰寫原則

1. **零 AI 依賴**：純 Shell 腳本，不呼叫 Claude
2. **快速執行**：timeout 通常 < 10000ms
3. **不影響主流程**：失敗不應阻塞對話
4. **可組合**：同一事件可掛多個 hook

---

## 轉換模式專用指引

把別人的 Skill 轉換成我們的結構時：

1. **讀取原始 SKILL.md**：理解它做什麼
2. **分類判斷**：依 classification.md 決定 Skill / Agent / Hook
3. **提取核心邏輯**：
   - 流程步驟 → SKILL.md 的流程區塊
   - 大段參考資料 → knowledge/ 資料夾
   - 固定輸出格式 → TEMPLATES.md
   - scripts/ → 保留（改名為更清晰的名稱如需要）
   - references/ → 合併到 knowledge/
4. **加入我們的元件**：
   - 補 GATE 對焦
   - 加 `disable-model-invocation: true`
   - 插入強制停止點
   - 加品質檢查（依類型）
   - 加完成條件 checklist
5. **精簡**：刪除 README.md、CHANGELOG.md 等非必要檔案
