import htmltags_to_corpus

ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = htmltags_to_corpus.get_sentences_from_corpora_kapellekensbaan()


def alliteration(corpus):
    """counts the number of alliteration in a corpus """
    counter_alliteration = 0

    for sentence in corpus:
        alliteration_found = False
        previous_word = False
        previous_word =""
        for word in sentence["words"]:
            
            if previous_word[:1] == word[:1]:
                counter_alliteration += 1
                # print(previous_word + " - " + word)
                # print("---------")
                previous_word = True
                previous_word = word
          
            else:
                previous_word = True
                previous_word = word

    return counter_alliteration


def alliteration_first2(corpus):
    """counts the number of alliteration of 2 characters in a corpus """
    counter_alliteration_first2 = 0

    for sentence in corpus:
        alliteration_found = False
        previous_word = False
        previous_word =""
        for word in sentence["words"]:
            
            if previous_word[:2] == word[:2]:
                counter_alliteration_first2 += 1
                # print(previous_word + " - " + word)
                # print("---------")
                previous_word = True
                previous_word = word
          
            else:
                previous_word = True
                previous_word = word

    return counter_alliteration_first2


def alliteration_first3(corpus):
    """counts the number of alliteration of 3 characters in a corpus """
    counter_alliteration_first3 = 0

    for sentence in corpus:
        alliteration_found = False
        previous_word = False
        previous_word =""
        for word in sentence["words"]:
            
            if previous_word[:3] == word[:3]:
                counter_alliteration_first3 += 1
                # print(previous_word + " - " + word)
                # print("---------")
                previous_word = True
                previous_word = word
          
            else:
                previous_word = True
                previous_word = word

    return counter_alliteration_first3

print(alliteration(KB_sentences))
print("/////////////")
print(alliteration_first2(KB_sentences))
print(".................")
print(alliteration_first3(KB_sentences))


words = ("dit", "is", "een", "erste", "test")
counter_alliteration = 0
alliteration_found = False
previous_word = False
previous_word =""
for word in words:
            
    if previous_word[:1] == word[:1]:
        counter_alliteration += 1
        # print(previous_word + " **** " + word)
        # print("***********************")
        previous_word = True
        previous_word = word
          
    else:
        previous_word = True
        previous_word = word
