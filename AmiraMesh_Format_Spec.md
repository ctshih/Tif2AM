# AmiraMesh 3D ASCII 2.0 檔案格式說明

AmiraMesh 是一種靈活的 3D 數據儲存格式，廣泛應用於科學視覺化領域（如 Thermo Scientific Amira/Avizo）。本文檔主要說明其 **ASCII** 版本的結構，特別針對規則網格的體積數據 (Uniform Volume Data)。

## 1. 檔案總覽 (Overview)

一個標準的 AmiraMesh ASCII 檔案由三個部分組成：
1. **Header (標頭)**：包含版本宣告、維度定義、元數據 (Metadata)。
2. **Data Layout (數據宣告)**：連結定義的維度與數據類型。
3. **Data Section (數據區)**：實際的數值內容。

---

## 2. 標頭結構 (Header Structure)

### 2.1 版本宣告 (Magic String)
檔案的第一行必須嚴格遵守以下格式（區分大小寫）：
```text
# AmiraMesh 3D ASCII 2.0
```

### 2.2 維度定義 (Definitions)
使用 `define` 關鍵字宣告數據結構的大小。對於 Volume Data，通常命名為 `Lattice` 表示 3D 網格。

**語法**：
```text
define <Name> <DimX> <DimY> <DimZ>
```

**範例**：
```text
define Lattice 317 317 201
```
這表示一個 317(寬) x 317(高) x 201(深) 的 3D 陣列。

### 2.3 參數區塊 (Parameters)
包含關於數據的元數據，包裹在 `Parameters { ... }` 中。

| 參數 | 說明 | 範例 |
| :--- | :--- | :--- |
| **Content/ContentType** | 描述數據內容或類型，提供軟體提示。 | `"317x317x201 int, uniform coordinates"` |
| **BoundingBox** | 定義數據在 3D 空間中的物理範圍。<br>`xMin xMax yMin yMax zMin zMax` | `0.0 316.0 0.0 316.0 0.0 200.0` |
| **CoordType** | 座標類型。`"uniform"` 表示規則網格。 | `"uniform"` |
| **DataWindow** | (可選) 建議的顯示窗寬窗位 (Min Max)。 | `250 63273` |

**範例**：
```text
Parameters {
    Content "317x317x201 int, uniform coordinates",
    DataWindow 250 63273,
    BoundingBox 0.0 316.0 0.0 316.0 0.0 200.0,
    CoordType "uniform"
}
```

---

## 3. 數據宣告 (Data Layout)

定義變數名稱、數據類型以及在檔案中的位置標記。

**語法**：
```text
<DefinitionName> { <Type> <VarName> } @<ID>
```

*   **DefinitionName**：必須對應上方 `define` 的名稱 (如 `Lattice`)。
*   **Type**：數據類型，常見的有 `byte`, `short`, `int`, `float`, `double`。
*   **VarName**：變數名稱，通常為 `Data`。
*   **ID**：對應下方數據區的標記 (如 `@1`)。

**範例**：
```text
Lattice { int Data } @1
```
表示數據是整數類型 (int)，內容位於標記 `@1` 之後。

---

## 4. 數據區 (Data Section)

以註解 `# Data section follows` 開始，接著是位置標記 `@<ID>`，然後是實際數值。

**排列順序 (Ordering)**：
數據通常遵循 **x-fastest** 的順序（X 軸變化最快，其次 Y，最後 Z）。
索引邏輯：$(x, y, z) \rightarrow i = x + y \times DimX + z \times DimX \times DimY$

**範例**：
```text
# Data section follows
@1
0
0
128
255
...
```

---

## 5. 完整範例 (Complete Example)

這是一個 $2 \times 2 \times 2$ 的微型 Volume Data 範例：

```text
# AmiraMesh 3D ASCII 2.0

# 1. 定義網格大小
define Lattice 2 2 2

# 2. 設定參數
Parameters {
    Content "2x2x2 float grid",
    BoundingBox 0 1 0 1 0 1,
    CoordType "uniform"
}

# 3. 宣告數據位置與類型
Lattice { float Data } @1

# 4. 實際數據內容
# Data section follows
@1
0.1 0.2
0.3 0.4
0.5 0.6
0.7 0.8
```
*註：上述數據共 8 個值，前 2 個為 z=0, y=0 的 row，接著是 z=0, y=1 的 row，依此類推。*
