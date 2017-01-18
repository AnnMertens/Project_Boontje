
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
# def all_possible_bigrams_in_corpus(testset):
#     """ make al list of tuples with all theorethically possible combinations of bigrams of a set"""
#     list_possible_bigrams = list()
#     for word1 in testset:
#         for word2 in testset:   
#             list_possible_bigrams.append((word1, word2))
    
#     return list_possible_bigrams

# testen
#testset_bigram_ondineke = set(wordlist_of_corpus.make_list_in_lower_words_from_corpus(ondineke_sentences))
#testset_bigram_KB = set(wordlist_of_corpus.make_list_in_lower_words_from_corpus(KB_sentences))
#print(len(all_possible_bigrams_in_corpus(testset_bigram_ondineke)))
#print(all_possible_bigrams_in_corpus(testset_bigram_ondineke)
#all_possible_bigram_KB = all_possible_bigrams_in_corpus(testset_bigram_KB)
#print((all_possible_bigrams_KB)[0:4])

# from nltk import bigrams
# for sentence in KB_sentences:
#     sentence_bigrams = bigrams(sentence["words"])
#     for bigram in sentence_bigrams:
#         print(type(bigram)) # geeft tuples

# from nltk import bigrams
# def make_bigrams_from_corpus(corpus):
#     for sentence in KB_sentences:
#         sentence_bigrams = bigrams(sentence["words"])

#     return sentence_bigrams # geeft generator object

#testen
#print(make_bigrams_from_corpus(KB_sentences))


# def get_bigrams_with_frequency(wordlist):
#     bigram_measures = nltk.collocations.BigramAssocMeasures()
#     finder = BigramCollocationFinder.from_words(wordlist)
#     scored = finder.score_ngrams(bigram_measures.raw_freq)
#     return scored

def get_bigrams_with_specific_tag_with_frequency(corpus):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    list_of_words_with_tag_none_or_noun_or_adj = list()
    for sentence in corpus:
        for word, tag in sentence["tagged_alpino_words"]:
            if tag == None or tag == "noun" or tag == "adj":
                list_of_words_with_tag_none_or_noun_or_adj.append(word.lower())
    finder = BigramCollocationFinder.from_words(list_of_words_with_tag_none_or_noun_or_adj)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    return scored

print("++++++")
print(get_bigrams_with_specific_tag_with_frequency(KB_sentences))
print("+++++++")


test = [("ik","bla"), ("ben","jk"), ("rijk","ek")]
def get_bigrams_with_frequency(wordlist):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(wordlist)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    return scored

print(get_bigrams_with_frequency(test))


# def get_top_500_bigrams(wordlist):
    
#     bigram_measures = nltk.collocations.BigramAssocMeasures()
#     finder = BigramCollocationFinder.from_words(wordlist)
#     scored = sorted(finder.nbest(bigram_measures.raw_freq, 500))
#     return scored


# def get_trigrams_with_frequency(wordlist):
#     """ aanvullen"""
#     trigram_measures = nltk.collocations.TrigramAssocMeasures()
#     finder = TrigramCollocationFinder.from_words(wordlist)
#     scored = finder.score_ngrams(trigram_measures.raw_freq)
#     return scored

# def get_top_30_trigrams(wordlist):
#     """ aanvullen"""
#     trigram_measures = nltk.collocations.TrigramAssocMeasures()
#     finder = TrigramCollocationFinder.from_words(wordlist)
#     scored = sorted(finder.nbest(trigram_measures.raw_freq, 30))
#     return scored

# # testen
# print(get_trigrams_with_frequency(wordlist_of_corpus.make_list_in_lower_words_from_corpus(KB_sentences)))
# print("-----------------------")
# print(get_top_30_trigrams(wordlist_of_corpus.make_list_in_lower_words_from_corpus(KB_sentences)))


print(get_bigrams_with_frequency(reinaert_sentences[36]["tagged_alpino_words"]))




