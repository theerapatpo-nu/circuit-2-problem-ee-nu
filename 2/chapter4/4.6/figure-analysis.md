# การวิเคราะห์ภาพและโทโปโลยีเชิงลึก โจทย์ [4.6] (Figure & Topological Analysis)

เอกสารนี้ทำหน้าที่ถอดรหัสโครงสร้างวงจร กราฟ ทรี และการแปลงโดเมนความถี่ของโจทย์ข้อ [4.6] อย่างเป็นระบบ ก่อนนำไปเขียนสมการเมทริกซ์

---

## 1. การวิเคราะห์โครงสร้างวงจรจริง (รูปที่ 4บ.6)

![วงจรข่ายในสถานะอยู่ตัว](./figures/fig-4b6-steady-state-circuit.png)

### 1.1 ปมไฟฟ้าหลัก (Principal Electrical Nodes)
วงจรประกอบด้วย **3 ปมหลัก**:
1. **ปม \(A\) (ปมซ้ายบน / Node 1):**
   - เชื่อมต่อกับขั้วบวกของแหล่งจ่ายกระแส \(I_0\sin(\omega t)\)
   - เชื่อมต่อกับปลายบนของตัวต้านทาน \(R_2\)
   - เชื่อมต่อกับขั้วซ้ายของตัวเก็บประจุ \(C\)
2. **ปม \(B\) (ปมขวาบน / Node 2):**
   - เชื่อมต่อกับขั้วขวาของตัวเก็บประจุ \(C\)
   - เชื่อมต่อกับปลายบนของตัวเหนี่ยวนำ \(L\)
   - เชื่อมต่อกับขั้วซ้ายของตัวต้านทาน \(R_1\)
3. **ปม \(O\) (ปมล่างร่วม / Reference Datum / Node 0):**
   - ราวด้านล่างต่อเนื่องที่เชื่อมขั้วลบของแหล่งจ่ายกระแส \(I_0\), ปลายล่างของ \(R_2\), ปลายล่างของ \(L\), และขั้วลบของแหล่งจ่ายแรงดัน \(V_0\cos(\omega t)\)
   - กำหนดให้เป็นจุดอ้างอิงศักย์ไฟฟ้า \(V_O = 0\text{ V}\)

---

## 2. การแปลงสู่โดเมนความถี่ (Frequency-Domain / Phasor Transform)

ใช้การแปลงเฟสเซอร์อ้างอิงฟังก์ชันโคไซน์ (Cosine Reference Standard):
\[
A\cos(\omega t + \theta) \longleftrightarrow \mathbf{A} = A\angle\theta = A e^{j\theta}
\]

### 2.1 แหล่งกำเนิดไฟฟ้า
1. **แหล่งจ่ายแรงดัน:**
   \[
   v_s(t) = V_0\cos(\omega t) \longleftrightarrow \mathbf{V}_s = V_0\angle 0^\circ = V_0 + j0
   \]
2. **แหล่งจ่ายกระแส:**
   \[
   i_s(t) = I_0\sin(\omega t) = I_0\cos(\omega t - 90^\circ) \longleftrightarrow \mathbf{I}_s = I_0\angle -90^\circ = -jI_0
   \]

### 2.2 อิมพีแดนซ์เชิงซ้อนขององค์ประกอบพาสซีฟ (\(\mathbf{Z} = R + jX\))
- ตัวต้านทาน: \(\mathbf{Z}_{R1} = R_1,\quad \mathbf{Z}_{R2} = R_2\)
- ตัวเก็บประจุ: \(\mathbf{Z}_C = \dfrac{1}{j\omega C} = -j\dfrac{1}{\omega C}\)
- ตัวเหนี่ยวนำ: \(\mathbf{Z}_L = j\omega L\)

---

## 3. การจัดกิ่งประกอบ (Composite Branch Modeling)

