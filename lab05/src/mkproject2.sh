#!/usr/bin/bash
# mkproject2.sh — 디렉터리 구조 생성 스크립트
set -x
if [ -z "$1" ]; then
    echo "사용법: $0 <프로젝트이름>"
    exit 1
fi

PROJ="$1"

if [ -d "$PROJ" ]; then
    echo "오류: 이미 존재하는 디렉터리입니다: $PROJ"
    exit 2
fi

mkdir -p "$PROJ/data" "$PROJ/src" "$PROJ/doc"
touch "$PROJ/README.md"

echo "프로젝트가 성공적으로 생성되었습니다: $PROJ"
echo "생성된 구조:"
ls -R "$PROJ"
