from helpers import *
Q=[]
def q(*a): Q.extend(a)

# ---------- Bagian 1: peran dan unsur ----------
q(pick("T1","Departemen yang bertugas memilih dan menyiapkan pakaian aktor sesuai karakter adalah...",
  [("Tata busana (wardrobe)",1),("Tata rias",0),("Dekorasi properti",0)],
  "Tata busana mengurus pakaian dan aksesori. Tata rias mengurus wajah dan rambut.","T1",True),
  pick("C11","Pekerjaan merias wajah dan menata rambut aktor sesuai tuntutan peran adalah tugas...",
  [("Tata rias",1),("Tata busana",0),("Penataan set",0)],
  "Tata rias menangani wajah dan rambut, termasuk rias karakter seperti penuaan atau luka.","1.1",True),
  pick("C12","Pencahayaan set adalah tugas...",
  [("Tata cahaya, bukan tata artistik",1),("Dekorasi properti",0),("Tata busana",0)],
  "Cahaya ditangani departemen tata cahaya (Modul 2). Tata artistik bekerja pada benda, pakaian, dan rias yang akan disinari.","1.2",True),
  tf("C13","Tentukan benar atau salah untuk tiap pernyataan.",
   [("Tata busana bertugas memilih pakaian aktor, sedangkan tata rias mengatur rias wajah dan rambut.",1,"Keduanya berbeda: pakaian dan wajah."),
    ("Penataan set berkaitan dengan konstruksi dan tata ruang set, sedangkan dekorasi properti dengan penempatan benda.",1,"Ruang dibentuk lebih dulu, lalu diisi benda."),
    ("Penataan set dan dekorasi properti memiliki tugas yang sepenuhnya identik.",0,"Berbeda: struktur ruang dan benda pengisinya.")],"Soal 1.3 · benar atau salah"))

# ---------- Bagian 2: klasifikasi ----------
q(pick("T2","Vas bunga kecil di meja tamu yang tidak disentuh aktor dan hanya memperindah latar termasuk...",
  [("Set dressing",1),("Action prop",0),("Set structure",0)],
  "Benda dekoratif penunjang atmosfer yang tidak disentuh aktor adalah set dressing.","T2",True),
  pick("C21","Cangkir kopi yang dipegang dan diminum aktor dalam adegan sarapan termasuk...",
  [("Action prop",1),("Set dressing",0),("Set structure",0)],
  "Benda yang berinteraksi langsung dengan aktor dalam adegan adalah action prop.","2.1",True),
  pick("C22","Dinding, lantai, pintu, dan tangga yang dibangun untuk set termasuk...",
  [("Set structure (konstruksi set)",1),("Set dressing",0),("Action prop",0)],
  "Bagian bangunan set disebut set structure.","2.2",True),
  pick("C23","Sofa dan meja makan yang melengkapi fungsi ruang dan menjadi bagian dari set termasuk...",
  [("Set property",1),("Action prop",0),("Rias karakter",0)],
  "Set property adalah perabot atau benda besar yang melengkapi fungsi ruang dan menjadi bagian dari set.","2.3",True),
  tf("C24","Tentukan benar atau salah untuk tiap pernyataan.",
   [("Benda yang sama dapat berpindah kategori menurut fungsinya dalam adegan.",1,"Cangkir di rak adalah set dressing, tetapi menjadi action prop saat aktor meminumnya."),
    ("Wardrobe termasuk unsur set yang dibangun, seperti dinding dan lantai.",0,"Wardrobe adalah pakaian aktor, bukan bagian set."),
    ("Action prop paling rawan terhadap kesalahan kontinuitas karena dipegang dan berubah selama adegan.",1,"Isi gelas atau posisi benda dapat berubah antar-shot.")],"Soal 2.4 · benar atau salah"))

