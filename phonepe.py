import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image

#Dataframe creation

#MYsql connection

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd="ajaysuria@070",
    auth_plugin='mysql_native_password',
    database="Phonepe_data")
mycursor=mydb.cursor(buffered=True)

#aggregated_transaction_df

mycursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1=mycursor.fetchall()
aggregated_transaction=pd.DataFrame(table1,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Transaction_type",
                                                    "Transaction_amount",
                                                    "Transaction_count"))

#aggregated_users_df

mycursor.execute("SELECT * FROM aggregated_users")
mydb.commit()
table2=mycursor.fetchall()
aggregated_users=pd.DataFrame(table2,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Brands",
                                                    "Percentage",
                                                    "Transaction_count"))


#aggregated_insurance_df

mycursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table3=mycursor.fetchall()
aggregated_insurance=pd.DataFrame(table3,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Transaction_type",
                                                    "Transaction_amount",
                                                    "Transaction_count"))

#map_transaction_df

mycursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table4=mycursor.fetchall()
map_transaction=pd.DataFrame(table4,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Districts",
                                                    "Transaction_amount",
                                                    "Transaction_count"))

#map_user_df

mycursor.execute("SELECT * FROM map_user")
mydb.commit()
table5=mycursor.fetchall()
map_user=pd.DataFrame(table5,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Districts",
                                                    "RegisteredUsers",
                                                    "AppOpens"))

#map_insurance_df

mycursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table6=mycursor.fetchall()
map_insurance=pd.DataFrame(table6,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Districts",
                                                    "Transaction_amount",
                                                    "Transaction_count"))

#top_transaction_df

mycursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table7=mycursor.fetchall()
top_transaction=pd.DataFrame(table7,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Pincodes",
                                                    "Transaction_amount",
                                                    "Transaction_count"))

#top_users_df

mycursor.execute("SELECT * FROM top_users")
mydb.commit()
table8=mycursor.fetchall()
top_users=pd.DataFrame(table8,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Pincodes",
                                                    "RegisteredUsers"
                                                    ))

#top_insurance_df

mycursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table9=mycursor.fetchall()
top_insurance=pd.DataFrame(table9,columns=("States",
                                                    "Years", 
                                                    "Quarter",
                                                    "Pincodes",
                                                    "Transaction_amount",
                                                    "Transaction_count"))



def Transaction_amount_count_Y(df,Year):
    

    tacy = df[df["Years"] == Year]
    tacy.reset_index(drop = True, inplace = True) 

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{Year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Oranges_r, width=600, height=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{Year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Magenta_r, width=600, height=600)
        st.plotly_chart(fig_count)


    col1, col2 = st.columns(2)

    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()


        fig_india_1=px.choropleth(tacyg,geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{Year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600
                                )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="Rainbow",
                                    range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name="States", title=f"{Year} TRANSACTION COUNT",fitbounds="locations",
                                    height=600,width=600
                                    )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy


def Transaction_amount_count_Y_Q(df,quarter):
    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace = True) 

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2= st.columns(2)

    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Oranges_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        
        fig_count=px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Magenta_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)

    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600
                                )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="Rainbow",
                                    range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name="States", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                    height=600,width=600
                                    )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Agg_tran_transaction_type(df, state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True) 

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2= st.columns(2)

    with col1:

        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width=600, title=f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)


# Aggre_user_analysis_1
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop=True, inplace=True)
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#aggre_user_analysis_2
def Aggre_user_plot_2(df,Quarter):
    aguyq= df[df["Quarter"]== Quarter]
    aguyq.reset_index(drop=True, inplace=True)
    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title=f"{Quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.Bluyl_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggre_user_analysis_3
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"] == state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1= px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage",
                        title=f"{state.upper()}    BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000,
                        markers=True)
    st.plotly_chart(fig_line_1)

#Map_insurance_District
def Map_insur_District(df, state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True) 

    tacyg = tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2= st.columns(2)

    with col1:

        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Purples_r)
        st.plotly_chart(fig_bar_2)

# Map_user_plot_1
def map_user_plot_1(df,year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop=True, inplace=True)
    muyg= muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1= px.line(muyg, x="States", y=["RegisteredUsers","AppOpens"],
                        title=f"{year}  REGISTERED USERS, APPOPENS",width=1000, height=800,
                        markers=True)
    st.plotly_chart(fig_line_1)

    return muy

