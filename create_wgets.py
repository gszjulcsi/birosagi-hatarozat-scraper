import json
import os
import sys

year = sys.argv[1]

input_file = 'structured_data/{}.json'.format(year)
output_file = 'wget_files_{}.sh'.format(year)

with open(input_file, 'r') as f:
    hatarozatok = json.load(f)


with open(output_file, 'w') as wf:
    for hatarozat in hatarozatok:
        filename = hatarozat["haratozat_url"].split("/")[-2] + ".rtf"
        birosagkod = hatarozat["haratozat_url"].split("/")[-4]
        folder = hatarozat['ev'] + "/" + birosagkod

        target = '{}/{}'.format(folder, filename)

        wf.write("mkdir -p {}\n".format(folder))
        wf.write("wget {} -O {}\n".format(hatarozat["haratozat_url"].strip('"'), target))
        wf.write("sleep 2\n")
