from aksharamukha import GeneralMap
import re
from . import Convert,PostOptions,PostProcess,PreProcess
from . import ConvertFix
import json
import requests
import html
import itertools
from collections import Counter
import unicodedata
import io
import collections
import yaml
import warnings
import langcodes
from inspect import getmembers, isfunction


def removeA(a):
    if a.count('a') == 1:
        return a.replace('a', '')

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def auto_detect(text, plugin = False):
    scripts = []

    for uchar in text:
        try:
            scripts.append(unicodedata.name(uchar).split(' ')[0].lower())
        except ValueError:
            pass
            # print('Script not found')

    counts = Counter(scripts)
    script_percent = []

    for script, count  in counts.items():
        percent = count/len(scripts) * 100
        script_percent.append((percent, script))

    #print(sorted(script_percent))

    if not plugin:
        if len(script_percent) > 0:
            script = sorted(script_percent)[-1][1]
        else:
            script = ''
    else:
        #print('here')
        if len(script_percent) > 0:
            if sorted(script_percent)[-1][1] == 'latin':
                script = sorted(script_percent)[-2][1]
            else:
                script = sorted(script_percent)[-1][1]
        else:
            script = ''

    #print('the script is')
    #print(script)
    inputScript = script[0].upper() + script[1:]

    laoPali = ['ຆ', 'ຉ', 'ຌ', 'ຎ', 'ຏ', 'ຐ', 'ຑ', 'ຒ', 'ຓ', 'ຘ', 'ຠ', 'ຨ', 'ຩ', 'ຬ', '຺']

    if inputScript == 'Bengali':
        if 'ৰ' in text or 'ৱ' in text:
            inputScript = 'Assamese'
    elif inputScript == 'Lao':
        if any(char in text for char in laoPali):
            inputScript = 'LaoPali'
    elif inputScript == 'Batak':
        inputScript = 'BatakKaro'
    elif inputScript == 'Myanmar':
        inputScript = 'Burmese'

        mon = ['ၚ', 'ၛ', '္ည', 'ၞ', 'ၟ', 'ၠ', 'ဳ', 'ဨ']
        if any([char in text for char in mon]):
            inputScript = 'Mon'

        countSub = {'Shan': 0, 'TaiLaing': 0, 'KhamtiShan': 0}

        text = text.replace('ႃ', '')

        for uchar in text:
            try:
                char = unicodedata.name(uchar).lower()
            except:
                pass
            if 'shan' in char:
                countSub['Shan'] += 1
            elif 'tai laing' in char:
                countSub['TaiLaing'] += 1
            elif 'khamti' in char:
                countSub['KhamtiShan'] += 1

        import operator
        sorted_x = sorted(countSub.items(), key=operator.itemgetter(1))

        if countSub['Shan'] > 0 or countSub['TaiLaing'] > 0 or countSub['KhamtiShan'] > 0:
            inputScript = sorted_x[-1][0]


        #shan = ['ႃ', '\u1086', '\u1084', 'ၵ', 'ၶ', 'ၷ', 'ꧠ', 'ၸ', 'ꧡ', 'ꩡ', 'ꧢ', 'ၺ', 'ꩦ', 'ꩧ', 'ꩨ', 'ꩩ', 'ꧣ', 'ၻ', 'ꩪ', 'ၼ','ၽ', 'ꧤ', 'ႁ', 'ꩮ', 'ၹ', 'ၾ']
        #if any([char in text for char in shan]):
            #inputScript = 'Shan'

    elif inputScript == 'Meetei':
        inputScript = 'MeeteiMayek'
    elif inputScript == 'Old':
        inputScript = 'OldPersian'
    elif inputScript == 'Phags-pa':
        inputScript = 'PhagsPa'
    elif inputScript == 'Ol':
        inputScript = 'Santali'
    elif inputScript == 'Sora':
        inputScript = 'SoraSompeng'
    elif inputScript == 'Syloti':
        inputScript = 'SylotiNagri'
    elif inputScript == 'Tai':
        inputScript = 'TaiTham'
    elif inputScript == 'Warang':
        inputScript = 'WarangCiti'
    elif inputScript == 'Siddham':
        preOptions = 'siddhamUnicode'
    elif inputScript == 'Cyrillic':
        inputScript = 'RussianCyrillic'
    elif inputScript == 'Zanabazar':
        inputScript = 'ZanabazarSquare'
    elif inputScript == 'Arabic':
        inputScript = 'Urdu'
        shahmukh_char = 'ݨ لؕ مھ نھ یھ رھ لھ وھ'.split(" ")
        if any(char in text for char in shahmukh_char):
            inputScript = 'Shahmukhi'
    elif inputScript == 'Latin':
        diacritics = ['ā', 'ī', 'ū', 'ṃ', 'ḥ', 'ś', 'ṣ', 'ṇ', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'ḻ', 'ṉ', 'ṟ', 'ṭ', 'ḍ', 'ṅ', 'ñ']
        Itrans = ['R^i', 'R^I', 'L^i', 'L^I', '.N', '~N', '~n', 'Ch', 'sh', 'Sh']
        if 'ʰ' in text:
            inputScript = 'Titus'
        elif any(char in text for char in diacritics):
            if 'ē' in text or 'ō' in text or 'r̥' in text:
                inputScript = 'ISO'
            else:
                inputScript = 'IAST'
        elif any(char in text for char in Itrans):
            inputScript = 'Itrans'
        else:
            inputScript = 'HK'

    return inputScript

