# Panduan Pemasangan · Platform Pembekalan TKA BCF (online)

Waktu pengerjaan sekitar 30–40 menit. Semua layanan memakai paket gratis (Firebase Spark, Vercel Hobby), tanpa kartu kredit.

Isi paket:
- `public/` — situs yang diunggah ke Vercel (aplikasi, PWA, `firebase-config.js`).
- `firestore.rules` — aturan keamanan basis data (wajib dipasang).
- `vercel.json`, `firebase.json` — konfigurasi.
- `sumber/cloud.js` — kode sambungan Firebase (sebelum dibundel), untuk dibaca.

## A. Firebase

1. Buka https://console.firebase.google.com, masuk dengan akun Google, lalu **Create a project** (nama bebas, mis. `tka-bcf-ileboleng`). Google Analytics boleh dimatikan.
2. **Project settings (ikon roda gigi) → Your apps → ikon web `</>`** → beri nama → **Register app**. Salin blok `firebaseConfig`.
3. Buka `public/firebase-config.js`, ganti semua nilai `ISI_...` dengan nilai dari langkah 2. Kunci ini memang tampil di peramban dan bukan rahasia; keamanan dijaga oleh `firestore.rules`.
4. **Build → Authentication → Get started → Sign-in method → Email/Password → Enable → Save.**
5. **Build → Firestore Database → Create database** → pilih lokasi `asia-southeast2 (Jakarta)` → **Production mode**.
6. Tab **Rules** pada Firestore → hapus isinya → tempel seluruh isi `firestore.rules` → **Publish**.
7. Buat akun guru: **Authentication → Users → Add user** (email dan kata sandi Bapak sendiri). Salin **User UID** akun itu.
8. **Firestore → Start collection** → ID koleksi `guru` → Document ID = UID tadi → tambah satu field `nama` (string) berisi `Frans` → Save. Dokumen inilah yang menjadikan akun tersebut guru.

## B. Vercel

1. Buat akun di https://vercel.com (boleh masuk dengan GitHub).
2. Cara paling mudah: unggah folder ini ke repositori GitHub baru, lalu di Vercel pilih **Add New → Project → Import** repositori itu. Framework: **Other**. Pengaturan lain biarkan (sudah diatur oleh `vercel.json`: folder keluaran `public`, tanpa perintah build). **Deploy.**
   Alternatif lewat terminal: `npm i -g vercel`, masuk ke folder ini, jalankan `vercel --prod`.
3. Catat alamat situs (mis. `tka-bcf.vercel.app`).
4. Kembali ke Firebase: **Authentication → Settings → Authorized domains → Add domain** → masukkan alamat Vercel tadi (tanpa `https://`).

## C. Menyiapkan siswa

1. Buka situs → **Rekap Guru** → masuk dengan akun guru (langkah A7).
2. Tab **Kelola siswa → Buat akun untuk … siswa**. Tunggu sampai muncul "Selesai: 31 akun dibuat".
3. **Cetak kartu PIN** (atau unduh CSV), lalu bagikan kartu ke masing-masing siswa. PIN tersimpan hanya di Firestore dan hanya terbaca oleh guru; bila ada siswa lupa, buka tab yang sama, atau **Reset PIN**. Reset tidak menghapus kemajuan belajar siswa.
4. Siswa membuka situs, memilih nama, mengetik PIN. Centang "Ingat saya" hanya di ponsel pribadi, jangan di komputer lab.
5. Opsional setelah semua akun jadi: pada **Authentication → Settings → User actions**, matikan *Enable create (sign-up)* bila opsi itu tersedia pada konsol Bapak, supaya orang luar tidak bisa membuat akun lewat kunci web. Nyalakan lagi hanya saat menambah/reset akun.

## D. Memakai di lab dan di rumah

- Hasil tersimpan otomatis ke server beberapa detik setelah siswa bekerja; pojok kanan atas menunjukkan status (☁ Tersimpan, ⟳ Mengirim, ⚠ Offline).
- Jika jaringan putus, siswa tetap bisa mengerjakan; data antre di perangkat dan terkirim sendiri saat jaringan kembali. Tombol **Unduh JSON** tetap tersedia sebagai cadangan.
- Ponsel: Chrome Android → menu ⋮ → **Pasang aplikasi**; iPhone (Safari) → Bagikan → **Tambah ke Layar Utama**. Setelah dibuka sekali dengan internet, aplikasi bisa dibuka tanpa internet.
- Kuota gratis Firebase (50 ribu baca dan 20 ribu tulis per hari) lebih dari cukup untuk 31 siswa.

## E. Batasan yang perlu Bapak ketahui

1. **Kunci jawaban masih ada di dalam berkas aplikasi.** Siswa yang paham membuka kode sumber bisa melihatnya. Nilai di dashboard dihitung ulang dari jawaban siswa, sehingga angka nilai tidak bisa dipalsukan lewat data, tetapi jawaban benar tetap bisa diintip. Untuk tryout resmi, awasi seperti ujian biasa di lab. Tahap berikutnya (bila diperlukan): soal dan kunci dipindah ke Firestore dan kunci baru dibuka setelah siswa mengumpulkan.
2. Daftar nama siswa terbaca publik (dibutuhkan halaman login). Datanya hanya nama; PIN dan hasil tidak publik.
3. Satu perangkat satu sesi aktif adalah praktik terbaik: jika siswa bekerja bersamaan di dua perangkat, yang tersimpan terakhir yang menang untuk bagian yang sama (hasil yang sudah dikumpulkan tidak akan tertimpa).
4. PIN 6 angka dilindungi pembatasan percobaan bawaan Firebase; jangan dibagikan di grup.
5. Pembaruan aplikasi: unggah ulang berkas ke Vercel; siswa menerima versi baru pada pembukaan berikutnya.
