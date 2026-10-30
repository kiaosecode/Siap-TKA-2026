/* ======================================================================
   DASHBOARD GURU (online, real-time dari Firestore)
   ====================================================================== */
const GC={tab:"rekap",prog:[],siswa:[],pin:{},unsub:[],on:false,cache:false,at:0,err:"",detail:null,paket:"diag",busy:false,msg:"",showPin:false,rows:[],raf:0};
const ago=ts=>{ if(!ts) return "–"; const s=Math.round((Date.now()-ts)/1000); if(s<90) return "baru saja"; if(s<3600) return Math.round(s/60)+" mnt lalu"; if(s<86400) return Math.round(s/3600)+" jam lalu"; return Math.round(s/86400)+" hari lalu"; };
const subList=()=>{ const s=[]; PAKET.diag.qs().forEach(q=>{ if(!s.includes(q.meta.sub)) s.push(q.meta.sub); }); return s; };
const subVal=(an,sub)=>{ if(!an) return null; const g=an.groups.find(x=>x.title==="Per Sub-elemen"); const r=g&&g.rows.find(x=>x.label===sub); return r?r.pct:null; };
const heatSt=v=>v==null?"":`background:hsl(${Math.round(v*1.2)},70%,${88-v*0.2}%)`;
const mean=a=>{ const v=a.filter(x=>typeof x==="number"); return v.length?Math.round(v.reduce((s,x)=>s+x,0)/v.length):null; };
const nz=v=>v==null?"–":v;

function computeRows(){
  const pm={}; GC.prog.forEach(p=>pm[p.sid]=p);
  const sm={}; GC.siswa.forEach(s=>sm[s.sid]=s);
  const names=NAMES.slice(); GC.prog.forEach(p=>{ if(p.name&&!names.includes(p.name)) names.push(p.name); });
  GC.rows=names.map((name,i)=>{ const sid=slug(name), p=pm[sid], rec=p&&p.rec; const an={};
    ["diag","to1","to2"].forEach(k=>{ const S=rec&&rec.paket&&rec.paket[k]; an[k]=(S&&S.finished)?analyze(PAKET[k],S):null; });
    const mods=rec?MODNUM.filter(n=>rec.mod&&rec.mod[n]&&rec.mod[n].done).length:0;
    return {no:i+1,name,sid,rec,at:p?p.updatedAt:0,an,mods,akun:sm[sid]||null};
  });
}
function guruStart(){
  if(GC.on) return; GC.on=true;
  GC.unsub=[
    CL.pantauProgres((a,c)=>{ GC.prog=a; GC.cache=c; GC.at=Date.now(); GC.err=""; guruRefresh(); },e=>{ GC.err=(e&&e.code)||String(e); guruRefresh(); }),
    CL.pantauSiswa(a=>{ GC.siswa=a; guruRefresh(); },()=>{}),
    CL.pantauPin(o=>{ GC.pin=o; guruRefresh(); })];
}
function guruStop(){ GC.unsub.forEach(u=>{ try{u();}catch(e){} }); GC.unsub=[]; GC.on=false; }
function guruRefresh(){ if(V.name!=="guru"||!GC.on) return; cancelAnimationFrame(GC.raf); GC.raf=requestAnimationFrame(()=>{ computeRows(); drawGuruBody(); }); }

