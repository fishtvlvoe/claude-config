# Token Report — Claude Code Token 使用量分析

## 描述
分析最近 7 天的 Claude Code token 使用情況，按專案、session、子代理分拆統計，產出詳細報告與成本估算。

## 觸發
用戶輸入 `/token-report`

## 流程
1. 執行 `python3 ~/.claude/skills/token-report/analyze.py`
2. 腳本讀取 `~/.claude/projects/` 下的 JSONL 對話紀錄
3. 統計最近 7 天的 token 消耗
4. 產出 Markdown 報告存檔至 `~/.claude/reports/token-report-{YYYY-MM-DD}.md`
5. 在終端顯示摘要 + ASCII bar chart

## 報告維度
- 按專案分拆（input/output tokens、估計成本）
- 按 session 分拆（Top 5 最昂貴）
- 按子代理分拆（Opus / Sonnet / Haiku / cursor-agent / Kimi / Gemini / Codex）

## 輸出格式

### 報告檔案
- 路徑：`~/.claude/reports/token-report-{YYYY-MM-DD}.md`
- 內容：
  1. 總覽（期間、總 token 數、估計成本）
  2. 按專案排序的表格（專案名 | input tokens | output tokens | 估計成本）
  3. 按子代理排序的表格（model | input tokens | output tokens | 估計成本）
  4. Top 5 最昂貴 session 列表
  5. ASCII bar chart（按專案 token 消耗排列）

### 終端輸出
同報告內容

## 完成條件
- [x] 報告已存檔到 `~/.claude/reports/`
- [x] 終端顯示完整摘要與 bar chart
- [x] 統計邏輯涵蓋 input/output/cache tokens
- [x] 成本估算採用正確費率

## 成本估算（美元/百萬 token）
- Opus: input $15, output $75
- Sonnet: input $3, output $15
- Haiku: input $0.25, output $1.25

## 技術棧
- 語言：Python 3
- 依賴：僅使用標準庫（json, os, pathlib, datetime, collections）
- 字元編碼：UTF-8

metadata: 建立於 2026-04-08 | 類型: 分析工具
