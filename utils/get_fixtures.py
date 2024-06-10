import pandas as pd
from google.cloud import storage
import requests
import json
import datetime

# function to get fetch the API
def get_api_response(url, querystring, method="GET"):
    url = url
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "3087a5495fbf480453366ecf111f146d"
        }
    response = requests.request(method, url, headers=headers, params=querystring)

    return json.loads(response.content)

# function to change json to wide pandas dataframe
def d_to_df(d):
    df = pd.json_normalize(d['response'])
    return df

if __name__ == "__main__":

    # parameters for API
    url = 'https://v3.football.api-sports.io/fixtures'
    qs = {'league':4, 'season':2024}

    # get response
    d = get_api_response(url, qs)

    # generate dataframe
    df = d_to_df(d)
    # change 
    df['fixture.date'] = pd.to_datetime(df['fixture.date'])
    df['fixture.date'] += pd.Timedelta(hours=2)
    df['fixture.date'] = pd.to_datetime(df['fixture.date']).dt.tz_localize(None)
    df['fixture.date_nice'] = df['fixture.date'].dt.strftime('%Y-%m-%d %H:%M')
    df['fixture.gameday.id'] = df['fixture.date'].dt.date.rank(method='dense')
    df['fixture.gameday.name'] = 'Gameday ' + df['fixture.gameday.id'].astype(int).astype(str)

    df = df.sort_values(['fixture.date', 'fixture.id'])

    print(df.tail())
    # df.to_csv(f'/Users/jakubpaczusko/Desktop/gcp/eurobox24/data/fixtures_{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv', index=False)
    df.to_csv('/Users/jakubpaczusko/Desktop/gcp/eurobox24/data/fixtures.csv', index=False)

    # client = storage.Client()
    # bucket = client.get_bucket('eurobox24')
    # bucket.blob(f'fixtures_{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv').upload_from_string(df.to_csv(), 'text/csv')

