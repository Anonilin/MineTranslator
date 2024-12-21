import json
import os
import dearpygui.dearpygui as dpg  #Import UI library

from translators.gtrans import GTranslator
from translator_selecter import *
import threading

class App:
    def __init__(self):
        # Define variables
        self.translator = GTranslator()
        # Languages and their codes
        language_file = open('languages.json', 'rb')
        self.languages = json.load(language_file)
        self.lang_select = [x for x in self.languages.keys()]
        self.fonts = list()

    # Callback for edit font size
    def get_font_size_callback(self, sender, data):
        ...

    def select_translator(self, sender, data):
        if(check_translator(data) == 0):
            print("ERROR!")
        elif(check_translator(data) == 1):
            if(data == "Google"):
                self.translator = GTranslator()
        elif(check_translator(data) == 2):
            print("API!")

    def run(self):
        # Create Viewport for draw other windows
        dpg.create_context()

        with dpg.font_registry():
            with dpg.font(file=r'fonts/ubuntu.ttf', size=14, tag='font1') as font1:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        dpg.show_metrics()

        dpg.create_viewport(title="MineTranslator", width=655, height=480, resizable=False)
        dpg.setup_dearpygui()

        # Create main app window
        with dpg.window(tag="Main"):
            # Menu bar
            with dpg.menu_bar():
                with dpg.menu(label="Settings"):
                    dpg.add_slider_int(label='Font scale', min_value=1, max_value=32, callback=self.get_font_size_callback)
                    dpg.add_checkbox(label='Always on top', callback=lambda s,e: dpg.set_viewport_always_top(e))
                with dpg.menu(label="Translator"): # Select translator base
                    dpg.add_combo(label="Select Translator", items=("Google", "Yandex", "DeepL"), default_value="Google", callback=self.select_translator)

            # Window with standard translator
            # with dpg.child_window(label='Translator', pos=(0,10), width=640, height=400):
            with dpg.tab_bar():
                with dpg.tab(label="Translator"):
                    translator = TranslatorBase()

                    translator_thread = threading.Thread(target=translator.choose_tab)
                    translator_thread.start()
                    translator_thread.join()

        dpg.show_viewport()
        dpg.set_primary_window('Main', True)
        dpg.start_dearpygui()
        dpg.destroy_context()

class TranslatorBase(App):

    def key_handler(self):
        with dpg.handler_registry(show=True, tag='take_enter'):
            enter_relase = dpg.add_key_release_handler(key=dpg.mvKey_Return, callback=lambda s,e: self.send_data(s,e))

    def detect_language(self, text):
        language = self.translator.define_language(text)
        for key, value in self.languages.items():
            if value == language:
                dpg.set_value(item='input_combo', value=key)
                return

    def send_data(self, sender, event):
        print(self.translator.get_info)
        value = dpg.get_value(item='input_txt')
        if(len(value) <= 1):
            dpg.set_value(item='output_txt', value='')
            return
        translate = self.translator.translate(base=self.languages[dpg.get_value('input_combo')], dest=self.languages[dpg.get_value('output_combo')], data=value)

        detect_lang_thread = threading.Thread(target=self.detect_language(value))
        detect_lang_thread.start()
        detect_lang_thread.join()

        dpg.set_value('output_txt', value=translate)

    def choose_tab(self) -> None:
        with dpg.table(header_row=False) as table:
            dpg.add_table_column(label="Original Language")
            dpg.add_table_column(label="Translate Language")
            with dpg.table_row():
### ОТРИСОВКА COMBO ДЛЯ ВЫБОРА ЯЗЫКА ###
                for i in ['input_combo', 'output_combo']:
                    self.combo_language = dpg.add_combo(default_value="English", items=self.lang_select, tag=i,
                                                        callback=lambda s,v: dpg.set_value(item=s, value=v))
### ОТРИСОВКА ТЕКСТОВЫХ ПОЛЕЙ ###
            with dpg.table_row():
                for i in ['input_txt', 'output_txt']:
                    self.input_text = dpg.add_input_text(multiline=True, tab_input=True, tag=i, height=300, width=300)
                    dpg.bind_item_font(dpg.last_item(), 'font1')  # Change font for text area widget
### КНОПКИ ДЛЯ ОКОН НАСТРОЕК ###
            with dpg.table_row():
                self.option_button = dpg.add_button(label='Options', tag='text_area_option')

            with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag='modal_textarea_option'):
                dpg.add_text('Options for text areas')


        key_handler_thread = threading.Thread(target=self.key_handler)

        key_handler_thread.start()
        key_handler_thread.join()

if __name__ == "__main__":
    app = App()
    main_thread = threading.Thread(target=app.run)
    main_thread.start()
    main_thread.join()