# ---------- Bagian 3: wardrobe dan rias ----------
q(pick("C31","Aktor berperan sebagai kakek berusia 80 tahun. Tata rias yang dipakai untuk menampilkan penuaan disebut...",
  [("Rias karakter",1),("Rias korektif",0),("Set dressing",0)],
  "Rias karakter mengubah penampilan sesuai peran seperti usia atau luka. Rias korektif menjaga penampilan alami.","3.1",True),
  pick("C32","Pakaian dan aksesori disiapkan agar sesuai karakter, era, dan perkembangan cerita. Ini fungsi...",
  [("Tata busana",1),("Tata rias",0),("Tata suara",0)],
  "Wardrobe membantu penonton memahami siapa karakter itu dan kapan ia hidup.","3.2",True),
  pick("C33","Foto kondisi pakaian dan rias sebelum syuting berguna untuk...",
  [("Menjaga kontinuitas antar-shot dan antar-hari syuting",1),("Menggantikan naskah",0),("Mengatur pencahayaan",0)],
  "Foto menjadi acuan agar tampilan sama, seperti kancing, lengan, atau luka di wajah.","3.3",True))

# ---------- Latihan ----------
q(pick("S1","Dalam sebuah set terdapat tiga benda. Benda P: foto keluarga yang dipasang di dinding tanpa disentuh aktor. Benda Q: pedang mainan yang dihunus aktor dalam adegan. Benda R: tangga kayu yang dibangun sebagai bagian rumah. Klasifikasi P, Q, dan R secara berurutan adalah...",
  [("Set dressing, Action prop, Set structure",1,"Foto menunjang suasana, pedang dipegang aktor, tangga bagian bangunan set."),
   ("Action prop, Set dressing, Set structure",0,"Foto tidak disentuh aktor, jadi bukan action prop."),
   ("Set structure, Action prop, Set dressing",0,"Foto bukan bagian bangunan, tangga bukan sekadar dekorasi."),
   ("Set dressing, Set structure, Action prop",0,"Pedang yang dipegang aktor bukan set structure."),
   ("Set property, Set dressing, Action prop",0,"Pedang yang dipegang adalah action prop dan tangga bagian bangunan.")],
  "Klasifikasi ditentukan oleh fungsi benda dan interaksinya dengan aktor: dekoratif tak disentuh, dipegang aktor, atau bagian bangunan.","Soal 1 · memahami · pilihan ganda"),
  pick("S2","Departemen tata artistik memiliki subbidang penataan set, dekorasi properti, tata busana, dan tata rias. Manakah pasangan subbidang dan tugas yang paling tepat?",
  [("Tata busana memilih dan menyiapkan pakaian sesuai karakter; tata rias mengatur riasan wajah dan rambut sesuai peran.",1,"Pembagian yang benar."),
   ("Tata busana merias wajah; tata rias memilih pakaian.",0,"Terbalik."),
   ("Dekorasi properti mengatur pencahayaan; penataan set memilih kostum.",0,"Pencahayaan bukan tugas dekorasi dan kostum bukan tugas penataan set."),
   ("Tata rias hanya membersihkan wajah; tata busana hanya menyetrika.",0,"Mereduksi peran secara keliru."),
   ("Penataan set dan dekorasi properti selalu identik.",0,"Struktur ruang berbeda dengan benda pengisinya.")],
  "Pakaian untuk tata busana, wajah dan rambut untuk tata rias, struktur ruang untuk penataan set, benda pengisi untuk dekorasi properti.","Soal 2 · memahami · pilihan ganda"),
  mcma("S3","Pilih semua pernyataan yang tepat tentang fungsi tata artistik.",
   [("Membangun latar tempat dan waktu cerita.",1,"Set dan benda menunjukkan lokasi dan era."),
    ("Membantu menunjukkan karakter lewat pakaian dan rias.",1,"Wardrobe dan rias menyampaikan status dan kepribadian."),
    ("Menjaga kontinuitas benda, pakaian, dan rias antar-shot.",1,"Tampilan harus konsisten."),
    ("Mengatur eksposur kamera dan frame rate.",0,"Itu pekerjaan tata kamera."),
    ("Merekam dialog di lokasi.",0,"Itu pekerjaan tata suara.")],
   "Tata artistik menentukan apa yang tampak di depan kamera: tempat, benda, pakaian, dan rias.","Soal 3 · memahami · pilihan majemuk"),
  tf("S4","Tentukan benar atau salah untuk tiap pernyataan.",
   [("Set dressing adalah benda dekoratif yang tidak perlu disentuh aktor.",1,"Fungsinya membangun atmosfer."),
    ("Action prop adalah benda yang dipakai langsung oleh aktor dalam adegan.",1,"Contoh: telepon yang diangkat."),
    ("Tata rias termasuk pengaturan pakaian aktor.",0,"Pakaian adalah tugas tata busana.")],"Soal 4 · memahami · benar atau salah"))

