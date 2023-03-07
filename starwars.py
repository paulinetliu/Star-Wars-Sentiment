"""
Pauline Liu
November 18, 2022
Sentiment Analysis of Star Wars

Reads the script of the Star Wars original movie into a list of dictionaries. Calculates sentiment score for each line
of dialogue based on number of positive and negative words in the line. Reports the most positive and most negative
line in the script. Reports minimum, average, and maximum sentiment score for main characters. Creates a histogram
of the sentiment scores for Luke and Leia. Visualizes the story arc of the movie using a moving average of sentiment
scores. Graphs the number of positive and negative lines spoken by main characters.
"""

import matplotlib.pyplot as plt
STARWARS = "starwars.txt"
POSWORDS = "positive-words.txt"
NEGWORDS = "negative-words.txt"
PUNC = ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";","<", "=", ">", "?", "@",
        "[", "]", "^", "_", "`", "{", "}", "|", "~"]

def read_data_dict(filename, type_cast_dict = {}):
    """
    reads data into a list of dictionaries; each dictionary contains the data from one line; the column headers are
    the keys and the values are the values for the corresponding row
    :param filename: str
        name of the dataset; columns are separated by "|"
    :param type_cast_dict: dict
        optional, dictionary where the keys are the column headers and the values are the desired cast for each column
    :return: data
        list of dictionaries
        for each dictionary, the column headers are the keys and the values are the values for the corresponding row
    """
    file = open(filename, "r")
    data = []

    # each item in the header become the keys for each dictionary
    keys = file.readline().strip().split("|")

    for line in file:
        # create a dictionary for each line
        row_dict = {}
        pieces = line.strip().split("|")

        # link the value to the appropriate header
        for i in range(len(pieces)):
            # convert to proper cast if specified
            if keys[i] in type_cast_dict:
                cast_func = type_cast_dict[keys[i]]
                row_dict[keys[i]] = cast_func(pieces[i])
            # assign key-value pairs
            else:
                row_dict[keys[i]] = pieces[i]
        # append dictionary for each line
        data.append(row_dict)

    file.close()
    return data

def read_data_singlelist(filename):
    """
    Reads the data in a given file and stores the values in a list of strings.
    :param filename: str; name of the file
    :return: ls; list
        list of strings for all lines in the file
    """
    file = open(filename, "r")
    ls = []

    for line in file:
        ls.append(line.strip())

    file.close()
    return ls

def sentiment_score(dataset, punc_ls, positivewords, negativewords):
    """
    calculates a sentiment score for each row of a list of dictionaries by adding the number of positive words and
    subtracting the number of negative words in each line of dialogue. cleans each line before calculating sentiment
    score. updates each dictionary with the sentiment score.
    :param dataset: list
        list of dictionaries; each dictionary contains the keys "line_number", "character", and "dialogue".
    :param punc_ls: list
        list of strings of punctuation to be cleaned out of each piece of dialogue before sentiment analysis
    :param positivewords: list
        list of words that are considered positive; each positive word in a line of dialogue adds to the sentiment score
    :param negativewords: list
        list of words that are considered negative; each negative word in a line of dialogue subtracts from the
        sentiment score
    :return:
        None
    """
    for dict in dataset:
        # extract dialogue as a string, make lowercase
        dialogue = dict["dialogue"].lower()
        # clean dialogue
        for punc in punc_ls:
            dialogue = dialogue.replace(punc, "")
        # split dialogue into a list of words
        dialogue = dialogue.strip().split()

        # calculate sentiment score
        score = 0
        for word in dialogue:
            if word in positivewords:
                score += 1
            elif word in negativewords:
                score -= 1

        # update dictionary with sentiment score
        dict["sentiment"] = score

