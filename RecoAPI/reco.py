from flask import Flask, request, jsonify
import json
import save_in_s3
import get_reco_site
import make_reco_model
import save_dont_track_url
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=['POST'])
def reco():
    if request.headers.get('recoRequest'):
        recommended_url = get_reco_site.get_reco()
        print(datetime.now())
        print("recommended_url:", recommended_url)
        return recommended_url
    elif request.headers.get('sendHistory'):
        json_history = json.loads(request.data)
        history_data_dump = json.dump_s3(json_history, "history1")
        return "history_saved"
    elif request.headers.get('dontTrackRequest'):
        print(request.data)
        track_or_not = save_dont_track_url.save(parse((request.data).decode("utf-8")))
        
        return "We track this page" if track_or_not else "We don't track this page"
    else:
        return "this???"

def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print("URL format error!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
