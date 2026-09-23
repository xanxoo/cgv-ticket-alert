import os
import smtplib
import time
from email.mime.text import MIMEText
import requests

MOVIE_NAME = "극장판 치이카와-인어 섬의 비밀"
THEATER_NAME = "CGV 왕십리"
RECEIVER_EMAIL = "gsgg2390219@gmail.com"
TARGET_URL = "https://m.cgv.co.kr/WebApp/Reservation/"

# 감지 주기 설정 (초 단위: 10초마다 확인)
CHECK_INTERVAL = 10 
# 1회 실행당 감시할 총 시간 (초 단위: 5분간 지속 감시 후 종료)
TOTAL_RUN_TIME = 300 

def check_movie_open():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        response = requests.get(TARGET_URL, headers=headers, timeout=5)
        
        if "치이카와" in response.text or "인어 섬" in response.text:
            return True
    except Exception as e:
        print(f"체크 중 오류: {e}")
    return False

def send_email_alert(sender_email, app_password):
    subject = f"🎬 [{THEATER_NAME}] {MOVIE_NAME} 예매 오픈 알림!"
    body = f"요청하신 영화의 예매가 오픈되었습니다!\n\n예매 링크: {TARGET_URL}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = RECEIVER_EMAIL
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, RECEIVER_EMAIL, msg.as_string())
        print(f"{RECEIVER_EMAIL}로 알림 전송 완료!")
    except Exception as e:
        print(f"이메일 발송 실패: {e}")

if __name__ == "__main__":
    print(f"[{THEATER_NAME}] '{MOVIE_NAME}' 초고속 감지 시작 ({CHECK_INTERVAL}초 간격)...")
    
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_pw = os.environ.get("GMAIL_APP_PASSWORD")
    
    start_time = time.time()
    
    # 설정한 시간(5분) 동안 계속 반복 감시
    while time.time() - start_time < TOTAL_RUN_TIME:
        if check_movie_open():
            print("🎉 예매 오픈 감지됨!")
            if gmail_user and gmail_pw:
                send_email_alert(gmail_user, gmail_pw)
            break
        
        print(f"[{time.strftime('%H:%M:%S')}] 미오픈 상태... {CHECK_INTERVAL}초 후 재확인")
        time.sleep(CHECK_INTERVAL)
