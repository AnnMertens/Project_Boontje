""" html corpora opdelen in zinnen en woorden en deze zinnen in een lijst teruggeven als corpus"""
import nltk.data
import make_corpus
import filefunctions
from nltk.tokenize import word_tokenize
import tagging
import glob

# variabele tagger maken
#tagger_conll = tagging.tagger_conll2002('b')
tagger_alpino = tagging.tagger_alpino()

# functie die een corpus doorloopt en alles wegschrijft naar list of dicts
def corpus_to_sentences(corpus):
    """divide a corpus (this is a list of chapters) in sentences and put them in a list"""
    sentences = list()

    for chapter in corpus:
        # dit is een list van dictionarys voor elke zin in de chapter 1.
        chapter_sentences = chapter_to_sentences(chapter)
        #extend ipv append gebruiken om te vermijden dat er een list of list binnen de list gemaakt wordt
        sentences.extend(chapter_sentences)

    return sentences


# functie om chapters in zinnen te splitsen
def chapter_to_sentences(chapter):
    """divide a chapter in sentences (list of sentence dictionaries) and put them in a list"""
    sentences = list()
    dict_of_title = sentence_to_dict(chapter["title"].get_text())
    sentences.append(dict_of_title)
    sentences.extend(part_to_sentences(chapter["paragraphs"]))
    # for paragraph in chapter["paragraphs"]:
    #      # dit is een list van dictionaries, voor elke zin in de paragraaf 1.
    #      paragraph_sentences = paragraph_to_sentences(paragraph)
    #      # extend ipv append gebruiken om te vermijden dat er een list of list binnen de list gemaakt wordt
    #      sentences.extend(paragraph_sentences)

    return sentences


def part_to_sentences(part):
    """devide a book part in sentences (list of sentence dictionaries) and put them in a list"""
    sentences = list()

    for paragraph in part:
        # dit is een list van dictionaries, voor elke zin in de paragraaf 1.
        paragraph_sentences = paragraph_to_sentences(paragraph)
        # extend ipv append gebruiken om te vermijden dat er een list of list binnen de list gemaakt wordt
        sentences.extend(paragraph_sentences)

    return sentences


# functie die een paragraaf splitst in zinnen
def paragraph_to_sentences(paragraph):
    """divide a paragraph in sentences (list of sentence dictionaries) and put them in a list"""
    sentences = list()
    tokenizer = nltk.data.load('tokenizers/punkt/dutch.pickle')
    sentences_only_text = list()
    # List van strings maken van alle zinnen (string) in de paragraaf
    sentences_only_text.extend(tokenizer.tokenize(paragraph.get_text()))

    # Overloop de zinnen (string) uit de paragraaf
    for sentence_only_text in sentences_only_text:
        # Maak van elke zin een dict en voeg hem toe aan de list (sentences) van alle zin dictionaries van de paragraaf
        sentences.append(sentence_to_dict(sentence_only_text))

    return sentences


# functie die zin omzet in dictionary met als key "sentence"" en als value de zin en tweede key "words" en als value een list van alle woorden 
def sentence_to_dict(text_only_sentence):
    """ make a dict with 
    key "sentence", value the text_only_sentence and
    key "words", value list of words and 
    key "tagged_alpino_words", value list of sets (word, alpino_tag)
     of that text_only_sentence"""
    result = dict()
    result["sentence"] = text_only_sentence
    result["words"] = sentence_to_list_of_words(text_only_sentence)
    #result["tagged_conll_words"] = tagger_conll.tag(result["words"])
    result["tagged_alpino_words"] = tagger_alpino.tag(result["words"])

    return result


# functie die zin omzet in list van woorden
def sentence_to_list_of_words(sentence):
    """ divide a sentence in words and put them in a list"""
    list_of_words_without_punctuation = list()
    list_of_words = word_tokenize(sentence)

    for word in list_of_words:
        word_without_punctuation = make_corpus.remove_punctation(word)
        if word_without_punctuation != "":
            list_of_words_without_punctuation.append(word_without_punctuation)

    return list_of_words_without_punctuation


