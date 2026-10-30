import re
t=open('app.template.html').read()
glue=open('glue.js').read(); guru=open('guru_cloud.js').read()
def rep(old,new,cnt=1):
    global t
    assert t.count(old)==cnt,(t.count(old),old[:70])
    t=t.replace(old,new)

# CSS
rep(".footer{background:var(--navy)", """.syncchip{border:0;font:600 12px/1 inherit;padding:7px 11px;border-radius:999px;background:rgba(255,255,255,.14);color:#fff;cursor:pointer;white-space:nowrap;max-width:210px;overflow:hidden;text-overflow:ellipsis}
.syncchip.ok{background:rgba(31,157,85,.45)}.syncchip.wait{background:rgba(242,165,22,.45)}.syncchip.off{background:rgba(214,69,69,.6)}
.pinrow{display:none;gap:14px;align-items:center;margin-top:10px;flex-wrap:wrap}.pinrow.on{display:flex}
.pinrow input[type=password]{font:700 20px/1 monospace;letter-spacing:6px;width:170px;padding:10px 12px;border:1.5px solid var(--line);border-radius:10px}
.errtxt{color:var(--red);font-weight:600}
.gtop{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.gtabs{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0}.gtb{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 16px;font:600 13.5px/1 inherit;cursor:pointer;color:var(--navy)}.gtb.cur{background:var(--navy);color:#fff;border-color:var(--navy)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}.kpi{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px}.kpi b{display:block;font-size:24px;color:var(--navy)}.kpi span{font-size:12.5px;color:var(--muted)}
.livedot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);margin-right:4px}.livedot.c{background:var(--amber)}
.footer{background:var(--navy)""")
# header chip
rep('<div class="timer hidden" id="timer">','<button class="syncchip hidden noprint" id="syncchip" title="Status penyimpanan online">◌</button>\n    <div class="timer hidden" id="timer">')
# script tags
rep('<script>\nconst DATA = /*__DATA__*/null;','<script src="firebase-config.js"></script>\n<script src="cloud.js"></script>\n<script>\nconst DATA = /*__DATA__*/null;')
# save
rep('function save(){ try{ localStorage.setItem(STORE,JSON.stringify(DB)); }catch(e){} }',
    'function save(){ if(typeof USER!=="undefined"&&USER&&DB.students[USER]) DB.students[USER].updatedAt=Date.now(); try{ localStorage.setItem(STORE,JSON.stringify(DB)); }catch(e){} if(typeof queuePush==="function") queuePush(); }')
# glue after modRec
m=re.search(r"function modRec\(n\)\{.*?\n",t); assert m
t=t[:m.end()]+glue+"\n"+t[m.end():]
# render hooks
rep('clearInterval(tick); $("app").onclick=null; $("app").onchange=null;',
    'clearInterval(tick); $("app").onclick=null; $("app").onchange=null; if(V.name!=="guru"&&typeof GC!=="undefined"&&GC.on) guruStop(); drawSync();')
# finishExam
rep('  save(); go({name:"result",key:P.key});','  save(); pushNow(); go({name:"result",key:P.key});')
# logout
rep('$("btnLogout").onclick=()=>{ USER=null; go({name:"login"}); };','$("btnLogout").onclick=doLogout;\n$("syncchip").onclick=()=>{ tryLoad(); pushNow(); drawSync(); };')
# login html
rep('<div class="names" id="names"></div>','''<div class="names" id="names"></div>
    ${CL?`<div class="pinrow" id="pinrow"><input id="pin" type="password" inputmode="numeric" autocomplete="current-password" maxlength="6" placeholder="PIN"><label class="small" style="display:flex;gap:6px;align-items:center"><input type="checkbox" id="chkIngat"> Ingat saya di perangkat ini</label></div>
    <div class="small" id="loginMsg" style="min-height:20px;margin-top:6px">${cloudMode()?"":"Akun online belum tersedia di perangkat ini. Kamu dapat melanjutkan dalam mode lokal."}</div>`:""}''')
