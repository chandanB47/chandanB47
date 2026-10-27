"""Builds the README panels (assets/*.svg) in the portfolio theme.
Run:  python .github/readme/build_assets.py      (needs: pip install fonttools brotli)
Edit the TEXT in the build_* functions, re-run, commit the new assets/."""
import base64, io, os, random
from fontTools import subset

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'assets')
INK, PANEL, LINE = '#07070a', '#0d0d12', '#24242c'
BONE, MIST, SMOKE = '#f4f1ec', '#a7a6ad', '#6f6e76'
RED, HOT, CYAN, GREEN, AMBER = '#e5132b', '#ff3d5a', '#4cc9ff', '#46e3a8', '#ffb547'
GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,~%+-–—&/·•:'’!?"

def font_b64():
    o = subset.Options(); o.flavor = 'woff2'
    f = subset.load_font(os.path.join(HERE, 'BebasNeue.woff2'), o)
    s = subset.Subsetter(o); s.populate(text=GLYPHS); s.subset(f)
    buf = io.BytesIO(); subset.save_font(f, buf, o)
    return base64.b64encode(buf.getvalue()).decode()
FONT = font_b64()

CSS = f"""@font-face{{font-family:'BebasSub';src:url(data:font/woff2;base64,{FONT}) format('woff2')}}
.d{{font-family:'BebasSub','Bebas Neue',Impact,'Arial Narrow',sans-serif}}
.m{{font-family:ui-monospace,SFMono-Regular,'Cascadia Mono',Consolas,Menlo,monospace}}
.s{{font-family:-apple-system,'Segoe UI',Inter,Helvetica,Arial,sans-serif}}
.i{{font-family:'Instrument Serif',Georgia,'Times New Roman',serif;font-style:italic}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
@keyframes gr{{from{{transform:scaleY(0)}}}}
@keyframes dr{{to{{stroke-dashoffset:0}}}}
@keyframes dn{{from{{stroke-dasharray:0 100}}}}
@keyframes bk{{50%{{opacity:0}}}}
@keyframes up{{from{{opacity:0;transform:translateY(10px)}}}}
@keyframes pl{{0%{{opacity:.5;transform:scale(.9)}}100%{{opacity:0;transform:scale(1.5)}}}}
.fl{{animation:fl 5s ease-in-out infinite}} .fl2{{animation:fl 6.5s ease-in-out -2s infinite}}
.bar{{transform-box:fill-box;transform-origin:bottom;animation:gr 1.4s cubic-bezier(.22,1,.36,1) both}}
.ln{{stroke-dasharray:640;stroke-dashoffset:640;animation:dr 2.4s .5s cubic-bezier(.22,1,.36,1) forwards}}
.dn{{animation:dn 1.8s .6s cubic-bezier(.22,1,.36,1) both}}
.bk{{animation:bk 1.1s steps(1) infinite}}
.up{{animation:up .9s cubic-bezier(.22,1,.36,1) both}}
.pl{{transform-box:fill-box;transform-origin:center;animation:pl 3s ease-out infinite}}
@keyframes d1{{from{{transform:translate(-50px,14px)}}to{{transform:translate(70px,-24px)}}}}
@keyframes d2{{from{{transform:translate(36px,-12px)}}to{{transform:translate(-60px,30px)}}}}
@keyframes sh{{from{{transform:translateX(-340px)}}to{{transform:translateX(1750px)}}}}
@keyframes tw{{0%,100%{{opacity:.12;transform:scale(.5)}}50%{{opacity:1;transform:scale(1.35)}}}}
@keyframes em{{0%{{opacity:0;transform:translateY(0)}}15%{{opacity:1}}100%{{opacity:0;transform:translateY(-200px)}}}}
@keyframes cm{{to{{stroke-dashoffset:-100}}}}
@keyframes wv{{0%,12%,100%{{stroke:#24242c}}5%{{stroke:#ff3d5a}}}}
@keyframes br{{0%,100%{{opacity:.45;transform:scale(1)}}50%{{opacity:1;transform:scale(1.1)}}}}
@keyframes sk{{from{{transform:translateX(44px)}}to{{transform:translateX(1160px)}}}}
@keyframes sc{{from{{transform:translateX(-80px)}}to{{transform:translateX(480px)}}}}
@keyframes gw{{0%,100%{{filter:drop-shadow(0 0 0 #ff3d5a)}}50%{{filter:drop-shadow(0 0 9px #ff3d5a)}}}}
.d1{{animation:d1 16s ease-in-out infinite alternate}} .d2{{animation:d2 19s ease-in-out infinite alternate}}
.sh{{animation:sh 7.5s ease-in-out infinite}}
.tw{{transform-box:fill-box;transform-origin:center;animation:tw 3s ease-in-out infinite}}
.em{{animation:em 5s ease-in infinite}}
.cm{{stroke-dasharray:15 85;animation:cm 4.5s linear infinite}}
.wv{{animation:wv 6s linear infinite}}
.br{{transform-box:fill-box;transform-origin:center;animation:br 4s ease-in-out infinite}}
.sk{{animation:sk 4.4s cubic-bezier(.45,0,.2,1) infinite}}
.sc{{animation:sc 4.2s ease-in-out 1s infinite}}
.gw{{animation:gw 2.4s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.ln{{stroke-dashoffset:0}}}}"""

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def T(x, y, s, size, fill=BONE, cls='s', anchor='start', ls=0, w=None, extra=''):
    wt = f' font-weight="{w}"' if w else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" class="{cls}" text-anchor="{anchor}" letter-spacing="{ls}"{wt}{extra}>{esc(s)}</text>'
