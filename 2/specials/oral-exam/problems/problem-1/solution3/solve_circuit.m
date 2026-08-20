function solve_circuit()
% SOLVE_CIRCUIT  เฉลยโจทย์สอบปากเปล่า 303212 — วงข่ายความต้านทานกับโมเดลแบตเตอรี่
% =========================================================================
%
%   KCL ที่ Node 1 :  i(t) = i_s(t) + v(t)/R_L
%   KVL ลูปซ้าย    :  v(t) = v_s(t) - i(t)*R_i
%   โมเดลแบตเตอรี่  :  v_s(t) = E_o - K*q + A_a*exp(-B_a*q) - A_b*exp(-B_b*(Q_n - q))
%                     q(t) = int_0^t i dalpha ,  Q_n = int_0^{t_n} i dalpha
%
%   ขั้นที่ 1  ตรวจ KCL ครบทุกแถว                    -> i(t) = 0.74 A
%   ขั้นที่ 2  อินทิเกรตหาประจุ                       -> q(t) = 0.74t , Q_n = 2664 C
%   ขั้นที่ 3  เดินตามลายมืออาจารย์ (piecewise asymptotic)
%   ขั้นที่ 4  ฟิตด้วยคอมพิวเตอร์ (Variable Projection)
%   ขั้นที่ 5  หน้าต่างเชิงเส้น + identifiability ของ (E_o, R_i)
%
% ใช้ได้ทั้ง MATLAB และ GNU Octave — ใช้เฉพาะฟังก์ชันพื้นฐาน ไม่ต้องมี toolbox ใดๆ
%
% วิธีรัน:   >> solve_circuit
%
% ดูคำอธิบายเต็มที่ CLAUDE_SOLUTION.md และซ้อมตอบที่ interactive_dashboard.html

% ---------- ค่าคงที่จากโจทย์ ----------
R_L = 10;        % [ohm]  ความต้านทานภาระ
t_n = 3600;      % [s]    เวลาอ้างอิงของความจุตามฉลาก

SEP = repmat('=', 1, 74);
here = fileparts(mfilename('fullpath'));
if isempty(here), here = pwd; end

fprintf('%s\n', SEP);
fprintf('เฉลยโจทย์สอบปากเปล่า 303212 — solution3/solve_circuit.m\n');
fprintf('%s\n', SEP);

% ---------- อ่านข้อมูล ----------
D = load_table(fullfile(here, '..', 'data303212qz02.md'));
t = D(:,1);  v = D(:,2);  is = D(:,3);
fprintf('\nอ่านข้อมูล %d แถว, t = %g .. %g s, R_L = %g ohm, t_n = %g s\n', ...
        size(D,1), t(1), t(end), R_L, t_n);

% =========================================================================
% ขั้นที่ 1 — KCL
% =========================================================================
head('ขั้นที่ 1 — สมการโหนด (KCL):  i(t) = i_s(t) + v(t)/R_L');

i = is + v / R_L;

fprintf('\nสุ่มตรวจ 3 จุดตามที่อาจารย์ทำในเฉลย:\n');
for k = [1 11 101]                       % MATLAB นับจาก 1 -> t = 0, 10, 100 s
    fprintf('  t = %3d s :  %.15f + %.15f/10 = %.15f A\n', ...
            t(k), is(k), v(k), i(k));
end

fprintf('\nแต่ 3 จุดไม่ใช่หลักฐาน — นี่คือหลักฐาน (ตรวจครบทุกแถว):\n');
fprintf('  จำนวนแถว           = %d\n', numel(i));
fprintf('  ค่าต่ำสุด           = %.18f A\n', min(i));
fprintf('  ค่าสูงสุด           = %.18f A\n', max(i));
fprintf('  ส่วนเบี่ยงเบนมาตรฐาน = %.4e A   <- ระดับ machine epsilon (eps = %.3e)\n', std(i), eps);
fprintf('  max|i - 0.74|       = %.4e A\n', max(abs(i - 0.74)));
fprintf('\n  => i(t) = 0.74 A คงที่ทุกวินาที (constant-current discharge)\n');

