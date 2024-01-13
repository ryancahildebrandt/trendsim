#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 02:05:04 PM EST 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import itertools
import threading
import numpy as np
import time
import os
import pickle
from datetime import datetime

from utils import *

# author class
class Author:
	def __init__(self, author_id, author_name, other_authors, corpus):
		self.id = author_id
		self.name = author_name
		self.mentions = other_authors
		self.corpus = corpus
		self.rng = np.random.default_rng()
		self.transitions_file = f"data/transitions/{self.id}.pickle"
		self.location_coords, self.location_name = get_location()
		self.post_length = self.rng.integers(5, 100)
	
	def _process_corpus(self, tokenizer):
		self.texts = "".join(itertools.chain.from_iterable(self.corpus))
		self.tokens = [i.surface for i in tokenizer.tokenize(self.texts)]
		self.tokens = [i.split(" ") for i in self.tokens]
		self.tokens = list(itertools.chain.from_iterable(self.tokens))
		self.transitions = generate_markov_chain(self.tokens)
		print("Transitions calculated")

	def _write_transitions_to_file(self):
		with open(self.transitions_file, 'wb') as f:
			pickle.dump(self.transitions, f)
		print(f"Transitions written to {self.transitions_file}")

	def _load_transitions_from_file(self):
		with open(self.transitions_file, 'rb') as f:
			self.transitions = pickle.load(f)
		print(f"Transitions loaded from {self.transitions_file}")
	
	def populate_corpus(self, tokenizer):
		print(f"{self.name}, ID {self.id}")
		if os.path.isfile(self.transitions_file):
			self._load_transitions_from_file()
		else:
			self._process_corpus(tokenizer)
			self._write_transitions_to_file()
	
	def _write_post(self):
		transitions = self.transitions
		seed = np.random.choice(list(self.transitions.keys()))
		length = self.post_length + self.rng.integers(0, 10)
		out = generate_text(transitions, seed, length)
		return out

	def _pick_mentions(self):
		mentions = self.mentions
		length = self.rng.integers(0, 5)
		out = np.random.choice(mentions, length).tolist()
		return out
	
	def _pick_location(self):
		base = self.location_coords
		noise = self.rng.normal(0, .1, 2)
		out = (base + noise).astype(float).tolist()
		return out

	def post(self):
		time = datetime.now()
		tokens = self._write_post()
		text = "".join(tokens)
		mentions = self._pick_mentions()
		location = self._pick_location()
		out = {
			"name" : self.name,
			"time" : time,
			"location" : location,
			"city" : self.location_name,
			"mentions" : mentions,
			"tokens" : tokens,
			"text" : text
		}
		return out

	def timed_post(self, n_posts, sink_func = None):
		for t in self.rng.exponential(size = n_posts):
			time.sleep(t)
			p = self.post()
			if sink_func == None:
				return p
			else:
				sink_func(p)

	def create_thread(self, n_posts, sink_func):
		self.thread = threading.Thread(target = self.timed_post, args = [n_posts, sink_func])

	def start_thread(self):
		self.thread.start()
