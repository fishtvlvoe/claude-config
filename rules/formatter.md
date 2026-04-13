# Formatter Gate — 格式檢查規範

Formatter 在 build 和 review 之間執行，確保代碼格式正確才進入內容驗收層。

## 檢查項目

Formatter 必須檢查以下 4 項：

### 1. File Structure（檔案結構）

**檢查**：spec 定義的檔案存在且完整，沒有多餘檔案

**判定方式**：
- 遍歷 spec 中的「預期檔案清單」
- 確認每個預期檔案存在
- 確認新增檔案都在 spec 範圍內（不是 build 的副作用殘留）

**輸出**：
- 通過：不輸出
- 失敗：列出缺失/多餘的檔案名和路徑

### 2. Conventional Commits（提交訊息格式）

**檢查**：stage 中的 commit message 符合 conventional commits 格式

**合法格式**：`<type>(<scope>): <subject>`
- **type**：feat, fix, docs, style, refactor, perf, test, chore（必填）
- **scope**：可選，括號內
- **subject**：必填，小寫開頭，不以句號結尾

**範例**：
- ✓ `feat(mesh): add flow definition system`
- ✓ `fix: correct typo in README`
- ✗ `Add new feature`（缺 type）
- ✗ `feat(mesh): Add flow`（subject 首字大寫）

**輸出**：
- 通過：不輸出
- 失敗：指出違反的規則和正確格式

### 3. No Residual Statements（無殘留陳述）

**檢查**：代碼中沒有 `console.log`、`TODO`、`FIXME`、`debugger` 等調試/臨時陳述

**掃描範圍**：
- 所有 .ts / .tsx / .js / .jsx / .py / .go 等代碼檔案
- 排除 node_modules、.git、spec 檔案、測試檔案中合理的 TODO（測試檔案中的 TODO/FIXME 可接受）

**規則**：
- `console.log` / `console.error` / `console.warn` — 禁止
- `TODO`、`FIXME`、`HACK` — 禁止（文件中可以有，代碼中禁止）
- `debugger` — 禁止
- `alert()`、`confirm()` — 禁止（Web only）

**輸出**：
- 通過：不輸出
- 失敗：列出檔案名、行號、找到的陳述內容

### 4. Comment Language（註解語言）

**檢查**：代碼檔案的註解語言符合規範

**規則**：
- **代碼註解**：英文（code logic 解釋必須英文，方便跨國協作）
- **文檔檔案**（README、DESIGN、SPEC）：繁體中文（用戶文檔）

**掃描**：
- 檢查檔案副檔名判定類型
- 代碼檔案（.ts/.js/.py/.go 等）中的註解，掃描中文字
- 如果檢查到大量中文註解 → violation

**輸出**：
- 通過：不輸出
- 失敗：指出檔案名和第一個中文註解的行號

## 輸出格式

Formatter 輸出統一 JSON：

```json
{
  "format_valid": true,
  "violations": []
}
```

當有違反時：

```json
{
  "format_valid": false,
  "violations": [
    {
      "file": "src/auth.ts",
      "line": 42,
      "rule": "no-residual-statement",
      "message": "TODO comment in production code"
    },
    {
      "file": null,
      "line": null,
      "rule": "conventional-commit",
      "message": "Commit message 'Add feature' missing type prefix (expected: feat/fix/docs/...)"
    }
  ]
}
```

## Formatter 流程

1. **檢查順序**：依上述 4 項順序檢查
2. **提前退出**：找到第一個違反即加入 violations（不需全部找完，但建議掃完整）
3. **輸出**：JSON 格式，包含 `format_valid` 和 `violations[]`
4. **Return to Build**：若 `format_valid: false`，系統自動回到 build step（Haiku 任務完成，不需手動回退）

## 執行者

- **Agent**：Haiku（輕量、快速）
- **頻率**：每次 build 完成後、review 前
- **成本**：極低（Haiku ≈ 0.00001 USD/call）

## 與 Review 層的界線

- **Formatter**（格式層）：檢查檔案存在、commit message、殘留陳述、註解語言
- **Review**（內容層）：檢查邏輯正確、架構合理、edge case 涵蓋、測試覆蓋率

分離原因：讓 Kimi 專心看邏輯，不被「格式對不對」打斷。
