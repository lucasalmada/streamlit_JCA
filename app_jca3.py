import pandas as pd  
import plotly.express as px  
import streamlit as st  
import random
from datetime import datetime



st.set_page_config(layout="wide")



df = pd.read_excel('operacional.xlsx')

df['Ano'] = df['ENTRADA'].apply(lambda x: x.year)
df['Mês'] = df['ENTRADA'].apply(lambda x: x.month)

df = df[df['Ano'] == 2024]

df['STATUS'] = df['STATUS'].replace({'AGUARDANDO APROVAÇÃO':'APROVADO PELO COMERCIAL',
                                     'EM MANUTENÇÃO':'APROVADO PELO COMERCIAL',
                                     'DEVOLVIDO':'APROVADO PELO COMERCIAL',
                                     'CONCLUÍDO':'MANUTENÇÃO CONCLUÍDA'})

# Usando a função pivot_table para calcular os totais por mês e status
pivot_df = pd.pivot_table(df, index='Mês', columns='STATUS', aggfunc='size', fill_value=0).reset_index()

# Calcular o total por mês
pivot_df['ENTRADAS GERAL'] = pivot_df.sum(axis=1)

# Melt para criar uma única coluna para os valores
melted_df = pivot_df.melt(id_vars='Mês', var_name='STATUS', value_name='Quantidade')

#Usar
#https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/


def grafico_barras(variavel):

    fig = px.bar(melted_df, x = 'Mês', y = 'Quantidade', title=f'Quantidade de processos por: {1}',color='STATUS', 
                 barmode='group',template="plotly_white",width=900, height=500)

    fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="rgba(0,0,0,0)", yaxis=(dict(showgrid=False)),)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))

    #fig.update_yaxes(tickfont=dict(size=8))
    #fig.update_xaxes(tickfont=dict(size=8))
    return fig

#--------MAINPAGE-----#
st.title(':bar_chart: Números anuais do operacional')
st.markdown("""---""")

# ---- SIDEBAR ----

st.sidebar.image('logo2.png', caption='Manutenção de motores')
st.sidebar.header("Adicione Filtros")
ano = st.sidebar.multiselect(
    "Selecione o ano:",
    options=df["Ano"].unique(),
    default=df["Ano"].unique()
)

status = st.sidebar.multiselect(
    "Selecione o STATUS:",
    options=df["STATUS"].unique(),
    default=df["STATUS"].unique()
)



df_selection = df.query(
    "Ano==@ano & STATUS==@status" 
)

#st.dataframe(df_selection)

col1, col2, col3,col4 = st.columns(4)
col1.metric("Manutenção concluída", "62 OS's")
col2.metric("Em manutenção", "15 OS's")
col3.metric("Aguardando aprovação", "8 OS's")
col4.metric("Equipamentos devolvidos", "3 OS's")

st.markdown("""---""")


col = st.columns((6, 2), gap='medium')

with col[0]:
    #st.markdown('#### Análise Gráfica')

    grafico1 = px.bar(melted_df, x = 'Mês', y = 'Quantidade', 
                  title=f'Análise geral',color='STATUS',barmode='group',text='Quantidade',height=400)

    grafico1.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="rgba(0,0,0,0)", yaxis=(dict(showgrid=False)),)
    st.plotly_chart(grafico1,use_container_width=True)


dados = [['Cliente 1',15],
         ['Cliente 2',9],
         ['Cliente 3',11],
         ['Cliente 4',8],
         ['Cliente 5',12],
         ['Cliente 1',15],
         ['Cliente 2',9],
         ['Cliente 3',11]]

df_clientes = pd.DataFrame(dados, columns = ['Cliente', 'Servicos'])



with col[1]:
    st.markdown('#### Top Clientes')
    # Função para criar as barras de progresso coloridas
    column_config = {
    "Cliente": st.column_config.TextColumn(
        "Cliente",
    ),
    "Servicos": st.column_config.ProgressColumn(
        "Serviços",
        format="%f",
        min_value=0,
        max_value=max(df_clientes['Servicos']),
    )
}

    # Formatar valores de Serviços para serem exibidos na barra de progresso
    # Exibir DataFrame com barras de progresso coloridas
    st.dataframe(df_clientes, column_config=column_config, hide_index=True,
                 width=None)


colz1,colz2 = st.columns(2)

with colz1:
    fig = px.bar(melted_df, x = 'Mês', y = 'Quantidade', 
                title=f'Quantidade de processos por: {1}',color='STATUS',barmode='group',text='Quantidade',height=300)
    st.plotly_chart(fig,use_container_width=True)

with colz2:
    fig = px.bar(melted_df, x = 'Mês', y = 'Quantidade', 
                title=f'Quantidade de processos por: {1}',color='STATUS',barmode='group',text='Quantidade',height=300)
    st.plotly_chart(fig,use_container_width=True)







