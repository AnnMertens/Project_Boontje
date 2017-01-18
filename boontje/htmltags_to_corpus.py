""" html corpora opdelen in zinnen en woorden en deze zinnen in een lijst teruggeven als corpus"""
import nltk.data
import make_corpus
import filefunctions
from nltk.tokenize import word_tokenize
import tagging

# variabele tagger maken
#tagger_conll = tagging.tagger_conll2002('b')
tagger_alpino = tagging.tagger_alpino(2000)

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
    """ make a dict with 
    key "sentence", value the text_only_sentence and
    key "words", value list of words and 
    key "tagged_conll_words", value list of sets(word, conll_tag) and
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
    chapters = get_chapters("primaire bronnen/corpusKB/x97890295680436.xhtml")
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x97890295680438.xhtml"))
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x978902956804310.xhtml"))
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x978902956804312.xhtml"))
    chapters.extend(get_chapters("primaire bronnen/corpusKB/x978902956804313.xhtml", ["een onfatsoenlijk boek"]))
   

    ondineke_list_of_chapters, reinaert_list_of_chapters, vandaag_list_of_chapters, KB_list_of_chapters = make_corpus.divide_in_corpora(chapters)
    return corpus_to_sentences(ondineke_list_of_chapters), corpus_to_sentences(reinaert_list_of_chapters), corpus_to_sentences(vandaag_list_of_chapters), corpus_to_sentences(KB_list_of_chapters)


# functie om alle stukken van het corpus samen te klutsen
def get_chapters(filename, chapter_titles_to_skip=list()):
    filetext = filefunctions.read_file(filename)
    htmltagswithcontent = filefunctions.get_tags_with_specific_classnames_from_html(filetext)
    chapters = make_corpus.divide_in_chapters(htmltagswithcontent)
    # Verwijder ongewenste hoofdstukken (toevoegingen door andere schrijvers)
    for chapter in chapters:
        if chapter["title"].get_text() in chapter_titles_to_skip:
            chapters.remove(chapter)
    return chapters

# #testen
# ondineke_sentences, reinaert_sentences, vandaag_sentences, KB_sentences =  get_sentences_from_corpora_kapellekensbaan()
# # Print first Sentence
# print(KB_sentences[0]["sentence"])
# # Print last Sentence
# print(KB_sentences[-1]["sentence"])
# # Lengte van de corpora
# print(str(len(ondineke_sentences)) + ' - ' + str(len(reinaert_sentences)) + ' - ' + str(len(vandaag_sentences)) + ' - ' + str(len(KB_sentences)))
