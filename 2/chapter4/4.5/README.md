# โจทย์ 4.5 — Tie-set Analysis with CCCS

ชุดโจทย์และเฉลยฉบับ Gold Standard สำหรับวงจร 3 ปม 3 กิ่งประกอบที่มีแหล่งกระแสอิสระ \(I_0\) และแหล่งกระแสควบคุมด้วยกระแส \(\alpha i_x\)

## เริ่มอ่าน

- [Interactive Reader](./index.html) — ฉบับเว็บ มี MathJax, dark/light mode, สารบัญ, SVG และเครื่องคำนวณตรวจคำตอบ
- [เฉลยฉบับสมบูรณ์](./solution.md) — พิสูจน์สเกลาร์และเมทริกซ์ทุกขั้น พร้อมการตรวจอิสระ
- [โจทย์และสัญกรณ์](./problem.md)
- [การถอดรหัสรูป](./figure-analysis.md)
- [ภาพโจทย์ต้นฉบับ](./problem.png)

## ตารางคำตอบย่อ

กำหนด

\[
D=R_1+R_3+(1-\alpha)R_2\ne0.
\]

| ปริมาณ | คำตอบ |
|---|---|
| \(\mathbf B\) | \(\begin{bmatrix}1&1&-1\end{bmatrix}\) |
| \(j_1\) | \(\dfrac{(\alpha R_2-R_1)I_0}{D}\) |
| \(i_x\) | \(\dfrac{(R_2+R_3)I_0}{D}\) |
| \((i_1,i_2,i_3)\) | \((j_1,j_1,-j_1)\) |
| \(v_1\) | \(\dfrac{R_3(\alpha R_2-R_1)I_0}{D}\) |
| \(v_2\) | \(-\dfrac{R_2(R_1+\alpha R_3)I_0}{D}\) |
| \(v_3\) | \(-\dfrac{R_1(R_2+R_3)I_0}{D}\) |
| \(V_A\) | \(\dfrac{R_1(R_2+R_3)I_0}{D}\) |
| \(V_B\) | \(\dfrac{R_3(R_1-\alpha R_2)I_0}{D}\) |

กรณี \(D=0\) เป็นระบบเอกฐานและต้องพิจารณาแยกตามค่า \(I_0\); ดูรายละเอียดใน [solution.md §15.6](./solution.md#156-กรณีเอกฐาน-d0)

## โครงสร้างไฟล์

| พาธ | รายละเอียด |
|---|---|
| [`solution.md`](./solution.md) | เฉลย 21 หัวข้อ รวม matrix multiplication, nodal verification, KVL/KCL, limits และ Tellegen |
| [`index.html`](./index.html) | Interactive Reader แบบ responsive |
| [`make_figures.py`](./make_figures.py) | สคริปต์ Python standard library สำหรับสร้าง SVG 8 ภาพ |
| [`assets/`](./assets/) | SVG เวกเตอร์ที่สร้างซ้ำได้ |
| [`figures/`](./figures/) | ภาพครอบจากโจทย์ต้นฉบับ |
| [`problem.md`](./problem.md) | โจทย์ สัญกรณ์ ทิศกิ่ง และขั้วแรงดัน |
| [`figure-analysis.md`](./figure-analysis.md) | วิเคราะห์ปม กิ่ง tree/link และตัวแปรควบคุม |
| [`problem.png`](./problem.png) | ภาพโจทย์ต้นฉบับ |

## สร้างภาพใหม่

จากราก repository:

```bash
python3 engineering-problem/circuit/2/chapter4/4.5/make_figures.py
```

สคริปต์ไม่พึ่งไลบรารีภายนอกและจะเขียน SVG 8 ไฟล์ลง `assets/`

## แหล่งอ้างอิง

- [Lecture 04 — Loop / Tie-set Analysis](../lecture/303212S1Y2569lec04_5048.pdf)
- [Benchmark 4.3](../4.3/solution.md)
- [Benchmark 4.4](../4.4/solution.md)
- [Visual Matrix Benchmark 4.4](../4.4/solution-2/solution-matrix-visual.md)