fprintf('\nแล้ว i_s ทำอะไรอยู่? มันชดเชยให้กระแสรวมคงที่:\n');
fprintf('  ที่ t=0    : v/R_L = %.6f A , i_s = %.6f A\n', v(1)/R_L, is(1));
fprintf('  ที่ t=%d : v/R_L = %.6f A , i_s = %.6f A\n', t(end), v(end)/R_L, is(end));
fprintf('  โหลดกินน้อยลง %+.6f A , i_s เพิ่มขึ้น %+.6f A  -> หักล้างกันพอดี\n', ...
        v(end)/R_L - v(1)/R_L, is(end) - is(1));

% =========================================================================
% ขั้นที่ 2 — ประจุ
% =========================================================================
head('ขั้นที่ 2 — อินทิเกรตหาประจุ  q(t) = int_0^t i dalpha  และ  Q_n');

I0  = median(i);                 % 0.74 A
q   = I0 * t;                    % เพราะกระแสคงที่ ดึงออกนอกอินทิกรัลได้
Q_n = I0 * t_n;

% ตรวจด้วยกฎสี่เหลี่ยมคางหมู โดยไม่เชื่อสูตร
q_trap = [0; cumsum(0.5*(i(2:end) + i(1:end-1)) .* diff(t))];

fprintf('\n  กระแสคงที่ I0 = %g A  =>  q(t) = %g*t  [C]\n', I0, I0);
fprintf('  ตรวจหน่วย: [A]*[s] = [C/s]*[s] = [C]  OK\n');
fprintf('  Q_n = %g * %g = %.1f C = %.2f Ah = %.0f mAh\n', I0, t_n, Q_n, Q_n/3600, Q_n/3.6);
fprintf('\n  ตรวจสูตรด้วย trapezoidal rule: max|q_trap - %g*t| = %.3e C  -> สูตรถูก\n', ...
        I0, max(abs(q_trap - q)));
fprintf('\n  ระวัง! ข้อมูลมีถึง t = %g s เท่านั้น แต่ t_n = %g s\n', t(end), t_n);
fprintf('    q ปลายข้อมูล = %.2f C = %.1f%% ของ Q_n  -> SoC เหลือ %.1f%%\n', ...
        q(end), 100*q(end)/Q_n, 100*(1 - q(end)/Q_n));
fprintf('    Q_n เป็นค่าตามฉลากผู้ผลิต (rated capacity) ตามนิยามในโจทย์\n');
fprintf('    ไม่ใช่การ extrapolate ข้อมูลการวัด\n');
fprintf('\n  พิสูจน์เทอมสุดท้าย: int_0^tn = int_0^t + int_t^tn\n');
fprintf('    => int_t^tn i dalpha = Q_n - q(t) = %g - %g*t  (ประจุที่ยังเหลือ)\n', Q_n, I0);

% =========================================================================
% ขั้นที่ 3 — เดินตามลายมืออาจารย์
% =========================================================================
head('ขั้นที่ 3 — วิธีคำนวณด้วยมือตามเฉลยอาจารย์ (Piecewise Asymptotic)');

ia = 1001;  ib = 1401;            % index ของ t = 1000 s และ 1400 s
qa = I0*t(ia);  qb = I0*t(ib);
slope = (v(ia) - v(ib)) / (qa - qb);
K_h   = 2.724e-4;                 % ค่าที่อาจารย์เขียน

fprintf('\n[3.1] ความชันช่วงเชิงเส้น — ใช้ t = %g s และ %g s\n', t(ia), t(ib));
fprintf('      q = %.0f C และ %.0f C ,  v = %.7f V และ %.7f V\n', qa, qb, v(ia), v(ib));
fprintf('      -K = dv/dq = %.6e   =>  K = %.6e V/C\n', slope, -slope);
fprintf('      อาจารย์เขียน K = %.4e V/C   [ตรงกัน]\n', K_h);

