import boto3
import json
import make_reco_model
import settings


def save(url):
    track_or_not = False
    session = boto3.Session(
            aws_access_key_id = settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key = settings.AWS_SERVER_SECRET_KEY,
    )
    s3 = session.resource('s3').Bucket("dont-track-url-bucket")

    json.load_s3 = lambda f: json.load(s3.Object(key=f).get()["Body"])
    json.dump_s3 = lambda obj, f: s3.Object(key=f).put(Body=json.dumps(obj))
    try: 
        urls = json.load_s3("url")
        if url not in urls['url']:
            urls['url'].append(url)
        else:
            urls['url'].remove(url)
            track_or_not = True
    except:
        urls = {'url': [url]}
    json.dump_s3(urls, "url")
    
    make_reco_model.reco_model.update_model()
    return track_or_not
