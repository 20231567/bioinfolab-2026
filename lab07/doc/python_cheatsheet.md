| 기능 | Bash 코드 | Python 대응 코드 / 비고 |
| :--- | :--- | :--- |
| 인자 개수 확인 | `if [ $# -lt 1 ]` | `if len(sys.argv) < 2:` |
| 첫 번째 인자 가져오기 | `$1` | `sys.argv[1]` |
| 디렉터리 존재 여부 | `[ -d "$dir" ]` | `os.path.isdir(dir)` |
| 파일 존재 여부** | `[ -f "$file" ]` | `os.path.isfile(file)` |
| 디렉터리 생성 | `mkdir -p "$dir"` | `os.makedirs(dir, exist_ok=True)` |
| 프로그램 스크립트 종료 | `exit 1` | `sys.exit(1)` |
| 표준 출력 메시지 | `echo "Hello"` | `print("Hello")` |
| 파이프라인 연결 | `cat file \| grep "seq"` | 옮길 필요 없음(파이썬 내부에서 문자열 조건문 및 루프로 직접 처리) |
| 와일드카드 파일 목록 | `for f in *.fasta; do` | `glob.glob("*.fasta")` 또는 `os.listdir()` |
| 문자열 길이 측정 | `${#var}` | `len(var)` |
| 숫자 판별 | `[[ "$var" =~ ^[0-9]+$ ]]` | `var.isdigit()` |

lab 07>
1. def 로 함수 만드는 모양
def 함수이름(매개변수1, 매개변수2):
    # 들여쓰기 후 실행할 코드 작성
    return 반환할 값

2. print 와 return 의 차이를 한 줄로
print는 화면에 보여지게 출력하고 None값이 되고 return은 계산 결과를 다른 계산에 활용할 수 있도록 저장된 값임

3. from 모듈 import 함수
from fasta import read_fasta, gc_content, 특정 파일에서 필요한 함수만 골라서 바로 사용할 수 있도록 해주는 함

4. if __name__ == "__main__": 을 언제 쓰는지
작성한 파이썬 파일을 직접 실행할 때만 작동하고 다른 파일에서 import할 때는 테스트 코드가 실행되어서 원래 파이썬 파일이 실행되지 않도록 해줄 때 사용

5. "w" 와 "a" 의 차이, 그리고 bash의 어떤 기호와 같은지
w는 기존 내용을 모두 지우고 새 파일로 덮어쓰는 기호이고 a는 기존 내용 뒤에 새로운 내용을 이어서 작성할 때 사용한다.

6. 오늘 겪은 오류 두 가지
1) def함수에서 공백 띄어쓰기 오류로 인해 터미널 명령어가 작성하지 않았다.
2) zerodivisionerror: 빈 서열을 받았을 때는 나누기가 안 되므로 if len(seq) == 0: return 0.0을 이용해 편집기를 수정하였다. 