เพื่อให้วงจรมีจำนวนกิ่งพอดีกับกราฟ (\(b = 4\)) และเข้ากับแม่แบบสมการกิ่งมาตรฐานของบทที่ 4:
\[
\mathbf{v}_b = \mathbf{Z}_b\mathbf{i}_b + \mathbf{v}_{sb} - \mathbf{Z}_b\mathbf{i}_{sb}
\]

| กิ่ง (\(k\)) | ปลายกิ่ง (ทิศทาง) | องค์ประกอบภายในกิ่ง | โมเดลมาตรฐาน | \(\mathbf{Z}_{bk}\) | แหล่งจ่ายแรงดัน \(\mathbf{V}_{sb,k}\) | แหล่งจ่ายกระแส \(\mathbf{I}_{sb,k}\) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | \(B \to O\) (\(\downarrow\)) | \(R_1\) อนุกรม \(\mathbf{V}_s\) | Thévenin | \(R_1\) | \(+V_0\) | \(0\) |
| **2** | \(A \to O\) (\(\downarrow\)) | \(R_2\) ขนาน \(\mathbf{I}_s\) | Norton | \(R_2\) | \(0\) | \(+jI_0\) |
| **3** | \(A \to B\) (\(\rightarrow\)) | ตัวเก็บประจุ \(C\) | Passive | \(\dfrac{1}{j\omega C}\) | \(0\) | \(0\) |
| **4** | \(B \to O\) (\(\downarrow\)) | ตัวเหนี่ยวนำ \(L\) | Passive | \(j\omega L\) | \(0\) | \(0\) |

> **หมายเหตุเรื่องเครื่องหมายแหล่งจ่ายในกิ่ง:**
> - ในกิ่งที่ 1: กระแส \(i_1\) ไหลจาก \(B \to O\) ผ่าน \(R_1\) เข้าสู่ขั้ว \(+\) ของ \(\mathbf{V}_s\) ดังนั้น \(\mathbf{V}_{sb,1} = +V_0\)
> - ในกิ่งที่ 2: ทิศกิ่ง \(i_2\) ไหลลง (\(A \to O\)) แต่แหล่งจ่ายกระแส \(\mathbf{I}_s\) ไหลขึ้น (\(O \to A\)) สวนทางกับกิ่ง ดังนั้นกระแสแหล่งจ่ายในทิศกิ่งคือ \(-\mathbf{I}_s = -(-jI_0) = +jI_0\)

---

## 4. การเลือกทรี (Tree Selection) และการสร้างเมทริกซ์วงรอบหลักมูล \(\mathbf{B}\)

กราฟมีจำนวนปม \(n = 3\) และจำนวนกิ่ง \(b = 4\):
- จำนวนกิ่งของทรี (Twigs): \(n - 1 = 2\) กิ่ง
- จำนวนลิงก์ (Links / Co-tree): \(l = b - n + 1 = 4 - 3 + 1 = 2\) กิ่ง

### การเลือกทรีแบบมาตรฐาน (Canonical Tree Selection)
เลือกทรี \(T = \{\text{กิ่ง 3}, \text{กิ่ง 4}\}\) (ตัวเก็บประจุ \(C\) และตัวเหนี่ยวนำ \(L\))
ทำให้เซตของลิงก์คือ \(L = \{\text{กิ่ง 1}, \text{กิ่ง 2}\}\)

#### การเดินวงรอบหลักมูลทั้งสอง (Fundamental Loops):
1. **วงรอบหลักมูลที่ 1 (กำหนดโดยลิงก์ 1):**
   - เส้นทางเดิน: ลิงก์ 1 (\(B \to O\)) \(\to\) กิ่งทรี 4 ย้อนทิศ (\(O \to B\))
   - แถวที่ 1 ของ \(\mathbf{B}\): \([+1,\ 0,\ 0,\ -1]\)
