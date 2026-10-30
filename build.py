import json,hashlib,os,re,sys
from PIL import Image, ImageDraw, ImageFont
S='/home/claude/bcf-online/src/mods_v2.json'
mods=json.load(open(S)); diag=json.load(open('/home/claude/diagnostik/diagnostik_bcf.json')); to2=json.load(open('/home/claude/tryout2/to2_bcf.json'))
names=json.loads(re.search(r"names=(\[.*?\])\n",open('src/build_proto.py').read(),re.S).group(1))
assert len(names)==31
data=json.dumps({"MODS":mods,"DIAG":diag,"TO2":to2,"NAMES":names},ensure_ascii=False,separators=(',',':')).replace("</","<\\/")
t=open('src/app.online.template.html').read(); assert '/*__DATA__*/null' in t
html=t.replace('/*__DATA__*/null',data)
html=html.replace('<meta name="viewport" content="width=device-width, initial-scale=1">','<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="theme-color" content="#0b2a5b">\n<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icon-192.png">\n<link rel="apple-touch-icon" href="icon-192.png">',1)
os.makedirs('public',exist_ok=True)
open('public/index.html','w').write(html)
h=hashlib.sha1(html.encode()+open('public/cloud.js','rb').read()).hexdigest()[:10]
sw=open('src/sw.js').read().replace('__HASH__',h); open('public/sw.js','w').write(sw)
json.dump({"name":"Platform Pembekalan TKA BCF","short_name":"TKA BCF","description":"Pembekalan TKA Broadcasting dan Perfilman · Kelas XII Produksi Film SMKN Ile Boleng","start_url":"./","scope":"./","display":"standalone","orientation":"any","background_color":"#0b2a5b","theme_color":"#0b2a5b","lang":"id",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},{"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open('public/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
def icon(sz,pad):
    im=Image.new("RGB",(sz,sz),"#0b2a5b"); d=ImageDraw.Draw(im)
    try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",int(sz*0.30))
    except: f=ImageFont.load_default()
    r=int(sz*pad); d.rounded_rectangle([r,r,sz-r,sz-r],radius=int(sz*0.16),fill="#1d5fd1")
    w=d.textlength("TKA",font=f); d.text(((sz-w)/2,sz*0.36),"TKA",font=f,fill="white")
    d.rectangle([sz*0.30,sz*0.72,sz*0.70,sz*0.755],fill="#f2a516"); return im
icon(192,0.06).save('public/icon-192.png'); icon(512,0.06).save('public/icon-512.png'); icon(512,0.16).save('public/icon-maskable-512.png')
if not os.path.exists('public/firebase-config.js'):
    open('public/firebase-config.js','w').write('''/* Isi dengan konfigurasi aplikasi web dari Firebase Console (Project settings > Your apps > Web).
   Selama masih berisi ISI_..., aplikasi berjalan dalam mode lokal (tanpa server). */
window.FIREBASE_CONFIG = {
  apiKey: "ISI_API_KEY",
  authDomain: "ISI_PROJECT_ID.firebaseapp.com",
  projectId: "ISI_PROJECT_ID",
  storageBucket: "ISI_PROJECT_ID.firebasestorage.app",
  messagingSenderId: "ISI_SENDER_ID",
  appId: "ISI_APP_ID"
};
''')
print("index",os.path.getsize('public/index.html')//1024,"KB; sw",h)
