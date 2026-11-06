"""Source-only PDF crops, complete panel labels, no changes to diagram geometry."""
from pathlib import Path
import fitz
R=next(p for p in Path(__file__).resolve().parents if (p/'物理/00_原材料').is_dir())
doc=fitz.open(R/'物理/00_原材料/扫描件_普通高等教育十一五规划教材配套教辅.pdf')
JOBS=[(5, 151, [0.095, 0.71, 0.395, 0.93]), (10, 154, [0.115, 0.361, 0.38, 0.574])]
for num,page,box in JOBS:
 pg=doc[page-1];r=pg.rect
 pg.get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(r.width*box[0],r.height*box[1],r.width*box[2],r.height*box[3])).save(Path(__file__).with_name(f'{num:03}.png'))
