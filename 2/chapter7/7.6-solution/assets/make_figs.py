#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างสื่อประกอบการสอนโจทย์ [7.6]
y'''(t) + y'(t) - 2y(t) = x''(t) + x'(t) + 2x(t)
H(s) = (s^2+s+2)/(s^3+s-2) = 1/(s-1)  ->  h(t) = e^t u(t)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Polygon
from matplotlib.patches import FancyBboxPatch

# ---------- ฟอนต์ไทย ----------
for f in ["/System/Library/Fonts/Supplemental/SukhumvitSet.ttc",
          "/System/Library/Fonts/Supplemental/Thonburi.ttc"]:
    try:
        fm.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams["font.family"] = ["Sukhumvit Set", "Thonburi", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["savefig.facecolor"] = "white"

HERE = os.path.dirname(os.path.abspath(__file__))
def save(fig, name):
    p = os.path.join(HERE, name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    print("saved:", p)

# สีธีม
C_BLUE   = "#1f4e79"
C_RED    = "#c0392b"
C_GREEN  = "#1e8449"
C_ORANGE = "#d68910"
C_PURPLE = "#6c3483"
C_GRAY   = "#5d6d7e"
C_LIGHT  = "#eaf2f8"


# =========================================================
# FIG 1 : ภาพรวมกระบวนการแก้ปัญหา (Roadmap)
# =========================================================
def fig1_roadmap():
    fig, ax = plt.subplots(figsize=(13, 7.2))
    ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis("off")

    ax.text(6.5, 6.85, "แผนที่การแก้โจทย์ [7.6] : จาก ODE สู่ Impulse Response",
            ha="center", va="top", fontsize=17, fontweight="bold", color=C_BLUE)

    boxes = [
        (0.4,  4.6, "ขั้นที่ 1\nโจทย์ ODE", "$y'''+y'-2y$\n$=x''+x'+2x$", C_GRAY),
        (3.0,  4.6, "ขั้นที่ 2\nLaplace Transform", "$\\mathcal{L}\\{y^{(n)}\\}=s^nY(s)$\n(IC = 0)", C_BLUE),
        (5.6,  4.6, "ขั้นที่ 3\nจัดรูปพีชคณิต", "$(s^3+s-2)Y$\n$=(s^2+s+2)X$", C_PURPLE),
        (8.2,  4.6, "ขั้นที่ 4\nTransfer Function", "$H(s)=\\frac{Y(s)}{X(s)}$", C_ORANGE),
        (10.8, 4.6, "ขั้นที่ 5\nแยกตัวประกอบ", "$s^3+s-2$\n$=(s-1)(s^2+s+2)$", C_ORANGE),
        (10.8, 2.0, "ขั้นที่ 6\nตัดทอน (Cancel)", "$H(s)=\\frac{1}{s-1}$", C_RED),
        (8.2,  2.0, "ขั้นที่ 7\nกำหนด ROC", "$\\mathrm{Re}\\{s\\}>1$\n(causal)", C_RED),
        (5.6,  2.0, "ขั้นที่ 8\nInverse Laplace", "$\\frac{1}{s-a}\\leftrightarrow e^{at}u(t)$", C_GREEN),
        (3.0,  2.0, "ขั้นที่ 9\nคำตอบ", "$h(t)=e^{t}u(t)$", C_GREEN),
        (0.4,  2.0, "ขั้นที่ 10\nตรวจสอบ", "แทนกลับใน ODE\nและวิเคราะห์เสถียรภาพ", C_GRAY),
    ]
    W, H = 2.1, 1.55
    for (x, y, title, body, col) in boxes:
        box = FancyBboxPatch((x, y), W, H, boxstyle="round,pad=0.06,rounding_size=0.12",
                             linewidth=2, edgecolor=col, facecolor=col, alpha=0.10)
        ax.add_patch(box)
        ax.text(x + W/2, y + H - 0.22, title, ha="center", va="top",
                fontsize=10.5, fontweight="bold", color=col)
        ax.text(x + W/2, y + 0.42, body, ha="center", va="center",
                fontsize=10.5, color="#222222")

    # ลูกศรแถวบน (ซ้าย -> ขวา)
    for x in [0.4, 3.0, 5.6, 8.2]:
        ax.add_patch(FancyArrowPatch((x + W + 0.03, 4.6 + H/2), (x + 2.6 - 0.03, 4.6 + H/2),
                                     arrowstyle="-|>", mutation_scale=17,
                                     linewidth=2, color="#7f8c8d"))
    # ลูกศรลง
    ax.add_patch(FancyArrowPatch((10.8 + W/2, 4.6 - 0.03), (10.8 + W/2, 2.0 + H + 0.03),
                                 arrowstyle="-|>", mutation_scale=17, linewidth=2, color="#7f8c8d"))
    # ลูกศรแถวล่าง (ขวา -> ซ้าย)
    for x in [10.8, 8.2, 5.6, 3.0]:
        ax.add_patch(FancyArrowPatch((x - 0.03, 2.0 + H/2), (x - 2.6 + W + 0.03, 2.0 + H/2),
                                     arrowstyle="-|>", mutation_scale=17,
                                     linewidth=2, color="#7f8c8d"))

    ax.text(6.5, 0.95, "หัวใจของข้อนี้ : ตัวเศษ $s^2+s+2$ ตรงกับตัวประกอบหนึ่งของตัวส่วนพอดี $\\Rightarrow$ เกิด Pole-Zero Cancellation",
            ha="center", va="center", fontsize=12.5, fontweight="bold", color=C_RED,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#fdedec", edgecolor=C_RED, linewidth=1.8))
    ax.text(6.5, 0.35, "ระบบอันดับ 3 ยุบเหลือพฤติกรรมอันดับ 1 — แต่โหมดที่ถูกตัดยังคง 'ซ่อนอยู่' ในระบบจริง",
            ha="center", va="center", fontsize=11, color=C_GRAY, style="italic")
    save(fig, "fig01_roadmap.png")


# =========================================================
# FIG 2 : ตารางคู่แปลง Laplace + สมบัติอนุพันธ์
# =========================================================
def fig2_laplace_table():
    fig, ax = plt.subplots(figsize=(12.5, 7.6))
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 7.6); ax.axis("off")
    ax.text(6.25, 7.35, "เครื่องมือที่ใช้ : สมบัติอนุพันธ์ และคู่แปลงลาปลาซพื้นฐาน",
            ha="center", va="top", fontsize=16, fontweight="bold", color=C_BLUE)

    # กล่องซ้าย : สมบัติอนุพันธ์
    ax.add_patch(FancyBboxPatch((0.3, 3.6), 5.9, 3.3,
                                boxstyle="round,pad=0.1,rounding_size=0.15",
                                edgecolor=C_BLUE, facecolor=C_LIGHT, linewidth=2))
    ax.text(3.25, 6.72, "① สมบัติอนุพันธ์ (Differentiation Property)",
            ha="center", va="top", fontsize=12.5, fontweight="bold", color=C_BLUE)
    ax.text(3.25, 6.15, r"$\mathcal{L}\left\{\frac{d^n f}{dt^n}\right\}="
                        r"s^nF(s)-\sum_{k=1}^{n}s^{n-k}f^{(k-1)}(0^-)$",
            ha="center", va="center", fontsize=14)
    ax.text(3.25, 5.35, "เมื่อ Initial Conditions = 0 ทุกตัว พจน์ผลรวมหายหมด :",
            ha="center", va="center", fontsize=11, color="#333")
    ax.text(3.25, 4.75, r"$\mathcal{L}\left\{\frac{d^n f}{dt^n}\right\}=s^n F(s)$",
            ha="center", va="center", fontsize=16, color=C_RED,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=C_RED, linewidth=2))
    ax.text(3.25, 4.05, "→ 'หาอนุพันธ์ในโดเมนเวลา' = 'คูณด้วย s ในโดเมน s'",
            ha="center", va="center", fontsize=11, color=C_GREEN, fontweight="bold")

    # กล่องขวา : ตารางคู่แปลง
    ax.add_patch(FancyBboxPatch((6.4, 3.6), 5.8, 3.3,
                                boxstyle="round,pad=0.1,rounding_size=0.15",
                                edgecolor=C_GREEN, facecolor="#eafaf1", linewidth=2))
    ax.text(9.3, 6.72, "② คู่แปลงลาปลาซที่ต้องจำ", ha="center", va="top",
            fontsize=12.5, fontweight="bold", color=C_GREEN)
    pairs = [
        (r"$\delta(t)$",            r"$1$",                       "ทุก s"),
        (r"$u(t)$",                 r"$\dfrac{1}{s}$",            r"$\mathrm{Re}\{s\}>0$"),
        (r"$e^{at}u(t)$",           r"$\dfrac{1}{s-a}$",          r"$\mathrm{Re}\{s\}>a$"),
        (r"$-e^{at}u(-t)$",         r"$\dfrac{1}{s-a}$",          r"$\mathrm{Re}\{s\}<a$"),
    ]
    ax.text(7.35, 6.15, "f(t)", fontsize=11.5, fontweight="bold", ha="center")
    ax.text(9.35, 6.15, "F(s)", fontsize=11.5, fontweight="bold", ha="center")
    ax.text(11.3, 6.15, "ROC", fontsize=11.5, fontweight="bold", ha="center")
    ax.plot([6.6, 12.0], [5.95, 5.95], color=C_GREEN, linewidth=1.4)
    yy = 5.55
    for a, b, c in pairs:
        col = C_RED if "e^{at}u(t)" in a else "#222"
        w = "bold" if "e^{at}u(t)" in a else "normal"
        ax.text(7.35, yy, a, fontsize=13, ha="center", color=col)
        ax.text(9.35, yy, b, fontsize=13, ha="center", color=col)
        ax.text(11.3, yy, c, fontsize=10.5, ha="center", color=col)
        yy -= 0.52
    ax.text(9.3, 3.78, "แถวสีแดง = ตัวที่เราจะใช้ในข้อนี้ (a = 1)",
            ha="center", fontsize=10.5, color=C_RED, style="italic")

    # กล่องล่าง : นิยาม impulse response
    ax.add_patch(FancyBboxPatch((0.3, 0.35), 11.9, 2.9,
                                boxstyle="round,pad=0.1,rounding_size=0.15",
                                edgecolor=C_PURPLE, facecolor="#f4ecf7", linewidth=2))
    ax.text(6.25, 3.08, "③ ทำไม Impulse Response จึงสำคัญ ?", ha="center", va="top",
            fontsize=12.5, fontweight="bold", color=C_PURPLE)
    ax.text(6.25, 2.35,
            r"$x(t)=\delta(t)\ \Rightarrow\ X(s)=1\ \Rightarrow\ Y(s)=H(s)\cdot 1=H(s)"
            r"\ \Rightarrow\ y(t)=h(t)$",
            ha="center", va="center", fontsize=14)
    ax.text(6.25, 1.62,
            "แปลว่า : ผลตอบสนองอิมพัลส์ คือ 'ลายนิ้วมือ' ของระบบ — รู้ h(t) ตัวเดียว ทำนายเอาต์พุตของอินพุตใดก็ได้",
            ha="center", va="center", fontsize=11.5, color="#333")
    ax.text(6.25, 0.95,
            r"$y(t)=x(t)*h(t)=\int_{-\infty}^{\infty}x(\tau)h(t-\tau)\,d\tau"
            r"\qquad\Longleftrightarrow\qquad Y(s)=X(s)H(s)$",
            ha="center", va="center", fontsize=13.5, color=C_PURPLE)
    ax.text(6.25, 0.5, "convolution ในเวลา  ⟷  การคูณธรรมดาในโดเมน s  (นี่คือเหตุผลที่เราใช้ Laplace)",
            ha="center", va="center", fontsize=10.5, color=C_GRAY, style="italic")
    save(fig, "fig02_tools.png")