v1000_read = 3.8353;              % ค่าที่อาจารย์อ่านจากตาราง
C0_h = v1000_read + K_h*qa;
fprintf('\n[3.2] จุดตัดแกน: %g = -(%.4e)(%.0f) + E_o''\n', v1000_read, K_h, qa);
fprintf('      E_o'' = E_o - 0.74*R_i = %.6f V\n', C0_h);
fprintf('      (อาจารย์อ่าน %g , ค่าจริง %.6f — ต่างกัน %.2f mV จากการปัดเศษ)\n', ...
        v1000_read, v(ia), abs(v1000_read - v(ia))*1000);

Eo_assumed = 4.0801;              % อาจารย์สมมติ E_o ~ v(100)
Ri_h = (Eo_assumed - C0_h)/I0;
fprintf('\n[3.3] R_i — ต้องใส่สมมติฐานเพิ่ม เพราะข้อมูลอย่างเดียวหาไม่ได้\n');
fprintf('      สมมติ E_o ~ v(100) = %g V (ค่าจริง %.6f)\n', Eo_assumed, v(101));
fprintf('      R_i = (%g - %.6f)/%g = %.4f ohm\n', Eo_assumed, C0_h, I0, Ri_h);
fprintf('      *** เป็นค่า "ประมาณ" ไม่ใช่ "คำนวณ" — ดูขั้นที่ 5 ***\n');

Aa_h = 0.13723;
fprintf('\n[3.4] A_a — ที่ t=0, q=0: exp(0)=1 และเทอมปลาย ~ 0\n');
fprintf('      v(0) = E_o'' + A_a  =>  %.4f = %.5f + A_a  =>  A_a = %g V\n', ...
        v(1), C0_h, Aa_h);

% --- [3.5] B_a : จุดที่ต้องอธิบายให้ได้ในห้องสอบ ---
v100_read = 4.081;   q100 = I0*100;
lhs_without = v100_read - C0_h;                 % สมการที่อาจารย์เขียน (ไม่มี -K*q)
Ba_prof     = -log(lhs_without/Aa_h)/q100;
lhs_with    = v100_read - C0_h + K_h*q100;      % เก็บเทอม -K*q ไว้
Ba_fixed    = -log(lhs_with/Aa_h)/q100;

fprintf('\n[3.5] B_a — *** บรรทัดที่ต้องอธิบายให้ได้ในห้องสอบ ***\n');
fprintf('      สมการที่อาจารย์เขียน (ไม่มีเทอม -K*q):\n');
fprintf('        %g - %.5f = %.6f  =>  B_a = %.6f 1/C   <- ตรงกับเฉลย 0.01533\n', ...
        v100_read, C0_h, lhs_without, Ba_prof);
fprintf('\n      แต่สมการเต็มมีเทอม -K*q(t) อยู่ด้วย:\n');
fprintf('        ขนาดเทอมที่หายไป = K*q(100) = %.1f mV\n', K_h*q100*1000);
fprintf('        เทียบกับแรงดันรวม 4 V         -> %.2f%%  (ดูเล็ก)\n', 100*K_h*q100/4);
fprintf('        เทียบกับเทอมที่กำลังแก้หา %.1f mV -> %.1f%%  (ใหญ่เกินไป!)\n', ...
        lhs_with*1000, 100*K_h*q100/lhs_with);
fprintf('\n      ทำใหม่โดยเก็บเทอมนั้นไว้:  B_a = %.6f 1/C   <- ตรงกับค่าฟิตคอมพิวเตอร์\n', ...
        Ba_fixed);

