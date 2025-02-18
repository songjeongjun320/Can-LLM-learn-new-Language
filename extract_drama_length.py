from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#########################################################
# 로그인 자동화
#########################################################

# .env 파일 로드
load_dotenv()

# 환경 변수에서 ID와 PW 읽어오기
netflix_id = os.getenv("NETFLIX_ID")
netflix_pw = os.getenv("NETFLIX_PW")
netflix_profile_name = os.getenv("NETFLIX_PROFILE_NAME")
netflix_profile_pw0 = os.getenv("NETFLIX_PROFILE_PW0")
netflix_profile_pw1 = os.getenv("NETFLIX_PROFILE_PW1")
netflix_profile_pw2 = os.getenv("NETFLIX_PROFILE_PW2")
netflix_profile_pw3 = os.getenv("NETFLIX_PROFILE_PW3")

# 웹 드라이버 실행
driver = webdriver.Chrome()

# 넷플릭스 로그인 페이지로 이동
url = 'https://www.netflix.com/login'
print("--LOG : 넷플릭스 로그인 페이지로 이동 중...")
driver.get(url)

# ID와 PW 입력 및 로그인 시도
try:
    # 이메일 입력란 찾기
    print("--LOG : 이메일 입력란 찾기...")
    email_input = driver.find_element(By.NAME, "userLoginId")
    email_input.send_keys(netflix_id)
    
    # 비밀번호 입력란 찾기
    print("--LOG : 비밀번호 입력란 찾기...")
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(netflix_pw)
    
    # 로그인 버튼 클릭
    print("--LOG : 로그인 버튼 클릭 시도...")
    password_input.send_keys(Keys.RETURN)

    # 프로필 선택 화면이 로드될 때까지 대기
    print("--LOG : 프로필 선택 화면 대기...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-name"))
    )

    # 프로필 선택
    print("--LOG : 프로필 선택 시도...")
    profiles = driver.find_elements(By.CLASS_NAME, "profile-name")
    for profile in profiles:
        if profile.text == netflix_profile_name:
            profile.click()
            break

    # 4자리 비밀번호 입력
    print("--LOG : 4자리 비밀번호 입력 시도...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pin-input-container"))
    )

    # 각 PIN 입력 필드에 값을 입력
    pin_inputs = driver.find_elements(By.CLASS_NAME, "pin-number-input")
    pin_inputs[0].send_keys(netflix_profile_pw0)
    pin_inputs[1].send_keys(netflix_profile_pw1)
    pin_inputs[2].send_keys(netflix_profile_pw2)
    pin_inputs[3].send_keys(netflix_profile_pw3)

    # PIN 입력 후 Enter 키 전송 (필요한 경우)
    pin_inputs[3].send_keys(Keys.RETURN)

except Exception as e:
    print(f"--LOG : 에러 발생 - {e}")

print(f"--LOG : 로그인 자동화 완료")
time.sleep(5)

#########################################################
# 로그인 자동화 완료, 드라마 검색 이후 페이지 이동
#########################################################

# drama_title.txt에서 첫 번째 줄 읽기
with open('drama_title.txt', 'r', encoding='utf-8') as file:
    drama_title = file.readline().strip()

try:
    # search-icon 클래스를 가진 검색 버튼 클릭
    search_button = driver.find_element(By.CLASS_NAME, "search-icon")
    search_button.click()

    # 검색창 요소 찾기 (검색창의 입력 필드 찾기)
    search_box = driver.find_element(By.CLASS_NAME, "searchBox")
    
    # 검색창에 drama_title 입력 후 엔터
    search_box.send_keys(drama_title)
    time.sleep(5)
    ###################
    # 여기부터 재작성 해야하는데, 검색한 이후에
    # 엔터키 누르는게 아니라, 제목만 넣어논 이후에
    # 가장 첫번째 드라마 클릭하는 코드로 변경해야함
    ##################
    search_box.send_keys(Keys.RETURN)

    print(f"'{drama_title}' 검색 완료!")

    # 검색 결과 대기 (적절한 시간 설정)
    time.sleep(5)

except Exception as e:
    print(f"오류 발생: {e}")

print(f"--LOG : 드라마 검색 성공", drama_title)
time.sleep(10)

#########################################################
# 드라마 검색 이후 페이지 이동, 드라마 길이 추출
#########################################################
while True:
    try:
        # LTR-1QTCBDE 클래스에서 시간 데이터 추출
        time_remaining = driver.find_element(By.CLASS_NAME, "ltr-1qtcbde").text
        print(f"남은 시간: {time_remaining}")
        
        # 시간이 '0'인 경우 종료
        if time_remaining == "0":
            print("시간이 0이 되어 종료됩니다.")
            break
        
        # 1초 대기 후 다시 시도
        time.sleep(1)
    except Exception as e:
        print(f"오류 발생: {e}")
        break
#########################################################
# 드라마 길이 추출
#########################################################


# 슬라이더 요소 찾기
try:
    print("--LOG : 슬라이더 요소 찾기...")
    # 현재 시간과 전체 시간을 담고 있는 슬라이더 찾기
    slider = driver.find_element(By.CSS_SELECTOR, "button[aria-label='재생 시간 표시줄']")  # 해당 버튼 찾기
    aria_value = driver.find_element(By.CSS_SELECTOR, "div[aria-valuetext]")  # aria-valuetext 값 찾기
    
    # 전체 비디오 길이와 현재 재생 시간 추출 (초 단위)
    print("--LOG : 전체 비디오 길이와 현재 재생 시간 추출 중...")
    total_time = int(aria_value.get_attribute('aria-valuemax'))  # 전체 시간
    current_time = int(aria_value.get_attribute('aria-valuenow'))  # 현재 시간

    # 목표 시간 설정 (예: 2분 7초 = 127초)
    target_time = 127
    print(f"--LOG : 목표 시간 {target_time}초 설정 완료")

    # 목표 시간으로 이동할 비율 계산
    move_ratio = target_time / total_time
    print(f"--LOG : 목표 시간 비율 계산: {move_ratio}")

    # 슬라이더 크기 가져오기
    slider_width = slider.size['width']
    print(f"--LOG : 슬라이더 크기: {slider_width} 픽셀")

    # 이동할 거리 계산
    move_distance = move_ratio * slider_width
    print(f"--LOG : 이동할 거리 계산 완료: {move_distance} 픽셀")

    # 슬라이더를 해당 위치로 이동
    print("--LOG : 슬라이더 이동 시작...")
    actions = ActionChains(driver)
    actions.click_and_hold(slider).move_by_offset(move_distance, 0).release().perform()

    print(f"--LOG : 슬라이더를 {target_time}초로 이동 완료")

except Exception as e:
    print(f"--ERROR : 슬라이더 이동 오류 - {e}")

# 드라이버 종료
print("--LOG : 드라이버 종료 중...")
driver.quit()