function renderGuru(){
  if(!CL||V.lokal) return renderGuruLokal();
  if(!(CL.uid()&&SY.guru)) return renderGuruLogin();
  $("app").innerHTML=`<main class="page"><div class="wrap">
   <div class="gtop"><div><h1 class="title" style="margin:0">Dashboard Guru</h1><p class="muted" style="margin:2px 0 0" id="gLive"></p></div>
   <div class="actions" style="margin:0"><button class="btn btn-ghost btn-sm" id="gImp">Impor JSON manual</button><button class="btn btn-ghost btn-sm" id="gOut">Keluar guru</button></div></div>
   <div class="gtabs" id="gTabs"></div><div id="gBody"></div></div></main>`;
  $("gImp").onclick=()=>go({name:"guru",lokal:true});
  $("gOut").onclick=async()=>{ guruStop(); try{ await CL.keluar(); }catch(e){} SY.guru=false; go({name:"login"}); };
  $("app").onclick=guruClick;
  guruStart(); computeRows(); drawGuruBody();
}
function renderGuruLogin(){
  $("app").innerHTML=`<main class="page"><div class="wrap" style="max-width:460px"><button class="btn btn-ghost btn-sm" id="gBack">← Kembali</button>
   <div class="card" style="margin-top:14px"><h2 style="margin:0 0 6px">Masuk sebagai guru</h2><p class="muted">Gunakan akun guru yang didaftarkan pada Firebase.</p>
   <label class="small">Email</label><input class="search" id="gEm" type="email" autocomplete="username" style="margin:4px 0 10px">
   <label class="small">Kata sandi</label><input class="search" id="gPw" type="password" autocomplete="current-password" style="margin:4px 0 12px">
   <div class="small" id="gMsg" style="min-height:18px"></div><button class="btn btn-primary" id="gGo">Masuk</button></div>
   <p class="small" style="margin-top:12px">Tanpa jaringan? <button class="linkbtn" id="gLok">Impor JSON manual</button></p></div></main>`;
  $("gBack").onclick=()=>go({name:"login"}); $("gLok").onclick=()=>go({name:"guru",lokal:true});
  const doIt=async()=>{ const em=$("gEm").value.trim(), pw=$("gPw").value; if(!em||!pw) return; $("gMsg").textContent="Memeriksa…"; $("gGo").disabled=true;
    try{ await CL.masuk(em,pw,true); if(await CL.apakahGuru()){ SY.guru=true; return go({name:"guru"}); }
      await CL.keluar(); $("gMsg").innerHTML='<span class="errtxt">Akun ini belum terdaftar sebagai guru.</span>'; }
    catch(e){ $("gMsg").innerHTML='<span class="errtxt">'+(/network/.test((e&&e.code)||"")?"Tidak ada jaringan.":"Email atau kata sandi salah.")+'</span>'; }
    $("gGo").disabled=false; };
  $("gGo").onclick=doIt; $("gPw").onkeydown=e=>{ if(e.key==="Enter") doIt(); };
}

function guruClick(e){
  const t=e.target.closest("[data-gt]"); if(t){ GC.tab=t.dataset.gt; GC.detail=null; return drawGuruBody(); }
  const d=e.target.closest("[data-detail]"); if(d){ GC.detail=d.dataset.detail; drawGuruBody(); return window.scrollTo(0,0); }
  const id=e.target.id||""; const a=e.target.closest("[data-act]"); const act=a?a.dataset.act:id;
  if(act==="back"){ GC.detail=null; return drawGuruBody(); }
  if(act==="csv") return guruCsv();
  if(act==="mk") return guruBuat(GC.rows.filter(r=>!r.akun).map(r=>r.name),false);
  if(act==="reset"){ const r=GC.rows.find(x=>x.sid===a.dataset.sid); if(r&&confirm(`Reset PIN ${r.name}? PIN lama tidak berlaku lagi; kemajuan belajarnya tetap aman.`)) guruBuat([r.name],true); return; }
  if(act==="togglepin"){ GC.showPin=!GC.showPin; return drawGuruBody(); }
  if(act==="cetak") return cetakKartu();
  if(act==="pincsv") return pinCsv();
  if(act==="sj"){ const r=GC.rows.find(x=>x.sid===a.dataset.sid); if(r&&r.rec) dl(`bcf_${slug(r.name)}.json`,studentOut(r.name,r.rec)); return; }
}
function drawGuruBody(){
  const live=$("gLive"); if(!live) return;
  live.innerHTML=GC.err?`<span class="errtxt">Gagal membaca data: ${esc(GC.err)}</span>`:`<span class="livedot ${GC.cache?"c":""}"></span> ${GC.cache?"Data dari cache perangkat (menunggu server)":"Langsung dari server"} · ${GC.at?new Date(GC.at).toLocaleTimeString("id-ID"):"memuat…"}`;
  const tabs=[["rekap","Rekap kelas"],["butir","Analisis butir"],["akun","Kelola siswa"]];
  $("gTabs").innerHTML=tabs.map(([k,l])=>`<button class="gtb ${GC.tab===k&&!GC.detail?"cur":""}" data-gt="${k}">${l}</button>`).join("");
  $("gBody").innerHTML=GC.detail?guruDetail():GC.tab==="rekap"?guruRekap():GC.tab==="butir"?guruButir():guruAkun();
  if(GC.tab==="butir"&&!GC.detail){ const s=$("gPaket"); if(s) s.onchange=()=>{ GC.paket=s.value; drawGuruBody(); }; }
}

