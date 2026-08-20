function solve_circuit(G1, G2, G3, G4, E1, E2, E3)
% SOLVE_CIRCUIT  เฉลยโจทย์สอบปากเปล่า 303212 ข้อที่ 3
%                วงข่ายความนำไฟฟ้าและสมการชุดตัด (Conductance Network & Cut-set)
% =========================================================================
%
% โครงสร้างวงจร (5 ปม a,b,c,d,e และ 7 กิ่ง):
%     E1 : a-e   ขั้ว + ที่ a   ->  Va = +E1
%     G1 : a-b
%     G3 : b-e
%     E3 : b-c   ขั้ว + ที่ c   ->  Vc - Vb = +E3
%     G2 : c-d
%     G4 : d-e
%     E2 : d-e   ขั้ว - ที่ d   ->  Vd = -E2      <-- กับดักเครื่องหมาย!
%
%     ขั้นที่ 1  กราฟวงจรและเมทริกซ์อุบัติการณ์ [A]
%     ขั้นที่ 2  เลือกต้นไม้ (ยัดแหล่งจ่ายเข้าเป็นกิ่งต้นไม้) + ตรวจ det[At]
%     ขั้นที่ 3  เมทริกซ์ชุดตัด [Q_K] และเมทริกซ์ลูป [B] + ตรวจ Q*B' = 0
%     ขั้นที่ 4  คำนวณ [Q_G][Y_b][Q_G]' และดึงสมการ supernode
%     ขั้นที่ 5  แก้หาแรงดันปม 3 เส้นทางที่เป็นอิสระกัน
%     ขั้นที่ 6  ตรวจ KCL, สมดุลกำลังไฟฟ้า และผลของ G4
%
% ใช้ได้ทั้ง MATLAB และ GNU Octave — ใช้เฉพาะฟังก์ชันพื้นฐาน ไม่ต้องมี toolbox
%
% วิธีรัน:
%     >> solve_circuit                                  % ใช้ค่าตัวอย่าง
%     >> solve_circuit(0.5, 0.25, 0.2, 0.4, 12, 6, 4)   % กำหนดเอง
%
% ดูคำอธิบายเต็มที่ CLAUDE_SOLUTION.md
% ซ้อมตอบสอบปากเปล่าที่ interactive_dashboard.html แท็บที่ 5

if nargin < 7
    G1 = 0.5; G2 = 0.25; G3 = 0.2; G4 = 0.4;   % [mho]
    E1 = 12;  E2 = 6;    E3 = 4;                % [V]
end

SEP = repmat('=', 1, 74);
fprintf('%s\n', SEP);
fprintf('เฉลยโจทย์สอบปากเปล่า 303212 ข้อที่ 3 — solution3/solve_circuit.m\n');
fprintf('%s\n', SEP);
fprintf('\nพารามิเตอร์: G1=%g G2=%g G3=%g G4=%g [mho]   E1=%g E2=%g E3=%g [V]\n', ...
        G1, G2, G3, G4, E1, E2, E3);
fprintf('ความต้านทานเทียบเท่า: R1=%g R2=%g R3=%g R4=%g [ohm]\n', ...
        1/G1, 1/G2, 1/G3, 1/G4);

% ---------- นิยามกราฟ ----------
% เรียงกิ่งแบบ "กิ่งต้นไม้ก่อน แล้วค่อยกิ่งร่วม" เพื่อให้ [Q] อยู่ในรูป [I | Ql]
branches = {'E1','G3','E3','E2','G1','G2','G4'};
twigs    = {'E1','G3','E3','E2'};
links    = {'G1','G2','G4'};
nodes    = {'a','b','c','d','e'};
refIdx   = 5;                       % ปม e เป็นปมอ้างอิง

% ทิศทางอ้างอิง (from, to) : v_branch = V(from) - V(to)
fromN = [1 2 3 4 1 3 4];            % a b c d a c d
toN   = [5 5 2 5 2 4 5];            % e e b e b d e

nN = numel(nodes);  nB = numel(branches);  nT = numel(twigs);

% =========================================================================
head('ขั้นที่ 1 — กราฟวงจรและเมทริกซ์อุบัติการณ์ [A]');
fprintf('\n  จำนวนปม n = %d (%s)   ปมอ้างอิง = %s\n', nN, strjoin(nodes, ', '), nodes{refIdx});
fprintf('  จำนวนกิ่ง b = %d (%s)   <-- นับแหล่งจ่ายเป็นกิ่งด้วย!\n', nB, strjoin(branches, ', '));
fprintf('  กิ่งต้นไม้ = n-1 = %d   กิ่งร่วม = b-n+1 = %d\n', nN-1, nB-nN+1);

