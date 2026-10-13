fasta.py 에 들어 있는 함수 목록 및 설명
1. read_fasta(filename): 받는 것/ 들려주는 것, 파일 경로를 받아 {서열 이름: 서열 문자열}형태의 딕셔너리로 나타냄
예시: seqs = read_fasta("../data/seqs.fasta")

2. write_fasta(seqs, filename): {서열 이름: 서열 문자열}딕셔너리와 저장할 파일 경로를 받아 Fasta file로 저장
예시: write_fasta(selected_seqs, "doc/long.fasta")

3. gc_content(seq): DNA 서열(문자열)을 받아 GC비율을 0과 1 사이의 실수로 표현해줌
예시: gc_ratio = gc_content("ATGCGCTTA")

4. reverse_complement(seq): DNA 서열(문자열)을 받아 상보적 염기로, 역상보 서열을 확인할 수 있음
예시: rc_seq = reverse_complement("ATGC")

5. length_stats(seqs): {서열이름: 서열 문자열}딕셔너리를 받아, 개수, 총 길이, 평균 길이, 가장 짧은 길이, 가장 긴 길이를 표현해줌
예시: stats = length_stats(seqs)


아직 부족하다고 느끼는 점이나 추가하고 싶은 함수
문자열에서 염기서열을 제외한 다른 문자나 숫자를 검사하거나 오류라고 뜨게 하는 함수가 있으면 좋을 것 같