function guruRekap(){
  const R=GC.rows, subs=subList(), act=R.filter(r=>r.rec);
  const dayAct=R.filter(r=>r.at&&Date.now()-r.at<864e5).length;
  const aw=R.filter(r=>r.an.diag), t1=R.filter(r=>r.an.to1), t2=R.filter(r=>r.an.to2);
  const kpi=(v,l)=>`<div class="kpi"><b>${v}</b><span>${l}</span></div>`;
  let h=`<div class="kpis">${kpi(act.length+" / "+R.length,"Siswa sudah masuk")}${kpi(dayAct,"Aktif 24 jam terakhir")}${kpi(aw.length,"Selesai Asesmen Awal")}${kpi(nz(mean(aw.map(r=>r.an.diag.nilai))),"Rata-rata Asesmen Awal")}${kpi(nz(mean(t1.map(r=>r.an.to1.nilai))),"Rata-rata Tryout 1")}${kpi(nz(mean(t2.map(r=>r.an.to2.nilai))),"Rata-rata Tryout 2")}${kpi(act.length?(Math.round(act.reduce((s,r)=>s+r.mods,0)/act.length*10)/10)+" / "+MODNUM.length:"–","Rata-rata modul selesai")}</div>`;
  const lastT=r=>r.an.to2||r.an.to1; const both=R.filter(r=>r.an.diag&&lastT(r)); if(both.length) h+=`<p class="small" style="margin:10px 0 0">Tren: dari ${both.length} siswa yang punya Asesmen Awal dan minimal satu Tryout, rata-rata berubah ${mean(both.map(r=>r.an.diag.nilai))} (Awal) → ${mean(both.map(r=>lastT(r).nilai))} (Tryout terakhir).</p>`;
  h+=`<div class="card" style="margin-top:14px"><div class="actions" style="margin:0 0 8px"><button class="btn btn-primary btn-sm" data-act="csv">⬇ Unduh CSV (buka di Excel)</button></div>
   <table class="gtab"><thead><tr><th>No</th><th>Nama</th><th>Aktif</th><th>Awal</th><th>Modul</th><th>Tryout 1</th><th>Tryout 2</th><th>Δ</th>${subs.map(s=>`<th title="Asesmen Awal">${esc(s)}</th>`).join("")}</tr></thead><tbody>`+
   R.map(r=>{ const d=r.an.diag, t=r.an.to1, t2_=r.an.to2, lt=lastT(r), dl_=d&&lt?lt.nilai-d.nilai:null;
     return `<tr><td>${r.no}</td><td><button class="linkbtn" data-detail="${r.sid}" ${r.rec?"":"disabled"}>${esc(r.name)}</button></td><td>${r.rec?ago(r.at):'<span class="badge x">Belum masuk</span>'}</td><td class="heat" style="${heatSt(d&&d.nilai)}">${d?d.nilai:"–"}</td><td>${r.rec?r.mods+" / "+MODNUM.length:"–"}</td><td class="heat" style="${heatSt(t&&t.nilai)}">${t?t.nilai:"–"}</td><td class="heat" style="${heatSt(t2_&&t2_.nilai)}">${t2_?t2_.nilai:"–"}</td><td>${dl_==null?"–":(dl_>0?"+":"")+dl_}</td>${subs.map(s=>{ const v=subVal(d,s); return `<td class="heat" style="${heatSt(v)}">${nz(v)}</td>`; }).join("")}</tr>`; }).join("")+
   `</tbody><tfoot><tr><th></th><th>Rata-rata kelas</th><th></th><th>${nz(mean(aw.map(r=>r.an.diag.nilai)))}</th><th></th><th>${nz(mean(t1.map(r=>r.an.to1.nilai)))}</th><th>${nz(mean(t2.map(r=>r.an.to2.nilai)))}</th><th></th>${subs.map(s=>`<th>${nz(mean(aw.map(r=>subVal(r.an.diag,s))))}</th>`).join("")}</tr></tfoot></table>
   <p class="small">Nilai dihitung ulang dari jawaban siswa dengan kunci pada aplikasi ini, bukan diambil dari angka yang dikirim siswa. Warna: merah rendah, hijau tinggi. Klik nama untuk melihat rincian.</p></div>`;
  return h;
}
function guruCsv(){
  const subs=subList(); const rows=[["No","Nama","Aktif terakhir","Asesmen Awal","Modul selesai","Tryout 1","Tryout 2","Selisih (terakhir − Awal)",...subs.map(s=>"Awal: "+s)]];
  GC.rows.forEach(r=>{ const d=r.an.diag,t=r.an.to1,t2_=r.an.to2,lt=t2_||t; rows.push([r.no,r.name,r.at?new Date(r.at).toLocaleString("id-ID"):"",d?d.nilai:"",r.rec?r.mods:"",t?t.nilai:"",t2_?t2_.nilai:"",d&&lt?lt.nilai-d.nilai:"",...subs.map(s=>nz(subVal(d,s)).toString().replace("–",""))]); });
  csvOut("rekap_bcf.csv",rows);
}
function csvOut(name,rows){ const csv=rows.map(r=>r.map(c=>`"${String(c).replace(/"/g,'""')}"`).join(",")).join("\n"); const a=document.createElement("a"); a.href=URL.createObjectURL(new Blob(["﻿"+csv],{type:"text/csv"})); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500); }

