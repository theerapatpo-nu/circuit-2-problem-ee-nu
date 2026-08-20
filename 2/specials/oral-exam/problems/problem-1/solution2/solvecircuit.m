%% solvecircuit.m
% Oral-exam battery circuit: KCL, charge integration, parameter fitting,
% identifiability check, and plots.  Run this file from any working folder;
% paths are resolved relative to the script itself.
%
% IMPORTANT IDENTIFIABILITY RESULT
% With i(t)=I0 constant, terminal voltage contains Eo and Ri only through
% C0 = Eo - I0*Ri.  This dataset cannot identify Eo and Ri separately.
% RI_ASSUMED must come from an independent current-pulse/impedance test.

clear; clc; close all;

RL = 10.0;                    % load resistance [ohm]
tn = 3600.0;                  % nominal discharge time [s]
RI_ASSUMED = 0.20;            % teaching assumption, NOT fitted from these rows
scriptDir = fileparts(mfilename('fullpath'));
parentDir = fileparts(scriptDir);
xlsFile = fullfile(parentDir, 'data303212qz02.xls');
mdFile = fullfile(parentDir, 'data303212qz02.md');

%% 1) Read the original .xls; fall back to the Markdown table.
try
    raw = readmatrix(xlsFile, 'FileType', 'spreadsheet');
    raw = raw(:, 1:3);
    raw = raw(all(isfinite(raw), 2), :);
    sourceFile = xlsFile;
catch readError
    warning('Excel read failed (%s). Reading the Markdown table.', readError.message);
    raw = readMarkdownNumericTable(mdFile);
    sourceFile = mdFile;
end

t = raw(:, 1);                % [s]
v = raw(:, 2);                % measured terminal voltage [V]
isrc = raw(:, 3);             % dependent-source current [A]
assert(numel(t) == 2753, 'Expected 2,753 numeric rows.');

%% 2) KCL at Node 1 and charge integration.
% Incoming battery current = both outgoing branch currents.
% i(t) = is(t) + v(t)/RL
i = isrc + v/RL;
I0 = mean(i);
assert(max(abs(i - I0)) < 1e-12, 'The supplied dataset should have constant i(t).');
q = cumtrapz(t, i);           % q(0)=0 [C]
Qn = I0*tn;                   % constant-current extension to t_n [C]
remainingQ = Qn - q;

%% 3) Robust nonlinear identification in the identifiable coordinates.
% Model: v = C0 - K*q + Aa*exp(-Ba*q) - Ab*exp(-Bb*(Qn-q))
% where C0 = Eo - I0*Ri.
%
% For fixed Ba and Bb, [C0 K Aa Ab] are linear coefficients.  Optimize only
% log(Ba),log(Bb) globally from several starts, then solve the linear block.
starts = log([0.001 0.001; 0.001 0.01; 0.005 0.005; 0.01 0.01; ...
              0.01 0.02; 0.02 0.01; 0.05 0.02; 0.02 0.05]);
bestCost = inf;
bestLogRates = starts(1, :);
fmOpts = optimset('Display', 'off', 'MaxFunEvals', 2e4, 'MaxIter', 2e4, ...
                  'TolX', 1e-12, 'TolFun', 1e-20);
for row = 1:size(starts, 1)
    candidate = fminsearch(@(z) projectedSSE(z, q, remainingQ, v), ...
                           starts(row, :), fmOpts);
    candidateCost = projectedSSE(candidate, q, remainingQ, v);
    if candidateCost < bestCost
        bestCost = candidateCost;
        bestLogRates = candidate;
    end
end

[~, linearCoefficients] = projectedSSE(bestLogRates, q, remainingQ, v);
Ba0 = exp(bestLogRates(1));
Bb0 = exp(bestLogRates(2));
p0 = [linearCoefficients(1), linearCoefficients(2), ...
      linearCoefficients(3), Ba0, linearCoefficients(4), Bb0];
