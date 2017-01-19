import nltk
from filefunctions import read_file
import htmltags_to_corpus

ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = htmltags_to_corpus.get_sentences_from_corpora_kapellekensbaan()
walschap_sentences = htmltags_to_corpus.get_sentences_from_corpus_walschap()
hvvb_sentences = htmltags_to_corpus.get_sentences_from_corpus_het_verdriet_van_belgie()

# functie nog uit te werken of weg te smijten
# def read_syllables_corpus(filename):
#     file_text = read_file(filename)
#     return_list = list()
#     for line in file_text.split("\n"):
#         first_word = True
#         word_dict = dict()
#         word_dict["syl"] = list()
        
#         for word in line.split(" "):
#             if first_word:
#                 word_dict["word"] = word
#             else:
#                 word_dict["syl"].append(word)
#             first_word = False
#         return_list.append(word_dict)
#     return return_list

# functie nog uit te werken of weg te smijten
# def rhyme(inp, level):
#     entries = read_syllables_corpus("resource/voxforge_nl_sphinx.dic")
#     syllables = [(word, syl) for word, syl in entries if word == inp]
#     rhymes = []
#     for (word, syllable) in syllables:
#         rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
#     return set(rhymes)

# print("word?")
# word = input()
# print("level?")
# level = input()
# print(rhyme(word, level))

#for dict_item in read_syllables_corpus("resource/voxforge_nl_sphinx.dic")[0:50]:
    #print(dict_item)


# functie die eerste x characters van opeenvolgende woorden gaat controleren
def alliteration(char_num, corpus):
    """counts the number of alliterations with x characters in a corpus """
    counter_alliteration = 0

    for sentence in corpus:
        alliteration_found = False
        previous_word = False
        previous_word =""

        for word in sentence["words"]:
            if previous_word[:char_num] == word[:char_num]:
                counter_alliteration += 1
                # print(previous_word + " - " + word)
                # print("---------")
                previous_word = True
                previous_word = word
            else:
                previous_word = True
                previous_word = word

    return counter_alliteration

# # testen
# print("222222222222")
# print(alliteration(2, KB_sentences))
# print(alliteration(2, walschap_sentences))
# print("333333333333")
# print(alliteration(3, KB_sentences))
# print(alliteration(3, walschap_sentences))
# print("4444444444444")
# print(alliteration(4, KB_sentences))
# print(alliteration(4, walschap_sentences))
# print("555555555")
# print(alliteration(5, KB_sentences))
# print(alliteration(5, walschap_sentences))



