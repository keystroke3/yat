import pickle
import json
import dominate
import argparse
from translator import translate
from dominate.util import raw
from dominate.tags import body, sup, ol, ul, li, link, div, p

theme = ''

with open('../lib/language_names.p', 'rb') as l:
    langs = pickle.load(l)


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
        'translation_font': '15px roboto',
        'lit_fg': '#98C379',
        'lit_bg': '#1E1C31',
        'lit_font': '15px roboto',
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
               'translation', 'lit', 'synonyms',)

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
        css += class_style
    exta_css = f""".has_example{{
            text-decoration: underline;
            cursor: pointer;
        }}\n.variant{{
            display: inline;
        }}\n.indent{{
            margin-left: 5%;
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


def parse_dict(payload):
    p=payload[0]
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
    return (query, definitions)


def dict_html(container, query, dict_, source, target):
    container.add(div(query, cls='word'))
    container.add(div(raw(
        f'{langs[source]} -> {langs[target]}'), cls='lang'))
    for w in dict_:
        def_box = container.add(div()).add(ul())
        defin = dict_[w]
        def_box.add(li(f'{w} ({defin["word_type"]})'.lower(),
                    cls='definition'))
        synonyms = def_box.add(ol())
        for syn in defin['variants']:
            if not syn[1]:
                synonyms.add(li(syn[0], cls='synonyms'))
            else:
                syn_word = synonyms.add(li(f'{syn[0]} ',
                                        cls='synonyms has_example'))
                syn_word.add(sup(syn[1]))


def trans_html(container, payload, source):
    container.add(div(f'{langs[source]} detected', cls='lang'))
    trlns_box = container.add(div()).add(ul(cls='definition'))
    for t in payload:
        trlns_box.add(ul())
        trlns_box.add(li(langs[t['to']]))
        trln_text = trlns_box.add(div(cls='indent'))
        trln_text.add(div(t['text'], cls='translation'))
        try:
            lit = t['transliteration']
            trln_text.add(p(f"({lit['text']})", cls='lit'))
        except KeyError:
            continue


def parse(target='', source='', payload=''):
    try:
        with open('../lib/style.css'):
            pass
    except FileNotFoundError:
        create_css()
        parse(target, source, payload)

    doc = dominate.document(title=f'YAT')
    with doc.head:
        link(rel='stylesheet', href='../lib/style.css')
    with doc:
        container = body(cls='body').add(div(cls='def_box'))
    try:
        payload[0]['translations'][0]['backTranslations']
        query, dict_ = parse_dict(payload)
        dict_html(container, query, dict_, source, target)
        return doc
    except (KeyError,KeyError):
        trans_html(container, payload, source)
        return doc


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("-t", "--text", metavar="'text'",
                            help="Text to translate")
    cli_parser.add_argument("-T", "--target", metavar="'language'",
                            help="Target language to translate to")
    cli_parser.add_argument("-s", "--source", default='', metavar="'language'",
                            help="Source language of the text")
    args = cli_parser.parse_args()
    if not args.text:
        print('Nothing to translate')
        exit(1)
    if not args.target:
        exit(1)
        print('Target language not set')
    response = translate(text=args.text,
                        to_lang=args.target,
                        from_lang=args.source)
    payload = response[1]
    if not source:
        source = response[0]
    else:
        source = args.source
    print(parse(target=args.target,
                source=source,
                payload=payload))
