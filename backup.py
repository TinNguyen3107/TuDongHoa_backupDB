import os
import schedule
import time
import smtplib
import ssl
import shutil
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_NGUOI_GOI = os.getenv("EMAIL_NGUOI_GOI")
MAT_KHAU = os.getenv("MAT_KHAU")
EMAIL_NGUOI_NHAN = os.getenv("EMAIL_NGUOI_NHAN")

DB_FILE = "fileTest/database.sqlite3"

def send_email(subject, content):
    msg = EmailMessage()
    msg['From'] = EMAIL_NGUOI_GOI
    msg['To'] = EMAIL_NGUOI_NHAN
    msg['Subject'] = subject
    msg.set_content(content)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_NGUOI_GOI, MAT_KHAU)
            server.send_message(msg)
        print("Đã gửi email thông báo.")
    except Exception as e:
        print(f"Không thể gửi email: {e}")

def backup_database():
    try:
        backup_dir = "backup"
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir)
        shutil.copy(DB_FILE, backup_file)

        send_email(
            subject="Backup thành công",
            content=f"Đã backup database thành công"
        )
        print(f"Backup thành công")
    except Exception as e:
        send_email(
            subject="Backup thất bại",
            content=f"Đã xảy ra lỗi khi backup database"
        )
        print(f"Lỗi backup: {e}")

# backup_database()

schedule.every().day.at("00:00").do(backup_database)

print("Đang chạy lịch backup")
while True:
    schedule.run_pending()
    time.sleep(5)