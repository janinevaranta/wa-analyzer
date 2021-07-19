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
from command_functions import *

COMMANDS = {
    "help": help,
    "exit": ex,
    "frame": frame,
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

DATEFORMATS = {
    "0": "%d/%m/%Y",
    "1": "%m/%d/%Y",
    "2": "%Y/%m/%d",
    "3": "%d.%m.%Y",
    "4": "%m.%d.%Y",
    "5": "%Y.%m.%d"
}

TIMEFORMATS = {
    "0": "%H:%M",
    "1": "%H.%M",
    "2": "%H:%M:%S",
    "3": "%H.%M.%S",
    "4": "%I:%M %p",
    "5": "%I:%M:%S %p"
}


print("""WA-Analyzer v0.2 - Get insight about your WhatsApp conversations!
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


while True:
    # Ask the user importing related questions.
    print("Please enter the corresponding number for the operating system on your device:")
    print("0 = Android")
    print("1 = iOS")
    device = input(">")
    if device != "0" and device != "1":
        print("Invalid device! Please enter '0' or '1'.")
    else:
        print("Please enter the corresponding number for the date format on your phone:")
        print("0 = dd/mm/yyyy")
        print("1 = mm/dd/yyyy")
        print("2 = yyyy/mm/dd")
        print("3 = dd.mm.yyyy")
        print("4 = mm.dd.yyyy")
        print("5 = yyyy.mm.dd")
        date_format = input(">")
        if date_format not in DATEFORMATS:
            print("Invalid device! Please enter '0', '1', '2', '3', '4', or '5'.")
            continue
        else:
            print(
                "Please enter the corresponding number for the time format on your phone:")
            print("0 = 00:00")
            print("1 = 00.00")
            print("2 = 00:00:00")
            print("3 = 00.00.00")
            print("4 = 00:00 am")
            print("5 = 00:00:00 am")
            time_format = input(">")
            if time_format not in TIMEFORMATS:
                print("Invalid device! Please enter '0', '1', '2', '3', '4', or '5'.")
                continue
            else:
                break


def parse_file(text_file, device, date_format, time_format):
    '''Convert WhatsApp chat log text file to a Pandas dataframe.'''

    time_format = TIMEFORMATS[time_format]
    date_format = DATEFORMATS[date_format]

    if device == "0":  # Android
        text_regex = r'^(\d{1,2}\/\d{1,2}\/\d\d\d\d.*?)(?=^^\d{1,2}\/\d{1,2}\/\d\d\d\d|\Z)'
        search_string = ' - (.*?):'
        datetime_format = date_format+", "+time_format
        row_splitter = " - "
    else:  # iOS
        text_regex = r'^(\[\d{1,2}\.\d{1,2}\.\d\d\d\d.*?)(?=^^\[\d{1,2}\.\d{1,2}\.\d\d\d\d|\Z)'
        search_string = '] (.*?):'
        # To account for the [] format in iOS devices.
        date_format = "[" + date_format
        datetime_format = date_format+" "+time_format
        row_splitter = "] "

    # some regex to account for messages taking up multiple lines
    pat = re.compile(text_regex, re.S | re.M)
    with open(text_file, encoding="utf-8") as f:
        data = [m.group(1).strip().replace('\n', ' ')
                for m in pat.finditer(f.read())]
        print(data)

    sender = []
    message = []
    datetime = []
    for row in data:

        # timestamp is before the first dash
        datetime.append(row.split(row_splitter)[0])

        # sender is between a dash and colon
        try:
            s = re.search(search_string, row).group(1)
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
    df['timestamp'] = pd.to_datetime(
        df.timestamp, format=datetime_format)

    # remove events not associated with a sender
    df = df[df.sender != ''].reset_index(drop=True)

    return df


# Parse the file
print("Parsing the file...")
chat_df = parse_file(path, device, date_format, time_format)


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
