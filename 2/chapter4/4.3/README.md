# โจทย์ [4.3] — สมการรอบ แรงดันกิ่ง และกระแสกิ่ง

วงจรข่ายความต้านทานที่มีแหล่งกำเนิดแรงดันอิสระอนุกรม $R_1$ บนกิ่งที่ 2 และแหล่งกำเนิดกระแส
อิสระขนานกับ $(R_2+R_3)$ บนกิ่งที่ 1 โจทย์กำหนดทรีของกราฟและกระแสวงรอบ $j_1$ มาให้
แล้วให้เขียนสมการรอบพร้อมคำนวณแรงดันกิ่งและกระแสกิ่ง

## คำตอบย่อ

ให้ $R_T=R_1+R_2+R_3$

| ปริมาณ | คำตอบ |
|---|---|
| สมการรอบ | $(R_1+R_2+R_3)\,j_1=(R_2+R_3)i_s-v_s$ |
| กระแสวงรอบ | $j_1=\dfrac{(R_2+R_3)i_s-v_s}{R_T}$ |
| กระแสกิ่ง | $i_1=+j_1$ , $i_2=-j_1$ |
| แรงดันกิ่ง | $v_1=v_2=-\dfrac{(R_2+R_3)(v_s+R_1i_s)}{R_T}$ |
| แรงดันปม $a$ | $v(a)=+\dfrac{(R_2+R_3)(v_s+R_1i_s)}{R_T}$ |

## เอกสารในโฟลเดอร์นี้

| ไฟล์ | เนื้อหา |
|---|---|
| [problem.md](problem.md) | โจทย์ที่ถอดความจากภาพ สิ่งที่กำหนดให้ สิ่งที่ต้องหา และข้อตกลงสัญกรณ์ |
| [figure-analysis.md](figure-analysis.md) | วิเคราะห์รูป 4บ.3(ก) และ 4บ.3(ข) แยกทีละรูปอย่างละเอียด |
| [solution.md](solution.md) | **เฉลยละเอียด 12 หัวข้อ** ตั้งแต่ยุบกราฟ เมทริกซ์ tie-set สมการเฉพาะกิ่ง จนถึงการตรวจคำตอบ 4 ทาง |
| [index.html](index.html) | หน้าเว็บรวมทุกอย่างไว้ในหน้าเดียว เปิดอ่านได้เลย |
| [problem.png](problem.png) | ภาพโจทย์ต้นฉบับ |
| `figures/` | รูปที่สกัดจากภาพโจทย์ต้นฉบับ |
| `assets/` | สื่อประกอบที่สร้างใหม่ 8 รูป พร้อมสคริปต์ `make_figures.py` |

## สื่อประกอบที่สร้างขึ้น

| รูป | ไฟล์ | ใช้อธิบายเรื่อง |
|---|---|---|
| 1 | [fig-01-figure-a-anatomy.svg](assets/fig-01-figure-a-anatomy.svg) | อ่านรูป (ก): องค์ประกอบ ปม และดีกรีของปม |
| 2 | [fig-02-composite-branches.svg](assets/fig-02-composite-branches.svg) | ยุบปมดีกรี 2 แล้วจัดกลุ่มเป็นกิ่งประกอบ 2 กิ่ง |
| 3 | [fig-03-figure-b-anatomy.svg](assets/fig-03-figure-b-anatomy.svg) | อ่านรูป (ข): ทวิก ลิงก์ ทิศ $j_1$ และการนับทางโทโปโลยี |
| 4 | [fig-04-branch-models.svg](assets/fig-04-branch-models.svg) | สมการเฉพาะกิ่งของรูปทีวินินและรูปนอร์ตัน |
| 5 | [fig-05-tieset-matrix.svg](assets/fig-05-tieset-matrix.svg) | เมทริกซ์ $\mathbf{B}$, $\mathbf{i}_b=\mathbf{B}^{\mathsf T}\mathbf{j}$ และ $\mathbf{B}\mathbf{v}_b=0$ |
| 6 | [fig-06-kvl-walk-and-solve.svg](assets/fig-06-kvl-walk-and-solve.svg) | เดินรอบวงรอบเก็บเครื่องหมาย แล้วแก้หา $j_1$ |
| 7 | [fig-07-results.svg](assets/fig-07-results.svg) | ทิศทางจริงของกระแสและคำตอบเชิงสัญลักษณ์ |
| 8 | [fig-08-numeric-check.svg](assets/fig-08-numeric-check.svg) | ตัวอย่างตัวเลข การตรวจด้วยวิธีปม และสมดุลกำลัง |

สร้างรูปใหม่ทั้งหมดได้ด้วย

```bash
python3 assets/make_figures.py
```

## องค์ความรู้ที่ใช้

- กราฟของวงจร ปม กิ่ง ดีกรี — [lectures/01-foundations-of-graphs.md](../../lectures/01-foundations-of-graphs.md)
- ทวิก ลิงก์ และการเลือกทรี — [lectures/03-circuit-topology-branches-twigs-links.md](../../lectures/03-circuit-topology-branches-twigs-links.md)
- คู่ตรงข้ามของวิธีนี้คือชุดตัดอิสระ — [lectures/04-cutsets-and-fundamental-cutsets.md](../../lectures/04-cutsets-and-fundamental-cutsets.md)
- เมทริกซ์และความเป็นอิสระเชิงเส้น — [lectures/06-advanced-problem-solving.md](../../lectures/06-advanced-problem-solving.md)
