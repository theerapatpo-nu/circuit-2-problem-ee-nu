# โจทย์สอบปากเปล่า 303212 — ข้อที่ 5

> **หัวข้อ:** วงข่ายความนำไฟฟ้าและกราฟมีทิศทางกำกับ (Conductance Network with Directed Graph)

---

## 📌 เอกสารและสื่อการสอนประจำข้อที่ 5

✅ **พร้อมใช้งาน:** [เข้าสู่เฉลย & สื่อโต้ตอบ](solution3/interactive_dashboard.html)

1. **[PROMPT_FOR_CLAUDE_OPUS.md](PROMPT_FOR_CLAUDE_OPUS.md):** Master Prompt สำหรับส่งสั่งการ Claude Opus / Claude 3.7 Sonnet เพื่อประมวลผลเฉลยละเอียดและแดชบอร์ดตามมาตรฐาน **Skill `circuit2-oral-exam-generator`**
2. **[oral_exam_problem.md](oral_exam_problem.md):** ถอดข้อความโจทย์ต้นฉบับ รูปภาพวงจร กราฟมีทิศทาง และตารางสรุปตัวแปร (Component & Graph Edge Matrix)
3. **[image.png](image.png) & [circuit_fig5.png](circuit_fig5.png):** รูปภาพโจทย์ วงจรไฟฟ้า และกราฟมีทิศทางกำกับต้นฉบับ

---

## ⚡ สภาพวงจรและเป้าหมายการคำนวณ

- **องค์ประกอบในวงจร:** ความนำไฟฟ้า $G_1, G_2, G_3, G_4 [\mho]$, แหล่งกำเนิดแรงดันอิสระ $E_1, E_2, E_3 [\text{V}]$
- **กราฟมีทิศทาง (Directed Graph):** กิ่งที่ 1 ($e \to a$), กิ่งที่ 2 ($a \to b$), กิ่งที่ 3 ($a \to e$), กิ่งที่ 4 ($e \to b$)
- **เป้าหมาย:** เขียนสมการชุดตัดในรูปแบบเมทริกซ์เวกเตอร์ $[Q_K][Y_b][Q_K]^T \mathbf{V}_n = \mathbf{J}_{cut}$ และหาค่าแรงดันปม $V_a$ และ $V_b$ เทียบกับกราวด์ $e$ ($V_e = 0\text{ V}$)
