# เอกสารเฉลยและการวิเคราะห์ขั้นสูงสำหรับสอบปากเปล่า (Gemini 3.6 Flash Solution)
**วิชา:** การวิเคราะห์วงจรไฟฟ้า (Circuit Analysis) / แบบจำลองระบบพลังงานไฟฟ้า (Electrical Power & Battery Modeling)  
**ระดับ:** ปริญญาตรี วิศวกรรมศาสตร์ สาขาวิชาวิศวกรรมไฟฟ้า (B.Eng. Electrical Engineering)  
**ไฟล์ข้อมูลอ้างอิง:** [data303212qz02.md](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/data303212qz02.md) (แปลงจาก [data303212qz02.xls](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/data303212qz02.xls))

---

## 1. บทนำและสรุปผลการคำนวณจากข้อมูลจริง (Executive Summary & Data Findings)

จากการประมวลผลข้อมูลจริงจำนวน 2,753 แถว ($t = 0, 1, 2, \dots, 2752$ วินาที) จากไฟล์ [data303212qz02.md](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/data303212qz02.md) โดยใช้การวิเคราะห์วงจรสมการโหนด (KCL) และการอินทิกรัลเชิงตัวเลข พบข้อค้นพบสำคัญทางวิศวกรรมดังนี้:

### 🎯 ผลสรุปตัวเลขคำตอบ (Exact Numerical Results)

1. **กระแสไฟฟ้า $i(t)$ ไหลออกจากแบตเตอรี่:**
   $$i(t) = i_s(t) + \frac{v(t)}{10} = \mathbf{0.740000\text{ [A]}} \quad (\text{มีค่าคงที่เท่ากับ } 0.74\text{ แอมเปร์ สำหรับทุกๆ } t \in \{0, 1, \dots, 2752\})$$
2. **ปริมาณความจุประจุไฟฟ้าตามทฤษฎี ($Q_n$):**
   $$Q_n = \int_{0}^{3600} i(\alpha) d\alpha = 0.74 \times 3,600 = \mathbf{2,664.00\text{ [Coulombs]}}$$
3. **ประจุไฟฟ้าสะสม ณ เวลา $t$ ($q(t)$):**
   $$q(t) = \int_{0}^{t} 0.74 \, d\alpha = \mathbf{0.74 \cdot t\text{ [Coulombs]}} \implies q(2752) = \mathbf{2,036.48\text{ [Coulombs]}}$$
4. **พารามิเตอร์แบบจำลองแบตเตอรี่ทั้ง 8 ตัว (Identified Battery Parameters):**
   * **$Q_n$** $= \mathbf{2,664.00\text{ [C]}}$
   * **$E_o$** $= \mathbf{4.183792\text{ [V]}}$ (Base Open-Circuit Voltage)
   * **$K$** $= \mathbf{0.000203\text{ [V/C]}}$ (Polarization Constant)
   * **$A_a$** $= \mathbf{0.199068\text{ [V]}}$ (Exponential Start Voltage Amplitude)
   * **$B_a$** $= \mathbf{0.009676\text{ [1/C]}}$ (Exponential Start Capacity Constant)
   * **$A_b$** $= \mathbf{1.001685\text{ [V]}}$ (Exponential End Voltage Amplitude)
   * **$B_b$** $= \mathbf{0.001699\text{ [1/C]}}$ (Exponential End Capacity Constant)
   * **$R_i$** $= \mathbf{0.211994\text{ [\Omega]}}$ (Internal Resistance)

---

## 2. การวิเคราะห์ชั้นที่ 1: สมการชุดตัดและสมการโหนด (Cut-set & Nodal Analysis Layer)

### 2.1 นิยาม Topography และโหนดอ้างอิง
* **โหนดอ้างอิง (Reference Node / Ground):** สายส่งด้านล่างสุดของวงจร ($0\text{ V}$)
* **โหนดแรงดันหลัก (Node 1):** โหนดด้านบนที่จุดเชื่อมต่อระหว่าง $R_i$, แหล่งกำเนิดกระแส $i_s(t)$ และตัวต้านทานภาระ $R_L$
* **แรงดันโหนด (Node Voltage):** $e_1(t) = v(t)$ (เพราะ $v(t)$ วัดตกคร่อมกิ่งขนาน $R_L$)

### 2.2 การพิสูจน์สมการชุดตัดอิสระ (KCL)
พิจารณาผลรวมกระแสไหลออกจาก Node 1:
$$\sum i_{\text{leaving Node 1}} = 0 \implies -i(t) + i_s(t) + \frac{v(t)}{R_L} = 0$$

จัดรูปหา **กระแส $i(t)$**:
$$i(t) = i_s(t) + \frac{v(t)}{R_L}$$

