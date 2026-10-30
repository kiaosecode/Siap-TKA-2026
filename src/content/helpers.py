import math
def pick(id,stem,opts,explain,label=None,bare=False):
    # opts: (teks, benar?, alasan?)
    assert sum(1 for o in opts if o[1])==1,(id,"harus tepat satu kunci")
    q={"id":id,"kind":"pick","label":label or id,"stem":stem,"opts":[[o[0],1 if o[1] else 0]+([o[2]] if len(o)>2 else []) for o in opts],"explain":explain}
    if bare: q["bare"]=True
    return q
def mcma(id,stem,opts,explain,label=None):
    n=sum(1 for o in opts if o[1]); assert n>=2,(id,"MCMA minimal 2 kunci")
    return {"id":id,"kind":"mcma","label":label or id,"stem":stem,"opts":[[o[0],1 if o[1] else 0]+([o[2]] if len(o)>2 else []) for o in opts],"explain":explain}
def tf(id,stem,items,label=None):
    return {"id":id,"kind":"tf","label":label or id,"stem":stem,"opts":[{"t":t,"c":bool(c),"why":w} for t,c,w in items],"explain":""}
def tebak(ids): return {"type":"tebak","ids":ids}
def cek(ids): return {"type":"cek","ids":ids}
def lead(t): return {"type":"lead","text":t}
def html(h): return {"type":"html","html":h}
def table(head,rows): return {"type":"table","head":head,"rows":rows}
def callout(kind,tag,h): return {"type":"callout","kind":kind,"tag":tag,"html":h}
def steps(items): return {"type":"steps","items":[{"title":a,"desc":b} for a,b in items]}
def cards(items): return {"type":"cards","items":[{"title":a,"penyebab":b,"solusi":c} for a,b,c in items]}
def checklist(items): return {"type":"checklist","items":[{"id":a,"text":b} for a,b in items]}
def panel(h): return {"type":"panel","html":h}
def note(id,ph): return {"type":"html","html":f'<textarea data-note="{id}" placeholder="{ph}"></textarea>'}
def svg(s): return {"type":"svg","svg":s}

def polar_svg():
    def path(f,cx,cy,R):
        pts=[]
        for d in range(0,361,3):
            t=math.radians(d); r=abs(f(t)); pts.append((cx+R*r*math.sin(t),cy-R*r*math.cos(t)))
        return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)+" Z"
    pats=[("Omnidirectional",lambda t:1.0,"Segala arah"),("Cardioid",lambda t:0.5+0.5*math.cos(t),"Depan; belakang diredam"),("Shotgun",lambda t:0.25+0.75*math.cos(t),"Sempit ke depan")]
    out='<svg viewBox="0 0 600 230" width="100%" role="img" aria-label="Pola tangkap mikrofon: omnidirectional, cardioid, shotgun" style="display:block;max-width:600px;margin:8px auto">'
    for i,(nm,f,cap) in enumerate(pats):
        cx=100+i*200; cy=100; R=70
        for k in (0.5,1.0): out+=f'<circle cx="{cx}" cy="{cy}" r="{R*k}" fill="none" style="stroke:var(--line)" stroke-width="1"/>'
        out+=f'<line x1="{cx}" y1="{cy-R-6}" x2="{cx}" y2="{cy+R+6}" style="stroke:var(--line)"/><line x1="{cx-R-6}" y1="{cy}" x2="{cx+R+6}" y2="{cy}" style="stroke:var(--line)"/>'
        out+=f'<path d="{path(f,cx,cy,R)}" style="fill:var(--blue);stroke:var(--blue)" fill-opacity=".22" stroke-width="2"/>'
        out+=f'<text x="{cx}" y="{cy-R-10}" text-anchor="middle" font-size="11" style="fill:var(--muted)">depan</text>'
        out+=f'<text x="{cx}" y="{cy+R+22}" text-anchor="middle" font-weight="800" font-size="14" style="fill:var(--navy)">{nm}</text>'
        out+=f'<text x="{cx}" y="{cy+R+40}" text-anchor="middle" font-size="12" style="fill:var(--ink)">{cap}</text>'
    return out+'</svg>'

