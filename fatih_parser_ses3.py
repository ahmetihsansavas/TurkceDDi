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

with sr.Microphone() as source:
    print('Bir şey söyleyin : ')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language="tr-TR")
        text2 = text.lower()
        print('Söylediğiniz şey : {}'.format(text))
        liste1 = text2.split()
        print('\n'.join(map(str, liste1)))
    except :

       print('Üzgünüm söylediğinizi anlayamadım...')
    textt=""




#Cümleleri ögelerine ayırmak için Java da yazılan kodları python a çevirdik
Tr = Language.TR
SentenceAnalyzer = SentenceAnalyzerBuilder.build(Language.TR)

Parserexample = Parser(SentenceAnalyzer,ParserFactory.buildEarlyParser(Language.TR.getGrammarFilePath()),ParseTreeValidatorBuilder.build(Language.TR))
#yapılacak_liste = []

string = Str
parsedsentencelist = []
parsedsentencelist1 = []
parsedsentencelist2 = []
#text2 sesli çalıştırmak için text1 'i text2 ye atıyoruz.
text1 = text2
text1 = text1.capitalize()
#eğer ses yerine doğrudan cümle vermek istiyorsak text1 i aşağıdan elle cümleye atıyoruz.
#text1 = "Ahmet kapıyı geç sonra kutuyu al"
is_sirasi=[]
#is_sirasi2 yi texte yazdırmak için kullandık.
is_sirasi2=[]
#Çıktıyı dosyaya yazdırmak için myfile adında dosya oluşturup yazma modunda çalıştırıyoruz.
file1 = open("myfile.txt","a")#append mode 
file1.write('\n')
#zaman bağlacı
if 'sonra' in text1 or 'Sonra' in text1:      
#kullanılan bağlaç
      file1.writelines(text1+'\n')
      print("kullanılan bağlaç : sonra")
      file1.write("kullanılan bağlaç : sonra \n")
      splits = text1.split("sonra")
      print(splits)
      #file1.write(" ".join(splits)+'\n')
      parsedsentencelist1 = Parserexample.parse(splits[0])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("----------")
      #file1.write("----Cümlenin birinci kısmı ------\n")
      for i in range(len(parsedsentencelist1)):
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm: " + str(max(set(maxilist), key = maxilist.count)))
        #file1.write("En çok geçen çözüm: " + str(max(set(maxilist), key = maxilist.count))+'\n')
#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b=x3.split("]")
        
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
        #for kelime in b:
              #file1.write(kelime + '\n')
  #aranankelime="-ve"
        for j in a :                             
              print(j,end=' ')
              #file1.write(''.join(j))
      else:
        print ("-----yok---")
      #file1.write('\n')
      print("-------------")
      splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
      parsedsentencelist2 = Parserexample.parse(splits[1])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      #file1.write("---ikinci kısım---"+'\n')
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))
        #file1.write("En çok geçen çözüm: " + str(max(set(maxilist), key = maxilist.count))+'\n')

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        #x3 text e yazdırmak için kullandık
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
              #file1.write(''.join(j))
      else:
        print ("-----yok---")
      print("-----------------")
      #file1.write("\n")
      print("Cümlenin is sırası")
      file1.write("Cümlenin is sırası"+'\n')
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
            #file1.write(str(i+1)+". yapılacak is"+str(' '.join(is_sirasi[i]).split())+'\n')
      #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')
                        #print(aaa)
                  
                  #file1.write(aaa+'\n')
                  
                  

#zaman bağlacı
elif 'önce' in text1:
      file1.writelines(text1+'\n')
      #is_sirasi=[]
      #kullanılan bağlaç
      print("kullanılan bağlaç : önce")
      file1.write("kullanılan bağlaç : önce \n")
      splitstring=""
      if 'meden' in text1:
            splitliste = text1.split("meden")
            for s in splitliste:
                  splitstring +=s
            text1= splitstring
      elif 'madan' in text1:
            splitliste = text1.split("madan")
            for s in splitliste:
                  splitstring +=s
            text1 = splitstring
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
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b=x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      
      print("-------------")
      
      parsedsentencelist2 = Parserexample.parse(splits[0])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3 +=" "+i
        a = x2.split("]")
        b= x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
        
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      print("-----------------")
      print("Cümlenin is sırası")
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
            #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')
            
