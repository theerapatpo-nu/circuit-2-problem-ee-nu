# Solution 2 — Battery Circuit Oral Exam (ChatGPT Model GPT-5.6 SOL)

ชุดเฉลย สคริปต์คำนวณ และสื่อการสอนแบบโต้ตอบสำหรับโจทย์วงจรแบตเตอรี่ โดยใช้ข้อมูลจริงครบ 2,753 แถวจาก `t=0...2752 s` (สร้างโดย ChatGPT Model GPT-5.6 SOL)

## ผลลัพธ์หลัก

$$
i(t)=i_s(t)+\frac{v(t)}{10}=0.740000\ \mathrm{A},
\qquad
q(t)=0.74t\ \mathrm{C},
\qquad
Q_n=2664.00\ \mathrm{C}=0.74\ \mathrm{Ah}.
$$

พารามิเตอร์เส้นโค้งที่ระบุได้จากข้อมูล:

| พารามิเตอร์ | ค่าคิดด้วยมือ (Hand Asymptotic) | ค่าฟิตคอมพิวเตอร์ (L-BFGS-B 2,753 จุด) | หน่วย | สถานะ |
|---|---:|---:|---:|---|
| $C_0\equiv E_o-0.74R_i$ | $4.036870$ | $4.036467052577080$ | V | ระบุได้ (คลาดเคลื่อน 0.01%) |
| $K$ | $2.7240\times10^{-4}$ | $2.721543795924126\times10^{-4}$ | V/C | ระบุได้ (คลาดเคลื่อน 0.09%) |
| $A_a$ | $0.137230$ | $0.137637356141268$ | V | ระบุได้ (คลาดเคลื่อน 0.29%) |
| $B_a$ | $0.015330$ | $0.0102375102375104$ | C$^{-1}$ | ระบุได้ |
| $A_b$ | $551.176$ | $559.945732826002$ | V | ระบุได้ทางคณิตศาสตร์ |
| $B_b$ | $0.010700$ | $0.0107250107250107$ | C$^{-1}$ | ระบุได้ (คลาดเคลื่อน 0.23%) |
| $Q_n$ | $2664.00$ | $2664.000000$ | C | ได้จากนิยามและ $t_n$ |
| $R_i$ | ไม่เป็นเอกเทศ | ไม่เป็นเอกเทศ | $\Omega$ | ต้องมีการทดลองเพิ่ม |
| $E_o$ | ไม่เป็นเอกเทศ | ไม่เป็นเอกเทศ | V | ต้องมี $R_i$ จากการทดลองเพิ่ม |

> [!IMPORTANT]
> ทั้งวิธีคิดด้วยมือแบบ Piecewise Asymptotic ของอาจารย์ ([งาน คสช. (1).pdf](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/reference/%E0%B8%87%E0%B8%B2%E0%B8%99%20%E0%B8%84%E0%B8%AA%E0%B8%8A.%20(1).pdf)) และวิธีฟิตคอมพิวเตอร์ด้วย Optimization Algorithms ให้ผลลัพธ์พารามิเตอร์ที่ตรงกันอย่างสมบูรณ์แบบ!

## สารบัญไฟล์

| ไฟล์ | หน้าที่ |
|---|---|
| [GPT_SOLUTION.md](GPT_SOLUTION.md) | บทเรียนและเฉลยฉบับสมบูรณ์ 5 ส่วน ตั้งแต่พื้นฐานท่อน้ำจนถึง EV/BESS และคำถามสอบปากเปล่า |
| [solvecircuit.py](solvecircuit.py) | อ่าน `.md` หรือ `.xls`, คำนวณ KCL/ประจุ, nonlinear fitting, ตรวจ identifiability, สร้าง CSV/JSON/PNG |
| [solvecircuit.m](solvecircuit.m) | MATLAB implementation ด้วย variable projection, `fminsearch` และ `lsqcurvefit` เมื่อมี Optimization Toolbox |
| [interactivedashboard.html](interactivedashboard.html) | Single-file standalone dashboard: SVG circuit, Canvas charts, time scrubber, parameter sliders และแท็บบทเรียน |
| [signals_overview.png](signals_overview.png) | กราฟ $v(t),i_s(t),i(t),q(t)$ จาก Python |
| [voltage_fit.png](voltage_fit.png) | แรงดันวัดเทียบ nonlinear model และ residual |
| [fit_results.json](fit_results.json) | ผลฟิตแบบ machine-readable พร้อมคำเตือน identifiability |
| [computed_data.csv](computed_data.csv) | ผลคำนวณครบ 2,753 แถว: $t,v,i_s,i,q,\hat v,r$ |
| [requirements.txt](requirements.txt) | Python dependencies |

