import os
import zipfile

def extract_all_zips(source_directory, target_directory):
    # 지정한 소스 디렉토리를 순회하며 zip 파일 검색
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_path = os.path.join(root, file)
                # zip 파일과 같은 이름의 폴더(이미 존재하지 않을 경우 생성) 생성
                extract_folder = os.path.join(target_directory, os.path.splitext(file)[0])
                os.makedirs(extract_folder, exist_ok=True)
                print(f"Extracting '{zip_path}' to '{extract_folder}'...")
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_folder)
                except Exception as e:
                    print(f"Error extracting {zip_path}: {e}")
    print("모든 zip 파일 추출 완료.")

# 사용 예시
source_directory_path = r"C:\Users\songj\OneDrive\Desktop\Can-LLM-learn-new-Language\Samples_zip"
target_directory_path = r"C:\Users\songj\OneDrive\Desktop\Can-LLM-learn-new-Language\Samples"
extract_all_zips(source_directory_path, target_directory_path)
