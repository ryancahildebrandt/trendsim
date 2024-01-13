#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 04:42:51 PM EST 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import duckdb
import pickle
import threading
from konoha import WordTokenizer

from author_class import *
from utils import *

con = duckdb.connect("data/aozora_corpus.db")
wt = WordTokenizer("Janome")

authors = con.sql("SELECT 人物ID, 著者, 本文 FROM works JOIN texts USING (作品ID) JOIN authors USING (人物ID) where 本文 != ''").fetchall()
author_ids = set([i[0] for i in authors])
author_names = set([i[1] for i in authors])
author_dict = {i : {"corpus" : ""} for i in author_ids}

for id, name, text in authors:
	author_dict[id]["name"] = name
	author_dict[id]["mentions"] = list(author_names)
	author_dict[id]["mentions"].remove(name)
	author_dict[id]["corpus"] += text

for id, info in author_dict.items():
	a = Author(id, info["name"], info["mentions"], info["corpus"])
	a.populate_corpus(wt)
	author_dict[id]["author_obj"] = a

with open("data/all_authors.pickle", "wb") as f:
	pickle.dump(author_dict, f)

