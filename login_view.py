import tkinter as tk
from tkinter import messagebox
import winsound
from system_auth import SystemAuth


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber-Guard Auth")
        self.root.geometry("400x350")
        self.root.configure(bg="black")

        self.auth_system = SystemAuth()
        self.is_authenticated = False

        # 👈 متغيرات جديدة لحفظ بيانات الدخول
        self.is_admin = False
        self.logged_username = ""

        # 🧠 العنوان
        tk.Label(root, text="SYSTEM LOCKED", bg="black",
                 fg="#00FF00", font=("Consolas", 18, "bold")).pack(pady=15)

        # 👤 Username
        tk.Label(root, text="Username", bg="black", fg="#00FF00").pack()
        self.ent_user = tk.Entry(root, width=20, font=("Consolas", 14), bg="#222", fg="#00FF00")
        self.ent_user.pack(pady=5)

        # 🔐 Password
        tk.Label(root, text="Password", bg="black", fg="#00FF00").pack()
        self.ent_pass = tk.Entry(root, show="*", width=20, font=("Consolas", 14), bg="#222", fg="#00FF00")
        self.ent_pass.pack(pady=5)

        # 🔘 الأزرار
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=15)

        self.btn_login = tk.Button(btn_frame, text="LOGIN", bg="#00FF00", fg="black", font=("Consolas", 12, "bold"),
                                   width=10, command=self.check_login)
        self.btn_login.grid(row=0, column=0, padx=10)

        self.btn_register = tk.Button(btn_frame, text="REGISTER", bg="#2196f3", fg="white",
                                      font=("Consolas", 12, "bold"), width=10, command=self.register)
        self.btn_register.grid(row=0, column=1, padx=10)

        # 📢 الحالة
        self.lbl_status = tk.Label(root, text="Enter Username & Password...", bg="black", fg="#00FF00",
                                   font=("Consolas", 10))
        self.lbl_status.pack(pady=5)

    # 🔑 تسجيل الدخول
    def check_login(self):
        username = self.ent_user.get()
        password = self.ent_pass.get()

        result = self.auth_system.attempt_login(username, password)

        # 👈 التعديل هنا لتمييز الأدمن عن المستخدم العادي
        if result == "GRANTED_ADMIN":
            self.is_authenticated = True
            self.is_admin = True
            self.logged_username = username
            messagebox.showinfo("Access Granted", "Welcome to Cyber-Guard Terminal, ADMIN.")
            self.root.destroy()

        elif result == "GRANTED_NORMAL":
            self.is_authenticated = True
            self.is_admin = False
            self.logged_username = username
            messagebox.showinfo("Access Granted", f"Welcome {username}.")
            self.root.destroy()

        elif "LOCKED" in result:
            self.trigger_panic_mode()

        else:
            self.lbl_status.config(text=result, fg="red")

    # 🆕 تسجيل حساب
    def register(self):
        username = self.ent_user.get()
        password = self.ent_pass.get()

        if not username or not password:
            messagebox.showwarning("Error", "Enter username and password!")
            return

        result = self.auth_system.register_user(username, password)

        if "SUCCESSFULLY" in result or "successfully" in result.lower():
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

    # 🚨 وضع الطوارئ
    def trigger_panic_mode(self):
        self.root.configure(bg="red")
        self.lbl_status.config(text="INTRUDER DETECTED! SYSTEM LOCKDOWN!", fg="white", bg="red",
                               font=("Consolas", 12, "bold"))
        self.btn_login.config(state="disabled")
        self.btn_register.config(state="disabled")
        self.ent_pass.config(state="disabled")
        self.ent_user.config(state="disabled")
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
