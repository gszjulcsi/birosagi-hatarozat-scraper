from biro_nev_parser import biro_in_hatarozat 
import pandas as pd
import os.path


df = pd.read_csv("./results/2004_2018.csv", index_col=1)

def generate_filelocation(hatarozat): 
    filename = hatarozat["haratozat_url"].split("/")[-2] + ".rtf"
    birosagkod = hatarozat["haratozat_url"].split("/")[-4]
    folder = str(hatarozat['ev']) + "/" + birosagkod
    return 'hatarozatok/{}/{}'.format(folder, filename)

df['file_location'] = df.apply(generate_filelocation, axis=1)
df['hatarozat_letoltve'] = df['file_location'].map(os.path.isfile) 
df['birok'] = df['file_location'].map(biro_in_hatarozat)
df['birok_szama'] = df['birok'].map(lambda arr: len(arr) if arr else 0)
print(df['birok_szama'].value_counts())
df.to_csv("./results/v5_2004_2018_with_file_location_and_birok.csv", sep="\t")
df[df.hatarozat_letoltve == False].to_csv("./results/v5_hatarozat_hianyzik.csv", sep="\t")
df[df.birok_szama == 0].to_csv("./results/v5_biro_hianyzik.csv")