#zaman bağlacı      
elif 'ardından' in text1:
      file1.writelines(text1+'\n')
      #is_sirasi=[]
      #kullanılan bağlaç
      print("kullanılan bağlaç : ardından")
      file1.write("kullanılan bağlaç : ardından \n")
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
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      
      print("-------------")
      splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
      parsedsentencelist2 = Parserexample.parse(splits[1])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm: " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      print("-----------------")
      print("Cümlenin is sırası")
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
      #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:       
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')
#zaman bağlacı
elif 'zaman' in text1:
      file1.writelines(text1+'\n')
      #is_sirasi=[]
      #kullanılan bağlaç
      print("kullanılan bağlaç : zaman")
      file1.writelines("kullanılan bağlaç : zaman \n")
      splitstring=""
      if 'diğin' in text1:
            splitliste = text1.split("diğin")
            for s in splitliste:
                  splitstring +=s
            text1= splitstring
      elif 'tığın' in text1:
            splitliste = text1.split("tığın")
            for s in splitliste:
                  splitstring +=s
            text1 = splitstring
      elif 'tiğin' in text1:
            splitliste = text1.split("tiğin")
            for s in splitliste:
                  splitstring +=s
            text1 = splitstring
      splits = text1.split("zaman")
      print(splits)
      parsedsentencelist1 = Parserexample.parse(splits[0])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("----------")
      for i in range(len(parsedsentencelist1)):
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
                  temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)	
                  #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
                  format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
                  maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
		      #if trees.get(j).isValid():

      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      
      print("-------------")
      splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
      parsedsentencelist2 = Parserexample.parse(splits[1])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      print("-----------------")
      print("Cümlenin is sırası")
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
      #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:       
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')

elif 'sonunda' in text1:
      file1.writelines(text1+'\n')
      #is_sirasi=[]
         #kullanılan bağlaç
      print("kullanılan bağlaç : sonunda")
      file1.writelines("kullanılan bağlaç : sonunda \n")
      splits = text1.split("sonunda")
      print(splits)
      parsedsentencelist1 = Parserexample.parse(splits[0])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("----------")
      for i in range(len(parsedsentencelist1)):
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3 +=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      
      print("-------------")
      splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
      parsedsentencelist2 = Parserexample.parse(splits[1])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      print("-----------------")
      print("Cümlenin is sırası")
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
      #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:       
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')

elif 'en son' in text1:
      file1.writelines(text1+'\n')
      #is_sirasi=[]
      print("kullanılan bağlaç : en son")
      file1.writelines("kullanılan bağlaç : en son \n")
      splits = text1.split("en son")
      print(splits)
      parsedsentencelist1 = Parserexample.parse(splits[0])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("----------")
      for i in range(len(parsedsentencelist1)):
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      
      print("-------------")
      splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
      parsedsentencelist2 = Parserexample.parse(splits[1])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      print("-----------------")
      print("Cümlenin is sırası")
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
      #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:       
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')



