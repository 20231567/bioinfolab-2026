import sys
from fasta import read_fasta
from Bio import SeqIO
 
filename = sys.argv[1]
 
mine = read_fasta(filename)
 
for rec in SeqIO.parse(filename, "fasta"):
    same = len(rec.seq) == len(mine[rec.id])
    print(rec.id, len(rec.seq), len(mine[rec.id]), same)

