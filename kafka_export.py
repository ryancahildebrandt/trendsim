#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 06:22:14 PM EST 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import pickle
import numpy as np
import json
from kafka import KafkaProducer

from author_class import *
from utils import *

def kafka_sink(post):
	post["time"] = post["time"].isoformat()
	con = KafkaProducer(bootstrap_servers = ["localhost:9092"])
	con.send("trendsim", json.dumps(post).encode("utf-8"))

with open("data/all_authors.pickle", "rb") as f:
	author_dict = pickle.load(f)
print("authors loaded from disk")

sample = np.random.choice(list(author_dict.keys()), replace = False, size = 100)
author_dict_sample = {id: author_dict[id]["author_obj"] for id in sample}

for a in author_dict_sample.values():
	a.create_thread(20, kafka_sink)
	a.start_thread()
