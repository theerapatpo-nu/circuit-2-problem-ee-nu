# เตรียมสอบปากเปล่า 303212 — การวิเคราะห์วงจรไฟฟ้า 2

**Oral Exam Learning Portal** · คลังโจทย์ เฉลย และสื่อการสอนแบบโต้ตอบ ทั้ง 5 ข้อ

> 🚀 **ทางเข้าหลัก:** เปิด **[index.html](index.html)** ด้วยเบราว์เซอร์ แล้วเลือกข้อที่ต้องการ

---

## สถานะความคืบหน้า

| ข้อ | หัวข้อ | สถานะ | ทางเข้า |
| :---: | :--- | :---: | :--- |
| **1** | วงข่ายความต้านทาน &amp; แบบจำลองแบตเตอรี่ | ✅ พร้อมใช้งาน | [เข้าสู่เฉลย &amp; สื่อโต้ตอบ](problems/problem-1/solution3/interactive_dashboard.html) |
| 2 | — | 📌 รอดำเนินการ | — |
| **3** | วงข่ายความนำไฟฟ้า &amp; สมการชุดตัด | ✅ พร้อมใช้งาน | [เข้าสู่เฉลย &amp; สื่อโต้ตอบ](problems/problem-3/solution3/interactive_dashboard.html) |
| **4** | วงข่ายความนำไฟฟ้า &amp; แหล่งกำเนิดกระแสไม่อิสระ (CCCS) | ✅ พร้อมใช้งาน | [เข้าสู่เฉลย &amp; สื่อโต้ตอบ](problems/problem-4/solution3/interactive_dashboard.html) |
| **5** | วงข่ายความนำไฟฟ้า &amp; Directed Graph | ✅ พร้อมใช้งาน | [เข้าสู่เฉลย &amp; สื่อโต้ตอบ](problems/problem-5/solution3/interactive_dashboard.html) |

---

## ข้อที่ 1 — วงข่ายความต้านทานและแบบจำลองแบตเตอรี่

**เนื้อหา:** KCL/KVL · การอินทิเกรตประจุ · การระบุพารามิเตอร์แบตเตอรี่ 8 ตัวจากข้อมูลจริง 2,753 จุด · วิธีแยกช่วงแบบลายมืออาจารย์ ($y = mx + c$) · Structural Non-identifiability

**คำตอบหลัก:** $i(t) = 0.74$ A คงที่ · $q(t) = 0.74t$ C · $Q_n = 2{,}664$ C $= 0.74$ Ah

📁 [โฟลเดอร์ข้อที่ 1](problems/problem-1/) · 📘 [เอกสารเฉลย](problems/problem-1/solution3/CLAUDE_SOLUTION.md) · 🖥️ [สื่อโต้ตอบ](problems/problem-1/solution3/interactive_dashboard.html)

**จุดเด่นของชุดเฉลย:** ตามลายมืออาจารย์ทุกบรรทัดจนพบว่าค่า $B_a$ ที่ต่างจากค่าฟิตคอมพิวเตอร์ 50% เกิดจากการตัดเทอม $-Kq$ ในช่วงที่มันยังไม่เล็กพอ — ใส่กลับแล้ว RMSE ดีขึ้น 21 เท่า

---

## ข้อที่ 3 — วงข่ายความนำไฟฟ้าและสมการชุดตัด

**เนื้อหา:** ความนำไฟฟ้า $G$ [℧] · ทฤษฎีกราฟวงจร (ต้นไม้ / กิ่งร่วม / รอยตัดพื้นฐาน) · เมทริกซ์ชุดตัด $[Q_K][Y_b][Q_K]^T$ · Supernode · ทฤษฎีบทเทลเลเจน

**คำตอบหลัก:**

$$V_a = E_1 \qquad V_b = \frac{G_1E_1 - G_2E_2 - G_2E_3}{G_1+G_2+G_3} \qquad V_c = V_b + E_3 \qquad V_d = -E_2$$

