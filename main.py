import json
import dearpygui.dearpygui as dpg  #Import UI library
from translators.googletrans.gtrans import Gtranslator
from translator_selecter import *
import threading


class App:
    def __init__(self):
        # Define variables
        self.original_language = "English"
        self.translate_language = "Russian"

        self.use_translator = ''

        # Languages and their codes
        language_file = open('./languages/languages.json', 'rb')
        self.languages = json.load(language_file)
        self.lang_select = [x for x in self.languages.keys()]

    # Callback for edit font size
    def get_font_size_callback(self, sender, data):
        ...

    def select_translator(self, sender, data):
        if(check_translator(data) == 0):
            print("ERROR!")
        elif(check_translator(data) == 1):
            print('USE!')

            if(data == "Google"): self.use_translator = Gtranslator()

        elif(check_translator(data) == 2):
            print("API!")

    def run(self):
        # Create Viewport for draw other windows
        dpg.create_context()
        dpg.create_viewport(title="MineTranslator", width=655, height=480)
        dpg.setup_dearpygui()
        # Create main app window
        with dpg.window(tag="Main"):
            # Menu bar
            with dpg.menu_bar():
                with dpg.menu(label="Settings"):
                    dpg.add_slider_int(label='Font scale', min_value=1, max_value=32, callback=self.get_font_size_callback)
                with dpg.menu(label="Translator"): # Select translator base
                    dpg.add_combo(label="Select Translator", items=("Google", "Yandex", "DeepL"), callback=self.select_translator)

            # Window with standard translator
            with dpg.tab_bar():
                with dpg.tab(label="Translate"):
                    translator = TranslatorBase()
                    translator.choose_tab()

        dpg.show_viewport()
        dpg.set_primary_window('Main', True)
        dpg.start_dearpygui()
        dpg.destroy_context()


class TranslatorBase(App):
    def choose_tab(self) -> None:
        with dpg.table(header_row=False) as table:
            dpg.add_table_column(label="Original Language")
            dpg.add_table_column(label="Translate Language")
            with dpg.table_row():
                for i in range(2):
                    dpg.add_combo(default_value="English", items=self.lang_select,
                                  callback=lambda x, y: print(self.languages[y]))
            with dpg.table_row():
                for i in range(2):
                    dpg.add_input_text(multiline=True, tab_input=True, height=300, width=300)
                    

if __name__ == "__main__":
    app = App()
    mainWindow = threading.Thread(target=app.run)
    mainWindow.start()
    mainWindow.join()