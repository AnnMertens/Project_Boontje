"""divide the book in different corpora"""
import filefunctions
import string
from bs4 import BeautifulSoup # moet hele htmltekst doorlopen en tags zoeken


def divide_in_chapters(htmltagswithcontent): #format van htmltagswithcontent is een set
    """divide book in chapters"""
    # maak een list waarin alle hoofdstukken zullen komen
    # elk hoofdstuk wordt een aparte dict 
    # het resultaat is dus een list of dict
    list_of_chapters = list()
    last_dict = dict()
    
    # veiligheidsparagraphslist toevoegen om geen problemen te krijgen met files die niet zouden beginnen met een tussenkop
    last_dict["paragraphs"] = list()

    # tags allemaal doorlopen
    for tagwithcontent in htmltagswithcontent:
        # zoeken op klasse wp-tussenkop in de list met klassenamen van tagwithcontent 
        if "wp-tussenkop" in tagwithcontent['class']:
            # dan een nieuwe dict maken in de list met naam list_of_chapters
            list_of_chapters.append(dict())
            # de nieuw gecreeerde dict zal altijd het laatste element van de list_of_chapters zijn
            last_dict = list_of_chapters[-1]
            # de key in de dict is "title" en de value is de tagwithcontent
            last_dict["title"] = tagwithcontent
            last_dict["paragraphs"] = list()
        else:
            last_dict["paragraphs"].append(tagwithcontent)
    return list_of_chapters


# functie maken die gaat kijken of een paragraph bij ondineke hoort
def check_paragraph_for_ondineke(paragraph):
    """check if paragraph belongs to ondineke.Paragraph is value in dict"""
    all_spans_in_paragraphs = paragraph.find_all("span")
    paragraph_is_ondineke = True
    for span_with_content in all_spans_in_paragraphs:
        if "wpt-cursief" not in span_with_content['class'] and "wpt-cijfers1" not in span_with_content['class']:
           paragraph_is_ondineke = False

    # soms enkele letters niet cursief omdat het hoofdletters zijn, of interpunctie niet cursief in ondineke. 
    # hiervoor oplossing gezocht door maximum stukjes van 5 characters te laten afwijken van verplicht cursief of cijfer. 
    if paragraph_is_ondineke == True:
        # dit maakt een list met stukjes tekst die los in en rechtstreeks onder een paragraaf zitten
        alltextpieces_not_in_span = paragraph.find_all(text=True, recursive=False)
        for piece in alltextpieces_not_in_span:
            if len(piece) > 5:
                paragraph_is_ondineke = False
    return paragraph_is_ondineke

# functie maken om alle paragrafen van ondineke aan een hoofdstuk toe te voegen
def check_chapter_for_ondineke(chapter):
    """check if chapter belongs to ondineke. Chapter moet dict zijn met een list achter de key "paragraphs" """
    chapter_is_ondineke = True

    for paragraph in chapter["paragraphs"]:
        paragraph_is_ondineke = check_paragraph_for_ondineke(paragraph)
        if paragraph_is_ondineke == False:
            chapter_is_ondineke = False

    return chapter_is_ondineke        


# functie maken om interpunctie te verwijderen bij een gestript woord.
def remove_punctation(word):
    """remove punctuation on stripped word"""
    return_value = word.strip()
    for punctuation in string.punctuation:
        return_value = return_value.replace(punctuation, "")
    return return_value


# functie maken om alle paragrafen waarbij paragraph_is_reinaert True is aan een hoofdstuk toe te voegen
def check_chapter_for_reinaert(chapter):
    """ check if chapter ends with "johan janssens". Chapter moet dict zijn met een list als value bij de key"paragraphs" """
    chapter_is_reinaert = False
    last_paragraph = chapter["paragraphs"][-1]
    last_paragraph_text = last_paragraph.get_text()
    last_2_words = last_paragraph_text.split(" ")[-2:]
    last_word_without_punctuation = remove_punctation(last_2_words[-1])
    if last_2_words[0].lower() == "johan" and last_word_without_punctuation.lower() =="janssens":
        chapter_is_reinaert = True

    return chapter_is_reinaert


# functie maken die list_of_chapters gaat opdelen in 4 corpora, elk corpus in een aparte list
def divide_in_corpora(list_of_chapters):
    """ divide a list of chapters in corpora and put each corpus in a list of chapters"""
    # 4 corpora definieren
    ondineke_list_of_chapters = list()
    reinaert_list_of_chapters = list()
    vandaag_list_of_chapters = list()
    KB_list_of_chapters = list()


    for chapter in list_of_chapters:
        if check_chapter_for_ondineke(chapter) == True:
            ondineke_list_of_chapters.append(chapter)
        elif check_chapter_for_reinaert(chapter) == True:
            reinaert_list_of_chapters.append(chapter) 
        else:
            vandaag_list_of_chapters.append(chapter)
        KB_list_of_chapters.append(chapter)

    return ondineke_list_of_chapters, reinaert_list_of_chapters, vandaag_list_of_chapters, KB_list_of_chapters # dit geeft een tuple


# alles testen
filetext = filefunctions.read_file("primaire bronnen/corpusKB/x97890295680436.xhtml")
htmltagswithcontent = filefunctions.get_tags_with_specific_classnames_from_html(filetext)
chapters = divide_in_chapters(htmltagswithcontent)

# # testen hoeveel hoofdstukken er zijn
#print(len(chapters))

# # testen of tekst in hoofdstukken wordt verdeeld en deze titels printen
#for chapter in chapters:
    #print(chapter["title"].get_text())
    #print(chapter["paragraphs"][0].get_text()) #hier moet een index gegeven worden want value van paragraphs is een list
    #print(check_chapter_for_ondineke(chapter)) # geeft True (indien ondineke) or False voor alle hoofdstukken

ondineke_list_of_chapters, reinaert_list_of_chapters, vandaag_list_of_chapters, KB_list_of_chapters = divide_in_corpora(chapters)
print("ondineke " + str(len(ondineke_list_of_chapters)))
print("reinaert " + str(len(reinaert_list_of_chapters)))
print("vandaag " + str(len(vandaag_list_of_chapters)))
print("KB " + str(len(KB_list_of_chapters)))


