#!/usr/bin/env bash
# =============================================================
#  여덟 종의 rbcL 유전자(CDS) 서열을 NCBI에서 내려받는다.
#  사용법:  cd lab10 && bash src/get_rbcL.sh
#
#  방법: 각 종의 RefSeq 엽록체 전체 유전체에서
#        efetch rettype=fasta_cds_na 로 CDS를 모두 받은 뒤
#        [gene=rbcL] 인 서열 하나만 골라 저장한다.
#  (짧은 rbcL 단독 등록 서열은 종마다 길이·구간이 제각각이고
#   인삼은 아예 없어서, 전체 길이가 보장되는 RefSeq를 쓴다.)
# =============================================================

OUTDIR="data"
mkdir -p "$OUTDIR"
BASE="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# 파일이름  RefSeq번호  학명
while read -r NAME ACC SPECIES; do
    OUT="$OUTDIR/$NAME.fa"
    wget -q -O - "$BASE?db=nuccore&id=$ACC&rettype=fasta_cds_na&retmode=text" \
        | awk -v name="$NAME" -v sp="$SPECIES" '
            /^>/ { p = /\[gene=rbcL\]/; if (p) print ">" name " " sp " " substr($1, 6); next }
            p' > "$OUT"
    LEN=$(grep -v '>' "$OUT" | tr -d '\n' | wc -c)
    printf "%-18s %-12s %-28s %5s bp\n" "$NAME" "$ACC" "$SPECIES" "$LEN"
    sleep 0.4   # NCBI 요청 제한(초당 3회) 지키기
done <<'EOF'
rbcL_arabidopsis NC_000932 Arabidopsis thaliana
rbcL_ginseng     NC_006290 Panax ginseng
rbcL_rice        NC_001320 Oryza sativa
rbcL_maize       NC_001666 Zea mays
rbcL_ginkgo      NC_016986 Ginkgo biloba
rbcL_pine        NC_001631 Pinus thunbergii
rbcL_fern        NC_004766 Adiantum capillus-veneris
rbcL_liverwort   NC_037507 Marchantia polymorpha
EOF

# 여덟 개를 하나로 합친 파일 (정렬·계통수용)
rm -f "$OUTDIR/rbcL_all.fa"
cat "$OUTDIR"/rbcL_*.fa > "$OUTDIR/rbcL_all.tmp" && mv "$OUTDIR/rbcL_all.tmp" "$OUTDIR/rbcL_all.fa"
echo ">>> $OUTDIR/rbcL_all.fa 에 $(grep -c '>' "$OUTDIR/rbcL_all.fa")개 서열 저장"
