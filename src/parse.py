import pickle
import json
import dominate
from dominate.tags import *

theme = ''


def create_theme():
    theme = {
        'body_bg': '#1E1C31',
        'body_fg': '#E5C07B',
        'body_font': '15px roboto',
        'word_fg': '#E06C75',
        'word_bg': '#1E1C31',
        'word_font': '15px comfortaa',
        'lang_fg': '#61AFEF',
        'lang_bg': '#1E1C31',
        'lang_font': '15px comfortaa',
        'okay_fg': '#98C379',
        'query_fg': '#98C379',
        'query_bg': '#1E1C31',
        'query_font': '15px comfortaa',
        'synonyms_fg': '#98C379',
        'synonyms_bg': '#1E1C31',
        'synonyms_font': '15px comfortaa',
        'has_example_fg': '#98C379',
        'has_example_bg': '#1E1C31',
        'has_example_font': '15px comfortaa',
        'definition_fg': '#98C379',
        'definition_bg': '#1E1C31',
        'definition_font': '15px comfortaa',
        'translation_fg': '#98C379',
        'translation_bg': '#1E1C31',
        'translation_font': '16px comfortaa'
    }

    with open('../lib/theme.p', 'wb') as t:
        pickle.dump(theme, t)
    return theme


def create_css():
    try:
        with open('../lib/theme.p', 'rb') as t:
            theme = pickle.load(t)
    except FileNotFoundError:
        theme = create_theme()

    classes = ('body', 'word', 'lang', 'query', 'definition',
               'translation', 'synonyms', 'has_example')

    def special_check(name):
        if name == 'has_example':
            return "text-decoration: underline;"
        if name == 'body':
            return "overflow: scroll;"
        return ''

    css = ''
    for cls_name in classes:
        class_style = f""".{cls_name}{{
            font: {theme[f"{cls_name}_font"]};
            background-color: {theme[f"{cls_name}_bg"]};
            color: {theme[f"{cls_name}_fg"]};
            font: {theme[f"{cls_name}_font"]};
            {special_check(cls_name)}
            }}\n"""
        css = css+class_style

    with open('../lib/style.css', 'w') as f:
        f.write(css)


def parse_dict(p):
    query = p['displaySource']
    definitions = {}
    for word in p['translations']:
        trln = word['displayTarget']
        word_type = word['posTag']
        synonyms = [
            (var['displayText'], var['numExamples'])
            for var in word['backTranslations']]
        definition = {'word_type': word_type,
                      'variants': synonyms}
        definitions[trln] = definition
    return ('d', query, definitions)


def parse_translation():
    with open('tran.out.json', 'r') as f:
        t = json.load(f)[2][0]
    try:
        source = t['detectedLanguage']
    except KeyError:
        source = 'empty'

    translations = {trans['to']: trans['text']
                    for trans in t['translations']}

    return ('t', source, translations)


def auto_html():
    with open('run.dict.json', 'r') as r:
        payload = json.load(r)[0]
    try:
        with open('../lib/style.css'):
            pass
    except FileNotFoundError:
        create_css()
        auto_html()
    query_type, query, trans = parse_dict(payload)



if __name__ == '__main__':
    auto_html()
