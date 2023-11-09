import json
from mitmproxy import http


def read_words() -> [str]:
    try:
        with open('words.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            return [line for line in lines if len(line) > 0]
    except:
        return []


def response(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url

    if 'TweetDetail' in url and 'graphql' in url:
        suck_words = read_words()
        data = json.loads(flow.response.get_text())
        instruction = data['data']['threaded_conversation_with_injections_v2']['instructions'][0]
        entries = instruction['entries']
        filtered_entries = [
            entry for entry in entries if valid(entry, suck_words)
        ]
        instruction['entries'] = filtered_entries
        flow.response.text = json.dumps(data)


def valid(entry: dict, suck_words: [str]) -> bool:
    if 'items' not in entry['content']:
        return True

    for item in entry['content']['items']:
        if 'tweet_results' not in item['item']['itemContent']:
            continue

        result = item['item']['itemContent']['tweet_results']['result']
        results = [result]

        tweet = result.get('quoted_status_result', {}).get(
            'result', {}).get('tweet')

        if tweet is not None:
            results.append(tweet)

        for result in results:
            full_text = result['legacy']['full_text']

            legacy = result['core']['user_results']['result']['legacy']

            name = legacy['name']
            screen_name = legacy['screen_name']
            desc = legacy['description']
            location = legacy['location']

            features = [name, screen_name, desc, location, full_text]

            if sucks(features, suck_words):
                return False
    return True


def sucks(features: [str], suck_words: [str]) -> bool:
    for feature in features:
        for word in suck_words:
            if word in feature:
                return True
    return False
