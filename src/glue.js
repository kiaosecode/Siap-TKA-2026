/* ======================================================================
   SINKRONISASI ONLINE (Firebase) — aktif bila firebase-config.js terisi
   ====================================================================== */
const CL = (window.CLOUD && window.CLOUD.ready) ? window.CLOUD : null;
const MAPEL = "bcf";
const SY = {sid:null, uid:null, timer:null, mode:"lokal", list:null, guru:false, loaded:false, lastJ:null, retry:null};
const cloudMode = () => !!(CL && SY.list && SY.list.length);

function mergeRec(L,R){
  if(!L) return R||null; if(!R) return L;
  const lu=L.updatedAt||0, ru=R.updatedAt||0, W=lu>=ru?L:R, O=lu>=ru?R:L;
  const out={name:L.name||R.name,createdAt:Math.min(L.createdAt||Infinity,R.createdAt||Infinity),updatedAt:Math.max(lu,ru),mod:{},paket:{}};
  if(!isFinite(out.createdAt)) out.createdAt=Date.now();
  const mk=new Set([...Object.keys(L.mod||{}),...Object.keys(R.mod||{})]);
  mk.forEach(n=>{ const a=(W.mod||{})[n], b=(O.mod||{})[n]; if(!a||!b){ out.mod[n]=a||b; return; }
    const m={...b,...a}; m.done=!!(a.done||b.done);
    ["visited","q","s","notes","checks","lab"].forEach(k=>{ m[k]={...(b[k]||{}),...(a[k]||{})}; }); out.mod[n]=m; });
  const pk=new Set([...Object.keys(L.paket||{}),...Object.keys(R.paket||{})]);
  pk.forEach(k=>{ const a=(W.paket||{})[k], b=(O.paket||{})[k]; if(!a||!b){ out.paket[k]=a||b; return; }
    if(a.finished&&b.finished) out.paket[k]=(a.finishedAt||0)<=(b.finishedAt||0)?a:b;   // pengumpulan pertama yang berlaku
    else if(a.finished) out.paket[k]=a; else if(b.finished) out.paket[k]=b; else out.paket[k]=a; });
  return out;
}
function syncStatus(){
  if(!CL||SY.mode!=="online") return {cls:"lokal",text:"Mode lokal · hanya di perangkat ini"};
  if(!CL.online()) return {cls:"off",text:CL.pending()?"Offline · menunggu jaringan":"Offline"};
  if(!SY.loaded) return {cls:"wait",text:"Menyambung…"};
  if(CL.pending()) return {cls:"wait",text:"Mengirim…"};
  return {cls:"ok",text:"Tersimpan di server"};
}
function drawSync(){
  const el=$("syncchip"); if(!el) return;
  const show=!!USER&&!!CL; el.classList.toggle("hidden",!show); if(!show) return;
  const s=syncStatus(); el.className="syncchip "+s.cls; el.textContent=({ok:"☁ ",wait:"⟳ ",off:"⚠ ",lokal:"◌ "}[s.cls])+s.text;
}
function queuePush(){ if(!CL||SY.mode!=="online"||!SY.sid) return; clearTimeout(SY.timer); SY.timer=setTimeout(pushNow,1800); }
function pushNow(){
  clearTimeout(SY.timer);
  if(!CL||SY.mode!=="online"||!SY.sid||!USER||!DB.students[USER]||!CL.uid()) return;
  if(!SY.loaded){ tryLoad(); return; }              // jangan menimpa data server sebelum terbaca
  const rec=DB.students[USER], j=JSON.stringify({...rec,updatedAt:0});
  if(j===SY.lastJ) return; SY.lastJ=j;
  try{ CL.simpan(SY.sid,MAPEL,rec); }catch(e){ console.warn(e); } drawSync();
}
async function tryLoad(){
  if(!CL||SY.mode!=="online"||SY.loaded||!SY.sid) return;
  const r=await CL.muat(SY.sid,MAPEL);
  if(r.gagal) { drawSync(); clearTimeout(SY.retry); SY.retry=setTimeout(tryLoad,8000); return; }
  SY.loaded=true; const local=DB.students[USER];
  DB.students[USER]=mergeRec(local,r.rec)||local||newRec(USER);
  try{ localStorage.setItem(STORE,JSON.stringify(DB)); }catch(e){}
  SY.lastJ=null; pushNow(); drawSync(); if(["home","mapel"].includes(V.name)) render();
}
window.addEventListener("online",()=>{ drawSync(); tryLoad(); pushNow(); });
window.addEventListener("offline",drawSync);
document.addEventListener("visibilitychange",()=>{ if(document.hidden) pushNow(); });
if(CL) CL.onChange(drawSync);
setInterval(drawSync,5000);

