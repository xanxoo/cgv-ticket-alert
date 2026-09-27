import os
import smtplib
import time
from email.mime.text import MIMEText
import requests

# ----------------------------------------------------
# Target 설정: 극장판 치이카와-인어 섬의 비밀 / CGV 왕십리 & CGV 용산아이파크몰
# ----------------------------------------------------
MOVIE_NAME = "극장판 치이카와-인어 섬의 비밀"
THEATERS = ["CGV 왕십리", "CGV 용산아이파크몰"]
RECEIVER_EMAIL = "gsgg2390219@gmail.com"

# CGV 예매 관련 페이지/API URL
TARGET_URL = "https://m.cgv.co.kr/WebApp/Reservation/"

# 감지 주기 설정 (10초마다 확인)
CHECK_INTERVAL = 10 
# 1회 실행당 감시할 총 시간 (5분간 지속 감시 후 종료)
TOTAL_RUN_TIME = 300 

def check_movie_open():
    """
    CGV 예매 페이지를 확인하여 '치이카와' 예매가 오픈되었는지 체크합니다.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        response = requests.get(TARGET_URL, headers=headers, timeout=5)
        
        # 키워드 검사 (치이카와 또는 인어 섬 관련 키워드 포함 여부)
        if "치이카와" in response.text or "인어 섬" in response.text:
            return True
    except Exception as e:
        print(f"체크 중 오류: {e}")
    return False

def send_email_alert(sender_email, app_password):
    theaters_str = ", ".join(THEATERS)
    subject = f"🎬 [{theaters_str}] {MOVIE_NAME} 예매 오픈 알림!"
    body = (
        f"요청하신 영화의 예매가 오픈된 것으로 감지되었습니다!\n\n"
        f"- 영화명: {MOVIE_NAME}\n"
        f"- 대상 극장: {theaters_str}\n"
        f"- 예매 링크: {TARGET_URL}\n\n"
        f"지금 바로 접속해서 예매를 진행하세요!"
    )
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = RECEIVER_EMAIL
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, RECEIVER_EMAIL, msg.as_string())
        print(f"{RECEIVER_EMAIL}(으)로 성공적으로 알림 메일을 보냈습니다.")
    except Exception as e:
        print(f"이메일 발송 실패: {e}")

if __name__ == "__main__":
    theaters_str = ", ".join(THEATERS)
    print(f"[{theaters_str}] '{MOVIE_NAME}' 초고속 감지 시작 ({CHECK_INTERVAL}초 간격)...")
    
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_pw = os.environ.get("GMAIL_APP_PASSWORD")
    
    start_time = time.time()
    
    # 5분 동안 계속 반복 감시
    while time.time() - start_time < TOTAL_RUN_TIME:
        if check_movie_open():
            print("🎉 예매 오픈 감지됨!")
            if gmail_user and gmail_pw:
                send_email_alert(gmail_user, gmail_pw)
            break
        
        print(f"[{time.strftime('%H:%M:%S')}] 미오픈 상태... {CHECK_INTERVAL}초 후 재확인")
        time.sleep(CHECK_INTERVAL)
