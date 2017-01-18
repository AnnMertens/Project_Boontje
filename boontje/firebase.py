"""database toegang"""
import pyrebase
from htmltags_to_corpus import get_sentences_from_corpora_kapellekensbaan
from stijltesten import count_sentence_with_token
from distance import clisis_of_article_het_with_noun_or_verb
from wordlist_of_corpus import make_list_in_lower_words_from_corpus
from wordlist_of_corpus import make_list_of_words_from_corpus
from stijltesten import count_maximum_token_in_sentence
from stijltesten import count_sentence_with_number_of_token
from stijltesten import participia_praesentis
from stijltesten import auxiliary_verb
from stijltesten import auxiliary_verb_conj
from stijltesten import genitive_case
from stijltesten import selfcorrection
from stijltesten import use_of_capital
from rhymes import alliteration
from rhymes import alliteration_first2
from rhymes import alliteration_first3



from nltk import FreqDist

# functie create_connection maken die ....
def create_connection():
    config_settings = {
        "apiKey": "AIzaSyBF7l-W2MdF4yBbknmtNobInj1ujJ1IHA0", 
        "authDomain": "boontje-aa2c4.firebaseapp.com", 
        "databaseURL": "https://boontje-aa2c4.firebaseio.com", 
        "storageBucket": "boontje-aa2c4.appspot.com", 
        "messagingSenderId": "83637322760"
    }

    # Maak een verbinding met de firebase database
    firebase_link = pyrebase.initialize_app(config_settings)

    # Vraag aan de link een test om te authenticeren
    auth = firebase_link.auth()

    # Gebruik de teruggekregen authenticatie test om te authenticeren aan de hand van je gebruikersnaam en paswoord 
    user = auth.sign_in_with_email_and_password("abc@def.be", "abcdef")

    # Vraag aan de verbinding je database toegang te voorzien
    database = firebase_link.database()

    # Return je database toegang en je gebruikers token (jouw unieke sleutel) die je moet gebruiken om bewerkingen op je database te mogen doen.
    return database, user["idToken"]

# deze functie dient om zinnen naar database weg te schrijven
def write_sentence_to_database(corpusnaam, corpus, database, sectoken):
    # Verwijder alles uit de database dat als hoofd-element de naam van het corpus bevat. 
    # (om ervoor te zorgen dat het corpus geen tweede keer in de database word gestoken)
    #database.child(corpusnaam).remove(sectoken)
    # Voeg een element toe aan de database met de naam van het corpus en voeg ineens onder dit...
    # ... element al de zinnen van het corpus toe.
    results = database.child(corpusnaam).set(corpus[2], sectoken)
    # Return eventueel het antwoord wat de database geeft nadat het het corpus heeft proberen in te voegen.
    return results

def write_test_to_Database():
    database.child("testAnn").child("childAnn").set("Ik ben een waarde", sectoken)

# Haal al de corpussen op (1 corpus is 1 list van dictionaries, 1 zo'n dictionary stelt 1 zin voor)
ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = get_sentences_from_corpora_kapellekensbaan()

# # # Maak een verbinding met de database en bekom zo de verbinding en je token om te kunnen werken als user
database, sectoken = create_connection()
# # Schrijf het corpus Ondineke naar de database
# write_sentence_to_database("Ondineke", ondineke_sentences, database, sectoken)
# # Schrijf het corpus Reinaert naar de database
# write_sentence_to_database("Reinaert", reinaert_sentences, database, sectoken)
# # Schrijf het corpus Vandaag naar de database
# database.child("vandaag_sentences").remove(sectoken)
# write_sentence_to_database("Vandaag", vandaag_sentences, database, sectoken)
# # Schrijf het corpus KBCorpus naar de database
# database.child("KBCorpus").remove(sectoken)
# write_sentence_to_database("KB", KB_sentences, database, sectoken)

# write_test_to_Database()
# database.child("KBCorpus").remove(sectoken)
# database.child("KB").remove(sectoken)
# database.child("Ondineke").remove(sectoken)
# database.child("Vandaag").remove(sectoken)
# database.child("Reinaert").remove(sectoken)
# database.child("testAnn").remove(sectoken)



