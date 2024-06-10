import pandas as pd
import time
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

############################
### SUBMIT GAMEDAY PREDS ###
############################

def submit_gameday_preds(
    userId,
    fixtureId,
    hts,
    ats,
    ftts,
    fpts,
):
    
    form_df = pd.DataFrame.from_dict(
        {
            'user.id':[userId],
            'timestamp':[time.time()],
            'fixture.id':[fixtureId],
            'hts':[hts],
            'ats':[ats],
            'ftts':[ftts],
            'fpts':[fpts],
        },
        orient='columns'
    )

    progress_text = "Sending your predictions. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for seconds in range(3):
        my_bar.progress(seconds * 1 / 3, text=progress_text)
        time.sleep(1)
    time.sleep(0.5)
    my_bar.empty()

    try:
        form_df.to_csv(
            '/Users/jakubpaczusko/Desktop/gcp/eurobox24/data/preds.csv',
            index=False,
            mode='a',
            header=False
        )
        st.success('Submitted :grinning:')
    except:
        st.error('Ups... Something went wrong')


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
        st.success("Row inserted successfully.")
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