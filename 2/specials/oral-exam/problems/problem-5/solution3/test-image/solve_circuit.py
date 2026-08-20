#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solve Circuit Problem 5 using Fundamental Cut-set Method with EXACT 4 BRANCHES (Tree = {1, 2}, Links = {3, 4})
Branch Orientations: 1: e->a, 2: a->b, 3: a->e, 4: e->b
Q_f = [[1, 0, -1, 1], [0, 1, 0, 1]]
"""

import numpy as np

def solve_circuit(G1=0.4, G2=0.3, G3=0.2, G4=0.5, E1=12.0, E2=6.0, E3=2.0):
    # Fundamental Cut-set Matrix: [1, 2, 3, 4]
    # Row 1 (Cut c1): i1 - i3 + i4 = 0
    # Row 2 (Cut c2): i2 + i4 = 0
    Qf = np.array([
        [ 1,  0, -1,  1],
        [ 0,  1,  0,  1]
    ])
    
    # Voltage constraint Vb = -E2
    Vb = -E2
    
    # Va formula derived from Cut-set KCL
    denom = G1 + G2 + G3
    Va = (G1 * E1 - G2 * E3 - G2 * E2) / denom
    
    # Branch currents
    i1 = G1 * (E1 - Va)
    i2 = G2 * (Va + E3 - Vb)
    i3 = G3 * Va
    iG4 = -G4 * Vb  # G4 component directed e->b
    iE2 = -i2 - iG4  # E2 reaction current
    i4 = iG4 + iE2   # Total branch 4 current = -i2
    
    # KCL Residual checks:
    # Cut c1: i1 - i3 + i4
    # Cut c2: i2 + i4
    residual_c1 = i1 - i3 + i4
    residual_c2 = i2 + i4
    
    return {
        "Va": Va, "Vb": Vb,
        "i1": i1, "i2": i2, "i3": i3, "i4": i4,
        "iG4": iG4, "iE2": iE2,
        "residual_c1": residual_c1,
        "residual_c2": residual_c2
    }

if __name__ == "__main__":
    res = solve_circuit()
    print("=== Solution for Problem 5 (4 Branches, User Convention: Q_f = [[1,0,-1,1],[0,1,0,1]]) ===")
    print(f"Va = {res['Va']:.6f} V (exact: 8/3 V)")
    print(f"Vb = {res['Vb']:.6f} V")
    print(f"i1 = {res['i1']:.6f} A (Tree 1: e->a)")
    print(f"i2 = {res['i2']:.6f} A (Tree 2: a->b)")
    print(f"i3 = {res['i3']:.6f} A (Link 3: a->e)")
    print(f"i4 = {res['i4']:.6f} A (Link 4: e->b = -i2)")
    print(f"  └─ iG4 = {res['iG4']:.6f} A")
    print(f"  └─ iE2 = {res['iE2']:.6f} A")
    print(f"KCL Cut c1 (i1 - i3 + i4) residual: {res['residual_c1']:.2e} A")
    print(f"KCL Cut c2 (i2 + i4) residual: {res['residual_c2']:.2e} A")
