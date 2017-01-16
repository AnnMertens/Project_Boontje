from __future__ import print_function, division
import nltk
from collections import defaultdict
from nltk.compat import Counter
from nltk.tag import TaggerI
from nltk.tbl import Feature, Template
from nltk import jsontags
from nltk.corpus import alpino
from nltk.corpus import conll2002

#train_data is alpino of conll2002 a of b  
def train_brill_tagger(train_data):
    # Modules for creating the templates.
    from nltk.tag import UnigramTagger
    from nltk.tag.brill import Pos, Word
    #from nltk.tag.brill import ProximateTagsRule, ProximateWordsRule
    from nltk.tbl import feature
    # The brill tagger module in NLTK.
    from nltk.tag import brill_trainer
    #Unigram_tagger maken om later initiele tagging op zin die we willen laten taggen te doen
    unigram_tagger = UnigramTagger(train_data)
    #unigram_tagger = nltk.pos_tag(train_data)

    # ranges van woorden meegeven voor of na het woord zodat brill_trainer zelf regels gaat bouwen
    # op positie waarbij 0 huidige positie is en 1 tot 1 is de volgende positie, 2 op 2 is met 1 woord overgeslagen
    # hij kan het ook op word. Maar op pos kan hij ook achteruitgaan.  

    templates = [
        Template(Pos([1, 1])),
        Template(Pos([2, 2])),
        Template(Pos([1, 2])),
        Template(Pos([1, 3])),
        Template(Word([1, 1])),
        Template(Word([2, 2])),
        Template(Word([1, 2])),
        Template(Word([1, 3])),
        Template(Pos([-1, -1]), Pos([1, 1])),
        Template(Pos([-1, -1]), Pos([1, 1]))
    ]
    # brill_trainer wordt getraind aan de hand van alpino of conll2002    
    # unigram_tagger geeft initiele tagging aan zin die we willen taggen. Nadien gaat hij verbeteren door train_brill_tagger uit te voeren.
    # ... ranges van pos en woord we gebruiken om regels te determineren, trace en deterministic moeten er staan...
    # ... om het te laten werken, no idea why)
    trainer = brill_trainer.BrillTaggerTrainer(initial_tagger=unigram_tagger, templates=templates, trace=3, deterministic=True)
    brill_tagger = trainer.train(train_data, max_rules=10)
    print("------")
    return brill_tagger

# To train and test using Alpino Corpus (Dutch).
# geeft lists of sets van zinnen uit alpino of connll2002 terug die getagd zijn.
# elke list is 1 zin, elke set is 1 woord + zijn tag 

# alpino_tagged_sents = alpino.tagged_sents()
# conll_tagged_sents = conll2002.tagged_sents('ned.testab')

# for sent in alpino_tagged_sents[0:5]:
#     print(sent)

# # testen op verschillende corpora
# print('-----------')
# for sentence in conll_tagged_sents:
#     for wordset in sentence:
#         if wordset[0] == "lust":
#             print(wordset)
# print('-----------')

# Split corpus into train/test.
#datasize = len(alpino_tagged_sents)
#datasize = len(conll_tagged_sents)
#trainsize = int(datasize*90/float(100))
#alpino_train = list(alpino_tagged_sents)
#conll_train = list(conll_tagged_sents)
#alpino_test = list(alpino_tagged_sents[trainsize+1:])
#alpinotest1 = [i for i,j in alpino_tagged_sents[trainsize+1]]

#bt_nld = train_brill_tagger(alpino_train)

# brilltagger trainen tegenover volledig getagd corpus adhv functie train_brill_tagger
# trained_brill_tagger_dutch = train_brill_tagger(conll_train)
# print('Test sentence:', alpinotest1)
# nadien zelf zin geven om te testen
# Dit is zin 1 en het is goed want het is een mooie zin
# 
#print(train_brill_tagger.tag(["Dit", "is", "zin", "1", "en", "het", "is", "goed", "want", "het", "is", "een", "mooie", "zin"]))
# via functie tag geven we opdracht op een zin te taggen rekening houdend met verbeteringen uit de train_brill_tagger.
#print(trained_brill_tagger_dutch.tag(["ik","lust","geen","soep"]))


# #testzin = "Het is een boek dat gaat over de kinderjaren van Ondineke"
# testzin = "Zij was geboren in Aalst. Haar zoon ging naar school om te leren schrijven."
# testlist = testzin.split(" ")
# print(trained_brill_tagger_dutch.tag(testlist))

# functie die brill_tagger gaat trainen en nieuwe tagger teruggeeft
def tagger_conll2002(a_or_b):
    """make tagger from tagged corpus conll2002 and train it with brill_tagger """
    conll_tagged_sents = conll2002.tagged_sents('ned.test' + a_or_b) 
    conll_train = list(conll_tagged_sents)
    trained_brill_tagger_dutch = train_brill_tagger(conll_train)
    return trained_brill_tagger_dutch

def tagger_alpino(range = None):
    """aanvullen"""
    alpino_tagged_sents = alpino.tagged_sents()
    if range:
        alpino_tagged_sents = alpino_tagged_sents[0:range]
    trainer_brill_tagger = train_brill_tagger(alpino_tagged_sents)
    return trainer_brill_tagger