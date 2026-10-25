import math
BG='#fff6e8'; CY='#e8590c'; MG='#d6246e'; VI='#9b2f8f'; LM='#1f9d55'
TX='#2a1a2e'; MU='#5c4a5e'; DM='#8c7a89'; LN='#e6d5bd'
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def M(x,y,s,size=12,fill=MU,anchor='start',ls=0,extra=''):
    w=len(s)*(0.6*size+ls)
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" class="m" text-anchor="{anchor}" textLength="{w:.1f}" lengthAdjust="spacing"{extra}>{esc(s)}</text>'
def D(x,y,s,size,fill=TX,anchor='start',extra='',k=0.64):
    w=len(s)*k*size
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" class="d" text-anchor="{anchor}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs"{extra}>{esc(s)}</text>'
def poly(x,y,w,h,c=14):
    return f'{x+c},{y} {x+w},{y} {x+w},{y+h-c} {x+w-c},{y+h} {x},{y+h} {x},{y+c}'
def panel(x,y,w,h,stroke=LN,c=14,fill='url(#pn)',sw=1.2,extra=''):
    return f'<polygon points="{poly(x,y,w,h,c)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
def check(x,y,col=LM,sw=2.4):
    return f'<path d="M{x} {y} l3.6 3.6 l7.2 -8" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def glitch(x,y,s,size,anchor='start',k=0.64):
    o=' opacity=".85"'
    return (f'<g class="g1">{D(x,y,s,size,MG,anchor,o,k)}</g>'
            f'<g class="g2">{D(x,y,s,size,CY,anchor,o,k)}</g>'
            f'{D(x,y,s,size,"url(#tx)",anchor," style=\'filter:drop-shadow(0 0 14px rgba(214,36,110,.22))\'",k)}')
def count(x,y,size,n,dur,begin,fill,anchor='start'):
    out=''; r=[0.0]+[round(0.30+0.55*k/n,4) for k in range(n)]
    w=0.62*size
    for d in range(n+1):
        if d==0: vals,kts,b='1;0',f'0;{r[1]:.4f}','1'
        elif d<n: vals,kts,b='0;1;0',f'0;{r[d]:.4f};{r[d+1]:.4f}','0'
        else: vals,kts,b='0;0;1',f'0;{r[d]:.4f};1','0'
        out+=(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" class="d" text-anchor="{anchor}" opacity="{b}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{d}'
              f'<animate attributeName="opacity" values="{vals}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" begin="{begin}s" fill="freeze"/></text>')
    return out
def segs(x,y,n,filled,w,h,gap,col=CY,nxt=None,delay=0.6,stagger=0.08):
    out=''
    for i in range(n):
        sx=x+i*(w+gap)
        if i<filled:
            out+=(f'<rect x="{sx}" y="{y}" width="{w}" height="{h}" fill="{col}" opacity="0"><animate attributeName="opacity" values="0;1" dur=".25s" begin="{delay+i*stagger:.2f}s" fill="freeze"/></rect>')
        elif nxt is not None and i==nxt:
            out+=f'<rect x="{sx}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{MG}" stroke-width="1.5" class="pulse"/>'
        else:
            out+=f'<rect x="{sx}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{LN}" stroke-width="1.2"/>'
    return out
CSS='''.d{font-family:"Arial Black","Segoe UI Black",Impact,"Helvetica Neue",Arial,sans-serif;font-weight:900}
.m{font-family:"SF Mono","Cascadia Mono",Consolas,"Courier New",monospace;font-weight:400}
.in{animation:in .9s cubic-bezier(.16,1,.3,1) both}
@keyframes in{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.sl{animation:sl .9s cubic-bezier(.16,1,.3,1) both}
@keyframes sl{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:none}}
.blink{animation:bl 1s steps(2,end) infinite}
@keyframes bl{50%{opacity:0}}
.pulse{animation:pu 2s ease-in-out infinite}
@keyframes pu{50%{opacity:.3}}
.g1{animation:g1 5s infinite steps(1)}
@keyframes g1{0%,90%,100%{transform:translate(0,0)}91%{transform:translate(-6px,1px)}93%{transform:translate(5px,-1px)}95%{transform:translate(-3px,0)}}
.g2{animation:g2 5s infinite steps(1)}
@keyframes g2{0%,90%,100%{transform:translate(0,0)}91%{transform:translate(6px,-1px)}93%{transform:translate(-5px,1px)}95%{transform:translate(3px,0)}}
.role{animation:role 16s infinite both}
@keyframes role{0%{opacity:0;transform:translateY(10px)}3%,22%{opacity:1;transform:none}26%,100%{opacity:0;transform:translateY(-8px)}}
.sc{animation:sc 7s linear infinite}
@keyframes sc{from{transform:translateY(-80px)}to{transform:translateY(var(--h))}}
@keyframes fl{from{transform:translateX(-200px)}to{transform:translateX(620px)}}
.fl{animation:fl 11s ease-in-out infinite alternate}
@keyframes rb{to{filter:hue-rotate(360deg)}}
.rb{animation:rb 7s linear infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.sc{display:none}}'''
BGS={'hero':('#fffdf7','#fbf0dc','#f5dfc3'),'journey':('#ffffff','#fdf6ea','#f8e8d2'),'stack':('#fffaf0','#f9ecd6','#f3d9bc'),
     'projects':('#fffdf9','#fcefe0','#f7dcc8'),'jet':('#fffbf2','#faf0dd','#f4e0c4'),'connect':('#ffffff','#fdf3e3','#f7e1cc')}
