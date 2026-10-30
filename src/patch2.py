t=open('app.template.html').read(); g=open('guru_cloud.js').read()
def R(s,a,b,c=1):
    assert s.count(a)==c,(s.count(a),a[:80]); return s.replace(a,b)
# ---- template ----
t=R(t,"const MODS = DATA.MODS, DIAG = DATA.DIAG, NAMES = DATA.NAMES;","const MODS = DATA.MODS, DIAG = DATA.DIAG, TO2 = DATA.TO2, NAMES = DATA.NAMES;")
t=R(t,'const TO_EMPTY={to2:"Tryout 2",to3:"Tryout 3"};','''PAKET.to2={key:"to2",title:"Tryout 2",sub:"25 butir lintas elemen · simulasi TKA BCF",durasi:60,skema:"m7",qs:()=>TO2.soal.map(q=>normQ(q)),
  groups:[
   {title:"Per Elemen",lead:"Ketercapaian pada empat elemen kerangka asesmen.",f:q=>q.meta.elemenNama,order:[1,2,3,4].map(e=>TO2.soal.find(s=>s.meta.elemen===e).meta.elemenNama)},
   {title:"Per Sub-elemen",lead:"Bagian yang lebih rinci dalam tiap elemen.",f:q=>q.meta.sub},
   {title:"Per Level Kognitif",lead:"Memahami, menerapkan, dan menalar.",f:q=>LVL[q.meta.level],order:Object.values(LVL),half:true},
   {title:"Per Bentuk Soal",lead:"Ketepatan pada tiap format butir.",f:q=>FORM[q.kind],order:Object.values(FORM),half:true}]};
const TO_EMPTY={to3:"Tryout 3"};''')
t=R(t,'{id:"to2",label:"Tryout 2",type:"kosong"}','{id:"to2",label:"Tryout 2",type:"paket"}')
t=R(t,'if(id==="diag"||id==="to1") return !!(r.paket[id]&&r.paket[id].finished);','if(id==="diag"||id==="to1"||id==="to2") return !!(r.paket[id]&&r.paket[id].finished);')
t=R(t,'if(id==="to2"||id==="to3") return "kosong";','if(id==="to3") return "kosong";')
t=R(t,'  if(id==="to1") return MODNUM.every(n=>isDone("m"+n))?"open":"locked";','  if(id==="to1") return MODNUM.every(n=>isDone("m"+n))?"open":"locked";\n  if(id==="to2") return isDone("to1")?"open":"locked";')
t=R(t,'  if(id==="diag"||id==="to1"){\n    const s=rec().paket[id];','  if(id==="diag"||id==="to1"||id==="to2"){\n    const s=rec().paket[id];')
t=R(t,'${stageCard("to2","Tryout 2","Soal sedang disiapkan")}','${stageCard("to2","Tryout 2","25 butir · 60 menit · lintas elemen"+(to2&&to2.finished?" · nilai "+to2.result.nilai:""))}')
t=R(t,'const diag=r.paket.diag, to1=r.paket.to1;','const diag=r.paket.diag, to1=r.paket.to1, to2=r.paket.to2;')
t=R(t,'''<span class="chip" style="border-color:#7fe0a8">Tryout 1: ${to1&&to1.finished?to1.result.nilai:"belum"}</span>''','''<span class="chip" style="border-color:#7fe0a8">Tryout 1: ${to1&&to1.finished?to1.result.nilai:"belum"}</span><span class="chip" style="border-color:#c9a7ff">Tryout 2: ${to2&&to2.finished?to2.result.nilai:"belum"}</span>''')
t=R(t,'  if(P.key==="diag") X.result.prioritas=an.prioritas;','  if(P.key==="diag"||P.key==="to2") X.result.prioritas=an.prioritas;')
t=R(t,'  if(P.key==="diag"){ const mm={};','  if(P.key==="diag"||P.key==="to2"){ const mm={};')
t=R(t,'if(P.key==="diag"&&an.prioritas.length) h+=`<section class="card"><h3>Modul yang diprioritaskan</h3><p class="muted">Butir yang terkait modul-modul ini masih di bawah 60%. Beri perhatian lebih saat mempelajarinya (ditandai ★).</p>',
      'if((P.key==="diag"||P.key==="to2")&&an.prioritas.length) h+=`<section class="card"><h3>${P.key==="to2"?"Modul yang perlu diulang":"Modul yang diprioritaskan"}</h3><p class="muted">Butir yang terkait modul-modul ini masih di bawah 60%. ${P.key==="to2"?"Buka kembali modul tersebut sebelum Tryout berikutnya.":"Beri perhatian lebih saat mempelajarinya (ditandai ★)."}</p>')
