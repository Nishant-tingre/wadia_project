import re, shutil, sys
from pathlib import Path

CSS = Path("static/style.css")
THEME = sys.argv[1] if len(sys.argv) > 1 else "teal"   # teal | blue | purple

# ---- Palettes: accent, accent2, bg, primary-dark, nlp, nlp-end, ml, ml-end (hex) ----
THEMES = {
    "teal":   dict(a="#2dd4bf", a2="#34d399", bg="#0b1f1d", hover="#5eead4", dark="#0f766e",
                   nlp="#34d399", nlp2="#22c55e", ml="#38bdf8", ml2="#06b6d4",
                   rgb="45, 212, 191", nlp_rgb="52, 211, 153", ml_rgb="56, 189, 248",
                   text="#e6fffa", t2="#b5d6d1", tm="#8fb8b2"),
    "blue":   dict(a="#60a5fa", a2="#818cf8", bg="#0a1128", hover="#93c5fd", dark="#3730a3",
                   nlp="#34d399", nlp2="#22c55e", ml="#38bdf8", ml2="#06b6d4",
                   rgb="96, 165, 250", nlp_rgb="52, 211, 153", ml_rgb="56, 189, 248",
                   text="#e8f0ff", t2="#b8c6e6", tm="#8a9bc4"),
    "purple": dict(a="#c084fc", a2="#f472b6", bg="#150b2e", hover="#d8b4fe", dark="#6b21a8",
                   nlp="#34d399", nlp2="#22c55e", ml="#38bdf8", ml2="#06b6d4",
                   rgb="192, 132, 252", nlp_rgb="52, 211, 153", ml_rgb="56, 189, 248",
                   text="#f5ebff", t2="#d4c0ec", tm="#a58cc4"),
}
t = THEMES[THEME]

ROOT = f""":root {{
  /* ---- THEME COLORS: change these to re-theme everything ---- */
  --accent: {t['a']};
  --accent-2: {t['a2']};

  --bg-primary: {t['bg']};
  --bg-card: rgba(255, 255, 255, 0.05);

  --text-primary: {t['text']};
  --text-secondary: {t['t2']};
  --text-muted: {t['tm']};

  --border-color: rgba({t['rgb']}, 0.2);
  --border-hover: rgba({t['rgb']}, 0.5);

  --color-primary: {t['a']};
  --color-primary-hover: {t['hover']};
  --color-primary-dark: {t['dark']};
  --color-primary-glow: rgba({t['rgb']}, 0.35);

  --color-nlp: {t['nlp']};
  --color-nlp-bg: rgba({t['nlp_rgb']}, 0.12);
  --color-nlp-end: {t['nlp2']};
  --color-nlp-glow: rgba(34, 197, 94, 0.4);

  --color-ml: {t['ml']};
  --color-ml-bg: rgba({t['ml_rgb']}, 0.12);
  --color-ml-border: rgba({t['ml_rgb']}, 0.3);
  --color-ml-end: {t['ml2']};
  --color-ml-glow: rgba(6, 182, 212, 0.4);

  /* ---- Non-color tokens ---- */
  --font-sans: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --border-radius: 16px;
  --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.35);
  --transition-smooth: all 0.25s ease;
}}"""

if not CSS.exists():
    sys.exit("Run this from the project_wadia folder (static/style.css not found).")

shutil.copy(CSS, CSS.with_suffix(".css.bak"))
css = CSS.read_text(encoding="utf-8")
done = []

def sub(label, pattern, repl, flags=re.S):
    global css
    css, n = re.subn(pattern, lambda m: repl(m) if callable(repl) else repl, css, flags=flags)
    done.append((label, n))

# 1. Replace the whole :root block (first one only)
css, n = re.subn(r":root\s*\{.*?\n\}", lambda m: ROOT, css, count=1, flags=re.S)
done.append((":root block", n))

# 2. Hard-coded colors
sub(".bg-glow", r"rgba\(124, 58, 237, 0\.18\) 0%, rgba\(14, 165, 233, 0\.08\) 50%",
    f"rgba({t['rgb']}, 0.18) 0%, rgba({t['nlp_rgb']}, 0.08) 50%")
sub(".logo i", r"linear-gradient\(135deg, hsl\(263, 70%, 55%\), hsl\(188, 75%, 45%\)\)",
    "linear-gradient(135deg, var(--accent), var(--accent-2))")
sub(".badge", r"background-color:\s*hsla\(224, 25%, 20%, 0\.8\);",
    "background-color: rgba(255, 255, 255, 0.06);")
sub(".btn-primary bg", r"linear-gradient\(135deg, var\(--color-primary\), hsl\(244, 55%, 45%\)\)",
    "linear-gradient(135deg, var(--color-primary), var(--color-primary-dark))")
sub(".btn-primary text", r"(\.btn-primary\s*\{[^}]*?)color:\s*#fff;",
    lambda m: m.group(1) + "color: #04201c;")
sub(".btn-primary:hover", r"linear-gradient\(135deg, var\(--color-primary-hover\), hsl\(244, 55%, 52%\)\)",
    "linear-gradient(135deg, var(--color-primary-hover), var(--color-primary))")
sub(".mapped-pill", r"hsla\(188, 75%, 45%, 0\.3\)", "var(--color-ml-border)")
sub("nlp meter", r"linear-gradient\(90deg, var\(--color-nlp\), #22c55e\)",
    "linear-gradient(90deg, var(--color-nlp), var(--color-nlp-end))")
sub("nlp glow", r"box-shadow:\s*0 0 10px 0 rgba\(34, 197, 94, 0\.4\);",
    "box-shadow: 0 0 10px 0 var(--color-nlp-glow);")
sub("ml meter", r"linear-gradient\(90deg, var\(--color-ml\), #06b6d4\)",
    "linear-gradient(90deg, var(--color-ml), var(--color-ml-end))")
sub("ml glow", r"box-shadow:\s*0 0 10px 0 rgba\(6, 182, 212, 0\.4\);",
    "box-shadow: 0 0 10px 0 var(--color-ml-glow);")

CSS.write_text(css, encoding="utf-8")
print(f"Theme: {THEME}   (backup: static/style.css.bak)\n")
for label, n in done:
    print(f"  {'OK ' if n else 'SKIP'}  {label}  ({n} change)")
print("\nNow hard refresh the browser: Ctrl + Shift + R")