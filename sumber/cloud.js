/* Lapisan Firebase untuk Platform Pembekalan TKA. Dibundel menjadi window.CLOUD (cloud.js). */
import { initializeApp, getApps } from "firebase/app";
import { getAuth, connectAuthEmulator, signInWithEmailAndPassword, createUserWithEmailAndPassword,
  signOut, onAuthStateChanged, setPersistence, browserLocalPersistence, browserSessionPersistence } from "firebase/auth";
import { initializeFirestore, persistentLocalCache, persistentMultipleTabManager, memoryLocalCache,
  connectFirestoreEmulator, doc, getDoc, setDoc, onSnapshot, collection, writeBatch, deleteDoc } from "firebase/firestore";

const cfg = window.FIREBASE_CONFIG || {};
const EMU = window.FIREBASE_EMULATOR || null;
const DOMAIN = "xiipf.ileboleng.test";
const ready = !!(cfg.apiKey && cfg.projectId && !/ISI_|YOUR_/.test(cfg.apiKey));

let app, auth, db, secApp, secAuth;
const pend = { n: 0 };
const listeners = new Set();
const emit = () => listeners.forEach(f => { try { f(); } catch (e) {} });

if (ready) {
  app = initializeApp(cfg);
  auth = getAuth(app);
  try {
    db = initializeFirestore(app, { localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() }) });
  } catch (e) {
    db = initializeFirestore(app, { localCache: memoryLocalCache() });
  }
  if (EMU) { connectAuthEmulator(auth, `http://${EMU.host}:${EMU.auth}`, { disableWarnings: true }); connectFirestoreEmulator(db, EMU.host, EMU.fs); }
}

const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const emailFor = (sid, v) => `${sid}${v > 1 ? ".v" + v : ""}@${DOMAIN}`;
const pid = (sid, mapel) => `${sid}_${mapel || "bcf"}`;
const randPin = () => { const a = new Uint32Array(1); crypto.getRandomValues(a); return String(100000 + (a[0] % 900000)); };

async function authReady() {
  if (!ready) return null;
  return new Promise(res => { const un = onAuthStateChanged(auth, u => { un(); res(u); }); });
}
const withTimeout = (p, ms, msg) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error(msg || "timeout")), ms))]);

const CLOUD = {
  ready, slug, emailFor, randPin,
  onChange(f) { listeners.add(f); return () => listeners.delete(f); },
  pending() { return pend.n; },
  online() { return navigator.onLine !== false; },
  uid() { return auth && auth.currentUser ? auth.currentUser.uid : null; },
  email() { return auth && auth.currentUser ? auth.currentUser.email : null; },
  bootUser: authReady,

  /* ---------- daftar nama (halaman login) ---------- */
  async daftar() {
    if (!ready) return null;
    try {
      const s = await withTimeout(getDoc(doc(db, "publik", "siswa")), 8000, "daftar-timeout");
      const list = s.exists() ? (s.data().list || []) : [];
      try { localStorage.setItem("bcf-daftar", JSON.stringify(list)); } catch (e) {}
      return list;
    } catch (e) {
      try { return JSON.parse(localStorage.getItem("bcf-daftar") || "null"); } catch (x) { return null; }
    }
  },

  /* ---------- masuk / keluar ---------- */
  async masuk(email, pin, ingat) {
    await setPersistence(auth, ingat ? browserLocalPersistence : browserSessionPersistence);
    const c = await signInWithEmailAndPassword(auth, email, pin);
    return c.user.uid;
  },
  async keluar() { if (auth) await signOut(auth); },
  async apakahGuru() {
    if (!auth || !auth.currentUser) return false;
    try { const s = await getDoc(doc(db, "guru", auth.currentUser.uid)); return s.exists(); } catch (e) { return false; }
  },

  /* ---------- kemajuan siswa ---------- */
  async muat(sid, mapel) {
    try {
      const s = await withTimeout(getDoc(doc(db, "progres", pid(sid, mapel))), 12000, "muat-timeout");
      if (!s.exists()) return { ada: false, rec: null };
      return { ada: true, rec: JSON.parse(s.data().json) };
    } catch (e) { return { ada: false, rec: null, gagal: e && (e.code || e.message) }; }
  },
  simpan(sid, mapel, rec) {
    const json = JSON.stringify(rec);
    const p = setDoc(doc(db, "progres", pid(sid, mapel)), { sid, mapel: mapel || "bcf", name: rec.name, updatedAt: rec.updatedAt || Date.now(), json });
    pend.n++; emit();
    const done = () => { pend.n = Math.max(0, pend.n - 1); emit(); };
    p.then(done, e => { done(); console.warn("simpan gagal", e && e.code); });
    return p;
  },

  /* ---------- guru ---------- */
  pantauProgres(cb, onErr) {
    return onSnapshot(collection(db, "progres"), s => {
      const out = []; s.forEach(d => { const x = d.data(); try { out.push({ id: d.id, sid: x.sid, name: x.name, updatedAt: x.updatedAt, rec: JSON.parse(x.json) }); } catch (e) {} });
      cb(out, s.metadata.fromCache);
    }, onErr);
  },
  pantauSiswa(cb, onErr) {
    return onSnapshot(collection(db, "siswa"), s => {
      const out = []; s.forEach(d => out.push({ sid: d.id, ...d.data() })); cb(out);
    }, onErr);
  },
  pantauPin(cb) {
    return onSnapshot(collection(db, "pin"), s => { const o = {}; s.forEach(d => o[d.id] = d.data()); cb(o); }, () => cb({}));
  },
  /* Buat akun siswa lewat aplikasi kedua agar sesi guru tidak terganggu. */
  async buatAkun(sid, name, versi, pin) {
    if (!secApp) { secApp = initializeApp(cfg, "sekunder"); secAuth = getAuth(secApp); if (EMU) connectAuthEmulator(secAuth, `http://${EMU.host}:${EMU.auth}`, { disableWarnings: true }); }
    const email = emailFor(sid, versi);
    const c = await createUserWithEmailAndPassword(secAuth, email, pin);
    const uid = c.user.uid; await signOut(secAuth);
    return { uid, email };
  },
  async catatSiswa(entries, daftarPenuh) {
    // entries: [{sid,name,email,uid,versi,pin}], daftarPenuh: seluruh daftar [{sid,name,email}] untuk halaman login
    const b = writeBatch(db);
    entries.forEach(e => {
      b.set(doc(db, "siswa", e.sid), { name: e.name, email: e.email, uid: e.uid, versi: e.versi, aktif: true, kelas: "XII Produksi Film" });
      b.set(doc(db, "pin", e.sid), { pin: e.pin, versi: e.versi });
    });
    b.set(doc(db, "publik", "siswa"), { list: daftarPenuh, diperbarui: Date.now() });
    await b.commit();
  },
  async hapusProgres(sid, mapel) { await deleteDoc(doc(db, "progres", pid(sid, mapel))); },
};
window.CLOUD = CLOUD;
