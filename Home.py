import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

####################################################################
########################## initial set up ##########################
####################################################################
st.set_page_config(page_title= "2023AI作業",
                page_icon = "🤖",
                layout='wide', 
                initial_sidebar_state='expanded')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# ####################################################################
# ########################## menu on sidebar #########################
# ####################################################################
with st.sidebar:
    selected = option_menu(
        menu_title = "2023SOS AI改作業", 
        options=["分佈", "啞鈴圖"], 
        icons = ["bar-chart-line-fill", "balloon-fill"],# https://icons.getbootstrap.com/
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
####################################################################
############################### data ###############################
####################################################################
result_df = pd.read_csv("https://raw.githubusercontent.com/lnl1119/2023SOS_result/main/2023SOS_result_all_clean_final.csv")
####################################################################
############################# variable #############################
####################################################################
teacher_color = "#00a1de"
AI_color = "#ff7f50"
AIgreaterthanteacher_color='#cb2c31' #dark red
teachergreaterthanAI_color='#6897bb' #dark blue
####################################################################
############################# function #############################
####################################################################
# plot bar
def bar_plot(bar_df):
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
    bar_df['realInterval'] = pd.cut(bar_df['realscore'], bins=bins, labels=labels, right=False)
    bar_df['AIInterval'] = pd.cut(bar_df['AIscore'], bins=bins, labels=labels, right=False)
    realcounts = bar_df['realInterval'].value_counts(sort=False)
    AIcounts = bar_df['AIInterval'].value_counts(sort=False)
    combine_count_df = pd.concat([realcounts, AIcounts], axis = 1)
    combine_count_df.columns = ["teacher", "AI"]

    fig1 = go.Figure(data=[
            go.Bar(name='Teacher', 
                   x=labels, y=realcounts, 
                   marker_color = teacher_color),
            go.Bar(name='AI', 
                   x=labels, y = AIcounts, 
                   marker_color = AI_color),
                   ])
    # Change the bar mode
    fig1.update_layout(barmode='group')
    fig1.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig1, use_container_width=True,height=700, theme="streamlit")

def area_plot(bar_df):
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
    bar_df['realInterval'] = pd.cut(bar_df['realscore'], bins=bins, labels=labels, right=False)
    bar_df['AIInterval'] = pd.cut(bar_df['AIscore'], bins=bins, labels=labels, right=False)
    realcounts = bar_df['realInterval'].value_counts(sort=False)
    AIcounts = bar_df['AIInterval'].value_counts(sort=False)
    combine_count_df = pd.concat([realcounts, AIcounts], axis = 1)
    combine_count_df.columns = ["teacher", "AI"]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=labels, y=realcounts,
        text = realcounts, textposition="top left", 
        textfont=dict(
            size=20,
            color = teacher_color),
        name = "Teacher",
        marker = dict(color = teacher_color),
        mode="lines+markers+text", fill='tozeroy')) # fill down to xaxis
    fig2.add_trace(go.Scatter(
        x=labels, y=AIcounts, 
        text = AIcounts, textposition="top right", 
        textfont=dict(
            size=20,
            color = AI_color),
        name = "AI",
        marker = dict(color = AI_color),
        mode="lines+markers+text", fill='tonexty')) # fill to trace0 y

    st.plotly_chart(fig2, use_container_width=True,height=700, theme="streamlit")

