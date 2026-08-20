% Solve Circuit Problem 5 using Fundamental Cut-set Method (User Convention: Q_f = [[1,0,-1,1],[0,1,0,1]])
function res = solve_circuit(G1, G2, G3, G4, E1, E2, E3)
    if nargin < 7, E3 = 2.0; end
    if nargin < 6, E2 = 6.0; end
    if nargin < 5, E1 = 12.0; end
    if nargin < 4, G4 = 0.5; end
    if nargin < 3, G3 = 0.2; end
    if nargin < 2, G2 = 0.3; end
    if nargin < 1, G1 = 0.4; end

    Vb = -E2;
    Va = (G1*E1 - G2*E3 - G2*E2) / (G1 + G2 + G3);
    
    i1 = G1*(E1 - Va);
    i2 = G2*(Va + E3 - Vb);
    i3 = G3*Va;
    iG4 = -G4*Vb;
    iE2 = -i2 - iG4;
    i4 = iG4 + iE2;
    
    fprintf('=== Solution for Problem 5 (User Convention) ===\n');
    fprintf('Va = %.6f V\n', Va);
    fprintf('Vb = %.6f V\n', Vb);
    fprintf('i1 = %.6f A\n', i1);
    fprintf('i2 = %.6f A\n', i2);
    fprintf('i3 = %.6f A\n', i3);
    fprintf('i4 = %.6f A\n', i4);
end
