"""database toegang"""
import pyrebase
from htmltags_to_corpus import get_sentences_from_corpora_kapellekensbaan, get_sentences_from_corpus_het_verdriet_van_belgie, \
get_sentences_from_corpus_walschap
from stijltesten import count_sentence_with_token, count_maximum_token_in_sentence, count_sentence_with_number_of_token, \
participia_praesentis, auxiliary_verb, auxiliary_verb_conj, genitive_case, selfcorrection, use_of_capital
from distance import clisis_of_article_het_with_noun_or_verb
from wordlist_of_corpus import make_list_in_lower_words_from_corpus, make_list_of_words_from_corpus
from rhymes import alliteration
from nltk import FreqDist
from ngrams import adjective

# functie die connectie met mijn firebase-account maakt
def create_connection():
    """creates connection with firebase account"""
    config_settings = {
        "apiKey": "AIzaSyBF7l-W2MdF4yBbknmtNobInj1ujJ1IHA0", 
        "authDomain": "boontje-aa2c4.firebaseapp.com", 
        "databaseURL": "https://boontje-aa2c4.firebaseio.com", 
        "storageBucket": "boontje-aa2c4.appspot.com", 
        "messagingSenderId": "83637322760"
    }

    # verbinding maken met de firebase database
    firebase_link = pyrebase.initialize_app(config_settings)

    # link vragen om te authenticeren
    auth = firebase_link.auth()

    # teruggekregen authenticatietest gebruiken om te authenticeren met gebruikersnaam en paswoord 
    user = auth.sign_in_with_email_and_password("abc@def.be", "abcdef")

    # aan firebase vragen om databasetoegang te voorzien
    database = firebase_link.database()

    # return databasetoegang en gebruikerstoken (unieke sleutel) om bewerkingen op de database te mogen doen
    return database, user["idToken"]



# Haal al de corpussen op (1 corpus is 1 list van dicts, 1 dict is 1 zin)
ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences = get_sentences_from_corpora_kapellekensbaan()
walschap_sentences = get_sentences_from_corpus_walschap()
het_verdriet_van_belgie_sentences = get_sentences_from_corpus_het_verdriet_van_belgie()

    
# Maak verbinding met de database en bekom zo de verbinding en de token om te kunnen bewerken
database, sectoken = create_connection()

# Verwijder alles uit de database dat als hoofdelement de naam van het corpus bevat.
# (om ervoor te zorgen dat het corpus geen tweede keer in de database wordt gestoken)
database.child("HVVB").remove(sectoken)
database.child("KB").remove(sectoken)
database.child("Ondineke").remove(sectoken)
database.child("Vandaag").remove(sectoken)
database.child("Reinaert").remove(sectoken)
database.child("Walschap").remove(sectoken)


# functie die alle tests gaat uitvoeren en het resultaat gaat wegschrijven naar de database.
def execute_all_tests_and_store_results(corpusnaam, corpus, database, sectoken):
    """ do all the testing and write results to firebase"""

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

    counter_auxiliary_verb_conj = auxiliary_verb_conj(("begin", "begint", "beginnen", "begon", "begonnen"), corpus)
    results = database.child(corpusnaam).child("number_of_beginnen_as_conjugated_auxiliary_verb").set(counter_auxiliary_verb_conj, sectoken)

    counter_genitive_case = genitive_case(corpus)
    results = database.child(corpusnaam).child("number_of_genitive_case_with_des").set(counter_genitive_case, sectoken)

    counter_selfcorrection = selfcorrection(corpus)
    results = database.child(corpusnaam).child("number_of_sentences_with_selfcorrection").set(counter_selfcorrection, sectoken)

    counter_capital = use_of_capital(make_list_of_words_from_corpus(corpus))
    results = database.child(corpusnaam).child("number_words_with_more_than_1_capital").set(counter_capital, sectoken)

    counter_alliteration = alliteration(1, corpus)
    results = database.child(corpusnaam).child("number_of_alliterations_1_char").set(counter_alliteration, sectoken)

    counter_alliteration = alliteration(2, corpus)
    results = database.child(corpusnaam).child("number_of_alliterations_2_char").set(counter_alliteration, sectoken)

    counter_alliteration = alliteration(3, corpus)
    results = database.child(corpusnaam).child("number_of_alliterations_3_char").set(counter_alliteration, sectoken)

    counter_adjective = adjective(corpus)
    results = database.child(corpusnaam).child("number_of_adjectives").set(counter_adjective, sectoken)

execute_all_tests_and_store_results("Ondineke", ondineke_sentences, database, sectoken)
execute_all_tests_and_store_results("Reinaert", reinaert_sentences, database, sectoken)
execute_all_tests_and_store_results("Vandaag", vandaag_sentences, database, sectoken)
execute_all_tests_and_store_results("KB", KB_sentences, database, sectoken)
execute_all_tests_and_store_results("HVVB", het_verdriet_van_belgie_sentences, database, sectoken)
execute_all_tests_and_store_results("Walschap", walschap_sentences, database, sectoken)

# toegang tot project in mijn firebase gegeven aan volgende adressen :
# mike.kestemont@gmail.com
# walter.daelemans@gmail.com
