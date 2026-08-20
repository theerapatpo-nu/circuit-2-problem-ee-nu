#!/usr/bin/env python3
"""Solve the oral-exam battery circuit and identify its voltage model.

The script intentionally separates *identifiable* parameters from parameters
that cannot be uniquely recovered from a single constant-current experiment.
For this dataset, KVL contains Eo and Ri only as C0 = Eo - I*Ri.  Therefore Ri
must come from an independent pulse/impedance test (or be supplied with --ri),
after which Eo = C0 + I*Ri.

Examples
--------
python solvecircuit.py
python solvecircuit.py --data ../data303212qz02.xls --ri 0.20
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


RL_OHM = 10.0
TN_SECOND = 3600.0
DEFAULT_ASSUMED_RI_OHM = 0.20


@dataclass(frozen=True)
class FitResult:
    """Numerical result and the identifiability statement."""

    c0_volt: float
    eo_volt_conditional: float
    k_volt_per_coulomb: float
    aa_volt: float
    ba_per_coulomb: float
    ab_volt: float
    bb_per_coulomb: float
    ri_ohm_assumed: float
    qn_coulomb: float
    current_ampere: float
    sse_volt2: float
    rmse_volt: float
    max_abs_error_volt: float


def parse_markdown_table(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Read the three numeric columns from data303212qz02.md."""

    numeric_token = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    number = re.compile(
        rf"^\s*\|\s*{numeric_token}\s*\|\s*{numeric_token}\s*\|"
        rf"\s*{numeric_token}\s*\|\s*$"
    )
    rows: list[tuple[float, float, float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = number.match(line)
        if match:
            rows.append(tuple(float(value) for value in match.groups()))
    if not rows:
        raise ValueError(f"No numeric rows were found in {path}")
    array = np.asarray(rows, dtype=float)
    return array[:, 0], array[:, 1], array[:, 2]


def read_data(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, Path]:
    """Read .md directly, or .xls through pandas with a safe .md fallback."""

    if path.suffix.lower() == ".md":
        t, v, i_s = parse_markdown_table(path)
        return t, v, i_s, path

    if path.suffix.lower() in {".xls", ".xlsx"}:
        try:
            import pandas as pd  # Optional; old .xls also needs xlrd.

            frame = pd.read_excel(path)
            values = frame.iloc[:, :3].to_numpy(dtype=float)
            return values[:, 0], values[:, 1], values[:, 2], path
        except Exception as exc:  # pragma: no cover - depends on local Excel stack
            markdown = path.with_suffix(".md")
            if markdown.exists():
                print(
                    f"[note] Excel reader unavailable ({exc.__class__.__name__}); "
                    f"using {markdown.name} instead."
                )
                t, v, i_s = parse_markdown_table(markdown)
                return t, v, i_s, markdown
            raise RuntimeError(
                "Reading .xls needs pandas and xlrd. Install them or use the .md file."
            ) from exc

    raise ValueError(f"Unsupported data file: {path}")


def cumulative_trapezoid(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Cumulative trapezoidal integral with q(0)=0, using only NumPy."""

    if len(x) != len(y) or len(x) < 2:
        raise ValueError("x and y must have the same length and at least two samples")
    if np.any(np.diff(x) <= 0):
        raise ValueError("Time samples must be strictly increasing")
    areas = 0.5 * (y[:-1] + y[1:]) * np.diff(x)
    return np.concatenate(([0.0], np.cumsum(areas)))


def battery_terminal_voltage(
    q: np.ndarray,
    current: np.ndarray,
    qn: float,
    eo: float,
    k: float,
    aa: float,
    ba: float,
    ab: float,
    bb: float,
    ri: float,
) -> np.ndarray:
    """Return v = vs - i*Ri for the model stated in the problem."""

    return (
        eo
        - k * q
        + aa * np.exp(-ba * q)
        - ab * np.exp(-bb * (qn - q))
        - current * ri
    )


def _variable_projection(
    log_rates: Iterable[float], q: np.ndarray, remaining_q: np.ndarray, v: np.ndarray
) -> tuple[float, np.ndarray]:
    """For fixed Ba,Bb, solve C0,K,Aa,Ab by linear least squares."""

    ba, bb = np.exp(np.asarray(tuple(log_rates), dtype=float))
    design = np.column_stack(
        (
            np.ones_like(q),
            -q,
            np.exp(-ba * q),
            -np.exp(-bb * remaining_q),
        )
    )
    coefficients, *_ = np.linalg.lstsq(design, v, rcond=None)
    residual = design @ coefficients - v
    return float(residual @ residual), coefficients


def identify_parameters(
    q: np.ndarray,
    v: np.ndarray,
    current: np.ndarray,
    qn: float,
    assumed_ri: float,
    seed: int = 303212,
) -> tuple[FitResult, np.ndarray]:
    """Fit the six identifiable curve parameters, then condition Eo on Ri.

    A two-rate global search plus variable projection avoids the poor local
    minimum reached by a naive seven-parameter fit.  Bounded least_squares then
    polishes all six identifiable values simultaneously.
    """

    from scipy.optimize import differential_evolution, least_squares

    remaining_q = qn - q
    if np.any(remaining_q < 0):
        raise ValueError("Observed q exceeds Qn; check tn or the current sign")

    log_bounds = [(math.log(1e-5), math.log(0.1))] * 2

    def projected_sse(log_rates: np.ndarray) -> float:
        return _variable_projection(log_rates, q, remaining_q, v)[0]

    global_fit = differential_evolution(
        projected_sse,
        bounds=log_bounds,
        seed=seed,
        tol=1e-11,
        polish=True,
        workers=1,
        maxiter=800,
        popsize=24,
    )
    _, linear = _variable_projection(global_fit.x, q, remaining_q, v)
    ba0, bb0 = np.exp(global_fit.x)
    x0 = np.array([linear[0], linear[1], linear[2], ba0, linear[3], bb0])

    def residual(x: np.ndarray) -> np.ndarray:
        c0, k, aa, ba, ab, bb = x
        return c0 - k * q + aa * np.exp(-ba * q) - ab * np.exp(
            -bb * remaining_q
        ) - v

    # Bounds express the discharge-model sign convention, not a hidden prior.
    lower = np.array([0.0, 0.0, 0.0, 1e-7, 0.0, 1e-7])
    upper = np.array([10.0, 0.01, 10.0, 1.0, 5000.0, 1.0])
    polished = least_squares(
        residual,
        x0,
        bounds=(lower, upper),
        method="trf",
        x_scale="jac",
        ftol=1e-14,
        xtol=1e-14,
        gtol=1e-14,
        max_nfev=100000,
    )
    c0, k, aa, ba, ab, bb = polished.x
    mean_i = float(np.mean(current))
    eo = c0 + mean_i * assumed_ri
    fitted_v = battery_terminal_voltage(
        q, current, qn, eo, k, aa, ba, ab, bb, assumed_ri
    )
    error = fitted_v - v
    result = FitResult(
        c0_volt=float(c0),
        eo_volt_conditional=float(eo),
        k_volt_per_coulomb=float(k),
        aa_volt=float(aa),
        ba_per_coulomb=float(ba),
        ab_volt=float(ab),
        bb_per_coulomb=float(bb),
        ri_ohm_assumed=float(assumed_ri),
        qn_coulomb=float(qn),
        current_ampere=mean_i,
        sse_volt2=float(error @ error),
        rmse_volt=float(np.sqrt(np.mean(error**2))),
        max_abs_error_volt=float(np.max(np.abs(error))),
    )
    return result, fitted_v


def make_plots(
    output_dir: Path,
    t: np.ndarray,
    v: np.ndarray,
    i_s: np.ndarray,
    current: np.ndarray,
    q: np.ndarray,
    fitted_v: np.ndarray,
) -> None:
    """Create the requested signal overview and measured-vs-model figures."""

    import matplotlib.pyplot as plt

    plt.style.use("dark_background")
    colors = {"voltage": "#62d8ff", "source": "#a78bfa", "current": "#34d399", "charge": "#fbbf24", "fit": "#fb7185"}

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    fig.patch.set_facecolor("#07111f")
    fig.suptitle("Battery-circuit signals — 2,753 measured rows", fontsize=16)
    series = [
        (axes[0, 0], v, colors["voltage"], "Terminal voltage v(t)", "Voltage [V]"),
        (axes[0, 1], i_s, colors["source"], "Dependent-source current is(t)", "Current [A]"),
        (axes[1, 0], current, colors["current"], "Battery current i(t) from KCL", "Current [A]"),
        (axes[1, 1], q, colors["charge"], "Accumulated charge q(t)", "Charge [C]"),
    ]
    for axis, y, color, title, ylabel in series:
        axis.plot(t, y, color=color, linewidth=2.0)
        axis.set_title(title)
        axis.set_xlabel("Time [s]")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.18)
        axis.set_facecolor("#0b1728")
    fig.savefig(output_dir / "signals_overview.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)

    residual = fitted_v - v
    fig, axes = plt.subplots(
        2, 1, figsize=(14, 8), sharex=True, height_ratios=(3.2, 1), constrained_layout=True
    )
    fig.patch.set_facecolor("#07111f")
    axes[0].plot(t, v, color=colors["voltage"], linewidth=3.0, label="Measured v(t)")
    axes[0].plot(t, fitted_v, color=colors["fit"], linestyle="--", linewidth=1.6, label="Fitted model")
    axes[0].set_title("Terminal voltage: measurement vs nonlinear battery model")
    axes[0].set_ylabel("Voltage [V]")
    axes[0].legend(loc="best")
    axes[1].plot(t, residual * 1e6, color=colors["charge"], linewidth=1.2)
    axes[1].axhline(0.0, color="#dbeafe", linewidth=0.8, alpha=0.6)
    axes[1].set_xlabel("Time [s]")
    axes[1].set_ylabel("Error [µV]")
    for axis in axes:
        axis.grid(alpha=0.18)
        axis.set_facecolor("#0b1728")
    fig.savefig(output_dir / "voltage_fit.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


def write_outputs(
    output_dir: Path,
    t: np.ndarray,
    v: np.ndarray,
    i_s: np.ndarray,
    current: np.ndarray,
    q: np.ndarray,
    fitted_v: np.ndarray,
    result: FitResult,
    source: Path,
) -> None:
    """Save machine-readable results and all computed rows."""

    payload = asdict(result)
    payload.update(
        {
            "source_file": str(source.resolve()),
            "rows": int(len(t)),
            "identifiability": (
                "Eo and Ri are not separately identifiable at one constant current; "
                "Eo is conditional on ri_ohm_assumed."
            ),
            "family_equation": (
                f"Eo = {result.c0_volt:.15g} + "
                f"{result.current_ampere:.15g} * Ri"
            ),
        }
    )
    (output_dir / "fit_results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    matrix = np.column_stack((t, v, i_s, current, q, fitted_v, fitted_v - v))
    np.savetxt(
        output_dir / "computed_data.csv",
        matrix,
        delimiter=",",
        header="t_s,v_measured_V,is_A,i_A,q_C,v_fitted_V,residual_V",
        comments="",
        fmt="%.15g",
    )


def print_report(result: FitResult, rows: int, source: Path) -> None:
    print("=" * 76)
    print("BATTERY CIRCUIT ANALYSIS AND PARAMETER IDENTIFICATION")
    print("=" * 76)
    print(f"Data source                  : {source}")
    print(f"Rows                         : {rows}")
    print(f"i(t), mean                   : {result.current_ampere:.12f} A")
    print(f"Qn = i*3600                  : {result.qn_coulomb:.9f} C")
    print("\nIdentifiable voltage-curve parameters")
    print(f"C0 = Eo - i*Ri               : {result.c0_volt:.15f} V")
    print(f"K                            : {result.k_volt_per_coulomb:.15g} V/C")
    print(f"Aa                           : {result.aa_volt:.15g} V")
    print(f"Ba                           : {result.ba_per_coulomb:.15g} 1/C")
    print(f"Ab                           : {result.ab_volt:.15g} V")
    print(f"Bb                           : {result.bb_per_coulomb:.15g} 1/C")
    print("\nConditional Eo/Ri pair (Ri is supplied, not identified)")
    print(f"Ri (assumed)                 : {result.ri_ohm_assumed:.9f} ohm")
    print(f"Eo = C0 + i*Ri               : {result.eo_volt_conditional:.15f} V")
    print(
        f"All equivalent pairs obey    : Eo = {result.c0_volt:.15f} "
        f"+ {result.current_ampere:.12f}*Ri"
    )
    print("\nFit diagnostics")
    print(f"SSE                          : {result.sse_volt2:.6e} V^2")
    print(f"RMSE                         : {result.rmse_volt:.6e} V")
    print(f"Maximum absolute error       : {result.max_abs_error_volt:.6e} V")
    print("=" * 76)


def resolve_default_data(script_dir: Path) -> Path:
    markdown = script_dir.parent / "data303212qz02.md"
    excel = script_dir.parent / "data303212qz02.xls"
    if markdown.exists():
        return markdown
    if excel.exists():
        return excel
    raise FileNotFoundError("Neither data303212qz02.md nor data303212qz02.xls exists")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="Path to .md, .xls, or .xlsx data")
    parser.add_argument(
        "--ri",
        type=float,
        default=DEFAULT_ASSUMED_RI_OHM,
        help=(
            "Ri from an independent test [ohm]. Default 0.20 is an explicit "
            "teaching assumption, not an estimate from this dataset."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for PNG/JSON/CSV outputs (default: script directory)",
    )
    parser.add_argument(
        "--skip-plots",
        action="store_true",
        help="Run fitting and write JSON/CSV without importing matplotlib",
    )
    args = parser.parse_args()
    if args.ri < 0:
        parser.error("--ri must be non-negative")

    script_dir = Path(__file__).resolve().parent
    data_path = (args.data or resolve_default_data(script_dir)).resolve()
    output_dir = (args.output_dir or script_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    t, v, i_s, source = read_data(data_path)
    if len(t) != 2753:
        print(f"[warning] Expected 2,753 rows, found {len(t):,}")
    current = i_s + v / RL_OHM
    q = cumulative_trapezoid(current, t)
    mean_i = float(np.mean(current))
    if not np.allclose(current, mean_i, atol=1e-12, rtol=0.0):
        raise ValueError("This problem expects a constant-current discharge dataset")
    qn = mean_i * TN_SECOND

    result, fitted_v = identify_parameters(q, v, current, qn, args.ri)
    write_outputs(output_dir, t, v, i_s, current, q, fitted_v, result, source)
    if not args.skip_plots:
        make_plots(output_dir, t, v, i_s, current, q, fitted_v)
    print_report(result, len(t), source)


if __name__ == "__main__":
    main()
