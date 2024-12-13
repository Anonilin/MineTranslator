import googletrans

class Gtranslator:
    def __init__(self):
        self.translator = googletrans.Translator()

    def translate(self, text, base, dest) -> str:
        self.translation = self.translator.translate(text=text, src=base, dest=dest)

        return self.translation.text