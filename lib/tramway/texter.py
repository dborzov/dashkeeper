"""
MIT lisense, written by Dima Borzov

The project source code is available at:
gihub.com/dborzov/tramway
------------------------------
texter.py:
Some general text processing functions.
"""

# Transforms an array of words into the set ordered in the occurance frequency
def CountWordFrequency(word_array):
    unique_words=set(word_array)
    unsorted_word_frequencies=[(a_word,word_array.count(a_word)) for a_word in unique_words]
    word_frequencies=sorted(unsorted_word_frequencies,key=lambda x:(-1)*x[1])
    return word_frequencies
