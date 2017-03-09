from flask import Flask, make_response, request
import json
import os
from twython import Twython, TwythonError

app = Flask(__name__)

API_KEY = os.environ['TWITTER_API_KEY']
API_SECRET = os.environ['TWITTER_API_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']

@app.route('/tweet/', methods=['POST'])
def tweet():
    form = request.form
    payload = json.loads(form.get('payload'))
    if payload:
        repo = payload['repository']['url']
        if repo != 'https://github.com/sinker/tacofancy':
            resp = make_response(json.dumps({'status': 'error', 'message': 'Invalid github respository'}), 400)
            resp.headers['Content-Type'] = 'application/json'
        else:
            commits = payload['commits']
            addeds = [c for c in commits if c.get('added')]
            second_to_last = addeds[-2]
            message = second_to_last['message']
            url = second_to_last['url']
            status = '%s %s' % (message, url)
            tweeter = Twython(API_KEY, API_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
            try: 
                tweeter.update_status(status=status)
                resp = make_response(json.dumps({'status': 'success', 'message': 'Tweet sent'}))
                resp.headers['Content-Type'] = 'application/json'
            except TwythonError, e:
                resp = make_response(json.dumps({'status': 'error', 'message': str(e)}), 500)
                resp.headers['Content-Type'] = 'application/json'
    else:
        resp = make_response(json.dumps({'status': 'error', 'message': 'POST data not in the correct format'}), 400)
        resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