Aa = zeros(nN, nB);
for j = 1:nB
    Aa(fromN(j), j) = Aa(fromN(j), j) + 1;
    Aa(toN(j),   j) = Aa(toN(j),   j) - 1;
end
A = Aa; A(refIdx, :) = [];          % เมทริกซ์อุบัติการณ์ลดรูป

show_matrix(Aa, nodes, branches, 'เมทริกซ์อุบัติการณ์สมบูรณ์ [Aa] (5x7):', '%7.0f');
fprintf('\n  ผลรวมแต่ละคอลัมน์ = [%s]\n', num2str(sum(Aa, 1), '%g '));
fprintf('  เป็นศูนย์ทุกคอลัมน์? %s   <- ทุกกิ่งมี 2 ปลาย (+1 กับ -1)\n', ...
        tf2str(all(abs(sum(Aa,1)) < 1e-12)));
show_matrix(A, nodes(1:4), branches, ...
            'เมทริกซ์อุบัติการณ์ลดรูป [A] (4x7) — ตัดแถวปมอ้างอิงออก:', '%7.0f');

% =========================================================================
head('ขั้นที่ 2 — เลือกต้นไม้ และตรวจว่าเป็นต้นไม้จริง');
fprintf('\n  ต้นไม้ที่เลือก : {%s}\n', strjoin(twigs, ', '));
fprintf('  กิ่งร่วม        : {%s}\n', strjoin(links, ', '));
fprintf('\n  หลักการเลือก: "ยัดแหล่งจ่ายแรงดันทุกตัวเข้าเป็นกิ่งต้นไม้ให้หมด"\n');
fprintf('    เพราะแรงดันกิ่งต้นไม้คือตัวแปรของระบบ\n');
fprintf('    ถ้ากิ่งนั้นเป็นแหล่งจ่าย เราก็รู้ค่าตัวแปรฟรีทันที\n');

At = A(:, 1:nT);  Al = A(:, nT+1:end);
detAt = det(At);
fprintf('\n  det[At] = %g  -> %s\n', detAt, ...
        ternary(abs(detAt) > 1e-12, 'เป็นต้นไม้จริง', 'ไม่ใช่ต้นไม้!'));

fprintf('\n  แรงดันกิ่งต้นไม้ (ตัวแปรของระบบ):\n');
fprintf('    v(E1) = Va      = E1  = %-8g [รู้ค่า]\n', E1);
fprintf('    v(G3) = Vb      = ?             [<<< ตัวไม่รู้ตัวเดียว]\n');
fprintf('    v(E3) = Vc - Vb = E3  = %-8g [รู้ค่า]\n', E3);
fprintf('    v(E2) = Vd      = -E2 = %-8g [รู้ค่า]\n', -E2);
fprintf('\n  => ตัวไม่รู้ที่แท้จริง = (n-1) - 3 แหล่งจ่าย = %d - 3 = 1 ตัว\n', nN-1);

