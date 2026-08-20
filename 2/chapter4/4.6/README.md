# โจทย์ [4.6] — การวิเคราะห์วงรอบหลักมูลของวงจรข่าย RLC ในโดเมนความถี่ (AC Steady-State)

ชุดข้อมูล ภาพประกอบ และบทวิเคราะห์สำหรับแก้โจทย์ข้อ [4.6] ของบทที่ 4 (การวิเคราะห์วงรอบ / Loop–Tie-set Analysis) 
ซึ่งเป็นวงจรข่าย RLC ในสถานะอยู่ตัวไซน์ (Sinusoidal Steady State) ที่มีทั้ง **แหล่งจ่ายแรงดัน \(V_0\cos(\omega t)\)** และ **แหล่งจ่ายกระแส \(I_0\sin(\omega t)\)**

---

## 📁 โครงสร้างไฟล์ในโฟลเดอร์นี้

| ไฟล์ | รายละเอียด |
|---|---|
| [problem.png](problem.png) | ภาพโจทย์ต้นฉบับความละเอียดสูง (300 DPI) จากเอกสารบรรยายหน้า 105 |
| [problem.md](problem.md) | คำโจทย์ฉบับเต็ม ถอดความภาษาไทย สิ่งที่กำหนดให้ สิ่งที่ต้องหา และข้อตกลงเชิงสัญกรณ์ |
| [figure-analysis.md](figure-analysis.md) | บทวิเคราะห์โครงสร้างวงจร ปม กิ่งประกอบ การแปลงเฟสเซอร์ และการสร้างเมทริกซ์ \(\mathbf{B}\) |
| [index.html](index.html) | หน้าเว็บ Interactive สรุปโจทย์และสมการ พร้อมระบบสลับ Dark/Light Mode |
| [figures/](figures/) | ภาพแยกส่วน: ข้อความโจทย์ต้นฉบับ และ รูป 4บ.6 วงจรข่ายในสถานะอยู่ตัว |

---

## 🎯 สรุปสาระสำคัญของโจทย์

- **โทโปโลยี**: กราฟมี 3 ปม (\(n=3\)), 4 กิ่ง (\(b=4\)) \(\implies\) จำนวนวงรอบหลักมูล \(l = 4 - 3 + 1 = 2\)
- **การเลือกทรี**: ทรี \(T = \{3, 4\}\) (กิ่ง \(C\) และ \(L\)), ลิงก์ \(L = \{1, 2\}\) (กิ่ง \(R_1+V_s\) และ \(R_2\parallel I_s\))
- **Fundamental Tie-set Matrix (\(\mathbf{B}\))**:
  \[
  \mathbf{B} = \begin{bmatrix} 1 & 0 & 0 & -1 \\ 0 & 1 & -1 & -1 \end{bmatrix}
  \]
- **ระบบสมการวงรอบในรูปเมทริกซ์-เวกเตอร์**:
  \[
  \begin{bmatrix}
  R_1 + j\omega L & j\omega L \\
  j\omega L & R_2 + \dfrac{1}{j\omega C} + j\omega L
  \end{bmatrix}
  \begin{bmatrix} J_1 \\ J_2 \end{bmatrix}
  =
  \begin{bmatrix} -V_0 \\ j R_2 I_0 \end{bmatrix}
  \]
- **กระแสกิ่งในโดเมนความถี่**:
  \[
  \mathbf{I}_1 = J_1,\quad \mathbf{I}_2 = J_2,\quad \mathbf{I}_3 = -J_2,\quad \mathbf{I}_4 = -J_1 - J_2
  \]
- **กระแสกิ่งในโดเมนเวลา**: \(i_k(t) = |\mathbf{I}_k|\cos(\omega t + \phi_k)\) สำหรับ \(k=1,2,3,4\)

---

## 🤖 แนะนำสำหรับการแก้โจทย์ใน Session ถัดไป

สามารถใช้คำสั่ง prompt ให้ AI Agent ดำเนินการแก้โจทย์อย่างละเอียด (Solution 1 และ Solution 2 Visual Matrix) โดยอ้างอิงเอกสาร:
- `@2/chapter4/4.6/problem.md`
- `@2/chapter4/4.6/figures/`
- `@2/chapter4/4.6/figure-analysis.md`
- `@2/chapter4/lecture/303212S1Y2569lec04_5048.pdf` (หน้า 96–100 ตัวอย่าง 4.3)
