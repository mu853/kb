import re
import sys
import csv
import json
import urllib.parse
import requests

def get_article_id_from_legacy_id(legacy_id):
    try:
        #89137
        response = requests.get("https://knowledge.broadcom.com/external/article?legacyId={}".format(legacy_id))
        mark = "Article ID: "
        start = response.text.index(mark)
        start += len(mark)
        article_id = response.text[start:start+6]
        return article_id
    except:
        print("legacy_id = {} cannot found".format(legacy_id))

if len(sys.argv) != 3:
    print("usage: {0} <ID list file> <output file path>".format(sys.argv[0]))
    exit(0)
id_list_file = sys.argv[1]
output_file = sys.argv[2]

id_list = []

count = 0
with open(id_list_file, 'r', encoding='utf8') as f:
    for line in f:
        legacy_id = line.rstrip()
        article_id = legacy_id
        if len(legacy_id) == 5:
            article_id = get_article_id_from_legacy_id(legacy_id)
        id_list.append({"legacy_id": legacy_id, "article_id": article_id})
        if count > 5:
            break

with open(output_file, 'w', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(["Article ID", "Legacy ID"])
    for i in id_list:
        writer.writerow([i["article_id"], i["legacy_id"]])
