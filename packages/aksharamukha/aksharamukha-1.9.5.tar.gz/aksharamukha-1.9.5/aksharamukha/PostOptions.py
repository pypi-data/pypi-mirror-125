# -*- coding: utf-8 -*-

## Include AnusvaraToNasal for Santali, TolongSikhi, Limbu, Lepcha

## Generate without Short Vowels - Only include for preserver "Source"

from . import PostProcess as PP
from . import GeneralMap as GM

def ApplyScriptDefaults(Strng,Source,Target):
    Options = []

    if Target in GM.IndicScripts:
        Options += []#['RemoveDiacritics'] #Sometimes you may wanna keep it. Adjust options

    if Target == 'Telugu' or Target == 'Kannada':
        Options += ['NasalToAnusvara','MToAnusvara']

    elif Target == 'Hebrew':
        Options += ['HebrewVetVav', 'HebrewnonFinalShort']

    elif Target == 'Malayalam':
        Options += ['MalayalamAnusvaraNasal', 'MToAnusvara', 'MalayalamremoveHistorical']

    elif Target == 'Tamil':
        Options += ['TamilNaToNNa','AnusvaraToNasal', 'TamilpredictDentaNa']

    elif Target == 'Bengali':
        Options += ['VaToBa','YaToYYa']

    elif Target == 'MeeteiMayek':
        Options += ['MeeteiMayekremoveHistorical']

    elif Target == 'Limbu':
        Options += ['LimburemoveHistorical']

    elif Target == 'Assamese':
        Options += ['YaToYYa']

    elif Target == 'Oriya':
        Options += ['OriyaVa','YaToYYa']

    elif Target == 'Chakma':
        Options += ['YaToYYa']

    elif Target == 'Gurmukhi':
        Options += ['GurmukhiCandrabindu', 'GurmukhiTippiBindu','GurmukhiTippiGemination']

    elif Target == 'Saurashtra':
        Options += ['SaurashtraHaru']

    elif Target == 'Ahom':
        Options +=['AhomClosed']

    elif Target == 'Tibetan':
        Options += ['TibetanRemoveVirama', 'TibetanRemoveBa']

    elif Target == "Thaana":
        Options += ['ThaanaRemoveHistorical']

    elif Target == "Avestan":
        Options += ['AvestanConventions']

    elif Target == "Sundanese":
        Options += ['SundaneseRemoveHistoric']

    elif Target == "Multani":
        Options += ['MultaniAbjad']

    elif Target == "Modi":
        Options += ['ModiRemoveLong']

    elif Target == "WarangCiti":
        Options += ['WarangCitiModernOrthogaphy']

    else:
        Options += []

    for Option in Options:
        if Option.find(Target) != -1:
            Strng = getattr(PP,Option)(Strng)
        else:
            Strng = getattr(PP,Option)(Strng,Target)

    return Strng