def boom_svg():
    return ('<svg viewBox="0 0 600 300" width="100%" role="img" aria-label="Posisi mikrofon boom di atas batas bingkai, mengarah ke mulut aktor" style="display:block;max-width:600px;margin:8px auto">'
     # bingkai kamera
     '<rect x="60" y="120" width="360" height="160" fill="none" style="stroke:var(--blue)" stroke-width="2" stroke-dasharray="7 5"/>'
     '<text x="305" y="272" font-size="12" font-weight="700" style="fill:var(--blue)">Bingkai kamera</text>'
     # aktor
     '<circle cx="240" cy="178" r="26" style="fill:var(--surface2);stroke:var(--navy)" stroke-width="2"/>'
     '<path d="M190 280 Q190 214 240 214 Q290 214 290 280 Z" style="fill:var(--surface2);stroke:var(--navy)" stroke-width="2"/>'
     '<circle cx="251" cy="182" r="3" style="fill:var(--navy)"/>'
     # boom pole
     '<line x1="590" y1="40" x2="262" y2="96" style="stroke:var(--muted)" stroke-width="5" stroke-linecap="round"/>'
     '<rect x="226" y="88" width="46" height="16" rx="8" transform="rotate(-30 249 96)" style="fill:var(--amber);stroke:var(--navy)" stroke-width="2"/>'
     # arah on-axis
     '<line x1="246" y1="104" x2="246" y2="150" style="stroke:var(--green)" stroke-width="3"/><polygon points="246,158 239,144 253,144" style="fill:var(--green)"/>'
     '<text x="256" y="140" font-size="12" font-weight="700" style="fill:var(--green)">on-axis ke mulut</text>'
     '<text x="68" y="110" font-size="12" font-weight="700" style="fill:var(--navy)">tepat di atas batas bingkai</text>'
     # terlalu jauh
     '<rect x="60" y="14" width="46" height="16" rx="8" transform="rotate(-20 83 22)" fill="none" style="stroke:var(--red)" stroke-width="2" stroke-dasharray="4 3"/>'
     '<text x="60" y="52" font-size="12" style="fill:var(--red)">terlalu jauh: suara tipis, ruangan ikut masuk</text>'
     '</svg>')

def meter_svg():
    x0=20; w=520; per=w/60.0
    def X(db): return x0+(db+60)*per
    z=[(-60,-30,"var(--surface2)","Terlalu pelan"),(-30,-12,"var(--blue-soft)","Aman, tapi kecil"),(-12,-6,"var(--green-soft)","Ideal"),(-6,0,"var(--amber-soft)","Bahaya")]
    out='<svg viewBox="0 0 600 120" width="100%" role="img" aria-label="Skala level rekaman dalam dBFS dengan zona ideal -12 sampai -6" style="display:block;max-width:600px;margin:8px auto">'
    for a,b,c,l in z:
        out+=f'<rect x="{X(a):.1f}" y="30" width="{(b-a)*per:.1f}" height="36" style="fill:{c};stroke:var(--line)"/>'
        out+=f'<text x="{(X(a)+X(b))/2:.1f}" y="53" text-anchor="middle" font-size="12" font-weight="700" style="fill:var(--ink)">{l}</text>'
    out+=f'<rect x="{X(0)-4:.1f}" y="30" width="6" height="36" style="fill:var(--red)"/><text x="{X(0)-2:.1f}" y="86" text-anchor="end" font-size="12" font-weight="700" style="fill:var(--red)">0 dBFS = clip</text>'
    for db in (-60,-30,-12,-6,0):
        out+=f'<text x="{X(db):.1f}" y="22" text-anchor="middle" font-size="11" style="fill:var(--muted)">{db}</text>'
    out+=f'<text x="{X(-6):.1f}" y="104" text-anchor="end" font-size="12" font-weight="700" style="fill:var(--green)">puncak dialog sekitar −12 sampai −6 dBFS</text>'
    return out+'</svg>'
