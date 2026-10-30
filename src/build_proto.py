import json
mods=json.load(open('/tmp/claude-0/-home-claude/e1ce4835-a6c0-599c-8e37-52ed92ceecb5/scratchpad/mods.json'))
diag=json.load(open('/home/claude/diagnostik/diagnostik_bcf.json'))
names=["AGNESIA SAREN SAYAN","AGUSTINUS SILI BEDA","AHMAD SAPUTRA","ASMAWATI ABUBAKAR","BRENDENIUS DASI DEMON MUDA MAKIN","DIDIMUS LESU BOLEN","EMANUEL ELITZER","FABRICIO LORENZO BAHY","FITRI RAHMAN","FITRIANI TUTO","ILMA RAMDANIA","JULIANUS PHILIPUS AMA TUPEN ABA","JURIAH LATIF","MARIA NEZAVANERSI TOKAN","MARSELINA","MARTINUS BURA SUBAN RAYA MUDAMAKIN","MARTINUS PATI WATOWUAN","MELKIDIMUS DEAGUSTI ATAMUKIN","NURKAINI S. DORA","NURYASIN AMIR HUDZAIVAN","OKTAVIANUS KOPONG MITEN","ROMANRIO GELEUK OLA","SELVIANA SURA BELIDO","SIPRIANUS SINA SADA LAMANELE","SYAHARANI CB","TARSISIUS SILI TUPEN","THERESIA VELICIA PUTRI KEDANG","WULANRAMADHANI KEWA LELA","YOHANES RAYA MUDA MAKIN","YOSEP PAYONG","ZAKARIAS F. ORON TEWA"]
data=json.dumps({"MODS":mods,"DIAG":diag,"NAMES":names},ensure_ascii=False,separators=(',',':')).replace("</","<\\/")
t=open('app.template.html').read()
assert '/*__DATA__*/null' in t
open('platform-bcf.html','w').write(t.replace('/*__DATA__*/null',data))
import os; print(os.path.getsize('platform-bcf.html')//1024,'KB')
