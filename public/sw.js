/* Service worker: aplikasi tetap bisa dibuka tanpa jaringan. Data Firestore ditangani SDK (IndexedDB), bukan di sini. */
const V = "bcf-05810d20c4";
const SHELL = ["./", "index.html", "cloud.js", "firebase-config.js", "manifest.webmanifest", "icon-192.png", "icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET") return;
  const u = new URL(r.url); if (u.origin !== location.origin) return;   // Firebase/Google dibiarkan langsung ke jaringan
  e.respondWith(caches.match(r, { ignoreSearch: true }).then(hit => {
    const net = fetch(r).then(res => { if (res && res.ok) { const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); } return res; })
      .catch(() => hit || caches.match("index.html"));
    return hit || net;      // dari cache dulu, diperbarui diam-diam di belakang
  }));
});