# functie die alle tests gaat uitvoeren en het resultaat gaat wegschrijven naar de database.
def execute_all_tests_and_store_results(corpusnaam, corpus, database, sectoken):
    database, sectoken = create_connection()

    number_of_sentences = len(corpus)
    results = database.child(corpusnaam).child("number_sentences").set(number_of_sentences, sectoken)

    number_of_words = len(make_list_of_words_from_corpus(corpus))
    results = database.child(corpusnaam).child("number_words").set(number_of_words, sectoken)

    number_of_unique_words = len(set(make_list_of_words_from_corpus(corpus)))
    results = database.child(corpusnaam).child("number_unique_words").set(number_of_unique_words, sectoken)
    
    sentence_with, sentence_without = count_sentence_with_token("dingen", corpus)
    results = database.child(corpusnaam).child("dingen").child("number_sentence_with").set(sentence_with, sectoken)
    results = database.child(corpusnaam).child("dingen").child("number_sentence_without").set(sentence_without, sectoken)

    fdist_corpus = FreqDist(make_list_in_lower_words_from_corpus(corpus))
    results = database.child(corpusnaam).child("allo").set((fdist_corpus["allo"]), sectoken)
    results = database.child(corpusnaam).child("hallo").set((fdist_corpus["hallo"]), sectoken)
    
    sentence_with, sentence_without = count_sentence_with_token("allo", corpus)
    results = database.child(corpusnaam).child("allo").child("number_sentence_with").set(sentence_with, sectoken)
    results = database.child(corpusnaam).child("allo").child("number_sentence_without").set(sentence_without, sectoken)

    sentence_with, sentence_without = count_sentence_with_token("hallo", corpus)
    results = database.child(corpusnaam).child("hallo").child("number_sentence_with").set(sentence_with, sectoken)
    results = database.child(corpusnaam).child("hallo").child("number_sentence_without").set(sentence_without, sectoken)

    number_of_words = clisis_of_article_het_with_noun_or_verb(corpus)
    results = database.child(corpusnaam).child("number_proclisis_t").set(number_of_words, sectoken)

    fdist_corpus = FreqDist(make_list_in_lower_words_from_corpus(corpus))
    results = database.child(corpusnaam).child("number_enclisis_t_verb").child("ist").set((fdist_corpus["ist"]), sectoken)
    results = database.child(corpusnaam).child("percentage_of_words_enclisis_t_verb").child("ist").set(str(fdist_corpus.freq("ist")), sectoken)

    fdist_corpus = FreqDist(make_list_in_lower_words_from_corpus(corpus))
    results = database.child(corpusnaam).child("number_proclisis_k_verb").child("kzal").set((fdist_corpus["kzal"]), sectoken)
    results = database.child(corpusnaam).child("percentage_of_words_proclisis_k_verb").child("kzal").set(str(fdist_corpus.freq("kzal")), sectoken)

    counter_token = count_maximum_token_in_sentence("en", corpus)
    results = database.child(corpusnaam).child("maximum_number_of_specific_word_in_sentence").child("en").set(counter_token, sectoken)

    number_of_token_with_number_of_sentences = count_sentence_with_number_of_token("en", corpus)
    results = database.child(corpusnaam).child("number_of_sentences_with_specific_word").child("en").set(number_of_token_with_number_of_sentences, sectoken)
    
    counter_participia_praesentis = participia_praesentis(corpus)
    results = database.child(corpusnaam).child("number_of_participia_praesentis").set(counter_participia_praesentis, sectoken)

    counter_auxiliary_verb = auxiliary_verb("beginnen", corpus)
    results = database.child(corpusnaam).child("number_of_beginnen_as_auxiliary_verb").set(counter_auxiliary_verb, sectoken)

    counter_auxiliary_verb_conj = auxiliary_verb(("begin","begint", "beginnen", "begon", "begonnen"), corpus)
    results = database.child(corpusnaam).child("number_of_beginnen_as_conjugated_auxiliary_verb").set(counter_auxiliary_verb_conj, sectoken)

    counter_genitive_case= genitive_case(corpus)
    results = database.child(corpusnaam).child("number_of_genitive_case_with_des").set(counter_genitive_case, sectoken)

    counter_selfcorrection = selfcorrection(corpus)
    results = database.child(corpusnaam).child("number_of_sentences_with_selfcorrection").set(counter_selfcorrection, sectoken)

    counter_capital = use_of_capital(make_list_of_words_from_corpus(corpus))
    results = database.child(corpusnaam).child("number_words_with_more_than_1_capital").set(counter_capital, sectoken)

    counter_alliteration = alliteration(corpus)
    results = database.child(corpusnaam.child("number_of_alliterations").set(counter_alliteration, sectoken))

    counter_alliteration_first2 = alliteration_first2(corpus)
    results = database.child(corpusnaam.child("number_of_alliterations_2_char").set(counter_alliteration_first2, sectoken))

    counter_alliteration_first3 = alliteration(corpus)
    results = database.child(corpusnaam.child("number_of_alliterations_3_char").set(counter_alliteration_first3, sectoken))


execute_all_tests_and_store_results("Ondineke", ondineke_sentences, database, sectoken)
execute_all_tests_and_store_results("Reinaert", reinaert_sentences, database, sectoken)
execute_all_tests_and_store_results("Vandaag", vandaag_sentences, database, sectoken)
execute_all_tests_and_store_results("KB", KB_sentences, database, sectoken)
    


