import googletrans

class GTranslator:
    def __init__(self):
        self.translator = googletrans.Translator()
        self.translation = ''

    def translate(self, base, dest, data) -> str:
        translation = self.translator.translate(src=base, dest=dest, text=data)
        translation = translation.text
        return translation

    def define_language(self, text) -> str:
        detect_language = self.translator.detect(text=text).lang
        return  detect_language

    @property
    def get_translation(self) -> str:
        return self.translation
    @property
    def get_info(self) -> str:
        return 'Google translator'


if __name__ == "__main__":
    g = GTranslator()
    while True:
        string = input('> ')
        print(g.translate(base='en', dest='ru', data=string))
