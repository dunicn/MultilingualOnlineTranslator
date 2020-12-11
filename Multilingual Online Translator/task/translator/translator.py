import requests
from bs4 import BeautifulSoup
import argparse

s = requests.Session()


class MultilingualTranslator:

    def __init__(self):
        self.native_language = ""
        self.language_to_translate_to = ""
        self.word_to_translate = ""
        self.languages_dict = {"1": "arabic", "2": "german", "3": "english", "4": "spanish", "5": "french",
                               "6": "hebrew", "7": "japanese", "8": "dutch", "9": "polish", "10": "portuguese",
                               "11": "romanian", "12": "russian", "13": "turkish"}
        self.translated_words_list = []
        self.translated_examples_list = []

    def translate_to_all_languages(self):
        for elem in range(1, 14):
            if self.languages_dict.get(str(elem)).lower() == self.native_language:
                continue
            self.language_to_translate_to = self.languages_dict.get(str(elem))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            result = s.get(self.url_generator(), headers=headers)
            word_file = open("{}.txt".format(self.word_to_translate.lower()), "a", encoding="utf-8")
            if result.status_code == 200:
                self.translated_words(result)
                self.translated_examples(result)
                word_file.write("{} Translations:".format(self.language_to_translate_to) + "\n")
                word_file.write(self.translated_words_list[1] + "\n \n")
                word_file.writelines("{} Examples:".format(self.language_to_translate_to) + "\n")
                word_file.writelines(self.translated_examples_list[0] + "\n")
                word_file.writelines(self.translated_examples_list[1] + "\n \n")
                word_file.close()
        files = open("{}.txt".format(self.word_to_translate.lower()), "r", encoding="utf8")
        print(files.read())
        files.close()

    def final_all(self, language1, word):
        self.native_language = language1
        self.word_to_translate = word
        if self.native_language not in self.languages_dict.values():
            print("Sorry, the program doesn't support {}".format(self.native_language))
            exit()
        else:
            for elem in range(1, 14):
                if self.languages_dict.get(str(elem)).lower() == self.native_language:
                    continue
                self.language_to_translate_to = self.languages_dict.get(str(elem))
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                result = s.get(self.url_generator(), headers=headers)
                word_file = open("{}.txt".format(self.word_to_translate.lower()), "a", encoding="utf-8")
                if result.status_code == 404:
                    print("Sorry, unable to find {}".format(self.word_to_translate))
                    exit()
                elif result.status_code == 200:
                    self.translated_words(result)
                    self.translated_examples(result)
                    word_file.write("{} Translations:".format(self.language_to_translate_to) + "\n")
                    word_file.write(self.translated_words_list[1] + "\n \n")
                    word_file.writelines("{} Examples:".format(self.language_to_translate_to) + "\n")
                    word_file.writelines(self.translated_examples_list[0] + "\n")
                    word_file.writelines(self.translated_examples_list[1] + "\n \n")
                    word_file.close()
                else:
                    print("Something wrong with your internet connection")

            files = open("{}.txt".format(self.word_to_translate.lower()), "r", encoding="utf8")
            print(files.read())
            files.close()

    def final_main(self, language1, language2, word):
        self.native_language = language1
        self.language_to_translate_to = language2
        if self.native_language not in self.languages_dict.values():
            print("Sorry, the program doesn't support {}".format(self.native_language))
            exit()
        elif self.language_to_translate_to not in self.languages_dict.values():
            print("Sorry, the program doesn't support {}".format(self.language_to_translate_to))
            exit()
        else:

            self.word_to_translate = word
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            result = s.get(self.url_generator(), headers=headers)
            word_file = open("{}.txt".format(self.word_to_translate.lower()), "a", encoding="utf-8")
            if result.status_code == 404:
                print("Sorry, unable to find {}".format(self.word_to_translate))
                exit()
            elif result.status_code == 200:
                word_file.write("{} Translations:".format(self.language_to_translate_to) + "\n")
                self.translated_words(result)
                self.translated_examples(result)
                for x in range(1, 6):
                    if x >= len(self.translated_words_list):
                        break
                    word_file.write(self.translated_words_list[x] + "\n")
                word_file.write("\n")
                word_file.write("{} Examples:".format(self.language_to_translate_to) + "\n")
                for x in range(0, 10, 2):
                    for j in self.translated_examples_list[x:x + 2]:
                        word_file.write(j + "\n")
                    word_file.write("\n")
                word_file.close()
            else:
                print("Something wrong with your internet connection")
                exit()
            files = open("{}.txt".format(self.word_to_translate.lower()), "r", encoding="utf8")
            print(files.read())
            files.close()

    def translated_words(self, result):
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        words = soup.find_all("a", {"class": "translation"})
        self.translated_words_list = [i.text.strip().replace("[", "").replace("]", "") for i in words]

    def translated_examples(self, result):
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        phrases = soup.select('#examples-content span.text')
        self.translated_examples_list = [i.text.strip().replace("[", "").replace("]", "") for i in phrases]

    def url_generator(self):
        web_page = "https://context.reverso.net/translation/"
        url = web_page + self.native_language.lower() + "-" \
              + self.language_to_translate_to.lower() + "/" + self.word_to_translate
        return url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translates words")
    languages = ["arabic", "german", "english", "spanish", "french",
                 "hebrew", "japanese", "dutch", "polish", "portuguese",
                 "romanian", "russian", "turkish"]
    parser.add_argument("l1")
    parser.add_argument("l2")
    parser.add_argument("word")
    args = parser.parse_args()

    if args.l2 == "all":
        test = MultilingualTranslator()
        test.final_all(args.l1, args.word)
    else:
        test = MultilingualTranslator()
        test.final_main(args.l1, args.l2, args.word)
