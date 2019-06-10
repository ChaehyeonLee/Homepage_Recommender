import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm, metrics, decomposition
from sklearn.model_selection import train_test_split
import boto3
import json
import settings

def make_model():

    session = boto3.Session(
        aws_access_key_id = settings.AWS_SERVER_PUBLIC_KEY,
        aws_secret_access_key = settings.AWS_SERVER_SECRET_KEY,
    )

    s3_dont_url = session.resource('s3').Bucket("dont-track-url-bucket")
    json.load_s3 = lambda f: json.load(s3_dont_url.Object(key=f).get()["Body"])
    try:
        dont_track_urls = json.load_s3("url")
    except:
        dont_track_urls_list = []
    else:
        dont_track_urls_list = list(dont_track_urls.values())

    s3 = session.resource('s3').Bucket("history-bucket")
    json.load_s3 = lambda f: json.load(s3.Object(key=f).get()["Body"])
    json.dump_s3 = lambda obj, f: s3.Object(key=f).put(Body=json.dumps(obj))

    data = json.load_s3("history1")
    df = pd.DataFrame(data)
    df['visit_time'] = pd.to_datetime(df['visit_time'],unit='ms')
    df['hour_of_visit_time'] = df['visit_time'].dt.hour
    df['weekday'] = df['visit_time'].dt.weekday


    df['url'] = df['url'].apply(lambda x: parse(x))
    df['unique_url_id'] = df.groupby(['url']).ngroup()
    df['week_and_year'] = df['visit_time'].apply(lambda x: "%d/%d/%d" % (x.year, x.week, x.day))
    df['visit_date_count'] = df.groupby('unique_url_id')['week_and_year'].transform('nunique')
    total_date_count = df['week_and_year'].nunique()
    today_date = pd.to_datetime('today')
    df['time_rating'] = (1 / abs(1- (df['visit_time'] - today_date).dt.days)) + 2 * (df['visit_date_count']/total_date_count)
    
    df = df[3 < df['visit_count']]
    
    df = df[df['url'].str.contains('docs.google.com') == False]
    df = df[df['url'].str.contains('google.co.kr') == False]
    df = df[df['url'].str.contains('nid.naver.com') == False]
    df = df[df['url'].str.contains('speakerdeck.com') == False]
    df = df[df['url'].str.contains('search.naver.com') == False]
    df = df[df['url'].str.contains('careers.kakao.com') == False]
    for each_url in dont_track_urls_list:
        df = df[df['url'].str.contains(each_url) == False]  

    time_rating_df = df[['unique_url_id', 'time_rating']]
    time_rating_dict = time_rating_df.set_index('unique_url_id').T.to_dict('records')[0]

    data = df[['weekday', 'hour_of_visit_time']]
    label = df['unique_url_id']

    train_data, test_data, train_label, test_label = \
    train_test_split(data,label, test_size=0.1) # 이 데이터에서는 테스트가 중요하지 않으므로 90퍼센트를 훈련용데이터로 사용함


    # class_weight 옵션을 벡터로
    # kernel = rbf
    # C 값을 증가시키면 더 많은 url들이 추천가능해짐
    clf = svm.SVC(C = 2, probability=True, class_weight = time_rating_dict)

    clf.fit(train_data,train_label)
    #results=clf.predict(test_data)
    #score = metrics.accuracy_score(results,test_label)
    #print("정답률:",score) # doesn't care
    print("model_maded")
    return df, clf

def parse(url):
    try:
        return str(url.split('//')[0]) + '//' + str(url.split('//')[1].split('/', 1)[0])
    except IndexError:
        print("URL format error!")

df ,clf = make_model()
