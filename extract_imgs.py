from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import timedelta
import os
import time
from PIL import ImageGrab

# Chrome 웹드라이버 실행
driver = webdriver.Chrome()

# 넷플릭스 웹사이트로 이동
driver.get('https://www.netflix.com/')

# 로그인 (수동으로 로그인 후 자동화 시작)
input("로그인 후 Enter 키를 눌러주세요.")

# 특정 드라마와 에피소드로 이동
drama_name = "경성크리처"
episode_number = "1"
driver.get("https://www.netflix.com/watch/81618456")  # 1화의 URL로 이동

timestamp_list = ["00:02:17", "00:02:28", "00:02:31", "00:02:35"]

# 비디오가 로드될 때까지 기다리기
try:
    video_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )
except:
    print("비디오 로드 실패")
    driver.quit()

# 비디오가 로드된 후 Enter 키를 눌러서 스크립트 진행
input("비디오가 실행되면 Enter 키를 눌러주세요.")  # Enter를 눌러야 비디오가 실행된 후 진행

# 각 timestamp에 맞춰서 이동하고 스크린샷을 찍는 함수
def capture_screenshot_at_timestamps():
    for timestamp in timestamp_list:
        hour, minute, second = map(float, timestamp.split(":"))
        target_time = timedelta(hours=hour, minutes=minute, seconds=second)

        # 비디오의 currentTime 속성을 통해 시간을 이동
        driver.execute_script(f"arguments[0].currentTime = {target_time.total_seconds()};", video_element)

        # 시간 이동 후 잠시 대기
        time.sleep(2)  # 2초 기다려서 비디오가 시간대로 이동했는지 확인

        # 스크린샷 파일명 설정
        timestamp_str = timestamp.replace(":", "_")  # "00:02:17" => "00_02_17"
        screenshot_filename = os.path.join(screenshot_folder, f"{drama_name}_{episode_number}_{timestamp_str}.png")

        # 전체 화면 캡처
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_filename)

        print(f"스크린샷이 {screenshot_filename}으로 저장되었습니다.")

# 스크린샷 저장 경로 설정
screenshot_folder = "C:/Users/songj/OneDrive/Desktop/Can-LLM-learn-new-Language/screenshots"
os.makedirs(screenshot_folder, exist_ok=True)  # 폴더가 없으면 생성

# 타임스탬프에 맞춰서 스크린샷을 찍음
capture_screenshot_at_timestamps()

# 브라우저 종료
driver.quit()
