import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm

OUT = sys.argv[1]
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#1f1f1e", "#5e5d57", "#e4e3df"
NL = "\n"


def wilson(k, n, z=norm.ppf(0.975)):
    p = k / n
    den = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return c - h, c + h


# (label, x, k, n, color, marker, dx_log)
rl = [
    ("AdaMimic", 1, 57, 60, BLUE, "o", -0.09),
    ("ZEST box climb", 1, 10, 10, BLUE, "o", 0.0),
    ("ContactMimic", 1, 28, 30, BLUE, "o", 0.09),
    ("HuB", 5, 24, 25, BLUE, "o", 0.0),
    ("PhysHSI carry box", 16, 6, 10, BLUE, "o", 0.0),
    ("LIMMT curated 10%", 2420, 34, 40, ORANGE, "s", 0.0),
    ("LIMMT full AMASS", 24197, 31, 40, ORANGE, "s", 0.0),
    ("SONIC", 317189, 123, 124, ORANGE, "s", 0.0),
]
bc = [
    ("HumanoidExo 5 teleop", 5, 3, 60, AQUA, "D", 0.0),
    ("TrajBooster, pretrained", 28, 25, 40, AQUA, "D", 0.0),
    ("TrajBooster, no pretrain", 28, 0, 40, AQUA, "D", 0.0),
    ("Hierarchical VLP", 30, 29, 40, AQUA, "D", 0.0),
    ("Humanoid Everyday, best of 7", 40, 36, 70, AQUA, "D", 0.0),
    ("Humanoid Everyday, worst of 7", 40, 20, 70, AQUA, "D", 0.0),
    ("OmniClone + GR00T N1.6", 50, 18, 21, AQUA, "D", -0.06),
    ("HOMIE", 50, 23, 30, AQUA, "D", 0.02),
    ("AMO", 50, 42, 50, AQUA, "D", 0.06),
    ("TWIST2", 50, 6, 7, AQUA, "D", -0.02),
    ("HumanoidExo 200 teleop", 200, 48, 60, AQUA, "D", -0.03),
    ("HumanoidExo 5 teleop + 195 exo", 200, 48, 60, AQUA, "D", 0.03),
]

plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK})
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), sharey=True,
                         gridspec_kw={"width_ratios": [1.15, 1.15, 0.9], "wspace": 0.08})