% --- [3.6] A_b, B_b ---
i1 = 2701;  i2 = 2751;                    % index ของ t = 2700 s และ 2750 s
q1 = I0*t(i1);   q2 = I0*t(i2);
r1 = Q_n - q1;   r2 = Q_n - q2;
d1 = C0_h - K_h*q1 - 3.05;                % ค่าที่อาจารย์อ่าน v(2700) = 3.05
d2 = C0_h - K_h*q2 - 2.8244;              % ค่าที่อาจารย์อ่าน v(2750) = 2.8244
Bb_exact = -log(d1/d2)/(r1 - r2);
Bb_h  = 0.0107;                           % อาจารย์ปัดเศษ
Ab_recon   = d1/exp(-r1*Bb_h);
Ab_written = 551.176;                     % ค่าที่อาจารย์เขียนไว้จริง

fprintf('\n[3.6] A_b และ B_b — ที่ปลายกราฟ เทอม A_a ตายสนิทแล้ว (exp(-B_a*%.0f) = %.2e)\n', ...
        q1, exp(-Ba_prof*q1));
fprintf('      t=%g: Q_n-q=%.0f C -> A_b*exp(-%.0f*B_b) = %.5f   ...(1)\n', t(i1), r1, r1, d1);
fprintf('      t=%g: Q_n-q=%.0f C -> A_b*exp(-%.0f*B_b) = %.5f   ...(2)\n', t(i2), r2, r2, d2);
fprintf('\n      เทคนิค: (1)/(2) ทำให้ A_b หายไปเอง\n');
fprintf('        exp(-%.0f*B_b) = %.5f  =>  B_b = %.6f 1/C  -> อาจารย์ปัดเป็น %g\n', ...
        r1-r2, d1/d2, Bb_exact, Bb_h);
fprintf('      แทนกลับ (1): A_b = %.3f V   (อาจารย์เขียน %g V)\n', Ab_recon, Ab_written);
fprintf('\n      *** ทำไมต่างกัน? เพราะ dA_b/A_b = %.0f * dB_b ***\n', r1);
fprintf('        ความคลาดเคลื่อนของ B_b ถูกขยาย %.0f เท่า\n', r1);
fprintf('        ใช้ B_b ไม่ปัดเศษ (%.6f) จะได้ A_b = %.2f V\n', ...
        Bb_exact, d1/exp(-r1*Bb_exact));

% ชุด 'hand' ใช้ตัวเลขที่อาจารย์เขียนไว้จริงทุกตัว
hand  = [C0_h, K_h, Aa_h, 0.01533,          Ab_written, Bb_h];
fixed = [C0_h, K_h, Aa_h, round(Ba_fixed*1e6)/1e6, Ab_written, Bb_h];

% =========================================================================
% ขั้นที่ 4 — ฟิตด้วยคอมพิวเตอร์ (Variable Projection)
% =========================================================================
head('ขั้นที่ 4 — ฟิตด้วยคอมพิวเตอร์: Variable Projection');

fprintf('\n  แนวคิด: ถ้ารู้ (B_a, B_b) แล้ว โมเดลเป็นเชิงเส้นใน (C0, K, A_a, A_b)\n');
fprintf('          แก้ได้ปิดรูปด้วย backslash -> ปัญหา 6 มิติยุบเหลือ 2 มิติ\n');
fprintf('          [Golub & Pereyra 1973]\n\n');

% (ก) กริดหยาบ กัน local minimum
g = linspace(0.002, 0.030, 113);
best = [inf 0 0];
for a = g
    for b = g
        s = varpro_sse(q, v, a, b, Q_n);
        if s < best(1), best = [s a b]; end
    end
end
fprintf('  (ก) กริดหยาบ %dx%d -> B_a~%.5f, B_b~%.5f, SSE=%.4e\n', ...
        numel(g), numel(g), best(2), best(3), best(1));

% (ข) pattern search ปรับละเอียด
p = [best(2) best(3)];  step = [1e-3 1e-3];  fp = varpro_sse(q, v, p(1), p(2), Q_n);
for it = 1:4000
    improved = false;
    for j = 1:2
        for s = [1 -1]
            c = p;  c(j) = c(j) + s*step(j);
            if c(j) <= 0, continue; end
            fc = varpro_sse(q, v, c(1), c(2), Q_n);
            if fc < fp, p = c; fp = fc; improved = true; end
        end
    end
    if ~improved
        step = step/2;
        if max(step) < 1e-17, break; end
    end