# =========================================================
# FIG 3 : การแยกตัวประกอบ + Rational Root Theorem
# =========================================================
def fig3_factoring():
    fig, ax = plt.subplots(figsize=(12.5, 8.6))
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 8.6); ax.axis("off")
    ax.text(6.25, 8.42, "หัวใจของข้อนี้ : แยกตัวประกอบ $s^3+s-2$ ทีละขั้น",
            ha="center", va="top", fontsize=16, fontweight="bold", color=C_BLUE)

    # STEP A
    ax.add_patch(FancyBboxPatch((0.3, 5.45), 11.9, 2.45,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                edgecolor=C_BLUE, facecolor=C_LIGHT, linewidth=2))
    ax.text(0.6, 7.72, "ขั้น A : หารากตรรกยะด้วย Rational Root Theorem",
            fontsize=12.5, fontweight="bold", color=C_BLUE, va="top")
    ax.text(0.6, 6.78, "รากตรรกยะที่เป็นไปได้  =  ± (ตัวประกอบของค่าคงที่ 2) / (ตัวประกอบของสัมประสิทธิ์นำ 1)",
            fontsize=12, va="top")
    ax.text(0.6, 6.34, r"$=\ \pm\dfrac{1,\,2}{1}\ =\ \{\,\pm1,\ \pm2\,\}$",
            fontsize=13.5, va="top")
    ax.text(0.6, 5.72, r"ทดลอง $s=1$ :  $(1)^3+(1)-2=1+1-2=0$  จึงได้ $s=1$ เป็นราก  $\Rightarrow$  $(s-1)$ เป็นตัวประกอบ",
            fontsize=12.5, va="top", color=C_RED, fontweight="bold")

    # STEP B : synthetic division
    ax.add_patch(FancyBboxPatch((0.3, 2.55), 5.9, 2.65,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                edgecolor=C_ORANGE, facecolor="#fef5e7", linewidth=2))
    ax.text(3.25, 5.02, "ขั้น B : หารสังเคราะห์ (Synthetic Division) ด้วย s = 1",
            fontsize=12, fontweight="bold", color=C_ORANGE, ha="center", va="top")
    ax.text(3.25, 4.55, "เขียนสัมประสิทธิ์ให้ครบทุกอันดับ (อันดับ 2 หายไป → ใส่ 0)",
            fontsize=10, ha="center", va="top", color="#333")
    # ตารางหารสังเคราะห์
    cols = [1.35, 2.35, 3.35, 4.35]
    hdr = [r"$s^3$", r"$s^2$", r"$s^1$", r"$s^0$"]
    row1 = ["1", "0", "1", "-2"]
    row2 = ["", "1", "1", "2"]
    row3 = ["1", "1", "2", "0"]
    for c, h in zip(cols, hdr):
        ax.text(c, 4.14, h, fontsize=11, ha="center", color=C_GRAY)
    for c, v in zip(cols, row1):
        ax.text(c, 3.78, v, fontsize=13.5, ha="center", fontweight="bold")
    ax.text(0.75, 3.78, "1 ⌋", fontsize=13.5, ha="center", color=C_ORANGE, fontweight="bold")
    for c, v in zip(cols, row2):
        if v:
            ax.text(c, 3.42, "+ " + v, fontsize=12, ha="center", color=C_ORANGE)
    ax.plot([0.95, 4.75], [3.20, 3.20], color=C_ORANGE, linewidth=1.6)
    for c, v in zip(cols, row3):
        col = C_GREEN if v == "0" else C_BLUE
        ax.text(c, 2.92, v, fontsize=14, ha="center", fontweight="bold", color=col)
    ax.text(3.25, 2.62, "เศษเหลือ = 0 ถูกต้อง   ผลหาร = " r"$s^2+s+2$",
            fontsize=11.5, ha="center", color=C_GREEN, fontweight="bold")

    # STEP C : quadratic roots
    ax.add_patch(FancyBboxPatch((6.55, 2.55), 5.65, 2.65,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                edgecolor=C_PURPLE, facecolor="#f4ecf7", linewidth=2))
    ax.text(9.38, 5.02, "ขั้น C : รากของ $s^2+s+2$ (สูตรกำลังสอง)",
            fontsize=12, fontweight="bold", color=C_PURPLE, ha="center", va="top")
    ax.text(9.38, 4.42, r"$s=\dfrac{-1\pm\sqrt{1^2-4(1)(2)}}{2}=\dfrac{-1\pm\sqrt{-7}}{2}$",
            fontsize=13.5, ha="center", va="center")
    ax.text(9.38, 3.62, r"$s=-\dfrac{1}{2}\pm j\dfrac{\sqrt{7}}{2}\approx-0.5\pm j1.323$",
            fontsize=13.5, ha="center", va="center", color=C_PURPLE, fontweight="bold")
    ax.text(9.38, 2.92, "discriminant < 0 → รากเชิงซ้อนคู่สังยุค\n(แยกในจำนวนจริงต่อไม่ได้ = irreducible)",
            fontsize=10.5, ha="center", va="center", color="#333")

    # ผลสรุป
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 11.9, 2.0,
                                boxstyle="round,pad=0.08,rounding_size=0.12",
                                edgecolor=C_RED, facecolor="#fdedec", linewidth=2.4))
    ax.text(6.25, 2.12, "ผลลัพธ์ : ตัวส่วนแยกได้เป็น", fontsize=12.5,
            fontweight="bold", color=C_RED, ha="center", va="top")
    ax.text(6.25, 1.62, r"$s^3+s-2=(s-1)\,(s^2+s+2)$",
            fontsize=17, ha="center", va="center")
    ax.text(6.25, 1.12, "↑ ตัวประกอบนี้ตรงกับตัวเศษเป๊ะ !", fontsize=11,
            ha="center", va="center", color=C_RED, fontweight="bold")
    ax.text(4.9, 0.62, r"$H(s)=\dfrac{s^2+s+2}{(s-1)(s^2+s+2)}$",
            fontsize=19, ha="center", va="center", color=C_RED)
    ax.text(7.4, 0.62, r"$=$", fontsize=19, ha="center", va="center", color=C_RED)
    ax.text(8.9, 0.62, r"$\dfrac{1}{s-1}$", fontsize=26, ha="center", va="center",
            color=C_RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor=C_RED, linewidth=2.5))
    save(fig, "fig03_factoring.png")


