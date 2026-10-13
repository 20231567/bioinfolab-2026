import sys
from fasta import length_stats, read_fasta


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 src/stats.py <FASTA 파일 경로>")
        sys.exit(1)

    filename = sys.argv[1]
    seqs = read_fasta(filename)
    stats = length_stats(seqs)

    print(f"<{filename} 길이 통계>")
    print(f"서열 개수   : {stats['count']} 개")
    print(f"전체 길이   : {stats['total']} bp")
    print(f"평균 길이   : {stats['avg']:.2f} bp")
    print(f"가장 짧은 길이: {stats['min']} bp")
    print(f"가장 긴 길이  : {stats['max']} bp")


if __name__ == "__main__":
    main()