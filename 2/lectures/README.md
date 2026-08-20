# บทเรียนเสริม — Network Topology for Circuit Analysis

เอกสารชุดนี้เขียนขึ้นเพื่อสนับสนุนการเฉลย [โจทย์พิเศษ spanning tree และชุดตัดอิสระ](../chapter1-exercise-1-3-cutset-equations/SPECIAL_PROBLEM.md) และแบบฝึกหัด [1.3] โดยเนื้อหาอ้างอิงจาก [303212S1Y2569lec01.pdf](303212S1Y2569lec01.pdf)

## โครงสร้างหลักสูตร 12 ชั่วโมง

| ชั่วโมง | เอกสาร | หัวข้อหลัก |
|---:|:---|:---|
| 1–2 | [01-foundations-of-graphs.md](01-foundations-of-graphs.md) | พื้นฐานกราฟ: ปม, กิ่ง, ทิศทาง, การเชื่อมต่อ, วงรอบ, tree, spanning tree |
| 3–4 | [02-graph-matrices-and-matrix-tree-theorem.md](02-graph-matrices-and-matrix-tree-theorem.md) | พื้นฐานเมทริกซ์, การสร้าง Incidence/Laplacian Matrix ทีละขั้น, Matrix-Tree Theorem, ตัวอย่าง 3/4/6 ปม, การเชื่อมโยง SPECIAL_PROBLEM |
| 5–6 | [03-circuit-topology-branches-twigs-links.md](03-circuit-topology-branches-twigs-links.md) | Branch, twig, link, การเลือก tree, ความสัมพันธ์กับ KCL/KVL |
| 7–8 | [04-cutsets-and-fundamental-cutsets.md](04-cutsets-and-fundamental-cutsets.md) | Cutset, ชุดตัดอิสระ, fundamental cutset, การเขียนสมการเซตตัด |
| 9–10 | [05-worked-example-6-nodes-11-branches.md](05-worked-example-6-nodes-11-branches.md) | ตัวอย่างโจทย์ 6 ปม 11 กิ่ง: หา 139 tree และ fundamental cutset ทีละขั้น |
| 11–12 | [06-advanced-problem-solving.md](06-advanced-problem-solving.md) | Cutset matrix, branch-current vector, ความเป็นอิสระเชิงเส้น, สรุปและแบบฝึกหัด |

## รูปประกอบ (Figures)

แต่ละหน่วยมี SVG/PNG ประกอบให้ดูภาพประกอบความเข้าใจ ไฟล์อยู่ในโฟลเดอร์ `figures/` และ embed ในเนื้อหาบทเรียนแล้ว:

- หน่วยที่ 1: กราฟ, กราฟมีทิศทาง, กราฟเชื่อมต่อ, วงรอบ, ต้นไม้, spanning tree
- หน่วยที่ 2: incidence matrix, reduced incidence matrix, Laplacian matrix, Matrix-Tree theorem, 6-node special Laplacian
- หน่วยที่ 3: กิ่ง, twig/link, KCL
- หน่วยที่ 4: cutset, fundamental cutset, cutset matrix
- หน่วยที่ 5: กราฟ 6 ปม 11 กิ่ง, tree T₀, 5 cutsets
- หน่วยที่ 6: cutset matrix Q_f

สร้างรูปด้วย `gen_figures.py` (ใช้ `cairosvg` แปลง SVG เป็น PNG)

สไตล์รูป:
- Node ขนาดเล็ก 6 px พร้อม highlight ด้านใน
- ลูกศรอยู่กลางเส้น (midpoint) ชี้ตามทิศทางกิ่ง
- เลขกำกับกิ่ง (edge labels) เป็น badge สีขาวขอบเข้ม
- เมทริกซ์วาดเป็นตารางชัดเจน มีตัวห้อย/ตัวยกแสดงด้วย tspan แทนเครื่องหมาย `_` หรือ `^` ใน SVG

สมการในเอกสารใช้ standard Markdown-LaTeX delimiters `$` ... `$` สำหรับ inline และ `$$` ... `$$` บรรทัดแยกสำหรับ display โดยใช้ `\mathsf{T}` สำหรับ transpose, `\deg` สำหรับ degree, และ `\{ ... \}` สำหรับเซต เพื่อให้ render เป็นตัวห้อย/ตัวยก/สัญลักษณ์ทางคณิตศาสตร์อย่างถูกต้อง

## คำศัพท์

- [GLOSSARY.md](GLOSSARY.md) — รวมคำศัพท์ทางคณิตศาสตร์, วงจรไฟฟ้า, และกราฟเทอร์โปโลยี พร้อมตัวอย่างและการออกเสียง
