"""collection of functions to use with files"""
from bs4 import BeautifulSoup # Beautifulsoup is een htmlreader
import re


def read_file(filename):
    """Read_file text from file"""
    # openen, lezen en sluiten van tekst, ongeacht formaat
    open_file = open(filename, 'rt', encoding='utf-8')
    file_text = open_file.read()
    open_file.close()
    return file_text

def get_tags_with_specific_classnames_from_html(htmltext):
    """Get tags with classname wp-plat, wp-platmetwit or wp-tussenkop from html text and put in a set"""
    # deelt op in tags en geeft tags en de inhoud in een set
    soup = BeautifulSoup(htmltext, 'html.parser')
    pattern = re.compile(r"(wp\-plat)|(wp\-platmetwit)|(wp\-tussenkop)")
    # zoekt volledige tags waar de classname voldoet aan het patroon en returned een set
    result = soup.find_all(class_=pattern)
    return result

def get_tags_with_specific_classnames_from_html_start_element(htmltext, class_names_pattern, start_tag_class_name):
    """Get tags from tag types with classname in classNamesPattern from html text and put in a set"""
    # deelt op in tags en geeft tags en de inhoud in een set
    soup = BeautifulSoup(htmltext, 'html.parser')
    parent_tag_with_content = soup.find(attrs={'class':start_tag_class_name})

    pattern = re.compile(class_names_pattern)
    # zoekt volledige tags waar de classname voldoet aan het patroon en returned een set
    result = parent_tag_with_content.find_all(class_=pattern)
    return result

# # testen van de functie read_file
#filetext = read_file("primaire bronnen/corpusKB/x97890295680436.xhtml")
#print(filetext)

# testen van de functie get_tags_with_specific_classnames_from_html op tweede en derde tag
#htmltagswithcontent = get_tags_with_specific_classnames_from_html(filetext)
#print(htmltagswithcontent[1:2])
#print((type)(htmltagswithcontent)) # het resultaat is een set

# enkel leesbare tekst van de eerste tag via toevoeging van functie get_text() 
#print(htmltagswithcontent[0].get_text())
# print(htmltagswithcontent.get_text()) werkt niet op volledige set! Er moet steeds een index worden gegeven

# een list maken met de classnames uit de eerste tag
#print(htmltagswithcontent[0]['class'])
#print((type)(htmltagswithcontent[0]['class'])) # het resultaat is een list

# def get_only_text_from_set_of_tags_in_html(htmltext):
#     results = get_tags_with_specific_classnames_from_html(htmltext) # dit geeft set of tags
#     # variabele voor volledige tekst van wp-plat wp-platmetwit wp-tussenkop die we als resultaat gaan teruggeven
#     all_tags_only_text = ""
#     # Doorloop de tags één voor één en voeg de text van elke tag toe aan de variabele all_tags_only_text
#     for tag in results:
#         result_only_text = tag.get_text()
#         #voeg toe aan totaal resultaat string
#         all_tags_only_text += result_only_text
#     return all_tags_only_text

#print(get_only_text_from_set_of_tags_in_html(filetext))

# # testen functie get_only_text_from_tags_in_html
# only_text = get_only_text_from_set_of_tags_in_html([1], filetext)
# print(only_text)
  