# ---------- Cek akhir ----------
q(pick("L1","Tiga benda dalam adegan. Benda X: tangga kayu bagian dari set rumah. Benda Y: sofa yang melengkapi ruang tamu. Benda Z: gelas yang diminum aktor. Klasifikasi X, Y, dan Z secara berurutan adalah...",
  [("Set structure, Set property, Action prop",1),("Set property, Set structure, Action prop",0),("Set dressing, Set property, Set structure",0),("Action prop, Set property, Set dressing",0),("Set structure, Set dressing, Set property",0)],
  "Tangga bagian bangunan set. Sofa perabot yang melengkapi fungsi ruang. Gelas yang diminum adalah action prop.","Cek 1 · memahami"),
  pick("L2","Dalam film berlatar tahun 1960-an di kampung, seorang aktor tampak memakai jam tangan digital modern. Departemen yang paling bertanggung jawab memeriksanya adalah...",
  [("Tata busana, karena aksesori termasuk bagian pakaian aktor",1,"Aksesori dikelola tata busana dan harus sesuai era."),
   ("Tata suara",0,"Tidak berkaitan dengan tampilan."),
   ("Tata rias",0,"Rias menangani wajah dan rambut."),
   ("Penata cahaya",0,"Cahaya tidak menentukan kesesuaian aksesori."),
   ("Editor",0,"Editor bukan penanggung jawab kesesuaian era di lokasi.")],
  "Kesesuaian pakaian dan aksesori dengan era adalah tugas tata busana.","Cek 2 · memahami"),
  mcma("L3","Pada shot pertama aktor memiliki luka di dahi, tetapi pada shot ketiga luka itu hilang. Pilih semua pernyataan yang tepat.",
   [("Ini kesalahan kontinuitas rias.",1,"Tampilan rias tidak konsisten antar-shot."),
    ("Foto dan catatan kondisi rias sebelum syuting membantu mencegahnya.",1,"Foto menjadi acuan."),
    ("Tata rias bertugas menjaga konsistensi luka itu sepanjang adegan.",1,"Luka termasuk rias karakter."),
    ("Masalah ini dapat diatasi dengan menaikkan ISO.",0,"ISO tidak berkaitan."),
    ("Masalah ini tugas tata suara.",0,"Tata suara tidak mengurus tampilan.")],
   "Kontinuitas rias dijaga oleh tata rias dengan foto dan catatan.","Cek 3 · memahami"))

SC={"b1":["T1","C11","C12","C13"],"b2":["T2","C21","C22","C23","C24"],"b3":["C31","C32","C33"],"latihan":["S1","S2","S3","S4"],"cek":["L1","L2","L3"]}
PK=["pa1","pa2","pa3","pa4","pb1","pb2","pb3","pc1","pc2"]
meta={"id":14,"storageKey":"fke-modul14-mandiri-v1","topKick":"Modul 14","kicker":"Modul 14 · Elemen 3 BCF · Persiapan TKA 2026",
 "title":"Tata Artistik","intro":"Memahami fungsi, klasifikasi, dan istilah dasar unsur tata artistik: penataan set, dekorasi properti, tata busana (wardrobe), dan tata rias. Untuk siswa kelas XII Produksi Film, Elemen 3 sub-elemen Tata Artistik.",
 "chips":[{"label":"Memahami","color":"#ffb454"}],
 "howto":["<b>1. Tebak dulu, baru baca.</b> Tiap bagian dibuka dengan kotak <span class=\"small\">Tebak dulu</span> atau diakhiri <span class=\"small\">Cek paham</span>.","<b>2. Kenali dari fungsi.</b> Klasifikasi benda ditentukan oleh fungsinya dalam adegan, bukan oleh bentuknya.","<b>3. Praktik.</b> Bagian Praktik memakai benda dan pakaian yang tersedia di sekolah."],
 "objectives":["<b>Memahami:</b> membedakan tugas penataan set, dekorasi properti, tata busana, dan tata rias.","<b>Memahami:</b> mengklasifikasikan benda sebagai set structure, set dressing, set property, atau action prop.","<b>Memahami:</b> menjelaskan peran wardrobe dan rias dalam karakter dan kontinuitas."]}
