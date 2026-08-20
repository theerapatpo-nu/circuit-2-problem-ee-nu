# โจทย์ 4.6 — AC Steady-State Tie-set Analysis

ชุดโจทย์และเฉลยฉบับ Gold Standard สำหรับวงจร RLC ในสถานะอยู่ตัวไซน์ ใช้ Fundamental Tie-set Matrix และระบบเมทริกซ์-เวกเตอร์เชิงซ้อนเป็นแกนหลัก

## เริ่มอ่าน

- [Interactive Dashboard](./index.html) — MathJax, dark/light mode, SVG, เครื่องคำนวณเฟสเซอร์ และตัวตรวจ KVL/KCL/complex power
- [เฉลยฉบับสมบูรณ์](./solution.md) — พิสูจน์ทุกขั้นตั้งแต่ time-domain ถึง \(A_k\cos(\omega t+\phi_k)\)
- [โจทย์และสัญกรณ์](./problem.md)
- [วิเคราะห์รูปและ topology](./figure-analysis.md)
- [ภาพโจทย์ต้นฉบับ](./problem.png)

## คำตอบย่อ

เลือก

\[
T=\{3,4\},\qquad L=\{1,2\},
\]

\[
\mathbf B=
\begin{bmatrix}
1&0&0&-1\\
0&1&-1&-1
\end{bmatrix}.
\]

กำหนด \(Z_C=1/(j\omega C)\), \(Z_L=j\omega L\)

\[
\mathbf Z_l=
\begin{bmatrix}
R_1+Z_L&Z_L\\
Z_L&R_2+Z_C+Z_L
\end{bmatrix},
\qquad
\mathbf E_s=
\begin{bmatrix}-V_0\\jR_2I_0\end{bmatrix}.
\]

\[
\mathbf Z_l
\begin{bmatrix}J_1\\J_2\end{bmatrix}
=\mathbf E_s,
\qquad
\begin{bmatrix}I_1\\I_2\\I_3\\I_4\end{bmatrix}
=\begin{bmatrix}J_1\\J_2\\-J_2\\-J_1-J_2\end{bmatrix}.
\]

รายละเอียด determinant, คำตอบ rectangular/polar, แรงดันทุกกิ่ง และสูตรเวลาแบบปิดอยู่ใน [solution.md](./solution.md)

## โครงสร้างไฟล์

| พาธ | รายละเอียด |
|---|---|
| [`solution.md`](./solution.md) | เฉลย 24 หัวข้อ รวม nodal verification, limits และ complex power |
| [`index.html`](./index.html) | Interactive Dashboard แบบ responsive |
| [`make_figures.py`](./make_figures.py) | สคริปต์ Python standard library สร้าง SVG 8 ภาพ |
| [`assets/`](./assets/) | ภาพเวกเตอร์ phasor circuit, tree, matrix และ verification |
| [`problem.md`](./problem.md) | โจทย์ กิ่ง ทิศ และ phasor convention |
| [`figure-analysis.md`](./figure-analysis.md) | วิเคราะห์ปม กิ่ง tree/link และเมทริกซ์ตั้งต้น |
| [`figures/`](./figures/) | ภาพแยกจากเอกสารต้นฉบับ |

## สร้าง SVG ใหม่

```bash
python3 engineering-problem/circuit/2/chapter4/4.6/make_figures.py
```

## แหล่งอ้างอิง

- [Lecture 04 หน้าเอกสาร 96-100](../lecture/303212S1Y2569lec04_5048.pdf)
- [Gold Standard 4.5](../4.5/solution.md)
- [Visual Matrix 4.4](../4.4/solution-2/solution-matrix-visual.md)
- [Independent Checks 4.3](../4.3/solution.md)
