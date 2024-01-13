#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 06:25:31 PM EST 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import pandas as pd
import numpy as np
import panel as pn
from pymongo import MongoClient
from kafka import KafkaConsumer, TopicPartition
from datetime import datetime

con = MongoClient("mongodb://localhost:27017")["trendsim"]["trendsim"]
cursor = con.find()
df =  pd.DataFrame(list(cursor)).astype(str)
df["count"] = 1
initial_df = df.head()
df_iterator = df[5:].itertuples()

# all data live updating
main_df = pn.pane.Perspective(
    initial_df,
    columns = ["name", "time", "location", "city", "mentions", "text"],
    sizing_mode = 'stretch_width',
    height = 500,
    theme = 'material-dark'
)

# "name" # of posts
name_df = pn.pane.Perspective(
    initial_df,
    columns = ["count"],
    group_by = ["name"],
    sort = [["count", "desc"]],
    sizing_mode = 'stretch_width',
    height = 500,
    theme = 'material-dark'
)

# "city" # of posts 
city_df = pn.pane.Perspective(
    initial_df,
    columns = ["count"], 
    group_by = ["city"],
    sort = [["count", "desc"]],
    sizing_mode = 'stretch_width',
    height = 500,
    theme = 'material-dark'
)

# "text" text length
length_df = pn.pane.Perspective(
    pd.DataFrame.from_dict({"text" : [0]}),
    columns = ["text"], 
    plugin = "d3_y_line",
    sizing_mode = "stretch_width",
    height = 500,
    theme = 'material-dark'
)

def update():
    upd = next(df_iterator)._asdict()
    main_df.stream(upd)
    name_df.stream(upd)
    city_df.stream(upd)
    length_df.stream({"text" : len(upd["text"])}, rollover = 500)

pn.state.add_periodic_callback(update, 100)
pn.Column(
    "# All Data",
    pn.panel(main_df),
    pn.Row(
        pn.Column("# Author Leaderboard", pn.panel(name_df)),
        pn.Column("# City Leaderbord", pn.panel(city_df))
        ),
    "# Text Length",
    pn.panel(length_df)
    ).servable()
