import streamlit as st
import pandas as pd

# Định nghĩa tài khoản và mật khẩu
users = {"user1": "123", "user2": "456"}

# Hàm kiểm tra đăng nhập
def check_login(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Đọc file CSV
@st.cache
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Nhom'] = df['Nhom'].astype(str)  # Chuyển cột Nhom sang chuỗi
    return df

# Đường dẫn đến file CSV
file_path = 'student_data.csv'  # Thay bằng đường dẫn thực tế của bạn

# Giao diện đăng nhập
st.title("Quản lý Điểm Sinh viên")
username = st.sidebar.text_input("Tên đăng nhập")
password = st.sidebar.text_input("Mật khẩu", type="password")

if st.sidebar.button("Đăng nhập"):
    if check_login(username, password):
        st.sidebar.success(f"Đăng nhập thành công! Chào {username}.")

        # Tải dữ liệu
        df = load_data(file_path)

        # Người dùng chọn nhóm
        selected_group = st.selectbox("Chọn Nhóm", df['Nhom'].unique())

        # Lọc sinh viên theo nhóm đã chọn
        filtered_df = df[df['Nhom'] == selected_group].copy()

        if not filtered_df.empty:
            st.write(f"Danh sách sinh viên trong Nhóm {selected_group}")

            # Hiển thị bảng để nhập điểm
            edited_df = st.experimental_data_editor(filtered_df, num_rows="dynamic")

            # Nút lưu dữ liệu
            if st.button("Lưu điểm"):
                # Cập nhật dữ liệu mới vào dataframe gốc
                df.update(edited_df)
                df.to_csv(file_path, index=False)
                st.success("Điểm đã được lưu thành công!")
        else:
            st.warning("Không có sinh viên nào trong nhóm này.")
    else:
        st.sidebar.error("Tên đăng nhập hoặc mật khẩu không chính xác.")