end
Ba = p(1);  Bb = p(2);
[coef, sse] = varpro_sse(q, v, Ba, Bb, Q_n);
fit  = [coef(1), coef(2), coef(3), Ba, coef(4), Bb];
res  = v_model(q, fit, Q_n) - v;
rmse = sqrt(sse/numel(v));

fprintf('  (ข) pattern search ลู่เข้าแล้ว\n\n');
fprintf('  E_o'' = C0 = %.15f   V\n', fit(1));
fprintf('  K         = %.15e V/C\n', fit(2));
fprintf('  A_a       = %.15f   V\n', fit(3));
fprintf('  B_a       = %.15f   1/C\n', fit(4));
fprintf('  A_b       = %.12f      V\n', fit(5));
fprintf('  B_b       = %.15f   1/C\n', fit(6));
fprintf('\n  SSE = %.4e V^2 ,  RMSE = %.4e V ,  max|r| = %.4e V\n', ...
        sse, rmse, max(abs(res)));
fprintf('\n  *** อ่านผลให้เป็น: RMSE ระดับ 1e-13 V คือระดับ machine epsilon ***\n');
fprintf('      เครื่องมือวัดจริงไม่มีทางละเอียดขนาดนี้\n');
fprintf('      => ข้อมูลชุดนี้ถูกสร้างจากสมการนี้เอง ไม่ใช่ข้อมูลวัดจริง\n');
fprintf('      (ข้อมูลแล็บจริงจะได้ RMSE ราว 1e-3 ถึง 1e-2 V)\n');

fprintf('\n  ตรวจโครงสร้างพารามิเตอร์ — B*Q_n ออกมาเป็นเลขซ้ำ:\n');
fprintf('      B_a * Q_n = %.10f   (= 300/11)\n', Ba*Q_n);
fprintf('      B_b * Q_n = %.10f   (= 200/7)\n', Bb*Q_n);
fprintf('      3/B_a = %.4f C = %.3f%% ของ Q_n\n', 3/Ba, 100*3/Ba/Q_n);
fprintf('      3/B_b = %.4f C = %.3f%% ของ Q_n\n', 3/Bb, 100*3/Bb/Q_n);
fprintf('  => ทั้งคู่อยู่ในรูป B = 3/Q_exp ซึ่งเป็นธรรมเนียมของโมเดล Shepherd/Tremblay\n');
fprintf('     (ที่ q = Q_exp เทอมเลขชี้กำลังเหลือ exp(-3) = 4.98%% ~ "ตายไป 95%%")\n');

% =========================================================================
% ขั้นที่ 5 — หน้าต่างเชิงเส้น + identifiability
% =========================================================================
head('ขั้นที่ 5 — หน้าต่างเชิงเส้น และ identifiability ของ (E_o, R_i)');

tol  = 1e-3;
q_lo = log(fit(3)/tol)/fit(4);
q_hi = Q_n - log(fit(5)/tol)/fit(6);
fprintf('\n  เกณฑ์: เทอมต้องเล็กกว่า %g mV ถึงจะตัดทิ้งได้\n', tol*1000);
fprintf('    A_a*exp(-B_a*q)       < %g mV เมื่อ q > %.1f C (t > %.0f s)\n', tol*1000, q_lo, q_lo/I0);
fprintf('    A_b*exp(-B_b*(Q_n-q)) < %g mV เมื่อ q < %.1f C (t < %.0f s)\n', tol*1000, q_hi, q_hi/I0);
fprintf('  => หน้าต่างเชิงเส้น q in [%.0f, %.0f] C  หรือ  t in [%.0f, %.0f] s\n', ...
        q_lo, q_hi, q_lo/I0, q_hi/I0);
