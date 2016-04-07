import nltk
import re
from twokenize import tokenize
from nltk.tag.perceptron import PerceptronTagger



def getForm(tagged_line):


    # CASE 0 WISH VERB FORM
    # p0 = re.compile('\.*/will/MD/', re.IGNORECASE)
    # pq = re.compile('\.*\?.*')
    # if p0.search(tagged_line) != None or pq.search(tagged_line) != None:
    #     return 0


    # CASE 1 WISH VERB FORM
    p1 = re.compile('\.*(wish|wishing)/(VB.*/|JJ/)', re.IGNORECASE)
    if p1.search(tagged_line) != None:
        return 1


    # CASE 2 CONJUNTION NORMAL
    p2 = re.compile('\.*/CCJ/.*((/VBD/)|(/VBN/)).*/MD/', re.IGNORECASE)
    if p2.search(tagged_line) != None:
        return 2


    # CASE 3 CONJUNCTIVE CONVERSE
    p3 = re.compile('\.*/MD/.*/CCJ/.*((/VBN/)|(/VBD/))', re.IGNORECASE)
    if p3.search(tagged_line) != None:
        return 3

    # CASE 4 MODAL NORMAL
    p4 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)).*/MD/.*((/VBN/)|(/VBD/)|(/VB/)|(VBZ))', re.IGNORECASE)
    if p4.search(tagged_line) != None:
        return 4

    # CASE 4 MODAL NORMAL
    # p4 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)).*/MD/.*((/VBN/)|(/VBD/))', re.IGNORECASE)
    # if p4.search(tagged_line) != None:
    #    return 4


    # CASE  HYPOTHETICAL NORMAL -> now included in CCJ
    # Key words: rather, imagine, envision, conceptualize, conjure up, visualize


    # CASE 5 Should have
    p5 = re.compile('\.*/((should)|(shoulda)(shulda)|(shuda)|(shudda)|(shudve))/MD/((have)|(hve)|(ve))/(\w)*((/VBN/)|(/VBD/))', re.IGNORECASE)
    if p5.search(tagged_line) != None:
        return 5

    # CASE 6 VERB INVERSION
    p6 = re.compile('\.*((were/)|(had/)).*((/NN/)|(/NNP/)|(/NNPS/)|(/NNS/)|(/PRP.*/)).*((/VBN/)|(/VBD/)).*/MD/', re.IGNORECASE)
    if p6.search(tagged_line) != None:
        return 6

    # CASE 7 MODAL Adverb Comparative
    p7 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)|(/VB/)).*/RBR/.*/MD/.*((/VBN/)|(/VBD/)|(/VB/))', re.IGNORECASE)
    if p7.search(tagged_line) != None:
        return 7

    # If no matches
    return 0

def format_tagged(tagged_list):
    out = ''
    for t in tagged_list:
        out = out + t[0] + '/' + t[1] + '/'
    out = out + '\n'
    return out

def main(argv):

    tagger = PerceptronTagger()
    tagset = None
    tokens = tokenize(line)
    tags = nltk.tag._pos_tag(tokens, tagset, tagger)
    format_tagged(tags)