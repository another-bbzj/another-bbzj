"""Cinematic SVG profile with the owner's exact original lettering.

Run: python gen.py (requires fonttools and brotli).
No scripts or external resources are required by the generated SVG images.
"""
from pathlib import Path
import base64, math, random, re
import typekit
from typekit import text, line, rect, circle, SIGNATURE, ROOT, ASSETS

P={}
CSS='''
@keyframes breathe{0%,100%{opacity:.45;transform:translate(-40px,12px) scale(.94)}50%{opacity:.9;transform:translate(36px,-14px) scale(1.05)}}
@keyframes silk{0%,100%{transform:translate(0,0) rotate(-4deg)}50%{transform:translate(-18px,18px) rotate(5deg)}}
@keyframes glint{0%,12%{transform:translateX(-1100px)}65%,100%{transform:translateX(1100px)}}
@keyframes drift{0%,100%{transform:translateY(0);opacity:.3}50%{transform:translateY(-15px);opacity:.75}}
@keyframes orbit{to{stroke-dashoffset:-500}}
@keyframes frame{to{transform:translateX(-1152px)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
@keyframes pan{0%,100%{transform:translateY(0)}50%{transform:translateY(-112px)}}
@keyframes flight{0%,10%{offset-distance:0%;opacity:0}14%{opacity:1}74%{offset-distance:100%;opacity:1}78%,100%{offset-distance:100%;opacity:0}}
@keyframes trace{0%{stroke-dashoffset:560}80%,100%{stroke-dashoffset:0}}
@keyframes ring{0%,62%{transform:scale(.7);opacity:0}70%{opacity:.7}100%{transform:scale(1.4);opacity:0}}
@keyframes reel{0%,20%{transform:translateY(0)}30%,50%{transform:translateY(-88px)}60%,80%{transform:translateY(-176px)}90%,100%{transform:translateY(-264px)}}
.reel{animation:reel 12s cubic-bezier(.65,0,.35,1) infinite}
.breathe{transform-origin:750px 130px;animation:breathe 10s ease-in-out infinite}.silk{transform-origin:780px 170px;animation:silk 12s ease-in-out infinite}
.glint{animation:glint 9s cubic-bezier(.3,0,.6,1) infinite}.dust{animation:drift 6s ease-in-out infinite}.flow{stroke-dasharray:2 15;animation:orbit 18s linear infinite}
.frames{animation:frame 1.2s steps(6) infinite}.float{animation:float 4s ease-in-out infinite}.pan{animation:pan 15s ease-in-out infinite}
.flight{offset-path:path('M540 260 Q710 20 938 122');offset-rotate:auto;animation:flight 6s cubic-bezier(.22,.7,.4,1) infinite}
.trace{stroke-dasharray:560;animation:trace 6s ease-out infinite}.ring{transform-box:fill-box;transform-origin:center;animation:ring 6s ease-out infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.glint,.flight,.ring{display:none}.trace{stroke-dashoffset:0}}
'''

def document(name,w,h,content,accent,title,light=False):
    # Static fine grain and slowly moving illumination are separate layers.
    defs=f'''<defs>
<radialGradient id="bloom"><stop stop-color="{accent}" stop-opacity=".38"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="metal" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{P['metal0']}"/><stop offset=".28" stop-color="{P['metal1']}"/><stop offset=".46" stop-color="{P['metal2']}"/><stop offset=".56" stop-color="{P['metal0']}"/><stop offset=".76" stop-color="{P['metal1']}"/><stop offset=".88" stop-color="{P['metal2']}"/><stop offset="1" stop-color="{P['metal0']}"/></linearGradient>
<linearGradient id="shine"><stop stop-color="{P['ink']}" stop-opacity="0"/><stop offset=".5" stop-color="{P['ink']}" stop-opacity=".65"/><stop offset="1" stop-color="{P['ink']}" stop-opacity="0"/></linearGradient>
<linearGradient id="fade"><stop stop-color="{P['bg']}"/><stop offset=".57" stop-color="{P['bg']}" stop-opacity="0"/></linearGradient>
<linearGradient id="vertical" x2="0" y2="1"><stop stop-color="{P['bg']}"/><stop offset=".2" stop-color="{P['bg']}" stop-opacity="0"/><stop offset=".78" stop-color="{P['bg']}" stop-opacity="0"/><stop offset="1" stop-color="{P['bg']}"/></linearGradient>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".78" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
<clipPath id="canvas"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16"/></clipPath>
</defs>'''
    out=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{title}</title><style>{CSS}</style>{defs}'
    out+=f'<g clip-path="url(#canvas)"><path fill="{P["bg"]}" d="M0 0H{w}V{h}H0Z"/>'
    out+=f'<ellipse class="breathe" cx="800" cy="140" rx="390" ry="260" fill="url(#bloom)"/>'
    out+=content
    out+=f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity="{.035 if not light else .045}" style="mix-blend-mode:{"screen" if not light else "multiply"}" pointer-events="none"/>'
    out+=f'</g><rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="16" fill="none" stroke="{P["edge"]}" stroke-width="1.5"/></svg>'
    (ASSETS/(name+'.svg')).write_text(out,encoding='utf-8')

