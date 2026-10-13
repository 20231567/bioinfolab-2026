#!/usr/bin/bash
# fastainfo.sh — FASTA 파일 요약 정보 출력

if [ -z "$1" ]; then
    echo "사용법: $0 <FASTA파일>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "오류: 파일을 찾을 수 없습니다: $1"
    exit 1
fi

FILE="$1"

COUNT=$(grep -c ">" "$FILE")
NAMES=$(grep ">" "$FILE" | tr -d ">" | cut -d " " -f 1 | sed 's/^/  /')
BP=$(grep -v ">" "$FILE" | tr -d "\r\n" | wc -m)

echo "파일: $FILE"
echo "서열 개수: $COUNT"
echo "서열 이름:"
echo "$NAMES"
echo "총 염기 수(대략): $BP"