# functie die uit een corpus alle zinnen haalt en wegschrijft in een dict met keys "sentence" en "words" en values de zin en list of words
def get_sentences_from_corpora_kapellekensbaan():
    """find all the sentences in the 4 corpora and put them in a tuple with for each corpus a dict """
    # filetext = filefunctions.read_file("primaire bronnen/corpusKB/x97890295680438.xhtml")
    # htmltagswithcontent = filefunctions.get_tags_with_specific_classnames_from_html(filetext)
    # chapters = make_corpus.divide_in_chapters(htmltagswithcontent)

    # Files in juiste volgorde uitlezen.
    chapters = get_chapters("primaire bronnen/corpusKB/x97890295680436.xhtml")
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x97890295680438.xhtml"))
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x978902956804310.xhtml"))
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x978902956804312.xhtml"))
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x978902956804313.xhtml", ["een onfatsoenlijk boek"]))


    ondineke_list_of_chapters, reinaert_list_of_chapters, vandaag_list_of_chapters, KB_list_of_chapters = make_corpus.divide_in_corpora(chapters)
    return corpus_to_sentences(ondineke_list_of_chapters), corpus_to_sentences(reinaert_list_of_chapters), corpus_to_sentences(vandaag_list_of_chapters), corpus_to_sentences(KB_list_of_chapters)


def get_sentences_from_corpus_het_verdriet_van_belgie():
    """find all the sentences in the corpus Het verdriet van België and put them in a list """
    part = list()

    for found_file in glob.glob("primaire bronnen/corpusHVVB/*.xhtml"):
        part.extend(get_bulk_content(found_file, r"(wp\-.*)|(calibre1)|(wpv.*)", "wpo-newpage"))

    return part_to_sentences(part)


def get_sentences_from_corpus_walschap():
    """find all the sentences in the corpus Walschap and put them in a list """
    part = list()

    for found_file in glob.glob("primaire bronnen/corpusWalschap/*.html"):
        part.extend(get_bulk_content(found_file, r"(noindent)|(indent)", "booksection"))

    return part_to_sentences(part)


# functie om alle stukken van het corpus samen te klutsen
def get_chapters(filename, chapter_titles_to_skip=list()):
    """get chapters and excluse chapters from specific list """
    filetext = filefunctions.read_file(filename)
    htmltagswithcontent = filefunctions.get_tags_with_specific_classnames_from_html(filetext)
    chapters = make_corpus.divide_in_chapters(htmltagswithcontent)

    # Verwijder ongewenste hoofdstukken (toevoegingen door andere schrijvers in nawoord)
    for chapter in chapters:
        if chapter["title"].get_text() in chapter_titles_to_skip:
            chapters.remove(chapter)

    return chapters

# functie om andere corpora te lezen
def get_bulk_content(filename, classNamesPattern, start_tag):
    """ get content from html with specific classname"""
    filetext = filefunctions.read_file(filename)
    htmltags_with_content = filefunctions.get_tags_with_specific_classnames_from_html_start_element(filetext, classNamesPattern, start_tag)
    tags_with_content = list()

    return htmltags_with_content



# # KB
# ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences =  get_sentences_from_corpora_kapellekensbaan()
# # Print first Sentence
# print(KB_sentences[0]["sentence"])
# # Print last Sentence
# print(KB_sentences[-1]["sentence"])
# # Lengte van de corpora
# print(str(len(ondineke_sentences)) + ' - ' + str(len(reinaert_sentences)) + ' - ' + str(len(vandaag_sentences)) + ' - ' + str(len(KB_sentences)))

# # HVVB
# het_verdriet_van_belgie_sentences = get_sentences_from_corpus_het_verdriet_van_belgie()
# print("Het verdriet van België")
# print(het_verdriet_van_belgie_sentences[5])
# print(het_verdriet_van_belgie_sentences[-1])
# print(len(het_verdriet_van_belgie_sentences))

# # Walschap
# walschap_sentences = get_sentences_from_corpus_walschap()
# print("Walschap")
# print(walschap_sentences[0])
# print(walschap_sentences[-1])
# print(len(walschap_sentences))
