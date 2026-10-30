import json,sys
sys.path.insert(0,'content')
import mod13,mod14
base=json.load(open('/tmp/claude-0/-home-claude/e1ce4835-a6c0-599c-8e37-52ed92ceecb5/scratchpad/mods.json'))
m=base+[mod13.MOD,mod14.MOD]
for x in m:
    if x['meta']['id']==10:
        for b in x['sectionsContent']['materi']['blocks']:
            if b['type']=='table' and b['head'][0].startswith('Istilah'):
                row=["<b>Alur kerja tapeless</b>","Perekaman langsung ke media digital (kartu memori, hard disk) tanpa pita, sehingga materi dapat langsung disalin dan disunting."]
                if row not in b['rows']: b['rows'].append(row)

# koreksi: jam tayang 22.00-03.00 berlaku untuk klasifikasi D (Dewasa), bukan R
FIX=[("program dengan klasifikasi R (Remaja) hanya boleh tayang pada pukul...","program dengan klasifikasi D (Dewasa, 18+) hanya boleh tayang pada pukul..."),
("Klasifikasi R tayang pukul 22.00-03.00 WIB.","Klasifikasi D (Dewasa, 18+) hanya boleh tayang pukul 22.00-03.00 WIB."),
("Film dengan klasifikasi 13+ boleh ditayangkan pada pukul 18.30 WIB.","Film dengan klasifikasi D (18+) boleh ditayangkan pada pukul 18.30 WIB."),
("Klasifikasi R (13+) tayang pukul 22.00-03.00.","Klasifikasi D (18+) hanya tayang pukul 22.00-03.00."),
("Program dengan Klasifikasi R (Remaja/13+) hanya boleh ditayangkan pukul","Program dengan Klasifikasi D (Dewasa/18+) hanya boleh ditayangkan pukul"),
("Program dengan klasifikasi R (Remaja) hanya boleh ditayangkan pada pukul...","Program dengan klasifikasi D (Dewasa, 18+) hanya boleh ditayangkan pada pukul..."),
("Sesuai P3SPS KPI, klasifikasi R tayang malam.","Sesuai P3SPS KPI, klasifikasi D (Dewasa, 18+) hanya tayang malam, pukul 22.00-03.00."),
("Contoh: Klasifikasi R (Remaja) hanya boleh tayang pukul","Contoh: Klasifikasi D (Dewasa) hanya boleh tayang pukul")]
_t=json.dumps(m,ensure_ascii=False)
for a,b in FIX:
    a2=json.dumps(a,ensure_ascii=False)[1:-1]; b2=json.dumps(b,ensure_ascii=False)[1:-1]
    assert _t.count(a2)==1,(a,_t.count(a2)); _t=_t.replace(a2,b2)
m=json.loads(_t)
json.dump(m,open('mods_v2.json','w'),ensure_ascii=False)
print(len(m))