# Map_user_plot_2
def map_user_plot_2(df,Quarter):
    muyq= df[df["Quarter"]== Quarter]
    muyq.reset_index(drop=True, inplace=True)
    muyqg= muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)


    fig_line_1= px.line(muyqg, x="States", y=["RegisteredUsers","AppOpens"],
                        title=f"{df['Years'].min()} YEAR  {Quarter}  QUARTER REGISTERED USERS, APPOPENS",width=1000, height=800,
                        markers=True,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#Map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)

    col1,col2= st.columns(2)

    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation= "h",
                                title= "REGISTERED USERS", height=800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x="AppOpens", y="Districts", orientation= "h",
                                title= "APPOPENS", height=800, color_discrete_sequence= px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_map_user_bar_2)

#top_insurance_plot_1
def top_insurance_plot_1(df, states):
    tiy= df[df["States"]== states]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2= st.columns(2)

    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data="Pincodes",
                                title= "TRANSACTION AMOUNT", height=600,width=600, color_discrete_sequence= px.colors.sequential.Jet_r)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2= px.bar(tiy, x="Quarter", y="Transaction_count", hover_data="Pincodes",
                                title= "TRANSACTION COUNT", height=600,width=600, color_discrete_sequence= px.colors.sequential.BuPu_r)
        st.plotly_chart(fig_top_insur_bar_2)

#top_user_plot_1
def top_user_plot_1(df, years):
    tuy= df[df["Years"]== years]
    tuy.reset_index(drop=True, inplace=True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1= px.bar(tuyg, x="States",y="RegisteredUsers", color="Quarter", width=1000, height=800,
                        color_discrete_sequence= px.colors.sequential.Burgyl,hover_name="States",
                        title= f"{years} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#top_user_plot_2
def top_user_plot_2(df,states):
    tuys= df[df["States"]== states]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2= px.bar(tuys, x="Quarter", y="RegisteredUsers", title= "REGISTERED USERS, PINCODES, QUARTER",
                        width=1000, height=800, color="RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

#MYsql connection

def top_chart_transaction_amount(table_name):
    mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd="ajaysuria@070",
        auth_plugin='mysql_native_password',
        database="Phonepe_data")
    mycursor=mydb.cursor(buffered=True)

    #plot_1
    query1= f'''SELECT States, SUM(Transaction_amount) as Transaction_amount
                FROM {table_name}
                group by States
                Order by Transaction_amount desc
                limit 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "Transaction_amount"))

    col1,col2= st.columns(2)

    with col1:

        fig_amount_1=px.bar(df_1, x="States", y="Transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Oranges_r,height=650,width=600, hover_name="States")
        st.plotly_chart(fig_amount_1)

    #plot_2
    query2= f'''SELECT States, SUM(Transaction_amount) as Transaction_amount
                FROM {table_name}
                group by States
                Order by Transaction_amount
                limit 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "Transaction_amount"))

    with col2:

        fig_amount_2=px.bar(df_2, x="States", y="Transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Oranges,height=700,width=650, hover_name="States")
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT States, avg(Transaction_amount) as Transaction_amount
                FROM {table_name}
                group by States
                Order by Transaction_amount;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "Transaction_amount"))

    fig_amount_3=px.bar(df_3,x="Transaction_amount", y="States",    title="AVERAGE OF TRANSACTION AMOUNT",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r,height=800,width=1000, hover_name="States")
    st.plotly_chart(fig_amount_3)

#MYsql connection

