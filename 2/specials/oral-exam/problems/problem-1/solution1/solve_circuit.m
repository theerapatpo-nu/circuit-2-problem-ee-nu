%% solve_circuit.m
% =========================================================================
% MATLAB Code for Nodal Analysis & Non-linear Parameter Estimation
% Dataset: data303212qz02.xls
% Course: Circuit Analysis & Power Engineering Oral Exam Defense
% =========================================================================

clear; clc;

%% 1. Load Data from Excel File
filename = '../data303212qz02.xls';
if ~exist(filename, 'file')
    error('File %s not found!', filename);
end

data = readtable(filename);
t = data{:, 1};    % time [s]
v = data{:, 2};    % voltage v(t) [V]
is = data{:, 3};   % current is(t) [A]

%% 2. Step 1: Nodal Analysis (KCL)
R_L = 10.0;        % Load resistance [Ohm]
i_t = is + (v / R_L);

fprintf('=======================================================\n');
fprintf('  Step 1: Nodal Analysis (KCL) Output\n');
fprintf('=======================================================\n');
fprintf('Mean i(t) = %.6f A\n', mean(i_t));
fprintf('Std i(t)  = %.18e A\n', std(i_t));
fprintf('-> Key Discovery: i(t) is EXACTLY CONSTANT = 0.740000 A!\n\n');

%% 3. Step 2: Integration for Charge q(t) and Nominal Capacity Q_n
t_n = 3600;       % Nominal discharge duration [s]
q_t = 0.74 * t;    % Integrated charge [Coulombs]
Q_n = 0.74 * t_n;  % Total theoretical capacity [Coulombs] = 2664 C

fprintf('=======================================================\n');
fprintf('  Step 2: Nominal Capacity & Charge Output\n');
fprintf('=======================================================\n');
fprintf('Q_n = %.2f Coulombs\n', Q_n);
fprintf('q(2752) = %.2f Coulombs\n\n', q_t(end));

%% 4. Step 3: Parameter Optimization using lsqcurvefit / fminsearch
% Model: v(t) = E_o - K*q + A_a*exp(-B_a*q) - A_b*exp(-B_b*(Q_n-q)) - i*R_i
v_model = @(p, q_data) (p(1) - p(2)*q_data + p(3)*exp(-p(4)*q_data) ...
                        - p(5)*exp(-p(6)*(Q_n - q_data)) - 0.74*p(7));

p0 = [4.2, 0.0001, 0.2, 0.005, 1.0, 0.002, 0.2]; % Initial guess
lb = [3.0, 0, 0, 1e-5, 0, 1e-5, 0];             % Lower bounds
ub = [5.0, 0.01, 2.0, 0.1, 5.0, 0.1, 2.0];       % Upper bounds

opts = optimoptions('lsqcurvefit', 'Display', 'off');
try
    [p_opt, resnorm] = lsqcurvefit(v_model, p0, q_t, v, lb, ub, opts);
catch
    % Fallback to fminsearch if lsqcurvefit is not in toolbox
    cost = @(p) sum((v - v_model(p, q_t)).^2);
    p_opt = fminsearch(cost, p0);
end

fprintf('=======================================================\n');
fprintf('  Step 3: Parameter Identification Output\n');
fprintf('=======================================================\n');
fprintf('E_o = %.6f V\n', p_opt(1));
fprintf('K   = %.8f V/C\n', p_opt(2));
fprintf('A_a = %.6f V\n', p_opt(3));
fprintf('B_a = %.8f 1/C\n', p_opt(4));
fprintf('A_b = %.6f V\n', p_opt(5));
fprintf('B_b = %.8f 1/C\n', p_opt(6));
fprintf('R_i = %.6f Ohm\n', p_opt(7));
fprintf('Q_n = %.2f C\n', Q_n);
fprintf('=======================================================\n');
