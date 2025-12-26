import streamlit as st
import numpy as np
import tifffile
import os
import dialog_helpers  # Our custom helper for dialogs

# Main App Configuration
st.set_page_config(page_title="TifStack to AmiraMesh", layout="wide")
st.title("2D Tif Stack to AmiraMesh Converter")

# Session State
if 'selected_files' not in st.session_state:
    st.session_state['selected_files'] = []
if 'common_path' not in st.session_state:
    st.session_state['common_path'] = os.getcwd()

# 1. File Selection Section
st.header("1. 選擇檔案 (Select Files)")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("📂 瀏覽檔案 (Browse Files)", type="primary"):
        st.info("請在彈出的視窗中選取檔案... (Check popup window)")
        
        # Call Helper
        files = dialog_helpers.get_open_filenames(st.session_state['common_path'])
        
        if files:
            # Sort files alphanumerically
            sorted_files = sorted(files)
            st.session_state['selected_files'] = sorted_files
            if sorted_files:
                st.session_state['common_path'] = os.path.dirname(sorted_files[0])
            st.success(f"已選取 {len(sorted_files)} 個檔案")
            st.rerun() # Refresh to show files
        else:
            st.warning("未選取任何檔案 (No files selected)")

with col2:
    if st.session_state['selected_files']:
        st.write(f"**已選取 {len(st.session_state['selected_files'])} 個檔案:**")
        st.caption(f"位置: {st.session_state['common_path']}")
        
        display_list = st.session_state['selected_files']
        file_names = [os.path.basename(f) for f in display_list]
        
        # Display logic
        if len(display_list) > 10:
             display_str = "\n".join(file_names[:5]) + "\n...\n" + "\n".join(file_names[-5:])
        else:
             display_str = "\n".join(file_names)
        
        st.text_area("檔案列表 (File List)", value=display_str, height=200, disabled=True)
    else:
        st.info("請點擊左側按鈕選取 Tif 檔案。")

# 2. Voxel Configuration
st.header("2. 設定 Voxel 尺寸 (Voxel Size)")
st.write("請設定每個 Voxel 在 x, y, z 三個方向的物理長度。")

v_col1, v_col2, v_col3 = st.columns(3)
with v_col1:
    vox_x = st.number_input("Voxel X", value=1.0, step=0.1, format="%.6f")
with v_col2:
    vox_y = st.number_input("Voxel Y", value=1.0, step=0.1, format="%.6f")
with v_col3:
    vox_z = st.number_input("Voxel Z (Spacing)", value=1.0, step=0.1, format="%.6f")

# 3. Conversion Action
st.header("3. 執行轉檔 (Convert)")

if st.button("🔄 轉檔 (Convert to AmiraMesh)", type="primary", disabled=len(st.session_state['selected_files']) == 0):
    files = st.session_state['selected_files']
    
    st.info("請在彈出的視窗中選擇儲存位置... (Check popup window)")
    
    # Call Helper
    save_path = dialog_helpers.get_save_filename(st.session_state['common_path'])

    if save_path:
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            status_text.text("讀取影像中 (Reading images)...")
            
            # Read first image for metadata
            first_img = tifffile.imread(files[0])
            dim_y, dim_x = first_img.shape
            dim_z = len(files)
            dtype = first_img.dtype
            
            amira_type = "float"
            if np.issubdtype(dtype, np.integer):
                amira_type = "int"
            
            # Bounding Box
            bb_xmin, bb_xmax = 0.0, float((dim_x - 1) * vox_x)
            bb_ymin, bb_ymax = 0.0, float((dim_y - 1) * vox_y)
            bb_zmin, bb_zmax = 0.0, float((dim_z - 1) * vox_z)
            
            header = f"""# AmiraMesh 3D ASCII 2.0

define Lattice {dim_x} {dim_y} {dim_z}

Parameters {{
    Content "{dim_x}x{dim_y}x{dim_z} {amira_type}, uniform coordinates",
    BoundingBox {bb_xmin:.6f} {bb_xmax:.6f} {bb_ymin:.6f} {bb_ymax:.6f} {bb_zmin:.6f} {bb_zmax:.6f},
    CoordType "uniform"
}}

Lattice {{ {amira_type} Data }} @1

# Data section follows
@1
"""
            status_text.text(f"正在寫入 Header 到 {os.path.basename(save_path)}...")
            
            with open(save_path, 'w') as f:
                f.write(header)
                
                status_text.text("正在處理與寫入數據 (ASCII 格式較慢，請稍候)...")
                
                for z, file_path in enumerate(files):
                    img = tifffile.imread(file_path)
                    flat_data = img.flatten()
                    
                    if amira_type == 'int':
                         str_data = '\n'.join(map(str, flat_data))
                    else:
                         str_data = '\n'.join([f"{v:.6f}" for v in flat_data])

                    f.write(str_data)
                    f.write('\n')
                    
                    progress_bar.progress((z + 1) / dim_z)
            
            progress_bar.progress(100)
            status_text.success(f"成功轉檔! 檔案儲存於: {save_path}")
            st.balloons()
            
        except Exception as e:
            st.error(f"轉檔失敗: {str(e)}")
    else:
        st.warning("已取消儲存 (Save cancelled)")