# plot dumbbell
def dumbbell_plot(df, show_dashline):
    fig3= go.Figure()
    fig3.add_trace(
        go.Scatter(x = df.index,
                y = df["realscore"],
                mode = 'markers',
                marker=dict(
                        color=teacher_color,
                        size=6,
                        line=dict(
                            color='MediumPurple',
                            width=1
                        )
                    ),
                legendgroup="group1",
                legendgrouptitle_text="First Group Title",
                name = 'Teacher'))
    fig3.add_trace(
        go.Scatter(x = df.index,
                y = df["AIscore"],
                mode = 'markers',
                marker=dict(
                        color=AI_color,
                        size=6,
                        line=dict(
                            color='MediumPurple',
                            width=1
                        )
                    ),
                legendgroup="group1",
                name = 'AI'))
    for i in range(len(df)):
        if df["change"][i] > 0: # AI> teacher
            fig3.add_shape(
                type='line',
                x0 = i, y0 = df["realscore"][i],
                x1 = i, y1 = df["AIscore"][i],
                line=dict(color=AIgreaterthanteacher_color, width = 2)) #dark red
        elif df["change"][i] < 0: # AI < teacher
            fig3.add_shape(
                type='line',
                x0 = i, y0 = df["realscore"][i],
                x1 = i, y1 = df["AIscore"][i],
                line=dict(color=teachergreaterthanAI_color, width = 2)) # dark blue
    
    # plot vertical line to split negative and positve
    if show_dashline:
        fig3.add_shape(type='line',
                        x0 = df_n.shape[0]-0.5, y0 = 120,
                        x1 = df_n.shape[0]-0.5, y1 = 0,
                        line=dict(color='grey', width = 1, dash = "dashdot"))
        fig3.add_shape(type='line',
                        x0 = df_n.shape[0]+df_0.shape[0]-0.5, y0 = 120,
                        x1 = df_n.shape[0]+df_0.shape[0]-0.5, y1 = 0,
                        line=dict(color='grey', width = 1, dash = "dashdot"))
        # text
        fig3.add_annotation(x=45, y=110,
                text="老師 > AI",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color=teachergreaterthanAI_color))
        fig3.add_annotation(x=125, y=110,
                text="AI > 老師",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color=AIgreaterthanteacher_color))
    fig3.update_layout(autosize=False,width=1500,height=700,
                    title_text = "AI grading system in comparison to teacher's grading",
                    title_font_size = 20, 
                    xaxis_title="ID",
                    yaxis_title="分數")
    fig3.update_yaxes(range=[0, 120])

    st.plotly_chart(fig3, use_container_width=True,height=700, theme="streamlit")#

# #####################################################
# ####################### page 1 ######################
# #####################################################
result_df = result_df.sort_values(by=['realscore'])
result_df = result_df.reset_index(drop = True)

if selected == "分佈":#st.title(f"{selected}")
    st.markdown('## 成績分布')
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(
    #     x = result_df.index, 
    #     y = result_df["realscore"], 
    #     fill='tonexty',
    #     marker = dict(color = teacher_color),
    #     name = "Teacher",
    #     #mode = "none"
    #     mode='lines+markers'
    #     ))
    # fig.add_trace(go.Scatter(
    #     x = result_df.index, y = result_df["AIscore"], 
    #     fill='tozeroy',
    #     marker = dict(color = AI_color),
    #     name = "AI",
    #     # mode = "none"
    #     mode='lines+markers',
    #     ))
    # st.plotly_chart(fig, use_container_width=True,height=700, theme="streamlit")


    # each grade count
    tab1, tab2 = st.tabs(["📈直方圖", "🔼面積圖"])
    with tab1:
        bar_plot(result_df)
    with tab2:
        area_plot(result_df)

# #####################################################
# ####################### page 2 ######################
# #####################################################

# data
raw_df = result_df[["realscore", "AIscore"]]
raw_df['change'] = raw_df.iloc[:, 1] - raw_df.iloc[:, 0]# AI - real
raw_df['absolutechange'] = raw_df['change'].abs()
df_n = raw_df[raw_df['change'] < 0]
df_0 = raw_df[raw_df['change'] == 0]
df_p = raw_df[raw_df['change'] > 0]

if selected == "啞鈴圖":
    st.markdown('## AI改作業結果')
    # button
    on = st.toggle('以老師與AI差異顯示')
    sort_option = st.radio(
        '選擇作為排列的項目',
        ('老師分數', 'AI分數', '差距'))

    st.divider()

    # condition
    if on:
        if sort_option == "老師分數":
            sort_condition = "realscore"
        elif sort_option == "AI分數":
            sort_condition = "AIscore"
        elif sort_option == "差距":
            sort_condition = "change"
        df_n = df_n.sort_values([sort_condition])
        df_n.reset_index(inplace = True)
        df_0 = df_0.sort_values([sort_condition], ascending=False)
        df_0.reset_index(inplace = True)
        df_p = df_p.sort_values([sort_condition], ascending=False)#, ascending=False
        df_p.reset_index(inplace = True)
        df_on = pd.concat([df_n, df_0, df_p], axis = 0)
        df_on.reset_index(inplace = True, drop = True)
        show_dashline = True
        dumbbell_plot(df_on, show_dashline)
        
    else:
        if sort_option == "老師分數":
            sort_condition = "realscore"
        elif sort_option == "AI分數":
            sort_condition = "AIscore"
        elif sort_option == "差距":
            sort_condition = "absolutechange"
        df_off = raw_df.sort_values([sort_condition], ascending=False)#, ascending=False
        df_off.reset_index(inplace = True, drop = True)
        show_dashline = False
        dumbbell_plot(df_off, show_dashline)
