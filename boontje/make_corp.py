"""divide the book in different corpora"""
import filefunctions
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




# alles testen
filetext = filefunctions.read_file("primaire bronnen/corpusKB/x97890295680436.xhtml")
htmltagswithcontent = filefunctions.get_tags_with_specific_classnames_from_html(filetext)
chapters = divide_in_chapters(htmltagswithcontent)

# # testen hoeveel hoofdstukken er zijn
print(len(chapters))




