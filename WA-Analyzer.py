#!/usr/bin/env python
# coding: utf-8
# WA-Analyzer.py - Get insight about your WhatsApp conversations!
# v0.1
# Made by Jani Nevaranta, 2021/07

# # WhatsApp Data Analysis Template

# #### 1. Initialize the required modules

import os
import sys
import regex as re
import pandas as pd
import matplotlib
from datafunc import *

COMMANDS = {
    "help": help,
    "exit": ex,
    "sample": samp,
    "top": top,
    "bottom": bot,
    "messages-per-sender-bar": messages_per_sender_bar,
    "messages-per-sender-plot": messages_per_sender_plot,
    "total-daily-messages-plot": total_daily_messages_plot,
    "find-words": find_words,
    "find-date": find_date,
    "find-occurances": word_occurances,
    "leet": leet,
    "font-size": font_size
}


print("""WA-Analyzer v0.1 - Get insight about your WhatsApp conversations!
Made by Jani Nevaranta, 2021/07

""")

# #### 2. Parse the original file

# Give the absolute filepath as a string
while True:
    print("Give the absolute filepath to WhatsApp Chat .txt -file.")
    path = input("The path: ")

    if os.path.isfile(path):
        break
    elif path == "exit":
        sys.exit()
    else:
        print("Invalid path! Please check the filepath (the filepath must include the .txt -ending on the file).")


def parse_file(text_file):
    '''Convert WhatsApp chat log text file to a Pandas dataframe.'''

    # some regex to account for messages taking up multiple lines
    pat = re.compile(
        r'^(\d\d\/\d\d\/\d\d\d\d.*?)(?=^^\d\d\/\d\d\/\d\d\d\d|\Z)', re.S | re.M)
    with open(text_file, encoding="utf-8") as f:
        data = [m.group(1).strip().replace('\n', ' ')
                for m in pat.finditer(f.read())]

    sender = []
    message = []
    datetime = []
    for row in data:

        # timestamp is before the first dash
        datetime.append(row.split(' - ')[0])

        # sender is between a dash and colon
        try:
            s = re.search(' - (.*?):', row).group(1)
            sender.append(s)
        except:
            sender.append('')

        # message content is after the first colon
        try:
            message.append(row.split(': ', 1)[1])
        except:
            message.append('')

    df = pd.DataFrame(zip(datetime, sender, message), columns=[
                      'timestamp', 'sender', 'message'])
    df['timestamp'] = pd.to_datetime(df.timestamp, format='%d/%m/%Y, %H:%M')

    # remove events not associated with a sender
    df = df[df.sender != ''].reset_index(drop=True)

    return df


# Parse the file
print("Parsing the file...")
try:
    chat_df = parse_file(path)
except:
    print("Something went wrong!")


# Test the dataframe here. If the data presented here seems logical, the parsing was succesful.
print("Testing the dataframe...")
chat_df

# Convert date and time column values into strings
print("Converting datetime values into additional columns...")
chat_df["date"] = chat_df["timestamp"].dt.date
chat_df["time"] = chat_df["timestamp"].dt.time
chat_df["date"] = chat_df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
chat_df["time"] = chat_df["time"].apply(lambda x: x.strftime("%H:%M"))

chat_df["year"] = chat_df["timestamp"].dt.year
chat_df["month"] = chat_df["timestamp"].dt.month
chat_df["day"] = chat_df["timestamp"].dt.day

chat_df["hour"] = chat_df["timestamp"].dt.hour


# Add message related columns
print("Converting word related values into additional columns...")
chat_df["word_count"] = [len(x.split()) for x in chat_df["message"].to_list()]
chat_df["char_count"] = chat_df.message.apply(len)

# Ready
print("Dataframe initialized successfully!")
print(chat_df)

# Main loop
while True:
    print("Input command (enter 'help' for the command list):")
    command = input(">")
    command_key = COMMANDS.get(command)

    if command_key != None:
        command_key(chat_df)
