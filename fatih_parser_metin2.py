# -*- coding: utf-8 -*-

import speech_recognition as sr
import re
import jpype as jp

from collections import Counter

Fatih_Parser_PATH = 'fatih-parser.jar'
#Java kodlarını python da çalıştırmak için gerekli Java Virtual Machine kodu
jp.startJVM(jp.getDefaultJVMPath(),'-ea' , '-Djava.class.path=%s' % (Fatih_Parser_PATH))

#Projemizde kullandığımız java Class ' larını python projemize import ediyoruz.
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


# Google ın Türkçe sesli konuşmaları yazıya aktarmak için kullandığımız kod
r = sr.Recognizer()
"""
with sr.Microphone() as source:
    print('Bir şey söyleyin : ')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language="tr-TR")
        text2 = text
        print('Söylediğiniz şey : {}'.format(text))
        liste1 = text2.split()
        print('\n'.join(map(str, liste1)))
    except :

       print('Üzgünüm söylediğinizi anlayamadım...')
    textt=""

"""



#Cümleleri ögelerine ayırmak için Java da yazılan kodları python a çevirdik
Tr = Language.TR
SentenceAnalyzer = SentenceAnalyzerBuilder.build(Language.TR)

Parserexample = Parser(SentenceAnalyzer,ParserFactory.buildEarlyParser(Language.TR.getGrammarFilePath()),ParseTreeValidatorBuilder.build(Language.TR))
yapılacak_liste = []

string = Str
parsedsentencelist = []
parsedsentencelist1 = []
parsedsentencelist2 = []

fp = open('sonra_önce_cumleler.txt', 'r')
lines = fp.readlines()

