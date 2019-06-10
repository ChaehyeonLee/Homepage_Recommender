import make_reco_model
from datetime import datetime, timedelta

def get_reco():
    df = make_reco_model.reco_model.df
    clf = make_reco_model.reco_model.clf
    now_time = datetime.now() + timedelta(hours=9)    
    now_weekday = now_time.weekday()
    now_hour = now_time.hour
    print(now_time)
    recommended_unique_id = clf.predict([[now_weekday, now_hour]])
    return df[df['unique_url_id'] == recommended_unique_id[0]]['url'].as_matrix()[0]