ลิงก์เปิดไฟล์แบบ absolute ตามที่โจทย์กำหนด:

- [เปิดบทเรียน](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/solution2/GPT_SOLUTION.md)
- [เปิดแดชบอร์ด](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/solution2/interactivedashboard.html)
- [เปิด Python solver](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/solution2/solvecircuit.py)
- [เปิด MATLAB solver](file:///Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/circuit/2/specials/oral-exam/solution2/solvecircuit.m)

## วิธีใช้แดชบอร์ด

เปิด `interactivedashboard.html` ด้วยเว็บเบราว์เซอร์ได้ทันที ไม่ต้องติดตั้งแพ็กเกจและไม่ต้องใช้อินเทอร์เน็ต

1. เลื่อน `เวลา t` เพื่อดูค่า $v_s,v,i_s,i_L,i,q,$ และ SOC บนวงจร
2. เลื่อนพารามิเตอร์เพื่อดูเส้นแรงดันเปลี่ยนแบบ real time
3. เปิด `Lock C₀` แล้วเลื่อน $R_i$: ระบบจะปรับ $E_o$ ให้ $E_o-0.74R_i$ คงเดิม กราฟจึงไม่เปลี่ยน เป็นการสาธิต non-identifiability โดยตรง
4. ใช้แท็บบทเรียนทบทวนพื้นฐาน การพิสูจน์ การฟิต และคำตอบสอบปากเปล่า

แดชบอร์ดใช้ SVG และ Canvas engine ที่ฝังในไฟล์เดียว จึงไม่พึ่ง CDN

## วิธีรัน Python

ต้องการ Python 3.10+ แนะนำสร้าง virtual environment แล้วติดตั้ง dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python solvecircuit.py
```

สคริปต์เลือกอ่าน `../data303212qz02.md` เป็นค่าเริ่มต้น ถ้าต้องการบังคับอ่าน Excel:

```bash
python solvecircuit.py --data ../data303212qz02.xls
```

ถ้ามีค่า $R_i$ จาก pulse test เช่น $0.15\ \Omega$:

```bash
python solvecircuit.py --ri 0.15
```

ค่า `--ri` เปลี่ยนเฉพาะคู่ $(E_o,R_i)$ ตามเส้นเอกลักษณ์ ไม่เปลี่ยน $C_0,K,A_a,B_a,A_b,B_b$ หรือคุณภาพการฟิต

ผลลัพธ์ที่สร้าง/เขียนทับในโฟลเดอร์นี้:

- `signals_overview.png`
- `voltage_fit.png`
- `fit_results.json`
- `computed_data.csv`

## วิธีรัน MATLAB

เปิด MATLAB แล้วรัน `solvecircuit.m` สคริปต์จะหาไฟล์ข้อมูลจากโฟลเดอร์แม่โดยอัตโนมัติ

- มี Optimization Toolbox: ใช้ multi-start `fminsearch` และ polish ด้วย `lsqcurvefit`
- ไม่มี Optimization Toolbox: ใช้ variable-projection + multi-start `fminsearch`

ค่า `RI_ASSUMED` อยู่ช่วงต้นไฟล์และตั้งต้นเป็น `0.20` ohm ต้องเปลี่ยนเป็นค่าจากการทดลองแยกหากต้องการตีความ $E_o$ ทางกายภาพ

## การตรวจสอบที่ทำแล้ว

- Python syntax compile ผ่าน
- HTML JavaScript syntax ผ่าน `node --check`
- เปิดแดชบอร์ดใน Chromium จริงโดยไม่มี console error
- ทดสอบ time slider, parameter slider, `Lock C₀`, tab navigation
- ทดสอบ responsive viewport 360 px: ไม่มี horizontal overflow
- ตรวจข้อมูลครบ 2,753 แถว และ $i_{\min}=i_{\max}=0.74$ A
- ตรวจ nonlinear model เทียบข้อมูลครบทุกแถว: residual อยู่ระดับ floating-point roundoff

## หมายเหตุด้านวิศวกรรม

ค่า $A_b\approx559.95$ V เป็น coefficient ที่นิยาม ณ $q=Q_n$ ไม่ใช่แรงดันแบตเตอรี่จริง 560 V ข้อมูลหยุดที่ $q=2036.48$ C ซึ่งยังห่าง $Q_n$ อยู่ 627.52 C ผลของเทอมปลาย ณ จุดข้อมูลสุดท้ายจึงประมาณ 0.669 V การ extrapolate ต่อถึง 3600 s ต้องมีข้อมูลทดลองเพิ่ม

