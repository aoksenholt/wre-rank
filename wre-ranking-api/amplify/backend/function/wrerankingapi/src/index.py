import awsgi
import base64
import pandas as pd
import io

from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

# Constant variable with path prefix
BASE_ROUTE = "/seed"

def handler(event, context):
    return awsgi.response(app, event, context)

@app.route(BASE_ROUTE, methods=['GET'])
def seed():
    return jsonify(message="hello seed")

@app.route(BASE_ROUTE, methods=['POST'])
def perform_merge():
    request_json = request.get_json()

    men_first_startno=request_json.get("men_first_startno")
    women_first_startno=request_json.get("women_first_startno")
    excel_base64_content=request_json.get("excel_file_content")

    print("Først startnummer menn: " + str(men_first_startno))
    print("Først startnummer damer: " + str(women_first_startno))

    excel_file_decoded=base64.b64decode(excel_base64_content)

    excel_file=io.BytesIO()
    excel_file.write(excel_file_decoded)

    all_dfs = pd.read_excel(excel_file, sheet_name=None)

    women_df = all_dfs['WOMEN']
    men_df = all_dfs['MEN']
    etime_df = all_dfs['EVENTOR'].rename(columns = {'IOF-person-id':'IOF_ID'})

    all_df = pd.concat([women_df, men_df])

    df = etime_df.merge(all_df[["IOF_ID","WRS_POINTS"]], on="IOF_ID", how="left")

    df = df.sort_values(by=["Klasse","WRS_POINTS"], ascending=True, na_position="first")

    df.rename(columns = {'IOF_ID':'IOF-person-id'}, inplace = True)

    h21e = df[df['Klasse'] == 'H 21-E']
    h21e.insert(0, 'STARTNO', range(men_first_startno, men_first_startno + len(h21e)))

    d21e = df[df['Klasse'] == 'D 21-E']
    d21e.insert(0, 'STARTNO', range(women_first_startno, women_first_startno + len(d21e)))


    print("H 21-E, første startnr " + str(men_first_startno) + "\n")
    print(h21e)

    print("\nD 21-E, første startnr " + str(women_first_startno) + "\n")
    print(d21e)
    print(len(d21e.index))

    merged = pd.concat([h21e, d21e]	)
    print(merged)
#    print("Skriver til fil WRE_Eventor_merged.xlsx...")
#    merged.to_excel('WRE_Eventor_merged.xlsx', index=False)

#    print("Skriver SQL til update_startno.sql...")
#    merged = merged.reset_index()  # make sure indexes pair with number of rows

#    with open('update_startno.sql', 'w') as f:
#        f.write("COMMAND;\n")
#        for index, row in merged.iterrows():
#            f.write("UPDATE NAME SET STARTNO='" + str(row['STARTNO']) + "' WHERE KID='" + str(row['Person-id']) + "';\n")

    return jsonify(message="merge performed")