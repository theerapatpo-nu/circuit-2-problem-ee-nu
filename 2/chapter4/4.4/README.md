# โจทย์ [4.4] — Fundamental Tie-set Analysis

ชุดเฉลยสมบูรณ์ของวงจรข่าย 3 ปม 3 กิ่ง ซึ่งประกอบด้วยกิ่ง Thévenin หนึ่งกิ่งและกิ่ง Norton
สองกิ่ง ใช้วิธีวงรอบหลักมูลตามทรี \(T=\{2,3\}\) และลิงก์ \(L=\{1\}\)

เอกสารมี **2 วิธีที่เก็บแยกกัน**:

1. [วิธีที่ 1 — solution.md](solution.md): พิสูจน์เชิงลึก ตรวจคำตอบอิสระ 4 ทาง
2. [วิธีที่ 2 — Visual Matrix](solution-2/index.html): แนวทำข้อสอบ เน้นอ่านทิศจากรูปและคูณเมทริกซ์เป็นสามก้อน

## คำตอบย่อ

กำหนด

\[
R_T=R_1+R_2+R_3,\qquad K=v_s+R_1i_s
\]

| ปริมาณ | คำตอบ |
|---|---|
| Fundamental tie-set matrix | \(\mathbf B=\begin{bmatrix}1&1&-1\end{bmatrix}\) |
| สมการรอบ | \(R_Tj_1=(R_2+R_3)i_s-v_s\) |
| กระแสวงรอบ | \(j_1=\dfrac{(R_2+R_3)i_s-v_s}{R_T}\) |
| กระแสกิ่ง | \(i_1=i_2=j_1,\quad i_3=-j_1\) |
| แรงดันกิ่ง 1 | \(v_1=-\dfrac{R_3K}{R_T}\) |
| แรงดันกิ่ง 2 | \(v_2=-\dfrac{R_2K}{R_T}\) |
| แรงดันกิ่ง 3 | \(v_3=-\dfrac{(R_2+R_3)K}{R_T}\) |
| KVL | \(v_1+v_2-v_3=0\) |
| แรงดันปม | \(V_B=R_3K/R_T,\quad V_A=(R_2+R_3)K/R_T\) |

> ตารางนี้แก้ความคลาดเคลื่อนในร่างเดิม: พจน์แรงดัน \(v_1,v_2\) ต้องมีตัวประกอบ
> \(v_s+R_1i_s\) เหมือนกัน ไม่ใช่พจน์ที่มีความต้านทานตัวอื่นเพิ่มมา

## ดัชนีเอกสาร