# =========================================================
# FIG 4 : Pole-Zero plot ก่อน/หลังตัดทอน
# =========================================================
def fig4_polezero():
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
    poles = [1.0, -0.5 + 1.3228756555j, -0.5 - 1.3228756555j]
    zeros = [-0.5 + 1.3228756555j, -0.5 - 1.3228756555j]

    for k, ax in enumerate(axes):
        ax.axhline(0, color="#aab7b8", linewidth=1.1)
        ax.axvline(0, color="#aab7b8", linewidth=1.1)
        ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.4, 2.4)
        ax.set_aspect("equal")
        ax.grid(True, linestyle=":", alpha=0.45)
        ax.set_xlabel(r"$\mathrm{Re}\{s\}\ (\sigma)$", fontsize=12)
        ax.set_ylabel(r"$\mathrm{Im}\{s\}\ (j\omega)$", fontsize=12)
        # แรเงา ROC : Re{s} > 1
        ax.add_patch(Rectangle((1.0, -2.4), 1.6, 4.8, facecolor=C_GREEN,
                               alpha=0.13, edgecolor="none"))
        ax.axvline(1.0, color=C_GREEN, linestyle="--", linewidth=1.8)
        ax.text(1.85, -2.05, "ROC\nRe{s} > 1", fontsize=10.5, color=C_GREEN,
                ha="center", fontweight="bold")
        # แรเงาครึ่งขวา (unstable region) เบา ๆ
        ax.add_patch(Rectangle((0, -2.4), 2.6, 4.8, facecolor=C_RED,
                               alpha=0.045, edgecolor="none"))

        if k == 0:
            ax.set_title("ก่อนตัดทอน : $H(s)=\\dfrac{s^2+s+2}{s^3+s-2}$\n(3 โพล , 2 ซีโร)",
                         fontsize=13, fontweight="bold", color=C_BLUE, pad=12)
            P, Z = poles, zeros
        else:
            ax.set_title("หลังตัดทอน : $H(s)=\\dfrac{1}{s-1}$\n(เหลือ 1 โพล , ไม่มีซีโรจำกัด)",
                         fontsize=13, fontweight="bold", color=C_RED, pad=12)
            P, Z = [1.0], []
            # แสดงตำแหน่งที่ถูกตัดเป็นสีจาง
            for z in zeros:
                ax.plot(z.real, z.imag, "o", markersize=15, markerfacecolor="none",
                        markeredgecolor="#bdc3c7", markeredgewidth=1.6, linestyle="")
                ax.plot(z.real, z.imag, "x", markersize=13, color="#bdc3c7",
                        markeredgewidth=2.2)
            ax.text(-1.95, 1.85, "จุดจางคือ pole/zero\nที่หักล้างกันไป", fontsize=9.5,
                    color="#7f8c8d", ha="left", style="italic")

        for p in P:
            ax.plot(np.real(p), np.imag(p), "x", markersize=16, color=C_RED,
                    markeredgewidth=3.4, zorder=5)
        for z in Z:
            ax.plot(np.real(z), np.imag(z), "o", markersize=14, markerfacecolor="none",
                    markeredgecolor=C_BLUE, markeredgewidth=2.8, zorder=5)

        ax.annotate("โพล s = 1\n(ครึ่งขวา ไม่เสถียร)", xy=(1.0, 0), xytext=(0.55, 1.68),
                    fontsize=10, color=C_RED, fontweight="bold", ha="center",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                              edgecolor="none", alpha=0.88),
                    arrowprops=dict(arrowstyle="->", color=C_RED, linewidth=1.5))
        if k == 0:
            ax.annotate(r"$-\frac{1}{2}\pm j\frac{\sqrt{7}}{2}$" + "\n(โพลทับซีโรพอดี)",
                        xy=(-0.5, 1.323), xytext=(-2.42, 1.62),
                        fontsize=9.5, color=C_PURPLE, fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                                  edgecolor="none", alpha=0.88),
                        arrowprops=dict(arrowstyle="->", color=C_PURPLE, linewidth=1.4))

    fig.suptitle("แผนภาพโพล-ซีโร : ระบบอันดับ 3 ยุบเหลืออันดับ 1",
                 fontsize=16, fontweight="bold", color=C_BLUE, y=0.99)
    fig.tight_layout(rect=[0, 0.085, 1, 0.95])
    fig.text(0.5, 0.028, "× = โพล (pole, รากตัวส่วน)   ○ = ซีโร (zero, รากตัวเศษ)   "
                         "แถบเขียว = ROC ของระบบคอซัล   แถบแดงจาง = ครึ่งขวาระนาบ s (ไม่เสถียร)",
             ha="center", fontsize=10.5, color=C_GRAY)
    save(fig, "fig04_polezero.png")


