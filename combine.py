#!/usr/bin/env python3

import sys
import pandas as pd

if len(sys.argv) != 4:
	print("Angi Excel-fil som data skal leses fra.\nMå inneholde 3 ark; MEN, WOMEN og EVENTOR. Hhv WRE-ranking for menn, damer og data fra Eventor.\nParameter 1: Excel-fil.\nParameter 2: første startnr damer.\nParameter 3: første startnr herre\n\nEks:\n./combine.py input.xlsx 101 201")
	sys.exit()

innfil = sys.argv[1]
d_first_startno = int(sys.argv[2])
h_first_startno = int(sys.argv[3])

print("Leser data fra: " + innfil + " ...")

all_dfs = pd.read_excel(innfil, sheet_name=None)

women_df = all_dfs['WOMEN']
men_df = all_dfs['MEN']
etime_df = all_dfs['EVENTOR'].rename(columns = {'IOF-person-id':'IOF_ID'})

all_df = pd.concat([women_df, men_df])

#all_df.to_excel('all.xlsx', index=False)

df = etime_df.merge(all_df[["IOF_ID","WRS_POINTS"]], on="IOF_ID", how="left")

df = df.sort_values(by=["Klasse","WRS_POINTS"], ascending=True, na_position="first")

df.rename(columns = {'IOF_ID':'IOF-person-id'}, inplace = True)

h21e = df[df['Klasse'] == 'H 21-E']
h21e.insert(0, 'STARTNO', range(h_first_startno, h_first_startno + len(h21e)))

d21e = df[df['Klasse'] == 'D 21-E']
d21e.insert(0, 'STARTNO', range(d_first_startno, d_first_startno + len(d21e)))


print("H 21-E, første startnr " + str(h_first_startno) + "\n")
print(h21e)

print("\nD 21-E, første startnr " + str(d_first_startno) + "\n")
print(d21e)
print(len(d21e.index))

#df = df.drop(columns = ['WRS_POINTS'])

merged = pd.concat([h21e, d21e]	)
print("Skriver til fil WRE_Eventor_merged.xlsx...")

merged.to_excel('WRE_Eventor_merged.xlsx', index=False)

#print("\n\nSkriver H 21-E til fil h21e.xlsx ...")
#h21e.to_excel('h21e.xlsx', index=False)

#print("Skriver D 21-E til fil d21e.xlsx ...")
#d21e.to_excel('d21e.xlsx', index=False)

# 
# https://pbpython.com/pandas-excel-tabs.html
#			 https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html