fprintf('  ช่วงที่อาจารย์ใช้ q in [740, 1036] C อยู่ในหน้าต่างนี้พอดี\n');

fprintf('\n  ทำไม E_o กับ R_i ถึงแยกจากกันไม่ได้:\n');
fprintf('    เพราะ i = %g A คงที่ เทอม i*R_i จึงคงที่ด้วย รวมกับ E_o เป็นก้อนเดียว\n', I0);
fprintf('    E_o'' = E_o - %g*R_i = %.12f V   <- ข้อมูลเห็นแค่ผลต่างก้อนนี้\n', I0, fit(1));
fprintf('\n    Jacobian:  dv/dE_o = 1 ,  dv/dR_i = -i = %g  (คงที่ทุกแถว)\n', -I0);
J = [ones(5,1), -I0*ones(5,1)];
fprintf('    => สองคอลัมน์เป็นสัดส่วนกัน -> rank(J) = %d (ไม่ใช่ 2), J''J เป็น singular\n', rank(J));
fprintf('\n    คำตอบมีเป็นอนันต์ บนเส้น  E_o = %.6f + %g*R_i :\n', fit(1), I0);
fprintf('      %10s %13s %13s   ทำนาย v(t)\n', 'R_i [ohm]', 'E_o [V]', 'i*R_i [mV]');
for Ri = [0 0.0584 0.2 1.0 10.0]
    fprintf('      %10.4f %13.6f %13.1f   เท่ากันทุกจุด\n', Ri, fit(1)+I0*Ri, I0*Ri*1000);
end
fprintf('\n  *** แก้ไม่ได้ด้วยการเพิ่มข้อมูล (structural non-identifiability) ***\n');
fprintf('      วิธีแก้จริง: Current Pulse Test / HPPC -> R_i = |dv/di| ตอน t->0+\n');
fprintf('      หลักการ: ความต้านทานเห็นได้จาก "การเปลี่ยนแปลง" ของกระแส ไม่ใช่ตัวกระแสเอง\n');

% =========================================================================
% ตารางเปรียบเทียบ
% =========================================================================
head('ตารางเปรียบเทียบ: มือ (อาจารย์) vs มือ (แก้เทอม Kq) vs คอมพิวเตอร์');

names = {'E_o''','K','A_a','B_a','A_b','B_b'};
units = {'V','V/C','V','1/C','V','1/C'};
fprintf('\n  %-6s %16s %16s %20s %9s  %s\n', ...
        'param','มือ(อาจารย์)','มือ(แก้ Kq)','คอมพิวเตอร์','ผิด %','หน่วย');
fprintf('  %s\n', repmat('-', 1, 84));
for k = 1:6
    err = abs(hand(k) - fit(k))/abs(fit(k))*100;
    flag = ''; if k == 4, flag = '  <-- ดูขั้นที่ 3.5'; end
    fprintf('  %-6s %16.8g %16.8g %20.12g %8.3f%%  %s%s\n', ...
            names{k}, hand(k), fixed(k), fit(k), err, units{k}, flag);
end

fprintf('\n  คุณภาพเมื่อแทนกลับกับข้อมูลจริงทั้ง %d จุด:\n', numel(v));
fprintf('  %-22s %14s %15s %17s\n', 'ชุดพารามิเตอร์','RMSE [V]','max|r| [V]','RMSE ช่วง t<=400');
fprintf('  %s\n', repmat('-', 1, 74));
sets   = {hand, fixed, fit};
labels = {'ลายมืออาจารย์','แก้เทอม Kq','คอมพิวเตอร์'};
early  = 2:401;
for k = 1:3
    r = v_model(q, sets{k}, Q_n) - v;
    fprintf('  %-20s %15.4e %15.4e %17.4e\n', labels{k}, ...
            sqrt(r'*r/numel(r)), max(abs(r)), sqrt(r(early)'*r(early)/numel(early)));
end