rep('<button class="linkbtn" id="btnGuru">Rekap Guru</button></div>','<button class="linkbtn hidden" id="btnPasang">Pasang aplikasi</button><button class="linkbtn" id="btnGuru">Rekap Guru</button></div>')
rep("const list=NAMES.map((n,i)=>({n,i}))","const base=cloudMode()?SY.list.map(x=>x.name):NAMES; const list=base.map((n,i)=>({n,i}))")
rep('''$("names").onclick=e=>{ const b=e.target.closest(".name-btn"); if(!b) return; pick=b.dataset.n; drawNames(); $("btnStart").disabled=false; $("pickHint").innerHTML="Dipilih: <b>"+esc(pick)+"</b>"; };''',
'''$("names").onclick=e=>{ const b=e.target.closest(".name-btn"); if(!b) return; pick=b.dataset.n; drawNames(); $("btnStart").disabled=false; $("pickHint").innerHTML="Dipilih: <b>"+esc(pick)+"</b>"; if(cloudMode()){ $("pinrow").classList.add("on"); $("pin").focus(); } };
  if(cloudMode()&&$("pin")) $("pin").onkeydown=e=>{ if(e.key==="Enter") $("btnStart").click(); };
  if(PWA_EVT) $("btnPasang").classList.remove("hidden"); $("btnPasang").onclick=()=>{ if(PWA_EVT){ PWA_EVT.prompt(); } };''')
rep('''$("btnStart").onclick=()=>{ if(!pick) return; USER=pick; if(!DB.students[USER]){ DB.students[USER]=newRec(USER); save(); } go({name:"mapel"}); };''',
'''$("btnStart").onclick=async()=>{ if(!pick) return;
    if(cloudMode()){ const pin=$("pin").value.trim(); if(!/^\\d{6}$/.test(pin)){ $("loginMsg").innerHTML='<span class="errtxt">Masukkan PIN 6 angka.</span>'; return; }
      $("btnStart").disabled=true; $("loginMsg").textContent="Memeriksa…";
      const r=await cloudLogin(pick,pin,$("chkIngat").checked);
      if(r.ok) return go({name:"mapel"});
      $("btnStart").disabled=false; $("loginMsg").innerHTML=`<span class="errtxt">${esc(r.err)}</span>`+(r.offline?` <button class="linkbtn" id="btnLokal">Lanjut tanpa jaringan (mode lokal)</button>`:"");
      const bl=$("btnLokal"); if(bl) bl.onclick=()=>enterLocal(pick); return; }
    enterLocal(pick); };''')
# guru: rename old, add new
rep("function renderGuru(){\n  $(\"app\").innerHTML=`<main class=\"page\"><div class=\"wrap\"><button class=\"btn btn-ghost btn-sm\" id=\"gBack\">","function renderGuruLokal(){\n  $(\"app\").innerHTML=`<main class=\"page\"><div class=\"wrap\"><button class=\"btn btn-ghost btn-sm\" id=\"gBack\">")
rep("/* peringatan sebelum menutup saat ujian */", guru+"\n/* peringatan sebelum menutup saat ujian */")
# refactor output
rep("function paketOut(k){\n  const P=PAKET[k], S=rec().paket[k]; if(!S||!S.finished) return null; const an=analyze(P,S);",
    "function paketOut(k){ return paketOutFor(k,rec().paket[k]); }\nfunction paketOutFor(k,S){\n  const P=PAKET[k]; if(!S||!S.finished) return null; const an=analyze(P,S);")
rep("function downloadStudent(){\n  const r=rec(); const pk={}; Object.keys(PAKET).forEach(k=>{ const o=paketOut(k); if(o) pk[k]=o; });",
    "function downloadStudent(){ dl(`bcf_${slug(USER)}.json`,studentOut(USER,rec())); }\nfunction studentOut(USER,r){\n  const pk={}; Object.keys(PAKET).forEach(k=>{ const o=paketOutFor(k,r.paket[k]); if(o) pk[k]=o; });")
rep("  dl(`bcf_${slug(USER)}.json`,{jenis:\"bcf-siswa\",versi:1,dibuat:","  return ({jenis:\"bcf-siswa\",versi:1,dibuat:")
# boot
rep("\nrender();\n</script>","""
render(); bootCloud();
if("serviceWorker" in navigator && /^https?:/.test(location.protocol)) navigator.serviceWorker.register("sw.js").catch(()=>{});
</script>""")
open('app.online.template.html','w').write(t)
print("ok",len(t))