sections=[{"id":"mulai","nav":"Mulai","title":"Tata Artistik"},
 {"id":"b1","nav":"Bagian 1","title":"Peran dan unsur tata artistik","time":"20 menit"},
 {"id":"b2","nav":"Bagian 2","title":"Klasifikasi set dan properti","time":"25 menit"},
 {"id":"b3","nav":"Bagian 3","title":"Wardrobe dan tata rias","time":"20 menit"},
 {"id":"latihan","nav":"Latihan","title":"Latihan soal bergaya TKA","time":"20 menit"},
 {"id":"cek","nav":"Cek akhir","title":"Uji dirimu sendiri","time":"10 menit"},
 {"id":"praktik","nav":"Praktik","title":"Bengkel artistik","time":"40 menit"},
 {"id":"kartu","nav":"Kartu","title":"Kartu tata artistik"}]
B={}
B["b1"]=[tebak(["T1"]),
 lead("Tata artistik membentuk dunia yang dilihat penonton: di mana, kapan, dan siapa. Departemen ini bekerja pada ruang, benda, pakaian, dan wajah."),
 table(["Subbidang","Tugas","Contoh pekerjaan"],[
  ["<b>Penataan set panggung</b>","Merancang dan membangun atau menata ruang set sesuai naskah.","Dinding, lantai, pintu, tangga, denah set"],
  ["<b>Dekorasi properti</b>","Memilih dan menempatkan benda yang mengisi set.","Perabot, hiasan, benda yang dipakai aktor"],
  ["<b>Tata busana (wardrobe)</b>","Memilih, menyiapkan, dan merawat pakaian dan aksesori sesuai karakter, era, dan alur cerita.","Kostum, sepatu, jam tangan, topi"],
  ["<b>Tata rias</b>","Mengatur riasan wajah dan rambut sesuai tuntutan peran.","Rias alami, penuaan, luka, tata rambut"]]),
 callout("penting","Bedakan","<p>Tata busana menyangkut pakaian. Tata rias menyangkut wajah dan rambut. Dekorasi properti menyangkut benda di ruang. Pencahayaan adalah tugas tata cahaya, bukan tata artistik.</p>"),
 html("<h3>Fungsi tata artistik</h3>"),
 table(["Fungsi","Maksudnya"],[["Menetapkan latar","Tempat dan waktu cerita (era, daerah, musim)."],["Membangun karakter","Status sosial dan kepribadian lewat pakaian dan rias."],["Membangun suasana","Mood dan palet warna ruang."],["Mendukung cerita","Benda yang bermakna bagi alur."],["Menjaga kontinuitas","Benda, pakaian, dan rias konsisten antar-shot."]]),
 callout("penting","Bekerja bersama","<p>Departemen ini berkoordinasi dengan sutradara, penata kamera dan cahaya (warna dan bahan), serta script supervisor (kontinuitas, Modul 5).</p>"),
 cek(["C11","C12","C13"])]
