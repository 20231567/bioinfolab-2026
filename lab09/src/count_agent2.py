#!/usr/bin/env python3
# count_agent2.py — FASTA 파일의 서열 개수를 출력한다
# count_agent.py 와 달리 직접 '>' 줄을 세지 않고, lab07 의 공용 모듈 read_fasta 로 읽는다.
# 사용법: python3 src/count_agent2.py <FASTA파일>

import sys
import os

# 공용 FASTA 모듈은 lab07/src/fasta.py 에 있다.
# 이 스크립트 위치(lab09/src)를 기준으로 ../../lab07/src 경로를 계산해 sys.path 에 넣으면
# 어느 폴더에서 실행하든 `from fasta import read_fasta` 가 동작한다.
script_dir = os.path.dirname(os.path.abspath(__file__))
fasta_module_dir = os.path.join(script_dir, "..", "..", "lab07", "src")
sys.path.insert(0, os.path.normpath(fasta_module_dir))

from fasta import read_fasta

# 인자가 없으면 사용법을 보여 주고 종료한다.
if len(sys.argv) < 2:
    print("사용법: python3 count_agent2.py <FASTA파일>")
    sys.exit(1)

filename = sys.argv[1]

# 파일이 없으면 오류 메시지를 출력하고 종료한다.
if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

# read_fasta 는 {이름: 서열} 딕셔너리를 돌려주므로, 딕셔너리 크기가 곧 서열 개수이다.
# 주의: 이름(헤더 첫 단어)이 같은 서열이 여러 개면 하나로 합쳐져 적게 셀 수 있다.
seqs = read_fasta(filename)
print(len(seqs))
