# rbcL 데이터 출처

받은 방법: `src/get_rbcL_search.sh`
(esearch `"학명"[ORGN] AND rbcL[GENE] AND 1300:1500[SLEN]`, 첫 번째 결과 1개 → efetch FASTA + GenBank)

확인 방법: GenBank 파일의 `VERSION`, `ORGANISM` 줄을 `grep`으로 확인하고,
FASTA의 `>` 개수(`grep -c '>'`)와 서열 길이(`grep -v '>' | tr -d '\n' | wc -c`)를 셌다.

| 파일 | VERSION | ORGANISM | 길이 (bp) | 확인 방법 | 문제 |
|---|---|---|---|---|---|
| rbcL_arabidopsis | OK432498.1 | Arabidopsis thaliana | 1440 | GenBank VERSION/ORGANISM, FASTA 서열 1개 | 종은 맞음. 그러나 DEFINITION이 **"UNVERIFIED: ... large subunit-like (rbcL) gene, partial sequence"** — NCBI가 검증하지 않은 레코드라 믿기 어려움 |
| rbcL_ginseng | — | — | — | esearch 결과 개수 확인 | **파일 없음.** `"Panax ginseng"[ORGN] AND rbcL[GENE] AND 1300:1500[SLEN]` 검색 결과가 0건 (길이 조건을 빼면 137건 — 엽록체 전체 유전체나 짧은 조각뿐) |
| rbcL_rice | L24073.1 | Oryza sativa | 1355 | GenBank VERSION/ORGANISM, FASTA 서열 1개 | 종·길이는 맞음. 단, 분자 종류가 DNA가 아니라 **mRNA** (complete cds) |
| rbcL_maize | Z11973.1 | Zea mays | 1431 | GenBank VERSION/ORGANISM, FASTA 서열 1개 | 없음 |
| rbcL_ginkgo | KF221173.1 | Ginkgo biloba | 1317 | GenBank VERSION/ORGANISM, FASTA 서열 1개 | 없음 (partial cds, 범위 안) |
| rbcL_pine | JQ512595.1 | Pinus thunbergii | 1428 | GenBank VERSION/ORGANISM, FASTA 서열 1개 | 없음 (complete cds) |
| rbcL_fern | MW620303.1 | Adiantum capillus-veneris | 1308 | GenBank VERSION/ORGANISM, FASTA 서열 1개 | 없음 (partial cds, 범위 하한에 가까움) |
| rbcL_liverwort | LC536762.1 | Marchantia polymorpha subsp. ruderalis | 1399 | GenBank VERSION/ORGANISM, FASTA 서열 1개 | 요청한 *Marchantia polymorpha*의 **아종(subsp. ruderalis)** — 정확히 같은 이름은 아님 |

## 점검 결과

- **ORGANISM이 요청한 종과 같은가**: 6개는 정확히 일치. liverwort는 아종(subsp. ruderalis)이 섞였다. ginseng은 파일이 없다.
- **길이 1,300~1,500**: 받은 7개 모두 범위 안 (1308 ~ 1440).
- **파일마다 서열 1개**: 받은 7개 모두 `>` 1개.

## 문제 파일과 다시 받는 방법

1. **rbcL_ginseng (없음)**
   - 원인: 인삼은 rbcL 단독 레코드 중 1,300~1,500 bp인 것이 NCBI에 없다. 검색 조건이 너무 좁았다.
   - 다시 받으려면: 길이 조건으로 찾지 말고, **RefSeq 엽록체 유전체 NC_006290.1에서 rbcL CDS만 잘라 받도록** 지시한다.
     예: `efetch -db nuccore -id NC_006290.1 -format fasta_cds_na` 결과에서 `[gene=rbcL]` 서열만 뽑기
     (이미 `data/refseq_cds/rbcL_ginseng.fa`, 1437 bp로 받아 둔 것이 있음).
2. **rbcL_arabidopsis (UNVERIFIED)**
   - 다시 받으려면: 검색어에 `NOT UNVERIFIED[TITL]`을 붙이거나, RefSeq `NC_000932.1`의 rbcL CDS를 받도록 지시한다.
3. **rbcL_liverwort (아종)**
   - 다시 받으려면: 아종을 피하려면 RefSeq `NC_037507.1`의 rbcL CDS를 받도록 지시한다. (아종을 허용한다면 그대로 써도 된다.)

> 공통 개선안: "첫 번째 검색 결과"는 레코드 품질을 보장하지 않는다. 8종 모두 **RefSeq 엽록체 유전체의 rbcL CDS**를 받으면 종·길이·형식이 한 번에 맞춰진다 (`data/refseq_cds/`, 모두 1428~1440 bp).
