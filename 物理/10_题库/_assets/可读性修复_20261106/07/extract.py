"""Source-only PDF crops, complete panel labels, no changes to diagram geometry."""
from pathlib import Path
import fitz
R=next(p for p in Path(__file__).resolve().parents if (p/'物理/00_原材料').is_dir())
doc=fitz.open(R/'物理/00_原材料/扫描件_普通高等教育十一五规划教材配套教辅.pdf')
JOBS=[(1, 135, [0.14, 0.477, 0.388, 0.623]), (2, 135, [0.395, 0.477, 0.635, 0.623]), (3, 135, [0.64, 0.477, 0.895, 0.623]), (4, 138, [0.215, 0.098, 0.5, 0.237]), (5, 138, [0.54, 0.098, 0.84, 0.237]), (6, 138, [0.215, 0.246, 0.5, 0.39]), (7, 138, [0.54, 0.246, 0.84, 0.39])]
for num,page,box in JOBS:
 pg=doc[page-1];r=pg.rect
 pg.get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(r.width*box[0],r.height*box[1],r.width*box[2],r.height*box[3])).save(Path(__file__).with_name(f'{num:03}.png'))
