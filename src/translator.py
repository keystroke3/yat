import requests
import uuid
import json
import argparse
import utils 

cache_dir = utils.cache_dir
lib_dir = utils.lib_dir

try:
    with open(f'{lib_dir}/env.json', 'r') as f:
        creds = json.load(f)
except FileNotFoundError:
    print('No credentials found')
    exit(1)

subscription_key = creds['key']
endpoint = creds['endpoint']
location = creds['location']
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def translate(text, to_lang, from_lang=''):
    if not text:
        return 'Nothing to translate'
    if not to_lang:
        return 'Target Language cannot be empty'

    if type(to_lang) == str:
        if ', ' in to_lang:
            to_lang = to_lang.replace(', ', ',')
        if ' ' in to_lang or ',' in to_lang:
            to_lang = [to_lang.split(i) for i in (',', ' ') if i in to_lang][0]
        else:
            to_lang = (to_lang)

    if len(to_lang) == 1:
        toScript = 'latn'
    else:
        toScript = ['latn' for i in to_lang[0]]

    params = {
        'api-version': '3.0',
        'from': from_lang,
        'toScript': toScript,
        'to': to_lang
    }
    if not from_lang\
            and ' ' not in text.strip()\
                and len(to_lang) == 1:
        from_lang = api(text, 'detect')[0]['language']
        params['from'] = from_lang
        d_text = api(text, 'dict', params)
        return from_lang, d_text 
    else:
        r = api(text, 'translate', params)
        try:
            r=r[0]
            from_lang = r['detectedLanguage']['language']
            translations = r['translations']
            return from_lang, translations
        except KeyError:
            print('key error')
            print(r)
            return 1, r


def api(text, mode, params={}):
    if mode == 'translate' or mode == '':
        path = '/translate'
    elif mode == 'dict':
        path = '/dictionary/lookup'
    elif mode == 'detect':
        path = '/detect'
        params = {
            'api-version': '3.0'
        }
    constructed_url = endpoint + path
    body = [{
        'text': str(text)
    }]
    request = requests.post(
        constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response


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
        print('Target language not set')
        exit(1)

    print(translate(text=args.text,
                    to_lang=args.target,
                    from_lang=args.source))