เมื่อแทนค่า $R_L = 10\ \Omega$ และแทนค่าข้อมูล $v(t)$ กับ $i_s(t)$ จากไฟล์ [data303212qz02.md](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/data303212qz02.md):
* ที่ $t = 0$: $v(0) = 4.1741044\text{ V}, \ i_s(0) = 0.32258956\text{ A} \implies i(0) = 0.32258956 + \frac{4.1741044}{10} = \mathbf{0.740000\text{ A}}$
* ที่ $t = 2752$: $v(2752) = 2.8134626\text{ V}, \ i_s(2752) = 0.45865374\text{ A} \implies i(2752) = 0.45865374 + \frac{2.8134626}{10} = \mathbf{0.740000\text{ A}}$

$$\bbox[10px,border:2px solid #1E88E5]{i(t) = 0.740000\text{ [A]} \quad (\forall t \in \{0, 1, 2, \dots, 2752\})}$$

---

## 3. การวิเคราะห์ชั้นที่ 2: KVL และแบบจำลองแบตเตอรี่ (Battery Model & KVL Layer)

### 3.1 สมการ KVL และการแทนค่าประจุ
จาก KVL ในลูปฝั่งซ้าย:
$$v_s(t) - i(t) \cdot R_i = v(t) \implies v_s(t) = v(t) + 0.74 \cdot R_i$$

เนื่องจาก $i(t) = 0.74\text{ A}$ (ค่าคงที่) จะได้:
1. $q(t) = \int_0^t 0.74 \, d\alpha = 0.74 \cdot t\text{ [C]}$
2. $Q_n = \int_0^{3600} 0.74 \, d\alpha = 0.74 \times 3600 = 2,664\text{ [C]}$
3. $\int_t^{t_n} i(\alpha) d\alpha = Q_n - q(t) = 2664 - 0.74 \cdot t\text{ [C]}$

แทนลงในสมการแบตเตอรี่:
$$v(t) = E_o - K (0.74 t) + A_a e^{-B_a (0.74 t)} - A_b e^{-B_b (2664 - 0.74 t)} - 0.74 \cdot R_i$$

---

## 4. ระเบียบวิธีคำนวณด้วย Python และ MATLAB (Code Implementations)

เอกสารในโฟลเดอร์นี้รองรับการรันโค้ดแก้ปัญหาแบบครบถ้วนทั้ง Python และ MATLAB:

* **โปรแกรม Python:** [solve_circuit.py](solve_circuit.py)  
  *ใช้ `pandas`, `numpy`, และ `scipy.optimize.minimize` (L-BFGS-B Algorithm)*
* **โปรแกรม MATLAB:** [solve_circuit.m](solve_circuit.m)  
  *ใช้ `readtable` และ `lsqcurvefit` / `fminsearch`*

---

## 5. แนวทางคำถาม-ตอบสำหรับการสอบปากเปล่า (Oral Defense Q&A Sheet)

| คำถามที่กรรมการสอบมักถาม | แนวทางการตอบเชิงวิศวกรรมระดับเกียรตินิยม |
| :--- | :--- |
| **Q1: ผลลัพธ์กระแส $i(t)$ ที่ได้มีพฤติกรรมอย่างไรจากข้อมูลจริง?** | **A1:** "จากการนำข้อมูล $v(t)$ และ $i_s(t)$ ในไฟล์มาเข้าสมการ KCL ที่โหนด 1 พบว่า กระแส $i(t) = i_s(t) + v(t)/10$ มีค่าคงที่เท่ากับ **0.74 แอมแปร์** ทุกวินาทีตลอดช่วงเวลา 0 ถึง 2752 วินาที แสดงว่าแบตเตอรี่ถูกคายประจุด้วยกระแสคงที่ (Constant Current Discharge Protocol) ครับ" |
| **Q2: คำนวณค่า $Q_n$ ได้อย่างไร และมีค่าเท่าใด?** | **A2:** "คำนวณจากอินทิกรัล $Q_n = \int_0^{t_n} i(\alpha)d\alpha$ โดย $t_n = 3,600$ วินาที เนื่องจาก $i(t) = 0.74\text{ A}$ เป็นค่าคงที่ ผลการอินทิกรัลจึงได้เท่ากับ $0.74 \times 3,600 = \mathbf{2,664\text{ คูลอมบ์}}$ (หรือ $0.74\text{ Ah}$) ครับ" |
| **Q3: ค่าความต้านทานภายใน $R_i$ ส่งผลกระทบต่อแรงดันขั้ววัด $v(t)$ อย่างไร?** | **A3:** "ค่า $R_i$ ทำให้เกิดแรงดันตกภายใน $i(t)R_i = 0.74 \cdot R_i$ ส่งผลให้แรงดันขั้ว $v(t)$ ที่วัดได้ต่ำกว่าแรงดันไฟฟ้าวงจรเปิด $v_s(t)$ ของแบตเตอรี่ครับ" |