# panduan alur di beranda & kartu mapel tidak berubah. Guru lokal: kolom Tryout 2
t=R(t,'<th>Tryout 1</th>${subs.map(s=>`<th>${esc(s)}</th>`).join("")}</tr></thead>','<th>Tryout 1</th><th>Tryout 2</th>${subs.map(s=>`<th>${esc(s)}</th>`).join("")}</tr></thead>')
t=R(t,'<td>${g.paket.to1?g.paket.to1.nilai:"–"}</td>${subs.map(','<td>${g.paket.to1?g.paket.to1.nilai:"–"}</td><td>${g.paket.to2?g.paket.to2.nilai:"–"}</td>${subs.map(')
t=R(t,'<th>${avgOf(ok,g=>g.paket.to1&&g.paket.to1.nilai)}</th>${subs.map(','<th>${avgOf(ok,g=>g.paket.to1&&g.paket.to1.nilai)}</th><th>${avgOf(ok,g=>g.paket.to2&&g.paket.to2.nilai)}</th>${subs.map(')
t=R(t,'["Nama","Asesmen Awal","Modul selesai","Tryout 1",...subs]','["Nama","Asesmen Awal","Modul selesai","Tryout 1","Tryout 2",...subs]')
t=R(t,'g.paket.to1?g.paket.to1.nilai:"",...subs.map(s=>val(g,s)??"")]','g.paket.to1?g.paket.to1.nilai:"",g.paket.to2?g.paket.to2.nilai:"",...subs.map(s=>val(g,s)??"")]')
# ---- guru cloud ----
g=R(g,'["diag","to1"].forEach(k=>{ const S=rec&&rec.paket','["diag","to1","to2"].forEach(k=>{ const S=rec&&rec.paket')
g=R(g,'const aw=R.filter(r=>r.an.diag), t1=R.filter(r=>r.an.to1);','const aw=R.filter(r=>r.an.diag), t1=R.filter(r=>r.an.to1), t2=R.filter(r=>r.an.to2);')
g=R(g,'''"Rata-rata Tryout 1")}${kpi(act.length?''','''"Rata-rata Tryout 1")}${kpi(nz(mean(t2.map(r=>r.an.to2.nilai))),"Rata-rata Tryout 2")}${kpi(act.length?''')
g=R(g,'const both=R.filter(r=>r.an.diag&&r.an.to1); if(both.length) h+=`<p class="small" style="margin:10px 0 0">Tren: dari ${both.length} siswa yang sudah menyelesaikan keduanya, rata-rata berubah ${mean(both.map(r=>r.an.diag.nilai))} → ${mean(both.map(r=>r.an.to1.nilai))}.</p>`;',
 'const lastT=r=>r.an.to2||r.an.to1; const both=R.filter(r=>r.an.diag&&lastT(r)); if(both.length) h+=`<p class="small" style="margin:10px 0 0">Tren: dari ${both.length} siswa yang punya Asesmen Awal dan minimal satu Tryout, rata-rata berubah ${mean(both.map(r=>r.an.diag.nilai))} (Awal) → ${mean(both.map(r=>lastT(r).nilai))} (Tryout terakhir).</p>`;')
g=R(g,'<th>Tryout 1</th><th>Δ</th>${subs','<th>Tryout 1</th><th>Tryout 2</th><th>Δ</th>${subs')
g=R(g,'R.map(r=>{ const d=r.an.diag, t=r.an.to1, dl_=d&&t?t.nilai-d.nilai:null;','R.map(r=>{ const d=r.an.diag, t=r.an.to1, t2_=r.an.to2, lt=lastT(r), dl_=d&&lt?lt.nilai-d.nilai:null;')
g=R(g,'''${t?t.nilai:"–"}</td><td>${dl_==null?"–":''','''${t?t.nilai:"–"}</td><td class="heat" style="${heatSt(t2_&&t2_.nilai)}">${t2_?t2_.nilai:"–"}</td><td>${dl_==null?"–":''')
g=R(g,'''<th>${nz(mean(t1.map(r=>r.an.to1.nilai)))}</th><th></th>${subs''','''<th>${nz(mean(t1.map(r=>r.an.to1.nilai)))}</th><th>${nz(mean(t2.map(r=>r.an.to2.nilai)))}</th><th></th>${subs''')
g=R(g,'"Modul selesai","Tryout 1","Selisih"','"Modul selesai","Tryout 1","Tryout 2","Selisih (terakhir − Awal)"')
g=R(g,'const d=r.an.diag,t=r.an.to1; rows.push([r.no,r.name,r.at?new Date(r.at).toLocaleString("id-ID"):"",d?d.nilai:"",r.rec?r.mods:"",t?t.nilai:"",d&&t?t.nilai-d.nilai:"",','const d=r.an.diag,t=r.an.to1,t2_=r.an.to2,lt=t2_||t; rows.push([r.no,r.name,r.at?new Date(r.at).toLocaleString("id-ID"):"",d?d.nilai:"",r.rec?r.mods:"",t?t.nilai:"",t2_?t2_.nilai:"",d&&lt?lt.nilai-d.nilai:"",')
g=R(g,'const d=r.an.diag,t=r.an.to1; let h=`<button','const d=r.an.diag,t=r.an.to1,t2_=r.an.to2; let h=`<button')
g=R(g,'''<span>Tryout 1${t?" · "+predikat(t.nilai):""}</span></div></div></div>`;''','''<span>Tryout 1${t?" · "+predikat(t.nilai):""}</span></div><div class="kpi"><b>${t2_?t2_.nilai:"–"}</b><span>Tryout 2${t2_?" · "+predikat(t2_.nilai):""}</span></div></div></div>`;''')
g=R(g,'''  h+=`<section class="card"><h3>Kemajuan modul</h3>''','''  if(t2_){ if(t2_.prioritas.length) h+=`<div class="card"><b>Modul yang perlu diulang (dari Tryout 2)</b><div class="recs" style="margin-top:8px">${t2_.prioritas.map(k=>`<span class="rec">Modul ${k} · ${esc(MOD[k].meta.title)}</span>`).join("")}</div></div>`;
    t2_.groups.slice(0,2).forEach(g=>{ h+=`<section class="card"><h3>Tryout 2 · ${esc(g.title)}</h3>${bars(g.rows)}</section>`; }); }
  h+=`<section class="card"><h3>Kemajuan modul</h3>''')
g=R(g,'const ks=["diag","to1"];','const ks=["diag","to1","to2"];')
open('app.template.html','w').write(t); open('guru_cloud.js','w').write(g); print("patch2 ok")
