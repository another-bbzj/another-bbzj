import base64, io, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset
G="/usr/share/fonts/truetype/sand-box/google/"
FONTS={
 "D":(G+"Space Grotesk/SpaceGrotesk-VariableFont_wght.ttf",None,700),
 "I":(G+"Inter/Inter-VariableFont_opsz,wght.ttf",None,500),
 "IB":(G+"Inter/Inter-VariableFont_opsz,wght.ttf",None,700),
 "M":(G+"JetBrains Mono/JetBrainsMono-VariableFont_wght.ttf",None,500),
 "C":("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",2,None),
 "CB":("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",2,None),
}
_cache={}
def load(k):
    p,idx,w=FONTS[k]
    f=TTFont(p,fontNumber=idx) if idx is not None else TTFont(p)
    if 'fvar' in f:
        axes={a.axisTag:a.defaultValue for a in f['fvar'].axes}
        axes['wght']=w
        if 'opsz' in axes: axes['opsz']=24
        f=instancer.instantiateVariableFont(f,axes)
    return f
def face(k,text):
    f=load(k)
    o=subset.Options(); o.flavor='woff2'; o.layout_features=['kern','liga']; o.name_IDs=[]; o.notdef_outline=True
    s=subset.Subsetter(o); s.populate(text=text+" "); s.subset(f)
    b=io.BytesIO(); f.flavor='woff2'; f.save(b)
    return "@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');}"%(
        "f"+k,base64.b64encode(b.getvalue()).decode())