modelC0 = @(p, qData) p(1) - p(2)*qData + p(3)*exp(-p(4)*qData) ...
    - p(5)*exp(-p(6)*(Qn-qData));

if exist('lsqcurvefit', 'file') == 2
    lower = [0, 0, 0, 1e-7, 0, 1e-7];
    upper = [10, 0.01, 10, 1, 5000, 1];
    lsqOpts = optimoptions('lsqcurvefit', 'Display', 'off', ...
        'FunctionTolerance', 1e-14, 'StepTolerance', 1e-14, ...
        'OptimalityTolerance', 1e-14, 'MaxFunctionEvaluations', 1e5);
    p = lsqcurvefit(modelC0, p0, q, v, lower, upper, lsqOpts);
    optimizerName = 'multi-start fminsearch + lsqcurvefit';
else
    % The variable-projection fminsearch result is already a complete fit.
    p = p0;
    optimizerName = 'multi-start fminsearch (Optimization Toolbox unavailable)';
end

C0 = p(1); K = p(2); Aa = p(3); Ba = p(4);
Ab = p(5); Bb = p(6);
Ri = RI_ASSUMED;
Eo = C0 + I0*Ri;             % conditional on the independently supplied Ri
vFit = modelC0(p, q);
residual = vFit - v;
SSE = sum(residual.^2);
RMSE = sqrt(mean(residual.^2));
maxError = max(abs(residual));

%% 4) Report results without claiming that Ri came from this experiment.
fprintf('\n%s\n', repmat('=', 1, 76));
fprintf('BATTERY CIRCUIT ANALYSIS AND PARAMETER IDENTIFICATION (MATLAB)\n');
fprintf('%s\n', repmat('=', 1, 76));
fprintf('Source: %s\n', sourceFile);
fprintf('Rows: %d\n', numel(t));
fprintf('Optimizer: %s\n\n', optimizerName);
fprintf('i(t) = %.12f A for every row\n', I0);
fprintf('q(t) = %.12f*t C; q(2752) = %.9f C\n', I0, q(end));
fprintf('Qn = %.9f C = %.9f Ah\n\n', Qn, Qn/3600);
fprintf('Identifiable values:\n');
fprintf('  C0 = Eo - i*Ri = %.15f V\n', C0);
fprintf('  K  = %.15g V/C\n', K);
fprintf('  Aa = %.15g V\n', Aa);
fprintf('  Ba = %.15g 1/C\n', Ba);
fprintf('  Ab = %.15g V\n', Ab);
fprintf('  Bb = %.15g 1/C\n\n', Bb);
fprintf('Conditional pair (Ri assumed from a separate test):\n');
fprintf('  Ri = %.9f ohm [ASSUMED]\n', Ri);
fprintf('  Eo = C0 + i*Ri = %.15f V [CONDITIONAL]\n', Eo);
fprintf('  Family: Eo = %.15f + %.12f*Ri\n\n', C0, I0);
fprintf('SSE = %.6e V^2; RMSE = %.6e V; max|error| = %.6e V\n', ...
        SSE, RMSE, maxError);
fprintf('%s\n\n', repmat('=', 1, 76));

%% 5) Save calculated rows and a machine-readable summary.
resultTable = table(t, v, isrc, i, q, vFit, residual, ...
    'VariableNames', {'t_s','v_measured_V','is_A','i_A','q_C','v_fitted_V','residual_V'});
writetable(resultTable, fullfile(scriptDir, 'computed_data_matlab.csv'));
summary = struct('source_file', sourceFile, 'rows', numel(t), ...
    'c0_volt', C0, 'eo_volt_conditional', Eo, ...
    'k_volt_per_coulomb', K, 'aa_volt', Aa, 'ba_per_coulomb', Ba, ...
    'ab_volt', Ab, 'bb_per_coulomb', Bb, 'ri_ohm_assumed', Ri, ...
    'qn_coulomb', Qn, 'current_ampere', I0, 'sse_volt2', SSE, ...
    'rmse_volt', RMSE, 'max_abs_error_volt', maxError, ...
    'identifiability', 'Eo and Ri are not separately identifiable at constant current.');
