
import htmltags_to_corpus
from nltk.tokenize import word_tokenize
import nltk
from nltk.collocations import *
import make_corpus
import filefunctions
import string
from nltk import bigrams
import wordlist_of_corpus
ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = htmltags_to_corpus.get_sentences_from_corpora()

# functie die list van tuples van mogelijke bigrams maakt op basis van de set van unieke woorden uit corpus
# list of tuples gemaakt om gemakkelijker te kunnen vergelijken met resultaat uit nltk bigrams 
def all_possible_bigrams_in_corpus(testset):
    """ make al list of tuples with all theorethically possible combinations of bigrams of a set"""
    list_possible_bigrams = list()
    for word1 in testset:
        for word2 in testset:   
            list_possible_bigrams.append((word1, word2))
    
    return list_possible_bigrams

# testen
testset_bigram_ondineke = set(wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(ondineke_sentences))
testset_bigram_reinaert = set(wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(reinaert_sentences))
#print(len(all_possible_bigrams_in_corpus(testset_bigram_ondineke)))
#print(all_possible_bigrams_in_corpus(testset_bigram_ondineke)
all_possible_bigram_reinaert = all_possible_bigrams_in_corpus(testset_bigram_reinaert)
#print((all_possible_bigrams_reinaert)[0:4])

# from nltk import bigrams
# for sentence in reinaert_sentences:
#     sentence_bigrams = bigrams(sentence["words"])
#     for bigram in sentence_bigrams:
#         print(type(bigram)) # geeft tuples

# from nltk import bigrams
# def make_bigrams_from_corpus(corpus):
#     for sentence in reinaert_sentences:
#         sentence_bigrams = bigrams(sentence["words"])
 
#     return sentence_bigrams # geeft generator object

# #testen
# print(make_bigrams_from_corpus(reinaert_sentences))

# for sentence in reinaert_sentences:
#     sentence_bigrams = bigrams(sentence["words"])
#     for bigram in sentence_bigrams:
#         if bigram in all_possible_bigram_reinaert:
#             print(bigram)

# for sentence in reinaert_sentences:
#     sentence_bigrams = BigramCollocationFinder.from_words(sentence["words"])  
#     print(type(sentence_bigrams))

def get_bigrams_with_frequency(wordlist):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(wordlist)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    return scored

def get_top_500_bigrams(wordlist):
    
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(wordlist)
    scored = sorted(finder.nbest(bigram_measures.raw_freq, 500))
    return scored
# # testen
#print(get_bigrams_with_frequency(wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(ondineke_sentences)))
#print("-----------------------")
#print(get_top_500_bigrams(wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(ondineke_sentences)))

# def get_trigrams_with_frequency(wordlist):
#     """ aanvullen"""
#     trigram_measures = nltk.collocations.TrigramAssocMeasures()
#     finder = TrigramCollocationFinder.from_words(wordlist)
#     scored = finder.score_ngrams(trigram_measures.raw_freq)
#     return scored

def get_top_30_trigrams(wordlist):
    """ aanvullen"""
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(wordlist)
    scored = sorted(finder.nbest(trigram_measures.raw_freq, 30))
    return scored

# # testen
# print(get_trigrams_with_frequency(wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(reinaert_sentences)))
# print("-----------------------")
print(get_top_30_trigrams(wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(reinaert_sentences)))







