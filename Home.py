import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
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
        options=["啞鈴圖", "分佈"], 
        icons = ["balloon-fill", "bar-chart-line-fill"],
        # options=["分佈", "啞鈴圖"], 
        # icons = ["bar-chart-line-fill", "balloon-fill"],# https://icons.getbootstrap.com/
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
############################# variable #############################
####################################################################
teacher_color = "#00a1de"
AI_color = "#ff7f50"
AIgreaterthanteacher_color='#cb2c31' #dark red #>0
teachergreaterthanAI_color='#6897bb' #dark blue #<0
####################################################################
############################# function #############################
####################################################################
def bins_function(start_num, end_num, range_differ):
    real_end = end_num + range_differ
    bin_list = list(range(start_num, real_end, range_differ))
    return bin_list
def labels_function(bins):
    label_list = [str(bins[i]) + "-" + str(bins[i+1]) for i in range(len(bins)-1)]
    return label_list

# plot bar
def bar_plot(bar_df):
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Teacher', 
                    x=labels_0100, y=realcounts, 
                    marker_color = teacher_color,
                    text = realcounts, textposition="outside", 
                    textfont=dict(size=13,color = teacher_color)))
    fig1.add_trace(go.Bar(name='AI', 
                    x=labels_0100, y = AIcounts, 
                    marker_color = AI_color,
                    text = AIcounts, textposition="outside", 
                    textfont=dict(size=13, color = AI_color)))
    fig1.update_layout(autosize=False,width=1500,height=700)
    fig1.update_layout(barmode='group')
    fig1.update_xaxes(title="級距")
    fig1.update_yaxes(title="數量", range=[0, 110])
    st.plotly_chart(fig1, use_container_width=True,height=700, theme="streamlit")

def area_plot(bar_df):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=labels_0100, y=realcounts,
        text = realcounts, textposition="top left", 
        textfont=dict(
            size=15,
            color = teacher_color),
        name = "Teacher",
        marker = dict(color = teacher_color),
        mode="lines+markers+text", fill='tozeroy')) # fill down to xaxis
    fig2.add_trace(go.Scatter(
        x=labels_0100, y=AIcounts, 
        text = AIcounts, textposition="top right", 
        textfont=dict(
            size=15,
            color = AI_color),
        name = "AI",
        marker = dict(color = AI_color),
        mode="lines+markers+text", fill='tonexty')) # fill to trace0 y
    fig2.update_layout(autosize=False,width=1500,height=700)
    fig2.update_xaxes(title="級距")
    fig2.update_yaxes(title="數量", range=[0, 110])
    st.plotly_chart(fig2, use_container_width=True,height=700, theme="streamlit")

