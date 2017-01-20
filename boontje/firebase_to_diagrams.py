"""database toegang en wegschrijven in grafieken naar pdf"""
import pyrebase
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# functie create_connection maken die connectie met firebase maakt
def create_connection():
    """ Create a firebase connection """
    config_settings = {
        "apiKey": "AIzaSyBF7l-W2MdF4yBbknmtNobInj1ujJ1IHA0",
        "authDomain": "boontje-aa2c4.firebaseapp.com",
        "databaseURL": "https://boontje-aa2c4.firebaseio.com",
        "storageBucket": "boontje-aa2c4.appspot.com",
        "messagingSenderId": "83637322760"
    }

    firebase_link = pyrebase.initialize_app(config_settings)
    auth = firebase_link.auth()
    user = auth.sign_in_with_email_and_password("abc@def.be", "abcdef")
    database = firebase_link.database()

    return database, user["idToken"]

database, sectoken = create_connection()


def get_single_result_from_test(test_name_result_list):
    """ Create a dictionary with all the values from the corpora for the specified test """
    # build_question --> get(sectoken) --> val()
    hvvb_result = build_question("HVVB",test_name_result_list).get(sectoken).val()
    walschap_result = build_question("Walschap",test_name_result_list).get(sectoken).val()
    kb_result = build_question("KB",test_name_result_list).get(sectoken).val()
    ondineke_result = build_question("Ondineke",test_name_result_list).get(sectoken).val()
    vandaag_result = build_question("Vandaag",test_name_result_list).get(sectoken).val()
    reinaert_result = build_question("Reinaert",test_name_result_list).get(sectoken).val()

    return {'KB': kb_result, 'Ondineke': ondineke_result, 'Reinaert': reinaert_result, 'Vandaag': vandaag_result, 'HVVB': hvvb_result, 'Walschap': walschap_result}


def get_number_of_sentences_with_multiple_en_above(number):
    """ Create a dictionary with all the values from the corpora for the test multiple en in sentence.
    Count the total number above the specified number """
    # Get all the values from count en for every corpus. Dict of lists {'KB':[10,5,2,3], 'Ondineke':[7,4,2,1], ...}
    number_lists = get_single_result_from_test(["number_of_sentences_with_specific_word","en"])
    # een dict maken voor alle resultaten
    result = dict()

    # Doorloop de dictionary number_lists elke corpus met zijn lijst van waarden in value
    for key, value in number_lists.items():
        # Per corpus het total_number op 0 zetten om het te kunnen berekenen
        total_number = 0
        # Eerst controleren of de lijst wel lang genoeg is om de items boven number terug te kunnen geven.
        if len(value) >= number:
            # Geef alle totalen voor en dat voorkomt met dan aantal keer in een zin.
            only_above_number = value[number:]
            # Doorloop deze totalen
            for counter in only_above_number:
                # Als er een totaal aanwezig is ...
                if counter is not None:
                    # Tel het op bij total_number voor dit corpus
                    total_number += counter
        # Zet het totaal gevonden number in de resultaat dict bij de key met naam van de corpus
        result[key] = total_number

    return result


def get_result_from_test_to_total_words(test_name_result_list):
    dict_total_words = get_single_result_from_test(["number_words"])
    dict_values = get_single_result_from_test(test_name_result_list)
    recalculated_values = dict()

    for key, value in dict_values.items():
        recalculated_values[key] = (value/dict_total_words[key])*dict_total_words["KB"]

    return recalculated_values


def get_result_from_test_to_total_sentences(test_name_result_list):
    dict_total_sentences = get_single_result_from_test(["number_sentences"])
    dict_values = get_single_result_from_test(test_name_result_list)
    recalculated_values = dict()

    for key, value in dict_values.items():
        recalculated_values[key] = (value/dict_total_sentences[key])*dict_total_sentences["KB"]

    return recalculated_values


def get_result_from_test_to_unique_words(test_name_result_list):
    # Haal de opgeslagen waarden op voor number_unique_words van alle corpora
    dict_unique_words = get_single_result_from_test(["number_unique_words"])
    # Haal de gewenste waarden op voor de aangeduide test, aangeduid door de waarden in test_name_result_list
    dict_values = get_single_result_from_test(test_name_result_list)
    # Dict voor de herberekende waardes
    recalculated_values = dict()

    # Doorloop de verschillende items in values dict
    for key, value in dict_values.items():
        # Herbereken de value en stop hem in de resultaat dict onder dezelfde key
        recalculated_values[key] = (value/dict_unique_words[key])*dict_unique_words["KB"]

    return recalculated_values


def build_question(corpus_naam,test_name_result_list):
    # resultaat opvragen startend vanaf database.child(corpus_naam)
    return_element = database.child(corpus_naam)
    for name in test_name_result_list:
        return_element = return_element.child(name)

    # voorbeeld resultaat: database.child('KB').child('number_enclisis_t_verb').child('ist')
    return return_element


