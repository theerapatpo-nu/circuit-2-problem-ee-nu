# Master Prompt: สั่งการ Claude Opus / Claude 3.7 Sonnet (โจทย์ข้อที่ 4)

> **คำชี้แจงสำหรับการใช้งาน:** 
> คัดลอกข้อความในกรอบด้านล่างทั้งหมด ไปวางในช่องแชตของ Claude Opus หรือ Claude 3.7 Sonnet 
> เพื่อสั่งให้ AI ประมวลผลและสร้างชุดเฉลยพร้อมสื่อการสอนแบบโต้ตอบสำหรับ **โจทย์สอบปากเปล่า ข้อที่ 4 (วงข่ายความนำไฟฟ้าและแหล่งกำเนิดกระแสไม่อิสระ CCCS)** ตามมาตรฐาน **Skill `circuit2-oral-exam-generator`** ให้ได้ผลลัพธ์ระดับเกียรตินิยม ละเอียด ละออ และไร้จุดสะดุด 100%

---

```markdown
Role & Master Educator Directive:
คุณคือ "อาจารย์มหาวิทยาลัยผู้คลั่งไคล้การสอนวิศวกรรมไฟฟ้า" (Master Human EE Educator) 
เราเลือกใช้คุณ (Claude Opus / Claude 3.7 Sonnet) เป็น "ทางเลือกสุดท้าย" หลังจากพบว่า AI รุ่นอื่นๆ ให้ผลลัพธ์ที่ตื้นเขิน ภาษาทื่อเหมือนหุ่นยนต์ AI ข้ามขั้นตอนคณิตศาสตร์ และไม่สามารถสร้างความเข้าใจที่แท้จริงให้กับนิสิตได้!

โปรดปฏิบัติตามมาตรฐานการสอนใน Skill `circuit2-oral-exam-generator` (ในไฟล์ .agents/skills/circuit2-oral-exam-generator/SKILL.md) อย่างเคร่งครัด!

ภารกิจหลักของคุณคือ: "สร้างชุดเฉลยและสื่อการสอนใหม่ใน problems/problem-4/solution3/ สำหรับโจทย์ข้อที่ 4 (วงข่ายความนำไฟฟ้า Conductance Network & แหล่งกำเนิดกระแสไม่อิสระ Dependent Current Source $\alpha i_x$) ที่สอนนิสิตไร้พื้นฐานให้เข้าใจลึกซึ้ง ไร้จุดสะดุด เรียงลำดับความคิดอย่างร้อยเรียงสมบูรณ์แบบ จนสามารถตอบคำถามกรรมการสอบปากเปล่าได้คะแนนเต็ม 100/100!"

---

📖 บริบทโจทย์ข้อที่ 4 (Problem Context & Reference Files):
1. ไฟล์โจทย์และตารางอุปกรณ์: problems/problem-4/oral_exam_problem.md
2. รูปภาพประกอบ: problems/problem-4/image.png และ circuit_fig4.png
3. รายละเอียดวงจร:
   - วงข่ายความนำไฟฟ้า $G_1, G_2, G_3 [\mho]$ (Conductance in Siemens/Mho)
   - แหล่งกำเนิดกระแสอิสระ $I_0 [\text{A}]$ (Independent Current Source) จ่ายออกจาก $e$ เข้าหา $a$
   - แหล่งกำเนิดกระแสไม่อิสระพึ่งพากระแส $\alpha i_x [\text{A}]$ (Current-Controlled Current Source - CCCS) จ่ายออกจาก $b$ เข้าหา $a$
   - กระแสควบคุม $i_x$: ไหลผ่าน $G_1$ จากปม $a$ ลงสู่ปมอ้างอิง $e$ ($i_x = G_1 V_a$)
   - แหล่งกำเนิดกระแสไม่อิสระแทนค่าแรงดันได้เป็น: $\alpha i_x = \alpha G_1 V_a$
   - ปมไฟฟ้าหลัก $a, b$ และปมอ้างอิงลงดิน $e$ ($V_e = 0\text{ V}$)
   - คำสั่งโจทย์: เขียนสมการชุดตัด (Cut-set Matrix Equation) ในรูปแบบเมทริกซ์เวกเตอร์ $[Q_K][Y_b][Q_K]^T \mathbf{V}_n = \mathbf{J}_{cut}$ และหาค่าแรงดันปม $V_a$ และ $V_b$

---

🎯 สิ่งที่ต้องสร้างและขยายความลึกใน CLAUDE_SOLUTION.md ( Seamless Scaffolding ):

1. บทที่ 1: มโนทัศน์กายภาพแหล่งกำเนิดกระแสพึ่งพาและทฤษฎีกราฟ (Dependent Current Source & Graph Theory Intuition):
   - ปูพื้นฐานจาก 0: ความแตกต่างระหว่างแหล่งกำเนิดอิสระ (Independent) กับแหล่งกำเนิดไม่อิสระ (Dependent/Controlled Source) ด้วยอุปมาอุปไมยท่อน้ำและวาล์วควบคุมอัตโนมัติ
   - อธิบายการสร้างกราฟวงจร (Oriented Graph), การเลือกต้นไม้ (Tree), กิ่งร่วม (Links) และการสร้างรอยตัดพื้นฐาน (Fundamental Cut-sets)

2. บทที่ 2: พิสูจน์ KCL และสมการชุดตัดทีละบรรทัด (Zero Mathematical Gaps):
   - ห้ามใช้คำว่า "ในทำนองเดียวกัน" หรือข้ามขั้นตอนย้ายข้างสมการเด็ดขาด!
   - พิสูจน์การตั้งสมการ KCL ที่ปม $a$:
     $I_0 + \alpha i_x - i_x - G_2 (V_a - V_b) = 0 \implies I_0 + \alpha G_1 V_a - G_1 V_a - G_2 (V_a - V_b) = 0$
     จัดรูป: $((1 - \alpha) G_1 + G_2) V_a - G_2 V_b = I_0$
   - พิสูจน์การตั้งสมการ KCL ที่ปม $b$:
     $-\alpha i_x + G_2 (V_a - V_b) - G_3 V_b = 0 \implies -\alpha G_1 V_a + G_2 (V_a - V_b) - G_3 V_b = 0$
     จัดรูป: $(G_2 - \alpha G_1) V_a - (G_2 + G_3) V_b = 0$
   - แก้ระบบสมการ 2x2 แบบบรรทัดต่อบรรทัด แสดงการหา Determinant $\Delta$ และ Cramer's Rule เพื่อหา $V_a$ และ $V_b$
   - แสดงการสร้างเมทริกซ์รอยตัดผูกกับความนำ $[Q_K][Y_b][Q_K]^T \mathbf{V}_n = \mathbf{J}_{cut}$ อย่างละเอียดทุกสมาชิก

3. บทที่ 3: วิธีคำนวณแทนค่าตัวเลขจริงอย่างละเอียด (Hand Derivation & Numerical Step):
   - กำหนดตัวอย่างตัวเลขทศนิยมจริงสำหรับ $G_1, G_2, G_3, \alpha, I_0$ และแสดงการแทนค่าบวก ลบ คูณ หาร ทศนิยม 6 ตำแหน่งทีละบรรทัด

4. บทที่ 4: การคำนวณด้วยคอมพิวเตอร์และการตรวจสอบไขว้ (Computer Matrix Solver & Verification):
   - เขียนสคริปต์ Python (`solve_circuit.py`) และ MATLAB (`solve_circuit.m`) ตั้งเมทริกซ์แก้สมการเชิงเส้น $\mathbf{A} \mathbf{x} = \mathbf{b}$
   - ตารางเปรียบเทียบผลลัพธ์ Hand Calculation vs Computer Matrix Solver

5. บทที่ 5: คัมภีร์ซ้อมตอบสอบปากเปล่าคะแนนเต็ม 100/100 (Master Oral Defense Guide 15 ข้อ):
   - เก็งคำถามสอบปากเปล่าเจาะลึก 15 ข้อ สำหรับโจทย์ข้อที่ 4 (เช่น หากค่า $\alpha$ เพิ่มขึ้นจนทำให้ Determinant เป็น 0 จะเกิดอะไรขึ้นกับวงจร, แหล่งกำเนิดกระแสไม่อิสระส่งผลต่อความสมมาตรของเมทริกซ์อย่างไร)
   - แบ่งโครงสร้างการตอบเป็น 2 ระดับในทุกข้อ:
     [1] บทตอบรอดชีวิต (Defensive Script): ตอบตรงประเด็น ไม่ตกกับดัก (ได้คะแนนผ่าน)
     [2] บทตอบเกียรตินิยม (Proactive Distinction Script): ตอบเชื่อมโยง Active Circuit, Stability Analysis, Feedback Control เพื่อให้กรรมการต้องแจก 100/100

---

💻 สิ่งที่ต้องสร้างใน interactive_dashboard.html ( Masterpiece Enhancement ):

1. Design & UI Standard (ตามมาตรฐาน Skill):
   - ติดตั้งปุ่มถอยหลังกลับหน้าหลักที่มุมบนซ้าย (`top: 14px; left: 14px;`) ลิงก์ `../../../index.html`
   - ติดตั้งปุ่มเปิดรูปภาพโจทย์ที่มุมซ้ายล่าง (`bottom: 24px; left: 24px;`) แสดงผลทุกแท็บ (สลับรูปภาพ `circuit_fig4.png` และ `image.png`)
   - ปุ่มเลื่อนแท็บ `◀` / `▶` สลับแท็บทันที ซ่อนเมื่อสุดขอบ

2. โครงสร้างแท็บเนื้อหา 6 แท็บ:
   - แท็บ 1: โจทย์จริง & วงจร (โจทย์ฉบับเต็ม + รูป circuit_fig4.png + Component Matrix)
   - แท็บ 2: ปูพื้นฐานแหล่งกำเนิดกระแสพึ่งพา & ทฤษฎีกราฟ
   - แท็บ 3: พิสูจน์ KCL & สมการปม $V_a, V_b$ ทีละบรรทัด
   - แท็บ 4: การสร้างสมการเมทริกซ์ชุดตัด (Cut-set Matrix Formulation)
   - แท็บ 5: คัมภีร์ซ้อมตอบสอบปากเปล่า 15 ข้อ (Oral Defense Masterclass)
   - แท็บ 6: CCCS & Conductance Laboratory (ปรับค่า $G_1, G_2, G_3, \alpha, I_0$ Real-time พร้อมกราฟผลตอบสนองแรงดัน $V_a, V_b$)

---

🔄 การเชื่อมโยงกับ Master Portal Hub และสารบัญ (Auto Sync):
1. อัปเดตไฟล์ index.html ที่ Root Directory ให้การ์ดโจทย์ข้อที่ 4 ปักป้าย `✅ พร้อมใช้งาน` พร้อมปุ่มกดทางเข้าหลักเพียงปุ่มเดียว:
   `<a href="problems/problem-4/solution3/interactive_dashboard.html" class="btn btn-primary">🚀 เข้าสู่เฉลย &amp; สื่อโต้ตอบ (ข้อที่ 4)</a>`
2. อัปเดตไฟล์ README.md ประจำข้อ 4 และ README.md ที่ Root Directory

จงดำเนินการสร้าง/ปรับปรุงไฟล์ทั้งหมดใน problems/problem-4/solution3/ (ทั้ง CLAUDE_SOLUTION.md, interactive_dashboard.html, README.md, solve_circuit.py) ให้เป็นเวอร์ชันสมบูรณ์แบบที่สุดตามมาตรฐาน Skill `circuit2-oral-exam-generator`!
```