def top_chart_transaction_count(table_name):
    mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd="ajaysuria@070",
        auth_plugin='mysql_native_password',
        database="Phonepe_data")
    mycursor=mydb.cursor(buffered=True)

    #plot_1
    query1= f'''SELECT States, SUM(Transaction_count) as Transaction_count
                FROM {table_name}
                group by States
                Order by Transaction_count desc
                limit 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "Transaction_count"))

    col1,col2= st.columns(2)

    with col1:

        fig_amount_1=px.bar(df_1, x="States", y="Transaction_count", title="TOP 10 OF TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Oranges_r,height=650,width=600, hover_name="States")
        st.plotly_chart(fig_amount_1)

    #plot_2
    query2= f'''SELECT States, SUM(Transaction_count) as Transaction_count
                FROM {table_name}
                group by States
                Order by Transaction_count
                limit 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "Transaction_count"))

    with col2:

        fig_amount_2=px.bar(df_2, x="States", y="Transaction_count", title="LAST 10 OF TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Oranges,height=700,width=650, hover_name="States")
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT States, avg(Transaction_count) as Transaction_count
                FROM {table_name}
                group by States
                Order by Transaction_count;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "Transaction_count"))

    fig_amount_3=px.bar(df_3, x="Transaction_count",y="States",    title="AVERAGE OF TRANSACTION COUNT",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height=800,width=1000, hover_name="States")
    st.plotly_chart(fig_amount_3)

#MYsql connection

def top_chart_registered_user(table_name, state):
    mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd="ajaysuria@070",
        auth_plugin='mysql_native_password',
        database="Phonepe_data")
    mycursor=mydb.cursor(buffered=True)

    #plot_1
    query1= f'''SELECT Districts, SUM(RegisteredUsers) as RegisteredUsers
                FROM {table_name}
                where States= "{state}"
                group by Districts
                order by RegisteredUsers desc
                limit 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "RegisteredUsers"))

    col1,col2= st.columns(2)

    with col1:

        fig_amount_1=px.bar(df_1, x="Districts", y="RegisteredUsers", title="TOP 10 OF REGISTERED USER",
                        color_discrete_sequence=px.colors.sequential.Brwnyl_r,height=700,width=650, hover_name="Districts")
        st.plotly_chart(fig_amount_1)

    #plot_2
    query2= f'''SELECT Districts, SUM(RegisteredUsers) as RegisteredUsers
                FROM {table_name}
                where States= "{state}"
                group by Districts
                order by RegisteredUsers
                limit 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "RegisteredUsers"))

    with col2:

        fig_amount_2=px.bar(df_2, x="Districts", y="RegisteredUsers", title="LAST 10 REGISTERED USER",
                        color_discrete_sequence=px.colors.sequential.Cividis_r,height=700,width=650, hover_name="Districts")
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT Districts, AVG(RegisteredUsers) as RegisteredUsers
                FROM {table_name}
                where States= "{state}"
                group by Districts
                order by RegisteredUsers 
                ;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "RegisteredUsers"))

    fig_amount_3=px.bar(df_3, x="RegisteredUsers",y="Districts",   title="AVERAGE OF REGISTERED USER",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Oryel_r,height=800,width=1000, hover_name="Districts")
    st.plotly_chart(fig_amount_3)

#MYsql connection

def top_chart_appopens(table_name, state):
    mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd="ajaysuria@070",
        auth_plugin='mysql_native_password',
        database="Phonepe_data")
    mycursor=mydb.cursor(buffered=True)

    #plot_1
    query1= f'''SELECT Districts, SUM(AppOpens) as AppOpens
                FROM {table_name}
                where States= "{state}"
                group by Districts
                order by AppOpens desc
                limit 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "AppOpens"))

    col1,col2= st.columns(2)

    with col1:

        fig_amount_1=px.bar(df_1, x="Districts", y="AppOpens", title="TOP 10 OF APPOPENS",
                        color_discrete_sequence=px.colors.sequential.Brwnyl_r,height=700,width=650, hover_name="Districts")
        st.plotly_chart(fig_amount_1)

    #plot_2
    query2= f'''SELECT Districts, SUM(AppOpens) as AppOpens
                FROM {table_name}
                where States= "{state}"
                group by Districts
                order by AppOpens
                limit 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "AppOpens"))

    with col2:

        fig_amount_2=px.bar(df_2, x="Districts", y="AppOpens", title="LAST 10 APPOPENS",
                        color_discrete_sequence=px.colors.sequential.Cividis_r,height=700,width=650, hover_name="Districts")
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT Districts, AVG(AppOpens) as AppOpens
                FROM {table_name}
                where States= "{state}"
                group by Districts
                order by AppOpens 
                ;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "AppOpens"))

    fig_amount_3=px.bar(df_3, x="AppOpens",y="Districts",   title="AVERAGE OF APPOPENS",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Oryel_r,height=800,width=1000, hover_name="Districts")
    st.plotly_chart(fig_amount_3)

