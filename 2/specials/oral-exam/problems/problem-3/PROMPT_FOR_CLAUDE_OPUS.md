# Master Prompt: สั่งการ Claude Opus / Claude 3.7 Sonnet (โจทย์ข้อที่ 3)

> **คำชี้แจงสำหรับการใช้งาน:** 
> คัดลอกข้อความในกรอบด้านล่างทั้งหมด ไปวางในช่องแชตของ Claude Opus หรือ Claude 3.7 Sonnet 
> เพื่อสั่งให้ AI ประมวลผลและสร้างชุดเฉลยพร้อมสื่อการสอนแบบโต้ตอบสำหรับ **โจทย์สอบปากเปล่า ข้อที่ 3 (วงข่ายความนำไฟฟ้าและสมการชุดตัด)** ตามมาตรฐาน **Skill `circuit2-oral-exam-generator`** ให้ได้ผลลัพธ์ระดับเกียรตินิยม ละเอียด ละออ และไร้จุดสะดุด 100%

---

```markdown
Role & Master Educator Directive:
คุณคือ "อาจารย์มหาวิทยาลัยผู้คลั่งไคล้การสอนวิศวกรรมไฟฟ้า" (Master Human EE Educator) 
เราเลือกใช้คุณ (Claude Opus / Claude 3.7 Sonnet) เป็น "ทางเลือกสุดท้าย" หลังจากพบว่า AI รุ่นอื่นๆ ให้ผลลัพธ์ที่ตื้นเขิน ภาษาทื่อเหมือนหุ่นยนต์ AI ข้ามขั้นตอนคณิตศาสตร์ และไม่สามารถสร้างความเข้าใจที่แท้จริงให้กับนิสิตได้!

โปรดปฏิบัติตามมาตรฐานการสอนใน Skill `circuit2-oral-exam-generator` (ในไฟล์ .agents/skills/circuit2-oral-exam-generator/SKILL.md) อย่างเคร่งครัด!

ภารกิจหลักของคุณคือ: "สร้างชุดเฉลยและสื่อการสอนใหม่ใน problems/problem-3/solution3/ สำหรับโจทย์ข้อที่ 3 (วงข่ายความนำไฟฟ้า Conductance Network & สมการชุดตัด Cut-set Matrix) ที่สอนนิสิตไร้พื้นฐานให้เข้าใจลึกซึ้ง ไร้จุดสะดุด เรียงลำดับความคิดอย่างร้อยเรียงสมบูรณ์แบบ จนสามารถตอบคำถามกรรมการสอบปากเปล่าได้คะแนนเต็ม 100/100!"

---

📖 บริบทโจทย์ข้อที่ 3 (Problem Context & Reference Files):
1. ไฟล์โจทย์และตารางอุปกรณ์: problems/problem-3/oral_exam_problem.md
2. รูปภาพประกอบ: problems/problem-3/image.png และ circuit_fig3.png
3. รายละเอียดวงจร:
   - วงข่ายความนำไฟฟ้า $G_1, G_2, G_3, G_4 [\mho]$ (Conductance in Siemens/Mho)
   - แหล่งกำเนิดแรงดันอิสระ $E_1, E_2, E_3 [\text{V}]$ (Independent Voltage Sources)
   - ปมไฟฟ้า $a, b, c, d$ และปมอ้างอิงลงดิน $e$ ($V_e = 0\text{ V}$)
   - ความสัมพันธ์แหล่งกำเนิดแรงดัน:
     • $V_a = E_1$
     • $V_d = -E_2$ (ขั้วลบต่อที่ปม $d$, ขั้วบวกต่อที่กราวด์ $e$)
     • $V_c - V_b = E_3 \implies V_c = V_b + E_3$ (สร้าง Supernode ระหว่างปม $b$ และ $c$)
   - คำสั่งโจทย์: เขียนสมการชุดตัด (Cut-set Matrix Equation) ในรูปแบบเมทริกซ์เวกเตอร์ $[Q_K][Y_b][Q_K]^T \mathbf{V}_n = \mathbf{J}_{cut}$ และหาค่าแรงดันปม $V_a, V_b, V_c, V_d$

---

🎯 สิ่งที่ต้องสร้างและขยายความลึกใน CLAUDE_SOLUTION.md ( Seamless Scaffolding ):

1. บทที่ 1: มโนทัศน์กายภาพความนำไฟฟ้าและทฤษฎีกราฟวงจร (Physical Conductance & Graph Theory Intuition):
   - ปูพื้นฐานจาก 0: ความแตกต่างระหว่างความต้านทาน $R [\Omega]$ กับความนำไฟฟ้า $G [\mho]$, อุปมาอุปไมยความกว้างของท่อน้ำ
   - อธิบายมโนทัศน์กราฟวงจร (Oriented Graph), กิ่งต้นไม้ (Tree Branches), กิ่งร่วม (Links/Co-tree) และรอยตัดพื้นฐาน (Fundamental Cut-sets) ด้วยภาษามนุษย์ที่อบอุ่นและเห็นภาพชัดเจน

2. บทที่ 2: พิสูจน์ KCL, Supernode และสมการชุดตัดทีละบรรทัด (Zero Mathematical Gaps):
   - ห้ามใช้คำว่า "ในทำนองเดียวกัน" หรือข้ามขั้นตอนย้ายข้างสมการเด็ดขาด!
   - พิสูจน์การตั้งสมการ KCL ที่ Supernode $(b, c)$:
     $G_1 (V_b - V_a) + G_3 V_b + G_2 (V_c - V_d) = 0$
   - แทนค่า $V_a = E_1, V_d = -E_2, V_c = V_b + E_3$ ลงในสมการ และแสดงการย้ายข้างจัดรูปหาค่า $V_b, V_c$ แบบบรรทัดต่อบรรทัด:
     $V_b = \frac{G_1 E_1 - G_2 E_3 - G_2 E_2}{G_1 + G_2 + G_3}$
     $V_c = \frac{G_1 E_1 + (G_1 + G_3) E_3 - G_2 E_2}{G_1 + G_2 + G_3}$
   - แสดงการสร้างเมทริกซ์รอยตัดผูกกับความนำ $[Q_K][Y_b][Q_K]^T \mathbf{V}_n = \mathbf{J}_{cut}$ อย่างละเอียดทุกสมาชิก (Matrix Element)

3. บทที่ 3: วิธีคำนวณแทนค่าตัวเลขแบบแสดงวิธีทำอย่างละเอียด (Hand Derivation & Numerical Step):
   - กำหนดตัวอย่างตัวเลขทศนิยมจริงสำหรับ $G_1, G_2, G_3, G_4$ และ $E_1, E_2, E_3$ และแสดงการแทนค่าบวก ลบ คูณ หาร ทศนิยม 6 ตำแหน่งทีละบรรทัด

4. บทที่ 4: การคำนวณด้วยคอมพิวเตอร์และเปรียบเทียบวิธีคิด (Computer Matrix Solver & Verification):
   - เขียนสคริปต์ Python (`solve_circuit.py`) และ MATLAB (`solve_circuit.m`) ตั้งเมทริกซ์แก้สมการเชิงเส้น $\mathbf{A} \mathbf{x} = \mathbf{b}$
   - ตารางเปรียบเทียบผลลัพธ์ Hand Calculation vs Computer Matrix Solver

5. บทที่ 5: คัมภีร์ซ้อมตอบสอบปากเปล่าคะแนนเต็ม 100/100 (Master Oral Defense Guide 15 ข้อ):
   - เก็งคำถามสอบปากเปล่าเจาะลึก 15 ข้อ สำหรับโจทย์ข้อที่ 3 (เช่น ทำไมถึงต้องสร้าง Supernode, สัญลักษณ์ขั้ว $E_2$ มีผลต่อเครื่องหมายอย่างไร, สมการชุดตัดแตกต่างจาก Node Analysis ปกติอย่างไร)
   - แบ่งโครงสร้างการตอบเป็น 2 ระดับในทุกข้อ:
     [1] บทตอบรอดชีวิต (Defensive Script): ตอบตรงประเด็น ไม่ตกกับดัก (ได้คะแนนผ่าน)
     [2] บทตอบเกียรตินิยม (Proactive Distinction Script): ตอบเชื่อมโยง Graph Theory, Incidence Matrix และ State-space Formulation เพื่อให้กรรมการต้องแจก 100/100

---

💻 สิ่งที่ต้องสร้างใน interactive_dashboard.html ( Masterpiece Enhancement ):

1. Design & UI Standard (ตามมาตรฐาน Skill):
   - ติดตั้งปุ่มถอยหลังกลับหน้าหลักที่มุมบนซ้าย (`top: 14px; left: 14px;`) ลิงก์ `../../../index.html`
   - ติดตั้งปุ่มเปิดรูปภาพโจทย์ที่มุมซ้ายล่าง (`bottom: 24px; left: 24px;`) แสดงผลทุกแท็บ (สลับรูปภาพ `circuit_fig3.png` และ `image.png`)
   - ปุ่มเลื่อนแท็บ `◀` / `▶` สลับแท็บทันที ซ่อนเมื่อสุดขอบ

2. โครงสร้างแท็บเนื้อหา 6 แท็บ:
   - แท็บ 1: โจทย์จริง & วงจร (โจทย์ฉบับเต็ม + รูป circuit_fig3.png + Component Matrix)
   - แท็บ 2: ปูพื้นฐานความนำไฟฟ้า & ทฤษฎีกราฟ
   - แท็บ 3: พิสูจน์ KCL & Supernode ทีละบรรทัด
   - แท็บ 4: การสร้างสมการเมทริกซ์ชุดตัด (Cut-set Matrix Formulation)
   - แท็บ 5: คัมภีร์ซ้อมตอบสอบปากเปล่า 15 ข้อ (Oral Defense Masterclass)
   - แท็บ 6: Matrix & Conductance Laboratory (ปรับค่า $G_1..G_4, E_1..E_3$ โต้ตอบ Real-time พร้อมแสดงผลแรงดันปม $V_a, V_b, V_c, V_d$)

---

🔄 การเชื่อมโยงกับ Master Portal Hub และสารบัญ (Auto Sync):
1. อัปเดตไฟล์ index.html ที่ Root Directory ให้การ์ดโจทย์ข้อที่ 3 ปักป้าย `✅ พร้อมใช้งาน` พร้อมปุ่มกดทางเข้าหลักเพียงปุ่มเดียว:
   `<a href="problems/problem-3/solution3/interactive_dashboard.html" class="btn btn-primary">🚀 เข้าสู่เฉลย &amp; สื่อโต้ตอบ (ข้อที่ 3)</a>`
2. อัปเดตไฟล์ README.md ประจำข้อ 3 และ README.md ที่ Root Directory

จงดำเนินการสร้าง/ปรับปรุงไฟล์ทั้งหมดใน problems/problem-3/solution3/ (ทั้ง CLAUDE_SOLUTION.md, interactive_dashboard.html, README.md, solve_circuit.py) ให้เป็นเวอร์ชันสมบูรณ์แบบที่สุดตามมาตรฐาน Skill `circuit2-oral-exam-generator`!
```
