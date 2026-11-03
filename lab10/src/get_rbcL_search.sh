#!/usr/bin/env bash
# =============================================================
#  여덟 종의 rbcL 서열을 esearch → efetch 로 받는다 (FASTA + GenBank)
#  사용법:  cd lab10 && bash src/get_rbcL_search.sh
#
#  - 검색어: "학명"[ORGN] AND rbcL[GENE] AND 1300:1500[SLEN]
#  - 검색 결과의 첫 번째 것만 받는다 (retmax=1)
#  - 이미 있는 파일은 다시 받지 않고 건너뛴다
#  - 요청 사이에 sleep 1
# =============================================================

OUTDIR="data"
EUTILS="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
mkdir -p "$OUTDIR"

# 검색어를 URL에 넣을 수 있게 바꾼다 (공백, 따옴표, 대괄호)
urlencode() { echo "$1" | sed 's/ /+/g; s/"/%22/g; s/\[/%5B/g; s/\]/%5D/g'; }

while read -r NAME SPECIES; do
    FA="$OUTDIR/$NAME.fa"
    GB="$OUTDIR/$NAME.gb"

    # 둘 다 있으면 검색도 하지 않는다
    if [ -s "$FA" ] && [ -s "$GB" ]; then
        printf "%-18s %-28s 둘 다 있음 → 건너뜀\n" "$NAME" "$SPECIES"
        continue
    fi

    TERM="\"$SPECIES\"[ORGN] AND rbcL[GENE] AND 1300:1500[SLEN]"

    # 1) esearch: 첫 번째 ID 하나만
    ID=$(wget -q -O - "$EUTILS/esearch.fcgi?db=nuccore&retmax=1&term=$(urlencode "$TERM")" \
         | grep -o '<Id>[0-9]*</Id>' | head -1 | sed 's/<[^>]*>//g')
    sleep 1
    if [ -z "$ID" ]; then
        printf "%-18s %-28s 검색 결과 없음\n" "$NAME" "$SPECIES"
        continue
    fi

    # 2) FASTA (있으면 건너뜀)
    if [ -s "$FA" ]; then
        FA_MSG="fa 있음(건너뜀)"
    else
        wget -q -O "$FA" "$EUTILS/efetch.fcgi?db=nuccore&id=$ID&rettype=fasta&retmode=text"
        sleep 1
        FA_MSG="fa 받음"
    fi

    # 3) GenBank (있으면 건너뜀)
    if [ -s "$GB" ]; then
        GB_MSG="gb 있음(건너뜀)"
    else
        wget -q -O "$GB" "$EUTILS/efetch.fcgi?db=nuccore&id=$ID&rettype=gb&retmode=text"
        sleep 1
        GB_MSG="gb 받음"
    fi

    printf "%-18s %-28s ID=%-12s %s, %s\n" "$NAME" "$SPECIES" "$ID" "$FA_MSG" "$GB_MSG"
done <<'EOF'
rbcL_arabidopsis Arabidopsis thaliana
rbcL_ginseng     Panax ginseng
rbcL_rice        Oryza sativa
rbcL_maize       Zea mays
rbcL_ginkgo      Ginkgo biloba
rbcL_pine        Pinus thunbergii
rbcL_fern        Adiantum capillus-veneris
rbcL_liverwort   Marchantia polymorpha
EOF