def style(ax, xlabel, title):
    ax.set_xscale("log")
    ax.set_ylim(-0.03, 1.05)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.grid(True, axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left", fontsize=10, fontweight="bold", color=INK)
    ax.axhline(0.8, color=INK2, linewidth=0.8, linestyle=(0, (4, 3)))


def draw(ax, rows):
    for name, x, k, n, col, mk, dx in rows:
        p = k / n
        lo, hi = wilson(k, n)
        xp = x * 10**dx
        ax.plot([xp, xp], [lo, hi], color=col, linewidth=1.6, solid_capstyle="round", alpha=0.9)
        ax.plot(xp, p, marker=mk, markersize=7, color=col, markeredgecolor="white",
                markeredgewidth=1.2, linestyle="none")


def note(ax, text, xy, ha="left", va="center", color=INK2):
    ax.annotate(text, xy, ha=ha, va=va, fontsize=7.5, color=color)


# Panel A
ax = axes[0]
style(ax, "Reference clips in training set (log scale)", "A. RL motion tracking on G1 hardware")
draw(ax, rl)
ax.set_xlim(0.5, 2e6)
ax.set_ylabel("Hardware success rate (Wilson 95% interval)")
note(ax, NL.join(["1 clip per task", "ZEST box climb 10/10", "AdaMimic 57/60", "ContactMimic 28/30"]), (0.55, 0.47), va="top")
note(ax, NL.join(["HuB 24/25", "5 clips"]), (8, 0.985))
note(ax, NL.join(["PhysHSI carry box 6/10", "16 clips"]), (26, 0.58))
note(ax, "LIMMT curated 10% 34/40", (1400, 0.935), ha="right")
note(ax, "LIMMT full AMASS 31/40", (14000, 0.66), ha="right")
note(ax, "SONIC 123/124", (180000, 0.945), ha="right")
ax.plot([], [], "o", color=BLUE, label="specialist, 1 to 16 clips")
ax.plot([], [], "s", color=ORANGE, label="generalist, thousands of clips")
ax.legend(loc="lower left", frameon=False, fontsize=8)

# Panel B
ax = axes[1]
style(ax, "Teleoperated demonstrations per task (log scale)", "B. Imitation and VLA policies on G1 hardware")
draw(ax, bc)
ax.set_xlim(2.5, 5000)
ax.plot(1000, 0.988, marker="D", markersize=7, markerfacecolor="white", markeredgecolor=AQUA,
        markeredgewidth=1.6, linestyle="none")
note(ax, NL.join(["HumanoidExo", "5 teleop 3/60"]), (6.5, 0.17))
note(ax, NL.join(["TrajBooster", "pretrained 25/40"]), (22, 0.66), ha="right")
note(ax, NL.join(["TrajBooster", "no pretrain 0/40"]), (22, 0.04), ha="right")
note(ax, "Hierarchical VLP 29/40", (22, 0.78), ha="right")
note(ax, NL.join(["Humanoid Everyday", "best of 7 policies 36/70"]), (22, 0.49), ha="right")
note(ax, NL.join(["Humanoid Everyday", "worst of 7 policies 20/70"]), (22, 0.27), ha="right")
note(ax, NL.join(["50 demos per task", "OmniClone + GR00T N1.6 18/21", "AMO 42/50", "HOMIE 23/30", "TWIST2 6/7"]), (75, 0.42))
note(ax, NL.join(["200 demos", "HumanoidExo teleop 48/60", "5 teleop + 195 exo 48/60"]), (280, 0.57))
note(ax, NL.join(["GR00T N1.5", "1,000 episodes", "98.8%, trials", "not stated"]), (3800, 0.78), ha="right", va="top")
ax.plot([], [], "D", color=AQUA, label="teleop imitation or VLA")
ax.plot([], [], "D", markerfacecolor="white", markeredgecolor=AQUA, label="no trial count published")
ax.legend(loc="lower right", frameon=False, fontsize=8, bbox_to_anchor=(1.0, 0.10))

# Panel C
ax = axes[2]
style(ax, "Minutes of motion data (log scale)", "C. Minutes axis: one H1 study, no G1 study")
ax.set_xlim(1.5, 130)
mins = [10, 20, 40]
vals = [0.40, 0.65, 0.80]
ax.plot(mins, vals, color=INK2, linewidth=1.2, linestyle=(0, (2, 2)))
ax.plot(mins, vals, marker="o", markersize=7, markerfacecolor="white", markeredgecolor=INK2,
        markeredgewidth=1.6, linestyle="none")
for m, v in zip(mins, vals):
    note(ax, NL.join([f"{m} min", f"{v:.2f}"]), (m, v + 0.07), ha="center")
note(ax, NL.join(["OmniH2O, Unitree H1", "diffusion policy, 25/50/100% of",
                  "about 40 min teleop; task average,", "10 trials per task"]), (2.0, 0.17))
for lv in [2.8, 5.6, 11.3, 22.5, 45]:
    ax.axvline(lv, ymin=0.0, ymax=0.045, color=BLUE, linewidth=2)
note(ax, NL.join(["proposed lab levels (box task, 12 s clips):", "2.8, 5.6, 11.3, 22.5, 45 min"]), (2.0, 0.93), color=BLUE)

cap1 = ("Every point is a reported hardware result on a physical robot; bars are Wilson 95% intervals on k/n. "
        "Horizontal units differ by panel because no published study uses minutes for the G1. Dashed line: 0.8 target.")
cap2 = ("Sources: AdaMimic Table IV; ZEST Fig. S5; ContactMimic Table 2; HuB Table 2; PhysHSI Table III; LIMMT Table 6; "
        "SONIC Fig. 2K; HumanoidExo Fig. 6; TrajBooster Table II; Hierarchical VLP Sec. IV; Humanoid Everyday Table II; "
        "OmniClone Table II; HOMIE Table V; AMO Table IV; TWIST2 Sec. IV-C; GR00T N1.5 GEAR page; OmniH2O Table 3.")
fig.text(0.01, -0.03, cap1 + NL + cap2, fontsize=7, color=INK2, ha="left", va="top")
fig.savefig(OUT, dpi=170, bbox_inches="tight", facecolor="white")
print("saved", OUT)