fid = fopen(fullfile(scriptDir, 'fit_results_matlab.json'), 'w');
fprintf(fid, '%s\n', jsonencode(summary, 'PrettyPrint', true));
fclose(fid);

%% 6) Plots requested in the problem.
signalFigure = figure('Color', [0.03 0.07 0.12], 'Position', [80 80 1280 760]);
tiledlayout(2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
drawSignal(t, v, [0.38 0.85 1.00], 'Terminal voltage v(t)', 'Voltage [V]');
drawSignal(t, isrc, [0.65 0.55 0.98], 'Dependent current i_s(t)', 'Current [A]');
drawSignal(t, i, [0.20 0.83 0.60], 'Battery current i(t) from KCL', 'Current [A]');
drawSignal(t, q, [0.98 0.75 0.18], 'Accumulated charge q(t)', 'Charge [C]');
sgtitle('Battery-circuit signals - 2,753 measured rows', 'Color', 'w');
exportgraphics(signalFigure, fullfile(scriptDir, 'signals_overview_matlab.png'), 'Resolution', 180);

fitFigure = figure('Color', [0.03 0.07 0.12], 'Position', [100 100 1280 720]);
tiledlayout(2, 1, 'TileSpacing', 'compact', 'Padding', 'compact');
nexttile;
plot(t, v, 'Color', [0.38 0.85 1.00], 'LineWidth', 2.5); hold on;
plot(t, vFit, '--', 'Color', [0.98 0.45 0.55], 'LineWidth', 1.4);
title('Terminal voltage: measurement vs nonlinear model', 'Color', 'w');
ylabel('Voltage [V]'); legend('Measured', 'Fitted', 'TextColor', 'w', 'Location', 'best');
styleAxis(gca);
nexttile;
plot(t, 1e6*residual, 'Color', [0.98 0.75 0.18], 'LineWidth', 1.2);
xlabel('Time [s]'); ylabel('Error [microvolt]');
styleAxis(gca);
exportgraphics(fitFigure, fullfile(scriptDir, 'voltage_fit_matlab.png'), 'Resolution', 180);

%% Local functions
function numeric = readMarkdownNumericTable(filename)
    lines = readlines(filename);
    rows = zeros(numel(lines), 3);
    count = 0;
    pattern = '^\s*\|\s*([-+0-9.eE]+)\s*\|\s*([-+0-9.eE]+)\s*\|\s*([-+0-9.eE]+)\s*\|\s*$';
    for index = 1:numel(lines)
        tokens = regexp(lines(index), pattern, 'tokens', 'once');
        if ~isempty(tokens)
            count = count + 1;
            rows(count, :) = str2double(tokens);
        end
    end
    numeric = rows(1:count, :);
end

function [cost, coefficients] = projectedSSE(logRates, q, remainingQ, voltage)
    rates = exp(logRates);
    design = [ones(size(q)), -q, exp(-rates(1)*q), -exp(-rates(2)*remainingQ)];
    coefficients = design\voltage;
    error = design*coefficients - voltage;
    cost = error'*error;
end

function drawSignal(t, y, color, plotTitle, yLabel)
    nexttile;
    plot(t, y, 'Color', color, 'LineWidth', 1.8);
    title(plotTitle, 'Color', 'w'); xlabel('Time [s]'); ylabel(yLabel);
    styleAxis(gca);
end

function styleAxis(axisHandle)
    axisHandle.Color = [0.04 0.10 0.17];
    axisHandle.XColor = [0.78 0.84 0.91];
    axisHandle.YColor = [0.78 0.84 0.91];
    axisHandle.GridColor = [0.35 0.43 0.53];
    axisHandle.GridAlpha = 0.22;
    grid(axisHandle, 'on'); box(axisHandle, 'on');
end