async function afterAuth(ent,uid){
  SY.sid=ent.sid; SY.uid=uid; SY.mode="online"; SY.loaded=false; SY.lastJ=null; USER=ent.name;
  if(!DB.students[USER]){ DB.students[USER]=newRec(USER); }
  await tryLoad();
}
async function cloudLogin(name,pin,ingat){
  const ent=(SY.list||[]).find(x=>x.name===name); if(!ent) return {err:"Akun untuk nama ini belum dibuat oleh guru."};
  try{ const uid=await CL.masuk(ent.email,pin,ingat); await afterAuth(ent,uid); return {ok:true}; }
  catch(e){ const c=(e&&e.code)||"";
    if(/invalid-credential|wrong-password|invalid-login|user-not-found/.test(c)) return {err:"PIN salah. Periksa kembali kartu PIN-mu."};
    if(/too-many/.test(c)) return {err:"Terlalu banyak percobaan. Tunggu beberapa menit lalu coba lagi."};
    if(/network|unavailable/.test(c)||!CL.online()) return {err:"Tidak ada jaringan.",offline:true};
    return {err:"Gagal masuk ("+(c||"tidak diketahui")+")."}; }
}
function enterLocal(name){ USER=name; SY.mode="lokal"; SY.sid=null; if(!DB.students[USER]){ DB.students[USER]=newRec(USER); save(); } go({name:"mapel"}); }
async function bootCloud(){
  if(!CL) return;
  try{ SY.list=await CL.daftar(); const u=await CL.bootUser();
    if(u){ if(await CL.apakahGuru()){ SY.guru=true; }
      else{ const ent=(SY.list||[]).find(x=>x.email===u.email); if(ent){ await afterAuth(ent,u.uid); return go({name:"mapel"}); } } }
  }catch(e){ console.warn(e); }
  if(V.name==="login") render();
}
async function doLogout(){
  if(CL&&SY.mode==="online"){
    pushNow();
    if(CL.pending()>0&&CL.online()){ for(let i=0;i<12&&CL.pending()>0;i++) await new Promise(r=>setTimeout(r,500)); }
    if(CL.pending()>0){
      return openModal(`<h3>Data belum terkirim</h3><p>Perangkat sedang tanpa jaringan, sehingga sebagian hasilmu belum sampai ke server. Datamu tetap aman di perangkat ini dan akan terkirim saat kamu masuk lagi dengan jaringan. Unduh JSON sebagai cadangan bila perlu.</p>
       <div class="row"><button class="btn btn-ghost" id="mStay">Tetap di sini</button><button class="btn btn-primary" id="mOut">Unduh JSON &amp; keluar</button></div>`),
        $("mStay").onclick=closeModal, $("mOut").onclick=async()=>{ closeModal(); downloadStudent(); await finishLogout(); };
    }
  }
  await finishLogout();
}
async function finishLogout(){
  try{ if(CL) await CL.keluar(); }catch(e){}
  USER=null; SY.mode="lokal"; SY.sid=null; SY.loaded=false; SY.lastJ=null; go({name:"login"});
}
let PWA_EVT=null;
window.addEventListener("beforeinstallprompt",e=>{ e.preventDefault(); PWA_EVT=e; const b=$("btnPasang"); if(b) b.classList.remove("hidden"); });
