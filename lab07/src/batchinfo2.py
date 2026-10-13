#!/usr/bin/env python3
import glob
import os
import sys

# 만든 fasta.py 모듈에서 함수꺼내기
from fasta import gc_content, length_stats, read_fasta

if len(sys.argv) < 3:
    print("사용법: python3 src/batchinfo2.py <폴더경로> <저장할TSV경로>")
    sys.exit(1)

folder = sys.argv[1]
outfile = sys.argv[2]

# TSV
with open(outfile, "w") as out:
    out.write("filename\tcount\ttotal_len\tavg_gc\n")

    for path in sorted(glob.glob(folder + "/*.fasta")):
        seqs = read_fasta(path)
        stats = length_stats(seqs)
        if stats["count"] > 0:
            gc_sum = sum(gc_content(s) for s in seqs.values())
            avg_gc = gc_sum / stats["count"]
        else:
            avg_gc = 0.0
        fname = os.path.basename(path)
        out.write(
            f"{fname}\t{stats['count']}\t{stats['total']}\t{avg_gc:.3f}\n"
        )

print(f"결과가 {outfile} 에 저장되었습니다.")