elif 'gelince' in text1:
      file1.writelines(text1+'\n')
      #text1 = re.sub(r'(\bgelince\b)', r'\1,', text1)
      #is_sirasi=[]
      print("kullanılan kelime : gelince")
      file1.writelines("kullanılan kelime : gelince \n")
      splits = text1.split("ince")
      print(splits)
      parsedsentencelist1 = Parserexample.parse(splits[0])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("----------")
      for i in range(len(parsedsentencelist1)):
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      
      print("-------------")
      splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
      parsedsentencelist2 = Parserexample.parse(splits[1])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      print("-----------------")
      print("Cümlenin is sırası")
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
      #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:       
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')
elif 'yapınca' in text1:
      file1.writelines(text1+'\n')
      #text1 = re.sub(r'(\bgelince\b)', r'\1,', text1)
      print("kullanılan kelime : yapınca")
      file1.writelines("kullanılan kelime : yapınca \n")
      #is_sirasi=[]
      splits = text1.split("ınca")
      print(splits)
      parsedsentencelist1 = Parserexample.parse(splits[0])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan cümle içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("----------")
      for i in range(len(parsedsentencelist1)):
	      #print("Çözüm ",i ," ",parsedsentencelist1.get(i).getSentence().toString())
	      trees = parsedsentencelist1.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      
      print("-------------")
      splits[1] = splits[1].lstrip() #metin basındaki boslugu silmek için lstrip kullandık..
      parsedsentencelist2 = Parserexample.parse(splits[1])
      trees=""
      temp = ""
      maxilist = []
      format1 = ""
#Aşağıdaki kodda ögelerine ayrılan 2. cümle için içerisinden doğru derivasyonlardan en çok geçeni yazdırmak için yazılan kod
      print("---ikinci kısım---")
      for i in range(len(parsedsentencelist2)):
	      #print("Çözüm ",i ," ",parsedsentencelist2.get(i).getSentence().toString())
	      trees = parsedsentencelist2.get(i).getTrees()				
	      for j in range(len(trees)) :
		      if trees.get(j).isValid():
			      temp = ParseSimplifier.simplify(trees.get(j).toString(),ParseDetail.Level_4)			
			      #print("\tParse ",j,ParseFormatter.format(temp, ParseLanguage.Turkish))
			      format1=ParseFormatter.format(temp, ParseLanguage.Turkish)			
			      maxilist.append(format1.replace("Belirtili","").replace("Belirtisiz",""))
      if(len(maxilist)>0):
        res = max(set(maxilist), key = maxilist.count) 
        str1 = str(max(set(maxilist), key = maxilist.count))
      
  #en çok tekrar eden çözüm ve sayısı
        print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
        x = str1.split("[")

        yenix = x
        x2=""
        x3=""
        for i in yenix:
          if i != "S":
            x2+="-"+i
            x3+=" "+i
        a = x2.split("]")
        b = x3.split("]")
        is_sirasi.append(a)
        is_sirasi2.append(b)
        print(a)
  #aranankelime="-ve"
        for j in a :                
              print(j,end=" ")
      else:
        print ("-----yok---")
      print("-----------------")
      print("Cümlenin is sırası")
      for i in range(len(is_sirasi)):
            print(i+1,". yapılacak is",' '.join(is_sirasi[i]).split())
      #text dosyasına istediğimiz formatta yazdırmak için kullandığımız kod kısmı
      for isler in is_sirasi2:       
            file1.write(str(is_sirasi2.index(isler)+1)+".is  \n")
            for iss in isler:
                  if iss != '' :
                        if len(iss)!=2:
                              file1.write(iss+'\n')
      
#eğer cümlede zaman zarfı yoksa çalışıcak kısım            
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
	  print("Çözüm ",i ," ",parsedsentencelist.get(i).getSentence().toString())
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
    print ("En çok geçen çözüm : " + str(max(set(maxilist), key = maxilist.count)))

#parsed tree yi istediğimiz şekilde yazdırmak için köşeli parantezleri sonuçtan çıkarmak için yazılan kodlar
    x = str1.split("[")

    yenix = x
    x2=""
    for i in yenix:
      if i != "S":
        x2+="-"+i

    a = x2.split("]")

    print(a)
  #aranankelime="-ve"
    for j in a :
        
        
          print(j,end=" ")
  else:
    print ("-----yok---")

Cumle_Ogeleri = ["Özne","Yüklem","Nesne","Tümleç","Zarf"]

file1.close()
#Gerekli çıktıyı aldıktan sonra JVM yi kapatıyoruz.
jp.shutdownJVM()

