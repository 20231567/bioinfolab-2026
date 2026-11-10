#!/usr/bin/env python3
# md2pdf.py — 간단한 markdown → PDF 변환 (matplotlib, 한글 폰트 사용)
# 제목(#), 문단, 코드 블록(```), 표(|)만 처리한다.
# 사용법: python3 src/md2pdf.py <md파일> <pdf파일> <폰트폴더> [tsv1 tsv2]
#   - tsv1, tsv2(qual_by_position.py 결과)를 주면 마지막 쪽에 위치별 평균 품질 그래프를 넣는다.
# 예: python3 src/md2pdf.py doc/qual_by_position.md doc/qual_by_position.pdf fonts \
#         doc/qual_by_position.tsv doc/qual_by_position_trimmed.tsv
#
# 한글 폰트 준비 (Codespace에는 한글 폰트가 없다. lab11/ 에서 실행):
#   mkdir -p fonts && cd fonts
#   wget https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Regular.ttf
#   wget https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Bold.ttf
#   wget https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothiccoding/NanumGothicCoding-Regular.ttf
import sys, os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages

if len(sys.argv) < 4:
    print("사용법: python3 src/md2pdf.py <md파일> <pdf파일> <폰트폴더> [tsv1 tsv2]")
    sys.exit(1)

md, pdf, fd = sys.argv[1], sys.argv[2], sys.argv[3]

# 입력 파일과 폰트 파일이 있는지 확인
need_files = [md, fd + "/NanumGothic-Regular.ttf", fd + "/NanumGothic-Bold.ttf",
              fd + "/NanumGothicCoding-Regular.ttf"] + sys.argv[4:6]
for path in need_files:
    if not os.path.isfile(path):
        print("오류: 파일을 찾을 수 없습니다:", path)
        sys.exit(2)
REG = fm.FontProperties(fname=fd + "/NanumGothic-Regular.ttf")
BOLD = fm.FontProperties(fname=fd + "/NanumGothic-Bold.ttf")
fm.fontManager.addfont(fd + "/NanumGothicCoding-Regular.ttf")
MONO = fm.FontProperties(family=["DejaVu Sans Mono", "NanumGothicCoding"])
W, H = 8.27, 11.69          # A4 (inch)
LM, TOP, BOT = 0.08, 0.95, 0.05

items = []  # (kind, text)
lines = open(md, encoding="utf-8").read().split("\n")
i = 0
while i < len(lines):
    l = lines[i]
    if l.startswith("```"):
        i += 1; buf = []
        while not lines[i].startswith("```"):
            buf.append(lines[i].replace("\t", "    ")); i += 1
        items.append(("code", buf))
    elif l.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                rows.append([c.replace("`", "").replace("**", "") for c in cells])
            i += 1
        items.append(("table", rows)); continue
    elif l.startswith("#"):
        lvl = len(l) - len(l.lstrip("#"))
        items.append(("h%d" % lvl, l.lstrip("#").strip().replace("`", "")))
    elif l.strip():
        txt = l.strip()
        while i + 1 < len(lines) and lines[i + 1].startswith("   ") and lines[i + 1].strip():
            i += 1; txt += " " + lines[i].strip()
        items.append(("p", re.sub(r"\*\*|`", "", txt)))
    else:
        items.append(("gap", None))
    i += 1

pp = PdfPages(pdf)
state = {"fig": None, "y": TOP}
def newpage():
    if state["fig"]: pp.savefig(state["fig"]); plt.close(state["fig"])
    state["fig"] = plt.figure(figsize=(W, H)); state["y"] = TOP
def need(h):
    if state["fig"] is None or state["y"] - h < BOT: newpage()
def text(s, fp, size, x=LM, dy=None):
    dy = dy or size * 1.55 / 72 / H
    need(dy)
    state["fig"].text(x, state["y"], s, fontproperties=fp, fontsize=size, va="top")
    state["y"] -= dy

def wrapw(s, n):  # 한글은 폭 2로 계산해 줄바꿈
    out, cur, w = [], "", 0
    for ch in s:
        cw = 2 if ord(ch) > 0x1100 else 1
        if w + cw > n and ch != " ":
            out.append(cur); cur, w = "", 0
        cur += ch; w += cw
    return out + [cur]

for kind, t in items:
    if kind == "h1": text(t, BOLD, 20); state["y"] -= 0.01
    elif kind == "h2": state["y"] -= 0.008; text(t, BOLD, 15)
    elif kind == "h3": text(t, BOLD, 12)
    elif kind == "p":
        for ln in wrapw(t, 86): text(ln, REG, 10)
    elif kind == "gap": state["y"] -= 0.006
    elif kind == "code":
        dy = 9 * 1.5 / 72 / H
        need(dy * len(t) + 0.01)
        f = state["fig"]
        f.patches.append(plt.Rectangle((LM - 0.01, state["y"] - dy * len(t) - 0.005), 0.86, dy * len(t) + 0.01,
                         transform=f.transFigure, color="#f0f0f0", zorder=-1))
        for ln in t: text(ln, MONO, 9, x=LM + 0.005, dy=dy)
        state["y"] -= 0.008
    elif kind == "table":
        ncol = len(t[0])
        widths = [max(sum(2 if ord(c) > 0x1100 else 1 for c in r[j]) for r in t) + 2 for j in range(ncol)]
        tot = sum(widths); fs = 9 * min(1.0, 90 / tot)
        step = fs * 0.62 / 72 / W   # 반각 글자 1개 폭
        dy = fs * 1.8 / 72 / H
        for ri, r in enumerate(t):
            need(dy); x = LM
            for j, c in enumerate(r):
                state["fig"].text(x, state["y"], c, fontproperties=BOLD if ri == 0 else MONO, fontsize=fs, va="top")
                x += widths[j] * step
            state["y"] -= dy
            if ri == 0:
                state["fig"].add_artist(plt.Line2D([LM, 0.92], [state["y"] + 0.003] * 2, color="gray", lw=0.6))
        state["y"] -= 0.006

# 그래프 페이지
if len(sys.argv) > 5:
    newpage(); f = state["fig"]
    ax = f.add_axes([0.12, 0.55, 0.8, 0.35])
    for path, lab, col in [(sys.argv[4], "SRR1553607_1 (원본)", "#2a6fdb"), (sys.argv[5], "trimmed (fastp 후)", "#e07b00")]:
        xs, ys = zip(*[(int(a), float(b)) for a, b in (l.split() for l in open(path))])
        ax.plot(xs, ys, label=lab, color=col, lw=1.8)
    ax.axhspan(28, 42, color="#d8f0d8", zorder=-2); ax.axhspan(20, 28, color="#f6f0d0", zorder=-2)
    ax.set_ylim(24, 40); ax.set_xlim(1, 101)
    ax.set_xlabel("read 내 위치 (bp)", fontproperties=REG); ax.set_ylabel("평균 품질 (Phred)", fontproperties=REG)
    ax.set_title("위치별 평균 품질 (qual_by_position.py 출력)", fontproperties=BOLD, fontsize=13)
    ax.legend(prop=REG); ax.grid(alpha=0.3)
    f.text(0.12, 0.49, "배경색: 초록 = 좋음(≥28), 노랑 = 보통(20~28) — FastQC 그래프와 같은 기준", fontproperties=REG, fontsize=9)
newpage(); plt.close(state["fig"]); pp.close()
print("PDF 저장:", pdf)
