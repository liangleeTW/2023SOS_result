import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import datetime

####################################################################
########################## initial set up ##########################
####################################################################

st.set_page_config(page_title= "ewant data dashboard",
                page_icon = "🌊",
                layout='wide', 
                initial_sidebar_state='expanded')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# import mysql.connector
# connection = mysql.connector.connect(**st.secrets.mysql)
# # mdl_user_info_field_query = "SELECT * FROM `mdl_user_info_field`"
# # field_df = pd.read_sql(mdl_user_info_field_query, con = connection).iloc[:, :2].set_index('id')
# # field_df_dict = list(field_df.to_dict(orient='dict').values())[0]
# field_df_dict = {
#     1: 'title',
#     2: 'unit',
#     3: 'dept',
#     4: 'gender',
#     5: 'age',
#     6: 'jobstatus',
#     7: 'company',
#     8: 'studystatus',
#     9: 'edulevel',
#     10: 'paycode',
#     12: 'birthday'
#     }

# #@st.cache_data(ttl=43200)
# mdl_user_info_data_query = "SELECT * FROM `mdl_user_info_data`"
# data_df = pd.read_sql(mdl_user_info_data_query, con = connection).set_index('id')
# data_df = data_df.replace({"fieldid": field_df_dict})
# nona_df = data_df[data_df["data"]!= ""]# na is represent as "", filter data that has no na
# gender_df = nona_df[nona_df["fieldid"] == "gender"]
# gender_df["data"] = gender_df["data"].str.replace(r'<[^<>]*>', '', regex=True)
# gender_replace_dict = {
#     'male男 ': '男', 
#     'please click未填 ': '未填',
#     '未填 ': '未填',
#     'female女 ': '女',
#     '女 ': '女', 
#     '男 ': '男', 
#     'please click ': '未填', 
#     '未填\r': '未填', 
#     '男\r': '男', 
#     'male ': '男', 
#     'female ': '女'
# }
# gender_df = gender_df.replace({"data": gender_replace_dict})
# #gender_df["data"].value_counts()
# gender_count_df = pd.DataFrame(gender_df["data"].value_counts()).reset_index()
# st.markdown('### 📩註冊者:blue[性別]分佈')
# gender_pie_chart = px.pie(gender_count_df, values='data', names='index')# , title = "註冊者信箱分佈"
# gender_pie_chart.update_traces(textposition='inside', textinfo='percent+label')
# st.plotly_chart(gender_pie_chart)

####################################################################
############################### data ###############################
####################################################################
login_20162022_raw = pd.read_csv("https://raw.githubusercontent.com/lnl1119/ewant_registration_datadashboard/main/login_2016to2022.csv")
register_20142022_raw = pd.read_csv("https://raw.githubusercontent.com/lnl1119/ewant_registration_datadashboard/main/register_2014to2022.csv")
register20230717_df = pd.read_csv("https://raw.githubusercontent.com/lnl1119/ewant_registration_datadashboard/main/registerdata20230717.csv")
####################################################################
############################# variable #############################
####################################################################

today_date = datetime.date.today()
yesterday_date = today_date - datetime.timedelta(days=1)
lastweek_date = today_date - datetime.timedelta(weeks=1)

register_year_list = [2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014]
login_year_list = [2022, 2021, 2020, 2019, 2018, 2017, 2016]
color_mapping = {
    2014: "#ffa500", 
    2015: "#c6e2ff",
    2016: "#008080",
    2017: "#0D1282",
    2018: "#F8DE22",
    2019: "#ff80ed",
    2020: "#D71313",
    2021: "#64CCC5",
    2022: "#ffa500",
}
# color_mapping = {
#     2016: 'rgb(255, 127, 14)',
#     2017: 'rgb(44, 160, 44)',
#     2018: 'rgb(214, 39, 40)',
#     2019: 'rgb(148, 103, 189)',
#     2020: 'rgb(140, 86, 75)',
#     2021: 'rgb(227, 119, 194)',
#     2022: 'rgb(127, 127, 127)',
# }

color_list = ["#ff80ed", "#000000", "#008080", "#ff0000", "#ffd700", 
"#ffa500", "#c6e2ff", "#0000ff"]
country_dict = {
    'TW' : '台灣', 'MY' : '馬來西亞', 'CN' : '中國大陸', 'VN' : '越南', 'PY' : '巴拉圭', 
    'HK' : '香港', 'ID' : '印尼', 'JP' : '日本', 'TH' : '泰國', 'MO' : '澳門',
    'US' : '美國', 'AL' : '阿爾巴尼亞', 'PK' : '巴基斯坦', 'AU' : '澳大利亞', 'AE' : '阿拉伯聯合大公國', 
    'GM' : '甘比亞', 'CA' : '加拿大', 'KR' : '韓國', 'DE' : '德國', 'PH' : '菲律賓', 
    'IE' : '愛爾蘭','CY' : '塞普路斯', 'GB' : '英國', 'FR' : '法國', 'LU' : '盧森堡', 
    'TF' : '法屬南部屬地', 'PM' : '聖匹及密啟倫群島', 'SV' : '薩爾瓦多', 'MS' : '蒙瑟拉特島', 'BH' : '巴林', 
    'AF' : '阿富汗', 'SD' : '蘇丹'
    }

