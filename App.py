import streamlit as st
import pandas as pd
import  numpy as np
import altair as alt

df = pd.read_excel (  
    io='./datasets/system_extraction.xlsx',
    engine='openpyxl',
    sheet_name='salesreport',
    usecols='A:J',
    nrows=4400
)

with st.sidebar:
    st.subheader("Menu dashboar de Vendas")
    fVendedor = st.selectbox (
        'Selecione o vendedor',
        options=df['Vendedor'].unique()
        )
    fProduto = st.selectbox(
        'Selecione o produto',
        options=df['Produto vendido'].unique()
    )
    fCliente =  st.selectbox(
        'Selecione o cliente',
        options=df['Cliente'].unique())

#Vendas por produto   
tab1_qte_produto_vendido = df.loc[(
        df['Vendedor'] == fVendedor) & 
        (df['Cliente'] == fCliente)
    ]

tab1_qte_produto_vendido = tab1_qte_produto_vendido.groupby("Produto vendido").sum(numeric_only=True).reset_index()

tab1_qte_produto_vendido

#Vendas margem
tab_vendas_margem = df.loc[
    (df['Vendedor'] == fVendedor) & 
    (df['Cliente'] == fCliente) & 
    (df['Produto vendido'] == fProduto)
]

tab_vendas_margem

#Vendas por vendedor 

tab_vendas_por_vendedor = df.loc[
    ((df['Produto vendido']) == fProduto) &
    (df['Cliente'] == fCliente )
].groupby('Vendedor').sum(numeric_only=True).reset_index().drop(columns=["Nº pedido","Preço"])

tab_vendas_por_vendedor

#Vendas por Cliente 

tab_vendas_cliente = df.loc[
      ((df['Produto vendido']) == fProduto) &
      (df['Vendedor'] == fVendedor)
].groupby('Cliente').sum(numeric_only=True).reset_index()

tab_vendas_cliente

#Vendas Mensasis 

tab_vendas_mensais = df.loc[  
    ((df['Produto vendido']) == fProduto) &
    (df['Vendedor'] == fVendedor) & 
    (df['Cliente'] == fCliente )
]
tab_vendas_mensais["mm"] = tab_vendas_mensais['Data'].dt.strftime('%m/%Y')
tab_vendas_mensais


# Gráficos das tabelas 
#PADROES
cor_grafico = '#000000'
#------------------------
# Grafico qte vendida por produto

graf_qte_vendida_produto = alt.Chart(tab1_qte_produto_vendido).mark_bar(
    color= cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusBottomRight=9,

).encode(
    x = 'Produto vendido',
    y = 'Quantidade',
    tooltip=['Produto vendido','Quantidade']
).properties(title="QUANTIDADE VENDIDA POR PRODUTO"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

st.altair_chart(graf_qte_vendida_produto)


# Grafico valor de venda por produto

graf_valor_venda_produto = alt.Chart(tab1_qte_produto_vendido).mark_bar(
    color= cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusBottomRight=9,

).encode(
    x = 'Produto vendido',
    y = 'Valor Pedido',
    tooltip=['Produto vendido','Valor Pedido']
).properties(title="QUANTIDADE DE VALOR POR PRODUTO"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

st.altair_chart(graf_valor_venda_produto)


# Gráfico vendas por vendedor

graf_vendas_por_vendedor = alt.Chart(tab_vendas_por_vendedor).mark_arc( 
    innerRadius=100,
    outerRadius=150
).encode(
    theta=alt.Theta(field='Valor Pedido',type='quantitative',stack=True),
    color=alt.Color(
        field='Vendedor',
        type='nominal'
    ),
    tooltip=["Vendedor",'Valor Pedido']
).properties(height=500, width=560, title='Valor de venda por vendedor')
rot2Ve = graf_vendas_por_vendedor.mark_text(radius=210,size=14).encode(text='Vendedor')
rot2Vp = graf_vendas_por_vendedor.mark_text(radius=180,size=14).encode(text='Valor Pedido')

st.altair_chart(graf_vendas_por_vendedor + rot2Ve + rot2Vp)


# Grafico qte vendida por Cliente

graf_qte_vendida_cliente = alt.Chart(tab_vendas_cliente).mark_bar(
    color= cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusBottomRight=9,

).encode(
    x = 'Cliente',
    y = 'Valor Pedido',
    tooltip=['Quantidade','Valor Pedido']
).properties(title="QUANTIDADE VENDIDA POR CLIENTE"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

st.altair_chart(graf_qte_vendida_cliente)


# Grafico vendas mensais 
graf_vendas_mensais = alt.Chart(tab_vendas_mensais).mark_line(
    color=cor_grafico
).encode( 
    alt.X('monthdate(Data):T'),
    y = "Valor Pedido:Q",
    tooltip=['Valor Pedido']
).properties(title='VENDAS MENSAIS'
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)

st.altair_chart(graf_vendas_mensais)