#!/usr/bin/bash

if [ -z "$1" ]; then
    echo "사용법: $0 <디렉터리경로>"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "오류: 디렉터리를 찾을 수 없습니다: $1"
    exit 1
fi

DIR="$1"

echo -e "file\tcount"
for f in "$DIR"/*.fasta; do
    if [ ! -f "$f" ]; then
        echo "FASTA 파일을 찾을 수 없습니다."
        break
    fi
    echo -e "$(basename "$f")\t$(grep -c ">" "$f")"
done
