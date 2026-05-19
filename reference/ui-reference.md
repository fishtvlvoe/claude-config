# UI Reference 規則（強制）

## 硬規則

寫任何 UI 代碼前，專案內必須存在對應的視覺定義檔（`ui-reference/` 目錄）。

沒有視覺定義 = 不能寫 UI 代碼。先建定義，再寫碼。

## 結構

```
<app>/ui-reference/
├── pages/<page-name>.md       ← 頁面級規格
├── components/<component>.md  ← 元件級規格
└── screenshots/               ← 參考截圖（png）
```

## 每個 spec 檔必須包含

1. 參考截圖（路徑或內嵌）
2. 必要元素清單（順序 + 內容 + 樣式重點）
3. 資料來源（API 端點 + 欄位對應）
4. 不做的事（明確排除）

## 派工規則

- 任何 UI 任務的 prompt / task description 必須指向對應 spec 檔路徑
- 代理看不到對話 context，只看得到檔案 — 所以規格必須在檔案裡
- 寫出來跟 spec 不符 = 退回重做

## 來源

視覺定義的來源不限：仿站截圖、Figma 匯出、自繪 wireframe、HTML 原型。
重點是「存在且明確」，不是「在某次對話裡講過」。
