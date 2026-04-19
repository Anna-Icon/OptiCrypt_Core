import os
import json
from datetime import datetime

class SystemAuth:
    def __init__(self):
        self.max_attempts = 3
        self.file_name = "security.json"

        self.users = {}
        self.registration_dates = {}
        self.activity_logs = []
        self.__failed_attempts = {}
        self.__is_locked = {}

        self.__load_security_file()

    # =========================
    # 📂 تحميل البيانات
    # =========================
    def __load_security_file(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                data = json.load(file)

                self.users = data.get("users", {})
                self.registration_dates = data.get("registration_dates", {})
                self.activity_logs = data.get("activity_logs", [])
                self.__failed_attempts = data.get("failed_attempts", {})
                self.__is_locked = data.get("is_locked", {})
        else:
            self.__save_security_file()

    # =========================
    # 💾 حفظ البيانات
    # =========================
    def __save_security_file(self):
        data = {
            "users": self.users,
            "registration_dates": self.registration_dates,
            "activity_logs": self.activity_logs,
            "failed_attempts": self.__failed_attempts,
            "is_locked": self.__is_locked
        }
        with open(self.file_name, 'w') as file:
            json.dump(data, file, indent=4)

    # =========================
    # 🆕 تسجيل حساب
    # =========================
    def register_user(self, username, password):
        if username in self.users:
            return "USER_EXISTS"

        self.users[username] = password
        self.registration_dates[username] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__failed_attempts[username] = 0
        self.__is_locked[username] = False

        self.__save_security_file()
        return "REGISTERED SUCCESSFULLY"

    # =========================
    # 🔐 تسجيل الدخول
    # =========================
    def attempt_login(self, username, entered_password):
        # 👑 فحص حساب الأدمن أولاً
        if username == "gx11" and entered_password == "2026":
            return "GRANTED_ADMIN"

        # فحص المستخدمين العاديين
        if username not in self.users:
            return "USER NOT FOUND"

        if self.__is_locked.get(username, False):
            return "LOCKED"

        if entered_password == self.users[username]:
            self.__failed_attempts[username] = 0
            self.__save_security_file()
            return "GRANTED_NORMAL"

        self.__failed_attempts[username] += 1
        if self.__failed_attempts[username] >= self.max_attempts:
            self.__is_locked[username] = True
            self.__save_security_file()
            return "LOCKED"

        self.__save_security_file()
        return f"DENIED ({self.max_attempts - self.__failed_attempts[username]} attempts left)"

    # =========================
    # 📝 تسجيل حركة التشفير (Activity Log)
    # =========================
    def log_activity(self, username, action, cipher_type):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        password = self.users.get(username, "N/A")
        reg_date = self.registration_dates.get(username, "N/A")

        log_entry = {
            "Time": now,
            "User": username,
            "Password": password,
            "Account_Created": reg_date,
            "Action": action,
            "Cipher_Method": cipher_type
        }
        self.activity_logs.append(log_entry)
        self.__save_security_file()

    def reset_lock(self, username):
        self.__failed_attempts[username] = 0
        self.__is_locked[username] = False
        self.__save_security_file()
