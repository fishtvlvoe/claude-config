---
paths:
  - ".claude/skills/**"
  - "skills/**"
---

# Skill 安裝規則

> 安裝任何 Skill（自建或下載）都必須套用雙層優化模式，不得例外。

## 安裝流程（強制）

trigger: 用戶說「安裝 skill」「加入 skill」「裝這個」，或提供 SKILL.md 檔案/目錄要求安裝
action: 按以下步驟處理，不問用戶要不要優化（永遠優化）

### Step 1：判斷類型
- 有步驟、會改檔案 → Skill（放 `~/.claude/skills/名稱/`）
- 只讀分析、審查 → Agent（放 `~/.claude/agents/名稱.md`）

### Step 2：瘦身 description
- frontmatter description **必須 ≤1 句話、≤20 字**
- 刪除觸發詞列表、使用情境說明（這些留在內容裡）
- 加上 `disable-model-invocation: true`

### Step 3：拆骨架
- SKILL.md 只放：frontmatter + 角色定義 + 步驟 + 核心規則
- SKILL.md 目標 **< 500 tokens**
- 知識內容（範例、checklist、參考資料）→ `knowledge/` 子目錄
- 步驟中寫 `Read knowledge/xxx.md`（按需載入）

### Step 4：Agent 格式（如果是分析型）
- 不需要 frontmatter
- 必須限制工具：`Allowed: Read, Glob, Grep`
- 結構：角色 → 檢查項目 → 輸出格式 → 工具限制

## 品質檢查

policy: 安裝完成後自動檢查
- [ ] description ≤ 20 字？
- [ ] SKILL.md < 500 tokens？
- [ ] 大內容已拆到 knowledge/？
- [ ] disable-model-invocation: true？

## 規則衛生檢查（新增任何規則/設定時順便確認）

reminder: 新增規則前快速掃一眼，非強制但建議養成習慣
- [ ] 這條規則在其他檔案是否已經有了？（查 CLAUDE.md、gates.md、triggers.md）
- [ ] 這是「規則」還是「踩坑紀錄」？紀錄放 lessons.md，不放規則檔
- [ ] 這條需要每次對話都載入嗎？低頻觸發的考慮放 on-demand