| ไฟล์ | เนื้อหา |
|---|---|
| [problem.md](problem.md) | ข้อความโจทย์ สิ่งที่กำหนดให้ สิ่งที่ต้องหา และสัญกรณ์ |
| [problem.png](problem.png) | ภาพโจทย์ต้นฉบับ |
| [figure-analysis.md](figure-analysis.md) | วิเคราะห์รูป (ก) และ (ข): ปม กิ่ง ทิศ ทรี ลิงก์ และ \(\mathbf B\) |
| [solution.md](solution.md) | **เฉลยฉบับเต็ม 14 หัวข้อ** พร้อมพิสูจน์และการตรวจอิสระ 4 ทาง |
| [index.html](index.html) | Interactive Reader: MathJax, dark mode, image zoom, proof toggles และ Numeric Lab |
| [solution-2/solution-matrix-visual.md](solution-2/solution-matrix-visual.md) | **เฉลยวิธีที่ 2**: Visual Matrix workflow, Branch Cards และแบบเขียน 7 ช่องในห้องสอบ |
| [solution-2/index.html](solution-2/index.html) | Responsive Reader ของวิธีที่ 2 พร้อม stepper, image zoom และ Numeric Lab แบบสามก้อน |
| [solution-2/assets/make_figures.py](solution-2/assets/make_figures.py) | สร้างภาพ SVG เส้นตรง คมชัด และขยายได้ของวิธีที่ 2 |
| [assets/make_figures.py](assets/make_figures.py) | สคริปต์ Python standard library สำหรับสร้าง SVG ทั้ง 8 ภาพ |
| **figures/** | ภาพย่อยจากโจทย์ต้นฉบับ |
| **assets/** | ภาพเวกเตอร์ประกอบที่สร้างใหม่ |

## สื่อประกอบที่สร้างขึ้น

| # | ไฟล์ | ใช้อธิบาย |
|---:|---|---|
| 1 | [fig-01-topology-duality.svg](assets/fig-01-topology-duality.svg) | ความสมมาตร cycle space / cut space และ \(\mathbf B\mathbf Q^{\mathsf T}=0\) |
| 2 | [fig-02-circuit-anatomy.svg](assets/fig-02-circuit-anatomy.svg) | จากวงจรจริงสู่กิ่งประกอบ Thévenin/Norton 3 กิ่ง |
| 3 | [fig-03-tree-tieset.svg](assets/fig-03-tree-tieset.svg) | ทรี ลิงก์ การเดินวงรอบ และการสร้าง \(\mathbf B\) |
| 4 | [fig-04-branch-models.svg](assets/fig-04-branch-models.svg) | สมการเฉพาะกิ่งทั้งสาม |
| 5 | [fig-05-matrix-solve.svg](assets/fig-05-matrix-solve.svg) | การประกอบ \(\mathbf B\mathbf Z_b\mathbf B^{\mathsf T}\mathbf j\) |
| 6 | [fig-06-symbolic-results.svg](assets/fig-06-symbolic-results.svg) | คำตอบเชิงสัญลักษณ์ครบทุกกระแสและแรงดัน |
| 7 | [fig-07-independent-checks.svg](assets/fig-07-independent-checks.svg) | Node, Mesh/Supermesh, limiting cases และ Tellegen |
| 8 | [fig-08-numeric-power.svg](assets/fig-08-numeric-power.svg) | ตัวอย่างตัวเลข KCL/KVL และสมดุลกำลัง |

### ภาพสำหรับวิธีที่ 2

| # | ไฟล์ | ใช้อธิบาย |
|---:|---|---|
| 1 | [fig-01-exam-roadmap.svg](solution-2/assets/fig-01-exam-roadmap.svg) | แผนทำข้อสอบ 4 ขั้น: วงทรี อ่านเครื่องหมาย กรอกเมทริกซ์ คูณสามก้อน |
| 2 | [fig-02-read-b-from-tree.svg](solution-2/assets/fig-02-read-b-from-tree.svg) | รูปทรีวาดใหม่แบบสมมาตรและการอ่าน \(+1,+1,-1\) |
| 3 | [fig-03-matrix-workbench.svg](solution-2/assets/fig-03-matrix-workbench.svg) | โต๊ะเตรียม \(B,Z_b,i_{sb},v_{sb}\) และผลคูณสามก้อน |
| 4 | [fig-04-answer-map.svg](solution-2/assets/fig-04-answer-map.svg) | แผนที่จาก \(j_1\) ไปยังกระแสและแรงดันกิ่ง |

สร้างภาพใหม่ทั้งหมดได้ด้วย

~~~bash
python3 assets/make_figures.py
~~~

สคริปต์ไม่พึ่งพาไลบรารีภายนอกและไฟล์ SVG ทุกไฟล์มี viewBox, title, role="img"
และข้อความกำกับสำหรับการเข้าถึง

สร้างภาพของวิธีที่ 2 ใหม่ได้ด้วย

~~~bash
python3 solution-2/assets/make_figures.py
~~~

## ตัวอย่างตัวเลขมาตรฐาน

กำหนด \(R_1=2\ \Omega,\ R_2=3\ \Omega,\ R_3=5\ \Omega,\ v_s=10\ \mathrm V,\ i_s=4\ \mathrm A\)

| ปริมาณ | ค่า |
|---|---:|
| \(j_1\) | \(2.2\ \mathrm A\) |
| \(i_1,i_2,i_3\) | \(2.2,\ 2.2,\ -2.2\ \mathrm A\) |
| \(v_1,v_2,v_3\) | \(-9.0,\ -5.4,\ -14.4\ \mathrm V\) |
| \(V_B,V_A\) | \(9.0,\ 14.4\ \mathrm V\) |
| KVL residual | \(0\ \mathrm V\) |
| Power residual | \(0\ \mathrm W\) |

## วิธีเปิด Interactive Reader

เปิด [index.html](index.html) โดยตรง หรือให้บริการผ่าน local HTTP server:

~~~bash
python3 -m http.server 8000 --directory .
~~~

จากนั้นเปิด http://127.0.0.1:8000/index.html

## แหล่งทฤษฎี

- [เอกสารบรรยายบทที่ 4](../lecture/303212S1Y2569lec04_5048.pdf) หน้า 91–94:
  ทฤษฎีบทวงรอบหลักมูล, \(\mathbf B\mathbf v=0\), \(\mathbf i=\mathbf B^{\mathsf T}\mathbf j\),
  สมการกิ่ง และ \(\mathbf B\mathbf Z_b\mathbf B^{\mathsf T}\mathbf j\)
- [Gold Standard ข้อ 4.3](../4.3/solution.md): รูปแบบการอธิบาย การตรวจอิสระ และมาตรฐานสื่อประกอบ
- [NPTEL / IIT Kharagpur — Network Analysis](https://archive.nptel.ac.in/content/syllabus_pdf/108105159.pdf):
  graph, tree, cut-set และความสัมพันธ์ของเมทริกซ์ \([A],[B],[Q]\)
- [MIT OpenCourseWare — Circuit Analysis using the Node and Mesh Methods](https://ocw.mit.edu/courses/6-071j-introduction-to-electronics-signals-and-measurement-spring-2006/9d19116cbabeada1c98004a4367a0ee0_nodal_mesh_methd.pdf):
  ขั้นตอนกำหนดทิศกระแส/ขั้วก่อนใช้ KVL และแก้สมการ
- [Nilsson & Riedel, Electric Circuits, Pearson](https://www.pearson.com/content/dam/one-dot-com/one-dot-com/us/en/files/14939-ENG-Nilsson-ElectricCircuits-12E.pdf):
  ตำราระดับปริญญาตรีในหัวข้อ Techniques of Circuit Analysis
