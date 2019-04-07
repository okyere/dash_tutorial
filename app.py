# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

trans_df = pd.read_csv("transactions_as.csv")
unique_tellers = trans_df["TELLERNUMBER"].unique().tolist()

# df_ghc = df[df['CURRENCY'] == 'GHS']
# tellers_ghc = df_ghc.groupby(['TELLERNUMBER','BANKNAME'])['AMOUNTINFIGURES'].sum().reset_index()

# withdrawals
def get_teller_debits(teller):
    withdrawals = trans_df[ (trans_df["TELLERNUMBER"] == teller) & (trans_df["TRANSACTIONTYPE"] == "Withdrawal") ]["AMOUNTINFIGURES"].sum()
    return withdrawals

# deposits
def get_teller_credits(teller):
    deposits = trans_df[ (trans_df["TELLERNUMBER"] == teller) & (trans_df["TRANSACTIONTYPE"] == "Deposit") ]["AMOUNTINFIGURES"].sum()
    return deposits

# Generate the list of tellers and all their attributes
def generate_list(tellers):

    teller_list = []
    for i in tellers:

            credit = get_teller_credits(i)
            debit = get_teller_debits(i)

            teller_list.append(
                    dbc.Row(dbc.ListGroup([
                           dbc.ListGroupItem(i),
                           dbc.ListGroupItem("Credit: {}".format(credit)),
                           dbc.ListGroupItem("Debit: {}".format(debit)),
                        ]))
                
             )
    
    return teller_list

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    # Use container to wrap everything in the app
    dbc.Container(children=[
                   dbc.Row(dbc.Col(html.H1("Management Dashboard", 
                                           style={'textAlign': 'center'}
                   ))),

                   html.Hr(),

                   dbc.Row(dbc.Col(dbc.ListGroup(
                           [
                                   dbc.ListGroupItem("Credit"),
                                   dbc.ListGroupItem("Debit"),
                                   dbc.ListGroupItem("Balance")
                           ],
                           style={"flex-direction": "row"}
                   ), width={"size": 8,  "offset": 9} ) ),

                    html.Hr(),

                    html.Div(generate_list(unique_tellers))
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)