import re
def build(name,w,h,body):
    # collect text per font class: elements use class="d|i|ib|m|c|cb"; latin+cjk mix => font stack
    texts=re.findall(r'>([^<>]+)<',body)
    alltext="".join(texts)
    css="".join(face(k,alltext) for k in FONTS)
    css+="""text{font-family:'fI','fC',sans-serif;fill:#c9d1e0}
.d{font-family:'fD','fCB';font-weight:700}.ib{font-family:'fIB','fCB'}.m{font-family:'fM','fC';}
.c{font-family:'fI','fC'}.cb{font-family:'fIB','fCB'}"""
    # ensure needed fonts embedded: mark usage
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{css}</style>
<defs>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".045"/></pattern>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff8a3d"/><stop offset=".5" stop-color="#7c5cff" stop-opacity=".5"/><stop offset="1" stop-color="#2ee6c8"/></linearGradient>
<linearGradient id="txt" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#ffd3b0"/><stop offset="1" stop-color="#ff8a3d"/></linearGradient>
<linearGradient id="txt2" x1="0" x2="1"><stop offset="0" stop-color="#9f8bff"/><stop offset="1" stop-color="#2ee6c8"/></linearGradient>
<radialGradient id="g1"><stop offset="0" stop-color="#ff7a2f" stop-opacity=".35"/><stop offset="1" stop-color="#ff7a2f" stop-opacity="0"/></radialGradient>
<radialGradient id="g2"><stop offset="0" stop-color="#6d4cff" stop-opacity=".35"/><stop offset="1" stop-color="#6d4cff" stop-opacity="0"/></radialGradient>
<radialGradient id="g3"><stop offset="0" stop-color="#18d6b5" stop-opacity=".25"/><stop offset="1" stop-color="#18d6b5" stop-opacity="0"/></radialGradient>
<clipPath id="clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="#090b11"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
{body}
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="url(#edge)" stroke-opacity=".75" stroke-width="1.5"/>
</svg>'''
    # make sure 'fD','fM','fIB','fCB' are included when classes used
    open(f"assets/{name}.svg","w").write(svg)
    print(name, os.path.getsize(f"assets/{name}.svg")//1024,"KB")

def chips(x,y,items,mono=True,h=26,gap=8,size=13):
    out=[];cx=x
    for t,col in items:
        wdt=int(len(t.encode('utf-8'))*0+sum(14 if ord(c)>255 else 8.2 for c in t)*size/13)+22
        out.append(f'<rect x="{cx}" y="{y}" width="{wdt}" height="{h}" rx="7" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".45"/>'
                   f'<text x="{cx+wdt/2}" y="{y+h/2+4.5}" text-anchor="middle" class="m" font-size="{size}" style="fill:{col}">{t}</text>')
        cx+=wdt+gap
    return "".join(out)

OR,VI,TE,BL="#ff8a3d","#9f8bff","#2ee6c8","#6aa8ff"
# ---------- header ----------
term=[("$ whoami","#7d8799"),("邹俊 · Zou Jun  @another-bbzj","#e6ebf5"),("$ cat focus.txt","#7d8799"),
      ("embedded  → STM32 · 电机控制 · 状态机",OR),("ai-agent  → Claude Code 多智能体团队",VI),
      ("tooling   → 看得见、算得清、验得了",TE),("$ ","#7d8799")]
tl="".join(f'<text x="790" y="{122+i*26}" class="m" font-size="14" style="fill:{c}">{t}</text>' for i,(t,c) in enumerate(term))
header=f'''
<circle cx="180" cy="40" r="300" fill="url(#g1)"><animate attributeName="r" values="280;330;280" dur="8s" repeatCount="indefinite"/></circle>
<circle cx="1050" cy="330" r="320" fill="url(#g2)"><animate attributeName="r" values="330;280;330" dur="9s" repeatCount="indefinite"/></circle>
<circle cx="640" cy="380" r="220" fill="url(#g3)"/>
<rect x="0" y="0" width="1200" height="2" fill="{OR}" opacity=".5"><animate attributeName="y" values="0;380;0" dur="10s" repeatCount="indefinite"/></rect>
<text x="56" y="64" class="m" font-size="13" letter-spacing="3" style="fill:{OR}">EMBEDDED × AI AGENT · NEUQ</text>
<text x="56" y="150" class="d" font-size="78" fill="url(#txt)" style="fill:url(#txt)">邹俊</text>
<text x="246" y="150" class="d" font-size="44" style="fill:#e6ebf5">Zou Jun</text>
<text x="56" y="198" class="cb" font-size="24" style="fill:#e6ebf5">在 MCU 上写确定性，在 Agent 里找协作。</text>
<text x="56" y="232" class="c" font-size="15" style="fill:#9aa4b8">东北大学秦皇岛分校 · RoboMaster / 智能车嵌入式 · Claude Code 多智能体工具作者</text>
{chips(56,262,[("C / C++",BL),("STM32H7",OR),("HAL · CubeMX",OR),("Python",VI),("Node.js",TE),("Claude Code",OR)])}
<text x="56" y="336" class="m" font-size="12" style="fill:#5d6678">// firmware that never misses a beat · agents you can actually watch</text>
<rect x="760" y="56" width="400" height="268" rx="14" fill="#0e1119" fill-opacity=".85" stroke="#ffffff" stroke-opacity=".08"/>
<circle cx="782" cy="78" r="5" fill="#ff5f57"/><circle cx="800" cy="78" r="5" fill="#febc2e"/><circle cx="818" cy="78" r="5" fill="#28c840"/>
<text x="1140" y="82" text-anchor="end" class="m" font-size="11" style="fill:#5d6678">zsh — 80×24</text>
<line x1="760" y1="96" x2="1160" y2="96" stroke="#fff" stroke-opacity=".06"/>
{tl}
<rect x="808" y="268" width="9" height="17" fill="{OR}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>
'''
build("header",1200,380,header)

# ---------- cards ----------
def card(name,w,h,idx,title,sub,lines,tags,accent,glow):
    ls="".join(f'<circle cx="38" cy="{h-172+i*28-4}" r="3" fill="{accent}"/><text x="52" y="{h-172+i*28}" class="c" font-size="14.5" style="fill:#c9d1e0">{t}</text>' for i,t in enumerate(lines))
    body=f'''<circle cx="{w-40}" cy="20" r="260" fill="url(#{glow})"><animate attributeName="opacity" values=".7;1;.7" dur="6s" repeatCount="indefinite"/></circle>
