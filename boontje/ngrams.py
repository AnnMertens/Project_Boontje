""" stijltesten die gebruik maken van bigrams --> enkel functie tellen adjectieven weerhouden bij resultaten"""
import htmltags_to_corpus
from nltk.tokenize import word_tokenize
import nltk
from nltk.collocations import *
import make_corpus
import filefunctions
import string
from nltk import bigrams
import wordlist_of_corpus

# ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = htmltags_to_corpus.get_sentences_from_corpora_kapellekensbaan()
# walschap_sentences = htmltags_to_corpus.get_sentences_from_corpus_walschap()
# hvvb_sentences = htmltags_to_corpus.get_sentences_from_corpus_het_verdriet_van_belgie()

# functie om gebruik van adjectieven, gevolgd door zelfstandig naamwoord te tellen
def adjective(corpus):
    """ count use of adjectives corpus"""
    counter_adjective = 0

    for sentence in corpus:
        adj_found = False
        previous_word_is_adj = False
        previous_word = ""

        for word, tag in sentence["tagged_alpino_words"]:
            if previous_word_is_adj is True and tag == "noun":
                adj_found = True
                if adj_found is True:
                    counter_adjective += 1
            if tag == "adj":
                previous_word_is_adj = True
                previous_word = word
            else:
                previous_word_is_adj = False

    return counter_adjective

# # testen
# print("----")
# print(adjective(KB_sentences))
# print(adjective(reinaert_sentences))
# print(adjective(ondineke_sentences))
# print(adjective(vandaag_sentences))
# print("----")
# print(adjective(walschap_sentences))
# print("----")
# print(adjective(hvvb_sentences))


# # niet verder gebruikte tests. Eventueel opnieuw op te nemen voor thesis.
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

def get_bigrams_with_noun_adj_with_frequency(corpus):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    list_of_words_with_tag_noun_or_adj = list()

    for sentence in corpus:
        for word, tag in sentence["tagged_alpino_words"]:
            if tag == "noun" or tag == "adj":
                list_of_words_with_tag_noun_or_adj.append(word.lower())
    finder = BigramCollocationFinder.from_words(list_of_words_with_tag_noun_or_adj)
    scored = finder.score_ngrams(bigram_measures.raw_freq)

    return scored

def get_longer_bigrams_with_noun_adj_with_frequency(corpus):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    list_of_longer_words_with_tag_noun_or_adj = list()

    for sentence in corpus:
        for word, tag in sentence["tagged_alpino_words"]:
            if len(word) > 4:
                if tag == "noun" or tag == "adj":
                    list_of_longer_words_with_tag_noun_or_adj.append(word.lower())
    finder = BigramCollocationFinder.from_words(list_of_longer_words_with_tag_noun_or_adj)
    scored = finder.score_ngrams(bigram_measures.raw_freq)

    return scored

# # testen
# print(len(get_trigrams_with_frequency(KB_sentences)))    
# print ("++++++++++")
# print(get_trigrams_with_frequency(KB_sentences))    

# print("+++++++ met none")
# print(len(get_bigrams_with_specific_tag_with_frequency(KB_sentences)))
# print("+++++++ zonder none")
# print(len(get_bigrams_with_noun_adj_with_frequency(KB_sentences)))
# print("+++++++ longer zonder none")
# print(len(get_longer_bigrams_with_noun_adj_with_frequency(KB_sentences)))
# print("+++++++ longer zonder none")
# print(get_longer_bigrams_with_noun_adj_with_frequency(KB_sentences))
# print(get_longer_trigrams_with_noun_adj_with_frequency(KB_sentences))


#test = [("ik","bla"), ("ben","jk"), ("rijk","ek")]
#def get_bigrams_with_frequency(wordlist):
    #bigram_measures = nltk.collocations.BigramAssocMeasures()
    #finder = BigramCollocationFinder.from_words(wordlist)
    #scored = finder.score_ngrams(bigram_measures.raw_freq)

    #return scored

# print(get_bigrams_with_frequency(test))


# def get_top_500_bigrams(wordlist):
#     bigram_measures = nltk.collocations.BigramAssocMeasures()
#     finder = BigramCollocationFinder.from_words(wordlist)
#     scored = sorted(finder.nbest(bigram_measures.raw_freq, 500))
#
#     return scored

# list_of_words_with_tag_none_or_noun_or_adj = list()
# for sentence in KB_sentences:
#     for word, tag in sentence["tagged_alpino_words"]:
#         if tag == None or "noun" or tag == "adj":
#             list_of_words_with_tag_none_or_noun_or_adj.append(word.lower())
# # print(get_top_500_bigrams(list_of_words_with_tag_none_or_noun_or_adj))


# def get_trigrams_with_frequency(wordlist):
#     trigram_measures = nltk.collocations.TrigramAssocMeasures()
#     finder = TrigramCollocationFinder.from_words(wordlist)
#     scored = finder.score_ngrams(trigram_measures.raw_freq)
#
#     return scored

# def get_top_30_trigrams(wordlist):
#     trigram_measures = nltk.collocations.TrigramAssocMeasures()
#     finder = TrigramCollocationFinder.from_words(wordlist)
#     scored = sorted(finder.nbest(trigram_measures.raw_freq, 30))
#
#     return scored

# # testen
# print(get_trigrams_with_frequency(wordlist_of_corpus.make_list_in_lower_words_from_corpus(KB_sentences)))
# print("-----------------------")
# print(get_top_30_trigrams(wordlist_of_corpus.make_list_in_lower_words_from_corpus(KB_sentences)))










