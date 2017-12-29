from googletrans import Translator
import time


class Translate:
    def __init__(self, src='en', target='zh-cn'):
        self.translator = Translator()
        self.src = src
        self.trg = target

    def translate(self, sentence, max_try=3, count=0):
        # text is string
        if count >= 3:
            return ''
        try:
            translation = self.translator.translate(sentence, dest=self.trg, src=self.src)
        except:
            time.sleep(5)
            translation = self.translate(sentence, max_try, count=count + 1)
        finally:
            time.sleep(0.1)

        return translation

    def translate_batch(self, sentences, max_try=3, count=0):
        # sentences is list
        if count >= max_try:
            return []
        try:
            translations = self.translator.translate(sentences, dest=self.trg, src=self.src)
        except:
            time.sleep(5)
            translations = self.translate_batch(sentences, max_try, count=count + 1)
        finally:
            time.sleep(0.5)

        results = []
        for translation in translations:
            translation = translation.text
            results.append(translation)

        return results