def most_pos_neg_line(dataset, posneg):
    """
    reports the most positive or most negative line of dialogue along with its corresponding sentiment score and the
    character who speaks the line. in the case of ties, reports any one of the lines.
    :param dataset: list
        list of dictionaries; each dict contains the keys "line_number", "character", "dialogue", and "sentiment".
        "sentiment" is sentiment score calculated by adding the number of positive words and subtracting the number
        of negative words in the dialogue.
    : param posneg: boolean
        whether to report the most positive or most negative line. if true, reports the most positive line.
    :return:
        None
    """
    # set score to 0 so we can compare
    score = 0

    if posneg == True:
    # find most positive sentiment score
        for dict in dataset:
            if dict["sentiment"] > score:
                score = dict["sentiment"]
                mostposneg = dict
        print("Most positive line:")

    if posneg == False:
    # find most negative sentiment score
        for dict in dataset:
            if dict["sentiment"] < score:
                score = dict["sentiment"]
                mostposneg = dict
        print("Most negative line:")

    # report most positive or most negative line
    print("character:", mostposneg["character"])
    print("dialogue:", mostposneg["dialogue"])
    print("score:", mostposneg["sentiment"])
    print()

def character_sentiment_scores(dataset):
    """
    creates a dictionary mapping character names to a list of sentiment scores for every line of dialogue spoken by
    that character.
    :param dataset: str
        list of dictionaries; each dict contains the keys "line_number", "character", "dialogue", and "sentiment".
    :return: scores_dict: dict
        dictionary; keys are character names and values are lists of sentiment scores
    """
    # make a dictionary to add characters and scores to
    scores_dict = {}
    for dict in dataset:
        if dict["character"] not in scores_dict:
            # add characters to dictionary
            # create list to add scores to
            scores_dict[dict["character"]] = []

    for character in scores_dict:
        # append all sentiment scores for each character
        for dict in dataset:
            if dict["character"] == character:
                scores_dict[character].append(dict["sentiment"])

    return scores_dict

def sentiment_stats(character_scores_dict, character):
    """
    finds the minimum, maximum, and average sentiment scores of lines spoken by a specific character.
    :param character_scores_dict: dict
        dictionary that maps character names to a list of sentiment scores for that character
    :param character: str
        name of the character to find the summary stats for
    :return: stats: dict
        dictionary of character name, minimum score, average score, and maximum score for the named character
        keys are "character", "min", "avg", and "max".
    """
    # extract list of sentiment scores from dictionary
    scores = character_scores_dict[character]

    # find summary stats of list of sentiment scores
    stats = {"character": character, "min": min(scores), "avg": round(avg(scores), 3), "max": max(scores)}
    return stats

def generate_table(characters, character_scores_dict):
    """
    generates a table that displays the min, avg, and max sentiment scores for lines spoken by the specified characters
    in a readable format
    :param characters: list
        list of character names as strings to display statistics for
    :param character_scores_dict: dict
        dictionary that maps character names to a list of sentiment scores for that character
    :return:
        None
    """
    # table title and headers
    print("Sentiment Scores for Main Characters")
    print(f'{"Character":15} {"Minimum Score":15} {"Average Score":15} {"Maximum Score":15}')

    # print character stats
    for character in characters:
        stats = sentiment_stats(character_scores_dict, character)
        print(f'{stats["character"]:12} {stats["min"]:10} {stats["avg"]:15} {stats["max"]:15}')

def compare_sentiment_scores(character_scores_dict, character1="LEIA", character2="LUKE"):
    """
    creates overlapping histograms of the sentiment scores for two characters.
    :param character_scores_dict: dict
        dictionary that maps character names to a list of sentiment scores for that character
    :param character1: str
        name of the first character to show the sentiment scores for; default to "LEIA"
    :param character2: str
        name of the second character to show the sentiment scores for; default to "LUKE"
    :return:
        None
    """
    # extract lists of sentiment scores for each character
    character1_scores = character_scores_dict[character1]
    character2_scores = character_scores_dict[character2]

    # plot sentiment scores
    plt.hist(character1_scores, color="red", label=character1, alpha=0.5, bins=10)
    plt.hist(character2_scores, color="blue", label=character2, alpha=0.5, bins=10)
    plt.legend()
    plt.xlim(-6, 6)
    plt.xlabel("Sentiment Score per Line")
    plt.ylabel("Frequency")
    plt.title("Comparison of Characters: Sentiment Scores")
    plt.show()

def avg(ls):
    """
     Compute the numerical average of a list of numbers. If list is empty, return 0.0
    :param ls: list
        list of numbers
    :return: avg
        average of the list. if the list is empty, avg = 0.0
    """
    if len(ls) > 0:
        avg = sum(ls) / len(ls)
    else:
        avg = 0.0
    return avg

