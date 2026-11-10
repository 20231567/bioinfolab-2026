#!/usr/bin/env python3
# check_paired.py — paired-end FASTQ 두 파일이 올바르게 짝을 이루는지 확인한다
#   1) 두 파일의 read 개수가 같은지
#   2) 같은 순서의 read끼리 이름이 짝을 이루는지
#      (헤더 첫 단어에서 끝의 /1, /2, _1, _2 같은 짝 표시를 뗀 뒤 비교)
# 사용법: python3 src/check_paired.py <R1.fastq> <R2.fastq>

import sys
import os
import re


def base_name(header):
    """헤더 줄(@로 시작)에서 짝 표시를 뗀 read 이름을 돌려준다."""
    name = header[1:].split()[0]          # '@' 제거 후 첫 단어만 사용
    return re.sub(r"[/_][12]$", "", name)


def read_headers(filename):
    """FASTQ 파일에서 각 read의 헤더 줄(4줄 중 첫 줄)을 차례로 돌려준다."""
    with open(filename) as f:
        for i, line in enumerate(f):
            if i % 4 == 0:
                line = line.rstrip("\n")
                if not line.startswith("@"):
                    print("오류: FASTQ 형식이 아닙니다 (%s, %d번째 줄)" % (filename, i + 1))
                    sys.exit(3)
                yield line


if len(sys.argv) < 3:
    print("사용법: python3 src/check_paired.py <R1.fastq> <R2.fastq>")
    sys.exit(1)

file1, file2 = sys.argv[1], sys.argv[2]
for fn in (file1, file2):
    if not os.path.isfile(fn):
        print("오류: 파일을 찾을 수 없습니다:", fn)
        sys.exit(2)

# 두 파일의 헤더 목록 읽기
headers1 = list(read_headers(file1))
headers2 = list(read_headers(file2))
n1, n2 = len(headers1), len(headers2)

print("R1 read 개수:", n1)
print("R2 read 개수:", n2)
print("개수 일치:", "예" if n1 == n2 else "아니오")

# 같은 위치의 read 이름 비교 (짧은 쪽 길이까지)
mismatch = 0
for i, (h1, h2) in enumerate(zip(headers1, headers2)):
    if base_name(h1) != base_name(h2):
        mismatch += 1
        if mismatch <= 5:   # 처음 5개만 예시로 출력
            print("  불일치 %d번째 read: %s | %s" % (i + 1, h1, h2))

print("이름 불일치 쌍:", mismatch)
print("첫 쌍 예시:", base_name(headers1[0]) if headers1 else "-",
      "|", base_name(headers2[0]) if headers2 else "-")

if n1 == n2 and mismatch == 0:
    print("결과: 정상적인 paired-end 파일입니다.")
else:
    print("결과: 짝이 맞지 않습니다.")
    sys.exit(4)
