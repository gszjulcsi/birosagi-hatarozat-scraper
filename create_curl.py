from process_birosagok_response import birosagok_koddal

curl_template = """curl 'http://ukp.birosag.hu/portal-frontend/hu.sri.uke.portal.AnonimizaltHatarozatok/springGwtServices/anonimizaltHatarozatokFrontendService' \
-H 'Cookie: JSESSIONID=4B4F5B0E282B91BBAC5C035049E6F48F; __utmc=186801467; __utmz=186801467.1525070800.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SL_C_23361dd035530_KEY=872f5401cde0da68372b0b841aec2dcca3f32bf0; __utma=186801467.2115107260.1525070800.1525160416.1525163177.5' \
-H 'Origin: http://ukp.birosag.hu' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,hu;q=0.8,de;q=0.7,sv;q=0.6' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36' \
-H 'Content-Type: text/x-gwt-rpc; charset=UTF-8' -H 'Accept: */*' -H 'X-GWT-Module-Base: http://ukp.birosag.hu/portal-frontend/hu.sri.uke.portal.AnonimizaltHatarozatok/' \
-H 'X-GWT-Permutation: AAFE4A0A2B240DD334C3DDF9092A910D' -H 'Referer: http://ukp.birosag.hu/portal-frontend/embeddable_anonimhatarozatok.html' -H 'Connection: keep-alive' \
--data-binary $'7|0|21|http://ukp.birosag.hu/portal-frontend/hu.sri.uke.portal.AnonimizaltHatarozatok/|1485B3A2F9FEFDD2D6996339C27D6304|hu.sri.uke.portal.shared.services.AnonimizaltHatarozatokFrontendService|fetchAnonimizaltHatarozatok|java.lang.String/2004016611|hu.sri.uke.portal.shared.dto.SolrMetadataDTO/3753956777|com.sencha.gxt.data.shared.loader.PagingLoadConfig||hu.sri.uke.portal.shared.dto.BirosagKodDTO/249899968|{birosag_tipus_parameter}{jogterulet_parameter}com.sencha.gxt.data.shared.loader.PagingLoadConfigBean/38458988|1|2|3|4|3|5|6|7|8|6|9|10|11|12|13|D|13|C|14|15|-4|13|B|16|0|8|0|17|{year}|16|0|18|0|19|20|-6|-6|0|0|0|0|0|0|0|21|{resultLength}|{offset}|16|0|' \
--compressed"""


# print(curl_template)

def clean_up(name):
    return name.replace('á', '\\xe1').replace('Á', '\\xc1')\
            .replace('é', '\\xe9').replace('É', '\\xc9')\
            .replace('í', '\\xed').replace('Í', '\\xcd')\
            .replace('ó', '\\xf3').replace('Ó', '\\xd3')\
            .replace('ö', '\\xf6').replace('Ö', '\\xd6')\
            .replace('ő', '\\u0151').replace('Ő', '\\u0150')\
            .replace('ü', '\\xfc').replace('Ű', '\\xdc')\
            .replace('ú', '\\xfa').replace('Ú', '\\xda')\
            .replace('ű', '\\u0171').replace('Ű', '\\u0170')

def birosag_tipus_parameter(birosagKod, birosagNev):
    if birosagKod == 'K':
        return 'hu.sri.uke.portal.shared.dto.BirosagTipusDTO/997099267|K|K\\xfaria|java.lang.Long/4227064769|0001|java.util.ArrayList/4159755760||java.lang.Integer/3438268394|'
    else:
        birosagTipus = ''
        birosagTipusKod = ''
        if "ítélőtábla" in birosagNev.lower():
            birosagTipus = "\\xcdt\\xe9l\\u0151t\\xe1bla"
            birosagTipusKod = "I"
        elif "törvényszék" in birosagNev.lower():
            birosagTipus = "Törv\\xe9nysz\\xe9k"
            birosagTipusKod = "T"
        elif "bíróság" in birosagNev.lower():
            birosagTipus = "J\\xe1r\\xe1sb\\xedr\\xf3s\\xe1g"
            birosagTipusKod = "J"
        if birosagTipus == '' or birosagTipusKod == '':
            return ''
        else:
            return 'hu.sri.uke.portal.shared.dto.BirosagTipusDTO/997099267|{tipusKod}|{tipus}|java.lang.Long/4227064769|{kod}|{nev}|java.util.ArrayList/4159755760|java.lang.Integer/3438268394|'.format(
                tipus=clean_up(birosagTipus),
                tipusKod=birosagTipusKod,
                kod=birosagKod,
                nev=clean_up(birosagNev)
            )

def jogterulet_parameter(jogTeruletKod, jogTeruletNev):
    return 'hu.sri.uke.portal.shared.dto.JogteruletKodDTO/4168614906|{jogTeruletKod}|{jogTeruletNev}|'.format(
        jogTeruletKod=clean_up(jogTeruletKod),
        jogTeruletNev=clean_up(jogTeruletNev)
        )

bunteto_jogterulet = {
    # bunteto kollegium B
    'SZJ': 'szab\\xe1lys\\xe9rt\\xe9si jog',
    'BJ': 'b\\xfcntet\\u0151jog', 
    'KBJ': 'katonai b\\xfcntet\\u0151jog',
    'BVJ': 'b\\xfcntet\\xe9s v\\xe9grehajt\\xe1si \\xfcgy',
    # polgari  P
    'VJ': 'v\\xe9grehajt\\xe1si \\xfcgy',
    'PJ': 'polg\\xe1ri jog',
    # gazdasagi G
    'GJ': 'gazdas\\xe1gi jog',
    # kollegium KM|közigazgatási-munkaügyi
    'MJ': 'munka\\xfcgy',  
    'KJ': 'k\\xf6zigazgat\\xe1si jog'
}

hatarozat_meghozatalanak_eve = range(2017, 2019) #range(1989, 2019)

birosagok_koddal = birosagok_koddal()

for year in hatarozat_meghozatalanak_eve:
    for birosagKod, birosagNev in birosagok_koddal.items():
        for jogteruletKod, jogteruletNev in bunteto_jogterulet.items():
            print(curl_template.format(
                birosag_tipus_parameter=birosag_tipus_parameter(birosagKod, birosagNev),
                jogterulet_parameter=jogterulet_parameter(jogteruletKod, jogteruletNev),
                year=year,
                resultLength=50,
                offset=0
                )
            )
