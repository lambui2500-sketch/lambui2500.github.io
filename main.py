import os
from collections import defaultdict

# ================== CLASS ==================
class Employee:
    def __init__(self, emp_id, name, base_salary):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary
        self.performance = 0
        self.projects = []

    def calc_salary(self):
        return self.base_salary

    def __str__(self):
        return f"{self.emp_id} | {self.name} | Lương: {self.calc_salary()} | Điểm: {self.performance}"


class Manager(Employee):
    def calc_salary(self):
        return self.base_salary * 2


class Developer(Employee):
    def __init__(self, emp_id, name, base_salary, language):
        super().__init__(emp_id, name, base_salary)
        self.language = language

    def calc_salary(self):
        return self.base_salary * 1.5


class Intern(Employee):
    def calc_salary(self):
        return self.base_salary * 0.8


# ================== DATA ==================
employees = []


# ================== HELPER ==================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nNhấn Enter để tiếp tục...")


def find_by_id(emp_id):
    for e in employees:
        if e.emp_id == emp_id:
            return e
    return None


# ================== MENU ==================
def menu():
    clear()
    print("=" * 60)
    print("   HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY ".center(60))
    print("=" * 60)
    print("1. Thêm nhân viên")
    print("2. Hiển thị danh sách")
    print("3. Tìm kiếm")
    print("4. Quản lý lương")
    print("5. Quản lý dự án")
    print("6. Đánh giá hiệu suất")
    print("7. Quản lý nhân sự")
    print("8. Thống kê")
    print("9. Thoát")
    print("=" * 60)


# ================== FUNCTION ==================
def add_employee():
    print("\na. Manager\nb. Developer\nc. Intern")
    choice = input("Chọn: ")

    emp_id = input("ID: ")
    name = input("Tên: ")
    salary = float(input("Lương cơ bản: "))

    if choice == 'a':
        employees.append(Manager(emp_id, name, salary))
    elif choice == 'b':
        lang = input("Ngôn ngữ: ")
        employees.append(Developer(emp_id, name, salary, lang))
    elif choice == 'c':
        employees.append(Intern(emp_id, name, salary))

    print("✔ Thêm thành công")


def show_employees():
    print("\na. Tất cả\nb. Theo loại\nc. Theo hiệu suất")
    choice = input("Chọn: ")

    if choice == 'a':
        for e in employees:
            print(e)

    elif choice == 'b':
        typ = input("Nhập loại (Manager/Developer/Intern): ")
        for e in employees:
            if e.__class__.__name__ == typ:
                print(e)

    elif choice == 'c':
        for e in sorted(employees, key=lambda x: x.performance, reverse=True):
            print(e)


def search_employee():
    print("\na. ID\nb. Tên\nc. Ngôn ngữ")
    choice = input("Chọn: ")

    if choice == 'a':
        emp = find_by_id(input("ID: "))
        print(emp if emp else "Không tìm thấy")

    elif choice == 'b':
        name = input("Tên: ")
        for e in employees:
            if name.lower() in e.name.lower():
                print(e)

    elif choice == 'c':
        lang = input("Ngôn ngữ: ")
        for e in employees:
            if isinstance(e, Developer) and e.language == lang:
                print(e)


def salary_management():
    print("\na. Tính lương từng NV\nb. Tổng lương\nc. Top 3 lương cao")
    choice = input("Chọn: ")

    if choice == 'a':
        for e in employees:
            print(e.name, e.calc_salary())

    elif choice == 'b':
        print("Tổng:", sum(e.calc_salary() for e in employees))

    elif choice == 'c':
        top = sorted(employees, key=lambda x: x.calc_salary(), reverse=True)[:3]
        for e in top:
            print(e)


# ================== PROJECT ==================
def project_management():
    print("""
a. Phân công
b. Xóa khỏi dự án
c. Xem dự án
d. Top 10 nhiều dự án
e. Top 10 ít dự án
f. Nhân viên 1 dự án
""")
    choice = input("Chọn: ")

    if choice == 'a':
        emp = find_by_id(input("ID: "))
        if emp:
            p = input("Tên dự án: ")
            emp.projects.append(p)

    elif choice == 'b':
        emp = find_by_id(input("ID: "))
        if emp:
            p = input("Tên dự án: ")
            if p in emp.projects:
                emp.projects.remove(p)

    elif choice == 'c':
        emp = find_by_id(input("ID: "))
        if emp:
            print(emp.projects)

    elif choice == 'd':
        top = sorted(employees, key=lambda x: len(x.projects), reverse=True)[:10]
        for e in top:
            print(e.name, len(e.projects))

    elif choice == 'e':
        top = sorted(employees, key=lambda x: len(x.projects))[:10]
        for e in top:
            print(e.name, len(e.projects))

    elif choice == 'f':
        for e in employees:
            if len(e.projects) == 1:
                print(e.name, "|", e.__class__.__name__)


# ================== PERFORMANCE ==================
def performance_management():
    print("\na. Cập nhật\nb. Xuất sắc\nc. Cần cải thiện")
    choice = input("Chọn: ")

    if choice == 'a':
        emp = find_by_id(input("ID: "))
        if emp:
            emp.performance = float(input("Điểm: "))

    elif choice == 'b':
        for e in employees:
            if e.performance > 8:
                print(e)

    elif choice == 'c':
        for e in employees:
            if e.performance < 5:
                print(e)


# ================== HR ==================
def hr_management():
    print("""
a. Xóa nhân viên
b. Tăng lương
c. Thăng chức
d. Cắt giảm nhân sự
""")
    choice = input("Chọn: ")

    if choice == 'a':
        emp = find_by_id(input("ID: "))
        if emp:
            employees.remove(emp)

    elif choice == 'b':
        emp = find_by_id(input("ID: "))
        if emp:
            emp.base_salary += float(input("Tăng thêm: "))

    elif choice == 'c':
        emp = find_by_id(input("ID: "))
        if isinstance(emp, Intern):
            employees.remove(emp)
            employees.append(Developer(emp.emp_id, emp.name, emp.base_salary, "Python"))

        elif isinstance(emp, Developer):
            employees.remove(emp)
            employees.append(Manager(emp.emp_id, emp.name, emp.base_salary))

    elif choice == 'd':
        # ✅ FIX LỖI Ở ĐÂY
        employees[:] = [e for e in employees if e.performance >= 5]
        print("✔ Đã cắt giảm nhân sự yếu")


# ================== REPORT ==================
def report():
    print("\na. Theo loại\nb. Tổng lương\nc. TB dự án")
    choice = input("Chọn: ")

    if choice == 'a':
        d = defaultdict(int)
        for e in employees:
            d[e.__class__.__name__] += 1
        print(dict(d))

    elif choice == 'b':
        print(sum(e.calc_salary() for e in employees))

    elif choice == 'c':
        if employees:
            avg = sum(len(e.projects) for e in employees) / len(employees)
            print("Trung bình:", avg)


# ================== MAIN ==================
while True:
    menu()
    choice = input("Chọn: ")

    if choice == '1':
        add_employee()
    elif choice == '2':
        show_employees()
    elif choice == '3':
        search_employee()
    elif choice == '4':
        salary_management()
    elif choice == '5':
        project_management()
    elif choice == '6':
        performance_management()
    elif choice == '7':
        hr_management()
    elif choice == '8':
        report()
    elif choice == '9':
        break

    pause()