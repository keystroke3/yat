import pickle
import json
import dominate
from dominate.tags import body, sup, ol, ul, li, link, div

theme = ''


def create_theme():
    theme = {
        'body_bg': '#1E1C31',
        'body_fg': '#E5C07B',
        'body_font': '15px roboto',
        'word_fg': '#98C379',
        'word_bg': '#1E1C31',
        'word_font': '20px comfortaa',
        'lang_fg': '#61AFEF',
        'lang_bg': '#1E1C31',
        'lang_font': '15px comfortaa',
        'okay_fg': '#98C379',
        'query_fg': '#98C379',
        'query_bg': '#1E1C31',
        'query_font': '15px comfortaa',
        'synonyms_fg': '#98C379',
        'synonyms_bg': '#1E1C31',
        'synonyms_font': '15px roboto',
        'definition_fg': '#E5C07B',
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
               'translation', 'synonyms',)

    def special_check(name):
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
        css +=class_style
    exta_css=f""".has_example{{
            text-decoration: underline;
            cursor: pointer;
        }}\n.variant{{
            display: inline;
        }}\n.def_box{{
            border: 3px;
            border-style: dotted;
            border-radius: 10px;
            border-color: '#E5C07B';
            padding: 10px;
            margin: 5px;
            width: 20rem;
            height: max-content;
        }}\n
    """
    css += exta_css
    

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


def parse(payload=''):
    if not payload:
        with open('run.dict.json', 'r') as r:
            payload = json.load(r)[0]
        
    try:
        with open('../lib/style.css'):
            pass
    except FileNotFoundError:
        create_css()
        parse()
    query_type, query, trans = parse_dict(payload)

    doc = dominate.document(title=f'YAT {query}')
    with doc.head:
        link(rel='stylesheet', href='../lib/style.css')
    with doc:
        container = body(cls='body').add(div(cls='def_box'))

    word = container.add(div(query, cls='word'))
    language = container.add(div('en - es', cls='lang'))

    def add_syn(synonyms, vars):
        for syn in vars:
            if not syn[1]:
                synonyms.add(li(syn[0], cls='synonyms'))
            else:
                syn_word = synonyms.add(li(f'{syn[0]} ',
                cls='synonyms has_example'))
                syn_eg_no = syn_word.add(sup(syn[1]))
                

    for w in trans:
        def_box = container.add(div()).add(ul())
        defin = trans[w]
        def_box.add(li(f'{w} ({defin["word_type"]})'.lower(),
                        cls='definition'))
        synonyms = def_box.add(ol())
        add_syn(synonyms, defin['variants'])
    
    return doc



if __name__ == '__main__':
    print(parse())
