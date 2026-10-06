#!/usr/bin/env python3
"""Contribution Jet — turns a GitHub contribution graph into an animated SVG shooter.

usage: python jet.py <github-username> <output.svg>
Only the Python standard library is needed. Fonts are embedded from this folder.
"""
import base64, datetime as dt, os, re, sys, urllib.request
from xml.sax.saxutils import escape

USER = sys.argv[1] if len(sys.argv) > 1 else 'chandanB47'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'contribution-jet.svg'
HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ data
def fetch(user):
    req = urllib.request.Request(f'https://github.com/users/{user}/contributions',
                                 headers={'User-Agent': 'Mozilla/5.0 (contribution-jet)'})
    html = urllib.request.urlopen(req, timeout=30).read().decode()
    cells = re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?data-level="(\d)"', html)
    if not cells: raise SystemExit('No contribution cells found — is the username right?')
    days = {dt.date.fromisoformat(d): int(l) for d, l in cells}
    first = min(days); start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # back to Sunday
    grid = {}
    for d, lvl in days.items():
        grid[((d - start).days // 7, (d.weekday() + 1) % 7)] = lvl
    ncols = max(c for c, _ in grid) + 1
    return grid, ncols

grid, NC = fetch(USER)

# ------------------------------------------------------------------ geometry
W, H = 1200, 500
P, CS = 18, 14                       # pitch, cell size
X0 = (W - (NC * P - 4)) / 2
GY0 = 186
JY = 366                             # jet lane
SPEED = 520.0                        # bullet px / s
BLUE, LBLUE, RED, BG = '#247bff', '#8bc6ff', '#ff354f', '#070b16'
LEVEL = ['#101a2e', '#0e3a7a', '#1561d6', '#2f8bff', '#8bc6ff']

def cx(c): return X0 + c * P + CS / 2
def cy(r): return GY0 + r * P + CS / 2

# ------------------------------------------------------------------ timeline
LEAD, EXIT, HOLD = 1.0, 1.2, 1.9
t = LEAD
cols = []      # (col, arrive, depart, [hits])
hits = []      # (time, col, row, fire_time, dist)
for c in range(NC):
    rows = sorted([r for r in range(7) if grid.get((c, r), 0) > 0], reverse=True)   # nearest (bottom) first
    k = len(rows)
    slot = 0.17 if k == 0 else 0.30 + 0.11 * k
    arrive, depart = t, t + slot - 0.07
    for j, r in enumerate(rows):
        ft = arrive + 0.05 + j * 0.11
        dist = (JY - 18) - cy(r)
        hits.append((ft + dist / SPEED, c, r, ft, dist))
    cols.append((c, arrive, depart))
    t += slot
SWEEP_END = t
T = round(SWEEP_END + EXIT + HOLD, 2)
hits.sort()
N = len(hits)

def kf(points):
    """points: [(seconds, value)] -> (values, keyTimes) strictly increasing within [0,1]"""
    vs, ks, last = [], [], -1.0
    for tt, v in points:
        k = max(0.0, min(1.0, tt / T))
        if k <= last: k = last + 1e-5
        vs.append(str(v)); ks.append(f'{min(k,1):.5f}'); last = k
    ks[-1] = '1'
    return ';'.join(vs), ';'.join(ks)

def anim(attr, points, extra=''):
    v, k = kf(points)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{T}s" repeatCount="indefinite" {extra}/>'

# ------------------------------------------------------------------ svg parts
font_d = base64.b64encode(open(os.path.join(HERE, 'barlow-bold-subset.woff2'), 'rb').read()).decode()
font_m = base64.b64encode(open(os.path.join(HERE, 'plexmono-subset.woff2'), 'rb').read()).decode()

def txt(x, y, s, size, fill='#f2f5ff', mono=False, ls=0, anchor=None, extra=''):
    a = f' text-anchor="{anchor}"' if anchor else ''
    l = f' letter-spacing="{ls}"' if ls else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" style="fill:{fill}"{" class=\"mono\"" if mono else ""}{l}{a}{extra}>{escape(s)}</text>'

parts = []
# cells
for (c, r), lvl in sorted(grid.items()):
    x, y = X0 + c * P, GY0 + r * P
    if lvl == 0:
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{CS}" height="{CS}" rx="3" fill="{LEVEL[0]}"/>')
    else:
        th = next(h[0] for h in hits if h[1] == c and h[2] == r)
        a = anim('opacity', [(0, 1), (th - 0.01, 1), (th, 0), (T - 1.2, 0), (T - 0.6, 1), (T, 1)])
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{CS}" height="{CS}" rx="3" fill="{LEVEL[lvl]}">{a}</rect>')

# bullets + explosions
for th, c, r, ft, dist in hits:
    x, y1, y0 = cx(c), cy(r), JY - 18
    parts.append(
        f'<rect x="{x-1.5:.1f}" y="0" width="3" height="11" rx="1.5" fill="{LBLUE}" opacity="0">'
        + anim('y', [(0, y0), (ft, y0), (th, y1 - 5), (T, y1 - 5)])
        + anim('opacity', [(0, 0), (ft - 0.001, 0), (ft, 1), (th, 1), (th + 0.001, 0), (T, 0)]) + '</rect>')
    parts.append(
        f'<circle cx="{x:.1f}" cy="{y1:.1f}" r="2" fill="none" stroke="#ffd5db" stroke-width="1.6" opacity="0">'
        + anim('r', [(0, 2), (th, 2), (th + 0.38, 15), (T, 15)])
        + anim('opacity', [(0, 0), (th - 0.001, 0), (th, .95), (th + 0.38, 0), (T, 0)]) + '</circle>')

# jet path
xs, xe = X0 - 60, X0 + NC * P + 60
pts = [(0, f'{xs:.1f} 0')]
for c, a, d in cols:
    pts += [(a, f'{cx(c):.1f} 0'), (d, f'{cx(c):.1f} 0')]
pts += [(SWEEP_END + EXIT, f'{xe:.1f} 0'), (T, f'{xe:.1f} 0')]
v, k = kf(pts)
jet = (f'<g transform="translate(0,{JY})"><g><animateTransform attributeName="transform" type="translate" values="{v}" keyTimes="{k}" dur="{T}s" repeatCount="indefinite"/>'
       f'<ellipse cx="0" cy="18" rx="9" ry="14" fill="{RED}" opacity=".25" filter="url(#blur)"/>'
       f'<path d="M-2.5 11 L0 26 L2.5 11 Z" fill="{RED}"><animateTransform attributeName="transform" type="scale" values="1 .7;1 1.25;1 .7" dur=".18s" repeatCount="indefinite" additive="sum"/></path>'
       f'<path d="M0 -17 L5 -3 L17 10 L17 14 L5 9 L3 14 L0 11 L-3 14 L-5 9 L-17 14 L-17 10 L-5 -3 Z" fill="url(#jetg)" stroke="{LBLUE}" stroke-width=".8"/>'
       f'<path d="M0 -10 C2.5 -6 2.5 0 0 3 C-2.5 0 -2.5 -6 0 -10 Z" fill="#0a1a3a"/>'
       f'<circle cx="-17" cy="12" r="1.8" fill="{RED}"/><circle cx="17" cy="12" r="1.8" fill="{RED}"/></g></g>')
parts.append(jet)

# score strips (hundreds / tens / ones) — discrete steps at every hit
digits = max(2, len(str(N)))
SX = 44; DW = 27
strips = ''
for i in range(digits):
    div = 10 ** (digits - 1 - i)
    seq = [(0, 0)] + [(h[0], (n + 1) // div % 10) for n, h in enumerate(hits)] + [(T - 0.6, 0), (T, 0)]
    vals = ';'.join(f'0 {-d * 48}' for _, d in seq)
    # discrete: keyTimes must start at 0 and be increasing
    kt = []; last = -1
    for tt, _ in seq:
        kk = max(0, min(1, tt / T)); kk = kk if kk > last else last + 1e-5; kt.append(kk); last = kk
    kt[-1] = 1
    x = SX + i * DW
    ds = ''.join(txt(x, 470 + n * 48, str(n), 44) for n in range(10))
    strips += (f'<clipPath id="dg{i}"><rect x="{x-2}" y="434" width="{DW}" height="44"/></clipPath>'
               f'<g clip-path="url(#dg{i})"><g><animateTransform attributeName="transform" type="translate" calcMode="discrete" '
               f'values="{vals}" keyTimes="{";".join(f"{q:.5f}" for q in kt)}" dur="{T}s" repeatCount="indefinite"/>{ds}</g></g>')

legend_x = X0 + NC * P - 4 - 5 * 14 - 34 - 34
legend = txt(legend_x, 326, 'LESS', 10, '#6f7f9c', True, 1.4, 'end')
for i in range(5):
    legend += f'<rect x="{legend_x+8+i*14}" y="318" width="10" height="10" rx="2.5" fill="{LEVEL[i]}"/>'
legend += txt(legend_x + 8 + 5 * 14 + 4, 326, 'MORE', 10, '#6f7f9c', True, 1.4)

bar_x, bar_w = 520, 636
progress = (f'<rect x="{bar_x}" y="458" width="{bar_w}" height="6" rx="3" fill="#111c33"/>'
            f'<rect x="{bar_x}" y="458" width="0" height="6" rx="3" fill="url(#bar)">'
            + anim('width', [(0, 0), (LEAD, 0), (SWEEP_END, bar_w), (T - 1.2, bar_w), (T - 0.6, 0), (T, 0)]) + '</rect>')

CSS = ('@font-face{font-family:Display;font-weight:700;src:url(data:font/woff2;base64,' + font_d + ') format("woff2")}'
       '@font-face{font-family:Mono;font-weight:400;src:url(data:font/woff2;base64,' + font_m + ') format("woff2")}'
       'text{font-family:Display,sans-serif;font-weight:700;fill:#f2f5ff}.mono{font-family:Mono,monospace;font-weight:400}'
       '.enter{animation:entry 1s cubic-bezier(.16,1,.3,1) both}@keyframes entry{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}'
       '.blink{animation:blink 1s steps(2,end) infinite both}@keyframes blink{50%{opacity:.2}}'
       '.scan{animation:scan 8s ease-in-out infinite both}@keyframes scan{0%,30%{transform:translateX(-300px)}70%,100%{transform:translateX(1500px)}}'
       '@media(prefers-reduced-motion:reduce){.enter,.blink,.scan{animation:none!important}.scan{display:none}}')

stars = ''
import random; random.seed(7)
for _ in range(30):
    sx, sy = random.randint(30, W - 30), random.randint(100, JY + 60)
    d = random.uniform(2, 5)
    stars += f'<circle cx="{sx}" cy="{sy}" r="{random.choice([.8,1.1,1.5])}" fill="#bcd4ff" opacity="0"><animate attributeName="opacity" values="0;.7;0" dur="{d:.1f}s" begin="{-random.uniform(0,d):.1f}s" repeatCount="indefinite"/></circle>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="jt jd">
<title id="jt">Contribution jet — {escape(USER)}</title>
<desc id="jd">An animated jet flies across the GitHub contribution graph of {escape(USER)} and shoots down {N} active days, keeping score, then the graph respawns and the game loops.</desc>
<style>{CSS}</style>
<defs>
<linearGradient id="hair"><stop stop-color="{BLUE}" stop-opacity=".7"/><stop offset=".5" stop-color="#567394" stop-opacity=".25"/><stop offset="1" stop-color="{RED}" stop-opacity=".65"/></linearGradient>
<linearGradient id="aurora" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff"/><stop offset=".45" stop-color="{LBLUE}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<linearGradient id="jetg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff"/><stop offset=".55" stop-color="#9cc2ff"/><stop offset="1" stop-color="#2f6fe0"/></linearGradient>
<linearGradient id="bar" x1="0" x2="1"><stop stop-color="{BLUE}"/><stop offset="1" stop-color="{LBLUE}"/></linearGradient>
<linearGradient id="foil"><stop stop-color="#76afff" stop-opacity="0"/><stop offset=".45" stop-color="#76afff" stop-opacity="0"/><stop offset=".5" stop-color="#d2ecff" stop-opacity=".14"/><stop offset=".56" stop-color="{RED}" stop-opacity=".06"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#1266ed" stop-opacity=".34"/><stop offset="1" stop-color="#1266ed" stop-opacity="0"/></radialGradient>
<radialGradient id="rhalo"><stop stop-color="#ff1c3f" stop-opacity=".2"/><stop offset="1" stop-color="#ff1c3f" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#99b1db" opacity=".13"/></pattern>
<pattern id="lines" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0 0V8" stroke="#4b6d9c" stroke-opacity=".10" stroke-width="2"/></pattern>
<filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>
<clipPath id="outer"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="24"/></clipPath>
</defs>
<g clip-path="url(#outer)">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="{BG}"/>
<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="21" fill="url(#dots)"/>
<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="21" fill="url(#lines)"/>
<ellipse cx="260" cy="{JY}" rx="420" ry="220" fill="url(#halo)"/><ellipse cx="1150" cy="80" rx="260" ry="220" fill="url(#rhalo)"/>
{stars}
{txt(44, 44, '07 / CONTRIBUTION JET', 11, '#8e9db9', True, 1.6)}
{txt(W-44, 44, 'LIVE DATA / ' + USER.upper(), 11, '#8e9db9', True, 1.6, 'end')}
<path d="M42 76 L{W-42} 76" stroke="#223149" stroke-width="1.5" fill="none"/>
<g class="enter"><text x="40" y="128" font-size="52" style="fill:url(#aurora)">SHOOT DOWN THE GRAPH.</text></g>
<g class="enter" style="animation-delay:.2s">{txt(44, 158, 'EVERY GLOWING CELL IS A DAY I SHOWED UP. THE JET CLEARS THEM — THEN THEY RESPAWN.', 12, '#8e9db9', True, 1.6)}</g>
{''.join(parts)}
{legend}
<path d="M{X0:.1f} {JY+26} H{X0+NC*P-4:.1f}" stroke="#223149" stroke-dasharray="3 7"/>
{txt(44, 424, 'ACTIVE DAYS DESTROYED', 11, '#8e9db9', True, 1.6)}
{strips}
{txt(SX + digits * DW + 6, 470, '/ ' + str(N), 28, '#5b6b88')}
{txt(bar_x, 446, 'SWEEP PROGRESS', 11, '#8bc6ff', True, 1.6)}
{txt(W-44, 446, 'AUTOPILOT / LOOPING', 11, '#8e9db9', True, 1.6, 'end')}
{progress}
{txt(bar_x, 486, 'SOURCE / GITHUB CONTRIBUTION GRAPH — REFRESHED BY GITHUB ACTIONS', 10, '#5b6b88', True, 1.4)}
<rect x="{bar_x-14}" y="446" width="6" height="12" fill="{RED}" class="blink"/>
<g class="scan"><rect x="-200" y="0" width="220" height="{H}" fill="url(#foil)" transform="skewX(-18)"/></g>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="none" stroke="url(#hair)"/>
</svg>'''
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
open(OUT, 'w').write(svg)
print(f'{OUT}: {len(svg)//1024} KB | weeks={NC} | active days={N} | loop={T}s')