####################################################################
############################# function #############################
####################################################################

def register_check_change():
    # this runs BEFORE the rest of the script whe  n a change is detected 
    # from your checkbox to set selectbox
    if st.session_state.register_all_option:
        st.session_state.register_year_select = register_year_list
    else:
        st.session_state.register_year_select = []
    return

def register_multi_change():
# this runs BEFORE the rest of the script when a change is detected
# from your selectbox to set checkbox
    if len(st.session_state.register_year_select) == len(register_year_list):
        st.session_state.register_all_option = True
    else:
        st.session_state.register_all_option = False
    return

def login_check_change():
    if st.session_state.login_all_option:
        st.session_state.login_year_select = login_year_list
    else:
        st.session_state.login_year_select = []
    return

def login_multi_change():
    if len(st.session_state.login_year_select) == len(login_year_list):
        st.session_state.login_all_option = True
    else:
        st.session_state.login_all_option = False
    return

####################################################################
########################## menu on sidebar #########################
####################################################################

# menu on sidebar
with st.sidebar:
    selected = option_menu(
        menu_title = "ewant資料", 
        options=["概覽", "註冊人數", "登入人數", "學員樣貌"], 
        icons = ["house-fill", "rocket-takeoff-fill", "bar-chart-line-fill", "folder-fill"],# https://icons.getbootstrap.com/
        menu_icon = "three-dots-vertical",
        default_index = 0,
        styles={
                #"container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#36b9cc"},
            },
    )

#####################################################
####################### page 1 ######################
#####################################################

if selected == "概覽":#st.title(f"{selected}")
    st.title(f"{selected}")
    total_registration_count = 482656
    lastweek_registration_count = 478731
    increasefromlastweek_total_registration_count = total_registration_count - lastweek_registration_count
    thisyear_registration_count = 44990
    lastyear_registration_count = 31573
    increasecomparelastyear_registration_count = thisyear_registration_count - lastyear_registration_count
    Acol1, Acol2, Acol3, Acol4 = st.columns(4)
    Acol1.metric("本週註冊人數", "{:,}".format(total_registration_count)+"人", str(increasefromlastweek_total_registration_count)+"人")
    Acol2.metric("上週註冊人數", "{:,}".format(lastweek_registration_count)+"人")
    Acol3.metric("本年度註冊人數", "{:,}".format(thisyear_registration_count)+"人", str(increasecomparelastyear_registration_count)+"人")
    Acol4.metric("近期增加人數原因：", "  ")
    # col1.metric("累積至昨日"+str(today_date), "70 °F", "1.2 °F")
    # col2.metric("昨日"+str(yesterday_date), "9 mph", "-8%")
    # col3.metric("上週"+str(lastweek_date), "86%", "4%")

#####################################################
####################### page 2 ######################
#####################################################

if selected == "註冊人數":
    st.markdown('## ewant平台每週註冊人數統計圖')
    st.divider()
    #st.subheader('💥每週註冊人數選項')    
    # register control
    if "register_all_option" not in st.session_state:
        st.session_state.register_all_option = True
        st.session_state.register_year_select = register_year_list

    register_year_select = st.multiselect("選擇一個或多個年份: ",
            register_year_list,key="register_year_select", on_change = register_multi_change)
    all = st.checkbox("全選", key='register_all_option',on_change= register_check_change)
    
    # register plot
    #Rtab1, Rtab2, Rtab3 = st.tabs(["📈折線圖", "🔼面積圖", "熱圖"])
    Rtab1, Rtab2 = st.tabs(["📈折線圖", "🔼面積圖"])
    with Rtab1:
        register_melt_df = register_20142022_raw.melt(id_vars=["week"])
        register_melt_df.columns = ["week", "year", "value"]
        register_melt_df['year'] = register_melt_df['year'].astype('int')
        filtered_register_melt_df = register_melt_df[register_melt_df['year'].isin(register_year_select)]

        fig = px.line(filtered_register_melt_df, x='week', y = "value", color='year', markers=True, color_discrete_map=color_mapping)
        fig.update_layout(xaxis_rangeslider_visible=True, height=700)
        fig.update_yaxes(title_text='數量')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True,height=700)
        #st.line_chart(register_20142022_raw, x = 'week', y = register_year_select, height = 500)
    with Rtab2:    
        fig = px.area(filtered_register_melt_df, x='week', y = "value", color='year', markers=True, color_discrete_map=color_mapping)
        fig.update_layout(xaxis_rangeslider_visible=True, height=700)
        fig.update_yaxes(title_text='數量')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True,height=700)
    # with Btab3:

#####################################################
####################### page 3 ######################
#####################################################

if selected == "登入人數":
    st.markdown('## ewant平台登入人數統計圖')
    st.divider()
    #st.subheader('💥每日登入人數選項')
    # login control
    if "login_all_option" not in st.session_state:
        st.session_state.login_all_option = True
        st.session_state.login_year_select = login_year_list

    login_year_select = st.multiselect("選擇一個或多個年份: ",
            login_year_list,key="login_year_select", on_change=login_multi_change)
    all = st.checkbox("全選", key='login_all_option',on_change = login_check_change)

    # login plot
    Ctab1, Ctab2 = st.tabs(["📈折線圖", "🔼面積圖"])
    with Ctab1:
        month_date = pd.date_range(start='2019/01/01', end='2019/12/31', freq='D').strftime("%b %d")
        login_2016_2022_df = login_20162022_raw.drop(["date"], axis = 1)
        login_2016_2022_df.insert(loc = 0, column='date', value = month_date)
        login_melt_df = login_2016_2022_df.melt(id_vars=["date"])
        login_melt_df.columns = ["date", "year", "value"]
        login_melt_df['year'] = login_melt_df['year'].astype('int')
        filtered_login_melt_df = login_melt_df[login_melt_df['year'].isin(login_year_select)]

        fig = px.line(filtered_login_melt_df, x='date', y = "value", color='year', markers=True, color_discrete_map=color_mapping)
        fig.update_layout(xaxis_rangeslider_visible=True, height=700)
        fig.update_yaxes(title_text='數量')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True,height=700)
        #st.line_chart(login_20162022_raw, x = 'date', y = login_year_select, height = 500)# , height = login_plot_height

    with Ctab2:    
        fig = px.area(filtered_login_melt_df, x='date', y = "value", color='year', markers=True, color_discrete_map=color_mapping)
        fig.update_layout(xaxis_rangeslider_visible=True, height=700)
        fig.update_yaxes(title_text='數量')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, height=700)
        #st.area_chart(login_20162022_raw, x = 'date', y = login_year_select, height = 500)# , height = login_plot_height

#####################################################
####################### page 4 ######################
#####################################################

if selected == "學員樣貌":
    # data preprocessing for register
    ## email domain
    email_list = register20230717_df["email"].values
    domain_name_list = [i[i.index('@') + 1 : ] for i in email_list]
    domain_list = ["edu.tw", "gmail", "qq", "yahoo", "hotmail"]
    each_domain_count_list = [len([i for i in domain_name_list if d in i]) for d in domain_list]
    data = {'domain': domain_list + ["other"],
            'count': each_domain_count_list + [len(domain_name_list) - sum(each_domain_count_list)]}
    domain_count_df = pd.DataFrame(data)


    ## country
    register20230717_df['country'] = register20230717_df['country'].replace(['""'], '未填')
    country_count_df = pd.DataFrame(register20230717_df['country'].value_counts())
    country_count_df.reset_index(inplace=True)
    country_count_df.columns = ["country", "count"]
    
    country_count_df.replace({"country": country_dict},inplace=True)

    ##########################################                     
    # plot pie chart
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('### 📩註冊者:blue[信箱]分佈')
        domain_max_type = domain_count_df['domain'][domain_count_df['count'] == domain_count_df['count'].max()].values[0]
        st.write(f"最多註冊者信箱網域為： :blue[{domain_max_type}]")
        email_pie_chart = px.pie(domain_count_df, values='count', names='domain')# , title = "註冊者信箱分佈"
        email_pie_chart.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(email_pie_chart)
        
        domain_expander = st.expander("點我查看資料")
        domain_expander.dataframe(
            domain_count_df,
            column_config={
                "domain": "網域",
                "count": "數量",
            },
            hide_index=True,
            use_container_width = True,
            height = 250
        )
        
    with c2:
        st.markdown('### 🇹🇼註冊者:blue[國家]分佈')
        country_max_type = country_count_df['country'][country_count_df['count'] == country_count_df['count'].max()].values[0]
        st.write(f"最多註冊者國家為： :blue[{country_max_type}]")
        country_pie_chart = px.pie(country_count_df, values='count', names='country')
        country_pie_chart.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(country_pie_chart)
        country_expander = st.expander("點我查看資料")
        #country_expander.table(country_count_df.head(30))
        country_expander.dataframe(
            country_count_df,
            column_config={
                "country": "國家",
                "count": "數量",
            },
            hide_index=True,
            use_container_width = True,
            height = 250
        )