<text x="30" y="46" class="m" font-size="12" letter-spacing="2" style="fill:{accent}">{idx}</text>
<text x="30" y="88" class="d" font-size="32" style="fill:#f2f5fa">{title}</text>
<text x="30" y="116" class="c" font-size="14" style="fill:#9aa4b8">{sub}</text>
<line x1="30" y1="134" x2="{w-30}" y2="134" stroke="#fff" stroke-opacity=".07"/>
{ls}
{chips(30,h-50,tags,size=12,h=24)}
<text x="{w-30}" y="46" text-anchor="end" class="m" font-size="12" style="fill:#5d6678">open ↗</text>'''
    build(name,w,h,body)
card("card-cat",590,330,"01 · FLAGSHIP · PYTHON","claude-agent-team","Claude Code 部门制 Agent 团队 + 本机实时看板",
 ["常驻分部门 Agent，办公协议写进项目","子代理派工 / 回报 / 交接实时可视化","运行时零依赖：仅 Python 3.8+ 标准库","看板只绑定 127.0.0.1，不调用模型 API"],
 [("v1.4.2",OR),("zero-deps",TE),("Win·macOS·Linux",BL),("MIT",VI)],OR,"g1")
card("card-dsh",590,330,"02 · PLUGIN · JAVASCRIPT","dsh-agent-team","DeepSeek Harness 插件 · 可视化指挥室看板",
 ["8 位常驻成员 · 6 个部门，按岗位派工","每个子代理一只动画桌宠（自带 13 只）","token / 成本取真实 usage，未知模型不瞎算","纯 ESM，无需构建，一个 npm 包即一个 bundle"],
 [("Node ≥20",TE),("npm",OR),("ESM",BL),("MIT",VI)],VI,"g2")
dart=f'''<circle cx="1100" cy="40" r="300" fill="url(#g3)"/>
<text x="30" y="46" class="m" font-size="12" letter-spacing="2" style="fill:{TE}">03 · FIRMWARE · C</text>
<text x="30" y="92" class="d" font-size="34" style="fill:#f2f5fa">dart</text>
<text x="130" y="92" class="cb" font-size="20" style="fill:#e6ebf5">征龙凌沧 26 赛季 · RoboMaster 飞镖发射 / 换弹固件</text>
<text x="30" y="124" class="c" font-size="14.5" style="fill:#9aa4b8">STM32H723 上的发射、换弹流程状态机与电机控制。</text>
{chips(30,150,[("STM32H723",TE),("state-machine",OR),("motor-control",VI),("RoboMaster",BL)],size=12,h=24)}
<g transform="translate(760,40)" fill="none" stroke-linecap="round">
 <path d="M0 110 Q 180 -40 380 60" stroke="{TE}" stroke-opacity=".25" stroke-dasharray="4 6"/>
 <path id="arc" d="M0 110 Q 180 -40 380 60" stroke="url(#edge)" stroke-width="2" stroke-dasharray="60 900"><animate attributeName="stroke-dashoffset" values="0;-480" dur="3.2s" repeatCount="indefinite"/></path>
 <circle cx="380" cy="60" r="10" stroke="{OR}"/><circle cx="380" cy="60" r="4" fill="{OR}"/>
 <circle cx="380" cy="60" r="10" stroke="{OR}"><animate attributeName="r" values="10;26" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></circle>
</g>'''
build("card-dart",1200,200,dart)
# ---------- footer ----------
foot=f'''<circle cx="600" cy="140" r="380" fill="url(#g2)"/>
<text x="600" y="60" text-anchor="middle" class="cb" font-size="22" style="fill:#e6ebf5">如果这些项目对你有用，点个 Star 就是最好的反馈</text>
<text x="600" y="92" text-anchor="middle" class="m" font-size="13" style="fill:#7d8799">issues &amp; PRs welcome · github.com/another-bbzj</text>'''
build("footer",1200,130,foot)
