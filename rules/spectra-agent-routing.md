# Spectra Apply SDD 專用規則

> 代理速查表、禁用清單、分類規則 → `~/.claude/rules/routing.md`（SSOT）
> 詳細案例、SOP → `~/.claude/reference/spectra-agent-routing-full.md`

## 工作包合併原則

**不要拆太碎**（例如「修 API / 寫測試 / 再修 API」分三份）
**應該合併**（例如「TDD：寫測試 → 修 API → 跑驗證」給 Sonnet 子代理一包，或拆「Copilot 寫 API + Sonnet 寫測試」兩包並行）

## Wave SOP（強制）

### Wave 前
1. 前一 Wave 所有任務 `[x]`
2. `git status` 乾淨
3. `npm run build` 通過

### Wave 執行
```
同 Wave 任務 → 同一訊息多 tool call 並行派出
→ 等回傳
→ Kimi MCP CR（diff > 10 行）
→ build + test
→ git add + commit（conventional）
→ 下一 Wave
```

## 用量不足自動切換（不等 Fish 確認）

| 主力 | 備用 1 | 備用 2 | 備用 3 |
|------|-------|-------|-------|
| Copilot CLI | Kimi CLI | Sonnet 子代理 | — |
| Kimi CLI | Copilot CLI | Sonnet 子代理 | — |
| Sonnet 子代理 | Copilot CLI | Kimi CLI | 主對話直接做 |

切換時主動告知 Fish：「⚠️ [Agent X] 用量不足，切換至 [Y] 繼續」

## Wave 完成驗收（缺一不過）

- `npm run build` 0 錯誤
- Kimi MCP CR 無 Critical
- git commit 存在
- tasks.md `[x]` 已更新

---

> 失敗分類處置、完整 Gmail 專案路徑、Token 預算、並行策略細節
> → `Read ~/.claude/reference/spectra-agent-routing-full.md`
