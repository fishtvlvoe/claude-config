# SSOT — Single Source of Truth

> 每種資訊只住一個地方，寫之前先查這張表。違反 SSOT = 同一份資訊出現在兩個地方 → 遲早不同步 → 禁止。

| 資訊類型 | 唯一歸屬（寫這裡） | 禁止寫到 |
|---------|-------------------|---------|
| 今日進度 | `memory/today.md` | claude-mem（claude-mem 只用於跨日搜尋） |
| 技術踩坑/教訓 | `memory/lessons.md` | today.md、CLAUDE.md 註解、claude-mem |
| 判斷案例 | `memory/judgment-cases.md` | lessons.md（踩坑 ≠ 判斷） |
| 專案戰略狀態 | `memory/projects.md` | today.md（today = 當日進度，不是狀態） |
| 環境/SSH/部署 | `memory/environment.md` | CLAUDE.md `<conn>`（conn 只放指令事實） |
| 待辦事項 | Linear（長期追蹤）+ GSD todos（開發中短期） | memory 檔案（待辦不是記憶） |
| 外掛開發指引 | 各外掛 `CLAUDE.md` | 全域 CLAUDE.md（全域只放跨專案規則） |
| 工作流規則 | `~/.claude/CLAUDE.md` → `rules/` | memory 檔案（規則不是記憶） |
| Skill 開發紀錄 | 各 Skill 的 `SKILL.md` | memory 檔案 |
| 跨日記憶/搜尋 | claude-mem | today.md（today 隔天清空） |

policy: 寫任何資訊前，先查 SSOT 表確認歸屬，寫錯地方 = 違規
policy: 發現同一資訊出現在兩處 → 保留 SSOT 歸屬的那份，刪除另一份