def dust(w,h):
    rng=random.Random(58)
    return ''.join(f'<circle class="dust" cx="{rng.uniform(20,w-20):.2f}" cy="{rng.uniform(15,h-15):.2f}" r="{rng.uniform(.4,1.3):.2f}" fill="{P["metal1"]}" opacity=".4" style="animation-delay:-{rng.uniform(0,6):.1f}s"/>' for _ in range(65))

def ribbons():
    result='<g class="silk" fill="none" stroke="url(#metal)">'
    # Tightly layered curves form a continuous folded metallic ribbon.
    for i in range(64):
        t=i/63
        result+=f'<path d="M{565+t*88:.1f} 370 C{980-t*170:.1f} {270-t*155:.1f} {570+t*295:.1f} {45+t*165:.1f} {1030+t*75:.1f} {-70+t*65:.1f}" stroke-width="1.5" opacity="{.3+.7*math.sin(t*math.pi):.3f}"/>'
    result+='</g>'
    result+='<g class="silk" style="animation-delay:-6s" fill="none" stroke="url(#metal)" opacity=".3">'
    for i in range(24):
        result+=f'<path d="M{670+i*3} 390 C{500+i*4} 120 {1120-i*3} 220 {990+i*5} -50" stroke-width=".7"/>'
    return result+'</g>'

def hero(light,mobile=False):
    w,h=(600,370) if mobile else (1000,350)
    sig='<g transform="translate(38 72) scale(1.85) translate(-28 -74)">'+SIGNATURE.replace('#ece6dc',P['ink'])+'</g>'
    s=ribbons() if not mobile else '<g opacity=".4" transform="translate(-420 0)">'+ribbons()+'</g>'
    s+=dust(w,h)
    if not mobile:s+='<rect width="720" height="350" fill="url(#fade)"/>'
    s+=line(34,28,w-34,28,P['edge'])
    s+=text('EMBEDDED × AI AGENT',36,54,13,P['accent'],face='mono',spacing=2)
    if not mobile:s+=text('ZOU JUN',282,159,23,P['muted'],face='tight',spacing=4)
    else:s+=text('ZOU JUN',282,159,23,P['muted'],face='tight',spacing=4)
    s+=sig
    s+='<mask id="name">'+sig.replace(P['ink'],'#ffffff')+'</mask><g mask="url(#name)"><rect class="glint" x="0" y="65" width="230" height="170" fill="url(#shine)" transform="skewX(-22)"/></g>'
    s+=text('在 MCU 上写确定性，在 Agent 里找协作。',38,260,23 if not mobile else 21)
    s+=text('RoboMaster / 智能车嵌入式开发',38,294,17,P['muted'])
    s+=text('东北大学秦皇岛分校',38,321,15,P['muted'])
    if not mobile:s+=text('FIRMWARE / AGENTS / OPEN SOURCE',645,322,12,P['accent'],face='mono')
    document('header'+('-mobile' if mobile else '')+('-light' if light else ''),w,h,s,P['accent'],'邹俊 · 在 MCU 上写确定性，在 Agent 里找协作。',light)

