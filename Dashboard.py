import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc as pdb
import prettytable
import pandas.io.sql as psql
import pandas as pd
from pandas import DataFrame

conn = pdb.connect('Driver={SQL Server};' 
                   'Server=ADARSH\ADARSH;'
                   'Database=PGYR;'
                   'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute("select TOP 10 Physician_Profile_ID, Physician_First_Name, Physician_Last_Name,  "
               "CONVERT(varchar, CAST(SUM(Value_of_Interest) as Money), 1) Value_of_Interest "
               "from OP_DTL_OWNRSHP_PGYR_Final "
               "group by Physician_Profile_ID, Physician_First_Name, Physician_Last_Name "
               "order by SUM(Value_of_Interest) desc")

x = prettytable.PrettyTable(["Physician Profile ID", "Physician First Name", "Physician Last Name", "Value Of Interest"])
x.align["Physician Profile ID"] = "l"
x.align["Physician First Name"] = "l"
x.align["Physician Last Name"] = "l"
for row in cursor:
    x.add_row(row)

print(x)
qry = "select Physician_Profile_ID, Program_Year, SUM(CONVERT(numeric(18,2),Value_of_Interest)) as Value_of_Interest " \
      "from OP_DTL_OWNRSHP_PGYR " \
      "where Physician_Profile_ID in (select TOP 10 Physician_Profile_ID " \
      "from OP_DTL_OWNRSHP_PGYR_Final " \
      "group by Physician_Profile_ID, Physician_First_Name, Physician_Last_Name " \
      "order by SUM(Value_of_Interest) desc) " \
      "group by Physician_Profile_ID, Program_Year " \
      "order by Physician_Profile_ID, Program_Year"

df = DataFrame(psql.read_sql_query(qry, conn))

years = df["Program_Year"].unique()

PhysicianIds = sorted(df["Physician_Profile_ID"].unique())

pd.options.mode.chained_assignment = None

for ID in PhysicianIds:
    df_filter = df[df["Physician_Profile_ID"] == ID]
    for year in years:
        found = False
        for index, row in df_filter.iterrows():
            if row["Program_Year"] == year:
                found = True
                break
            else:
                found = False
        if not found:
            df_filter.loc[index+1] = [ID, year, 0]
    VoI = list(df_filter["Value_of_Interest"])
    sns.lineplot(x=years, y=VoI, label=ID, linestyle='-')

plt.ylabel("Value of Interest (in 100,000,000)")
plt.xlabel("Year")
plt.title("Top 10 Physicians")
plt.legend(title="Physician Profile ID")
plt.show()

