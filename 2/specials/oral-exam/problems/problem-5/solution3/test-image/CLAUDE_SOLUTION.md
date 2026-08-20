# เฉลยและบทเรียนฉบับพิสูจน์ตามหลักทฤษฎีกราฟ 21 ขั้นตอน — (Tree = {1, 2}, Links = {3, 4})

> **วิชา:** 303212 การวิเคราะห์วงจรไฟฟ้า 2 · **โจทย์:** สอบปากเปล่า (Oral Exam Special Problem 5)
> **วิธีการ:** Fundamental Cut-set Analysis อิงกิ่งต้นไม้ $T = \{1, 2\}$ และกิ่งร่วม $L = \{3, 4\}$
> **ทิศทางกิ่งอ้างอิง:** $1: e \to a, \ 2: a \to b, \ 3: a \to e, \ 4: e \to b$ (ตรงตามรูปกราฟ 5 ข)

---

# 1. ทิศของกิ่งทั้ง 4 จากกราฟโจทย์ (Figure 5b)

จากกราฟมีทิศทางของโจทย์ มี 4 กิ่งเป๊ะ:

$$\boxed{1: e \to a}$$
$$\boxed{2: a \to b}$$
$$\boxed{3: a \to e}$$
$$\boxed{4: e \to b}$$

เรียงเวกเตอร์กระแสกิ่งเป็น:

$$\mathbf{i} = \begin{bmatrix} i_1 \\ i_2 \\ i_3 \\ i_4 \end{bmatrix}$$

---

# 2. เลือก Tree และ Links

กำหนด:

$$\boxed{\text{Twigs} = \{1, 2\}} \qquad \boxed{\text{Links} = \{3, 4\}}$$

ลักษณะของ Tree เชื่อมต่อปม:

$$e \xrightarrow{1} a \xrightarrow{2} b$$

มี 3 ปม คือ $a, b, e$
จำนวนกิ่งต้นไม้ต้องเท่ากับ $n - 1 = 3 - 1 = 2$ กิ่งพอดี ดังนั้น Tree $=\{1, 2\}$ จึงเป็น Tree ที่ถูกต้องตามทฤษฎีกราฟ

---

# 3. Fundamental Cut-set ($c_1$)

## 3.1 ตัด Twig 1 ออกจาก Tree
Twig 1 เชื่อม $e \to a$ เมื่อถอดกิ่ง 1 ออก Tree จะแยกเป็น 2 กลุ่ม:
* กลุ่มแรก: $\{e\}$
* กลุ่มที่สอง: $\{a, b\}$

ดังนั้น Cut $c_1$ คือเส้นเกาส์ที่แบ่ง:

$$\boxed{c_1: \{e\} \mid \{a, b\}}$$

## 3.2 พิจารณากิ่งที่ข้ามผ่าน Cut $c_1$
* กิ่ง 1 ($e \to a$): ข้าม
* กิ่ง 2 ($a \to b$): อยู่ภายในชุดปม $\{a, b\}$ ไม่ข้าม
* กิ่ง 3 ($a \to e$): ข้าม
* กิ่ง 4 ($e \to b$): ข้าม

ดังนั้น Cut $c_1$ ตัดผ่านกิ่ง:

$$\boxed{c_1: \{1, 3, 4\}}$$

---

# 4. กำหนดเครื่องหมายของ Cut $c_1$

> **กติกา:** ให้ทิศของ Cut-set อิงตามทิศของ Tree Twig ที่สร้าง Cut นั้น (Twig 1 ชี้ $e \to a$)

ดังนั้น Cut $c_1$ ชี้จาก $\{e\} \to \{a, b\}$:

* **กิ่ง 1 ($e \to a$):** ทิศเดียวกับ Cut $c_1$ $\implies \mathbf{+1}$
* **กิ่ง 2 ($a \to b$):** ไม่ตัด $\implies \mathbf{0}$
* **กิ่ง 3 ($a \to e$):** สวนทางกับ Cut $c_1$ $\implies \mathbf{-1}$
* **กิ่ง 4 ($e \to b$):** ทิศเดียวกับ Cut $c_1$ (ชี้จาก $e \to \{a, b\}$) $\implies \mathbf{+1}$

ดังนั้น แถวที่ 1 ของเมทริกซ์ $[Q_f]$ คือ:

$$\boxed{\text{แถวที่ 1} = \begin{bmatrix} +1 & 0 & -1 & +1 \end{bmatrix}}$$

---

# 5. Fundamental Cut-set ($c_2$)

ถอด Twig 2 ($a \to b$) ออกจาก Tree
Tree จะถูกแยกเป็น 2 กลุ่ม:
* กลุ่มแรก: $\{e, a\}$
* กลุ่มที่สอง: $\{b\}$

ดังนั้น Cut $c_2$ แบ่ง:

$$\boxed{c_2: \{e, a\} \mid \{b\}}$$

## 5.1 กิ่งที่ตัดผ่าน Cut $c_2$
* กิ่ง 1 ($e \to a$): อยู่ฝั่งเดียวกัน ไม่ตัด $\implies 0$
* กิ่ง 2 ($a \to b$): ตัด $\implies$ ข้าม
* กิ่ง 3 ($a \to e$): อยู่ฝั่งเดียวกัน ไม่ตัด $\implies 0$
* กิ่ง 4 ($e \to b$): ตัด $\implies$ ข้าม

ดังนั้น Cut $c_2$ ตัดผ่านกิ่ง:

$$\boxed{c_2: \{2, 4\}}$$

---

# 6. กำหนดเครื่องหมายของ Cut $c_2$

ใช้ทิศ Twig 2 ($a \to b$) เป็นทิศอ้างอิงของ Cut $c_2$ (ชี้จาก $\{a, e\} \to \{b\}$):

* **กิ่ง 2 ($a \to b$):** ทิศเดียวกับ Cut $c_2$ $\implies \mathbf{+1}$
* **กิ่ง 4 ($e \to b$):** ชี้จากฝั่ง $\{a, e\}$ ไปยัง $b$ ทิศเดียวกับ Cut $c_2$ $\implies \mathbf{+1}$

ดังนั้น แถวที่ 2 ของเมทริกซ์ $[Q_f]$ คือ:

$$\boxed{\text{แถวที่ 2} = \begin{bmatrix} 0 & +1 & 0 & +1 \end{bmatrix}}$$

---

# 7. Fundamental Cut-set Matrix $[Q_f]$ ที่ถูกต้อง (2 x 4)

เรียงคอลัมน์ $[1, 2, 3, 4]$:

$$\boxed{Q_f = \begin{bmatrix} 1 & 0 & -1 & 1 \\ 0 & 1 & 0 & 1 \end{bmatrix}}$$

---

# 8. เขียนสมการ Cut-set Matrix $[Q_f] \mathbf{i} = \mathbf{0}$

$$\begin{bmatrix} 1 & 0 & -1 & 1 \\ 0 & 1 & 0 & 1 \end{bmatrix} \begin{bmatrix} i_1 \\ i_2 \\ i_3 \\ i_4 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$

คูณทีละแถว:

$$\boxed{i_1 - i_3 + i_4 = 0} \tag{C1}$$

$$\boxed{i_2 + i_4 = 0} \tag{C2}$$

จากสมการ (C2): $i_4 = -i_2$
แทนใน (C1): $i_1 - i_3 + (-i_2) = 0 \implies \mathbf{i_1 - i_2 - i_3 = 0}$ (ตรงตาม KCL ที่ปม $a$)

---

# 9. สมการกระแสกิ่งในรูปแรงดันโหนด $(V_a, V_b)$

กำหนด $V_e = 0$ (Reference Ground)

### กิ่ง 1 ($e \to a$):
$$i_1 = G_1(E_1 - V_a)$$

### กิ่ง 2 ($a \to b$):
$$i_2 = G_2(V_a + E_3 - V_b)$$

### กิ่ง 3 ($a \to e$):
$$i_3 = G_3 V_a$$

### กิ่ง 4 ($e \to b$):
ในวงจรจริงระหว่าง $e$ กับ $b$ มี $G_4 \parallel E_2$
$$i_4 = i_{G4} + i_{E2}$$
โดยกระแสผ่านความนำ $i_{G4} = G_4(V_e - V_b) = -G_4 V_b$ (ชี้ $e \to b$)
$$\boxed{i_4 = -G_4 V_b + i_{E2}}$$

---

# 10. แทนกระแสกิ่งทั้งหมดลงใน Cut-set Matrix