def get_window(L, idx, window_size=1):
    """
    Extract a window of values of specified size centered on the specified index
    :param L: List of values
    :param idx: Center index
    :param window_size: window size, default to 1
    :return: window; ls
        subset of list of values centered on the specified index
    """
    minrange = max(idx - window_size // 2, 0)
    maxrange = idx + window_size // 2 + (window_size % 2)
    window = L[minrange:maxrange]
    return window

def moving_average(L, window_size=1):
    """
    Compute a moving average over the list L using the specified window size
    :param L: List of values
    :param window_size: The window size (default=1)
    :return: mavg; ls
        A new list with smoothed values
    """
    mavg = []
    for i in range(len(L)):
        window = get_window(L, i, window_size)
        mavg.append(avg(window))
    return mavg

def get_values(data, key):
    """
    given a list of dictionaries and a key, returns the values associated with that key in every dictionary in the list
    :param data: list
        list of dictionaries
    :param key: string
        key to return the values for
    :return: values
        list - list of all the values for the given key
    """
    values = []
    for dict in data:
        values.append(dict[key])
    return values

def visualize_story_arc(dataset):
    """
    Visualizes the story arc of a script using sentiment scores. Plots a moving average sentiment score using a window
    size of 20. Labels high and low points of story arc.
    :param dataset: list
        list of dictionaries; each dict contains the keys "line_number", "character", "dialogue", and "sentiment".
    :return:
        None
    """
    # make list of sentiment scores to plot moving average of
    scores = get_values(dataset, "sentiment")

    mavg = moving_average(scores, window_size=20)
    plt.plot(mavg, linestyle="-", color="purple")
    plt.title("Moving Average of Sentiment Score Throughout Star Wars")
    plt.ylabel("Sentiment Score")
    plt.xlabel("Line in Movie")
    plt.text(289, -0.75, "Tarkin's Conference")
    plt.text(835, 0.95, "Rebels Attack")
    plt.show()

def visualize_character_scores(character_scores_dict):
    """
    counts the number of positive and negative lines score by each character. ignores lines with a sentiment score of 0.
    each character is represented by a point where the x-value is the number of negative lines and the y-value is the
    number of positive lines spoken. only plots characters where negativelines+positivelines > 10.
    :param character_scores_dict: dict
        dictionary that maps character names to a list of sentiment scores for that character
    :return:
        None
    """
    plt.figure(figsize=(6,6), dpi=200)
    for character in character_scores_dict:
        negative_lines = 0
        positive_lines = 0
        for score in character_scores_dict[character]:
            if score > 0:
                positive_lines += 1
            if score < 0:
                negative_lines += 1

        # only plot characters where negative_lines + positive_lines > 10
        if negative_lines + positive_lines > 10:
            plt.plot(negative_lines, positive_lines, "o", label=character)

    plt.legend(loc="lower right")
    plt.xlim(0,70)
    plt.ylim(0,70)
    plt.xlabel("Number of Negative Lines")
    plt.ylabel("Number of Positive Lines")
    plt.title("Number of Positive and Negative Lines Spoken by Star Wars Characters")
    plt.grid(color="gray", linestyle="-")
    plt.show()

def main():
    # read the data
    types = {"line_number": int, "character": str, "dialogue": str}
    starwars_script = read_data_dict(STARWARS, types)

    # read in positive and negative words list
    poswords = read_data_singlelist(POSWORDS)
    negwords = read_data_singlelist(NEGWORDS)

    # compute sentiment scores for each line
    sentiment_score(starwars_script, PUNC, poswords, negwords)

    # find most negative and most positive line in the movie
    most_pos_neg_line(starwars_script, True)
    most_pos_neg_line(starwars_script, False)

    # create dictionary mapping character to a list of sentiment scores for each line spoken by that character
    character_scores_dict = character_sentiment_scores(starwars_script)

    # generate table displaying min, avg, and max sentiment scores for main characters
    generate_table(["DARTH VADER", "LEIA", "C3PO", "LUKE", "OBIWAN", "HAN SOLO"], character_scores_dict)

    # visualizations
    compare_sentiment_scores(character_scores_dict)
    visualize_story_arc(starwars_script)
    visualize_character_scores(character_scores_dict)

main()