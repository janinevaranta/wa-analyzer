import sys
import time
import regex as re
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

plt.style.use('seaborn-whitegrid')
matplotlib.rcParams.update({'font.size': 14})


def help(*arg):
    print("""

    "exit": Exit the program.
    "sample": Give a randomly generated sample from the data. Can be used to validate the data.
    "messages-per-sender-bar": Create a bar graph listing the amount of messages sent by each participant.
    "messages-per-sender-plot": Create a plot graph detailing the amount of messages sent by each participant.
    "total-daily-messages-plot": Show how many messages were sent on each day.
    "find-words": Find specific words and the amount of times each were said.
    "find-date": Find a specific date on the dataset.
    "find-occurances": Find how many the given words occur in unique messages.
    "leet": Leet.
    "font-size": Change the font size.

    """)


def frame(chat_df):
    print(chat_df)


def ex(*arg):
    print("Closing the app...")
    sys.exit()


def font_size(*arg):
    print("The new font size: ")
    try:
        f_size = input(">")
        matplotlib.rcParams.update({'font.size': f_size})
        print("Font size updated!")
    except:
        print(
            "The font size must be a viable integer that is larger than 0.")


def top(chat_df):
    ...


def bot(chat_df):
    ...


def samp(chat_df):
    print(chat_df.sample(20))


def messages_per_sender_bar(chat_df):
    message_count = chat_df.groupby(
        "sender")["message"].count().sort_values(ascending=False)
    plt.figure(figsize=(14, 8))
    plt.title("Messages by the sender.")
    plt.bar(message_count.index, message_count.values)
    print("Displaying the graph...")
    plt.show()


def messages_per_sender_plot(chat_df):
    per_sender = chat_df.groupby([chat_df.date, chat_df.sender])[
        "message"].count()
    per_sender = per_sender.unstack(["sender"]).fillna(0).stack(["sender"])
    max_ticks = len(per_sender.index)
    plt.figure(figsize=(14, 8))
    plt.xticks(np.arange(0, max_ticks, step=50))

    # Loop through all the senders and create plots for each.
    for sender in chat_df["sender"].unique():
        plt.plot(per_sender.xs(sender, level=1), label=sender, alpha=0.5)

    plt.xlabel("Date")
    plt.ylabel("Messages")
    plt.legend()
    plt.show()


def total_daily_messages_plot(chat_df):
    plt.figure(figsize=(14, 8))

    date = chat_df.groupby("date")["message"].count()

    idx_range = pd.date_range(
        date.head(1).index.item(), date.tail(1).index.item())

    date.index = pd.DatetimeIndex(date.index)
    date = date.reindex(idx_range, fill_value=0)

    print(date)

    plt.plot(date.index, date.values, linewidth=1)
    plt.title("Daily messages")
    plt.xlabel("Date")
    plt.ylabel("Messages")
    plt.show()

# Helper function


def search_words(dataset, lst):
    found_dic = {}
    for arg in range(len(lst)):
        try:
            found_dic[lst[arg]] = dataset.at[lst[arg]]
        except KeyError:
            pass
    return found_dic


def find_words(chat_df):
    print("Give a list of words you want to search, seperated by ',' (without space).")
    print("Empty list will search for the top 30 most used words.")
    word_list_in = input(">")
    word_list = word_list_in.split(",")
    chat_df_lower = chat_df.message.str.lower()
    words = chat_df_lower.str.split(expand=True).stack().value_counts()
    if word_list_in != "":
        found_words = search_words(words, word_list)
        found_words_df = pd.DataFrame.from_dict(
            found_words, orient="index", columns=["frequency"])
        found_words_df = found_words_df.sort_values(
            by="frequency", ascending=False)
    else:
        top_words = words.head(30)
        found_words_df = top_words

    print("Printing the words found...")
    time.sleep(1)
    print(found_words_df)
    print("")
    print("Create a bar graph from the output? y/n")
    answer = input(">")
    if answer.lower() == "y":
        plt.figure(figsize=(14, 8))

        plt.bar(found_words_df.index, found_words_df.frequency)
        plt.title("Top Messages")
        plt.show()
    else:
        pass


def leet(chat_df):
    result_time = chat_df.loc[chat_df["time"] == "13:37"]
    result_leet = result_time.loc[result_time["message"] == "leet"]
    print(result_leet)
    if result_leet.empty == True:
        pass
    else:
        leet_count = result_leet.groupby("sender")["message"].count(
        ).sort_values(ascending=False)
        plt.figure(figsize=(14, 8))
        plt.title("The amount of times 'leet' has been said at 13:37.")
        plt.bar(leet_count.index, leet_count.values)
        print("Displaying the graph...")
        plt.show()


def word_occurances(chat_df):
    print("Give a regex object to search words for.")
    word = input(">")
    match_index = chat_df["message"].str.extractall(word).droplevel(1)
    n = chat_df.loc[match_index.index].groupby("sender")[["message"]].count(
    ).sort_values(by="message", ascending=False).head(10)
    n_df = chat_df.loc[match_index.index][["sender", "message", "date"]]

    print(n_df)

    print("")
    print("Create a bar graph from the output? y/n")
    answer = input(">")
    if answer.lower() == "y":
        plt.figure(figsize=(14, 8))
        plt.bar(n.index, n.message)

        tit = re.sub(r"[^\w]", " ", word)

        plt.title("The amount of messages featuring the word(s) '"+tit+"'")
        plt.show()
    else:
        pass


def find_date(chat_df):
    print("Give the date in the following format: yyyy-mm-dd.")
    date = input(">")
    result_date = chat_df.loc[chat_df["date"] == date]
    print(result_date)
