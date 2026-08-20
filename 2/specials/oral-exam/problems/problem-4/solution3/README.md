# solution3 — ข้อที่ 4: วงข่ายความนำไฟฟ้าและแหล่งกำเนิดกระแสไม่อิสระ

**วิชา 303212 การวิเคราะห์วงจรไฟฟ้า 2** · Conductance Network · CCCS · Fundamental Cut-set Matrix  
**เป้าหมาย:** อ่านจากศูนย์ เข้าใจทุกเครื่องหมาย สร้างสมการเอง และตอบกรรมการได้ถึงระดับ 100/100

> 🚀 **เริ่มที่นี่:** [interactive_dashboard.html](interactive_dashboard.html) — แดชบอร์ดโต้ตอบ 6 แท็บ เปิดในเบราว์เซอร์ได้ทันที

---

## เอกสารในโฟลเดอร์นี้

| ไฟล์ | หน้าที่ |
|---|---|
| [CLAUDE_SOLUTION.md](CLAUDE_SOLUTION.md) | บทเรียน 5 บท: ภาพกายภาพ → KCL/เมทริกซ์ชุดตัด → ตัวเลข → คอมพิวเตอร์/ความไว → ซ้อมปากเปล่า 15 ข้อ |
| [interactive_dashboard.html](interactive_dashboard.html) | สื่อ Dark Mode + Glassmorphism, 6 แท็บ, ปุ่มเปิดรูปโจทย์, Cut-set Inspector และ CCCS Lab |
| [solve_circuit.py](solve_circuit.py) | SymPy symbolic check (ถ้ามี), NumPy matrix solver, Cramer cross-check, KCL residual และ alpha sweep |
| [solve_circuit.m](solve_circuit.m) | MATLAB/Octave solver โครงสร้างเดียวกับ Python |

ไฟล์อ้างอิง: [โจทย์ฉบับเต็ม](../oral_exam_problem.md) · [รูปวงจร](../circuit_fig4.png) · [รูปโจทย์](../image.png) · [หน้าหลัก](../../../index.html)

---

## คำตอบย่อ

กำหนด \(V_e=0\), \(i_x=G_1V_a\) และ CCCS ไหลจาก \(b\to a\) เป็น \(\alpha i_x\)

\[
\begin{bmatrix}
(1-\alpha)G_1+G_2 & -G_2\\
\alpha G_1-G_2 & G_2+G_3
\end{bmatrix}
\begin{bmatrix}V_a\\V_b\end{bmatrix}
=\begin{bmatrix}I_0\\0\end{bmatrix}
\]

\[
\Delta=G_1G_2+G_2G_3+(1-\alpha)G_1G_3
\]

\[
\boxed{V_a=\frac{I_0(G_2+G_3)}{\Delta}},
\qquad
\boxed{V_b=\frac{I_0(G_2-\alpha G_1)}{\Delta}}.
\]

สำหรับตัวอย่างในเอกสาร \((G_1,G_2,G_3,\alpha,I_0)=(0.8,0.35,0.55,0.4,2.4)\) ได้

| ปริมาณ | ค่า |
|---|---:|
| \(\Delta\) | \(0.736500\ \mho^2\) |
| \(V_a\) | \(2.932790224\ \mathrm V\) |
| \(V_b\) | \(0.097759674\ \mathrm V\) |
| \(i_x\) | \(2.346232179\ \mathrm A\) |
| \(\alpha i_x\) | \(0.938492872\ \mathrm A\) |

---

## สมการชุดตัดที่ใช้

เลือกต้นไม้ \(\{G_1,G_3\}\), กิ่งร่วม \(\{G_2,I_0,\alpha i_x\}\) และเรียงกิ่งเป็น
\([G_1,G_3,G_2,I_0,\alpha i_x]\)

\[
Q_K=\begin{bmatrix}1&0&1&-1&-1\\0&1&-1&0&1\end{bmatrix}
\]

