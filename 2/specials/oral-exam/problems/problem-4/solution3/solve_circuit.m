function result = solve_circuit(G1, G2, G3, alpha, I0)
% solve_circuit.m — 303212 Oral Exam ข้อที่ 4
% Conductance network + CCCS alpha*ix
%
% ใช้ได้ทั้ง MATLAB และ GNU Octave โดยไม่ต้องมี toolbox พิเศษ
% ถ้าไม่ส่ง argument จะใช้ค่าตัวอย่างในบทเรียน:
%   G1=0.8, G2=0.35, G3=0.55 mho, alpha=0.4, I0=2.4 A
%
% โมเดล:
%   ix = G1*Va
%   dependent source = alpha*ix จาก b ไป a
%   I0 จาก e ไป a
%   Ve = 0
%
% สมการที่ได้:
%   ((1-alpha)*G1 + G2)*Va - G2*Vb = I0
%   (alpha*G1 - G2)*Va + (G2 + G3)*Vb = 0

if nargin == 0
    G1 = 0.8;
    G2 = 0.35;
    G3 = 0.55;
    alpha = 0.4;
    I0 = 2.4;
elseif nargin ~= 5
    error('ส่ง argument ให้ครบ 5 ตัว: G1, G2, G3, alpha, I0');
end

if G1 <= 0 || G2 <= 0 || G3 <= 0
    error('G1, G2 และ G3 ต้องเป็นค่าบวก');
end

% เลือกต้นไม้ {G1,G3}; กิ่งเรียงเป็น [G1,G3,G2,I0,alpha_ix]
QK = [1, 0,  1, -1, -1;
      0, 1, -1,  0,  1];

% ib = Yb*vb + Jb, vb = QK'*[Va;Vb]
% แถวสุดท้ายคือ CCCS: alpha*ix = alpha*G1*v_G1
Yb = [G1, 0,  0,  0, 0;
      0,  G3, 0,  0, 0;
      0,  0,  G2, 0, 0;
      0,  0,  0,  0, 0;
      alpha*G1, 0, 0, 0, 0];
Jb = [0; 0; 0; I0; 0];

A = QK*Yb*QK';
Jcut = -QK*Jb;
Delta = det(A);

if abs(Delta) <= 1e-12 * max(1, norm(A, inf)^2)
    error('เมทริกซ์ singular หรือเกือบ singular: Delta = %.12g', Delta);
end

% แก้ด้วย matrix solver
V = A\Jcut;
Va = V(1);
Vb = V(2);

% ตรวจด้วย Cramer's Rule
Dcramer = A(1,1)*A(2,2) - A(1,2)*A(2,1);
Da = I0*A(2,2);
Db = -I0*A(2,1);
Va_cramer = Da/Dcramer;
Vb_cramer = Db/Dcramer;

% กระแสกิ่งและ residual ของ KCL
ix = G1*Va;
idep = alpha*ix;
iG2 = G2*(Va - Vb);
iG3 = G3*Vb;
kcl_a = I0 + idep - ix - iG2;
kcl_b = -idep + iG2 - iG3;
residual = A*V - Jcut;

fprintf('==============================================================\n');
fprintf('303212 Oral Exam — Problem 4: Conductance + CCCS\n');
fprintf('==============================================================\n');
fprintf('G1=%.6f, G2=%.6f, G3=%.6f mho, alpha=%.6f, I0=%.6f A\n', ...
        G1, G2, G3, alpha, I0);
fprintf('\n[QK] =\n'); disp(QK);
fprintf('[Yb] =\n'); disp(Yb);
fprintf('A = QK*Yb*QK'' =\n'); disp(A);
fprintf('Jcut =\n'); disp(Jcut);
fprintf('Delta = %.12f mho^2\n\n', Delta);
fprintf('Va = %.12f V\n', Va);
fprintf('Vb = %.12f V\n', Vb);
fprintf('Cramer Va = %.12f V (difference %.3e)\n', Va_cramer, Va_cramer - Va);
fprintf('Cramer Vb = %.12f V (difference %.3e)\n', Vb_cramer, Vb_cramer - Vb);
fprintf('\nix       = %.12f A\n', ix);
fprintf('alpha*ix = %.12f A\n', idep);
fprintf('iG2      = %.12f A\n', iG2);
fprintf('iG3      = %.12f A\n', iG3);
fprintf('KCL(a) residual = %.3e A\n', kcl_a);
fprintf('KCL(b) residual = %.3e A\n', kcl_b);
fprintf('matrix residual  = %.3e\n', norm(residual, inf));

% ค่าที่คืนสำหรับเรียกจากสคริปต์/ผู้ใช้อื่น
result = struct();
result.parameters = struct('G1', G1, 'G2', G2, 'G3', G3, ...
                           'alpha', alpha, 'I0', I0);
result.QK = QK;
result.Yb = Yb;
result.Jb = Jb;
result.A = A;
result.Jcut = Jcut;
result.Delta = Delta;
result.Va = Va;
result.Vb = Vb;
result.ix = ix;
result.alpha_ix = idep;
result.iG2 = iG2;
result.iG3 = iG3;
result.kcl_a = kcl_a;
result.kcl_b = kcl_b;
result.residual = residual;

end

% หมายเหตุเชิงทฤษฎี:
% Delta = G1*G2 + G2*G3 + (1-alpha)*G1*G3
% alpha_critical = 1 + G2/G1 + G2/G3
% เมื่อ Delta เข้าใกล้ศูนย์ วงจร active จะไวต่อพารามิเตอร์มากและ A กลับไม่ได้
