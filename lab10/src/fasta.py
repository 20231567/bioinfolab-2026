"""FASTA 파일을 다루는 함수 모음"""

import sys


def read_fasta(filename):
    """FASTA 파일을 읽어 {이름: 서열} 딕셔너리로 돌려준다."""
    seqs = {}
    name = None
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                name = line[1:].split()[0]
                seqs[name] = ""
            else:
                # 읽어온 서열을 대문자로 변환하여 저장 (.upper() 추가)
                seqs[name] = seqs[name] + line.upper()
    return seqs


def gc_content(seq):
    """서열의 GC 비율을 0과 1 사이의 수로 돌려준다."""
    seq = seq.upper()  # 소문자 입력 대비 대문자 변환
    if len(seq) == 0:  # 빈 서열 예외 처리
        return 0.0
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)


# 직접 실행할 때만 동작하는 테스트 영역
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        seqs = read_fasta(filename)
        for name in seqs:
            print(name, len(seqs[name]), round(gc_content(seqs[name]), 3))


def write_fasta(seqs, filename):
    """{이름: 서열} 딕셔너리를 FASTA 파일로 저장한다."""
    with open(filename, "w") as out:
        for name in seqs:
            out.write(">" + name + "\n")
            out.write(seqs[name] + "\n")


def reverse_complement(seq):
    """DNA 서열의 역상보 서열 구하기"""
    seq = seq.upper()
    comp_map = {"A": "T", "T": "A", "G": "C", "C": "G"}
    comp_seq = ""
    for base in seq:
        comp_seq += comp_map.get(base, base)
    return comp_seq[::-1]

if __name__ == "__main__":
    # test 아무거나 넣음
    test = "ATGCGATACGCTTGA"
    
    # 역상보 서열과, 다시 역상보 확인하
    first_rc = reverse_complement(test)
    second_rc = reverse_complement(first_rc)
    
    print("original:", test)
    print("reverse_complement:", first_rc)
    print("reverse_complement(reverse_complement(seq)):", second_rc)
    print("원래 서열과 일치하는가?", test == second_rc)


#문제 3번 길이 통계 함수
def length_stats(seqs):
    """서열 딕셔너리를 받아 길이 통계(개수, 전체길이, 평균, 최소, 최대)를 딕셔너리로 돌려준다."""
    if not seqs:
        return {"count": 0, "total": 0, "avg": 0.0, "min": 0, "max": 0}

    lengths = [len(s) for s in seqs.values()]

    count = len(lengths)
    total = sum(lengths)
    avg = total / count
    min_len = min(lengths)
    max_len = max(lengths)

    return {
        "count": count,
        "total": total,
        "avg": avg,
        "min": min_len,
        "max": max_len,
    }