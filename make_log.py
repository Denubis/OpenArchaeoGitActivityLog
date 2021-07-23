#!/usr/bin/env python3

import requests
from frictionless import extract
from pydriller import Repository
from pprint import pprint
import os
import shutil
import datetime
import glob
import csv
import json
import tqdm

OPEN_ARCHAEO_LIST="https://raw.githubusercontent.com/zackbatist/open-archaeo/master/open-archaeo.csv"
BASE_OUTDIR="output"
OUTDIR = f"{BASE_OUTDIR}-{datetime.datetime.now().isoformat()}/"

open_archaeo_items = extract(OPEN_ARCHAEO_LIST)
for dir_name in glob.glob(f"{BASE_OUTDIR}*"):
  print(dir_name)
  shutil.rmtree(dir_name, ignore_errors=True)
os.mkdir(OUTDIR)


open_archaeo_commits = {}

for item in tqdm.tqdm(open_archaeo_items):
  item_id = item['item_name']
  open_archaeo_commits[item_id] = dict(item)
  #pprint(item)
  if repourl := (item.get("github") or item.get("gitlab") or item.get("bitbucket")):
    filename = f"{OUTDIR}name#{item.get('item_name')}+category#{item.get('category')}+tag1#{item.get('tag1')}+tag2#{item.get('tag2')}+tag3#{item.get('tag3')}+tag4#{item.get('tag4')}+tag5#{item.get('tag5')}.csv".replace(" ","_")
    #print(filename)
    #print(repourl)
    open_archaeo_commits[item_id]['commit_history'] = []
    with open(filename, "w") as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(["item_name", "category", "tag1", "tag2", "tag3", "tag4", "tag5", "author_date", "committer_date", "msg", "commmitter", "author"])
      for commit in Repository('https://github.com/ishepard/pydriller').traverse_commits():
        csvwriter.writerow([item.get('item_name'), item.get('category'), item.get('tag1'), item.get('tag2'),item.get('tag3'),item.get('tag4'),item.get('tag5'), commit.author_date.isoformat(), commit.committer_date.isoformat(), commit.msg, commit.committer.name, commit.author.name])
        open_archaeo_commits[item_id]['commit_history'].append({'committer_date':commit.committer_date.isoformat(),
                                                          'author_date':commit.author_date.isoformat(),
                                                           'message':commit.msg,
                                                           'author':commit.author.name,
                                                           'committer':commit.committer.name})

  #break
with open(f"{OUTDIR}/data.json","w") as jsonfile:
  json.dump(open_archaeo_commits, jsonfile)