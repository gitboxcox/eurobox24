import pandas as pd
import time
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from st_files_connection import FilesConnection

###################################
### GET ALL LATEST USER'S PREDS ###
###################################
        
def get_latest_user_preds(
        preds,
        userId
):
    raw_df = preds.loc[preds['user.id']==userId]
    if raw_df.shape[0] > 0:
        idx = raw_df.groupby('fixture.id')['timestamp'].idxmax()
        latest_df = raw_df.loc[idx].reset_index(drop=True)
        return latest_df
    else:
        return raw_df

##################
### SEND_TO_BQ ###
##################

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
CLIENT = bigquery.Client(credentials=credentials)

def send_to_bq(
        table,
        data
):
    table_ref = CLIENT.dataset('eurobox24').table(table)

    # Insert the row into the table
    errors = CLIENT.insert_rows_json(table_ref, [data])

    # Check for errors
    if errors == []:
        st.success("Successfully submitted.")
    else:
        st.error(errors)

##################
### READ PREDS ###
##################
        
def read_all_preds():

    sql = '''
    select * from `eurobox24.eurobox24.preds`
    '''

    df = CLIENT.query(sql).to_dataframe(int_dtype=None, float_dtype=None)

    return df

def read_all_heroes():

    sql = '''
    select * from `eurobox24.eurobox24.heroes`
    '''

    df = CLIENT.query(sql).to_dataframe(int_dtype=None, float_dtype=None)

    return df

def read_all_pretournament():

    sql = '''
    select * from `eurobox24.eurobox24.pretournament_preds`
    '''

    df = CLIENT.query(sql).to_dataframe(int_dtype=None, float_dtype=None)

    return df

conn = st.connection('gcs', type=FilesConnection)

def read_fixtures():
    fixtures = conn.read('eurobox24/data/fixtures.csv', input_format='csv')
    fixtures['fixture.date'] = pd.to_datetime(fixtures['fixture.date'])
    fixtures['fixture.gameday.deadline'] = pd.to_datetime(fixtures['fixture.gameday.deadline'])
    return fixtures

def read_squads():
    squads = conn.read('eurobox24/data/squads.csv', input_format='csv')
    return squads
