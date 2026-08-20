# บทที่ 4 — การวิเคราะห์วงรอบ (Loop / Tie-set Analysis)

โฟลเดอร์นี้รวมเอกสารคำสอน แบบฝึกหัด ภาพประกอบ และการวิเคราะห์วงรอบสำหรับรายวิชา Circuit Analysis 2

## เอกสารบรรยาย (Lecture)

- [Lecture 04 — เอกสารคำสอนบทที่ 4 การวิเคราะห์วงรอบ (303212S1Y2569lec04_5048.pdf)](lecture/README.md)
  - [เอกสารฉบับ Markdown สมบูรณ์ (Zero-Drift Page Tracking & 300 DPI Figures)](lecture/303212s1y2569lec04_5048_complete.md)

## แบบฝึกหัดและโจทย์ท้ายบท

| ข้อ | หัวข้อ | อ้างอิงหน้าในสไลด์ | โฟลเดอร์ |
|---|---|:---:|---|
| [4.3] | สมการรอบ แรงดันกิ่ง และกระแสกิ่งของวงจรข่ายความต้านทาน | หน้า 17 (รูป 4บ.3) | [4.3](4.3) |
| [4.4] | สมการรอบหลักมูล แรงดันกิ่ง และกระแสกิ่งของวงจรข่ายความต้านทาน (Dipole & Norton) | หน้า 17 (รูป 4บ.4) | [4.4](4.4) |
| [4.5] | **เฉลย Gold Standard:** Tie-set Matrix, CCCS \(\alpha i_x\), ระบบขยาย \(2\times2\), ตรวจ KVL/KCL/Limits/Tellegen | หน้า 18 (รูป 4บ.5) | [Reader](4.5/index.html) · [Solution](4.5/solution.md) |
| [4.6] | **เฉลย Gold Standard:** AC phasor, RLC Tie-set Matrix \(2\times2\), กระแสเวลา, Nodal/KVL/KCL/Limits/Complex Power | หน้า 18 (รูป 4บ.6) | [Dashboard](4.6/index.html) · [Solution](4.6/solution.md) |

## เฉลยแนะนำล่าสุด

โจทย์ [4.5](4.5/index.html) แสดงการคูณ \(\mathbf B\mathbf Z_b\mathbf B^{\mathsf T}\) และ \(\mathbf B\mathbf Z_b\mathbf i_{sb}\) ทีละขั้น จัดการตัวแปรควบคุม \(i_x\) ด้วยระบบเมทริกซ์ขยาย และมีภาพ SVG/เครื่องคำนวณสำหรับตรวจคำตอบบนทุกขนาดหน้าจอ

โจทย์ [4.6](4.6/index.html) ขยายวิธีเดียวกันสู่สถานะอยู่ตัวไซน์ โดยแสดงการแปลง peak phasor, การคูณ complex matrix, สูตร \(A_k\cos(\omega t+\phi_k)\) และ complex-power balance พร้อม Interactive Phasor Lab
