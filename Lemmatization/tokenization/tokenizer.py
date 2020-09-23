#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Deepak Paudel"
__copyright__ = "Copyright 2019"

import re
from Lemmatization.utility.reader import get_suffixes


class NepaliTextTokenizer(object):
    """Base class for all tokenizer"""

    def __init__(self):
        pass

    @staticmethod
    def sentence_tokenize(text):
        """
        :param text: text to split into sentences --> str
        :return: tokenized sentences from the text --> list
        """
        return re.split('(?<=[।?!]) +', text)

    @staticmethod
    def word_tokenize(text):
        """
        Tokenize sentence into words
        :param text: sentence to split into words
        :return: non-ascii array of words
        """
        colon_lexicon = ['अंशत:', 'मूलत:', 'सर्वत:', 'प्रथमत:', 'सम्भवत:', 'सामान्यत:', 'विशेषत:', 'प्रत्यक्षत:',
                         'मुख्यत:', 'स्वरुपत:', 'अन्तत:', 'पूर्णत:', 'फलत:', 'क्रमश:', 'अक्षरश:', 'प्रायश:',
                         'कोटिश:', 'शतश:', 'शब्दश:']

        # Handling punctuations: , " ' ) ( { } [ ] ! ‘ ’ “ ” :- ? । / —
        text = re.sub(r'\,|\"|\'| \)|\(|\)| \{| \}| \[| \]|!|‘|’|“|”| \:-|\?|।|/|\—', ' ', text)
        words_original = text.split()

        words = []
        for word in words_original:
            if word[len(word) - 1:] == '-':
                if not word == '-':
                    words.append(word[:len(word) - 1])
            else:
                if word[len(word) - 1:] == ':' and word not in colon_lexicon:
                    words.append(word[:len(word) - 1])
                else:
                    words.append(word)

        return words

    @staticmethod
    def word_minute_tokenize(words):
        suffixes = get_suffixes()
        new_words = list()
        for word in words:
            for suffix in suffixes:
                if word.endswith(suffix):
                    new_words.remove(word)
                    n_words = word.split(suffix)
                    new_words.extend(n_words)


if __name__ == "__main__":
    tokenizer = NepaliTextTokenizer()
    text1 = "मत्स्य एवं अग्नि पुराण अनुसार ब्रह्माजीले सृष्टि रचना गर्ने विचार गरेपछि सबभन्दा पहिला संकल्पको " \
            "माध्यमले मानसपुत्रको रचना गरे । उनीहरूमध्येका एक " \
            "मानसपुत्र ऋषि अत्रिको विवाह ऋषि कर्दमकी कन्या अनसूयासँग भएको हो । " \
            "उनीहरूबाट दुर्वासा, दत्तात्रेय र सोम तीन पुत्र उत्पन्न भए । सोम चन्द्रमाकै " \
            "अर्को नाम हो । पद्मपुराणमा चन्द्रको जन्मको अर्को वृत्तान्त पाइन्छ । ब्रह्माले आफ्नो मानसपुत्र " \
            "अत्रिलाई सृष्टि विस्तार गर्ने आज्ञा दिनुभयो । " \
            "यसका लागि महर्षि अत्रिले अनुत्तर नामक तप आरम्भ गर्नुभयो । तपस्याकालमा एक दिन महर्षिका नेत्रबाट " \
            "जलका केही थोपा चुहिए । " \
            "ती थोपा अत्यन्त चम्किला थिए । दिशाहरूले स्त्रीरूप धरेर पत्रप्राप्तिको कामना गर्दै ती थोपा पिए जुन " \
            "नीहरूको पेटमा गर्भ रूपमा स्थापित भयो । तर त्यस चम्किलो गर्भलाई दिशाहरूले" \
            " राखिरहन सकेनन् र त्यागिदिए । त्यही त्यागिएको गर्भलाई ब्रह्माले पुरुष रूप दिए जो चन्द्रमाको रूपमा " \
            "प्रख्यात भयो । देवताहरू, ऋषिहरू र गन्धर्वहरूले" \
            " उनको स्तुति गरे । उनकै तेजबाट पृथिवीमा दिव्य औषधि उत्पन्न भए । ब्रह्माजीले चन्द्रमालाई नक्षत्र, " \
            "वनस्पति, ब्राह्मण र तपको स्वामी नियुक्त गरे । " \
            "स्कन्द पुराणका अनुसार देवता तथा दैत्यहरूले क्षीरसागर मन्थन गरेपछि त्यहाँबाट चौध रत्न निस्केका थिए । " \
            "चन्द्रमा तिनै चौध रत्नमध्ये एक हुन् जसलाई" \
            " लोककल्याणका लागि मन्थनबाट प्राप्त कालकूट विष पिउने भगवान् शंकरले आफ्नो शिरमा राख्नुभएको छ । " \
            "चन्द्रमाको विवाह दक्षप्रजापतिका छोरीहरू २७ " \
            "नक्षत्रसँग भएको थियो । सत्ताईस नक्षत्रको भोगबाट एक चन्द्रमास पूर्ण हुन्छ ।"

    sentences = tokenizer.sentence_tokenize(text1)
    print(sentences)
    word_list = list()
    for sentence in sentences:
        word_list.append(tokenizer.word_tokenize(sentence))
    print(word_list)