# =========================================================
# FIG 5 : กราฟ h(t) = e^t u(t)
# =========================================================
def fig5_impulse_response():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))

    # ซ้าย : สเกลเชิงเส้น
    ax = axes[0]
    t1 = np.linspace(-1.5, 0, 200)
    t2 = np.linspace(0, 3.0, 400)
    ax.plot(t1, np.zeros_like(t1), color=C_GREEN, linewidth=3)
    ax.plot(t2, np.exp(t2), color=C_GREEN, linewidth=3, label=r"$h(t)=e^{t}u(t)$")
    ax.plot([0], [1], "o", color=C_GREEN, markersize=9, zorder=5)
    ax.fill_between(t2, 0, np.exp(t2), color=C_GREEN, alpha=0.12)
    ax.axhline(0, color="#95a5a6", linewidth=1)
    ax.axvline(0, color="#95a5a6", linewidth=1, linestyle="--")
    ax.set_xlim(-1.5, 3.0); ax.set_ylim(-1.5, 21)
    ax.set_xlabel("เวลา t (วินาที)", fontsize=12)
    ax.set_ylabel("h(t)", fontsize=12)
    ax.set_title("ผลตอบสนองอิมพัลส์ (สเกลเชิงเส้น)", fontsize=13,
                 fontweight="bold", color=C_GREEN, pad=10)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(fontsize=12, loc="upper left")
    ax.annotate("t < 0 : h(t) = 0\n(คอซัล — ไม่ตอบสนองก่อนถูกกระตุ้น)",
                xy=(-0.75, 0), xytext=(-1.45, 8.5), fontsize=10, color=C_BLUE,
                arrowprops=dict(arrowstyle="->", color=C_BLUE, linewidth=1.4))
    ax.annotate("h(0⁺) = 1", xy=(0, 1), xytext=(0.35, 4.2), fontsize=10.5,
                color=C_RED, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_RED, linewidth=1.4))
    ax.annotate("โตแบบเอกซ์โพเนนเชียล → ไม่เสถียร (BIBO)",
                xy=(2.55, np.exp(2.55)), xytext=(0.42, 16.5), fontsize=10.5,
                color=C_RED, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_RED, linewidth=1.4))

    # ขวา : สเกลลอการิทึม
    ax = axes[1]
    tt = np.linspace(0, 6, 600)
    ax.semilogy(tt, np.exp(tt), color=C_RED, linewidth=3)
    ax.set_xlabel("เวลา t (วินาที)", fontsize=12)
    ax.set_ylabel("h(t)  (สเกล log)", fontsize=12)
    ax.set_title("สเกลลอการิทึม : เส้นตรง = เอกซ์โพเนนเชียลแท้",
                 fontsize=13, fontweight="bold", color=C_RED, pad=10)
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    for tv in [1, 2, 3, 4, 5]:
        ax.plot([tv], [np.exp(tv)], "o", color=C_BLUE, markersize=7, zorder=5)
        ax.annotate(f"t={tv}\n{np.exp(tv):.1f}", xy=(tv, np.exp(tv)),
                    xytext=(tv - 0.05, np.exp(tv) * 1.9), fontsize=9,
                    color=C_BLUE, ha="center")
    ax.text(0.35, 90, "ทุก 1 วินาที ค่าโตขึ้น e ≈ 2.718 เท่า\nτ = 1 s (ค่าคงตัวเวลา)",
            fontsize=10.5, color=C_BLUE, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#eaf2f8",
                      edgecolor=C_BLUE, alpha=0.9))
    fig.suptitle(r"คำตอบ : $h(t)=e^{t}u(t)$", fontsize=17, fontweight="bold",
                 color=C_GREEN, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "fig05_impulse_response.png")


