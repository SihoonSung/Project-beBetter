from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os  # 폴더 생성을 위해 추가
import urllib.request
import random

# 0. 설정 및 검색어 변수화
search_word = "Pizza" # 검색어 변수 (여기를 바꾸면 폴더명과 파일명도 다 같이 바뀝니다)
save_path = f"AI/Dataset/{search_word}" # 저장될 최종 경로

# 1. 폴더 생성 로직 (요구사항 1)
if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"[{save_path}] 폴더를 생성했습니다.")
else:
    print(f"[{save_path}] 폴더가 이미 존재합니다.")

# 2. 브라우저 실행
service = Service(executable_path="chromedriver.exe") 
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

# 3. 검색어 입력 및 실행
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.send_keys(search_word + Keys.ENTER)

# 4. 스크롤 및 이미지 데이터 확보
# (이전 코드와 동일하되 속도 안정성을 위해 elem 정의 수정)
last_height = driver.execute_script("return document.body.scrollHeight")
for i in range(30): # 너무 빠르면 차단될 수 있어 30~60회 권장
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(random.uniform(0.5, 1.2))

# 5. 결과 더보기 버튼 처리
try:
    view_more_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mye4qd"))
    )
    view_more_button.click()
except:
    pass

# 6. 이미지 URL 리스트 수집
images = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")
links = [image.get_attribute("src") for image in images if image.get_attribute("src") is not None]
print(f"찾은 [{search_word}] 이미지 개수 : {len(links)}")

# 7. 이미지 다운로드 (요구사항 2)
print("다운로드를 시작합니다...")
for k, url in enumerate(links):
    try:
        # 파일명 형식: 클래스_숫자.jpg (1부터 시작하도록 k+1)
        filename = f"{search_word}_{k+1}.jpg"
        full_path = os.path.join(save_path, filename)
        
        urllib.request.urlretrieve(url, full_path)
        
        if (k+1) % 10 == 0: # 10개 단위로 진행 상황 출력
            print(f"{k+1}개 완료...")
    except Exception as e:
        print(f"에러 발생({filename}): {e}")
        continue

print(f" 모든 [{search_word}] 다운로드 완료 ---")
driver.quit()
