import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from tkinter import ttk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ===== DATABASE =====
conn = sqlite3.connect("nhansu.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS NhanSu (
    CCCD TEXT PRIMARY KEY,
    HoTen TEXT,
    NgaySinh TEXT,
    GioiTinh TEXT,
    DiaChi TEXT
)
""")
conn.commit()

# ===== FUNCTION =====
def clear_input():
    txt_cccd.delete(0, 'end')
    txt_ten.delete(0, 'end')
    txt_diachi.delete(0, 'end')
    txt_tim.delete(0, 'end')
    cb_gioitinh.set("")

def validate():
    if txt_cccd.get() == "" or txt_ten.get() == "":
        messagebox.showwarning("Lỗi", "Không được để trống CCCD hoặc Họ tên")
        return False
    return True

def load_data(keyword=""):
    for row in tree.get_children():
        tree.delete(row)

    if keyword == "":
        cursor.execute("SELECT * FROM NhanSu")
    else:
        cursor.execute("""
        SELECT * FROM NhanSu 
        WHERE CCCD LIKE ?
        """, ('%' + keyword + '%',))

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def them():
    if not validate(): return
    try:
        cursor.execute("INSERT INTO NhanSu VALUES (?, ?, ?, ?, ?)",
                       (txt_cccd.get(), txt_ten.get(), date_ngaysinh.get(),
                        cb_gioitinh.get(), txt_diachi.get()))
        conn.commit()
        load_data()
        messagebox.showinfo("OK", "Thêm thành công")
    except:
        messagebox.showerror("Lỗi", "CCCD đã tồn tại!")

def sua():
    if not validate(): return
    cursor.execute("""
    UPDATE NhanSu SET HoTen=?, NgaySinh=?, GioiTinh=?, DiaChi=? WHERE CCCD=?
    """, (txt_ten.get(), date_ngaysinh.get(), cb_gioitinh.get(),
          txt_diachi.get(), txt_cccd.get()))
    conn.commit()
    load_data()
    messagebox.showinfo("OK", "Sửa thành công")

def xoa():
    if txt_cccd.get() == "":
        return
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?"):
        cursor.execute("DELETE FROM NhanSu WHERE CCCD=?", (txt_cccd.get(),))
        conn.commit()
        load_data()

def tim():
    load_data(txt_tim.get())

def chon_dong(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        txt_cccd.delete(0, 'end')
        txt_cccd.insert(0, values[0])
        txt_ten.delete(0, 'end')
        txt_ten.insert(0, values[1])
        date_ngaysinh.set_date(values[2])
        cb_gioitinh.set(values[3])
        txt_diachi.delete(0, 'end')
        txt_diachi.insert(0, values[4])

# ===== UI =====
root = ctk.CTk()
root.title("Quản lý nhân sự")
root.geometry("900x550")

frame_left = ctk.CTkFrame(root)
frame_left.pack(side="left", padx=10, pady=10)

frame_right = ctk.CTkFrame(root)
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# INPUT
ctk.CTkLabel(frame_left, text="CCCD").pack()
txt_cccd = ctk.CTkEntry(frame_left)
txt_cccd.pack()

ctk.CTkLabel(frame_left, text="Họ tên").pack()
txt_ten = ctk.CTkEntry(frame_left)
txt_ten.pack()

ctk.CTkLabel(frame_left, text="Ngày sinh").pack()
date_ngaysinh = DateEntry(frame_left, date_pattern='yyyy-mm-dd')
date_ngaysinh.pack()

ctk.CTkLabel(frame_left, text="Giới tính").pack()
cb_gioitinh = ctk.CTkComboBox(frame_left, values=["Nam", "Nữ"])
cb_gioitinh.pack()

ctk.CTkLabel(frame_left, text="Địa chỉ").pack()
txt_diachi = ctk.CTkEntry(frame_left)
txt_diachi.pack()

# BUTTON
ctk.CTkButton(frame_left, text="Thêm", command=them).pack(pady=5)
ctk.CTkButton(frame_left, text="Sửa", command=sua).pack(pady=5)
ctk.CTkButton(frame_left, text="Xóa", command=xoa).pack(pady=5)
ctk.CTkButton(frame_left, text="Clear", command=clear_input).pack(pady=5)

# SEARCH
txt_tim = ctk.CTkEntry(frame_right, placeholder_text="Nhập CCCD cần tìm...")
txt_tim.pack(pady=5)

# 🔥 TÌM REALTIME THEO CCCD
txt_tim.bind("<KeyRelease>", lambda event: load_data(txt_tim.get()))

ctk.CTkButton(frame_right, text="Tìm kiếm", command=tim).pack()

# TABLE
tree = ttk.Treeview(frame_right, columns=("CCCD", "Tên", "Ngày sinh", "Giới tính", "Địa chỉ"), show="headings")

for col in tree["columns"]:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)
tree.bind("<ButtonRelease-1>", chon_dong)

load_data()

root.mainloop()