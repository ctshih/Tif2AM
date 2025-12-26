# Tif Stack to AmiraMesh Converter

這是一個協助您將 2D Tif 影像堆疊轉換為 3D AmiraMesh ASCII 檔案的工具。

## 檔案說明
- `tif2am_app.py`: 主程式 (Streamlit App)
- `dialog_helpers.py`: 協助開啟檔案視窗的輔助程式
- `README.md`: 本說明文件

## 安裝依賴

本程式需要 Python 環境，並安裝以下套件：

```bash
pip install streamlit numpy tifffile
```

## 如何執行

請開啟命令提示字元 (cmd) 或 PowerShell，切換到程式目錄，然後執行：

```bash
python -m streamlit run tif2am_app.py
```

## 使用步驟

1. 程式啟動後，瀏覽器會自動開啟 (預設網址 `http://localhost:8501`)。
2. **選擇檔案**：
   - 點擊 **「📂 瀏覽檔案」** 按鈕。
   - 系統會彈出一個檔案總管視窗 (請注意工作列，視窗可能會在瀏覽器後方)。
   - 選取您要轉換的 Tif 影像檔 (支援多選)。
3. **設定參數**：
   - 輸入 X, Y, Z 的 **Voxel Size** (體素尺寸)。
4. **執行轉檔**：
   - 點擊 **「🔄 轉檔」** 按鈕。
   - 再次彈出視窗，選擇存檔位置與檔名。
   - 程式會自動處理並轉換為 AmiraMesh 3D ASCII 2.0 格式。

## 注意事項

- 如果點擊按鈕後沒有反應，請檢查工具列是否有閃爍的 Python 圖示，視窗可能被遮擋。
- 程式會自動偵測 `2DTIF_Stack` 資料夾作為預設路徑。
