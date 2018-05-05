from process_birosagok_response import find_nth
import sys
import json



def url_to_id(url):
	id_with_underscores = url.split("/")[-2]
	return id_with_underscores.replace("_", "/")


def create_hatarozat(h_id, year, birosag, jog, doc_url):
	return {"azonosito": h_id,
			"ev": year,
			"birosag": birosag,
			"jogterulet": jog,
			"haratozat_url": doc_url}


MAX_LENGTH = 2000 

response_file = sys.argv[1]
result_file = sys.argv[2]
more_query_needed_file = sys.argv[3]

hatarozatok = []
responses_with_max_lengths = {}
with open(response_file, 'r') as f:

	for line in f:
		# print(line)
		if line.startswith('|'):
			#Example line: |2016|Kúria|b\xfcntet\u0151jog|
			parts = line.split('|')

			year = parts[1]
			birosag = parts[2]
			jog = parts[3]
		elif line.startswith('//OK'):
			start_pos = find_nth(line, '[', 2) +1
			end_pos = find_nth(line, ']', 1)
			arr = line[start_pos:end_pos].split('","')
			urls = ["http://ukp.birosag.hu/portal-frontend/" + i for i in arr if i.startswith("stream/birosagKod/")]
			ids = [url_to_id(url) for url in urls ] 

			for (id_, url) in zip(ids, urls):
				hatarozatok.append(create_hatarozat(id_, year, birosag, jog, url))
			if len(ids) == MAX_LENGTH:
				responses_with_max_lengths.append({"ev": year, "birosag": birosag, "jogterulet": jog})
with open(result_file, "w") as hatarozatok_file:
	hatarozatok_file.write(json.dumps(hatarozatok) + "\n")

with open(more_query_needed_file, "w") as followup_file:
	followup_file.write(json.dumps(responses_with_max_lengths) + "\n")
			# sys.exit(1)