function guruDetail(){
  const r=GC.rows.find(x=>x.sid===GC.detail); if(!r||!r.rec) return `<button class="btn btn-ghost btn-sm" data-act="back">← Kembali</button><p>Data tidak ditemukan.</p>`;
  const d=r.an.diag,t=r.an.to1,t2_=r.an.to2; let h=`<button class="btn btn-ghost btn-sm" data-act="back">← Kembali ke rekap</button>
   <div class="card" style="margin-top:12px"><div class="gtop"><div><h2 style="margin:0">${esc(r.name)}</h2><p class="muted" style="margin:2px 0 0">Aktif ${ago(r.at)} · ${r.mods} / ${MODNUM.length} modul selesai</p></div><button class="btn btn-primary btn-sm" data-act="sj" data-sid="${r.sid}">⬇ Unduh JSON siswa</button></div>
   <div class="kpis" style="margin-top:12px"><div class="kpi"><b>${d?d.nilai:"–"}</b><span>Asesmen Awal${d?" · "+predikat(d.nilai):""}</span></div><div class="kpi"><b>${t?t.nilai:"–"}</b><span>Tryout 1${t?" · "+predikat(t.nilai):""}</span></div><div class="kpi"><b>${t2_?t2_.nilai:"–"}</b><span>Tryout 2${t2_?" · "+predikat(t2_.nilai):""}</span></div></div></div>`;
  if(d){ if(d.prioritas.length) h+=`<div class="card"><b>Modul prioritas (dari Asesmen Awal)</b><div class="recs" style="margin-top:8px">${d.prioritas.map(k=>`<span class="rec">★ Modul ${k} · ${esc(MOD[k].meta.title)}</span>`).join("")}</div></div>`;
    d.groups.slice(0,2).forEach(g=>{ h+=`<section class="card"><h3>Asesmen Awal · ${esc(g.title)}</h3>${bars(g.rows)}</section>`; }); }
  if(t) t.groups.slice(0,1).forEach(g=>{ h+=`<section class="card"><h3>Tryout 1 · ${esc(g.title)}</h3>${bars(g.rows)}</section>`; });
  if(t2_){ if(t2_.prioritas.length) h+=`<div class="card"><b>Modul yang perlu diulang (dari Tryout 2)</b><div class="recs" style="margin-top:8px">${t2_.prioritas.map(k=>`<span class="rec">Modul ${k} · ${esc(MOD[k].meta.title)}</span>`).join("")}</div></div>`;
    t2_.groups.slice(0,2).forEach(g=>{ h+=`<section class="card"><h3>Tryout 2 · ${esc(g.title)}</h3>${bars(g.rows)}</section>`; }); }
  h+=`<section class="card"><h3>Kemajuan modul</h3><table class="gtab"><thead><tr><th>Modul</th><th>Bagian dibuka</th><th>Latihan dijawab</th><th>Rata-rata latihan</th><th>Status</th></tr></thead><tbody>`+MODNUM.map(n=>{ const mr=(r.rec.mod||{})[n]; const tot=secList(MOD[n]).length; const sk=mr?Object.values(mr.s||{}):[];
    return `<tr><td>Modul ${n} · ${esc(MOD[n].meta.title)}</td><td>${mr?Object.keys(mr.visited||{}).length:0} / ${tot}</td><td>${sk.length}</td><td>${sk.length?Math.round(sk.reduce((a,b)=>a+b,0)/sk.length*100)+"%":"–"}</td><td>${mr&&mr.done?'<span class="badge g">Selesai</span>':'<span class="badge x">Belum</span>'}</td></tr>`; }).join("")+`</tbody></table></section>`;
  return h;
}
function guruButir(){
  const ks=["diag","to1","to2"]; const k=GC.paket; const P=PAKET[k], qs=P.qs(); const fin=GC.rows.filter(r=>r.an[k]);
  const st=qs.map((q,i)=>{ const sk=fin.map(r=>r.an[k].items[i].skor); return {no:i+1,q,pct:sk.length?Math.round(sk.reduce((a,b)=>a+b,0)/sk.length*100):null}; });
  const sorted=[...st].sort((a,b)=>(a.pct==null)-(b.pct==null)||(a.pct||0)-(b.pct||0));
  return `<div class="card"><div class="actions" style="margin:0 0 8px;align-items:center"><label class="small">Paket:</label><select id="gPaket" class="search" style="width:auto;margin:0">${ks.map(x=>`<option value="${x}" ${x===k?"selected":""}>${PAKET[x].title}</option>`).join("")}</select><span class="small">${fin.length} siswa sudah mengerjakan · diurutkan dari yang tersulit</span></div>`+
   (fin.length?sorted.map(s=>`<div class="rowbar"><div class="lab"><b>No ${s.no} · ${esc(s.q.stem.slice(0,100))}${s.q.stem.length>100?"…":""}</b><span>${FORM[s.q.kind]}${s.q.meta.sub?" · "+esc(s.q.meta.sub):""}${s.q.meta.modul&&s.q.meta.modul.length?" · Modul "+s.q.meta.modul.join(", "):""}${s.q.label?" · "+esc(s.q.label):""}</span></div><div class="track"><i class="${colorCls(s.pct)}" style="width:${s.pct}%"></i></div><div class="val">${s.pct}%</div></div>`).join(""):'<p class="muted">Belum ada siswa yang menyelesaikan paket ini.</p>')+`</div>`;
}

