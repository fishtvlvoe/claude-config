# today.md — 2026-05-16

## Follow-up（之後有空再改）

### BuyGo+1 出貨明細「展開顯示中」模式也要顯示 variation_title

**現況**（v1.7.12）：
- 合併顯示中：父行 ×4 + 縮排子列 (A)/(B)/(C) ×N ✓
- 展開顯示中：4 行扁平 list，每行都只顯示父商品名「【預購】Kitty聯名可麗餅吊飾(5月到貨)」 — 看不出哪行是 A/B/C ❌

**用戶期望**：展開模式每行也要看到 variation_title。建議呈現方式（其一）：
- A：商品名稱欄改為「{product_name} - {variation_title}」（例：Kitty吊飾 - (A) 薄荷巧克力）
- B：商品名稱欄維持 product_name，但 variation_title 用副標 / 小字另起一行
- C：兩個欄位拆開顯示

**位置**：`admin/partials/shipment-details.php` 兩處 `<tr v-for="item in mergedDetailItems">`（detailModal + markShipped），在展開模式（即 `!mergeEnabled`，回傳原始 `detailModal.items`）時，`item.variation_title` 是有資料的（v1.7.12 detail endpoint 已 JOIN），只要顯示出來即可。

**範圍**：純前端 template 修改，1 個 PR、估 10 行內。