def create_bar_chart(result, y_label, header, pdf):
    values_list = list()
    # Eerste 4 bars zijn altijd die van boontje, volgorde vastgelegd
    name_list = ['KB','Ondineke','Reinaert', 'Vandaag']

    # Alle bijkomende / toekomstige corpora automatisch toevoegen 
    for key, value in result.items():
        if key not in name_list:
            name_list.append(key)

    # In volgorde van de namen de waarden toevoegen aan de list van values, zodat de values nog met de namen overeenkomen
    for name_key in name_list:
        values_list.append(result[name_key])

    # Het totale aantal bars in variabel N zetten
    N = len(values_list)

    # Positie van de eerste 4 bars
    ind = [0, 0.35, 0.7, 1.05]

    # Positie van de resterende corpora toevoegen
    intI = 1
    for i in name_list[4:]:
        intI += 1
        ind.append(intI)

    # Breedte van de bar vastleggen in variabele
    width = 0.35

    # creëren van de grafiek
    fig, ax = plt.subplots()
    # Rechthoeken opbouwen aan de hand van de locaties, de waardes, de breedte en de kleur
    rects1 = ax.bar(ind, values_list, width, color='r')

    # add some text for labels, title and axes ticks
    ax.set_ylabel(y_label)
    ax.set_title(header)

    # Labelposities berekenen. (zelfde positie als de balken + de helft van een balk)
    ax_positions = list()
    for i in ind:
        ax_positions.append(i+(width/2))

    # Label positie zetten naar de juist berekende posities
    ax.set_xticks(ax_positions)
    
    # De effectieve labels toevoegen + de text 25 graden roteren
    ax.set_xticklabels(name_list, rotation=25)

    # Labels boven de bars plaatsen
    autolabel(ax, rects1)

    #plt.show()
    pdf.savefig()
    plt.close()


def autolabel(ax, rects):
    """Attach a text label above each bar displaying its height"""
    # voor elke rechthoek
    for rect in rects:
        # vraag de hoogte op
        height = rect.get_height()
        # zet tekst boven rect op positie en hoogte, specifieke tekst, met uitlijning
        ax.text(rect.get_x() + rect.get_width()/2., 1.03*height, '%d' % int(height), ha='center', va='bottom')


with PdfPages("Boontje.pdf") as pdf:
    # echte waarden van resultaat
    result = get_single_result_from_test(["maximum_number_of_specific_word_in_sentence", "en"])
    create_bar_chart(result, "max number of 'en'", "Maximum number of 'en' in 1 sentence", pdf)

    # waarden van resultaat herberekend alsof alle corpora evenveel woorden zouden hebben als KB
    result = get_result_from_test_to_total_words(["number_enclisis_t_verb", "ist"])
    create_bar_chart(result, "number 'ist'", "'ist' to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_alliterations_1_char"])
    create_bar_chart(result, "number alliterations 1 char", "alliterations 1 character to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_alliterations_2_char"])
    create_bar_chart(result, "number alliterations 2 char", "alliterations 2 characters to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_alliterations_3_char"])
    create_bar_chart(result, "number alliterations 3 char", "alliterations 3 characters to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_beginnen_as_auxiliary_verb"])
    create_bar_chart(result, "number 'beginnen'", "'beginnen' as aux verb to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_beginnen_as_conjugated_auxiliary_verb"])
    create_bar_chart(result, "number conjugated 'beginnen'", "conjugated 'beginnen' to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_genitive_case_with_des"])
    create_bar_chart(result, "number genetive 'des'", "genetive 'des' to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_participia_praesentis"])
    create_bar_chart(result, "number participia praesentis", "participia praesentis to number of words KB", pdf)
    
    result = get_result_from_test_to_total_words(["number_proclisis_k_verb","kzal"])
    create_bar_chart(result, "number 'kzal'", "proclisis 'kzal' to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_words_with_more_than_1_capital"])
    create_bar_chart(result, "number words with more than 1 capital", "words with more than 1 capital to number of words KB", pdf)

    result = get_result_from_test_to_total_words(["number_of_adjectives"])
    create_bar_chart(result, "number adjectives", "adjectives to number of words KB", pdf)
    
    # vergelijking ten opzichte van aantal zinnen, herberekend naar aantal zinnen KB
    result = get_result_from_test_to_total_sentences(["number_of_sentences_with_selfcorrection"])
    create_bar_chart(result, "number self correction sentenses", "self correction sentences to number of sentences KB", pdf)

    # specifieke berekening voor dit geval
    result = get_number_of_sentences_with_multiple_en_above(5)
    create_bar_chart(result, "'en' in sentence", "'en' in sentence above 5", pdf)

    # alleen om te testen => Distributed to unique words
    #result = get_result_from_test_to_unique_words(["number_of_participia_praesentis"])
    #create_bar_chart(result, "number participia praesentis", "participia praesentis to number of unique words KB", pdf)

                                                                                                                                                                                                                           