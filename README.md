# birosagi-hatarozat-scraper

### Feladat:
"
Ez az oldal, innen kellene az összes határozatot az adataikkal együtt leszedeni (szám, bíróság neve, jogterület...): http://birosag.hu/ugyfelkapcsolati-portal/birosagi-hatarozatok-gyujtemenye"

### Problema
Az a gond, hogy az oldal minden lekeresnel kiszol egy service-nek, aminek eleg kriptikusan adja at az adatokat, es csak az elso 50 talalatot keri le, ezt jeleniti meg az ablakon belul egy kis appletben. Ezen az appleten belul a > nyilacskaval lehet haladni, es minden eredmenyt lekerdezni.
A fo problemam, hogy a hatarozatok olyan jellemzoi mint bíróság neve, jogterület, hatarozat eve nem jonnek vissza a valaszban - vagy csak encode-olva, amit eddig nem fejtettem meg. Ezt vagy a HTML oldalbol tudjuk parse-olni vagy a kimeno keres parametereibol.
 
Ez alapjan ket utat lattam:
1. Irni egy olyan robotot ami egy headless browserben minden lehetseges kombinaciojat a filter parametereknek, es a HTML tagek alapjan osszegyujteni a szukseges adatokat. Egyreszt ilyet meg sosem csinaltam, szoval ennek lenne egy tanulasi gorbeje is, masreszt neha ugy tunik, mintha bugos lenne az oldal, es nem lehetne bizonyos parameter kombokat beallitani, de egy frissites utan sikerul. Nem tudom, hogy ez a bug elojonne-e sok automatizalt lekerdezes soran, de inkabb nem kockaztatnek.

2. Egesz jol sikerult osszeraknom, hogy a backend service fele meno keresek hogyan epulnek fel. Igy ossze tudok rakni kereseket, amik egy bíróság neve, jogterület, ev kombinaciohoz visszaadjak a hatarozatokat. Ez alapjan jo sok lekerdezessel ossze tudunk rakni egy sajat adatbazist.


### Hogyan futtassuk?
Minden futtatas elott erdemes megnezni, mukodik-e meg a beepitett cookie. Ha nem, akkor browserbol ki kell masolni egy uj requestet es a cookie-t atirni. (TODO: esetleg megnezni, hogy ures cookie-val menne-e)
```
# 2012-es evre leszedni az osszes doksi urlt es parse-olni as eredmenyt
$ bash fetch_osszes_birosag.sh
$ python create_curl.py 2012 2012
$ bash curl_commands_generated_2012_2012.sh > responses_2012.txt
$  python parse_responses.py responses_2012.txt data_2012.json followup_queries.json
```


### Progress

1. Egy keressel (`fetch_osszes_birosag.sh`) le lehet szegni az osszes (157 db) birosag nevet es kodjat. Erre kesobb a requestek osszerakasanal lesz szukseg. Egyszer futtattam, a response a `birosagok.txt` file-ban talalhato. A response parse-olasat a `process_birosagok_response.py` tudja elvegezni.
2. Tobbfele request megy ki az oldalrol, ezek megerteset segitheti az `examples` es `examples_2` file-ok (ezek tartalma szimplan curl parancsok egymas utan rakosgava)
3. A celom az volt, hogy olyan requesteket rakjak ossze, melyek jogterulet, birosag es ev alapjan az osszes hatarozatot leszedik. Ezen az uton segit minket a `create_curl.py`. Ez a script curl parancsokat allit ossze megfeleloen felparameterezve.
4. A response-okat fel tudom parse-olni, amibol `(hatarozat_id, birosag, ev, jogterulet, hatarozat_url)` adat keszul el. 

