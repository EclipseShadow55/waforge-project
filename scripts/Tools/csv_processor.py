# Description: Processes csv files and returns the most similar rows to the input string.
import csv
from fuzzywuzzy import fuzz


def custom_ratio(str1: str, str2: str):
    """
    Custom ratio function that gives more weight to words that are in both strings.

    :param str1: The first string to compare.
        :type str1: str
    :param str2: The second string to compare.
        :type str2: str

    :return: The similarity ratio.
        :rtype: float
    """
    num_similar = [item in str1 for item in str2.split()].count(True)
    return (fuzz.token_set_ratio(str1, str2) + 92 * num_similar) / (1 + num_similar)


def smart_get(file_path, index_look_at, item_look_for):
    """
    Get the most similar rows to the input string from a csv file.

    :param file_path: The path to the csv file.
        :type file_path: str
    :param index_look_at: The index of the column to look at.
        :type index_look_at: int
    :param item_look_for: The string to look for.
        :type item_look_for: str

    :return: The most similar rows.
        :rtype: list
    """
    rets = []
    with open(file_path, 'r', encoding="utf-8", errors="replace") as file:
        reader = csv.reader(file)
        for row in reader:
            if (custom_ratio(row[index_look_at], item_look_for)) > 90:
                rets.append(row)

    rets.sort(key=lambda x: custom_ratio(x, item_look_for), reverse=True)
    return rets