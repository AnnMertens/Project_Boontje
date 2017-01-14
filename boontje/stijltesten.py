from nltk import FreqDist
import nltk.data
import make_corpus
import filefunctions
from nltk.tokenize import word_tokenize
import wordlist_of_corpus
import string
import htmltags_to_corpus
import re


ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = htmltags_to_corpus.get_sentences_from_corpora()
wordlist_ondineke = wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(ondineke_sentences)
wordlist_reinaert = wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(reinaert_sentences)
wordlist_vandaag = wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(vandaag_sentences)
wordlist_KB = wordlist_of_corpus.make_list_in_lower_without_punctuation_from_corpus(KB_sentences)
fdist_ondineke = FreqDist(wordlist_ondineke)
fdist_reinaert = FreqDist(wordlist_reinaert)
fdist_vandaag = FreqDist(wordlist_vandaag)
fdist_KB = FreqDist(wordlist_KB)

# # testen NLTK functies 
# print(fdist_ondineke)
# print(fdist_reinaert)
# print(fdist_ondineke["en"])
# print(fdist_ondineke.freq("en"))
# print(fdist_ondineke.most_common(20))


# functie die het specifiek gebruik van een woord in een fdist gaat zoeken # functie heeft geen nut want is bestaande nltk functie
def specific_use_of_token(token, fdist):
    if token in fdist:
        return fdist.freq(token)

# # testen
# result = specific_use_of_token("dingen", fdist_ondineke)
# print(result)

# # testen
# print(str(fdist_ondineke.freq("dingen")) +" % in corpus ondine")
# print(str(fdist_reinaert.freq("dingen")) +" % in corpus reinaert")
# print(str(fdist_vandaag.freq("dingen")) +" % in corpus vandaag")
# print(str(fdist_KB.freq("dingen")) +" % in corpus KB")



# functie die kijkt of specifiek woord in zin van corpus staat en zinnen met/zonder telt
# functie om gebruik van specifieke woorden te testen, bijvoorbeeld gebruik van "dingen"
def count_sentence_with_token(token, corpus):
    """count sentence with and without specific word in corpus"""
    counter_sentence_with_token = 0
    counter_sentence_without_token = 0
    for sentence in corpus:
        found_word = False
        for word in sentence["words"]:
            if word == token:
                found_word = True
        if found_word == True:
            counter_sentence_with_token += 1       
        else:
            counter_sentence_without_token += 1      

    return counter_sentence_with_token, counter_sentence_without_token

# # testen
# test_ondineke = count_sentence_with_token("dingen", ondineke_sentences)
# print(test_ondineke)
# test_reinaert = count_sentence_with_token("dingen", reinaert_sentences)
# print(test_reinaert)
# test_vandaag = count_sentence_with_token("dingen", vandaag_sentences)
# print(test_vandaag)
# test_KB = count_sentence_with_token("dingen", KB_sentences)
# print(test_KB)

# # testen
# test_ondineke = count_sentence_with_token(",", ondineke_sentences)
# print(test_ondineke)
# test_reinaert = count_sentence_with_token(",", reinaert_sentences)
# print(test_reinaert)
# test_vandaag = count_sentence_with_token(",", vandaag_sentences)
# print(test_vandaag)
# test_KB = count_sentence_with_token(",", KB_sentences)
# print(test_KB)

# test_ondineke = count_sentence_with_token("en", ondineke_sentences)
# print(test_ondineke)
# test_reinaert = count_sentence_with_token("en", reinaert_sentences)
# print(test_reinaert)
# test_vandaag = count_sentence_with_token("en", vandaag_sentences)
# print(test_vandaag)
# test_KB = count_sentence_with_token("en", KB_sentences)
# print(test_KB)


#functie die maximum aantal keer een zeker token in een zin gaat zoeken
#functie om enumeratie te vergelijken, zie ook functie count_sentence_with_number_of_token
def count_maximum_token_in_sentence(token, corpus):
    """count maximum frequency of token in 1 sentence"""
    counter_token = 0
    for sentence in corpus:
        counter_token_last = 0
        for word in sentence["words"]:
            if word == token:
                counter_token_last += 1
        if counter_token_last > counter_token:
            counter_token = counter_token_last
        #if counter_token_last == 16:
         #   print(sentence["sentence"])        

    return counter_token

# # testen
# print(count_maximum_token_in_sentence("en", ondineke_sentences))



# functie om dict van aantal keer zekere token te geven als key en met aantal zinnen als value
# functie om enumeratie te vergelijken met andere auteur. Zie ook count_maximum_token_in_sentence
def count_sentence_with_number_of_token(token, corpus):
    """count number of frequencies for certain token en gives dict with number of sentences for frequency of the token """
    number_of_token_with_number_of_sentences = dict()
    # zin per zin doorlopen
    for sentence in corpus:
        counter_token = 0
        # per zin het aantal keer "en" tellen
        for word in sentence["words"]:
            if word == token:
                counter_token +=1
        if counter_token in number_of_token_with_number_of_sentences:
            number_of_token_with_number_of_sentences[counter_token] += 1
        else:
            number_of_token_with_number_of_sentences[counter_token] = 1
    
    return number_of_token_with_number_of_sentences    

# #testen
# print(count_sentence_with_number_of_token("en", ondineke_sentences))


