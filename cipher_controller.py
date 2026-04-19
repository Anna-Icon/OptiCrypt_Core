from tkinter import filedialog, messagebox
import tkinter as tk
from model import CipherEngine
from pypdf import PdfReader, PdfWriter
import docx
import os
import json  # لقراءة السجلات وعرضها بشكل جميل
import uuid
from datetime import datetime
from vault_manager import VaultManager
# 👈 استيراد نظام الحماية لتسجيل الحركات
from system_auth import SystemAuth


class CipherController:
    def __init__(self, view,username):
        self.view = view
        self.vault = VaultManager(process_type="Secure") #التعرف على الخزن
        self.current_user = username
        self.auth = SystemAuth()  # إنشاء نسخة من الحماية للوصول للسجلات
        self.is_logged_out = False
        # ربط زر تسجيل الخروج
        self.view.btn_logout.config(command=self.logout)
        # ربط أزرار النص
        self.view.btn_encrypt.config(command=self.encrypt)
        self.view.btn_decrypt.config(command=self.decrypt)

        # ربط أزرار الملفات وسجلات الأدمن (فقط إذا كانت موجودة)
        if self.view.is_admin:
            self.view.btn_encrypt_file.config(command=self.file_encrypt)
            self.view.btn_decrypt_file.config(command=self.file_decrypt)
            self.view.btn_users_log.config(command=self.show_users_log)
            self.view.btn_activity_log.config(command=self.show_activity_log)

    # ================= LOG ACTION =================
    def record_action(self, action_name):
        """دالة مساعدة لتسجيل أي حركة يقوم بها المستخدم"""
        self.auth.log_activity(self.view.username, action_name, self.get_mode())

    # ================= ADMIN LOGS DISPLAY =================
    def show_users_log(self):
        log_window = tk.Toplevel(self.view.root)
        log_window.title("Registered Users Log")
        log_window.geometry("400x300")

        text_area = tk.Text(log_window, wrap="word")
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

        users_data = self.auth.users
        reg_dates = self.auth.registration_dates

        for user, pwd in users_data.items():
            date = reg_dates.get(user, "Unknown")
            text_area.insert(tk.END, f"👤 User: {user}\n🔑 Password: {pwd}\n📅 Registered: {date}\n{'-' * 30}\n")
        text_area.config(state="disabled")

    def show_activity_log(self):
        log_window = tk.Toplevel(self.view.root)
        log_window.title("System Activity Log")
        log_window.geometry("600x400")

        text_area = tk.Text(log_window, wrap="word")
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

        logs = self.auth.activity_logs
        for log in reversed(logs):  # عرض الأحدث أولاً
            formatted_log = json.dumps(log, indent=2)
            text_area.insert(tk.END, formatted_log + "\n" + "=" * 40 + "\n")
        text_area.config(state="disabled")

    # ================= KEY & ENGINE =================
    # ... (ضع نفس دوال get_key, get_engine, get_mode التي كتبناها في الردود السابقة هنا بدون تغيير) ...
    def get_key(self):
        mode = self.get_mode()
        raw_key = self.view.ent_key.get().strip()

        if mode in ["caesar", "xor"]:
            try:
                return int(raw_key)
            except ValueError:
                messagebox.showerror("Error", "This cipher requires an integer key!")
                return None
        elif mode == "vigenere":
            if not raw_key:
                messagebox.showerror("Error", "This cipher requires a text key!")
                return None
            return str(raw_key)
        return None

    def get_engine(self):
        mode = self.get_mode()
        key = self.get_key()
        if mode in ["caesar", "xor", "vigenere"] and key is None: return None
        return CipherEngine(key)

    def get_mode(self):
        return self.view.cipher_type.get()

    # ================= TEXT =================
    def encrypt(self):
        text = self.view.ent_message.get()
        engine = self.get_engine()
        if not engine and self.get_mode() in ["caesar", "xor", "vigenere"]: return
        mode = self.get_mode()
        self.view.lbl_output.config(text=self.apply_encrypt(engine, mode, text))

        # تجهيز بيانات السجل

        record_data = {
            "id": str(uuid.uuid4())[:8],
            "agent": self.current_user,
            "timestamp": str(datetime.now())
        }

        # استدعاء الحفظ في ملف JSON
        self.vault.save_record(record_data)

        # إبقاء تسجيل الحركة البسيطة للواجهة
        self.record_action(f"Encrypted using {self.get_mode()}")

    # 👈 تسجيل الحركة

    def decrypt(self):
        text = self.view.ent_message.get()
        engine = self.get_engine()
        if not engine and self.get_mode() in ["caesar", "xor", "vigenere"]: return
        mode = self.get_mode()
        self.view.lbl_output.config(text=self.apply_decrypt(engine, mode, text))

        # تجهيز بيانات فك التشفير

        dec_record = {
            "id": str(uuid.uuid4())[:8],
            "agent": self.current_user,
            "operation": "Decryption",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.vault.save_record(dec_record)  # حفظ في JSON
        # 👈 تسجيل الحركة

    # ================= APPLY =================
    def apply_encrypt(self, engine, mode, text):
        if mode == "caesar":
            return engine.caesar_encrypt(text)
        elif mode == "reverse":
            return engine.reverse_encrypt(text)
        elif mode == "xor":
            return engine.xor(text)
        elif mode == "rot13":
            return engine.rot13(text)
        elif mode == "base64":
            return engine.base64_encode(text)
        elif mode == "vigenere":
            return engine.vigenere_encrypt(text)
        return "Unsupported"


    def apply_decrypt(self, engine, mode, text):
        if mode == "caesar":
            return engine.caesar_decrypt(text)
        elif mode == "reverse":
            return engine.reverse_decrypt(text)
        elif mode == "xor":
            return engine.xor(text)
        elif mode == "rot13":
            return engine.rot13(text)
        elif mode == "base64":
            return engine.base64_decode(text)
        elif mode == "vigenere":
            return engine.vigenere_decrypt(text)
        return "Unsupported"

    # ================= FILE =================
    def file_encrypt(self):
        self.process_file("enc")
        self.record_action("Encrypt File")  # 👈 تسجيل الحركة

    def file_decrypt(self):
        self.process_file("dec")
        self.record_action("Decrypt File")  # 👈 تسجيل الحركة

    def process_file(self, mode):
        # ... (نفس كود process_file و handle_txt و handle_docx و handle_pdf السابق بالكامل، ضعه هنا) ...
        pass  # تذكر وضع الأكواد الخاصة بالملفات هنا كما في الردود السابقة


        # ================= LOGOUT =================
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.record_action("Logged Out")  # 👈 تسجيل حركة الخروج في السجلات
            self.is_logged_out = True  # 👈 تأكيد أن الإغلاق بسبب الخروج وليس زر الـ X
            self.view.root.destroy()  # 👈 إغلاق النافذة الحالية
