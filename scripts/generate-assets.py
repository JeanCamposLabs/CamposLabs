#!/usr/bin/env python3
"""
Generate EvenFee brand images: favicon, PWA icons, and the Open Graph image.

This is how the committed images in /assets were produced. Re-run it after you
rebrand (new name / colors) to regenerate everything in one go.

Requirements:
    pip install cairosvg          # needs system cairo libs (preinstalled on most Linux)
    # DejaVu fonts are used for the OG text and ship with most Linux distros.

Usage:
    python3 scripts/generate-assets.py
"""
import os
import cairosvg

# --- Edit these to rebrand ----------------------------------------------------
BRAND       = "EvenFee"
COLOR_DARK  = "#1e3a8a"   # gradient start (deep indigo)
COLOR_MAIN  = "#2563eb"   # gradient end / primary
COLOR_GREEN = "#6ee7b7"   # recovery-green accent
HEADLINE    = ["Recover the Amazon FBA", "fees you were overcharged."]
SUBHEAD     = ["Mis-measured dimensions push items into a higher size",
               "tier. We find the errors and help you get the money back."]
CHIPS       = [("Official Amazon SP-API", 318), ("No buyer data", 206), ("GDPR-compliant", 224)]
FONT        = "DejaVu Sans"
# -----------------------------------------------------------------------------

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
OUT = os.path.abspath(OUT)

def mark(rounded: bool) -> str:
    rx = 'rx="15"' if rounded else ""
    return f'''<rect width="64" height="64" {rx} fill="url(#g)"/>
  <rect x="16" y="25" width="32" height="7" rx="3.5" fill="#ffffff"/>
  <rect x="16" y="38" width="21" height="7" rx="3.5" fill="{COLOR_GREEN}"/>'''

def icon_svg(rounded: bool) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{COLOR_DARK}"/><stop offset="1" stop-color="{COLOR_MAIN}"/>
  </linearGradient></defs>
  {mark(rounded)}
</svg>'''

def write(name, svg, w, h):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, name),
                     output_width=w, output_height=h)
    print("wrote", name, f"{w}x{h}")

# favicon.svg (rounded, vector — primary favicon)
with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(icon_svg(rounded=True).replace("<svg ",
            '<svg role="img" aria-label="%s" ' % BRAND, 1) + "\n")
print("wrote favicon.svg")

# PNG fallbacks / app icons
write("favicon-32.png",       icon_svg(rounded=True),  32,  32)
write("apple-touch-icon.png", icon_svg(rounded=False), 180, 180)
write("icon-192.png",         icon_svg(rounded=False), 192, 192)
write("icon-512.png",         icon_svg(rounded=False), 512, 512)

# Open Graph image (1200x630)
chips_svg, x = "", 90
for label, w in CHIPS:
    chips_svg += (f'<rect x="{x}" y="528" width="{w}" height="52" rx="26" '
                  f'fill="#ffffff" fill-opacity="0.08" stroke="{COLOR_GREEN}" stroke-opacity="0.5"/>'
                  f'<text x="{x+26}" y="561">{label}</text>')
    x += w + 18

og = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1526"/><stop offset="0.55" stop-color="#14264f"/><stop offset="1" stop-color="{COLOR_DARK}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.82" cy="0.1" r="0.6">
      <stop offset="0" stop-color="{COLOR_MAIN}" stop-opacity="0.45"/><stop offset="1" stop-color="{COLOR_MAIN}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="{COLOR_MAIN}"/></linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <g transform="translate(90,96)">
    <rect width="76" height="76" rx="18" fill="url(#m)"/>
    <rect x="19" y="29" width="38" height="9" rx="4.5" fill="#ffffff"/>
    <rect x="19" y="45" width="25" height="9" rx="4.5" fill="{COLOR_GREEN}"/>
    <text x="100" y="56" font-family="{FONT}" font-size="46" font-weight="bold" fill="#ffffff">{BRAND}</text>
  </g>
  <text x="90" y="296" font-family="{FONT}" font-size="62" font-weight="bold" fill="#ffffff">{HEADLINE[0]}</text>
  <text x="90" y="372" font-family="{FONT}" font-size="62" font-weight="bold" fill="#ffffff">{HEADLINE[1]}</text>
  <text x="92" y="436" font-family="{FONT}" font-size="29" fill="#aab8d4">{SUBHEAD[0]}</text>
  <text x="92" y="476" font-family="{FONT}" font-size="29" fill="#aab8d4">{SUBHEAD[1]}</text>
  <g font-family="{FONT}" font-size="22" fill="#dbe5f5">{chips_svg}</g>
</svg>'''
write("og-image.png", og, 1200, 630)
print("\nAll assets written to", OUT)
