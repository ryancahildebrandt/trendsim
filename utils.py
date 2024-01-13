#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 02:05:33 PM EST 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import numpy as np
import requests
import logging
import sys

logging.basicConfig(stream = sys.stdout, level = logging.INFO)

def softmax(arr):
	arr = arr - max(arr)
	e = np.exp(arr)
	out = e / np.sum(e, axis = 0)
	return out

def generate_markov_chain(tokens):
	out = {i : {} for i in set(tokens)}
	for i in range(len(tokens) - 1):
		t1 = tokens[i]
		t2 = tokens[i + 1]
		if t2 not in out[t1].keys():
			out[t1] = {t2 : 1}
		else:
			out[t1][t2] += 1
	for i in out:
		out[i][""] = 1
	out[""] = {i : 1 for i in set(tokens)}
	return out

def generate_text(markov_chain, seed_word, n_tokens):
	current_word = seed_word
	text = [current_word]
	for i in range(n_tokens - 1):
		vocab = list(markov_chain[current_word].keys())
		transitions = list(markov_chain[current_word].values())
		next_word = np.random.choice(
			a = np.array(vocab),
			p = softmax(np.array(transitions)),
			)
		text.append(next_word)
		current_word = next_word
	out = [i for i in text if i != ""]
	return out

def get_location():
	r = requests.get(
	url = "https://api.3geonames.org/?randomland=JP&json=1",
	headers = {"Accept" : "application/json"}
	)
	try:
		major = r.json()["major"]
	except:
		major = {"city" : "Kyoto", "latt" : "35.0116", "longt" : "135.7681"}
	coords = [np.float64(major["latt"]), np.float64(major["longt"])]
	name = major["city"]
	out = [coords, name]
	return out

