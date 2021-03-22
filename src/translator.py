import requests
import uuid
import json

# Add your subscription key and endpoint
subscription_key = "9cf8b66f2cd2402e98698ac3f7235826"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "northeurope"
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
        return 1, 'Destination Language empty'

    params = {
        'api-version': '3.0',
        'toScript': 'latn',
        'from': from_lang,
        'to': to_lang
    }
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