2. **วงรอบหลักมูลที่ 2 (กำหนดโดยลิงก์ 2):**
   - เส้นทางเดิน: ลิงก์ 2 (\(A \to O\)) \(\to\) กิ่งทรี 4 ย้อนทิศ (\(O \to B\)) \(\to\) กิ่งทรี 3 ย้อนทิศ (\(B \to A\))
   - แถวที่ 2 ของ \(\mathbf{B}\): \([0,\ +1,\ -1,\ -1]\)

ดังนั้น **เมทริกซ์วงรอบหลักมูล (Fundamental Tie-set Matrix \(\mathbf{B}\))** คือ:
\[
\mathbf{B} = \begin{bmatrix} 1 & 0 & 0 & -1 \\ 0 & 1 & -1 & -1 \end{bmatrix}
\]

---

## 5. การประกอบสมการเมทริกซ์วงรอบ (\(\mathbf{Z}_l \mathbf{J} = \mathbf{E}_s\))

### 5.1 เมทริกซ์อิมพีแดนซ์กิ่ง (\(\mathbf{Z}_b\))
\[
\mathbf{Z}_b = \begin{bmatrix}
R_1 & 0 & 0 & 0 \\
0 & R_2 & 0 & 0 \\
0 & 0 & \dfrac{1}{j\omega C} & 0 \\
0 & 0 & 0 & j\omega L
\end{bmatrix}
\]

### 5.2 เมทริกซ์อิมพีแดนซ์วงรอบ (\(\mathbf{Z}_l = \mathbf{B}\mathbf{Z}_b\mathbf{B}^{\mathsf T}\))
\[
\mathbf{Z}_l = \begin{bmatrix}
R_1 + j\omega L & j\omega L \\
j\omega L & R_2 + \dfrac{1}{j\omega C} + j\omega L
\end{bmatrix}
\]

### 5.3 เวกเตอร์แหล่งจ่ายวงรอบ (\(\mathbf{E}_s = \mathbf{B}\mathbf{Z}_b\mathbf{I}_{sb} - \mathbf{B}\mathbf{V}_{sb}\))
\[
\mathbf{E}_s = \begin{bmatrix} -V_0 \\ R_2(jI_0) \end{bmatrix} = \begin{bmatrix} -V_0 \\ j R_2 I_0 \end{bmatrix}
\]

### 5.4 สมการวงรอบรวม
\[
\begin{bmatrix}
R_1 + j\omega L & j\omega L \\
j\omega L & R_2 + \dfrac{1}{j\omega C} + j\omega L
\end{bmatrix}
\begin{bmatrix} J_1 \\ J_2 \end{bmatrix}
=
\begin{bmatrix} -V_0 \\ j R_2 I_0 \end{bmatrix}
\]

---

## 6. ความสัมพันธ์ระหว่างกระแสวงรอบกับกระแสกิ่งในวงจรจริง

จาก \(\mathbf{I}_b = \mathbf{B}^{\mathsf T}\mathbf{J}\):
\[
\begin{bmatrix} \mathbf{I}_1 \\ \mathbf{I}_2 \\ \mathbf{I}_3 \\ \mathbf{I}_4 \end{bmatrix}
=
\begin{bmatrix}
1 & 0 \\
0 & 1 \\
0 & -1 \\
-1 & -1
\end{bmatrix}
\begin{bmatrix} J_1 \\ J_2 \end{bmatrix}
\implies
\begin{cases}
\mathbf{I}_1 = J_1 \\
\mathbf{I}_2 = J_2 \\
\mathbf{I}_3 = -J_2 \\
\mathbf{I}_4 = -J_1 - J_2
\end{cases}
\]

เมื่อแก้หาเฟสเซอร์ \(\mathbf{I}_k = |\mathbf{I}_k|\angle\phi_k\) ได้แล้ว แปลงกลับสู่โดเมนเวลา:
\[
i_k(t) = \operatorname{Re}\{\mathbf{I}_k e^{j\omega t}\} = |\mathbf{I}_k|\cos(\omega t + \phi_k)
\]
