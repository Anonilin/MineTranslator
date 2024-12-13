from config import *
import json

file = json.load(CFG)['translator_list']

def check_translator(translator_title:str) -> int:
    """Codes:
        0 - Error;
        1 - Work;
        2 - Need API;
    """
    if(file[translator_title] == "Free"):
        return 1
    elif(file[translator_title] == "API"):
        return 2
    elif(file[translator_title] != "API"):
        return 1
    else:
        return 0