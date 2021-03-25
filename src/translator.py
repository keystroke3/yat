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


def translator(text, from_lang, to_lang, mode='translate'):
    if not text:
        return 1, 'Nothing to translate'
    if not to_lang and mode != 'detect':
        return 1, 'Target Language cannot be empty'

    if type(to_lang) == str:
        if ' ' in to_lang or ',' in to_lang:
            to_lang = [to_lang.split(i) for i in (',', ' ') if i in to_lang]
        else:
            to_lang = [to_lang]
    
    params = {
        'api-version': '3.0',
        'from': from_lang,
        'to': to_lang[0]
    }
    if mode == 'translate' or mode == '':
        path = '/translate'
    elif mode == 'dict':
        if not from_lang or not to_lang:
            print('You need to enter both source and target language for dictionary, en being one of them')
            exit(1)
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

    ans = (json.dumps(response, sort_keys=True,
                      ensure_ascii=False, indent=4, separators=(',', ': ')))
    return 0, ans


if __name__ == '__main__':
    data = translator(
        mode=input('mode: '),
        text=input('Text: '),
        to_lang=input('to: '),
        from_lang=input('from: '),
    )
    print(data[1])
