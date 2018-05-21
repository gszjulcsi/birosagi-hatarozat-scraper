import pandas as pd

df = pd.read_csv("results/v5_2004_2018_with_file_location_and_birok.csv", index_col=1, sep = "\t")
biro_dict = {}

# print(df['birok'].head())
for birok in df['birok'].values:
	try:
		for biro in birok.replace('[', '').replace(']', '').split(","):
			if biro not in biro_dict:
				biro_dict[biro] = 0
			biro_dict[biro] += 1
	except:
		pass


for biro, fqt in biro_dict.items():
	print(biro + "\t" + str(fqt))