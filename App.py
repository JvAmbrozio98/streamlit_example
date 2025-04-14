import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Leitura dos dados do Excel
df = pd.read_excel(  
    io='./datasets/system_extraction.xlsx',
    engine='openpyxl',
    sheet_name='salesreport',
    usecols='A:J',
    nrows=4400
)

# Cor padrão dos gráficos
cor_grafico = '#000000'

# Sidebar - Filtros de seleção
with st.sidebar:
    st.subheader("Dashboard de Vendas")
    fVendedor = st.selectbox(
        'Selecione o vendedor',
        options=df['Vendedor'].unique()
    )
    fProduto = st.selectbox(
        'Selecione o produto',
        options=df['Produto vendido'].unique()
    )
    fCliente = st.selectbox(
        'Selecione o cliente',
        options=df['Cliente'].unique()
    )

# ================================================================================
# Gráfico 1: Quantidade vendida por produto
tab1_qte_produto_vendido = df.loc[
    (df['Vendedor'] == fVendedor) & 
    (df['Cliente'] == fCliente)
]

tab1_qte_produto_vendido = tab1_qte_produto_vendido.groupby("Produto vendido").sum(numeric_only=True).reset_index()

graf_qte_vendida_produto = alt.Chart(tab1_qte_produto_vendido).mark_bar(
    color=cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusBottomRight=9
).encode(
    x='Produto vendido',
    y='Quantidade',
    tooltip=['Produto vendido', 'Quantidade']
).properties(title="QUANTIDADE VENDIDA POR PRODUTO"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

# ================================================================================
# Gráfico 2: Valor de venda por produto
tab_vendas_margem = df.loc[
    (df['Vendedor'] == fVendedor) & 
    (df['Cliente'] == fCliente) & 
    (df['Produto vendido'] == fProduto)
]

graf_valor_venda_produto = alt.Chart(tab1_qte_produto_vendido).mark_bar(
    color=cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusBottomRight=9
).encode(
    x='Produto vendido',
    y='Valor Pedido',
    tooltip=['Produto vendido', 'Valor Pedido']
).properties(title="VALOR TOTAL POR PRODUTO"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

# ================================================================================
# Gráfico 3: Valor de venda por vendedor
tab_vendas_por_vendedor = df.loc[
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
].groupby('Vendedor').sum(numeric_only=True).reset_index().drop(columns=["Nº pedido", "Preço"])

graf_vendas_por_vendedor = alt.Chart(tab_vendas_por_vendedor).mark_arc( 
    innerRadius=100,
    outerRadius=150
).encode(
    theta=alt.Theta(field='Valor Pedido', type='quantitative', stack=True),
    color=alt.Color(field='Vendedor', type='nominal'),
    tooltip=["Vendedor", 'Valor Pedido']
).properties(height=500, width=560, title='VALOR DE VENDA POR VENDEDOR')

# Rótulos do gráfico de pizza
rot2Ve = graf_vendas_por_vendedor.mark_text(radius=210, size=14).encode(text='Vendedor')
rot2Vp = graf_vendas_por_vendedor.mark_text(radius=180, size=14).encode(text='Valor Pedido')

# ================================================================================
# Gráfico 4: Valor vendido por cliente
tab_vendas_cliente = df.loc[
    (df['Produto vendido'] == fProduto) &
    (df['Vendedor'] == fVendedor)
].groupby('Cliente').sum(numeric_only=True).reset_index()

graf_qte_vendida_cliente = alt.Chart(tab_vendas_cliente).mark_bar(
    color=cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusBottomRight=9
).encode(
    x='Cliente',
    y='Valor Pedido',
    tooltip=['Quantidade', 'Valor Pedido']
).properties(title="VALOR VENDIDO POR CLIENTE"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

# ================================================================================
# Gráfico 5: Vendas mensais
tab_vendas_mensais = df.loc[  
    (df['Produto vendido'] == fProduto) &
    (df['Vendedor'] == fVendedor) & 
    (df['Cliente'] == fCliente)
].copy()

# Criando coluna com mês/ano
tab_vendas_mensais["mm"] = tab_vendas_mensais['Data'].dt.strftime('%m/%Y')

graf_vendas_mensais = alt.Chart(tab_vendas_mensais).mark_line(
    color=cor_grafico
).encode( 
    alt.X('monthdate(Data):T'),
    y='Valor Pedido:Q',
    tooltip=['Valor Pedido']
).properties(title='VENDAS MENSAIS'
).configure_axis(grid=False
).configure_view(strokeWidth=0)

# ================================================================================
# Exibindo os gráficos no Streamlit
st.altair_chart(graf_qte_vendida_produto)
st.altair_chart(graf_valor_venda_produto)
st.altair_chart(graf_qte_vendida_cliente)
st.altair_chart(graf_vendas_mensais)
st.altair_chart(graf_vendas_por_vendedor + rot2Ve + rot2Vp)