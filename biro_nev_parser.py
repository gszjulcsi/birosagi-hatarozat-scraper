import re
import sys
import os


prg = re.compile("(([A-Z]\S+){0,1}\s{0,1}[dD]r\.\s{0,1}(\S+ ){2,3}\s{0,1}s\.{0,1}\s{0,1}k\.{0,1})")
prg_2 = re.compile("(([A-Z]\S+){0,1}\s{0,1}[dD]r\.\s{0,1}( \S+){1,4})") 

prg_katonai = re.compile("([dD]r\. (\S+ ){2,3}(dand\S+bornok|ezredes|sz\S+zados) s\.{0,1}k\.)")
prg_katonai_2 = re.compile("([dD]r\. (\S+ ){2,3}(dand\S+bornok|ezredes|sz\S+zados))")

pattern_monogram = re.compile("([A-Z]\.\s*[A-Z]\.)")
pattern_dr_monogram = re.compile("[dD]r\.?\s?[A-Z]\.?\s?[A-Z]\.?")

blacklist = ["\\'fcgyv\\'e9d", "\\'dcgyv\\'e9d", "\\u220?gyv\\u233?d", "\\u252?gyv\\u233?d", 
             "v\\'e1dlott", "\cf4v\f1\'e1dlott", "alperes", "felperes", 
             "tan\\'fa",
             "szak\\'e9rt\'f5", "k\\'e9pvisel", "k\\u233?pvisel", 
             "\\u225?ltal", "\\'e1ltal", "...", "szak\\'e9rt\\'f5", "igazs\\'e1g\\'fcgyi", "neve"]

sk_lista = ["s.k.", "sk.", "s. k.", " sk", "s. k", "s.k"]

def ugyved_vagy_vadlott(talalat):
    return any([item in talalat for item in blacklist])

def monogram(talalat):
    return len(pattern_monogram.findall(talalat)) != 0 or len(pattern_dr_monogram.findall(talalat)) != 0

def remove_sk(talalat):
    for sk in sk_lista:
        talalat = talalat.replace(sk,  ' ')
    return talalat

def clean_up(talalat):
    codes = {
    "\\'e1": "á", "\\'e9": "é", "\\'f3": "ó", "\\'f6": "ö", "\\'c9": "É", "\\'c1": "Á", "\\'fc": "ü", "\\u246?": "ö",
    "\\'ed": "í", "\\'fa": "ú", "\\u337?": "ő","\\'f5": "ő", "\\'d3": "Ó", "\\'d5": "Ő","\\'fb": "ű", "\\'d6": "Ö",
    "\\u233?": "é", "\\u243?": "ó", "\\u225?": "á", "\\u252?": "ü", "\\u237?": "í", "\\u251?": "ű", "\\u193?": "Á", " \\u201?": "É", 
    "\\f1": "", "\\b0": "", "\\fs20": "",".\\fs24":"", "\\f0": "", "\\cf0": "", "\\deleted": "", "\\b": "" , "\\cf2": "", 
    "\\cf1": "", "\\cf6": "", "\\cf3": "", "\\cf4": ""
    }
    for code, letter in codes.items():
        talalat = talalat.replace(code, letter)
    return talalat.strip()


def biro_in_hatarozat(hatarozat): 
    birok = []
    if not os.path.isfile(hatarozat):
        return None
    with open(hatarozat , 'r') as f:
        for line in f:
            
            line = line.replace("\\tab", " ")
            if 'dr' not in line.lower():
                continue
            if "\\'fcgyv\\'e9d" in line.lower() or "\\'dcgyv\\'e9d" in line.lower() or "tan\\'fa" in line.lower() or "szak\\'e9rt\\'f5" in line.lower():
                continue
            # print("===" + line)

            if "s.k." in line or "sk." in line or "s. k." in line or " sk" in line :
                for p in [prg, prg_katonai]:
                    talalatok = [ i[0] for i in p.findall(line)]
                    birok.extend([remove_sk(talalat) for talalat in talalatok if not ugyved_vagy_vadlott(talalat) and not monogram(talalat)])
            else:
                for p in [prg_2, prg_katonai_2]:
                    talalatok = [ i[0] for i in p.findall(line)]
                    birok.extend([talalat for talalat in talalatok if not ugyved_vagy_vadlott(talalat) and not monogram(talalat)])

    return list(set([clean_up(nev) for nev in birok]))

if __name__ == "__main__":
    hatarozat = sys.argv[1]
    print(biro_in_hatarozat(hatarozat))
