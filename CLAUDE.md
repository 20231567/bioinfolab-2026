# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 개요

생물정보학실험 수업의 학생 실습 저장소이다. 빌드·린트·테스트 체계는 없고, 주차별 `labNN/` 폴더에 짧은 bash/파이썬 스크립트를 작성해 직접 실행하는 방식이다. 문서와 주석은 한국어로 쓴다.

## 폴더 구조와 규칙

- 새 주차는 `cp -r lab-template labNN` 으로 만든다. 각 주차 폴더 구성:
  - `data/` — 입력 데이터(FASTA 등)
  - `doc/` — 결과 파일(`.tsv`, `.fasta`), 보고서(`.md`)
  - `src/` — 직접 작성한 스크립트(`.sh`, `.py`)
- 스크립트는 주차 폴더(`labNN/`)를 작업 위치로 두고 실행하는 것을 전제로 한다. 예:
  `cd lab07 && python3 src/filter_fasta.py data/seqs.fasta 100 doc/long.fasta`
- `bash src/check_codespace.sh` 는 환경 확인 결과를 `doc/check_result.txt` 에 저장한다(각 lab 폴더에 복사되어 있음).
- 공용 예제 데이터: `resources/data/`, `data/`.
- 시퀀싱 데이터(`*.fastq*`, `*.sra`)와 조립/주석 결과 폴더(shovill, spades, prokka, flye)는 `.gitignore` 로 제외된다. 필요하면 `wget` 으로 다시 내려받는다.

## 실행 환경

Codespaces devcontainer(`.devcontainer/`)로 환경이 정해진다. 주차에 따라 사용 가능한 도구가 다르다:

| 주차 | 설정 | 도구 |
|------|------|------|
| 02~07 | `1-basic` | python3, 리눅스 기본 명령 |
| conda 실습 | `2-conda` | micromamba (직접 설치가 과제) |
| 08~09, 12~14 | `3-seq` | seqkit, blast, mafft, iqtree, fastqc, fastp |
| 10~11 | `4-genome` | 위 + shovill, prokka |

`.devcontainer/check.sh` 가 어떤 도구가 설치되어 있는지 보여 준다. 도구가 없으면 직접 설치하지 않는다(conda 실습 주차만 예외).

## 공용 FASTA 모듈: `lab07/src/fasta.py`

FASTA 처리는 이 모듈을 재사용한다(사용 설명은 `lab07/src/README.md`).

- `read_fasta(filename)` → `{이름: 서열}` 딕셔너리. 헤더의 첫 단어만 이름으로 쓰고, 서열은 대문자로 변환된다.
- `write_fasta(seqs, filename)`, `gc_content(seq)`, `reverse_complement(seq)`, `length_stats(seqs)` (`count/total/avg/min/max` 딕셔너리 반환)
- 같은 `src/` 안의 스크립트는 `from fasta import read_fasta, write_fasta` 로 가져온다(스크립트 폴더가 `sys.path` 에 들어가므로 작업 위치와 무관하게 동작).
- 파일 안에 `if __name__ == "__main__":` 블록이 두 개 있고, `write_fasta`·`reverse_complement` 는 첫 블록 뒤에, `length_stats` 는 두 번째 블록 뒤에 정의되어 있다. import 시에는 문제없지만 직접 실행(`python3 src/fasta.py data/seqs.fasta`)하면 블록 시점에 아직 정의되지 않은 함수는 쓸 수 없으므로, 테스트 코드를 추가할 때는 파일 맨 끝에 둔다.

## 코드 작성 규칙 (`lab09/src/CLAUDE.md`)

- FASTA 파일은 `lab07/src/fasta.py` 의 `read_fasta` 로 읽는다.
- 새 라이브러리(Biopython 등)를 쓰기 전에 먼저 물어본다. 표준 라이브러리만 쓰는 것이 기본이다.
- 주석은 한국어로 쓴다.
- 스크립트는 `sys.argv` 로 인자를 받고, 인자 부족·파일 없음은 사용법/오류 메시지와 함께 `sys.exit` 로 끝내는 형태를 따른다(`lab09/src/count_agent.py` 참고).

## 하지 말 것

- `rm` 으로 파일을 지우지 않는다.
- `pip install` 로 무언가를 설치하지 않는다.
- git 명령어를 실행하지 않는다(커밋·푸시는 학생이 직접 한다).