#MYsql connection

def top_chart_registered_users(table_name):
    mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd="ajaysuria@070",
        auth_plugin='mysql_native_password',
        database="Phonepe_data")
    mycursor=mydb.cursor(buffered=True)

    #plot_1
    query1= f'''SELECT States, SUM(RegisteredUsers) as RegisteredUsers
                FROM {table_name}
                group by States
                order by RegisteredUsers desc
                limit 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "RegisteredUsers"))

    col1,col2= st.columns(2)

    with col1:

        fig_amount_1=px.bar(df_1, x="States", y="RegisteredUsers", title="TOP 10 OF REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Brwnyl_r,height=650,width=600, hover_name="States")
        st.plotly_chart(fig_amount_1)

    #plot_2
    query2= f'''SELECT States, SUM(RegisteredUsers) as RegisteredUsers
                FROM {table_name}
                group by States
                order by RegisteredUsers 
                limit 10'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "RegisteredUsers"))

    with col2:

        fig_amount_2=px.bar(df_2, x="States", y="RegisteredUsers", title="LAST 10 REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Cividis_r,height=700,width=650, hover_name="States")
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT States, AVG(RegisteredUsers) as RegisteredUsers
                FROM {table_name}
                group by States
                order by RegisteredUsers 
                ;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "RegisteredUsers"))

    fig_amount_3=px.bar(df_3, x="RegisteredUsers",y="States",   title="AVERAGE OF REGISTERED USERS",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Oryel_r,height=800,width=1000, hover_name="States")
    st.plotly_chart(fig_amount_3)


#Streamlit Part

st.set_page_config(layout="wide")
st.title(":red[GUVI_PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")

with st.sidebar:
    
    select=option_menu("Main Menu",["Home","DATA EXPLORATION","TOP CHARTS"])

if select== "Home":
    col1,col2= st.columns(2)

    with col1:
        st.image(Image.open("D:\Data science\Project 2\photo1.jpg"))
        st.video("D:\Data science\Project 2\PhonePe - Introduction.mp4")
        
    with col2:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES:****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.image(Image.open("D:\Data science\Project 2\image_processing20200114-26356.jpg"))
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")


    col3,col4= st.columns(2)
    
    with col3:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    with col4:
        st.image(Image.open("D:\Data science\Project 2\PhonePe first fintech firm to allow international payments1675763759900.jpg"))


    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