# Cross check with inded convert() funciton within autodetect
# scripts available here must be added there
def detect_preoptions(text, inputScript):
    preoptions = []
    if inputScript == 'Thai':
        textNew = text.replace('ห์', '')
        if '\u035C' in text or '\u0325' in text or 'งํ' in text or '\u0E47' in text:
            preoptions = ['ThaiPhonetic']
        elif '์' in textNew and ('ะ' in text):
            preoptions = ['ThaiSajjhayawithA']
        elif '์' in textNew:
            preoptions = ['ThaiSajjhayaOrthography']
        elif 'ะ' in text or 'ั' in text:
            preoptions =  ['ThaiOrthography']
    elif inputScript == 'Lao' or inputScript == 'LaoPali':
        textNew = text.replace('ຫ໌', '')
        if '໌' in textNew and ('ະ' in text):
            preoptions = ['LaoSajhayaOrthographywithA']
        elif '໌' in textNew:
            preoptions = ['LaoSajhayaOrthography']
        elif 'ະ' in text or 'ັ' in text:
            preoptions = ['LaoTranscription']
    elif inputScript == 'Urdu':
            preoptions = ['UrduShortNotShown']

    return preoptions

def convert(src, tgt, txt, nativize, preoptions, postoptions):
    tgtOld = ""

    if src == "Itrans" and '##' in txt:
        textNew = [[i,word] for i, word in enumerate(txt.split("##")) if (i%2 == 0)]
        textRest = [(i,word) for i, word in enumerate(txt.split("##")) if (i%2 == 1)]

        txt = json.dumps(textNew).replace("\\n", "\n")

    if tgt == "" or tgt == "Ignore":
        return txt
    if preoptions == [] and postoptions == [] and nativize == False and src == tgt:
        return txt

    if src == tgt and (src != 'Hiragana' and src != 'Katakana'):
        tgtOld = tgt
        tgt = "Devanagari"

    txt = PreProcess.PreProcess(txt,src,tgt)

    if 'siddhammukta' in postoptions and tgt == 'Siddham':
        tgt = 'SiddhamDevanagari'
    if 'siddhamap' in postoptions and tgt == 'Siddham':
        tgt = 'SiddhamDevanagari'
    if 'siddhammukta' in preoptions and src == 'Siddham':
        src = 'SiddhamDevanagari'
    if 'LaoNative' in postoptions and tgt == 'Lao':
        tgt = 'Lao2'
    if 'egrantamil' in preoptions and src == 'Grantha':
        src = 'GranthaGrantamil'
    if 'egrantamil' in postoptions and tgt == 'Grantha':
        tgt = 'GranthaGrantamil'
    if 'nepaldevafont' in postoptions and tgt == 'Newa':
        tgt = 'Devanagari'
    if 'ranjanalantsa' in postoptions and tgt == 'Ranjana':
        tgt = 'Tibetan'
        nativize = False
    if 'ranjanawartu' in postoptions and tgt == 'Ranjana':
        tgt = 'Tibetan'
        nativize = False
    if 'SoyomboFinals' in postoptions and tgt == 'Soyombo':
        txt = '\u02BE' + txt

    for options in preoptions:
      txt = getattr(PreProcess, options)(txt)

    srcOld = ""

    if src == 'Hiragana' or src == 'Katakana':
        txt = PreProcess.JapanesePreProcess(src, txt, preoptions)
        srcOld = 'Japanese'
        src = 'ISO'

    if tgt == 'Hiragana' or tgt == 'Katakana':
        txt = PostProcess.JapanesePostProcess(src, tgt, txt, nativize, postoptions)

    if src == "Oriya" and tgt == "IPA":
        txt = ConvertFix.OriyaIPAFixPre(txt)

    if src == "Itrans" and '##' in txt:
        #print('I am here tyring to do things')
        transliteration = ''
        for i, word in enumerate(txt.split("##")):
            if (i%2 == 0):
                transliteration += Convert.convertScript(word, src, tgt)
            else:
                transliteration += word
    else:
        transliteration = Convert.convertScript(txt, src, tgt)

    if srcOld == 'Japanese' and tgt != 'Devanagari' and 'siddhammukta' not in postoptions:
        transliteration = Convert.convertScript(transliteration, "Devanagari", "ISO")

    if src == tgtOld:
        tgt = tgtOld
        transliteration = Convert.convertScript(transliteration, "Devanagari", tgt)

    if nativize:
      transliteration =  PostOptions.ApplyScriptDefaults(transliteration, src, tgt)
      if tgt != 'Tamil':
        transliteration = PostProcess.RemoveDiacritics(transliteration)
      else:
        transliteration = PostProcess.RemoveDiacriticsTamil(transliteration)

    if 'RemoveDiacritics' in postoptions:
      if tgt == 'Tamil':
        postoptions = map(lambda x: 'RemoveDiacriticsTamil' if x == 'RemoveDiacritics' else x, postoptions)

    for options in postoptions:
      transliteration = getattr(PostProcess, options)(transliteration)

    if src == "Tamil" and tgt == "IPA":
        r = requests.get("http://anunaadam.appspot.com/api?text=" + txt + "&method=2")
        r.encoding = r.apparent_encoding
        transliteration = r.text

    if src == "Oriya" and tgt == "IPA":
        transliteration = ConvertFix.OriyaIPAFix(transliteration)

    if src == "Itrans" and '##' in txt:
        textConv = {**dict(list(json.loads(transliteration.replace("\n", "\\n")))), ** dict(textRest)}
        textConv = collections.OrderedDict(sorted(textConv.items()))
        transliteration = "".join(textConv.values())

    return transliteration