def trajectory():
    s=''
    for r in [26,52,78]:
        s+=f'<ellipse cx="938" cy="122" rx="{r*.42}" ry="{r}" fill="none" stroke="{P["accent"]}" stroke-opacity=".3"/>'
    s+=f'<path d="M540 260Q710 20 938 122" fill="none" stroke="{P["accent"]}" stroke-opacity=".15"/>'
    s+=f'<path class="trace" d="M540 260Q710 20 938 122" fill="none" stroke="url(#metal)" stroke-width="2"/>'
    s+=f'<g class="flight"><path d="M-26 -3L12 0L-26 3L-19 0Z" fill="{P["metal2"]}"/><path d="M-27 -8L-15 0L-27 8L-23 0Z" fill="{P["accent"]}"/></g>'
    s+=f'<ellipse class="ring" cx="938" cy="122" rx="35" ry="80" fill="none" stroke="{P["metal2"]}"/>'
    for i in range(6):s+=line(560+i*60,282,560+i*60,288,P['edge'])
    s+=text('STM32H723 / MOTOR CONTROL',604,309,11,P['muted'],face='mono')
    return s

def card(kind,light,cover=False):
    title,sub,stack,accent={
        'cat':('claude-agent-team','派工、回报、交接，实时可见。','PYTHON / ZERO DEPS / LOCAL',P['accent']),
        'dsh':('dsh-agent-team','DeepSeek Harness 插件','JAVASCRIPT / ESM / NPM',P['blue']),
        'dart':('dart','RoboMaster 飞镖发射 / 换弹固件','C / C++ / STM32H723',P['accent'])}[kind]
    idx={'cat':'01','dsh':'02','dart':'03'}[kind]
    s=dust(1000,330)
    if kind in ['cat','dsh']:
        s+='<g opacity=".35" transform="translate(0 -20)">'+ribbons()+'</g>'
        words=['Plan.','Build.','Ship.','Plan.'] if kind=='cat' else ['Dispatch.','Observe.','Deliver.','Dispatch.']
        s+='<clipPath id="reel-window"><rect x="573" y="73" width="390" height="130"/></clipPath><g clip-path="url(#reel-window)"><g class="reel">'
        for i,word in enumerate(words):s+=text(word,587,164+i*88,67,P['ink'],face='serif')
        s+='</g></g>'
        s+=line(587,220,936,220,P['edge'])
        s+=text('A TEAM / IN MOTION' if kind=='cat' else 'ONE PLUGIN. ALL CONNECTED.',587,250,12,accent,face='mono')
    else:s+=trajectory()
    kicker=(('CLAUDE CODE / AGENT TEAM' if kind=='cat' else 'DEEPSEEK HARNESS / AGENT TEAM') if cover else idx+' / '+{'cat':'AGENT TEAM','dsh':'HARNESS PLUGIN','dart':'EMBEDDED SYSTEMS'}[kind])
    s+=text(kicker,36,48,12,accent,face='mono',spacing=1.5)
    s+=text(title,36,124,46 if kind!='dart' else 68,P['ink'],face='serif')
    s+=text(sub,38,175,21)
    if kind=='dsh':s+=text('可视化指挥室',38,208,20,P['muted'])
    s+=line(38,253,460,253,P['edge'])
    s+=text(stack,38,286,12,P['muted'],face='mono')
    document(('readme-' if cover else 'card-')+kind+('-light' if light else ''),1000,330,s,accent,title+' · '+sub,light)

def footer(light):
    s='<g opacity=".23" transform="translate(0 -80)">'+ribbons()+'</g>'
    s+=text('Thanks for reading.',36,56,33,face='serif')
    s+=text('欢迎 Star、Issue 与 PR',38,91,16,P['muted'])
    s+=text('GITHUB.COM/ANOTHER-BBZJ',680,78,12,P['muted'],face='mono')
    document('footer'+('-light' if light else ''),1000,125,s,P['accent'],'Thanks for reading. 欢迎 Star、Issue 与 PR',light)

for light in [False,True]:
    P=dict(bg='#f5f0e5',ink='#302b23',muted='#746857',edge='#d9cfbe',accent='#a46c32',blue='#536a7b',metal0='#a47b4b',metal1='#c3a46e',metal2='#fff8df') if light else dict(bg='#13120f',ink='#f2e9da',muted='#b7aa96',edge='#3b3226',accent='#d5aa69',blue='#9db7c9',metal0='#49321b',metal1='#c29454',metal2='#ffe6b0')
    typekit.P=P
    for mobile in [False,True]:hero(light,mobile)
    for kind in ['cat','dsh','dart']:card(kind,light)
    for kind in ['cat','dsh']:card(kind,light,True)
    footer(light)
print('Generated cinematic assets with original typography and reduced-motion support.')