import random as _r
def stars(W,H,n=46,seed=5):
    _r.seed(seed); o=''
    for _ in range(n):
        d=_r.uniform(2.5,6)
        o+=f'<circle cx="{_r.randint(30,W-30)}" cy="{_r.randint(80,H-30)}" r="{_r.choice([.7,1,1.3])}" fill="#e8590c" opacity="0"><animate attributeName="opacity" values="0;.45;0" dur="{d:.1f}s" begin="{-_r.uniform(0,d):.1f}s" repeatCount="indefinite"/></circle>'
    return o
def frame(W,H,left,right,body,extra_defs='',scene='',bg=None):
    bg=bg or BGS['hero']
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<style>{CSS}.sc{{--h:{H}px}}</style>
<defs>
<linearGradient id="bgg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{bg[0]}"/><stop offset=".55" stop-color="{bg[1]}"/><stop offset="1" stop-color="{bg[2]}"/></linearGradient>
<linearGradient id="ng" x1="0" x2="1"><stop stop-color="{CY}"/><stop offset=".5" stop-color="{VI}"/><stop offset="1" stop-color="{MG}"/></linearGradient>
<linearGradient id="tx" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#2a1a2e"/><stop offset=".55" stop-color="#6b1d4a"/><stop offset="1" stop-color="{MG}"/></linearGradient>
<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff" stop-opacity=".88"/><stop offset="1" stop-color="#fff1dc" stop-opacity=".86"/></linearGradient>
<linearGradient id="bar" x1="0" x2="1"><stop stop-color="{CY}"/><stop offset="1" stop-color="{VI}"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{CY}" stop-opacity="0"/><stop offset=".5" stop-color="{CY}" stop-opacity=".10"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></linearGradient>
<radialGradient id="gc"><stop stop-color="{CY}" stop-opacity=".20"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>
<radialGradient id="gm"><stop stop-color="{MG}" stop-opacity=".12"/><stop offset="1" stop-color="{MG}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{CY}" stroke-opacity=".07"/></pattern>
<pattern id="crt" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#5a3416" opacity=".05"/></pattern>
<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#6b3a1a" stop-opacity="0"/><stop offset="1" stop-color="#6b3a1a" stop-opacity=".15"/></radialGradient>
<filter id="bl" x="-20%" y="-300%" width="140%" height="700%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .2 0 0 0 0 .1 0 0 0 0 .05 1 0 0 0 0"/></filter>
<clipPath id="outer"><polygon points="{poly(1,1,W-2,H-2,30)}"/></clipPath>
{extra_defs}
</defs>
<title id="t">{esc(left[1])}</title><desc id="d">{esc(left[2])}</desc>
<g clip-path="url(#outer)">
<rect width="{W}" height="{H}" fill="url(#bgg)"/>{stars(W,H)}
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<ellipse cx="180" cy="{H-40}" rx="460" ry="260" fill="url(#gc)"/><ellipse cx="{W-100}" cy="60" rx="380" ry="240" fill="url(#gm)"/>
<rect class="sc" x="0" y="0" width="{W}" height="80" fill="url(#scan)"/>
{M(44,44,left[0],11,MU,ls=1.6)}{right}
<path d="M44 66H{W-44}" stroke="{LN}" stroke-width="1.5"/><rect x="44" y="64" width="90" height="3" fill="{CY}"/>
{body}
<rect width="{W}" height="{H}" fill="url(#vg)" pointer-events="none"/>
<g class="fl" pointer-events="none"><ellipse cx="{int(W*.2)}" cy="{int(H*.30)}" rx="440" ry="3" fill="#ffb347" opacity=".40" filter="url(#bl)"/><ellipse cx="{int(W*.2)}" cy="{int(H*.30)}" rx="150" ry="1.2" fill="#fff4d6" opacity=".95"/><ellipse cx="{int(W*.2)+380}" cy="{int(H*.30)}" rx="60" ry="1" fill="{MG}" opacity=".4"/></g>
<rect width="{W}" height="{H}" fill="#000" filter="url(#grain)" opacity=".08" pointer-events="none"/>
<rect width="{W}" height="{H}" fill="url(#crt)" pointer-events="none"/>
<rect width="{W}" height="16" fill="#2a1a2e"/><rect y="{H-16}" width="{W}" height="16" fill="#2a1a2e"/>
<circle cx="46" cy="8" r="3" fill="{MG}" class="blink"/>{M(56,11,"REC",8,MG,ls=1.6)}{M(96,11,scene,8,"#e9d8c9",ls=1.6)}{M(W-46,11,"CB PRODUCTIONS / 2026",8,"#e9d8c9","end",1.6)}
<path d="M0 16H{W}M0 {H-16}H{W}" stroke="{CY}" stroke-width="1.2" opacity=".7"/>
</g>
<polygon points="{poly(1,1,W-2,H-2,30)}" fill="none" stroke="url(#ng)" stroke-width="2"/>
<path d="M26 66V26H66M{W-26} {H-66}V{H-26}H{W-66}" fill="none" stroke="{CY}" stroke-width="2" opacity=".8"/>
</svg>'''
def rt(W,s,col=MU): return M(W-44,44,s,11,col,'end',1.6)