# plot dumbbell
def dumbbell_plot(df, AI_teacher_split, show_differlabel, score_differ):
    fig3= go.Figure()
    fig3.add_trace(go.Scatter(x = df.index,
                        y = df["realscore"],
                        mode = 'markers',
                        marker=dict(color=teacher_color,size=6,
                                line=dict(color='MediumPurple',width=1)),
                        name = 'Teacher'))
    fig3.add_trace(go.Scatter(x = df.index,
                        y = df["AIscore"],
                        mode = 'markers',
                        marker=dict(color=AI_color,size=6,
                                line=dict(color='MediumPurple',width=1)),
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
    
    # add change text to each line
    for i in range(df.shape[0]):
        change = df.iloc[i, 3]
        color=AIgreaterthanteacher_color if(change>0) else teachergreaterthanAI_color 
        y_position = df.iloc[i,2]+5 if change > 0 else df.iloc[i,2]-3
        if change >= show_differlabel or change <= -show_differlabel:
            fig3.add_annotation(x=df.index[i], y=y_position,# +random.randint(1,5),
                yanchor= "auto",
                text=str(change),
                showarrow=False,
                font=dict(size=show_differlabel*0.2+10,color=color))
    
    if AI_teacher_split:
        df_differ_n = raw_df[raw_df['change'] < -score_differ]
        df_differ_0 = raw_df[(raw_df['change'] <= score_differ) & (raw_df['change'] >= -score_differ)]
        df_differ_p = raw_df[raw_df['change'] > score_differ]
        # plot vertical line to split negative and positve
        fig3.add_shape(type='line',
                        x0 = df_differ_n.shape[0]-0.5, y0 = 105,
                        x1 = df_differ_n.shape[0]-0.5, y1 = 0,
                        line=dict(color='grey', width = 1, dash = "dashdot"))
        fig3.add_shape(type='line',
                        x0 = df_differ_n.shape[0]+df_differ_0.shape[0]-0.5, y0 = 105,
                        x1 = df_differ_n.shape[0]+df_differ_0.shape[0]-0.5, y1 = 0,
                        line=dict(color='grey', width = 1, dash = "dashdot"))
        # text
        fig3.add_annotation(x=df_differ_n.shape[0]/2, y=110,
                text="AI < 老師",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color=teachergreaterthanAI_color))
        fig3.add_annotation(x=df_differ_n.shape[0]/2, y=105,
                text=f"({int(100*df_differ_n.shape[0]/df.shape[0])}%)",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color=teachergreaterthanAI_color))
        fig3.add_annotation(x=df_differ_n.shape[0]+(df_differ_0.shape[0]/2), y=110,
                text="老師 = AI",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color="grey"))
        fig3.add_annotation(x=df_differ_n.shape[0]+(df_differ_0.shape[0]/2), y=105,
                text=f"({int(100*df_differ_0.shape[0]/df.shape[0])}%)",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color="grey"))
        fig3.add_annotation(x=df.shape[0]-df_differ_p.shape[0]/2, y=110,
                text="AI > 老師",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color=AIgreaterthanteacher_color))
        fig3.add_annotation(x=df.shape[0]-df_differ_p.shape[0]/2, y=105,
                text=f"({int(100*df_differ_p.shape[0]/df.shape[0])}%)",
                showarrow=False,
                yshift=10,
                font=dict(size=20,color=AIgreaterthanteacher_color))
        
    fig3.update_layout(autosize=False,width=1500,height=700,
                    title_text = "🏋️老師與AI分數啞鈴圖",
                    title_font_size = 20,
                    xaxis_rangeslider_visible=True)
    fig3.update_xaxes(title="每一位學生", showticklabels=False, visible = False)
    fig3.update_yaxes(title="分數", range=[0, 120])

    st.plotly_chart(fig3, use_container_width=True,height=700, theme="streamlit")#


# AI teacher differ count(dataprocess and plot)
def AI_teacher_differ_count_bar_plot(df_n, df_p, bins_type, labels_type):
    n_change_interval = pd.cut(df_n['absolutechange'], 
                            bins=bins_type, labels=labels_type, right=False)
    n_changecounts_df = pd.DataFrame(n_change_interval.value_counts(sort=False))
    n_changecounts_df.columns = ["nchange"]

    p_change_interval = pd.cut(df_p['absolutechange'], 
                            bins=bins_type, labels=labels_type, right=False)
    p_changecounts_df = pd.DataFrame(p_change_interval.value_counts(sort=False))
    p_changecounts_df.columns = ["pchange"]

    np_changecounts_df = pd.concat([p_changecounts_df, n_changecounts_df],axis = 1)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name='AI>teacher', 
                    x=labels_type, y = np_changecounts_df["pchange"], 
                    marker_color = AIgreaterthanteacher_color,
                    text = np_changecounts_df["pchange"], textposition="inside", 
                    textfont=dict(size=13,color = "white")))
    fig4.add_trace(go.Bar(name='teacher>AI', 
                    x=labels_type, y = np_changecounts_df["nchange"], 
                    marker_color = teachergreaterthanAI_color,
                    text = np_changecounts_df["nchange"], textposition="inside", 
                    textfont=dict(size=13,color = "white")))
    fig4.update_layout(autosize=False,width=1500,height=700,
                    title_text = "📊老師與AI分數差距各級距數量直方圖",
                    title_font_size = 20, barmode='stack')
    fig4.update_xaxes(title="級距")
    fig4.update_yaxes(title="數量", range=[0, 90])
    st.plotly_chart(fig4, use_container_width=True,height=800, theme="streamlit")

####################################################################
########################### data process ###########################
####################################################################
result_df = pd.read_csv("https://raw.githubusercontent.com/lnl1119/2023SOS_result/main/2023SOS_result_all_clean_final.csv")
# bar and area plot data
bar_df = result_df.sort_values(by=['realscore'])
bar_df = bar_df.reset_index(drop = True)

