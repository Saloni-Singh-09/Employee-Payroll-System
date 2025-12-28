import os

# File paths
EMPLOYEES_FILE = "employees.txt"
PAYROLL_FILE = "payroll.txt"
HRA_PERCENTAGE = 0.20

class Employee:
    def __init__(self, emp_id, name, basic_salary): # Fixed __init__
        self.emp_id = emp_id
        self.name = name
        self.basic_salary = basic_salary
    
    def calculate_hra(self):
        return self.basic_salary * HRA_PERCENTAGE
    
    def calculate_gross_salary(self):
        return self.basic_salary + self.calculate_hra()
    
    def display_info(self):
        print(f"ID: {self.emp_id} | Name: {self.name} | Basic: ₹{self.basic_salary:.2f}")

    def to_file_string(self):
        return f"{self.emp_id},{self.name},{self.basic_salary}\n"

class PayrollRecord:
    def __init__(self, emp_id, name, month, year, basic, hra, gross): # Fixed __init__
        self.emp_id = emp_id
        self.name = name
        self.month = month
        self.year = year
        self.basic = basic
        self.hra = hra
        self.gross = gross
    
    def display_breakdown(self):
        print(f"\n--- Pay Slip: {self.month}/{self.year} ---")
        print(f"Employee: {self.name} ({self.emp_id})")
        print(f"Basic: ₹{self.basic:.2f} | HRA: ₹{self.hra:.2f}")
        print(f"Gross Total: ₹{self.gross:.2f}\n")

    def to_file_string(self):
        return f"{self.emp_id},{self.name},{self.month},{self.year},{self.basic},{self.hra},{self.gross}\n"

class FileManager:
    @staticmethod
    def load_employees():
        employees = []
        if os.path.exists(EMPLOYEES_FILE):
            with open(EMPLOYEES_FILE, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        employees.append(Employee(parts[0], parts[1], float(parts[2])))
        return employees

    @staticmethod
    def save_employees(employees):
        with open(EMPLOYEES_FILE, 'w') as f:
            for emp in employees:
                f.write(emp.to_file_string())

    @staticmethod
    def save_payroll_record(record):
        with open(PAYROLL_FILE, 'a') as f:
            f.write(record.to_file_string())

    @staticmethod
    def load_payroll_records():
        records = []
        if os.path.exists(PAYROLL_FILE):
            with open(PAYROLL_FILE, 'r') as f:
                for line in f:
                    p = line.strip().split(',')
                    if len(p) == 7:
                        records.append(PayrollRecord(p[0], p[1], p[2], p[3], float(p[4]), float(p[5]), float(p[6])))
        return records

class EmployeeManager:
    def __init__(self): # Fixed __init__
        self.employees = FileManager.load_employees()
    
    def add_employee(self):
        emp_id = input("Enter ID: ")
        if any(e.emp_id == emp_id for e in self.employees):
            print("Error: ID already exists!")
            return
        name = input("Enter Name: ")
        salary = float(input("Enter Basic Salary: "))
        new_emp = Employee(emp_id, name, salary)
        self.employees.append(new_emp)
        FileManager.save_employees(self.employees)
        print("Employee saved!")

    def view_all(self):
        for e in self.employees: e.display_info()

    def find_employee_by_id(self, emp_id):
        return next((e for e in self.employees if e.emp_id == emp_id), None)

class PayrollManager:
    def __init__(self, emp_manager): # Fixed __init__
        self.emp_manager = emp_manager

    def process_payroll(self):
        eid = input("Enter Employee ID: ")
        emp = self.emp_manager.find_employee_by_id(eid)
        if emp:
            m = input("Month (1-12): ")
            y = input("Year: ")
            rec = PayrollRecord(eid, emp.name, m, y, emp.basic_salary, emp.calculate_hra(), emp.calculate_gross_salary())
            rec.display_breakdown()
            FileManager.save_payroll_record(rec)
        else:
            print("Not found!")

class PayrollSystem:
    def __init__(self):
        self.em = EmployeeManager()
        self.pm = PayrollManager(self.em)

    def run(self):
        while True:
            print("\n1. Add Emp | 2. View All | 3. Process Payroll | 4. Exit")
            ch = input("Choice: ")
            if ch == '1': self.em.add_employee()
            elif ch == '2': self.em.view_all()
            elif ch == '3': self.pm.process_payroll()
            elif ch == '4': break

if __name__ == "__main__":
    PayrollSystem().run()