""" alle manieren om lijsten uit de corpora te halen"""
import htmltags_to_corpus
from nltk.tokenize import word_tokenize
import make_corpus
import filefunctions
import string


# tuple, verdeeld over 4 variabelen
# ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = htmltags_to_corpus.get_sentences_from_corpora_kapellekensbaan()

#print(reinaert_sentences[0:2]) # geeft titel en de eerste zin in een dict met sentence and words als keys
#print(len(ondineke_sentences)) 
#print(type(ondineke_sentences)) #is een list of dict


# functie die alle woorden gaat ophalen uit de zinnen van een corpus en deze in één GROTE wordlist gaat steken.
def make_list_of_words_from_corpus(corpus):
    """make a list of words from the corpus"""
    wordlist = list()

    for sentence in corpus:
        for word in sentence["words"]:
            wordlist.append(word)

    return wordlist


# functie die unieke woorden uit de zinnen van een corpus haalt en in een set steekt.
def make_set_of_unique_words_from_corpus(corpus):
    """make a set of unique words from corpus"""
    wordset = list()

    for sentence in corpus:
        for word in sentence["words"]:
            wordset.append(word)

    return set(wordset)
#--> overbodige functie want kan ook via eerste functie, namelijk return set(wordlist)


# functie die alle woorden uit corpus lowered en in een lijst zet 
def make_list_in_lower_words_from_corpus(corpus):
    """lower all words in corpus and make a list of them"""
    wordlist_lower = list()

    for sentence in corpus:
        for word in sentence["words"]:
            wordlist_lower.append(word.lower())

    return wordlist_lower


# functie die alle woorden uit corpus in een lijst met hun tags zet 
def make_list_with_tagged_words_from_corpus(corpus):
    """ make a list the words with tag"""
    wordlist_lower_with_tag = list()

    for sentence in corpus:
        wordlist_lower_with_tag.extend(sentence["tagged_alpino_words"])

    return wordlist_lower_with_tag


# # functie die list van alle woorden van corpus geeft zonder interpunctie
# # functie overbodig want punctuation later weggehaald bij opzet dict
# def make_list_without_punctuation_from_corpus(corpus):
#     """make a list of words without punctuation of corpus"""
#     wordlist_without_punctuation = list()
#     for sentence in corpus:
#         for word in sentence["words"]:
#             # volgende lijnen toegevoegd na test omwille van quotes bij Boon
#             if len(word) > 1 and word[0] == "‘"or len(word) > 1 and word[0] == "“":
#                word = word[1]
#             if len(word) > 1 and word[-1] == "’"or len(word) > 1 and word[-1] == "”":
#                word = word[:-1]
#             if word not in string.punctuation and word != "..." and word != "’" and word != "–" and word != "––" and word != "–––":
#                wordlist_without_punctuation.append(word)
#     return wordlist_without_punctuation


# for sentence in KB_sentences:
#     for word in sentence["words"]:
#         if word == "’k" or word == "’s" or word == "’t":
#             print(sentence["sentence"])


# # alles testen
# wordlist_ondineke = make_list_of_words_from_corpus(ondineke_sentences)
# print(wordlist_ondineke)

# wordset_ondineke = make_list_of_words_from_corpus(ondineke_sentences)
# print(len(set(wordset_ondineke)))

# wordlist_lower_ondineke = make_list_in_lower_words_from_corpus(ondineke_sentences)
# print(wordlist_lower_ondineke)

# wordlist_without_punctuation_ondineke = make_list_without_punctuation_from_corpus(ondineke_sentences)
# print(sorted(set(wordlist_without_punctuation_ondineke))[-20:])

# wordlist_lower_nopunt = make_list_in_lower_words_from_corpus(ondineke_sentences)
# print(len(wordlist_lower_nopunt))

#wordlist_tagged_ondineke = make_list_with_tagged_words_from_corpus(ondineke_sentences)
#print(len(wordlist_tagged_ondineke))







