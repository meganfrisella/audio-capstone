import dict_data as data
import pickle
from collections import Counter as c

# STILL MUST IMPORT DATA FROM DATABASE #

song_IDs = data.import_dictionaries('int_to_title')


def match(fingerprints, base):
    """
    Compares the recorded fingerprints to fingerprints from songs stored in the database to identify the song.

    :param fingerprints: a list of tuples that store the fingerprints from the recorded audio file
    :return: a string indicating the matched song in the form '(song title) by (artist)'
    """
    matches = []

    database = base
    #print(list(database.keys())[0], database[list(database.keys())[0]])

    for fp in fingerprints:
        if fp[:3] in database:
            for idx, val in enumerate(database[fp[0:3]]):
                matches.append((val[0], fp[3]-val[1]))
    print(matches)
    print(c(matches))