ogelerine_ayrılan_cumleler = []
cumle_Sayisi = 0
ogelerineayrılmıscumlesayisi = 0
#text2 sesli çalıştırmak için text1 'i text2 ye atıyoruz.
#text1 = text2
text_birlestir = ""
#eğer ses yerine doğrudan cümle vermek istiyorsak text1 i aşağıdan elle cümleye atıyoruz.
#text1 = "Ali eve gel sonra markete git"
for line in lines:
      text1 = line
      cumle_Sayisi+=1
      if 'sonra' in text1:
            is_sırası=[]
            splits = text1.split("sonra")
            print(splits)
            parsedsentencelist1 = Parserexample.parse(splits[0])
            trees=""
            temp = ""
            maxilist = []
            format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
            print("----------")
            for i in range(len(parsedsentencelist1)):
	            print("Derivation ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	            trees = parsedsentencelist1.get(i).getTrees()				
	            for j in range(len(trees)) :
		            if trees.get(j).isValid():
			            temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			            print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			            format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			            maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
            if(len(maxilist)>0):
                  res = max(set(maxilist), key = maxilist.count) 
                  str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
                  print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
                  x = str1.split("[")

                  yenix = x
                  x2=""
                  for i in yenix:
                        if i != "S":
                              x2+="-"+i

                  a = x2.split("]")
                  is_sırası.append(a)
                  print(a)
                  #ogelerineayrılmıscumlesayisi+=1
                  #ogelerine_ayrılan_cumleler.append(text_birlestir) 
  #aranankelime="-ve"
                  for j in a :                
                        print(j,end=" ")
            else:
                  print ("-----yok---")
      
            print("-----ikinci kısım--------")
            splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
            parsedsentencelist2 = Parserexample.parse(splits[1])
            trees=""
            temp = ""
            maxilist = []
            format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
            print("----------")
            for i in range(len(parsedsentencelist2)):
	            print("Derivation ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	            trees = parsedsentencelist2.get(i).getTrees()				
	            for j in range(len(trees)) :
		            if trees.get(j).isValid():
			            temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			            print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			            format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			            maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
            if(len(maxilist)>0):
                  res = max(set(maxilist), key = maxilist.count) 
                  str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
                  print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
                  x = str1.split("[")

                  yenix = x
                  x2=""
                  for i in yenix:
                        if i != "S":
                              x2+="-"+i

                  a = x2.split("]")
                  is_sırası.append(a)
                  print(a)
                  ogelerineayrılmıscumlesayisi+=1
                  #ogelerine_ayrılan_cumleler.append(a) 
  #aranankelime="-ve"
                  for j in a :                
                        print(j,end=" ")
            else:
                  print ("-----yok---")
            for i in range(len(is_sırası)):
                  print(i+1,". yapılacak is",is_sırası[i])
                  ogelerine_ayrılan_cumleler.append(is_sırası[i])
      elif 'önce' in text1:
            is_sırası=[]
            splits = text1.split("önce") #cümleyi özel bağlacımızın olduğu yerden bölüyoruz ve array olarak tutuluyor.
            print(splits)
            splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
            parsedsentencelist1 = Parserexample.parse(splits[1])
            trees=""
            temp = ""
            maxilist = []
            format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
            print("----------")
            for i in range(len(parsedsentencelist1)):
	            print("Derivation ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	            trees = parsedsentencelist1.get(i).getTrees()				
	            for j in range(len(trees)) :
		            if trees.get(j).isValid():
			            temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			            print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			            format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			            maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
            if(len(maxilist)>0):
                  res = max(set(maxilist), key = maxilist.count) 
                  str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
                  print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
                  x = str1.split("[")

                  yenix = x
                  x2=""
                  for i in yenix:
                        if i != "S":
                              x2+="-"+i

                  a = x2.split("]")
                  is_sırası.append(a)
                  print(a)
                  #ogelerineayrılmıscumlesayisi+=1
                  #ogelerine_ayrılan_cumleler.append(a)             
  #aranankelime="-ve"
                  for j in a :                
                        print(j,end=" ")
            else:
                  print ("-----yok---")
      
            print("-----ikinci kısım--------")
      
            parsedsentencelist2 = Parserexample.parse(splits[0])
            trees=""
            temp = ""
            maxilist = []
            format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
            print("----------")
            for i in range(len(parsedsentencelist2)):
	            print("Derivation ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	            trees = parsedsentencelist2.get(i).getTrees()				
	            for j in range(len(trees)) :
		            if trees.get(j).isValid():
			            temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			            print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			            format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			            maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
            if(len(maxilist)>0):
                  res = max(set(maxilist), key = maxilist.count) 
                  str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
                  print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
                  x = str1.split("[")

                  yenix = x
                  x2=""
                  for i in yenix:
                        if i != "S":
                              x2+="-"+i

                  a = x2.split("]")
                  is_sırası.append(a)
                  print(a)
                  ogelerineayrılmıscumlesayisi+=1
                  #ogelerine_ayrılan_cumleler.append(a)             
  #aranankelime="-ve"
                  for j in a :                
                        print(j,end=" ")
            else:
                  print ("-----yok---")
            for i in range(len(is_sırası)):
                  print(i+1,". yapılacak is",is_sırası[i])
                  ogelerine_ayrılan_cumleler.append(is_sırası[i])
            
      
      elif 'ardından' in text1:
            is_sırası=[]
            splits = text1.split("ardından")
            print(splits)
            parsedsentencelist1 = Parserexample.parse(splits[0])
            trees=""
            temp = ""
            maxilist = []
            format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
            print("----------")
            for i in range(len(parsedsentencelist1)):
	            print("Derivation ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	            trees = parsedsentencelist1.get(i).getTrees()				
	            for j in range(len(trees)) :
		            if trees.get(j).isValid():
			            temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			            print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			            format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			            maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
            if(len(maxilist)>0):
                  res = max(set(maxilist), key = maxilist.count) 
                  str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
                  print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
                  x = str1.split("[")

                  yenix = x
                  x2=""
                  for i in yenix:
                        if i != "S":
                              x2+="-"+i

                  a = x2.split("]")
                  is_sırası.append(a)
                  print(a)
                  #ogelerineayrılmıscumlesayisi+=1
                  #ogelerine_ayrılan_cumleler.append(a)             
  #aranankelime="-ve"
                  for j in a :                
                        print(j,end=" ")
            else:
                  print ("-----yok---")
      
            print("-----ikinci kısım--------")
            splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
            parsedsentencelist2 = Parserexample.parse(splits[1])
            trees=""
            temp = ""
            maxilist = []
            format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
            print("----------")
            for i in range(len(parsedsentencelist2)):
	            print("Derivation ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	            trees = parsedsentencelist2.get(i).getTrees()				
	            for j in range(len(trees)) :
		            if trees.get(j).isValid():
			            temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			            print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			            format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			            maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
            if(len(maxilist)>0):
                  res = max(set(maxilist), key = maxilist.count) 
                  str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
                  print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
                  x = str1.split("[")

                  yenix = x
                  x2=""
                  for i in yenix:
                        if i != "S":
                              x2+="-"+i

                  a = x2.split("]")
                  is_sırası.append(a)
                  print(a)
                  ogelerineayrılmıscumlesayisi+=1
                  #ogelerine_ayrılan_cumleler.append(a)             
  #aranankelime="-ve"
                  for j in a :                
                        print(j,end=" ")
            else:
                  print ("-----yok---")
            for i in range(len(is_sırası)):
                  print(i+1,". yapılacak is",is_sırası[i])
                  ogelerine_ayrılan_cumleler.append(is_sırası[i])
      else :

      
#eger cümlemizde önce,sonra,ardından,daha sonra yoksa doğrudan cümle ögelerini bulmak için yazılan kod kısmı
            parsedsentencelist = Parserexample.parse(text1)
            trees=""
            temp = ""
            maxilist = []
            format1 = ""

#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
            print("----------")
            for i in range(len(parsedsentencelist)):
	            print("Derivation ",i ," ",parsedsentencelist.get(i).getSentence().toString())
	            trees = parsedsentencelist.get(i).getTrees()				
	            for j in range(len(trees)) :

		            if trees.get(j).isValid():

			            temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			            print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			            format1=ParseFormatter.format(temp, ParseLanguage.Turkish)
			
			            maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))

            if(len(maxilist)>0):
                  res = max(set(maxilist), key = maxilist.count) 
                  str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
                  print ("Most frequent parse is : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
                  x = str1.split("[")

                  yenix = x
                  x2=""
                  for i in yenix:
                        if i != "S":
                              x2+="-"+i

                  a = x2.split("]")
                  ogelerineayrılmıscumlesayisi+=1
                  ogelerine_ayrılan_cumleler.append(a) 
                  print(a)
  #aranankelime="-ve"
                  for j in a :
        
        
                        print(j,end=" ")
            else:
                  print ("-----yok---")

Cumle_Ogeleri = ["Özne","Yüklem","Nesne","Tümleç","Zarf"]

print("ögelerine ayrılan cümleler")
for cumle in ogelerine_ayrılan_cumleler:
      print(cumle)

print("-----------------------------------")


#print(cumle_Sayisi ," adet cümleden ogelerine ayrılan sayısı",ogelerineayrılmıscumlesayisi)

fp1 = open('sonra_önce_cumleler.txt', 'r')
lines1 = fp1.readlines()

for line1 in lines1:
      print(line1)


#Gerekli çıktıyı aldıktan sonra JVM yi kapatıyoruz.
jp.shutdownJVM()

