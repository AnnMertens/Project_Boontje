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
    # zoekt volledige tags waar de classname voldoet aan het patroon
    result = soup.find_all(class_=pattern)
    return result

# # testen van de functie read_file
filetext = read_file("primaire bronnen/corpusKB/x97890295680436.xhtml")
print(filetext)

# testen van de functie get_tags_with_specific_classnames_from_html op tweede en derde tag
htmltagswithcontent = get_tags_with_specific_classnames_from_html(filetext)
print(htmltagswithcontent[1:2])
#print((type)(htmltagswithcontent)) # het resultaat is een set

# enkel leesbare tekst van de eerste tag via toevoeging van functie get_text() 
#print(htmltagswithcontent[0].get_text())
#print(htmltagswithcontent.get_text()) werkt niet op volledige set! Er moet steeds een index worden gegeven

# een list maken met de classnames uit de eerste tag
#print(htmltagswithcontent[0]['class'])
#print((type)(htmltagswithcontent[0]['class'])) # het resultaat is een list

