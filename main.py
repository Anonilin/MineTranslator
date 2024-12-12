import dearpygui.dearpygui as dpg  #Import UI library
from numpy.core.multiarray import item

from translator_selecter import *

# Define variables
original_language = "English"
translate_language = "Russian"

# Create Viewport for draw other windows
dpg.create_context()
dpg.create_viewport(title="MineTranslator", width=655, height=480)
dpg.setup_dearpygui()
# Callback for edit font size
def get_font_size_callback(sender, data):
    ...

def select_translator(sender, data):
    if(check_translator(data) == 0):
        print("ERROR!")
    elif(check_translator(data) == 1):
        print('USE!')
    elif(check_translator(data) == 2):
        print("API!")

# Create main app window
with dpg.window(tag="Main"):
    # Menu bar
    with dpg.viewport_menu_bar():
        with dpg.menu(label="Settings"):
            dpg.add_slider_int(label='Font scale', min_value=1, max_value=32, callback=get_font_size_callback)
        with dpg.menu(label="Translator"): # Select translator base
            dpg.add_combo(label="Select Translator", items=("Google", "Yandex", "DeepL"), callback=select_translator)

    # Window with standard translator
    # with dpg.child_window(label='Translator', pos=(0,10), width=640, height=400):
    dpg.add_text("Translator")
    with dpg.table(header_row=False) as table:
        dpg.add_table_column(label="Original Language")
        dpg.add_table_column(label="Translate Language")
        with dpg.table_row():
            for i in range(2):
                dpg.add_combo(label="Choose language", default_value="English")
        with dpg.table_row():
            for i in range(2):
                dpg.add_input_text(multiline=True, tab_input=True, height=300)

dpg.show_viewport()
dpg.set_primary_window('Main', True)
dpg.start_dearpygui()
dpg.destroy_context()