def rect(x, y, w, h, r=12, fill=PANEL, stroke=LINE, sw=1, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
def comet(x, y, w, h, r, delay=0, col=HOT, dur=4.5):
    st = f'style="animation-delay:-{delay:.1f}s;animation-duration:{dur}s"'
    g = f'class="cm" {st} x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" pathLength="100" fill="none" stroke-linecap="round"'
    return f'<rect {g} stroke="{col}" stroke-width="8" opacity=".25"/><rect {g} stroke="#ffd9df" stroke-width="1.8"/>'
def embers(w, h, n, seed):
    r = random.Random(seed); o = ''
    for i in range(n):
        o += f'<circle class="em" style="animation-delay:-{r.uniform(0,5):.1f}s;animation-duration:{r.uniform(4,7):.1f}s" cx="{r.uniform(30,w-30):.0f}" cy="{h-16}" r="{r.choice((1.2,1.8,2.4))}" fill="{r.choice((HOT,AMBER,"#fff"))}"/>'
    return o
def sparkle(x, y, sc, col, d):
    return f'<path class="tw" style="animation-delay:-{d:.1f}s" transform="translate({x} {y}) scale({sc})" d="M0-7 1.6-1.6 7 0 1.6 1.6 0 7-1.6 1.6-7 0-1.6-1.6Z" fill="{col}"/>'
def lights(w, h, n, seed, big):
    r = random.Random(seed); o = ''
    for i in range(n):
        o += f'<circle class="tw" style="animation-delay:-{r.uniform(0,3):.1f}s;animation-duration:{r.uniform(2.4,4.6):.1f}s" cx="{r.uniform(20,w-20):.0f}" cy="{r.uniform(14,h-14):.0f}" r="{r.choice((1.1,1.5,2.1))}" fill="{r.choice(("#fff",HOT,"#ffd0d6",CYAN))}"/>'
    for i in range(big): o += sparkle(round(r.uniform(60, w-60)), round(r.uniform(24, h-24)), r.choice((.8, 1.1, 1.5)), r.choice(('#fff', '#ff8fa0', '#bff0ff')), r.uniform(0, 3))
    return o
def cmark(x, y, s=1, col=RED, sw=4):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M19 6.5C16.9 4.5 14.7 3.7 12 3.7 6.8 3.7 4 8.5 4 16s2.8 12.3 8 12.3c2.7 0 4.9-.8 7-2.8" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/></g>'
_wc = [0]
def chip(x, y, label, h=32, size=13, fill='#12121a', stroke=LINE, col=BONE, pad=15, cw=7.3, wave=False):
    w = round(len(label) * cw + pad * 2); ex = ''
    if wave: _wc[0] += 1; ex = f' class="wv" style="animation-delay:{(_wc[0]*.21)%6:.2f}s"'
    return w, rect(x, y, w, h, h / 2, fill, stroke, extra=ex) + T(x + w / 2, y + h / 2 + size * .35, label, size, col, 's', 'middle', 0, 500)

def svg(w, h, body, title, glow=True, fx='full', seed=1, nstars=14, big=3):
    defs = f"""<defs><style>{CSS}</style>
<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#12121a"/><stop offset="1" stop-color="#0b0b10"/></linearGradient>
<radialGradient id="gr1" cx=".5" cy=".5" r=".5"><stop stop-color="{RED}" stop-opacity=".58"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<radialGradient id="gr2" cx=".5" cy=".5" r=".5"><stop stop-color="{CYAN}" stop-opacity=".24"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<pattern id="dt" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#fff" opacity=".07"/></pattern>
<linearGradient id="lg" x1="0" x2="1"><stop stop-color="{HOT}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{HOT}" stop-opacity=".28"/><stop offset="1" stop-color="{HOT}" stop-opacity="0"/></linearGradient>
<linearGradient id="nm" gradientUnits="userSpaceOnUse" x1="-700" x2="700"><stop stop-color="{BONE}"/><stop offset=".38" stop-color="{BONE}"/><stop offset=".5" stop-color="#ff8fa0"/><stop offset=".62" stop-color="{BONE}"/><stop offset="1" stop-color="{BONE}"/><animateTransform attributeName="gradientTransform" type="translate" from="-300 0" to="1500 0" dur="7s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="hl" x1="0" x2="1"><stop stop-color="{RED}"/><stop offset=".5" stop-color="{RED}" stop-opacity=".25"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient><filter id="neon" x="-30%" y="-40%" width="160%" height="180%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="bl" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="11"/></filter>
<linearGradient id="shine" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#ffd9df" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="beam" x1="0" x2="1"><stop stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="#bff0ff" stop-opacity=".32"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="trail" x1="0" x2="1"><stop stop-color="{HOT}" stop-opacity="0"/><stop offset="1" stop-color="#ff9aa8"/></linearGradient>
<radialGradient id="spot" cx=".5" cy=".5" r=".5"><stop stop-color="#fff"/><stop offset=".25" stop-color="#ff8fa0" stop-opacity=".9"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<clipPath id="fc"><rect width="{w}" height="{h}" rx="16"/></clipPath></defs>"""
    bg = f'<rect width="{w}" height="{h}" rx="16" fill="{INK}"/>'
    if glow:
        bg += f'<ellipse cx="{w*.82:.0f}" cy="{h*.2:.0f}" rx="{w*.34:.0f}" ry="{h*.8:.0f}" fill="url(#gr1)"/><ellipse cx="{w*.05:.0f}" cy="{h}" rx="{w*.28:.0f}" ry="{h*.7:.0f}" fill="url(#gr2)"/>'
    bg += f'<rect width="{w}" height="{h}" rx="16" fill="url(#dt)"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{LINE}"/>'
    pre = ''
    if fx == 'full':
        pre = (f'<g clip-path="url(#fc)"><g class="d1"><ellipse cx="{w*.78:.0f}" cy="{h*.25:.0f}" rx="{w*.3:.0f}" ry="{h*.7:.0f}" fill="url(#gr1)"/></g>'
               f'<g class="d2"><ellipse cx="{w*.2:.0f}" cy="{h*.9:.0f}" rx="{w*.28:.0f}" ry="{h*.6:.0f}" fill="url(#gr2)"/></g></g>')
    post = ''
    if fx in ('full', 'lite'):
        n, bg_ = (nstars, big) if fx == 'full' else (5, 1)
        post = (f'<g clip-path="url(#fc)"><g transform="skewX(-22)"><rect class="sh" style="animation-delay:-{seed*1.7%7:.1f}s" x="0" y="-10" width="170" height="{h+20}" fill="url(#shine)"/></g>'
                + lights(w, h, n, seed, bg_) + '</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>{defs}{bg}{pre}{body}{post}</svg>'

def save(name, s):
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- hero
def build_hero():
    b = '<g filter="url(#neon)">' + cmark(40, 30, 1.0) + '</g>' + T(76, 55, 'SERIES', 13, MIST, 'm', 'start', 7, 700) + T(1156, 55, 'BENGALURU · INDIA', 12, SMOKE, 'm', 'end', 3)
    b += f'<path d="M44 80H1156" stroke="{LINE}"/>'
    b += T(44, 134, 'HELLO, WORLD —', 13, HOT, 'm', 'start', 6, 700)
    b += '<g class="br">' + T(40, 300, 'CHANDAN B', 172, HOT, 'd', 'start', 3, extra=' filter="url(#bl)" opacity=".55"') + '</g>'
    b += T(40, 300, 'CHANDAN B', 172, 'url(#nm)', 'd', 'start', 3)
    b += f'<rect x="46" y="318" width="120" height="4" rx="2" fill="{RED}" filter="url(#neon)"><animate attributeName="width" values="0;120;120" keyTimes="0;.4;1" dur="2.4s" fill="freeze"/></rect>'
    b += T(44, 362, 'DATA ANALYST  •  SQL  •  POWER BI  •  PYTHON', 14, HOT, 'm', 'start', 4, 700)
    b += T(44, 404, 'I clean data, build dashboards and turn operational records', 17, MIST) + T(44, 431, 'into reports people can act on.', 17, MIST)
    b += T(44, 431, '', 1) 
    b += rect(44, 456, 190, 40, 8, BONE, BONE) + T(139, 481, 'VIEW PORTFOLIO  →', 12, INK, 'm', 'middle', 2, 800)
    b += rect(248, 456, 262, 40, 8, 'none', '#3a3a44') + T(379, 481, 'chandanb47.github.io', 12, BONE, 'm', 'middle', 1.5, 600)
    # dashboard card
    b += '<ellipse class="br" cx="923" cy="275" rx="340" ry="230" fill="url(#gr1)"/>'
    b += '<g class="fl2">' + rect(690, 110, 466, 330, 18, 'url(#pn)', '#2c2c36') + comet(690, 110, 466, 330, 18, 0)
    b += T(716, 146, 'DATA / INSIGHTS', 12, BONE, 'm', 'start', 4, 700) + T(716, 166, 'ANALYZE · UNDERSTAND · COMMUNICATE', 9, SMOKE, 'm', 'start', 1.6)
    for i, x in enumerate((716, 860, 1004)):
        b += rect(x, 182, 134, 94, 10, '#101018', '#2c2c36')
    b += '<g filter="url(#neon)">'
    for i, hgt in enumerate((30, 52, 40, 62)):
        b += f'<rect class="bar" style="animation-delay:{i*.12:.2f}s" x="{738+i*20}" y="{262-hgt}" width="12" height="{hgt}" rx="2" fill="{HOT}"/>'
    b += '</g>'
    b += f'<polyline class="ln" pathLength="640" points="884,250 902,232 920,240 938,214 956,222 974,204" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><circle cx="974" cy="204" r="4" fill="{CYAN}"/>'
    b += f'<circle cx="1071" cy="229" r="26" fill="none" stroke="#1f2a26" stroke-width="8"/><circle class="dn" cx="1071" cy="229" r="26" fill="none" stroke="{GREEN}" stroke-width="8" stroke-linecap="round" pathLength="100" stroke-dasharray="72 100" transform="rotate(-90 1071 229)"/>'
    for x, l in ((726, 'PATTERNS'), (870, 'TRENDS'), (1014, 'DECISIONS')): b += T(x, 270, l, 8, MIST, 'm', 'start', 1.5)
    b += rect(716, 294, 414, 124, 10, '#101018', '#2c2c36') + T(734, 316, 'FROM RAW DATA TO CLARITY', 9, MIST, 'm', 'start', 2, 700)
    pts = '734,396 788,380 842,386 896,354 950,362 1004,334 1058,344 1112,322'
    b += f'<polygon points="{pts} 1112,404 734,404" fill="url(#ar)"/><polyline class="ln" pathLength="640" points="{pts}" fill="none" stroke="url(#lg)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' + '<clipPath id="cc"><rect x="690" y="110" width="466" height="330" rx="18"/></clipPath><g clip-path="url(#cc)"><rect class="sc" x="690" y="110" width="70" height="330" fill="url(#beam)"/></g></g>'
    b += '<g class="fl">' + rect(960, 84, 196, 54, 12, '#14141c', '#34343e') + T(978, 108, '~20% accuracy gain', 14, BONE, 's', 'start', 0, 700) + T(978, 126, 'KEMS FORGINGS', 9, SMOKE, 'm', 'start', 2.4) + '</g>'
    b += '<g class="fl2">' + rect(636, 392, 214, 54, 12, '#14141c', '#34343e') + T(654, 416, 'Power BI · Statistics', 14, BONE, 's', 'start', 0, 700) + T(654, 434, 'CURRENT FOCUS', 9, SMOKE, 'm', 'start', 2.4) + '</g>'
    b += embers(1200, 520, 16, 7)
    save('hero.svg', svg(1200, 520, b, "Hi, I'm Chandan B — Data Analyst working with SQL, Power BI, Python and Excel. C Series portfolio."))

# ---------------------------------------------------------------- section titles
def build_title(name, num, title, sub):
    b = '<g filter="url(#neon)">' + T(44, 62, num, 14, HOT, 'm', 'start', 4, 700) + '</g>' + T(92, 76, title, 62, BONE, 'd', 'start', 2) + T(1156, 70, sub, 24, MIST, 'i', 'end')
    b += f'<rect x="44" y="92" width="1112" height="1.5" fill="url(#hl)"/><g class="sk"><rect x="-130" y="91" width="130" height="3" fill="url(#trail)"/><circle cx="0" cy="92.5" r="14" fill="url(#spot)"/><circle cx="0" cy="92.5" r="2.5" fill="#fff"/></g>'
    save(f'title-{name}.svg', svg(1200, 106, b, f'{num} {title} — {sub}', glow=False, fx='lite', seed=len(name)))

# ---------------------------------------------------------------- about
def build_about():
    b = '<g filter="url(#neon)">' + cmark(44, 36, .9, HOT, 4) + '</g>'
    b += T(80, 60, 'THE PILOT', 12, HOT, 'm', 'start', 5, 700)
    for i, l in enumerate(('I turn messy operational data into', 'clear, trustworthy reports that', 'people can act on.')):
        b += f'<g class="up" style="animation-delay:{i*.15:.2f}s">' + T(44, 128 + i * 50, l, 35, BONE, 'i') + '</g>'
    b += T(44, 296, '— CHANDAN B', 12, SMOKE, 'm', 'start', 3)
    facts = [('FOCUS', 'Data Analytics · BI', 'SQL, Power BI, Excel'), ('CORE TOOLS', 'SQL · Python · Power BI', 'Cleaning, dashboards, KPIs'),
             ('EXPERIENCE', 'ERP & MIS reporting', 'SAP · TCS iON · Excel'), ('NOW  →  NEXT', 'Statistics  →  ML', 'Learning in public')]
    for i, (k, v, c) in enumerate(facts):
        x, y = 660 + (i % 2) * 248, 52 + (i // 2) * 120
        b += rect(x, y, 236, 106, 12, 'url(#pn)', LINE) + T(x + 18, y + 30, k, 10, HOT, 'm', 'start', 3, 700) + T(x + 18, y + 62, v, 15, BONE, 's', 'start', 0, 700) + T(x + 18, y + 84, c, 12, MIST)
    b += f'<path d="M44 326H1156" stroke="{LINE}"/>' + T(44, 364, 'ROADMAP', 11, SMOKE, 'm', 'start', 4, 700)
    x = 140
    for lab, st in (('Python', 1), ('SQL', 1), ('Excel', 1), ('Power BI', 1), ('Statistics', 2), ('Machine Learning', 0), ('AI', 0), ('Gen AI', 0), ('Agentic AI', 0)):
        txt = ('✓ ' if st == 1 else '') + lab
        col, stk = (GREEN, '#1f5a46') if st == 1 else (HOT, RED) if st == 2 else (SMOKE, LINE)
        w, c = chip(x, 346, txt, 30, 12, 'none', stk, col)
        b += (f'<g class="gw">{c}</g>' if st == 2 else c); x += w + 10
    save('about.svg', svg(1200, 400, b, "About: Chandan B, Data Analyst. I turn messy operational data into clear, trustworthy reports that people can act on. Roadmap: Python, SQL, Excel and Power BI complete; Statistics next, then Machine Learning, AI, Gen AI and Agentic AI."))

# ---------------------------------------------------------------- impact
def build_impact():
    items = [('~20%', ['higher data accuracy through', 'validation and reconciliation'], 'KEMS FORGINGS'),
             ('10–15%', ['fewer invoice discrepancies across', '50–80 invoices a day'], 'DIGHVIJAY PLASTICS'),
             ('10,000+', ['records cleaned and transformed', 'with SQL'], 'E-COMMERCE REVENUE ANALYSIS'),
             ('~40%', ['faster SQL queries after', 'optimisation'], 'SPOTIFY DATA ANALYSIS')]
    b = ''
    for i, (n, ls, src) in enumerate(items):
        x = 44 + i * 281
        if i: b += f'<path d="M{x-14} 36V214" stroke="{LINE}"/>'
        b += f'<g class="up" style="animation-delay:{i*.14:.2f}s">' + T(x, 118, n, 86, HOT, 'd', 'start', 2, extra=' filter="url(#bl)" opacity=".5"') + T(x, 118, n, 86, BONE, 'd', 'start', 2)
        b += T(x, 150, ls[0], 14, MIST) + T(x, 170, ls[1], 14, MIST) + T(x, 208, src, 10, SMOKE, 'm', 'start', 2.2) + '</g>'
    b += f'<rect x="44" y="30" width="60" height="3" rx="1.5" fill="{RED}" filter="url(#neon)"/>'
    save('impact.svg', svg(1200, 240, b, 'Impact: about 20 percent higher data accuracy at Kems Forgings; 10 to 15 percent fewer invoice discrepancies at Dighvijay Plastics; 10,000-plus records cleaned with SQL; about 40 percent faster SQL queries on the Spotify analysis.'))

# ---------------------------------------------------------------- stack + credentials
def build_stack():
    groups = [('LANGUAGES & DATABASES', ['Python', 'SQL', 'MySQL', 'SQLite', 'Joins', 'CTEs', 'Window Functions']),
              ('ANALYTICS & BI', ['Power BI', 'Excel', 'Pivot Tables', 'Data Cleaning', 'MIS Reporting', 'Dashboards', 'Statistics']),
              ('TOOLS & ERP', ['SAP ERP', 'TCS iON', 'Git', 'GitHub', 'VS Code', 'Jupyter'])]
    b = ''; y = 44
    for g, tools in groups:
        b += T(44, y, g, 11, HOT, 'm', 'start', 4, 700); y += 18; x = 44
        for t in tools:
            w, c = chip(x, y, t, 34, 13, wave=True)
            if x + w > 740: x = 44; y += 44; w, c = chip(x, y, t, 34, 13, wave=True)
            b += c; x += w + 10
        y += 66
    cx = 790
    b += rect(cx, 30, 366, 300, 16, 'url(#pn)', '#2c2c36') + comet(cx, 30, 366, 300, 16, 1.5) + T(cx + 24, 64, 'CREDENTIALS', 11, HOT, 'm', 'start', 4, 700)
    creds = [('FORAGE', 'Accenture North America', 'Data Analytics & Visualization'), ('LETSUPGRADE', 'SQL Bootcamp', ''), ('INFOSYS SPRINGBOARD', 'Microsoft Power BI', '')]
    yy = 96
    for iss, n1, n2 in creds:
        b += f'<rect x="{cx+24}" y="{yy}" width="3" height="{50 if n2 else 38}" rx="1.5" fill="{RED}" filter="url(#neon)"/>' + T(cx + 40, yy + 11, iss, 10, MIST, 'm', 'start', 2.4, 700) + T(cx + 40, yy + 33, n1, 16, BONE, 's', 'start', 0, 700)
        if n2: b += T(cx + 40, yy + 53, n2, 13, MIST)
        yy += 82 if n2 else 70
    save('stack.svg', svg(1200, 360, b, 'Tech stack. Languages and databases: Python, SQL, MySQL, SQLite, joins, CTEs, window functions. Analytics and BI: Power BI, Excel, pivot tables, data cleaning, MIS reporting, dashboards, statistics. Tools and ERP: SAP ERP, TCS iON, Git, GitHub, VS Code, Jupyter. Credentials: Accenture North America data analytics on Forage, Letsupgrade SQL Bootcamp, Infosys Springboard Microsoft Power BI.'))

# ---------------------------------------------------------------- projects
def build_projects():
    feat = [('01', 'SQL · POWER BI · REVENUE ANALYTICS', 'E-Commerce Pricing & Revenue Analysis', ['36 months of sales data cleaned in SQL and turned into', 'Power BI dashboards for revenue trends and regional performance.'], '10,000+ RECORDS CLEANED'),
            ('02', 'SQL · QUERY OPTIMISATION · ENGAGEMENT', 'Spotify Data Analysis & Insights', ['Normalised datasets, then analysed streaming trends with', 'CTEs, joins and window functions.'], '~40% FASTER QUERIES')]
    small = [('03', 'SQL · MYSQL · CTES', 'Retail Operations SQL Analytics'), ('04', 'PYTHON · SQLITE · OOP', 'EventSphere'), ('05', 'PYTHON · OOP · FILE HANDLING', 'Vehicle Rental System'),
             ('06', 'PYTHON · CRUD · CLI', 'Student Management System'), ('07', 'STATISTICS · EDA', 'Statistics for Data Science'), ('08', 'POWER BI · DATA MODELING', 'Power BI Analytics Journey')]
    b = ''
    for i, (n, g, t, d, m) in enumerate(feat):
        x = 44 + i * 568
        b += f'<g class="up" style="animation-delay:{i*.15:.2f}s">' + rect(x, 28, 544, 200, 16, 'url(#pn)', '#2c2c36') + f'<rect x="{x}" y="28" width="544" height="3" rx="1.5" fill="{RED}" filter="url(#neon)"/>' + comet(x, 28, 544, 200, 16, i * 2.2)
        b += T(x + 24, 62, n, 12, HOT, 'm', 'start', 3, 700) + T(x + 56, 62, g, 10, MIST, 'm', 'start', 2.4, 700) + T(x + 24, 112, t, 32, BONE, 'd', 'start', 1.5)
        b += T(x + 24, 142, d[0], 13.5, MIST) + T(x + 24, 162, d[1], 13.5, MIST)
        w, c = chip(x + 24, 182, m, 30, 11, '#1b0d11', RED, HOT, 14, 7.6); b += c + '</g>'
    for i, (n, g, t) in enumerate(small):
        x, y = 44 + (i % 3) * 380, 252 + (i // 3) * 116
        b += f'<g class="up" style="animation-delay:{.3+i*.08:.2f}s">' + rect(x, y, 352, 100, 14, 'url(#pn)', LINE, extra=f' class="wv" style="animation-delay:{i*.6:.1f}s"') + T(x + 20, y + 30, n, 11, HOT, 'm', 'start', 3, 700) + T(x + 20, y + 66, t, 25, BONE, 'd', 'start', 1.2) + T(x + 20, y + 86, g, 9.5, SMOKE, 'm', 'start', 2.2) + '</g>'
    save('projects.svg', svg(1200, 486, b, 'Eight projects. Featured: E-Commerce Pricing and Revenue Analysis (SQL, Power BI) and Spotify Data Analysis (SQL). Also: Retail Operations SQL Analytics, EventSphere, Vehicle Rental System, Student Management System, Statistics for Data Science, Power BI Analytics Journey.'))

# ---------------------------------------------------------------- connect + footer
def build_connect():
    b = '<g class="br">' + T(44, 150, "LET'S BUILD", 128, HOT, 'd', 'start', 3, extra=' filter="url(#bl)" opacity=".5"') + '</g>' + T(44, 150, "LET'S BUILD", 128, 'url(#nm)', 'd', 'start', 3) + T(48, 196, 'Open to conversations about data, dashboards and analytics.', 18, MIST)
    x = 44
    for lab in ('GITHUB  ·  chandanB47', 'LINKEDIN  ·  chandan47', 'PORTFOLIO  ·  chandanb47.github.io'):
        w, c = chip(x, 232, lab, 40, 12, '#12121a', '#34343e', BONE, 20, 8.2); b += c + comet(x, 232, w, 40, 20, x / 90, HOT, 5); x += w + 14
    b += f'<circle class="pl" cx="1010" cy="140" r="70" fill="none" stroke="{RED}" stroke-width="2"/><circle class="pl" style="animation-delay:1.5s" cx="1010" cy="140" r="70" fill="none" stroke="{RED}" stroke-width="2"/>' + f'<circle class="pl" style="animation-delay:3s" cx="1010" cy="140" r="70" fill="none" stroke="{HOT}" stroke-width="2"/>' + '<g filter="url(#neon)">' + cmark(962, 82, 3.3, HOT, 4) + '</g>'
    b += embers(1200, 310, 12, 3)
    save('connect.svg', svg(1200, 310, b, "Let's build. Connect on GitHub (chandanB47), LinkedIn (chandan47) or my portfolio (chandanb47.github.io)."))

def build_footer():
    b = '<g class="br" filter="url(#bl)">' + cmark(552, 26, 1.1, RED, 8) + '</g><g filter="url(#neon)">' + cmark(552, 26, 1.1, HOT) + '</g>' + T(600, 52, 'SERIES', 14, MIST, 'm', 'start', 7, 700)
    b += T(600, 96, 'LEARN  ·  PRACTICE  ·  BUILD  ·  DOCUMENT  ·  IMPROVE', 12, SMOKE, 'm', 'middle', 4) + T(600, 126, 'MAKING DATA USEFUL, CLEAR AND ACTIONABLE  —  © 2026 CHANDAN B', 10, '#4d4c54', 'm', 'middle', 2.4)
    save('footer.svg', svg(1200, 150, b, 'Learn, practice, build, document, improve — making data useful, clear and actionable. C Series, Chandan B.', glow=False, fx='full', seed=5, nstars=9, big=2))

if __name__ == '__main__':
    build_hero(); build_about(); build_impact(); build_stack(); build_projects(); build_connect(); build_footer()
    for n, num, t, s in (('about', '01', 'ABOUT ME', 'Hello, I’m Chandan.'), ('impact', '02', 'IMPACT', 'Results, not adjectives.'), ('stack', '03', 'STACK', 'The tools I reach for.'),
                         ('projects', '04', 'PROJECTS', 'Built, not just studied.'), ('activity', '05', 'ACTIVITY', 'Showing up, every day.'), ('connect', '06', 'CONNECT', 'Let’s learn, build and grow.')):
        build_title(n, num, t, s)
    print('built', len(os.listdir(OUT)), 'files')