สร้างตัวดำเนินการกิ่ง

\[
Y_b=\begin{bmatrix}
G_1&0&0&0&0\\
0&G_3&0&0&0\\
0&0&G_2&0&0\\
0&0&0&0&0\\
\alpha G_1&0&0&0&0
\end{bmatrix},
\qquad
J_b=\begin{bmatrix}0\\0\\0\\I_0\\0\end{bmatrix}.
\]

จึงได้

\[
Q_KY_bQ_K^T=
\begin{bmatrix}
(1-\alpha)G_1+G_2&-G_2\\
\alpha G_1-G_2&G_2+G_3
\end{bmatrix},
\qquad
J_{cut}=-Q_KJ_b=\begin{bmatrix}I_0\\0\end{bmatrix}.
\]

> ⚠️ จุดสำคัญ: ถ้าเป็นเครือข่าย passive ล้วน เมทริกซ์จะสมมาตร แต่ CCCS เป็น active/non-reciprocal source จึงทำให้สมาชิกนอกแนวทแยงไม่เท่ากันเมื่อ \(\alpha\ne0\)

---

## วิธีรัน

### Python

```bash
cd problems/problem-4/solution3
python3 solve_circuit.py
python3 solve_circuit.py --G1 0.8 --G2 0.35 --G3 0.55 --alpha 0.4 --I0 2.4
python3 solve_circuit.py --sweep-alpha --json
```

NumPy ใช้สำหรับตัวเลข ส่วน SymPy ใช้ตรวจรูปเชิงสัญลักษณ์ถ้าติดตั้งใน environment นั้น

```bash
python3 -m pip install numpy sympy
```

### MATLAB / GNU Octave

```matlab
cd problems/problem-4/solution3
solve_circuit
solve_circuit(0.8, 0.35, 0.55, 0.4, 2.4)
```

---

## เส้นทางอ่านที่แนะนำ

| เวลาที่มี | อ่าน/ทำอะไร |
|---|---|
| 10 นาที | CLAUDE_SOLUTION.md: “คำตอบปลายทาง” + กระดาษคำตอบ 30 วินาที |
| 30 นาที | บทที่ 1–2 และแดชบอร์ดแท็บ 1–4 |
| 20 นาที | บทที่ 3 พร้อมรัน `solve_circuit.py` |
| 45 นาที | บทที่ 5 ซ้อมบทตอบระดับรอดชีวิต แล้วเติมระดับเกียรตินิยม |
| ก่อนเข้าห้องสอบ | ใช้แท็บ 6 ปรับ \(\alpha\) และดูว่า \(\Delta\) เข้าใกล้ศูนย์อย่างไร |

## Checklist ความถูกต้อง

- [ ] อ่านทิศลูกศรของ \(I_0\), \(i_x\), CCCS ก่อนเขียน KCL
- [ ] จำว่า \(i_x=G_1V_a\) เพราะ \(G_1\) ต่อระหว่าง \(a\) กับกราวด์
- [ ] แยกสมการปม \(b\) สองรูปที่ต่างกันด้วยเครื่องหมายทั้งแถวได้
- [ ] ใส่ coupling \(\alpha G_1\) ใน \(Y_b\); ห้ามใช้ diagonal passive matrix อย่างเดียว
- [ ] ตรวจ \(\Delta\), Cramer’s Rule, KCL residual และ matrix residual
- [ ] อธิบายได้ว่า \(\Delta=0\) คือจุด singular/critical feedback ไม่ใช่เลขที่ควรหารผ่าน
- [ ] ซ้อมคำถามปากเปล่า 15 ข้อให้ตอบได้ทั้งสองระดับ

**ประโยคจำ:** *ภาพทิศทาง → KCL → เมทริกซ์ → ตรวจกลับ → อธิบายความหมาย* — อย่ากระโดดข้ามลำดับนี้
