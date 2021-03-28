import requests
import uuid
import json
try:
    with open('env.json', 'r') as f:
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


def translate(text, from_lang, to_lang):
    if not text:
        return 1, 'Nothing to translate'
    if not to_lang: 
        return 1, 'Target Language cannot be empty'

    if type(to_lang) == str:
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
        and ' ' not in text.strip():
        from_lang = api(text, 'detect')[0]['language']
        params['from'] = from_lang
        return 0, api(text, 'dict', params)
    else:
        return 0, api(text, 'translate', params)

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
    data = translate(
        text=input('Text: '),
        to_lang=input('to: '),
        from_lang=input('from: '),
    )
    print(data[1])
