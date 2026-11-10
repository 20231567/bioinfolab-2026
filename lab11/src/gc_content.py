#!/usr/bin/env python3
# gc_content.py — FASTQ의 각 read에 대해 GC 비율과 평균 품질을 계산하고,
# GC 비율이 극단적으로 높은/낮은 read N개(기본 10개)의 평균 품질을 전체 평균과 비교한다.
# 사용법: python3 src/gc_content.py <FASTQ파일> [read별결과.tsv] [N]
#   - read별결과.tsv: 이름<TAB>길이<TAB>GC비율(%)<TAB>평균품질 (생략하거나 - 이면 저장하지 않음)
#   - N: 고를 read 수 (기본 10)
#   - GC 비율 = (G + C 개수) / read 길이 × 100 (N 염기도 길이에 포함)
#   - 품질 점수는 Phred+33 인코딩으로 가정한다. .gz 파일도 읽을 수 있다.

import sys
import os
import gzip

PHRED_OFFSET = 33


def open_fastq(filename):
    """일반 파일과 gzip 압축 파일을 모두 텍스트 모드로 연다."""
    if filename.endswith(".gz"):
        return gzip.open(filename, "rt")
    return open(filename)


def gc_percent(seq):
    """서열의 GC 비율(%)을 돌려준다."""
    seq = seq.upper()
    return (seq.count("G") + seq.count("C")) / len(seq) * 100


def mean_quality(qual):
    """품질 문자열의 평균 Phred 점수를 돌려준다."""
    total = 0
    for ch in qual:
        total = total + ord(ch) - PHRED_OFFSET
    return total / len(qual)


def read_records(filename):
    """FASTQ를 4줄씩 읽어 (이름, 길이, GC%, 평균품질) 리스트를 돌려준다."""
    records = []
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

            if not header.startswith("@") or not plus.startswith("+"):
                print("오류: FASTQ 형식이 아닙니다 (read", len(records) + 1, "근처):", header.strip())
                sys.exit(3)
            if len(seq) != len(qual):
                print("오류: 서열과 품질 길이가 다릅니다:", header.strip())
                sys.exit(3)
            if len(seq) == 0:         # 길이 0인 read는 비율을 낼 수 없으므로 건너뛴다
                continue

            name = header[1:].split()[0]   # 헤더의 첫 단어만 이름으로 쓴다
            records.append((name, len(seq), gc_percent(seq), mean_quality(qual)))
    return records


def mean_and_sd(values):
    """평균과 표준편차(모집단)를 돌려준다."""
    m = sum(values) / len(values)
    var = 0
    for v in values:
        var = var + (v - m) ** 2
    return m, (var / len(values)) ** 0.5


def print_group(title, group, overall_q, overall_sd):
    """read 묶음을 표로 출력하고, 묶음 평균 품질을 전체 평균과 비교한다."""
    print(f"## {title}")
    print("이름\t길이\tGC(%)\t평균품질")
    for name, length, gc, q in group:
        print(f"{name}\t{length}\t{gc:.2f}\t{q:.2f}")
    gq = sum(r[3] for r in group) / len(group)
    diff = gq - overall_q
    if overall_sd > 0:
        print(f"→ 평균 품질 {gq:.2f} (전체 대비 {diff:+.2f}, 전체 표준편차의 {diff / overall_sd:+.2f}배)")
    else:
        print(f"→ 평균 품질 {gq:.2f} (전체 대비 {diff:+.2f})")
    print()


# ---- 인자 확인 ----
if len(sys.argv) < 2:
    print("사용법: python3 src/gc_content.py <FASTQ파일> [read별결과.tsv 또는 -] [N]")
    sys.exit(1)

filename = sys.argv[1]
if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

# 두 번째 인자가 없거나 "-" 이면 read별 결과를 저장하지 않는다
out_file = None
if len(sys.argv) >= 3 and sys.argv[2] != "-":
    out_file = sys.argv[2]

n_pick = 10
if len(sys.argv) >= 4:
    if not sys.argv[3].isdigit() or int(sys.argv[3]) < 1:
        print("오류: N은 1 이상의 정수여야 합니다:", sys.argv[3])
        sys.exit(1)
    n_pick = int(sys.argv[3])

# ---- 계산 ----
records = read_records(filename)
if len(records) == 0:
    print("오류: read가 하나도 없습니다:", filename)
    sys.exit(3)
if len(records) < n_pick:
    n_pick = len(records)

# read별 결과 저장
if out_file:
    try:
        with open(out_file, "w") as out:
            out.write("name\tlength\tgc_percent\tmean_quality\n")
            for name, length, gc, q in records:
                out.write(f"{name}\t{length}\t{gc:.2f}\t{q:.2f}\n")
    except OSError:
        print("오류: 결과 파일을 쓸 수 없습니다:", out_file)
        sys.exit(2)

gc_mean, gc_sd = mean_and_sd([r[2] for r in records])
q_mean, q_sd = mean_and_sd([r[3] for r in records])

# GC 비율로 정렬 (같은 GC면 파일 순서 유지)
by_gc = sorted(records, key=lambda r: r[2])
low = by_gc[:n_pick]                      # GC가 가장 낮은 N개
high = by_gc[-n_pick:][::-1]              # GC가 가장 높은 N개 (높은 순)

# ---- 출력 ----
print(f"# {filename}")
print(f"read 수: {len(records)}")
print(f"GC 비율 평균: {gc_mean:.2f}% (표준편차 {gc_sd:.2f})")
print(f"전체 평균 품질: {q_mean:.2f} (표준편차 {q_sd:.2f})")
if out_file:
    print("read별 결과 저장:", out_file)
print()
print_group(f"GC 비율이 가장 높은 read {n_pick}개", high, q_mean, q_sd)
print_group(f"GC 비율이 가장 낮은 read {n_pick}개", low, q_mean, q_sd)
