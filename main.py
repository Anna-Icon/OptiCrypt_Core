from cipher_view import CipherView
from cipher_controller import CipherController
import tkinter as tk
from login_view import LoginWindow


def start_app():
    # 👈 حلقة تكرارية لكي يبقى البرنامج يعمل إذا سجل المستخدم خروجه
    while True:
        # 1. تشغيل نافذة تسجيل الدخول
        login_root = tk.Tk()
        login_app = LoginWindow(login_root)
        login_root.mainloop()

        # 2. إذا نجح الدخول، نفتح الشاشة الرئيسية
        if login_app.is_authenticated:
            main_root = tk.Tk()
            view = CipherView(main_root, username=login_app.logged_username, is_admin=login_app.is_admin)
            controller = CipherController(view,login_app.logged_username)
            main_root.mainloop()

            # 3. بعد إغلاق الشاشة الرئيسية، نفحص السبب:
            if not controller.is_logged_out:
                # إذا أغلق المستخدم النافذة من زر (X) وليس من زر الخروج، ننهي البرنامج بالكامل
                break

                # إذا كان الخروج بسبب رز "Logout"، ستعاد الحلقة وتفتح شاشة الدخول من جديد
            # (يجب إعادة تعيين متغير الدخول لكي لا يمر مباشرة في الدورة القادمة)
            login_app.is_authenticated = False
        else:
            # إذا أغلق المستخدم شاشة الدخول نفسها من زر (X)، ننهي البرنامج
            break


if __name__ == "__main__":
    start_app()
