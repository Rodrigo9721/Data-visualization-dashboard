# -*- coding: utf-8 -*-
"""
Created on Tue May  1 16:49:41 2018

@author: rcabg
"""

from word_checker import WordChecker


def main(x, spanishWords):

    wordChecker = WordChecker(spanishWords.words, spanishWords.totalFreq)
    words = x

    sin_candidatos = []
    candidatos = []

    for idx, word in enumerate(words):
        try:
            asd = wordChecker.getCorrection(word.lower()) ##Retorna el primer candidato en caso exista, la misma palabra en caso esté bien escrita y nada si no se encuentra
            if asd is None:
                sin_candidatos.append(word)
                words.pop(idx) ## En caso no exista, la palabra se elimina del texto
            else:
                candidatos.append(asd)

        except Exception as e:
            continue



    candidatos_junto = ' '.join(candidatos)
    return candidatos_junto