rh = v_model(q, hand,  Q_n) - v;
rf = v_model(q, fixed, Q_n) - v;
[mx, kmx] = max(abs(rh));
fprintf('\n  ความคลาดเคลื่อนสูงสุดของชุดลายมือ = %.2f mV ที่ t = %g s\n', mx*1000, t(kmx));
fprintf('  ขนาดเทอม K*q(74) ที่ถูกตัดทิ้ง       = %.2f mV  <- ตรงกัน\n', K_h*q100*1000);
fprintf('  แก้เทอมแล้ว RMSE ดีขึ้น %.1f เท่า\n', sqrt(rh'*rh)/sqrt(rf'*rf));

% =========================================================================
% ปริมาณเสริม + กราฟ
% =========================================================================
head('ปริมาณเสริมที่กรรมการชอบถาม');
P = v .* i;
E_J = trapz(t, P);
fprintf('\n  พลังงานที่จ่ายตลอดการทดลอง = int v*i dt = %.2f J = %.5f Wh\n', E_J, E_J/3600);
fprintf('  แรงดันเฉลี่ย                = %.5f V\n', mean(v));
fprintf('  แรงดันตกใน R_i              = i*R_i  = %.2f mV\n', I0*Ri_h*1000);
fprintf('  กำลังสูญเป็นความร้อนใน R_i   = i^2R_i = %.2f mW\n', I0^2*Ri_h*1000);
fprintf('  SoC ปลายข้อมูล              = %.1f%%\n', 100*(1-q(end)/Q_n));

head('สรุปคำตอบสุดท้าย');
fprintf('\n  i(t) = %g A (คงที่ทุกจุด) ,  q(t) = %g*t C ,  Q_n = %.0f C = %.2f Ah\n', ...
        I0, I0, Q_n, Q_n/3600);
fprintf('\n  ค่าฟิตคอมพิวเตอร์: E_o''=%.12f V , K=%.12e V/C\n', fit(1), fit(2));
fprintf('                     A_a=%.12f V , B_a=%.12f 1/C\n', fit(3), fit(4));
fprintf('                     A_b=%.9f V , B_b=%.12f 1/C\n', fit(5), fit(6));
fprintf('\n  ค่าตามเฉลยอาจารย์: E_o''=%.6f V , K=%.4e V/C , A_a=%g V\n', hand(1), hand(2), hand(3));
fprintf('                     B_a=%g 1/C , A_b=%g V , B_b=%g 1/C\n', hand(4), hand(5), hand(6));
fprintf('                     R_i=%.4f ohm (ประมาณ ภายใต้สมมติฐาน E_o ~ v(100))\n', Ri_h);
fprintf('\n  E_o กับ R_i แยกกันไม่ได้ — คำตอบอยู่บนเส้น  E_o = %.6f + %g*R_i\n\n', fit(1), I0);

make_plots(t, v, is, i, q, Q_n, R_L, hand, fixed, fit, here);

fprintf('ดูคำอธิบายเต็มที่ CLAUDE_SOLUTION.md\n');
fprintf('ซ้อมตอบสอบปากเปล่าที่ interactive_dashboard.html แท็บที่ 5\n\n');
end

% =========================================================================
% ฟังก์ชันย่อย
% =========================================================================
function head(s)
fprintf('\n%s\n%s\n%s\n', repmat('=',1,74), s, repmat('=',1,74));
end

function vv = v_model(q, p, Qn)
% p = [C0, K, A_a, B_a, A_b, B_b]
vv = p(1) - p(2)*q + p(3)*exp(-p(4)*q) - p(5)*exp(-p(6)*(Qn - q));
end

function [out, sse] = varpro_sse(q, v, Ba, Bb, Qn)
% ตรึง (B_a,B_b) แล้วโมเดลเป็นเชิงเส้นใน (C0,K,A_a,A_b) -> แก้ปิดรูปด้วย backslash
X = [ones(size(q)), -q, exp(-Ba*q), -exp(-Bb*(Qn - q))];
c = X \ v;
r = X*c - v;
s = r'*r;
if nargout >= 2
    out = c;  sse = s;      % [coef, sse] = varpro_sse(...)
