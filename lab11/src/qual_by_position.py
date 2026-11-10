#!/usr/bin/env python3
# qual_by_position.py — FASTQ 파일에서 염기 위치별 평균 품질 점수를 계산한다
# 모든 read의 1번째 염기, 2번째 염기, ... 품질 점수를 위치별로 모아 평균을 낸다.
# FastQC의 "Per base sequence quality" 그래프가 계산하는 평균값과 같다.
# 사용법: python3 src/qual_by_position.py <FASTQ파일> [출력파일]
#   - 출력: 위치(1부터)<TAB>평균 품질 (출력파일이 없으면 화면에 출력)
#   - 품질 점수는 Phred+33 인코딩(Illumina 1.8 이후)으로 가정한다.
#   - .gz 로 끝나는 압축 파일도 읽을 수 있다.

import sys
import os
import gzip

PHRED_OFFSET = 33


def open_fastq(filename):
    """일반 파일과 gzip 압축 파일을 모두 텍스트 모드로 연다."""
    if filename.endswith(".gz"):
        return gzip.open(filename, "rt")
    return open(filename)


def qual_by_position(filename):
    """위치별 품질 합계와 개수를 모아 (read 수, 위치별 평균 리스트)를 돌려준다.

    파일을 한 번에 읽지 않고 4줄씩 읽으므로 큰 파일도 메모리 걱정 없이 처리한다.
    read 길이가 서로 달라도, 각 위치는 그 위치까지 길이가 있는 read만으로 평균을 낸다.
    """
    sums = []     # sums[i]  : (i+1)번째 위치 품질 점수의 합
    counts = []   # counts[i]: (i+1)번째 위치에 염기가 있는 read 수
    n_reads = 0

    with open_fastq(filename) as f:
        while True:
            header = f.readline()
            if header == "":          # 파일 끝
                break
            if header.strip() == "":  # 빈 줄은 무시
                continue
            seq = f.readline().rstrip("\r\n")
            plus = f.readline()
            qual = f.readline().rstrip("\r\n")

            # FASTQ 형식 검사: @헤더 / 서열 / + / 품질, 서열과 품질 길이가 같아야 한다
            if not header.startswith("@") or not plus.startswith("+"):
                print("오류: FASTQ 형식이 아닙니다 (read", n_reads + 1, "근처):", header.strip())
                sys.exit(3)
            if len(seq) != len(qual):
                print("오류: 서열과 품질 길이가 다릅니다:", header.strip())
                sys.exit(3)

            # 더 긴 read가 나오면 리스트를 늘린다
            while len(sums) < len(qual):
                sums.append(0)
                counts.append(0)

            for i, ch in enumerate(qual):
                sums[i] = sums[i] + ord(ch) - PHRED_OFFSET
                counts[i] = counts[i] + 1
            n_reads = n_reads + 1

    means = []
    for i in range(len(sums)):
        means.append(sums[i] / counts[i])
    return n_reads, means


if len(sys.argv) < 2:
    print("사용법: python3 src/qual_by_position.py <FASTQ파일> [출력파일]")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

n_reads, means = qual_by_position(filename)

if n_reads == 0:
    print("오류: read가 하나도 없습니다:", filename)
    sys.exit(3)

lines = []
for i, m in enumerate(means):
    lines.append(f"{i + 1}\t{m:.2f}")

if len(sys.argv) >= 3:
    with open(sys.argv[2], "w") as out:
        out.write("\n".join(lines) + "\n")
    print("read", n_reads, "개, 위치", len(means), "개 →", sys.argv[2])
else:
    print("\n".join(lines))