B["b2"]=[tebak(["T2"]),
 lead("Klasifikasi benda ditentukan oleh fungsinya dan interaksinya dengan aktor, bukan oleh bentuknya."),
 table(["Kategori","Pengertian","Contoh"],[
  ["<b>Set structure</b>","Bagian bangunan set yang dibangun.","Dinding, lantai, pintu, tangga"],
  ["<b>Set dressing</b>","Benda dekoratif kecil sampai sedang yang membangun atmosfer latar dan tidak perlu disentuh aktor.","Vas bunga, lukisan, foto di dinding, tirai"],
  ["<b>Set property</b>","Perabot atau benda yang lebih besar yang melengkapi fungsi ruang dan menjadi bagian dari set.","Sofa, meja makan, lemari"],
  ["<b>Action prop</b>","Benda yang berinteraksi langsung dengan aktor dalam adegan.","Cangkir yang diminum, telepon yang diangkat, pedang mainan"]]),
 html("<h3>Cara menentukan</h3>"),
 steps([("Apakah bagian bangunan set?","Ya: set structure."),("Apakah aktor memegang atau memakainya langsung dalam adegan?","Ya: action prop."),("Apakah perabot atau benda besar yang melengkapi fungsi ruang?","Ya: set property."),("Apakah benda dekoratif yang menunjang suasana tanpa disentuh?","Ya: set dressing.")]),
 callout("waspada","Fungsi menentukan kategori","<p>Cangkir di rak dapur adalah set dressing. Saat aktor mengambil dan meminumnya, cangkir itu menjadi action prop. Wardrobe bukan unsur set; ia adalah pakaian aktor.</p>"),
 html("<h3>Kontinuitas dan keselamatan</h3>"),
 table(["Hal","Penjelasan"],[["Kontinuitas properti","Action prop paling rawan berubah antar-shot (isi gelas, posisi benda). Catat dan foto dalam log kontinuitas (Modul 5)."],["Keselamatan","Set harus kokoh. Properti senjata dan bahan mudah terbakar dikelola dengan hati-hati dan diberi tahu kepada kru (Modul 9)."]]),
 cek(["C21","C22","C23","C24"])]
B["b3"]=[
 lead("Pakaian dan rias adalah cara tercepat penonton mengenali karakter. Keduanya juga harus konsisten dari shot ke shot."),
 html("<h3>Wardrobe</h3>"),
 table(["Hal","Penjelasan"],[["Fungsi","Menunjukkan karakter, era, status, dan perkembangan cerita."],["Aksesori","Jam tangan, topi, perhiasan, dan sepatu harus sesuai era dan karakter."],["Kontinuitas","Kancing, lengan yang digulung, dan kerapian harus sama antar-shot."],["Cadangan","Pakaian kunci sering disiapkan lebih dari satu agar aman."],["Kaitan dengan kamera","Warna dan pola dapat memengaruhi gambar: pola rapat dapat berkedip, putih murni mudah berlebih eksposur (Modul 1 dan 2)."]]),
 html("<h3>Tata rias</h3>"),
 table(["Jenis","Pengertian","Contoh"],[["<b>Rias korektif</b>","Menjaga penampilan tetap alami di depan kamera.","Menyamarkan kilap kulit, menyeragamkan warna"],["<b>Rias karakter</b>","Mengubah penampilan sesuai peran.","Penuaan, luka, kantung mata"],["<b>Rias efek khusus</b>","Perubahan besar dengan bahan khusus.","Luka berat, makhluk fiksi"],["<b>Tata rambut</b>","Mengatur gaya rambut sesuai karakter dan era.","Rambut klasik tahun 1960-an"]]),
 html("<h3>Istilah dasar</h3>"),
 table(["Istilah","Arti"],[["Breakdown artistik","Daftar kebutuhan set, benda, pakaian, dan rias per adegan dari naskah."],["Mood board","Kumpulan gambar acuan suasana dan gaya visual."],["Palet warna","Susunan warna utama yang dipakai dalam film atau adegan."],["Hero prop","Benda penting yang tampil dekat dan menjadi sorotan cerita."]]),
 cek(["C31","C32","C33"])]