def process(src, tgt, txt, nativize = True, post_options = [], pre_options = [], param="default"):
    if param == "default":
        return process_default(src, tgt, txt, nativize, post_options, pre_options)

    if param == "script_code":
        return process_script_tag(src, tgt, txt, nativize, post_options, pre_options)

    if param == "lang_code":
        return process_lang_tag(src, tgt, txt, nativize, post_options, pre_options)

    if param == "lang_name":
        return process_lang_name(src, tgt, txt, nativize, post_options, pre_options)

def convert_default(src, tgt, txt, nativize = True, post_options = [], pre_options = []):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/yaml/aksharamukha-scripts.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    scriptList = GeneralMap.IndicScripts + GeneralMap.LatinScripts

    preOptionList = list(map(lambda x: x[0], getmembers(PreProcess, isfunction)))
    preOptionListLower = list(map(lambda x: x.lower(), preOptionList))

    postOptionList = list(map(lambda x: x[0], getmembers(PostProcess, isfunction)))
    postOptionListLower = list(map(lambda x: x.lower(), postOptionList))

    post_options = [option_id for option in post_options for option_id in postOptionList if option.lower() == option_id.lower()]
    pre_options = [option_id for option in pre_options for option_id in preOptionList if option.lower() == option_id.lower()]

    # font hack warning
    font_hack_warning = tgt + ' uses an hacked font to display the script. In the absence of this font, you text may appear different. \n See: https://aksharamukha.appspot.com/describe/' + tgt + ' for the font used'

    if tgt in data_loaded and 'font_hack' in data_loaded[tgt]:
        warnings.warn(font_hack_warning)

    if src not in scriptList:
        script_not_found = 'Source script: ' + src + ' not found in the list of scripts supported. The text will not be transliterated.'
        warnings.warn(script_not_found)

    if tgt not in scriptList:
        script_not_found = 'Target script: ' + tgt + ' not found in the list of scripts supported. The text will not be transliterated.'
        warnings.warn(script_not_found)

    return convert(src, tgt, txt, nativize, pre_options, post_options)

def process_default(src, tgt, txt, nativize, post_options, pre_options):
    scriptList = GeneralMap.IndicScripts + GeneralMap.LatinScripts
    scriptListLower = list(map(lambda x: x.lower(), scriptList))

    if src == 'autodetect':
        src = auto_detect(txt)
        pre_options = detect_preoptions(txt, src)
    elif src.lower() in scriptListLower:
        src = [script_id for script_id in scriptList if src.lower() == script_id.lower()][0]

    if tgt.lower() in scriptListLower:
        tgt = [script_id for script_id in scriptList if tgt.lower() == script_id.lower()][0]

    return convert_default(src, tgt, txt, nativize, post_options, pre_options)


