import tkinter as tk
from tkinter import font


class CipherView:
    # 👈 نستقبل اسم المستخدم وحالة الأدمن من شاشة تسجيل الدخول
    def __init__(self, root, username="", is_admin=False):
        self.root = root
        self.username = username
        self.is_admin = is_admin

        self.root.title(f"Cyber Cipher Tool - User: {self.username}")
        # 👈 نكبر حجم النافذة قليلاً لتسع أزرار الأدمن
        self.root.geometry("500x550" if is_admin else "500x400")
        self.root.configure(bg="#1e1e2f")

        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)

        # تغيير لون العنوان إذا كان أدمن
        title_text = "🔐 Cyber Cipher Tool (ADMIN)" if is_admin else "🔐 Cyber Cipher Tool"
        title_color = "#f44336" if is_admin else "white"
        tk.Label(root, text=title_text, font=self.title_font, bg="#1e1e2f", fg=title_color).pack(pady=15)

        # ================= TEXT AREA =================
        tk.Label(root, text="Message:", font=self.label_font, bg="#1e1e2f", fg="white").pack()
        self.ent_message = tk.Entry(root, width=50)
        self.ent_message.pack(pady=5)

        self.lbl_key = tk.Label(root, text="Key (Integer):", font=self.label_font, bg="#1e1e2f", fg="white")
        self.lbl_key.pack()
        self.ent_key = tk.Entry(root, width=20)
        self.ent_key.pack(pady=5)

        btn_frame = tk.Frame(root, bg="#1e1e2f")
        btn_frame.pack(pady=10)
        self.btn_encrypt = tk.Button(btn_frame, text="Encrypt Text", bg="#4caf50", fg="white", width=12)
        self.btn_encrypt.grid(row=0, column=0, padx=10)
        self.btn_decrypt = tk.Button(btn_frame, text="Decrypt Text", bg="#f44336", fg="white", width=12)
        self.btn_decrypt.grid(row=0, column=1, padx=10)

        tk.Label(root, text="Encryption Type:", font=self.label_font, bg="#1e1e2f", fg="white").pack()

        # 👈 الأدمن له 6 طرق، والمستخدم العادي له 3 طرق فقط
        if self.is_admin:
            methods = ["caesar", "reverse", "xor", "rot13", "base64", "vigenere"]
        else:
            methods = ["caesar", "reverse", "rot13"]

        self.cipher_type = tk.StringVar(value=methods[0])
        self.cipher_type.trace_add("write", self.update_ui)
        self.cipher_menu = tk.OptionMenu(root, self.cipher_type, *methods)
        self.cipher_menu.pack(pady=5)

        # ================= ADMIN SECTION (الملفات والسجلات) =================
        self.btn_encrypt_file = None
        self.btn_decrypt_file = None
        self.btn_users_log = None
        self.btn_activity_log = None

        if self.is_admin:
            # 📂 خانة تشفير الملفات
            file_frame = tk.Frame(root, bg="#1e1e2f")
            file_frame.pack(pady=10)
            self.btn_encrypt_file = tk.Button(file_frame, text="Encrypt File", bg="#2196f3", fg="white", width=12)
            self.btn_encrypt_file.grid(row=0, column=0, padx=10)
            self.btn_decrypt_file = tk.Button(file_frame, text="Decrypt File", bg="#9c27b0", fg="white", width=12)
            self.btn_decrypt_file.grid(row=0, column=1, padx=10)

            # 📋 خانة سجلات النظام
            logs_frame = tk.Frame(root, bg="#1e1e2f")
            logs_frame.pack(pady=5)
            self.btn_users_log = tk.Button(logs_frame, text="📋 Users Log", bg="#ff9800", fg="black",
                                           font=("Helvetica", 10, "bold"), width=12)
            self.btn_users_log.grid(row=0, column=0, padx=10)
            self.btn_activity_log = tk.Button(logs_frame, text="🔍 Activity Log", bg="#ff9800", fg="black",
                                              font=("Helvetica", 10, "bold"), width=12)
            self.btn_activity_log.grid(row=0, column=1, padx=10)

        # ================= OUTPUT =================
        self.lbl_output = tk.Label(root, text="Output will appear here", bg="#1e1e2f", fg="#00FF00",
                                   font=("Consolas", 11), wraplength=450)
        self.lbl_output.pack(pady=15)

        # ================= LOGOUT BUTTON =================
        self.btn_logout = tk.Button(root, text="🚪 Logout", bg="#f44336", fg="white", font=("Helvetica", 11, "bold"),
                                    width=10)
        self.btn_logout.pack(pady=10)

    def update_ui(self, *args):
        mode = self.cipher_type.get()
        if mode in ["caesar", "xor"]:
            self.lbl_key.config(text="Key (Integer):")
            self.ent_key.config(state="normal")
        elif mode == "vigenere":
            self.lbl_key.config(text="Key (Text):")
            self.ent_key.config(state="normal")
        else:
            self.lbl_key.config(text="Key (Not Required):")
            self.ent_key.delete(0, tk.END)
            self.ent_key.config(state="disabled")
