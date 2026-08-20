# โจทย์สอบปากเปล่า 303212 — ข้อที่ 4

> **หัวข้อ:** วงข่ายความนำไฟฟ้าและแหล่งกำเนิดกระแสไม่อิสระ (Conductance Network with Dependent Current Source $\alpha i_x$)

---

## 📌 เอกสารและสื่อการสอนประจำข้อที่ 4

1. **[PROMPT_FOR_CLAUDE_OPUS.md](PROMPT_FOR_CLAUDE_OPUS.md):** Master Prompt สำหรับส่งสั่งการ Claude Opus / Claude 3.7 Sonnet เพื่อประมวลผลเฉลยละเอียดและแดชบอร์ดตามมาตรฐาน **Skill `circuit2-oral-exam-generator`**
2. **[oral_exam_problem.md](oral_exam_problem.md):** ถอดข้อความโจทย์ต้นฉบับ รูปภาพวงจร และตารางสรุปตัวแปร (Component Matrix)
3. **[image.png](image.png) & [circuit_fig4.png](circuit_fig4.png):** รูปภาพโจทย์และวงจรไฟฟ้าต้นฉบับ

---

## ⚡ สภาพวงจรและเป้าหมายการคำนวณ

- **องค์ประกอบในวงจร:** ความนำไฟฟ้า $G_1, G_2, G_3 [\mho]$, แหล่งกำเนิดกระแสอิสระ $I_0 [\text{A}]$, แหล่งกำเนิดกระแสพึ่งพา (CCCS) $\alpha i_x [\text{A}]$
- **กระแสควบคุม:** $i_x = G_1 V_a$ (กระแสไหลผ่าน $G_1$ จากปม $a$ ลงกราวด์ $e$)
- **เป้าหมาย:** เขียนสมการชุดตัดในรูปแบบเมทริกซ์เวกเตอร์ $[Q_K][Y_b][Q_K]^T \mathbf{V}_n = \mathbf{J}_{cut}$ และหาค่าแรงดันปม $V_a$ และ $V_b$ เทียบกับกราวด์ $e$ ($V_e = 0\text{ V}$)

---

## 🚀 ชุดเฉลยและสื่อการสอนฉบับสมบูรณ์

เข้าสู่ [Interactive Dashboard — ข้อที่ 4](solution3/interactive_dashboard.html) เพื่อเรียนแบบ 6 แท็บ ตั้งแต่ภาพท่อน้ำและ CCCS ไปจนถึง Cut-Set Matrix, คัมภีร์ซ้อมตอบปากเปล่า 15 ข้อ และห้องทดลองปรับพารามิเตอร์แบบ real-time

เอกสารประกอบอยู่ใน [solution3/README.md](solution3/README.md) และ [solution3/CLAUDE_SOLUTION.md](solution3/CLAUDE_SOLUTION.md) พร้อมสคริปต์ตรวจไขว้ด้วย [Python](solution3/solve_circuit.py) และ [MATLAB/Octave](solution3/solve_circuit.m)

**ประโยคแกนกลางของข้อนี้:**
\[
 i_x=G_1V_a,\qquad
 \Delta=G_1G_2+G_2G_3+(1-\alpha)G_1G_3,
\]
\[
 V_a=\frac{I_0(G_2+G_3)}{\Delta},\qquad
 V_b=\frac{I_0(G_2-\alpha G_1)}{\Delta}.
\]