/* ---- kelola siswa ---- */
function guruAkun(){
  const R=GC.rows, belum=R.filter(r=>!r.akun).length;
  let h=`<div class="card"><h3 style="margin:0 0 6px">Akun siswa</h3><p class="muted">Siswa masuk dengan memilih nama lalu mengetik PIN 6 angka. PIN dibuat acak dan hanya terbaca oleh guru.</p>
   <div class="actions" style="margin:0 0 8px"><button class="btn btn-primary btn-sm" data-act="mk" ${belum&&!GC.busy?"":"disabled"}>Buat akun untuk ${belum} siswa yang belum punya</button><button class="btn btn-ghost btn-sm" data-act="cetak">🖨 Cetak kartu PIN</button><button class="btn btn-ghost btn-sm" data-act="pincsv">⬇ Daftar PIN (CSV)</button><button class="btn btn-ghost btn-sm" data-act="togglepin">${GC.showPin?"Sembunyikan":"Tampilkan"} PIN</button></div>
   ${GC.msg?`<p class="small" id="gM">${GC.msg}</p>`:""}
   <table class="gtab"><thead><tr><th>No</th><th>Nama</th><th>Akun</th><th>PIN</th><th></th></tr></thead><tbody>`+
   R.map(r=>{ const p=GC.pin[r.sid]; return `<tr><td>${r.no}</td><td>${esc(r.name)}</td><td>${r.akun?'<span class="badge g">Aktif'+(r.akun.versi>1?" · v"+r.akun.versi:"")+'</span>':'<span class="badge x">Belum dibuat</span>'}</td><td style="font-family:monospace;letter-spacing:2px">${p?(GC.showPin?esc(p.pin):"••••••"):"–"}</td><td>${r.akun?`<button class="linkbtn" data-act="reset" data-sid="${r.sid}">Reset PIN</button>`:""}</td></tr>`; }).join("")+`</tbody></table></div>`;
  return h;
}
async function guruBuat(names,reset){
  if(GC.busy||!names.length) return; GC.busy=true; const sm={}; GC.siswa.forEach(s=>sm[s.sid]=s); const entries=[]; let gagal=[];
  for(let i=0;i<names.length;i++){ const name=names[i], sid=slug(name); GC.msg=`Membuat akun ${i+1} / ${names.length}: ${esc(name)}…`; drawGuruBody();
    let versi=sm[sid]?(sm[sid].versi||1)+(reset?1:0):1, ok=false;
    for(let t=0;t<4&&!ok;t++){ const pin=CL.randPin();
      try{ const a=await CL.buatAkun(sid,name,versi,pin); entries.push({sid,name,email:a.email,uid:a.uid,versi,pin}); ok=true; }
      catch(e){ if(/email-already-in-use/.test((e&&e.code)||"")) versi++; else { gagal.push(name+" ("+((e&&e.code)||"galat")+")"); break; } } } }
  try{
    if(entries.length){ const all={}; GC.siswa.forEach(s=>all[s.sid]={sid:s.sid,name:s.name,email:s.email}); entries.forEach(e=>all[e.sid]={sid:e.sid,name:e.name,email:e.email});
      await CL.catatSiswa(entries,Object.values(all)); }
    GC.msg=`Selesai: ${entries.length} akun dibuat${gagal.length?`. Gagal: ${esc(gagal.join("; "))}`:"."} ${entries.length?"Cetak kartu PIN lalu bagikan ke siswa.":""}`;
  }catch(e){ GC.msg=`Akun sudah dibuat tetapi gagal dicatat ke basis data (${esc((e&&e.code)||e)}). Periksa aturan Firestore, lalu tekan tombol lagi.`; }
  GC.busy=false; guruRefresh();
}
function cetakKartu(){
  const items=GC.rows.filter(r=>r.akun&&GC.pin[r.sid]); if(!items.length) return alert("Belum ada akun/PIN untuk dicetak.");
  const w=window.open("","_blank"); if(!w) return alert("Izinkan pop-up pada peramban untuk mencetak kartu.");
  w.document.write(`<!doctype html><meta charset="utf-8"><title>Kartu PIN</title><style>body{font-family:Arial,sans-serif;margin:12mm}h3{margin:0 0 10px;font-size:14px}.g{display:grid;grid-template-columns:1fr 1fr;gap:8px}.c{border:1px dashed #555;padding:10px 12px;break-inside:avoid;font-size:12.5px;line-height:1.5}.c b{font-size:14px}.p{font:700 22px monospace;letter-spacing:5px}</style><h3>Kartu PIN · Platform Pembekalan TKA BCF · Kelas XII Produksi Film SMKN Ile Boleng</h3><div class="g">${items.map(r=>`<div class="c"><b>${esc(r.name)}</b><br>Alamat: ${esc(location.origin)}<br>PIN: <span class="p">${esc(GC.pin[r.sid].pin)}</span><br><small>Pilih namamu, ketik PIN. Jangan bagikan PIN.</small></div>`).join("")}</div><script>onload=function(){print()}<\/script>`);
  w.document.close();
}
function pinCsv(){ const rows=[["No","Nama","PIN"]]; GC.rows.forEach(r=>{ if(GC.pin[r.sid]) rows.push([r.no,r.name,GC.pin[r.sid].pin]); }); csvOut("daftar_pin_bcf.csv",rows); }