elif select== "DATA EXPLORATION":

    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method=st.radio("Select The Method",["Insurance Analysis","Transacton Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",aggregated_insurance["Years"].unique().min(),aggregated_insurance["Years"].unique().max(),aggregated_insurance["Years"].unique().min())
            tac_Y= Transaction_amount_count_Y(aggregated_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",tac_Y["Quarter"].unique().min(),tac_Y["Quarter"].unique().max(),tac_Y["Quarter"].unique().min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)

        elif method == "Transacton Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",aggregated_transaction["Years"].unique().min(),aggregated_transaction["Years"].unique().max(),aggregated_transaction["Years"].unique().min())
            Agg_tran_tac_Y= Transaction_amount_count_Y(aggregated_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Agg_tran_tac_Y["States"].unique())

            Agg_tran_transaction_type(Agg_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",Agg_tran_tac_Y["Quarter"].unique().min(),Agg_tran_tac_Y["Quarter"].unique().max(),Agg_tran_tac_Y["Quarter"].unique().min())
            Agg_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Agg_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", Agg_tran_tac_Y_Q["States"].unique())

            Agg_tran_transaction_type(Agg_tran_tac_Y_Q, states)

        elif method == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",aggregated_users["Years"].unique().min(),aggregated_users["Years"].unique().max(),aggregated_users["Years"].unique().min())
            Aggre_user_Y= Aggre_user_plot_1(aggregated_users,years)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].unique().min(),Aggre_user_Y["Quarter"].unique().max(),Aggre_user_Y["Quarter"].unique().min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    
    with tab2:

        method2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",map_insurance["Years"].unique().min(),map_insurance["Years"].unique().max(),map_insurance["Years"].unique().min(),key="unique_key")
            map_insur_tac_Y= Transaction_amount_count_Y(map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())

            Map_insur_District(map_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",map_insur_tac_Y["Quarter"].unique().min(),map_insur_tac_Y["Quarter"].unique().max(),map_insur_tac_Y["Quarter"].unique().min(),key="unique_key_2")
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_insur_tac_Y_Q["States"].unique())

            Map_insur_District(map_insur_tac_Y_Q, states)

        elif method2 == "Map Transaction":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",map_transaction["Years"].unique().min(),map_transaction["Years"].unique().max(),map_transaction["Years"].unique().min(),key="unique_key_3")
            map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mt", map_tran_tac_Y["States"].unique())

            Map_insur_District(map_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",map_tran_tac_Y["Quarter"].unique().min(),map_tran_tac_Y["Quarter"].unique().max(),map_tran_tac_Y["Quarter"].unique().min(),key="unique_key_4")
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
               
                states= st.selectbox("Select The State_mt", map_tran_tac_Y_Q["States"].unique(),key='unique_key18')

            Map_insur_District(map_tran_tac_Y_Q, states)

        elif method2 == "Map User":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",map_user["Years"].unique().min(),map_user["Years"].unique().max(),map_user["Years"].unique().min(),key="unique_key_5")
            Map_user_Y= map_user_plot_1(map_user, years)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",Map_user_Y["Quarter"].unique().min(),Map_user_Y["Quarter"].unique().max(),Map_user_Y["Quarter"].unique().min(),key="unique_key_6")
            Map_user_Y_Q= map_user_plot_2(Map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                
                states= st.selectbox("Select The State_mu", Map_user_Y_Q["States"].unique())
            map_user_plot_3(Map_user_Y_Q, states)

    with tab3:

        method3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method3 == "Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",top_insurance["Years"].unique().min(),top_insurance["Years"].unique().max(),top_insurance["Years"].unique().min(),key="unique_key_7")
            top_insur_tac_Y= Transaction_amount_count_Y(top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                
                states= st.selectbox("Select The State_ti", top_insur_tac_Y["States"].unique())
            top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",top_insur_tac_Y["Quarter"].unique().min(),top_insur_tac_Y["Quarter"].unique().max(),top_insur_tac_Y["Quarter"].unique().min(),key="unique_key_9")
            top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)           


        elif method3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",top_transaction["Years"].unique().min(),top_transaction["Years"].unique().max(),top_transaction["Years"].unique().min(),key="unique_key_10")
            top_tran_tac_Y= Transaction_amount_count_Y(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                
                states= st.selectbox("Select The State_ti", top_tran_tac_Y["States"].unique())
            top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                
                quarters= st.slider("Select The Quarter",top_tran_tac_Y["Quarter"].unique().min(),top_tran_tac_Y["Quarter"].unique().max(),top_tran_tac_Y["Quarter"].unique().min(),key="unique_key_11")
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)

        elif method3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",top_users["Years"].unique().min(),top_users["Years"].unique().max(),top_users["Years"].unique().min(),key="unique_key_12")
            top_user_Y= top_user_plot_1(top_users, years)

            col1,col2= st.columns(2)
            with col1:
                
                states= st.selectbox("Select The State_tu", top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, states)            

elif select== "TOP CHARTS":
    
    question= st.selectbox("Select The Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                  "2. App Opens of Map User",
                                                  "3. Registered User of Top User",
                                                  "4. Registered User of Map User",
                                                  "5. Transaction Amount and Count of Map Insurance",
                                                  "6. Transaction Amount and Count of Top Insurance",
                                                  "7. Transaction Amount and Count of Aggregated Transaction",
                                                  "8. Transaction Amount and Count of Map Transaction",
                                                  "9. Transaction Amount and Count of Top Transaction",
                                                  "10. Transaction Count of Aggregated User",
                                                    ])
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
    
    elif question ==  "2. App Opens of Map User":
        
        states= st.selectbox("Select the State", map_user["States"].unique())
        st.subheader("APP OPENS")
        top_chart_appopens("map_user", states)
        
    elif question ==  "3. Registered User of Top User":
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_users")

    elif question ==  "4. Registered User of Map User":
        
        states= st.selectbox("Select the State", map_user["States"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_user", states)

    elif question ==  "5. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question ==  "6. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
    

    elif question ==  "7. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
    

    elif question ==  "8. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question ==  "9. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")


    elif question ==  "10. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_users")
    









