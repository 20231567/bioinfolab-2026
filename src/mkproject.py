import os
import sys

def main():
    # 1. 인자가 없으면 사용법 출력 후 종료
    if len(sys.argv) < 2:
        print("Usage: python src/mkproject.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]

    # 2. 같은 이름의 폴더가 이미 있으면 오류 메시지 출력 후 종료
    if os.path.isdir(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    # 3. 프로젝트 기본 폴더 및 하위 폴더 생성
    subfolders = ["data", "doc", "src"]
    for subfolder in subfolders:
        folder_path = os.path.join(project_name, subfolder)
        os.makedirs(folder_path, exist_ok=True)

    print(f"Project '{project_name}' created successfully with data, doc, and src folders.")

if __name__ == "__main__":
    main()
