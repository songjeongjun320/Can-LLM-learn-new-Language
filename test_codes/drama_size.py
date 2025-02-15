from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time

# .env 파일 로드
load_dotenv()

# 환경 변수에서 ID와 PW 읽어오기
netflix_id = os.getenv("NETFLIX_ID")
netflix_pw = os.getenv("NETFLIX_PW")

# 웹 드라이버 실행
driver = webdriver.Chrome()

# 넷플릭스 로그인 페이지로 이동
url = 'https://www.netflix.com/login'
driver.get(url)

# ID와 PW 입력 및 로그인 시도
try:
    # 이메일 입력란 찾기
    email_input = driver.find_element(By.NAME, "userLoginId")
    email_input.send_keys(netflix_id)
    
    # 비밀번호 입력란 찾기
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(netflix_pw)
    
    # 로그인 버튼 클릭
    password_input.send_keys(Keys.RETURN)
    
    # 로그인 후 페이지가 로드될 때까지 잠시 대기
    time.sleep(5)

    print("자동 로그인 성공!")

except Exception as e:
    print(f"로그인 오류: {e}")

# 넷플릭스 드라마 페이지로 이동 (이 부분을 수동으로 설정한 URL로 대체)
url = 'https://www.netflix.com/watch/81618456'  # 원하는 드라마의 URL을 입력
driver.get(url)

# 비디오가 로드될 때까지 기다리기
time.sleep(5)  # 비디오 로드 대기 (시간 조정 필요할 수 있음)

# 슬라이더 요소 찾기
try:
    # 현재 시간과 전체 시간을 담고 있는 슬라이더 찾기
    slider = driver.find_element(By.CSS_SELECTOR, "button[aria-label='재생 시간 표시줄']")  # 해당 버튼 찾기
    aria_value = driver.find_element(By.CSS_SELECTOR, "div[aria-valuetext]")  # aria-valuetext 값 찾기
    
    # 전체 비디오 길이와 현재 재생 시간 추출 (초 단위)
    total_time = int(aria_value.get_attribute('aria-valuemax'))  # 전체 시간
    current_time = int(aria_value.get_attribute('aria-valuenow'))  # 현재 시간

    # 목표 시간 설정 (예: 2분 7초 = 127초)
    target_time = 127

    # 목표 시간으로 이동할 비율 계산
    move_ratio = target_time / total_time

    # 슬라이더 크기 가져오기
    slider_width = slider.size['width']

    # 이동할 거리 계산
    move_distance = move_ratio * slider_width

    # 슬라이더를 해당 위치로 이동
    actions = ActionChains(driver)
    actions.click_and_hold(slider).move_by_offset(move_distance, 0).release().perform()

    print(f"슬라이더를 {target_time}초로 이동 완료")

except Exception as e:
    print(f"슬라이더 이동 오류: {e}")

# 드라이버 종료
driver.quit()