# =========================================================
# FIG 6 : Block diagram + physical meaning
# =========================================================
def fig6_block():
    fig, ax = plt.subplots(figsize=(13, 7.0))
    ax.set_xlim(0, 13); ax.set_ylim(0, 7.0); ax.axis("off")
    ax.text(6.5, 6.85, "มุมมองระบบ : จาก ODE → บล็อกไดอะแกรม → ความหมายทางกายภาพ",
            ha="center", va="top", fontsize=15.5, fontweight="bold", color=C_BLUE)

    # --- แถวบน : ระบบเต็ม (อันดับ 3)
    ax.text(0.35, 5.95, "① โครงสร้างจริงของระบบ (อันดับ 3)", fontsize=12.5,
            fontweight="bold", color=C_BLUE, va="top")
    y0 = 4.7
    ax.add_patch(FancyArrowPatch((0.5, y0), (2.0, y0), arrowstyle="-|>",
                                 mutation_scale=18, linewidth=2, color="#34495e"))
    ax.text(1.15, y0 + 0.22, r"$x(t)=\delta(t)$", fontsize=12, ha="center", color=C_BLUE)
    ax.add_patch(FancyBboxPatch((2.05, y0 - 0.62), 3.1, 1.24,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                edgecolor=C_BLUE, facecolor=C_LIGHT, linewidth=2))
    ax.text(3.6, y0 + 0.18, "ตัวเศษ (ซีโร)", fontsize=10, ha="center", color=C_GRAY)
    ax.text(3.6, y0 - 0.22, r"$s^2+s+2$", fontsize=14, ha="center", color=C_BLUE)
    ax.add_patch(FancyArrowPatch((5.2, y0), (6.2, y0), arrowstyle="-|>",
                                 mutation_scale=18, linewidth=2, color="#34495e"))
    ax.add_patch(FancyBboxPatch((6.25, y0 - 0.62), 3.55, 1.24,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                edgecolor=C_PURPLE, facecolor="#f4ecf7", linewidth=2))
    ax.text(8.0, y0 + 0.18, "ตัวส่วน (โพล)", fontsize=10, ha="center", color=C_GRAY)
    ax.text(8.0, y0 - 0.22, r"$\dfrac{1}{(s-1)(s^2+s+2)}$", fontsize=13.5,
            ha="center", color=C_PURPLE)
    ax.add_patch(FancyArrowPatch((9.85, y0), (11.3, y0), arrowstyle="-|>",
                                 mutation_scale=18, linewidth=2, color="#34495e"))
    ax.text(10.9, y0 + 0.25, r"$y(t)=h(t)$", fontsize=12, ha="center", color=C_GREEN)
    ax.text(6.5, 3.72, "โหมด $e^{-t/2}\\cos(\\frac{\\sqrt{7}}{2}t)$ ที่ตัวส่วนสร้าง ถูกตัวเศษ 'ลบล้าง' พอดี",
            fontsize=11, ha="center", color=C_RED, style="italic")

    # --- แถวล่าง : ระบบสมมูล
    ax.text(0.35, 3.25, "② ระบบสมมูลที่มองจากภายนอก (input-output equivalent)",
            fontsize=12.5, fontweight="bold", color=C_RED, va="top")
    y1 = 2.05
    ax.add_patch(FancyArrowPatch((0.5, y1), (2.6, y1), arrowstyle="-|>",
                                 mutation_scale=18, linewidth=2, color="#34495e"))
    ax.text(1.5, y1 + 0.25, r"$\delta(t)$", fontsize=13, ha="center", color=C_BLUE)
    ax.add_patch(FancyBboxPatch((2.65, y1 - 0.72), 3.6, 1.44,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                edgecolor=C_RED, facecolor="#fdedec", linewidth=2.4))
    ax.text(4.45, y1 + 0.28, "ระบบอันดับ 1", fontsize=10.5, ha="center", color=C_GRAY)
    ax.text(4.45, y1 - 0.22, r"$H(s)=\dfrac{1}{s-1}$", fontsize=16, ha="center", color=C_RED)
    ax.add_patch(FancyArrowPatch((6.3, y1), (8.4, y1), arrowstyle="-|>",
                                 mutation_scale=18, linewidth=2, color="#34495e"))
    ax.add_patch(FancyBboxPatch((8.45, y1 - 0.72), 3.9, 1.44,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                edgecolor=C_GREEN, facecolor="#eafaf1", linewidth=2.4))
    ax.text(10.4, y1 + 0.28, "ผลตอบสนองอิมพัลส์", fontsize=10.5, ha="center", color=C_GRAY)
    ax.text(10.4, y1 - 0.22, r"$h(t)=e^{t}u(t)$", fontsize=16, ha="center", color=C_GREEN)

    # กล่องเตือน
    ax.add_patch(FancyBboxPatch((0.4, 0.25), 12.2, 1.05,
                                boxstyle="round,pad=0.06,rounding_size=0.1",
                                edgecolor=C_ORANGE, facecolor="#fef5e7", linewidth=2))
    ax.text(6.5, 1.12, "⚠️ ข้อควรระวังเชิงวิศวกรรม", fontsize=11.5, fontweight="bold",
            color=C_ORANGE, ha="center", va="top")
    ax.text(6.5, 0.6, "การหักล้างเกิดใน 'ผลตอบสนองสภาวะศูนย์' เท่านั้น — ถ้าเงื่อนไขเริ่มต้นไม่เป็นศูนย์ "
                      "โหมด $e^{-t/2}\\cos(\\frac{\\sqrt{7}}{2}t)$ จะโผล่กลับมาเสมอ",
            fontsize=11, ha="center", va="center", color="#333")
    save(fig, "fig06_block.png")