$$\begin{bmatrix} 1 & 0 & -1 & 1 \\ 0 & 1 & 0 & 1 \end{bmatrix} \begin{bmatrix} G_1(E_1 - V_a) \\ G_2(V_a + E_3 - V_b) \\ G_3 V_a \\ -G_4 V_b + i_{E2} \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$

---

# 11. กระจายแถวที่ 1

จาก $i_1 - i_3 + i_4 = 0$:
$$G_1(E_1 - V_a) - G_3 V_a + (-G_4 V_b + i_{E2}) = 0$$
$$G_1 E_1 - G_1 V_a - G_3 V_a - G_4 V_b + i_{E2} = 0$$
$$\boxed{(G_1 + G_3) V_a + G_4 V_b - i_{E2} = G_1 E_1} \tag{1}$$

---

# 12. กระจายแถวที่ 2

จาก $i_2 + i_4 = 0$:
$$G_2(V_a + E_3 - V_b) + (-G_4 V_b + i_{E2}) = 0$$
$$G_2 V_a + G_2 E_3 - G_2 V_b - G_4 V_b + i_{E2} = 0$$
คูณด้วย (-1) เพื่อจัดรูปง่าย:
$$\boxed{-G_2 V_a + (G_2 + G_4) V_b - i_{E2} = G_2 E_3} \tag{2}$$

---

# 13. ระบบสมการเมทริกซ์เต็ม 3 ตัวแปร $(V_a, V_b, i_{E2})$

$$\begin{bmatrix} G_1 + G_3 & G_4 & -1 \\ -G_2 & G_2 + G_4 & -1 \\ 0 & 1 & 0 \end{bmatrix} \begin{bmatrix} V_a \\ V_b \\ i_{E2} \end{bmatrix} = \begin{bmatrix} G_1 E_1 \\ G_2 E_3 \\ -E_2 \end{bmatrix}$$

โดยที่แถวที่ 3 คือเงื่อนไขแหล่งจ่ายแรงดันอุดมคติ $V_e - V_b = E_2 \implies \mathbf{V_b = -E_2}$

---

# 14. กำจัดตัวแปร $i_{E2}$

นำสมการ (1) ลบ สมการ (2):
$$(1) - (2) \implies (G_1 + G_2 + G_3) V_a - G_2 V_b = G_1 E_1 - G_2 E_3 \tag{3}$$

---

# 15. ระบบสมการเมทริกซ์ 2 ตัวแปร $(V_a, V_b)$

$$\boxed{\begin{bmatrix} G_1 + G_2 + G_3 & -G_2 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} V_a \\ V_b \end{bmatrix} = \begin{bmatrix} G_1 E_1 - G_2 E_3 \\ -E_2 \end{bmatrix}}$$

---

# 16. ถอดคำตอบสุดท้ายสำหรับ $V_a$ และ $V_b$

$$\boxed{\mathbf{V_b = -E_2}}$$

$$\boxed{\mathbf{V_a = \frac{G_1 E_1 - G_2 E_3 - G_2 E_2}{G_1 + G_2 + G_3}}}$$

---

# 17. ตัวเลขคำนวณจริง (แทนค่าพารามิเตอร์):
$(G_1=0.4, G_2=0.3, G_3=0.2, G_4=0.5\ \Omega^{-1}, E_1=12, E_2=6, E_3=2\ \text{V})$

$$V_b = -6.000000\ \text{V}$$
$$V_a = \frac{0.4(12) - 0.3(2) - 0.3(6)}{0.4 + 0.3 + 0.2} = \frac{4.8 - 0.6 - 1.8}{0.9} = \frac{2.4}{0.9} = \mathbf{2.666667\ \text{V}} = \frac{8}{3}\ \text{V}$$

### กระแสกิ่งทั้ง 4:
* $i_1 = 0.4 \times (12 - 2.666667) = \mathbf{3.733333\ \text{A}}$
* $i_2 = 0.3 \times (2.666667 + 2 - (-6)) = \mathbf{3.200000\ \text{A}}$
* $i_3 = 0.2 \times 2.666667 = \mathbf{0.533333\ \text{A}}$
* $i_4 = -i_2 = \mathbf{-3.200000\ \text{A}}$ ($i_{G4} = 3.000000\ \text{A}, \ i_{E2} = -6.200000\ \text{A}$)
