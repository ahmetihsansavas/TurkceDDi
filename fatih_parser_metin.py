# -*- coding: utf-8 -*-

import speech_recognition as sr
import re
import jpype as jp

from collections import Counter

Fatih_Parser_PATH = 'fatih-parser.jar'

jp.startJVM(jp.getDefaultJVMPath(),'-ea' , '-Djava.class.path=%s' % (Fatih_Parser_PATH))


Language = jp.JClass('com.hrzafer.fatihparser.Language')
SentenceAnalyzerBuilder= jp.JClass('com.hrzafer.fatihparser.analyzer.SentenceAnalyzerBuilder')
Str = jp.JClass('java.lang.String')
#parsedsentencelist = jp.JClass('java.util.list')
SentenceAnalyzer = jp.JClass('com.hrzafer.fatihparser.analyzer.SentenceAnalyzer')

ParserFactory = jp.JClass('com.hrzafer.fatihparser.ParserFactory')
Parser = jp.JClass('com.hrzafer.fatihparser.Parser')
ParseTreeValidatorBuilder = jp.JClass('com.hrzafer.fatihparser.restriction.ParseTreeValidatorBuilder')
ParseFormatter = jp.JClass('com.hrzafer.fatihparser.format.ParseFormatter')
ParseDetail = jp.JClass('com.hrzafer.fatihparser.format.ParseDetail')
ParseSimplifier = jp.JClass('com.hrzafer.fatihparser.format.ParseSimplifier')
ParseLanguage = jp.JClass('com.hrzafer.fatihparser.format.ParseLanguage')

Sentence = jp.JClass('com.hrzafer.fatihparser.structure.Sentence')
Word = jp.JClass('com.hrzafer.fatihparser.structure.Word')
AmbigiousSentence = ('com.hrzafer.fatihparser.structure.AmbigiousSentence')

TableFileReader = jp.JClass('com.hrzafer.fatihparser.util.TableFileReader')
fatihparser = jp.JClass('com.hrzafer.fatihparser.FatihParser')

BracketedTree = jp.JClass('com.hrzafer.fatihparser.BracketedTree')
"""
r = sr.Recognizer()

with sr.Microphone() as source:
    print('Speak Anything : ')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language="tr-TR")
        print('Söylediğiniz şey : {}'.format(text))
        text2 = text
        liste1 = text2.split()
        print('\n'.join(map(str, liste1)))

    except :
        print('üzgünüm söylediğinizi anlayamadım..')
    textt=""

  """




Tr = Language.TR
SentenceAnalyzer = SentenceAnalyzerBuilder.build(Language.TR)

Parserexample = Parser(SentenceAnalyzer,ParserFactory.buildEarlyParser(Language.TR.getGrammarFilePath()),ParseTreeValidatorBuilder.build(Language.TR))


string = Str

parsedsentencelist = []




fp = open('cumleler.txt', 'r')
lines = fp.readlines()

ogelerine_ayrılan_cumleler = []
cumle_Sayisi = 0
ogelerineayrılmıscumlesayisi = 0

for line in lines:
  cumle_Sayisi +=1   
  trees=""
  temp = ""     
  maxilist = []
  format1 = ""    
  parsedsentencelist = Parserexample.parse(line)

  for i in range(len(parsedsentencelist)):
           
    print("Derivation ",i ," ",parsedsentencelist.get(i).getSentence().toString())
    trees = parsedsentencelist.get(i).getTrees()
    for j in range(len(trees)):	  
      if trees.get(j).isValid():
        temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
        print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
        format1=ParseFormatter.format(temp, ParseLanguage.Turkish)
        maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
  if(len(maxilist)>0):
    res = max(set(maxilist), key = maxilist.count) 
    str1 = str(max(set(maxilist), key = maxilist.count))
    print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))
    x = str1.split("[")
         
    yenix = x
    x2="" 
          
    for i in yenix:
      if i != "S":
        x2+="-"+i
    a = x2.split("]")
      #print(a)
    ogelerineayrılmıscumlesayisi+=1
    ogelerine_ayrılan_cumleler.append(a)    
    for j in a :
      b = print(j,end=" ")

    else:
      print ("-----yok---")

s = set()


#ogelerine_ayrılan_cumleler = set(ogelerine_ayrılan_cumleler)

for cumle in ogelerine_ayrılan_cumleler:
      print(cumle)

print(cumle_Sayisi ," adet cümleden ogelerine ayrılan sayısı",ogelerineayrılmıscumlesayisi)




Cumle_Ogeleri = ["Özne","Yüklem","Nesne","Tümleç","Zarf"]

jp.shutdownJVM()
