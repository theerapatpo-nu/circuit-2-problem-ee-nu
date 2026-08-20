# Master Prompt สำหรับส่งให้ ChatGPT (Model GPT-5.6 / GPT-5.6 SOL)

> 📌 **วิธีใช้งาน:** คัดลอกข้อความในกรอบด้านล่างนี้ทั้งหมด นำไปวางในช่องแชทของ **ChatGPT (GPT-5.6)** เพื่อให้ ChatGPT ดำเนินการวิเคราะห์ คำนวณ และสร้างเอกสารผลลัพธ์ลงในโฟลเดอร์ `solution2`

---

```markdown
# Role & Mission
คุณคือ **ChatGPT Model GPT-5.6 SOL (World-Class Electrical Engineering Professor & Master Systems Educator)** 

ภารกิจของคุณคือการเฉลยและสร้างสื่อการสอนสำหรับ **โจทย์การวิเคราะห์วงจรไฟฟ้าและโมเดลแบตเตอรี่ (Oral Exam Special Problem)** แบบ **"From Scratch" (สอนตั้งแต่ศูนย์)** เพื่อให้คนที่ไม่มีพื้นฐานวิศวกรรมเลยเข้าใจเรื่องวงจรไฟฟ้าทันที ตั้งแต่ที่มาที่ไป กฎทางฟิสิกส์ ทำไมต้องใช้สูตรนี้ ที่มาของสมการ ตลอดจนการทำ Parameter Estimation และคำนวณหาตัวเลขคำตอบจริงจากชุดข้อมูล 2,753 แถว

---

# Input Context & Reference Files
โปรดอ่านและอ้างอิงไฟล์ในระบบต่อไปนี้:
1. **ไฟล์โจทย์เพียวๆ และวิเคราะห์รูปวงจร:** `/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/oral_exam_problem.md`
2. **รูปภาพวงจรไฟฟ้า (รูปที่ 1):** `/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/circuit_fig1.png`
3. **ชุดข้อมูลอ้างอิง (2,753 แถว):** `/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/data303212qz02.md` (หรือ `data303212qz02.xls`)
4. **ไฟล์ประเมินและแผนผังความรู้:** `/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/PROBLEM_EVALUATION_AND_KNOWLEDGE_MAP.md`

---

# Target Output Directory
โปรดสร้างไฟล์และเก็บผลลัพธ์ทั้งหมดไว้ในโฟลเดอร์:
`/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/solution2/`

---

# Required Deliverables & Structure (สิ่งที่ต้องสร้างใน solution2/)

### 1. `GPT_SOLUTION.md` (เอกสารเฉลยและบทเรียนฉบับสมบูรณ์)
ให้เขียนเนื้อหาครอบคลุม 5 ส่วนหลักอย่างละเอียดลึกซึ้ง:

* **ส่วนที่ 1: ปูพื้นฐานจากศูนย์ (Circuit Fundamentals from Zero - Water Pipe Analogy)**
  * เปรียบเปรยไฟฟ้ากับ **"ระบบท่อน้ำ/ถังน้ำ"** เพื่ออธิบาย Voltage ($v$), Current ($i$), Resistance ($R$), KCL, KVL, และ Battery Model ($E_o, R_i, A_a, B_a, A_b, B_b$)
* **ส่วนที่ 2: การพิสูจน์และคำนวณโจทย์ทีละขั้นตอน (Step-by-Step Mathematical Derivation)**
  * พิสูจน์สมการโหนด KCL ที่ Node 1: $i(t) = i_s(t) + \frac{v(t)}{R_L} = 0.740000\text{ A}$ (ค่าคงที่ทุกจุดเวลา!)
  * อินทิกรัลหาประจุสะสม $q(t) = 0.74 t\text{ [C]}$ และความจุรวม $Q_n = 2,664.00\text{ [C]}$
* **ส่วนที่ 3: การวิเคราะห์แบตเตอรี่และการทำ Parameter Identification**
  * อธิบายโครงสร้างสมการนอนลินียร์ $v_s(t) = E_o - K q(t) + A_a e^{-B_a q(t)} - A_b e^{-B_b (Q_n - q(t))}$
  * การวิเคราะห์ Identifiability ($C_0 = E_o - 0.74 R_i$) และการทำ Non-linear Optimization
* **ส่วนที่ 4: คู่มือเตรียมสอบปากเปล่า (Oral Exam Defense Cheat Sheet)**
  * คำถาม-คำตอบสำหรับการสอบปากเปล่าวิศวกรรมไฟฟ้า
* **ส่วนที่ 5: สรุปเชิงเปรียบเทียบและการประยุกต์ใช้งานในโลกจริง (EV/BESS)**

---

### 2. `solvecircuit.py` (สคริปต์ Python)
* โค้ด Python สำหรับประมวลผลข้อมูล KCL, Non-linear Parameter Fitting และสร้างไฟล์กราฟ PNG (`signals_overview.png`, `voltage_fit.png`)

---

### 3. `solvecircuit.m` (สคริปต์ MATLAB)
* โค้ด MATLAB สำหรับคำนวณและทำ `fminsearch` / `lsqcurvefit`

---

### 4. `interactivedashboard.html` (แดชบอร์ดสื่อการสอนแบบโต้ตอบ Standalone HTML/JS)
* ไฟล์ HTML หน้าเดียว สไตล์ Modern Dark Mode + Glassmorphism UI พร้อม Interactive SVG Circuit, Dynamic Charts, Slider ปรับค่าพารามิเตอร์แบบ Real-time

---

### 5. `README.md` (เอกสารสารบัญสรุป solution2)
* สรุปสารบัญไฟล์ และคำอธิบายการใช้งานสื่อทั้งหมดในโฟลเดอร์ `solution2/`
```