# bin, label
bins_0100 = bins_function(0, 100, 10)
labels_0100 = labels_function(bins_0100)
bins_080 = bins_function(0, 80, 5)
labels_080 = labels_function(bins_080)
bar_df['realInterval'] = pd.cut(bar_df['realscore'], bins=bins_0100, labels=labels_0100, right=False)
bar_df['AIInterval'] = pd.cut(bar_df['AIscore'], bins=bins_0100, labels=labels_0100, right=False)
realcounts = bar_df['realInterval'].value_counts(sort=False)
AIcounts = bar_df['AIInterval'].value_counts(sort=False)
# dumbbell plot
raw_df = result_df[["realscore", "AIscore"]]
raw_df['change'] = raw_df.iloc[:, 1] - raw_df.iloc[:, 0]# AI - real
raw_df['absolutechange'] = raw_df['change'].abs()
# AI and teacher difference for histogram(show all range in bin)
df_n = raw_df[raw_df['change'] < 0]
df_0 = raw_df[raw_df['change'] == 0]
df_p = raw_df[raw_df['change'] > 0]


# #####################################################
# ####################### page 1 ######################
# #####################################################
if selected == "分佈":#st.title(f"{selected}")
    st.markdown('## 老師與AI給成績分布')
    # each grade count
    tab1, tab2 = st.tabs(["📈直方圖", "🔼面積圖"])
    with tab1:
        bar_plot(result_df)
    with tab2:
        area_plot(result_df)
# #####################################################
# ####################### page 2 ######################
# #####################################################
if selected == "啞鈴圖":
    st.markdown('## AI改作業結果')
    st.markdown('### 選項')
    # toggle 
    on = st.toggle('#### 1️⃣ 分開**老師>AI** 與 **老師<AI**', value = True)
    st.markdown('#### 2️⃣ 選擇**排序項目**')
    # radio list
    sort_option = st.radio(
        '',
        ('老師分數', 'AI分數', '差距'))
    # slider
    col1, col2= st.columns(2)#[0.3,0.7]
    with col1:
        st.markdown('#### 3️⃣ 你可以接受？分的**老師與AI分數誤差**')
        score_differ = st.slider('', 0, 50, 5)
    with col2:
        st.markdown('#### 4️⃣ 顯示？分以上的**分數差距標籤**（數字越大，顯示的標籤越少）')
        show_differlabel = st.slider('', 0, 50, 25)

    st.divider()

    # condition
    if on:
        if sort_option == "老師分數":
            sort_condition = "realscore"
        elif sort_option == "AI分數":
            sort_condition = "AIscore"
        elif sort_option == "差距":
            sort_condition = "change"
        
        # score_differ
        df_differ_n = raw_df[raw_df['change'] < -score_differ]
        df_differ_0 = raw_df[(raw_df['change'] <= score_differ) & (raw_df['change'] >= -score_differ)]
        df_differ_p = raw_df[raw_df['change'] > score_differ]
        # scorediffer_n_shape = df_differ_n.shape[0]
        # scorediffer_0_shape = df_differ_0.shape[0]
        # scorediffer_p_shape = df_differ_p.shape[0]



        df_differ_n.sort_values([sort_condition], inplace = True)
        df_differ_n.reset_index(inplace = True)
        df_differ_0.sort_values([sort_condition], ascending=False, inplace = True)
        df_differ_0.reset_index(inplace = True)
        df_differ_p.sort_values([sort_condition], ascending=False, inplace = True)#, ascending=False
        df_differ_p.reset_index(inplace = True)
        df_on = pd.concat([df_differ_n, df_differ_0, df_differ_p], axis = 0)
        df_on.reset_index(inplace = True, drop = True)

        AI_teacher_split = True
        dumbbell_plot(df_on, AI_teacher_split, show_differlabel, score_differ)
        # st.table(df_on.head())
        
    else:
        if sort_option == "老師分數":
            sort_condition = "realscore"
        elif sort_option == "AI分數":
            sort_condition = "AIscore"
        elif sort_option == "差距":
            sort_condition = "change"#absolutechange
        df_off = raw_df.sort_values([sort_condition], ascending=False)#, ascending=False
        df_off.reset_index(inplace = True)

        AI_teacher_split = False
        dumbbell_plot(df_off, AI_teacher_split, show_differlabel, score_differ)
        # st.table(raw_df.head())

    
    AI_teacher_differ_count_bar_plot(df_n, df_p, bins_080, labels_080)

    

