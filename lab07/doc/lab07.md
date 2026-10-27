# lab07 요약: 함수와 파일 저장

lab07에서는 Python **함수(`def`)** 를 만들고, 자주 쓰는 함수를 **모듈(`fasta.py`)** 로 모아 다른 스크립트에서 `import`해 쓰는 방법을 배웠다. 결과를 **FASTA/TSV 파일로 저장**하는 것도 함께 연습했다.

## 1. 핵심 개념

| 개념 | 내용 |
| :--- | :--- |
| 함수 정의 | `def 함수이름(매개변수): ... return 값` |
| `print` vs `return` | `print`는 화면에 보여 주기만 하고 함수는 `None`을 돌려준다. `return`은 값을 돌려주므로 다른 계산에 이어서 쓸 수 있다. (`fseqlen.py`) |
| 모듈 import | `from fasta import read_fasta, gc_content`처럼 다른 파일의 함수를 골라 가져온다 |
| `if __name__ == "__main__":` | 파일을 직접 실행할 때만 테스트 코드가 돌고, `import`할 때는 돌지 않게 한다 |
| 파일 쓰기 모드 | `"w"`는 덮어쓰기(bash `>`), `"a"`는 이어쓰기(bash `>>`) |
| 명령줄 인자 | `sys.argv[1]`, 인자 개수는 `len(sys.argv)`로 확인하고, 잘못되면 `sys.exit(1)` |

## 2. `fasta.py` 모듈의 함수

| 함수 | 입력 | 출력 |
| :--- | :--- | :--- |
| `read_fasta(filename)` | FASTA 파일 경로 | `{이름: 서열}` 딕셔너리 (서열은 대문자로 바꿔 저장) |
| `write_fasta(seqs, filename)` | 서열 딕셔너리, 저장 경로 | FASTA 파일 |
| `gc_content(seq)` | DNA 서열 | GC 비율 (0~1), 빈 서열이면 `0.0` |
| `reverse_complement(seq)` | DNA 서열 | 역상보 서열 |
| `length_stats(seqs)` | 서열 딕셔너리 | `count`, `total`, `avg`, `min`, `max` 딕셔너리 |

```python
seqs = read_fasta("data/seqs.fasta")
stats = length_stats(seqs)
rc = reverse_complement("ATGC")   # "GCAT"
```

`reverse_complement(reverse_complement(seq)) == seq`가 성립하는지 확인해서 함수가 맞게 동작하는지 검증했다.

## 3. 스크립트 목록 (`lab07/src/`)

| 파일 | 하는 일 | 사용법 |
| :--- | :--- | :--- |
| `fgc.py` | GC 함수 첫 연습 | `python3 fgc.py` |
| `fseqlen.py` | `print`와 `return`의 차이 비교 | `python3 fseqlen.py` |
| `countseq.py` | `>` 줄을 세서 서열 개수 출력 (인자·파일 존재 검사 포함) | `python3 countseq.py <FASTA>` |
| `countseq2.py` | 위 내용을 `read_fasta`로 다시 작성 | `python3 countseq2.py <FASTA>` |
| `filter_fasta.py` | 최소 길이 이상인 서열만 골라 FASTA로 저장 | `python3 filter_fasta.py <입력> <최소길이> <출력>` |
| `summary.py` | 서열별 이름/길이/GC를 TSV로 저장 | `python3 summary.py <입력> <출력.tsv>` |
| `stats.py` | `length_stats`로 길이 통계 출력 | `python3 stats.py <FASTA>` |
| `batchinfo2.py` | 폴더 안 모든 `*.fasta`의 개수/총 길이/평균 GC를 TSV로 저장 (`glob` 사용) | `python3 batchinfo2.py <폴더> <출력.tsv>` |

## 4. 결과 파일 (`lab07/doc/`)

- `long.fasta`: `filter_fasta.py`로 거른 결과 (2개 서열)
- `summary.tsv`: `seqs.fasta`의 서열별 길이와 GC

  | name | length | gc |
  | :--- | ---: | ---: |
  | gene1 | 30 | 0.5 |
  | gene2 | 15 | 0.4667 |
  | gene3 | 22 | 0.5455 |

- `batch_summary.tsv`: `data/` 폴더 전체 요약

  | filename | count | total_len | avg_gc |
  | :--- | ---: | ---: | ---: |
  | lower.fasta | 2 | 20 | 0.650 |
  | seqs.fasta | 3 | 67 | 0.504 |
  | seqs2.fasta | 2 | 16 | 0.250 |

- `python_cheatsheet.md`: Bash 문법과 Python 코드 대응표 (`$1` → `sys.argv[1]`, `[ -f ]` → `os.path.isfile()`, `mkdir -p` → `os.makedirs(..., exist_ok=True)` 등)

## 5. 겪은 오류와 해결

1. **들여쓰기 오류**: `def` 안쪽 코드의 공백이 맞지 않아 실행되지 않았다. 들여쓰기를 맞춰 해결했다.
2. **`ZeroDivisionError`**: 빈 서열이 들어오면 `len(seq)`가 0이 되어 나눌 수 없다. `if len(seq) == 0: return 0.0`을 넣어 해결했다.
3. **소문자 서열**: `lower.fasta`의 소문자 서열은 GC가 0으로 계산됐다. `read_fasta`와 `gc_content`에서 `.upper()`로 대문자로 바꿔 해결했다.

## 6. 앞으로 더 해 볼 것

- 서열에 A/T/G/C가 아닌 문자나 숫자가 섞였는지 검사하는 함수 추가
- `fasta.py`에서 `if __name__ == "__main__":` 블록이 두 번 나오는데, 파일 맨 아래 하나로 합치기