📁 [โฟลเดอร์ข้อที่ 3](problems/problem-3/) · 📘 [เอกสารเฉลย](problems/problem-3/solution3/CLAUDE_SOLUTION.md) · 🖥️ [สื่อโต้ตอบ](problems/problem-3/solution3/interactive_dashboard.html)

**จุดเด่นของชุดเฉลย:** พิสูจน์ว่า **รอยตัดพื้นฐานของกิ่ง $G_3$ คือสมการ supernode เป๊ะ** และอธิบายพร้อมหลักฐานเชิงตัวเลขว่าทำไม **$G_4$ ถึงไม่ปรากฏในคำตอบแรงดันเลยสักตัว**

---

## โครงสร้างโปรเจกต์

```text
oral-exam/
├── index.html                              <-- Master Portal รวมโจทย์ทุกข้อ
├── README.md                               <-- ไฟล์นี้
├── .nojekyll                               <-- ป้องกัน GitHub Pages 404
├── .agents/skills/
│   └── circuit2-oral-exam-generator/
│       └── SKILL.md                        <-- มาตรฐานการสร้างเนื้อหาทุกข้อ
└── problems/
    ├── problem-1/ … problem-5/
    │   ├── oral_exam_problem.md            <-- ถอดข้อความโจทย์ + Component Matrix
    │   ├── image.png / circuit_figN.png    <-- รูปโจทย์และแผนภาพวงจร
    │   ├── reference/                      <-- ลายมือเฉลยอาจารย์ (ถ้ามี)
    │   └── solution3/                      <-- ชุดเฉลยและสื่อการสอนฉบับสมบูรณ์
    │       ├── CLAUDE_SOLUTION.md          <-- บทเรียนและเฉลย 5 บท
    │       ├── interactive_dashboard.html  <-- สื่อโต้ตอบ 6 แท็บ
    │       ├── solve_circuit.py / .m       <-- สคริปต์คำนวณ
    │       └── README.md                   <-- สารบัญประจำข้อ
```

---

## มาตรฐานเนื้อหาทุกข้อ

ทุกชุดเฉลยสร้างตาม Skill [`circuit2-oral-exam-generator`](.agents/skills/circuit2-oral-exam-generator/SKILL.md) ซึ่งกำหนดไว้ว่า:

1. **Zero-to-Hero Scaffolding** — ปูพื้นฐานจาก 0 ด้วยมโนทัศน์กายภาพ (ท่อน้ำ ถังน้ำ เกาะกับสะพาน) ก่อนแตะสมการ
2. **Zero Mathematical Gaps** — พิสูจน์ทุกบรรทัด แสดงการย้ายข้างและแทนค่าทศนิยม ไม่มีคำว่า "ในทำนองเดียวกัน"
3. **Master Oral Defense** — เก็งคำถาม 10–15 ข้อ พร้อมบทพูดซ้อมจริง ชี้กับดัก และแบ่งคำตอบ 2 ระดับ (รอดชีวิต / เกียรตินิยม)
4. **Interactive Dashboard** — 6 แท็บ Dark Mode + Glassmorphism · ปุ่มกลับหน้าหลักมุมบนซ้าย · ปุ่มเปิดรูปโจทย์มุมซ้ายล่าง · ปุ่มเลื่อนแท็บที่ซ่อนอัตโนมัติเมื่อสุดขอบ
5. **Portal Auto Sync** — อัปเดตการ์ดใน `index.html` และ `README.md` ทุกครั้งที่เพิ่มข้อใหม่

---

## วิธีใช้งาน

**อ่านออนไลน์:** เปิด [index.html](index.html) ด้วยเบราว์เซอร์ ไม่ต้องติดตั้งอะไรเลย

**รันโค้ดตรวจตัวเลขเอง:**

```bash
python3 problems/problem-3/solution3/solve_circuit.py
```

ต้องการแค่ **NumPy** เท่านั้น (สคริปต์ทุกข้อเขียนให้ไม่ต้องพึ่ง SciPy)
