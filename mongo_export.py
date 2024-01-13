#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 06:22:53 PM EST 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import pickle
from pymongo import MongoClient
import numpy as np

from author_class import *
from utils import *

def mongo_sink(post):
	con = MongoClient("mongodb://localhost:27017")["trendsim"]["trendsim"]
	con.insert_one(post)

with open("data/all_authors.pickle", "rb") as f:
	author_dict = pickle.load(f)
print("authors loaded from disk")

sample = np.random.choice(list(author_dict.keys()), replace = False, size = 100)
author_dict_sample = {id: author_dict[id]["author_obj"] for id in sample}

for a in author_dict_sample.values():
	a.create_thread(20, mongo_sink)
	a.start_thread()