# =========================================================
# FIG 7 : ตรวจสอบคำตอบเชิงตัวเลข
# =========================================================
def fig7_verify():
    fig, axes = plt.subplots(2, 2, figsize=(13, 8.6))

    # (a) แทน h(t)=e^t เข้า LHS ของ ODE เทียบ RHS (สำหรับ t>0, x=0)
    ax = axes[0, 0]
    t = np.linspace(0.01, 2.5, 400)
    h = np.exp(t)
    lhs = h + h - 2 * h   # y'''+y'-2y = e^t + e^t - 2e^t = 0
    ax.plot(t, np.zeros_like(t), color=C_BLUE, linewidth=6, alpha=0.35,
            label="RHS = 0  (t > 0, x(t)=0)")
    ax.plot(t, lhs, "--", color=C_RED, linewidth=2.4,
            label=r"LHS $=h'''+h'-2h$")
    ax.set_title("(ก) ตรวจสอบ ODE สำหรับ t > 0", fontsize=12.5,
                 fontweight="bold", color=C_BLUE)
    ax.set_xlabel("t (s)"); ax.set_ylabel("ค่า")
    ax.set_ylim(-1, 1); ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(fontsize=10, loc="upper right")
    ax.text(1.25, -0.62, r"$e^t+e^t-2e^t\equiv 0$" "   สอดคล้องทุก t (ถูกต้อง)",
            fontsize=11.5, ha="center", color=C_GREEN, fontweight="bold")

    # (b) เปรียบเทียบ h(t) กับ inverse Laplace เชิงตัวเลข (สรุปด้วยการเทียบ 2 เส้น)
    ax = axes[0, 1]
    tt = np.linspace(0, 3, 300)
    exact = np.exp(tt)
    # จำลอง state-space ของ H(s)=(s^2+s+2)/(s^3+s-2) ด้วย RK4 (controllable canonical form)
    def simulate():
        # z''' = -z' + 2z + delta-driven ; ใช้ IC จาก impulse: z(0)=z'(0)=0, z''(0)=1
        dt = 3.0 / 6000
        n = 6001
        z = np.zeros(n); z1 = np.zeros(n); z2 = np.zeros(n)
        z[0], z1[0], z2[0] = 0.0, 0.0, 1.0
        for i in range(n - 1):
            z3 = -z1[i] + 2 * z[i]         # z''' = -z' + 2z
            z2[i+1] = z2[i] + dt * z3
            z1[i+1] = z1[i] + dt * z2[i]
            z[i+1]  = z[i]  + dt * z1[i]
        ts = np.linspace(0, 3, n)
        y = z2 + z1 + 2 * z                # y = z'' + z' + 2z
        return ts, y
    ts, ysim = simulate()
    ax.plot(ts, ysim, color=C_ORANGE, linewidth=4, alpha=0.7,
            label="จำลองระบบอันดับ 3 (เชิงตัวเลข)")
    ax.plot(tt, exact, "--", color=C_GREEN, linewidth=2.4, label=r"$e^{t}$ (คำตอบวิเคราะห์)")
    ax.set_title("(ข) จำลองระบบอันดับ 3 เทียบคำตอบ $e^t$", fontsize=12.5,
                 fontweight="bold", color=C_ORANGE)
    ax.set_xlabel("t (s)"); ax.set_ylabel("h(t)")
    ax.grid(True, linestyle=":", alpha=0.5); ax.legend(fontsize=10, loc="upper left")
    err = np.max(np.abs(np.interp(tt, ts, ysim) - exact) / exact)
    ax.text(0.12, exact.max() * 0.72,
            f"ค่าคลาดเคลื่อนสัมพัทธ์สูงสุด ≈ {err:.2e}\n→ ทับกันสนิท ✓",
            fontsize=10.5, color=C_GREEN, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#eafaf1",
                      edgecolor=C_GREEN, alpha=0.95))

    # (c) โหมดธรรมชาติทั้งสาม
    ax = axes[1, 0]
    tm = np.linspace(0, 4, 500)
    ax.plot(tm, np.exp(tm), color=C_RED, linewidth=3, label=r"โหมด $e^{t}$ (โพล $s=1$) — เหลืออยู่")
    ax.plot(tm, np.exp(-0.5 * tm) * np.cos(np.sqrt(7) / 2 * tm), color="#bdc3c7",
            linewidth=2.4, linestyle="--",
            label=r"โหมด $e^{-t/2}\cos(\frac{\sqrt{7}}{2}t)$ — ถูกตัด")
    ax.plot(tm, np.exp(-0.5 * tm) * np.sin(np.sqrt(7) / 2 * tm), color="#d5dbdb",
            linewidth=2.4, linestyle=":",
            label=r"โหมด $e^{-t/2}\sin(\frac{\sqrt{7}}{2}t)$ — ถูกตัด")
    ax.set_yscale("symlog", linthresh=1)
    ax.set_title("(ค) โหมดธรรมชาติ 3 โหมดของระบบอันดับ 3", fontsize=12.5,
                 fontweight="bold", color=C_PURPLE)
    ax.set_xlabel("t (s)"); ax.set_ylabel("ขนาด (symlog)")
    ax.grid(True, linestyle=":", alpha=0.5); ax.legend(fontsize=9.5, loc="upper left")
    ax.axhline(0, color="#95a5a6", linewidth=1)

    # (d) ตารางสรุป
    ax = axes[1, 1]; ax.axis("off")
    ax.text(0.5, 0.97, "(ง) สรุปคุณสมบัติของระบบ", fontsize=12.5, fontweight="bold",
            color=C_BLUE, ha="center", va="top", transform=ax.transAxes)
    rows = [
        ("อันดับของ ODE", "3 (แต่พฤติกรรม I/O = อันดับ 1)", C_BLUE),
        ("โพลของ H(s) ก่อนตัด", r"$1,\ -\frac{1}{2}\pm j\frac{\sqrt{7}}{2}$", C_PURPLE),
        ("ซีโรของ H(s)", r"$-\frac{1}{2}\pm j\frac{\sqrt{7}}{2}$", C_PURPLE),
        ("H(s) หลังตัดทอน", r"$\dfrac{1}{s-1}$", C_RED),
        ("ROC (คอซัล)", r"$\mathrm{Re}\{s\}>1$", C_GREEN),
        ("h(t)", r"$e^{t}u(t)$", C_GREEN),
        ("คอซัล ?", "ใช่ (h(t)=0 เมื่อ t<0)", C_GREEN),
        ("เสถียร BIBO ?", r"ไม่ ($\int|h|dt\to\infty$, โพลครึ่งขวา)", C_RED),
    ]
    yy = 0.86
    for label, val, col in rows:
        ax.text(0.03, yy, label, fontsize=11, transform=ax.transAxes,
                va="center", color="#333")
        ax.text(0.55, yy, val, fontsize=12, transform=ax.transAxes,
                va="center", color=col, fontweight="bold")
        ax.plot([0.02, 0.98], [yy - 0.045, yy - 0.045], transform=ax.transAxes,
                color="#e5e8e8", linewidth=1)
        yy -= 0.105

    fig.suptitle("การตรวจสอบคำตอบ 4 วิธี : วิเคราะห์ • เชิงตัวเลข • โหมด • คุณสมบัติ",
                 fontsize=15.5, fontweight="bold", color=C_BLUE, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    save(fig, "fig07_verify.png")


# =========================================================
# FIG 8 : กับดักที่พบบ่อย
# =========================================================
def fig8_pitfalls():
    fig, ax = plt.subplots(figsize=(12.6, 8.2))
    ax.set_xlim(0, 12.6); ax.set_ylim(0, 8.2); ax.axis("off")
    ax.text(6.3, 8.0, "กับดัก 6 ข้อที่นิสิตพลาดบ่อยในโจทย์นี้",
            ha="center", va="top", fontsize=16, fontweight="bold", color=C_RED)

    items = [
        ("① ลืมว่าอันดับ 2 ของ y หายไป",
         "ตอนหารสังเคราะห์ต้องเขียน 1, 0, 1, −2\nถ้าเขียน 1, 1, −2 จะหารผิดทันที", C_ORANGE),
        ("② สับสนเครื่องหมาย −2y กับ +2x",
         "ตัวส่วนคือ $s^3+s-2$ (ลบ)\nตัวเศษคือ $s^2+s+2$ (บวก)", C_RED),
        ("③ ไม่แยกตัวประกอบ แล้วรีบทำ PFE",
         "เสียเวลาแตกเศษส่วนย่อย 3 พจน์\nทั้งที่ตัดทอนแล้วเหลือพจน์เดียว", C_PURPLE),
        ("④ ลืมใส่ u(t)",
         "ตอบ $e^t$ เฉย ๆ ไม่ถูก — ต้องมี $u(t)$\nเพื่อระบุความเป็นคอซัล", C_BLUE),
        ("⑤ สรุปว่าระบบเสถียรเพราะตัดโพลแล้ว",
         "โพล $s=1$ ยังอยู่ $\\Rightarrow$ ยังไม่เสถียร\nและโหมดที่ตัดไปยังซ่อนอยู่ในระบบจริง", C_RED),
        ("⑥ เลือก ROC ผิดข้าง",
         "$\\mathrm{Re}\\{s\\}<1$ จะได้ $-e^tu(-t)$ (anti-causal)\nโจทย์ IC=0 $\\Rightarrow$ ต้องเลือกคอซัล", C_GREEN),
    ]
    W, H = 5.9, 2.15
    positions = [(0.3, 5.4), (6.4, 5.4), (0.3, 2.95), (6.4, 2.95), (0.3, 0.5), (6.4, 0.5)]
    for (x, y), (title, body, col) in zip(positions, items):
        ax.add_patch(FancyBboxPatch((x, y), W, H,
                                    boxstyle="round,pad=0.08,rounding_size=0.12",
                                    edgecolor=col, facecolor=col, alpha=0.09, linewidth=2))
        ax.text(x + 0.22, y + H - 0.28, title, fontsize=12, fontweight="bold",
                color=col, va="top")
        ax.text(x + 0.22, y + H - 0.95, body, fontsize=11, color="#333", va="top")
    save(fig, "fig08_pitfalls.png")


if __name__ == "__main__":
    fig1_roadmap()
    fig2_laplace_table()
    fig3_factoring()
    fig4_polezero()
    fig5_impulse_response()
    fig6_block()
    fig7_verify()
    fig8_pitfalls()
    print("\nDONE - ทุกภาพถูกสร้างเรียบร้อย")
