import googletrans

class GTranslator:
    def __init__(self):
        self.translator = googletrans.Translator()
        self.translation = ''
        print('GTRANS init')
    def translate(self, base, dest, data) -> str:
        print(base,dest,data)
        translation = self.translator.translate(src=base, dest=dest, text=data)
        translation = translation.text
        return translation

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
