""" html corpora opdelen in zinnen en woorden en deze zinnen in een lijst teruggeven als corpus"""
import nltk.data
import make_corpus
import filefunctions
from nltk.tokenize import word_tokenize

# functie die een corpus doorloopt en alles wegschrijft naar list of dicts
def corpus_to_sentences(corpus):
    """divide a corpus (this is a list of chapters) in sentences and put them in a list"""
    sentences = list()

    for chapter in corpus:
        # dit is een list van dictionarys voor elke zin in de chapter een.
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

    for paragraph in chapter["paragraphs"]:
         # dit is een list van dictionarys voor elke zin in de paragraaf een.
         paragraph_sentences = paragraph_to_sentences(paragraph)
         #extend ipv append gebruiken om te vermijden dat er een list of list binnen de list gemaakt wordt
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
    """ make a dict with key "sentence", value the text_only_sentence and key"words", value list of words of that text_only_sentence"""
    result = dict()
    result["sentence"] = text_only_sentence
    result["words"] = sentence_to_list_of_words(text_only_sentence)
    return result

# functie die zin omzet in list van woorden
def sentence_to_list_of_words(sentence):
    """ divide a sentence in words and put them in a list"""
    list_of_words = list()
    list_of_words = word_tokenize(sentence)
    return list_of_words

# functie die uit een corpus alle zinnen haalt en wegschrijft in een dict met keys "sentence" en "words" en values de zin en list of words
def get_sentences_from_corpora():
    """find all the sentences in the 4 corpora and put them in a tuple with for each corpus a dict """
    filetext = filefunctions.read_file("primaire bronnen/corpusKB/x97890295680436.xhtml")
    htmltagswithcontent = filefunctions.get_tags_with_specific_classnames_from_html(filetext)
    chapters = make_corpus.divide_in_chapters(htmltagswithcontent)

    ondineke_list_of_chapters, reinaert_list_of_chapters, vandaag_list_of_chapters, KB_list_of_chapters = make_corpus.divide_in_corpora(chapters)
    return corpus_to_sentences(ondineke_list_of_chapters), corpus_to_sentences(reinaert_list_of_chapters), corpus_to_sentences(vandaag_list_of_chapters), corpus_to_sentences(KB_list_of_chapters)

# testen
ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences =  get_sentences_from_corpora()
print(ondineke_sentences[1])
print(str(len(ondineke_sentences)) + ' - ' + str(len(reinaert_sentences)) + ' - ' + str(len(vandaag_sentences)) + ' - ' + str(len(KB_sentences)))

