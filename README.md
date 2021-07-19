# WA-Analyzer.py
WhatsApp message analyzer with pandas and matplotlib.

## What is this project about?
WA-Analyzer.py is a personal project of mine that started as a easily managable tool for my friends who were interested in seeing analytics of their own WhatsApp conversations.

## Features:
* Convert WhatsApp conversations into pandas dataframe objects for further analysis.
* Display series and graphs through commands.
* Search frequency and occurances of words in the conversations.
* See who has sent 'leet' at 13:37 the most.
* Works with many different datetime formats.

## How does it work?
The tool accesses the exported .txt file that the user has exported from their WhatsApp conversation. After a few questions to setup the datetime formating used in the .txt file the tool converts the .txt into a pandas dataframe. From there on the user can prompt commands to display statistics in a form of pandas series or matplotlib graph.

