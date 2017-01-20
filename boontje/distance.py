""" stijltesten van clisisvormen. Oorspronkelijk bedoeld via berekening distance """
import htmltags_to_corpus
from nltk.tokenize import word_tokenize
import nltk
from nltk.collocations import *
import make_corpus
import filefunctions
import string
from nltk import bigrams
import wordlist_of_corpus
from nltk.corpus import conll2002
from nltk.corpus import alpino
from wordlist_of_corpus import make_list_in_lower_words_from_corpus
from nltk import FreqDist

# ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = htmltags_to_corpus.get_sentences_from_corpora_kapellekensbaan()


# functie die list maakt van woorden (lower en zonder punctuation) met tag "None"
def make_list_of_lower_words_with_tag_none(corpus):
    """ make list of words (all lower and no punct) with tag "None" of corpus """
    list_of_words_lower_with_none_tag = list()

    for sentence in corpus:
        for word, tag in sentence["tagged_alpino_words"]:
            if tag is None:
                list_of_words_lower_with_none_tag.append(word.lower())

    return list_of_words_lower_with_none_tag


# functie die corpus krijgt en alle woorden met tag None ophaalt, in lower en beginnend met "t"
# idealiter worden de woorden uit test_corpora ook gelowered
def clisis_of_article_het_with_noun_or_verb(corpus):
    """count clisis of "t" at beginning with noun or verb """
    wordset_total_test_corpora = list(conll2002.words('ned.testb'))
    wordset_total_test_corpora.extend(list(alpino.words()))
    wordlist_lower_tag_none = make_list_of_lower_words_with_tag_none(corpus)
    wordlist_lower_tag_none_with_t_at_beginning = list()
    counter_clisis = 0

    for word in wordlist_lower_tag_none:
        if word[0] == "t":
            wordlist_lower_tag_none_with_t_at_beginning.append(word[1:])
            if word[1:] in wordset_total_test_corpora:
                counter_clisis += 1

    return counter_clisis


# functie die corpus krijgt en alle woorden met tag "None"" ophaalt, in lower en beginnend met "k"
# functie geeft te veel foute hits --> andere methode zoeken
# gecontroleerd en uiteindelijk komt "kzal" maar 1 keer voor in KB. Geen andere treffers.
def clisis_of_adverb_ik_with_verb(corpus):
    """count clisis of t at beginning with noun or verb """
    wordset_total_test_corpora = list(conll2002.words('ned.testb'))
    wordset_total_test_corpora.extend(list(alpino.words()))
    wordlist_lower_tag_none = make_list_of_lower_words_with_tag_none(corpus)
    wordlist_lower_tag_none_with_k_at_beginning = list()
    counter_clisis = 0

    for word in wordlist_lower_tag_none:
        if word[0] == "k":
            if word[1:] in wordset_total_test_corpora:
                counter_clisis += 1

    return counter_clisis


# functie die corpus krijgt en alle woorden telt waar "h"" aan het begin is weggevallen
# allo komt uiteindelijk maar in 1 zin voor. Boon gebruikt daarnaast ook hallo.--> bewering fout
def lost_of_h_at_beginning(corpus):
    """count lost of h at beginning of the words of a corpus"""
    wordset_total_test_corpora = list(conll2002.words('ned.testb'))
    wordset_total_test_corpora.extend(list(alpino.words()))
    wordlist_lower_tag_none = make_list_of_lower_words_with_tag_none(corpus)
    counter_lost_h = 0

    for word in wordset_total_test_corpora:
        if word[0] == "h":
            if word[1:] in wordlist_lower_tag_none:
                counter_lost_h += 1
            else:
                print("niks gevonden")

    return counter_lost_h


# # testen
# wordlist_lower_tag_none = make_list_of_lower_words_with_tag_none(KB_sentences)
# for word in wordset_lower_tag_none:
#     if "ist" in word:
#         print(word)
# print(len(sorted(wordlist_lower_tag_none)))

# print(clisis_of_article_het_with_noun_or_verb(KB_sentences))

# print(clisis_of_adverb_ik_with_verb(KB_sentences))

# # testen om clisis k with verb en clisis t after verb te tellen
# wordlist_KB = wordlist_of_corpus.make_list_in_lower_words_from_corpus(KB_sentences)
# fdist_KB = FreqDist(wordlist_KB)
# print("--------")
# print(fdist_KB["ist"])
# print("--------")
# print(fdist_KB["kzal"])
# print("--------")
# print(str(fdist_KB.freq("ist")) +" % in corpus KB")
# print("--------")
# print(str(fdist_KB.freq("kzal")) +" % in corpus KB")
# print("--------")


# niet verder gebruikte tests
# functie om twee woorden te vergelijken en afstand ervan te berekenen
def count_distance_word (word1, word2):
    """count distance between 2 lowered words """
    distance_word = 0

    for char1, char2 in zip(word1.lower(), word2.lower()):
        if char1 != char2:
            distance_word += 1

    return distance_word