B["latihan"]=[callout("penting","Strategi menjawab","<p>Tanyakan pada tiap benda: dipegang aktor atau tidak, bagian bangunan atau bukan. Untuk tugas departemen, ingat pembagiannya: pakaian, wajah dan rambut, ruang, dan benda.</p>"),{"type":"qlist","ids":["S1","S2","S3","S4"]}]
B["cek"]=[callout("penting","Cara mengerjakan","<p>Pembahasan terbuka setelah ketiga soal dikunci.</p>"),{"type":"qlist","ids":["L1","L2","L3"]}]
B["praktik"]=[panel("<b>Bahan:</b> benda dan pakaian yang tersedia di sekolah, kamera atau ponsel untuk foto, kertas label, lembar breakdown. Sesuaikan dengan yang ada."),
 callout("waspada","Keselamatan","<ul><li>Properti tajam atau meniru senjata hanya dari bahan aman dan ditunjukkan kepada seluruh kru.</li><li>Jangan memanjat set atau menumpuk benda tinggi.</li><li>Gunakan bahan rias hanya milik pribadi atau yang aman dan jangan dibagi antar siswa.</li></ul>"),
 html("<h2>Praktik 1 · Klasifikasi benda <span class=\"small\">(15 menit)</span></h2><p>Tiap tim memotret atau menulis 10 benda di ruang praktik, lalu menempelkan label: set structure, set dressing, set property, atau action prop, disertai alasan fungsinya.</p>"),
 checklist([("pa1","Sepuluh benda diklasifikasikan"),("pa2","Alasan fungsi ditulis untuk tiap benda"),("pa3","Satu benda yang kategorinya berubah menurut adegan ditemukan"),("pa4","Hasil dibandingkan dengan tim lain")]),
 note("pa_r","Benda mana yang paling sulit digolongkan dan mengapa?"),
 html("<h2>Praktik 2 · Breakdown artistik satu adegan <span class=\"small\">(15 menit)</span></h2><p>Ambil satu adegan pendek. Tulis kebutuhan set, benda, pakaian, dan rias, lengkap dengan siapa yang menangani tiap kebutuhan.</p>"),
 checklist([("pb1","Kebutuhan set dan benda ditulis"),("pb2","Pakaian dan rias ditulis"),("pb3","Tiap kebutuhan dikaitkan dengan subbidang yang menangani")]),
 note("pb_r","Hal apa yang tertinggal pada daftar pertamamu?"),
 html("<h2>Praktik 3 · Uji kontinuitas artistik <span class=\"small\">(10 menit)</span></h2><p>Foto kondisi benda, pakaian, dan rias sebelum take. Ulangi adegan dan bandingkan hasilnya antar-shot.</p>"),
 checklist([("pc1","Foto acuan dibuat sebelum take"),("pc2","Perbedaan antar-shot dicatat dan diperbaiki")]),
 note("pc_r","Perbedaan apa yang paling mudah terlewat?")]
B["kartu"]=[html("<p class=\"lead\">Rangkuman Modul 14 untuk dipakai saat Tryout.</p>"),
 table(["Topik","Intinya"],[
  ["Subbidang","Penataan set: ruang. Dekorasi properti: benda. Tata busana: pakaian. Tata rias: wajah dan rambut."],
  ["Set structure","Bagian bangunan set: dinding, lantai, pintu, tangga."],
  ["Set dressing","Dekoratif penunjang atmosfer yang tidak disentuh aktor: vas, lukisan."],
  ["Set property","Perabot atau benda besar yang melengkapi fungsi ruang: sofa, meja."],
  ["Action prop","Benda yang dipakai langsung oleh aktor dalam adegan."],
  ["Fungsi menentukan","Benda yang sama dapat berpindah kategori menurut adegan."],
  ["Kontinuitas","Foto dan catat benda, pakaian, dan rias antar-shot."]])]

MOD={"meta":meta,"sections":sections,"sectionQuestions":SC,"praktikChecks":PK,"labs":{},"questions":Q,"sectionsContent":{k:{"blocks":v} for k,v in B.items()}}
