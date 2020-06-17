package com.hrzafer.fatihparser.util;

import com.hrzafer.fatihparser.*;
import com.hrzafer.fatihparser.analyzer.SentenceAnalyzer;
import com.hrzafer.fatihparser.analyzer.SentenceAnalyzerBuilder;
import com.hrzafer.fatihparser.restriction.ParseTreeValidatorBuilder;
import com.hrzafer.fatihparser.structure.Sentence;
import com.hrzafer.fatihparser.util.TableFileReader;
import edu.osu.ling.pep.EarleyParser;
import edu.osu.ling.pep.Grammar;
import edu.osu.ling.pep.PepException;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class FatihParserTest {
    public static void main(String[] args) throws FileNotFoundException, IOException, PepException {
        SentenceAnalyzer sentenceAnalyzer = SentenceAnalyzerBuilder.build(Language.TR);
        ParserFactory parserFactory = new ParserFactory();
        FatihParser fatihparser = new FatihParser();
        Parser parser = new Parser(sentenceAnalyzer, parserFactory.buildEarlyParser(Language.TR.getGrammarFilePath()), ParseTreeValidatorBuilder.build(Language.TR));
        List<ParsedSentence> parsedSentences = parser.parse("Ali sarı topu at");
        fatihparser.printParsedSentences(parsedSentences);
        //runTest(NonTerminal.S, Language.TR);
        //runTest(NonTerminal.S, Language.TK);

        /*
        String rawSentence = "Zeynep kadına karşı çıkmaya ve çok fazla sigara içmeye başlar";
        List<Sentence> sentences = sentenceAnalyzer.analyze(rawSentence);
        for (Sentence sentence : sentences) {
            System.out.println(sentence);
        }
        */



    }
}