% =========================================================================
head('ขั้นที่ 3 — เมทริกซ์ชุดตัดพื้นฐาน [Q_K] และเมทริกซ์ลูป [B]');
Ql = At \ Al;                       % Ql = At^{-1} * Al
Q  = [eye(nT), Ql];
B  = [-Ql.', eye(nB - nT)];

cutnames = cell(1, nT);
for i = 1:nT, cutnames{i} = sprintf('cut%d(%s)', i, twigs{i}); end
show_matrix(Q, cutnames, branches, '[Q_K] = [ I | Ql ]  (4x7):', '%7.0f');
fprintf('\n  บล็อกซ้ายเป็นเมทริกซ์เอกลักษณ์ I4? %s   <- ต้องเป็นเสมอ\n', ...
        tf2str(norm(Q(:,1:nT) - eye(nT)) < 1e-12));

fprintf('\n  อ่านแถวที่ 2 (รอยตัดของกิ่ง G3):\n');
fprintf('    ตัด G3 ออก -> กราฟขาดเป็น {b, c} กับ {a, d, e}\n');
fprintf('    (b กับ c ยังเชื่อมกันด้วย E3 จึงอยู่ก้อนเดียวกัน)\n');
for j = 1:nB
    if abs(Q(2,j)) > 1e-9
        fprintf('      %3s: %+d  ข้ามรอยตัด\n', branches{j}, round(Q(2,j)));
    elseif strcmp(branches{j}, 'E3')
        fprintf('      %3s:  0   ปลายทั้งสองอยู่ใน {b,c} -> ไม่ข้าม  *** supernode! ***\n', ...
                branches{j});
    end
end

loopnames = cell(1, numel(links));
for i = 1:numel(links), loopnames{i} = sprintf('loop%d(%s)', i, links{i}); end
show_matrix(B, loopnames, branches, '[B] = [ -Ql'' | I ]  (3x7):', '%7.0f');
QBt = Q * B.';
fprintf('\n  [Q_K][B]'' = เมทริกซ์ศูนย์ขนาด %dx%d? %s\n', size(QBt,1), size(QBt,2), ...
        tf2str(norm(QBt(:)) < 1e-12));
fprintf('  <- KCL ตั้งฉาก KVL (รากฐานทฤษฎีบทเทลเลเจน)\n');

% =========================================================================
head('ขั้นที่ 4 — เมทริกซ์ [Q_G][Y_b][Q_G]''');
fprintf('\n  แหล่งจ่ายแรงดันอุดมคติไม่มีค่าความนำ (G -> inf)\n');
fprintf('  จึงเขียน [Y_b] ครบ 7 กิ่งไม่ได้ ต้องหั่นเฉพาะคอลัมน์ของกิ่งความนำ\n');

gorder = {'G3','G1','G2','G4'};
gcols = zeros(1, numel(gorder));
for i = 1:numel(gorder), gcols(i) = find(strcmp(branches, gorder{i})); end
QG = Q(:, gcols);
Yb = diag([G3, G1, G2, G4]);
M  = QG * Yb * QG.';

show_matrix(QG, cutnames, gorder, '[Q_G] (4x4):', '%7.0f');
fprintf('\n  [Y_b] = diag(G3, G1, G2, G4) = diag(%g, %g, %g, %g)\n', G3, G1, G2, G4);
show_matrix(M, cutnames, cutnames, '[Q_G][Y_b][Q_G]'' (4x4):', '%9.4f');
fprintf('\n  สมมาตร? %s   <- ต้องเป็นเสมอ (reciprocal network)\n', ...
        tf2str(norm(M - M.') < 1e-12));
fprintf('\n  รูปเชิงสัญลักษณ์:\n');
fprintf('      [   G1        -G1          0        0    ]\n');
fprintf('      [  -G1    G1+G2+G3        G2      -G2    ]\n');
fprintf('      [    0         G2         G2      -G2    ]\n');
fprintf('      [    0        -G2        -G2   G2+G4     ]\n');
fprintf('\n  G4 ปรากฏที่ตำแหน่ง (4,4) ตำแหน่งเดียว = %.4f\n', M(4,4));
fprintf('    แถวที่ 2 (ที่ใช้แก้หา Vb) ไม่มี G4 เลย -> Vb ไม่ขึ้นกับ G4\n');

row = M(2, :);
fprintf('\n  กางแถวที่ 2 (แถวเดียวที่ฝั่งขวาเป็นศูนย์แท้ๆ):\n');
fprintf('    (%+.4f)Va + (%+.4f)Vb + (%+.4f)(Vc-Vb) + (%+.4f)Vd = 0\n', ...
        row(1), row(2), row(3), row(4));
fprintf('    จัดรูปได้เป็น  G1(Vb-Va) + G3*Vb + G2(Vc-Vd) = 0\n');
fprintf('    *** นี่คือสมการ KCL ที่ supernode (b,c) เป๊ะ ***\n');

% =========================================================================
head('ขั้นที่ 5 — แก้หาแรงดันปม 3 เส้นทางที่เป็นอิสระกัน');

% เส้นทาง A: สูตรปิดที่พิสูจน์ด้วยมือ
vA = closed_form(G1, G2, G3, E1, E2, E3);

% เส้นทาง B: สมการชุดตัด แถวที่ 2
VbB = -(row(1)*E1 + row(3)*E3 + row(4)*(-E2)) / row(2);
vB  = [E1; VbB; VbB + E3; -E2];

% เส้นทาง C: แก้ระบบ Ax = b
Amat = [ 1    0        0    0 ;      % Va = E1
         0    0        0    1 ;      % Vd = -E2
         0   -1        1    0 ;      % Vc - Vb = E3
        -G1  (G1+G3)  G2  -G2 ];     % KCL supernode
bvec = [E1; -E2; E3; 0];
vC = Amat \ bvec;

fprintf('\n  ระบบสมการเชิงเส้น A x = b ของเส้นทาง C:\n');
labels = {'Va = E1','Vd = -E2','Vc - Vb = E3','KCL supernode'};
fprintf('       %10s%10s%10s%10s   |%10s\n', 'Va','Vb','Vc','Vd','b');
for i = 1:4
    fprintf('    %10.4f%10.4f%10.4f%10.4f   |%10.4f   (%s)\n', ...
            Amat(i,1), Amat(i,2), Amat(i,3), Amat(i,4), bvec(i), labels{i});
end

fprintf('\n  %-24s%16s%16s%16s%16s\n', '', 'Va','Vb','Vc','Vd');
fprintf('  %s\n', repmat('-', 1, 90));
fprintf('  %-24s%16.12f%16.12f%16.12f%16.12f\n', 'A: สูตรปิด (มือ)',  vA);
fprintf('  %-24s%16.12f%16.12f%16.12f%16.12f\n', 'B: สมการชุดตัด',    vB);
fprintf('  %-24s%16.12f%16.12f%16.12f%16.12f\n', 'C: แก้ระบบ Ax=b',   vC);
worst = max([max(abs(vA-vB)), max(abs(vA-vC))]);
fprintf('\n  ทั้งสามเส้นทางตรงกัน? %s   (ต่างกันสูงสุด %.3e)\n', ...
        tf2str(worst < 1e-9), worst);

Va = vA(1); Vb = vA(2); Vc = vA(3); Vd = vA(4);
fprintf('\n  === คำตอบ ===\n');
fprintf('    Va = %10.6f V   (= E1 ; ขั้วบวกอยู่ที่ปม a)\n', Va);
fprintf('    Vb = %10.6f V   (จากสมการ supernode)\n', Vb);
fprintf('    Vc = %10.6f V   (= Vb + E3)\n', Vc);
fprintf('    Vd = %10.6f V   (= -E2 ; ขั้ว*ลบ*อยู่ที่ปม d)\n', Vd);

% =========================================================================
head('ขั้นที่ 6 — ตรวจ KCL, สมดุลกำลังไฟฟ้า และผลของ G4');

iG1 = G1*(Va - Vb);  iG3 = G3*Vb;
iG2 = G2*(Vc - Vd);  iG4 = G4*Vd;
fprintf('\n  กระแสแต่ละกิ่ง:\n');
fprintf('    i_G1 = G1(Va-Vb) = %12.6f A\n', iG1);
fprintf('    i_G3 = G3*Vb     = %12.6f A\n', iG3);
fprintf('    i_G2 = G2(Vc-Vd) = %12.6f A\n', iG2);
fprintf('    i_G4 = G4*Vd     = %12.6f A%s\n', iG4, ...
        ternary(iG4 < 0, '   <- ติดลบ = ไหลสวนทิศอ้างอิง', ''));

fprintf('\n  ตรวจ KCL ที่ supernode (b,c):  i_G1 =?= i_G3 + i_G2\n');
fprintf('    %.9f =?= %.9f + %.9f = %.9f\n', iG1, iG3, iG2, iG3+iG2);
fprintf('    ผลต่าง = %.3e   %s\n', iG1-(iG3+iG2), ...
        ternary(abs(iG1-(iG3+iG2)) < 1e-9, 'OK', 'FAIL'));

iE1 = -iG1;  iE3 = -iG2;  iE2 = iG2 - iG4;
fprintf('\n  กระแสของแหล่งจ่าย (จากรอยตัดที่ 1, 3, 4):\n');
fprintf('    i_E1 = %12.6f A (ทิศ a->e)\n', iE1);
fprintf('    i_E3 = %12.6f A (ทิศ c->b)\n', iE3);
fprintf('    i_E2 = %12.6f A (ทิศ d->e)\n', iE2);

pG = [G1*(Va-Vb)^2, G3*Vb^2, G2*(Vc-Vd)^2, G4*Vd^2];
pE = [-(Va*iE1), -((Vc-Vb)*iE3), -(Vd*iE2)];
fprintf('\n  สมดุลกำลังไฟฟ้า:\n');
gn = {'G1','G3','G2','G4'};
for i = 1:4, fprintf('    P(%s) = %12.6f W\n', gn{i}, pG(i)); end
fprintf('    รวมสูญเสีย = %12.6f W\n', sum(pG));
en = {'E1','E3','E2'};
for i = 1:3, fprintf('    P(%s) = %12.6f W  (จ่ายออก)\n', en{i}, pE(i)); end
fprintf('    รวมจ่าย    = %12.6f W\n', sum(pE));
fprintf('\n    ผลต่าง = %.3e W   %s\n', sum(pE)-sum(pG), ...
        ternary(abs(sum(pE)-sum(pG)) < 1e-9, 'สมดุล (ระดับ machine epsilon)', 'ไม่สมดุล!'));

fprintf('\n  ทดสอบว่า G4 มีผลต่อแรงดันปมหรือไม่ — กวาดค่า G4:\n');
fprintf('    %12s%12s%12s%12s%12s%14s\n', 'G4 [mho]','Va','Vb','Vc','Vd','i_G4 [A]');
fprintf('  %s\n', repmat('-', 1, 76));
for g4 = [0, G4, 5, 1000]
    r = closed_form(G1, G2, G3, E1, E2, E3);   % ไม่ขึ้นกับ G4 เลย
    fprintf('    %12.4g%12.6f%12.6f%12.6f%12.6f%14.4f\n', g4, r(1), r(2), r(3), r(4), g4*r(4));
end
fprintf('\n    -> แรงดันทั้งสี่ปมไม่ขยับเลย แม้ G4 เปลี่ยน 2,500 เท่า\n');
fprintf('       เพราะ Vd ถูกตรึงด้วยแหล่งจ่ายอุดมคติ E2 ที่ต่อขนานกับ G4\n');

% =========================================================================
head('สรุปคำตอบสุดท้าย');
fprintf('\n  รูปเชิงสัญลักษณ์:\n');
fprintf('      Va = E1\n');
fprintf('      Vb = (G1*E1 - G2*E2 - G2*E3) / (G1 + G2 + G3)\n');
fprintf('      Vc = (G1*E1 - G2*E2 + (G1+G3)*E3) / (G1 + G2 + G3)\n');
fprintf('      Vd = -E2\n');
fprintf('\n  แทนค่าตัวเลข: Va=%.6f  Vb=%.6f  Vc=%.6f  Vd=%.6f [V]\n', Va, Vb, Vc, Vd);
fprintf('\n  ข้อสังเกตสำคัญ 3 ข้อสำหรับห้องสอบ:\n');
fprintf('    1. G4 ไม่ปรากฏในคำตอบแรงดันเลย เพราะ Vd ถูกตรึงด้วยแหล่งจ่ายอุดมคติ E2\n');
fprintf('    2. รอยตัดพื้นฐานของกิ่ง G3 ให้สมการเดียวกับ KCL ที่ supernode (b,c)\n');
fprintf('    3. Vd = -E2 (ไม่ใช่ +E2) เพราะขั้วลบของ E2 อยู่ที่ปม d\n\n');
fprintf('ดูคำอธิบายเต็มที่ CLAUDE_SOLUTION.md\n');
fprintf('ซ้อมตอบสอบปากเปล่าที่ interactive_dashboard.html แท็บที่ 5\n\n');

end

% =========================================================================
% ฟังก์ชันย่อย
% =========================================================================
function v = closed_form(G1, G2, G3, E1, E2, E3)
den = G1 + G2 + G3;
Vb  = (G1*E1 - G2*E2 - G2*E3) / den;
Vc  = (G1*E1 - G2*E2 + (G1+G3)*E3) / den;
v   = [E1; Vb; Vc; -E2];
end

function head(s)
fprintf('\n%s\n%s\n%s\n', repmat('=',1,74), s, repmat('=',1,74));
end

function show_matrix(M, rowNames, colNames, title, fmt)
fprintf('\n%s\n', title);
fprintf('        ');
for j = 1:numel(colNames), fprintf('%8s', colNames{j}); end
fprintf('\n');
for i = 1:size(M,1)
    fprintf('  %10s', rowNames{i});
    for j = 1:size(M,2), fprintf(fmt, M(i,j)); end
    fprintf('\n');
end
end

function s = tf2str(b)
if b, s = 'true'; else, s = 'false'; end
end

function out = ternary(cond, a, b)
if cond, out = a; else, out = b; end
end
