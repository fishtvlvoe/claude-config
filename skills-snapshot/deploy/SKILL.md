---
name: deploy
description: "WordPress 外掛一鍵部署"
disable-model-invocation: true
---

# WordPress 外掛部署

## GATE：強制對焦（不可跳過）

1. 複述「我理解你要部署 ___ 到 ___」
2. 確認：外掛名稱、branch、目標伺服器
3. 問「確認部署？」

> **等用戶說 OK 才往下執行任何操作**

> **強制停止點：確認外掛名稱、branch、目標伺服器後，呈現部署摘要（要部署什麼到哪裡），等用戶明確說「確認部署」才執行任何操作。**

## 部署前（必做）

- 跑所有測試：`composer test`，全過才繼續
- 確認無 .env 或敏感檔在暫存區

## 部署

1. Git commit（語意化 message：`feat:` / `fix:` / `chore:`）
2. SSH 部署：pull 最新代碼、清快取、重啟服務

**常用目標**

| 環境 | 網域 | SSH |
|------|------|-----|
| 正式 A | buygo.me | nuhohaleda0848@64.227.109.5 |
| 正式 B | one.buygo.me | vonosidaku6233@143.198.54.239 |
| 測試 | test.buygo.me | 本機 Cloudflare Tunnel |

詳細 SSH 指令：`Read ~/.claude/projects/-Users-fishtv-Development/memory/environment.md`

## 品質檢查（部署類 — 多軌驗收）

部署完成後填寫，全部 ✅ 才算通過：

| 軌道 | 驗收項目 | 結果 |
|------|---------|------|
| TRACK 1 部署確認 | Git pull 成功，無衝突 | ✅/❌ |
| TRACK 1 部署確認 | 快取已清除（wp-content/cache 或 Redis）| ✅/❌ |
| TRACK 1 部署確認 | PHP 版本號與 git tag 一致 | ✅/❌ |
| TRACK 2 API 驗收 | BGo: 訂單/庫存/搜尋端點 HTTP 200 | ✅/❌ |
| TRACK 2 API 驗收 | LineHub: webhook/綁定端點 HTTP 200 | ✅/❌ |
| TRACK 3 Log 監控 | 部署後 2 分鐘無 500/502 錯誤 | ✅/❌ |

任一 ❌ → 立即執行回滾。

## 驗收（三軌並行）

**TRACK 1 部署確認**：確認 pull 成功、清快取、版本號與 git tag 一致

**TRACK 2 API 驗收**：依外掛打關鍵端點（BGo: 訂單/庫存/搜尋；LineHub: webhook/綁定；Webinar: 列表/報名；Paygo: 支付狀態）

**TRACK 3 Log 監控**：部署後 2 分鐘持續監看，攔截 500/502 錯誤

## 回滾條件

任一 TRACK 失敗 → 立即執行：
```bash
git revert HEAD --no-edit
# SSH 重新部署上一版
```

## 完成條件

- [ ] `composer test` 全部通過
- [ ] TRACK 1 部署確認通過
- [ ] TRACK 2 API 驗收通過
- [ ] TRACK 3 無 500/502 錯誤
- [ ] 部署報告已輸出（外掛名 + 版本 + 環境 + commit hash）
- [ ] 用戶已確認結果

## 禁止

- 手寫 rsync（必須用此 skill）
- 任一 TRACK 失敗後繼續等待（立即回滾）
- 測試未通過就部署
