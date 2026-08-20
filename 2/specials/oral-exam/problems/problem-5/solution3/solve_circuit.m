%% 303212 Oral Exam — Problem 5
% Conductance network with directed graph; solve A*x=b and verify KCL.
clear; clc;
G1=.4; G2=.3; G3=.2; G4=.5; E1=12; E2=6; E3=2;
A=[G1+G2+G3, -G2; 0, 1];
b=[G1*E1-G2*E3; -E2];
x=A\b; Va=x(1); Vb=x(2);
iG1=G1*(E1-Va); iG2=G2*(Va+E3-Vb);
iG3=G3*Va; iG4=-G4*Vb; iE2=-iG2-iG4; i4total=iG4+iE2;
Qg=[-1 1 1 0; 0 -1 0 -1];
Yb=diag([G1 G2 G3 G4]); M=Qg*Yb*Qg.';
fprintf('Va = %.12f V\nVb = %.12f V\n',Va,Vb);
fprintf('iG1=%.12f, iG2=%.12f, iG3=%.12f, iG4=%.12f, iE2=%.12f A\n',iG1,iG2,iG3,iG4,iE2);
fprintf('graph branch i4 = iG4+iE2 = %.12f A\n',i4total);
fprintf('KCL-a residual = %.3e\n',-iG1+iG2+iG3);
fprintf('KCL-b graph residual = %.3e\n',-iG2-i4total);
fprintf('KCL-b physical residual = %.3e\n',-iG2-iG4-iE2);
disp('Qg*Yb*Qg^T ='); disp(M);
assert(abs(-iG1+iG2+iG3)<1e-10 && abs(-iG2-i4total)<1e-10 && abs(-iG2-iG4-iE2)<1e-10);
% กิ่ง 4 ชี้ e->b จึง iG4=-G4*Vb; E2 ใช้ทิศกระแส e->b เช่นกัน
