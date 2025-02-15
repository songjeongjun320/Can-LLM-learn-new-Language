from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

# Chrome 드라이버 경로 설정
chrome_driver_path = 'path/to/chromedriver'  # 경로를 본인의 크롬 드라이버 경로로 설정

# Selenium을 사용할 Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 창을 띄우지 않고 실행
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 웹 드라이버 실행
driver = webdriver.Chrome()

# 넷플릭스 드라마 페이지로 이동
url = 'https://www.netflix.com/watch/81618456'  # 원하는 드라마의 URL을 입력
driver.get(url)

# 로그인 (수동으로 로그인 후 자동화 시작)
input("로그인 후 Enter 키를 눌러주세요.")

# 비디오가 로드될 때까지 기다리기
time.sleep(5)  # 비디오 로드 대기 (시간 조정 필요할 수 있음)

# 에피소드 목록이 로드되면, 각 에피소드의 길이 추출
episode_lengths = []

# 에피소드 길이 추출
try:
    episodes = driver.find_elements(By.CSS_SELECTOR, "span[data-uia='video-title']")  # 에피소드 제목을 찾음
    durations = driver.find_elements(By.CSS_SELECTOR, "span[data-uia='video-duration']")  # 에피소드 길이를 찾음

    for duration in durations:
        episode_lengths.append(duration.text)
    
    # 각 에피소드 길이 출력
    print("에피소드 길이들: ", episode_lengths)

except Exception as e:
    print(f"에피소드 길이 추출 오류: {e}")

# 각 에피소드 길이를 합산하여 총 시간을 계산
total_minutes = 0
for length in episode_lengths:
    # "00:42"와 같은 형식에서 분과 초를 추출
    minutes, seconds = map(int, length.split(":"))
    total_minutes += minutes + seconds / 60

# 총 시간 출력
print(f"드라마 총 길이: {total_minutes:.2f} 분")

# 드라이버 종료
driver.quit()