# functie die participia_praesentis gaat tellen
# zich programmatorisch wel goed, maar taalkundig nog niet. Tagging kan helpen. Nog uitzoeken indien tijd.
# fouten : zo neemt hij ook woorden als uitstekend, vanzelfsprekend of volgende
# fouten : en ook werkwoorden zoals zoende en weende
def participia_praesentis(corpus):
    """counts the number of participia praesentis in a corpus """
    counter_participia_praesentis = 0
    for sentence in ondineke_sentences:
        for word in sentence["words"]:
            if len(word) > 3 and word[-3:] == "end":
                counter_participia_praesentis += 1
            if len(word) > 5 and word[-4:] == "ende":
                counter_participia_praesentis += 1

    return counter_participia_praesentis

# # testen
#print(participia_praesentis(ondineke_sentences))


# functie die telt hoe vaak een bepaald werkwoord als hulpwerkwoord wordt gebruikt in een corpus
# functie om gebruik van beginnen als hulpwerkwoord te tellen
def auxiliary_verb(verb, corpus):
    """ count specific verb used as auxiliary verb in corpus"""
    counter_auxiliary_verb = 0
    for sentence in corpus:
        auxiliary_verb_found = False
        previous_word_is_verb = False 
        previous_word = ""
        for word in sentence["words"]:    
            if previous_word_is_verb == True and (word[-2:] == "en" or word == "te" or word == "gaan" or word == "staan" or word == "slaan" or word == "zijn"):
                print("------------------")
                print(previous_word + ' - ' + word)
                print(sentence["sentence"])
                auxiliary_verb_found = True
                if auxiliary_verb_found == True:
                    counter_auxiliary_verb += 1
            # nu pas controleren op verb want anders zou het eerste woord al true zijn en zou previous word geen zin hebben
            if word == verb:
                previous_word_is_verb = True
                previous_word = word
            else:
                previous_word_is_verb = False

    return counter_auxiliary_verb

# # testen
# print(auxiliary_verb("beginnen", KB_sentences))


# functie die telt hoe vaak een lijst van werkwoorden als hulpwerkwoord wordt gebruikt in een corpus
# functie om gebruik van "gaan" of "moeten en de vervoegingen daarvan als hulpwerkwoord te tellen
# functie werkt maar geeft niet het gewenste resultaat owv semantiek: ook veel gebruik van moeten in "normale" betekenis.
def auxiliary_verb_conj(list_of_verbs, corpus):
    """ count specific conjugated verbs in a list used as auxiliary verb in corpus"""
    counter_auxiliary_verb_conj = 0
    for sentence in corpus:
        auxiliary_verb_found = False
        previous_word_is_verb = False 
        previous_word = ""
        for word in sentence["words"]:    
            if previous_word_is_verb == True and (word[-2:] == "en" or word == "te" or word == "gaan" or word == "staan" or word == "slaan" or word == "zijn"):
                print("------------------")
                print(previous_word + ' - ' + word)
                print(sentence["sentence"])
                auxiliary_verb_found = True
                if auxiliary_verb_found == True:
                    counter_auxiliary_verb_conj += 1
            if word in list_of_verbs:
                previous_word_is_verb = True
                previous_word = word
            else:
                previous_word_is_verb = False

    return counter_auxiliary_verb_conj

# # testen
# list_of_verbs = ["moeten", "moesten", "moet", "moest"]
# print(auxiliary_verb_conj(list_of_verbs, KB_sentences))
# list_of_verbs = ["beginnen", "begint", "begonnen", "begon"]
# print(auxiliary_verb_conj(list_of_verbs, KB_sentences))


# functie die telt hoe vaak "des", gevolgd door woord dat eindigt op "s" wordt gebruikt (genitief)
# functie om gebruik van genitief s te tellen
def genitive_case(corpus):
    """ count use of genitive in corpus"""
    counter_genitive = 0
    for sentence in corpus:
        des_found = False
        previous_word_is_des = False 
        previous_word = ""
        for word in sentence["words"]:    
            if previous_word_is_des == True and word[-1:] == "s":
                print("------------------")
                print(previous_word + ' - ' + word)
                print(sentence["sentence"])
                des_found = True
                if des_found == True:
                    counter_genitive += 1
            if word == "des":
                previous_word_is_des = True
                previous_word = word
            else:
                previous_word_is_des = False
   
    return counter_genitive

# # testen
# print(genitive_case(KB_sentences))


# functie die telt in hoeveel zinnen van een corpus zelfcorrectie wordt toegepast
# functie om gebruik van zelfcorrectie op verschillende manieren te testen
def selfcorrection(corpus):
    """ count number of sentences with self corrections of author in corpus"""
    counter_selfcorrection = 0
    for sentence in corpus:
        if "t.t.z." in sentence["sentence"] or "tis te zeggen" in sentence["sentence"]:
                counter_selfcorrection += 1
                print("--------------")
                print(sentence["sentence"])
        for word in sentence["words"]:
            if word == "nee" or word == "neen":
                counter_selfcorrection += 1
                print("--------------")
                print(sentence["sentence"])
    
    return counter_selfcorrection

# # testen
# print(selfcorrection(KB_sentences))
# print(len(KB_sentences))


#functie telt hoe vaak er meer dan 1 hoofdletter na elkaar in een woord staat in een bepaalde wordlist
def use_of_capital(wordlist):
    """count number of words in wordlist with more dan 1 succesive capital"""
    counter_capital = 0
    pattern = re.compile(r".*[A-Z]{2,}")
    for word in wordlist:
        if pattern.match(word):
            counter_capital += 1
    return counter_capital

# # testen
# list_ondineke_nopunct = wordlist_of_corpus.make_list_without_punctuation_from_corpus(ondineke_sentences)
# print(use_of_capital(list_ondineke_nopunct))
# testlist = ["AAn", "aAAn","aAN","qsmdfljqs","AAN", "AAAAnnn","aaaaNNN", "aAAAAAn"]
# print(use_of_capital(testlist))