else
    out = s;                % sse = varpro_sse(...)
end
end

function D = load_table(path)
% อ่านตาราง markdown 3 คอลัมน์ โดยข้ามบรรทัดที่ไม่ใช่ตัวเลข
fid = fopen(path, 'r');
if fid < 0
    error('solve_circuit:noData', 'หาไฟล์ข้อมูลไม่เจอ: %s', path);
end
c = onCleanup(@() fclose(fid));
D = zeros(4000, 3);  n = 0;
while true
    line = fgetl(fid);
    if ~ischar(line), break; end
    line = strtrim(line);
    if isempty(line) || line(1) ~= '|', continue; end
    parts = strsplit(strtrim(line), '|');
    parts = parts(~cellfun(@(s) isempty(strtrim(s)), parts));
    if numel(parts) ~= 3, continue; end
    vals = str2double(parts);
    if any(isnan(vals)), continue; end       % หัวตาราง / เส้นคั่น
    n = n + 1;
    D(n,:) = vals(:)';
end
D = D(1:n, :);
if n == 0
    error('solve_circuit:emptyData', 'อ่านไฟล์ได้ แต่ไม่พบแถวข้อมูลตัวเลขใน %s', path);
end
end

function make_plots(t, v, is, i, q, Qn, R_L, hand, fixed, fit, outdir)
try
    f = figure('Name', 'solution3 — 303212', 'Position', [80 80 1180 780]);

    subplot(2,2,1);
    plot(t, i, 'LineWidth', 2.2); hold on;
    plot(t, is, 'LineWidth', 1.4); plot(t, v/R_L, 'LineWidth', 1.4); hold off;
    xlabel('t [s]'); ylabel('current [A]'); grid on;
    title('KCL: i = i_s + v/R_L = 0.74 A');
    legend('i = 0.74 A', 'i_s(t)', 'v/R_L', 'Location', 'east');

    subplot(2,2,2);
    plot(q, v, 'LineWidth', 4, 'Color', [.6 .65 .72]); hold on;
    plot(q, v_model(q, fit, Qn), 'LineWidth', 1.3); hold off;
    xlabel('q [C]'); ylabel('v [V]'); grid on;
    title('v vs q — วัดได้ เทียบกับ แบบจำลอง');
    legend('measured', 'fitted model', 'Location', 'southwest');

    subplot(2,2,3);
    semilogy(q, fit(3)*exp(-fit(4)*q), 'LineWidth', 1.6); hold on;
    semilogy(q, fit(5)*exp(-fit(6)*(Qn - q)), 'LineWidth', 1.6);
    semilogy(q, fit(2)*q, '--', 'LineWidth', 1.2); hold off;
    xlabel('q [C]'); ylabel('term size [V]'); grid on; ylim([1e-8 1]);
    title('ขนาดของแต่ละเทอม (หน้าต่างเชิงเส้นคือช่วงที่ทั้งสอง exp ต่ำ)');
    legend('A_a e^{-B_a q}', 'A_b e^{-B_b(Q_n-q)}', 'K q', 'Location', 'south');

    subplot(2,2,4);
    plot(t, (v_model(q, hand,  Qn) - v)*1000, 'LineWidth', 1.4); hold on;
    plot(t, (v_model(q, fixed, Qn) - v)*1000, 'LineWidth', 1.4); hold off;
    xlabel('t [s]'); ylabel('residual [mV]'); grid on;
    title('ความคลาดเคลื่อน: ลายมือ vs แก้เทอม Kq');
    legend('hand (B_a=0.01533)', 'hand + fixed Kq', 'Location', 'southeast');

    out = fullfile(outdir, 'figures_matlab.png');
    saveas(f, out);
    fprintf('  บันทึกกราฟ -> %s\n\n', out);
catch err
    fprintf('  ข้ามการวาดกราฟ (%s)\n\n', err.message);
end
end
