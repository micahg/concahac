"""Module for CONCACAF popularity contest rigging."""
import json
import requests

POLL_URL = 'https://www.concacaf.com/umbraco/Surface/PollSurface/Submit'
VOTES = [
    {
        'pollId': '81059',
        'answerKey': 'a8f48427-ed9f-48be-beab-bc9de97ece58',
        'answerText': 'Jessie+Fleming',
        'culture': 'en-us'
    }, {
        'pollId': '81060',
        'answerKey': 'd0edab5f-379e-4a92-8c54-0bcf5112a135',
        'answerText': 'Jonathan+David',
        'culture': 'en-us'
    }
]

while True:
    for vote in VOTES:
        resp = requests.post(POLL_URL, vote)
        if resp.status_code != 200:
            print('ERROR: unable to cast vote. status {} - {}'.format(resp.status_code, resp.content))
        else:
            stats = {}
            js_obj = None
            try:
                js_obj = json.loads(resp.content)
            except ValueError:
                print('ERROR parsing json resposne - who cares')
                continue

            for culture in js_obj['LangInfo']:
                for option in culture['PollOptionList']:
                    if not option['OptionKey'] in stats:
                        stats[option['OptionKey']] = option['OptionTotalVotes']
                    else:
                        stats[option['OptionKey']] = stats[option['OptionKey']] + option['OptionTotalVotes']
            total_votes = 0
            max_votes = 0
            for (key, val) in stats.items():
                # print('{} = {}'.format(key, val))
                total_votes = total_votes + val
                if val > max_votes:
                    max_votes = val
            rigged_name = vote['answerText']
            rigged_votes = stats[vote['answerKey']]
            percentage_votes = rigged_votes / total_votes * 100
            print('{} has {} of {} ({} - max {})'.format(rigged_name, rigged_votes, total_votes, percentage_votes, max_votes))