def process_script_tag(src_tag, tgt_tag, txt, nativize, post_options, pre_options):
    # Read YAML file
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + "/yaml/aksharamukha-scripts.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    with open(dir_path + "/yaml/wikitra2-data.yaml", 'r', encoding='utf8') as stream:
        data_loaded_wiki = yaml.safe_load(stream)

    src = []
    tgt = []

    # loop through yaml to find match
    for scrpt in data_loaded.keys():
        scrpt_tag = data_loaded[scrpt]['script']

        # get the popuation of each language of the script
        if 'lang' in data_loaded[scrpt].keys():
            lang_tag = data_loaded[scrpt]['lang'].split(',')[0]
            lang = list(map(lambda x: x.lower(), data_loaded[scrpt]['lang'].split(',')))
        else:
            population = 0
            lang = ''

        if scrpt_tag in data_loaded_wiki.keys() and lang_tag in data_loaded_wiki[scrpt_tag].keys():
            population = data_loaded_wiki[scrpt_tag][lang_tag]['population']
        else:
            population = 0

        # find the match in the file
        if '-' not in src_tag and data_loaded[scrpt]['script'].lower() == src_tag.lower():
            src.append((population, scrpt))

        if '-' not in tgt_tag and data_loaded[scrpt]['script'].lower() == tgt_tag.lower():
            tgt.append((population, scrpt))

        # if hypthenated find the exact match
        if '-' in tgt_tag:
            lang_part = tgt_tag.split('-')[0].lower()
            script_part = tgt_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part.lower() and 'lang' in data_loaded[scrpt].keys() and lang_part.lower() in lang:
                tgt.append((0, scrpt))

        if '-' in src_tag:
            lang_part = src_tag.split('-')[0].lower()
            script_part = src_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part.lower() and 'lang' in data_loaded[scrpt].keys() and lang_part.lower() in lang:
                src.append((0, scrpt))

    if src_tag.lower() in ['latn', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. la-IAST or la-HK to select a particular scheme"
        warnings.warn(warn)

        src = [(0, 'ISO')]

    if tgt_tag.lower() in ['latn', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. la-IAST or la-HK to select a particular scheme"
        warnings.warn(warn)

        tgt = [(0, 'ISO')]

    # if latin ignore la and get the following part
    if '-' in src_tag and src_tag.split('-')[0].lower() in ['latn', 'en', 'eng']:
        src = [(0, src_tag.split('-')[1])]

    if '-' in tgt_tag and tgt_tag.split('-')[0].lower() in ['latn', 'en', 'eng']:
        tgt = [(0, tgt_tag.split('-')[1])]

    if src_tag == 'autodetect':
        src = [(0, auto_detect(txt))]
        pre_options = detect_preoptions(txt, src)

    if len(src) > 0:
        src_pop = sorted(src, reverse=True)[0][1]
    else:
        raise Exception('Source script code: ' + src_tag + ' not found')

    if len(tgt) > 0:
        tgt_pop = sorted(tgt, reverse=True)[0][1]
    else:
        raise Exception('Target script code: ' + tgt_tag + ' not found')

    if len(src) > 1:
        warn = "Multiple orthographies, " + ','.join(map(lambda x: x[1], src)) + ", are associated with the input script. The most popular '" + src_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. ur-Arab or pa-Arab to select a particular orthography"

        warnings.warn(warn)
    if len(tgt) > 1:
        warn = "Multiple orthographies: " + ', '.join(map(lambda x: x[1], tgt)) + " are associated with the target script. The most popular '" + tgt_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. ur-Arab or pa-Arab to select a particular orthography"
        warnings.warn(warn)

    return process_default(src_pop, tgt_pop, txt, nativize, post_options, pre_options)

def process_lang_tag(src_tag, tgt_tag, txt, nativize, post_options, pre_options):
    # Read YAML file
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + "/yaml/aksharamukha-scripts.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    with open(dir_path + "/yaml/wikitra2-data.yaml", 'r', encoding='utf8') as stream:
        data_loaded_wiki = yaml.safe_load(stream)

    src = []
    tgt = []

    # iterate through the yaml file
    for scrpt in data_loaded.keys():
        if 'lang' in data_loaded[scrpt].keys():
            lang = list(map(lambda x: x.lower(), data_loaded[scrpt]['lang'].split(',')))
        else:
            lang = ''

        scrpt_tag = data_loaded[scrpt]['script']

        # try to get the popular script from wiktionary file
        if scrpt_tag in data_loaded_wiki.keys():
            script_count = len(data_loaded_wiki[scrpt_tag])
        else:
            script_count = 1

        # trying to find the match in the yaml file
        if src_tag.lower() in lang:
            src.append((script_count, scrpt))

        if tgt_tag.lower() in lang:
            tgt.append((script_count, scrpt))

        if '-' in tgt_tag:
            lang_part = tgt_tag.split('-')[0].lower()
            script_part = tgt_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part and lang_part in lang:
                tgt.append((0, scrpt))

        if '-' in src_tag:
            lang_part = src_tag.split('-')[0].lower()
            script_part = src_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part and lang_part in lang:
                src.append((0, scrpt))

    if src_tag.lower() in ['sa','san', 'pi', 'pli']:
        warn = "The input language: " + src_tag + " is script-agnostic and can be written in multiple scripts. The most popular 'Devanagari' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. sa-Gran or sa-Sidd to select a particular script"
        warnings.warn(warn)

        src = [(0, 'Devanagari')]

    if tgt_tag.lower() in ['sa','san', 'pi', 'pli']:
        warn = "The ouptput language: " + tgt_tag + " is script-agnostic and can be written in multiple scripts. The most popular 'Devanagari' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. sa-Gran or sa-Sidd to select a particular script"
        warnings.warn(warn)

        tgt = [(0, 'Devanagari')]

    # if sa-deva ignore sanskrita and only get deva
    if '-' in src_tag and src_tag.split('-')[0].lower() in ['sa','san', 'pi', 'pli']:
        for scrpt in data_loaded.keys():
            scrpt_tag = data_loaded[scrpt]['script']

            if scrpt_tag.lower() == src_tag.split('-')[1].lower():
                src = [(0, scrpt)]

    if '-' in tgt_tag and tgt_tag.split('-')[0].lower() in ['sa','san', 'pi', 'pli']:
        for scrpt in data_loaded.keys():
            scrpt_tag = data_loaded[scrpt]['script']

            if scrpt_tag.lower() == tgt_tag.split('-')[1].lower():
                tgt = [(0, scrpt)]

    if src_tag.lower() in ['la', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. Latn-IAST or Latn-HK to select a particular scheme"
        warnings.warn(warn)

        src = [(0, 'ISO')]

    if tgt_tag.lower() in ['la', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. Latn-IAST or Latn-HK to select a particular scheme"
        warnings.warn(warn)

        tgt = [(0, 'ISO')]

    # if latin ignore la and get the following part
    if '-' in src_tag and src_tag.split('-')[0].lower() in ['la', 'en', 'eng']:
        src = [(0, src_tag.split('-')[1])]

    if '-' in tgt_tag and tgt_tag.split('-')[0].lower() in ['la', 'en', 'eng']:
        tgt = [(0, tgt_tag.split('-')[1])]

    if src_tag == 'autodetect':
        src = [(0,auto_detect(txt))]
        pre_options = detect_preoptions(txt, src)

    if len(src) > 0:
        src_pop = sorted(src, reverse=True)[0][1]
    else:
        raise Exception('Source language code: ' + src_tag + ' not found')

    if len(tgt) > 0:
        tgt_pop = sorted(tgt, reverse=True)[0][1]
    else:
        raise Exception('Target language code: ' + tgt_tag + ' not found')

    if len(src) > 1:
        warn = "Multiple scripts " + ','.join(map(lambda x: x[1], src)) + " associated with the input language. The most popular '" + src_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. pa-Guru or pa-Arab to select a particular script"
        warnings.warn(warn)
    if len(tgt) > 1:
        warn = "Multiple scripts " + ','.join(map(lambda x: x[1], tgt)) + " associated with the target language. The most popular '" + tgt_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. pa-Guru or pa-Arab to select a particular script"
        warnings.warn(warn)

    return process_default(src_pop, tgt_pop, txt, nativize, post_options, pre_options)

def process_lang_name(src_name, tgt_name, txt, nativize, post_options, pre_options):
    if src_name == 'autodetect':
        src = auto_detect(txt)
        pre_options = detect_preoptions(txt, src)
    else:
        src = str(langcodes.find(src_name))

    tgt = str(langcodes.find(tgt_name))

    return process_lang_tag(src, tgt, txt, nativize, post_options, pre_options)

## add the new libraries to requiesments.txt in both folders