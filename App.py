import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime as dt

# Leitura dos dados do Excel
df = pd.read_excel(  
    io='./datasets/system_extraction.xlsx',
    engine='openpyxl',
    sheet_name='salesreport',
    usecols='A:J',
    nrows=4400
)

# Cor padrão dos gráficos
cor_grafico = '#9DD1F1'
altura_grafico=250
st.set_page_config(
    page_title='DASHBOARD DE VENDAS',
    page_icon='💲',
    layout='wide',
    initial_sidebar_state='expanded'
)
# Sidebar - Filtros de seleção
df['Data'] = pd.to_datetime(df['Data'])
max_data = df['Data'].max().to_pydatetime()
min_data = df['Data'].min().to_pydatetime()



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
    sliderTemporal = st.slider(
        label="Sei lá",
        min_value=min_data,
        max_value=max_data)

# ================================================================================
vendas_totais_absolutas = round(df['Valor Pedido'].sum(), 2)
lucro_total_empresa = round(df['Margem Lucro'].sum(), 2)
porcentagem_total = int(100 * lucro_total_empresa / vendas_totais_absolutas)


# ================================================================================
# Gráfico 1: Quantidade vendida por produto
tab1_qte_produto_vendido = df.loc[
    (df['Vendedor'] == fVendedor) & 
    (df['Cliente'] == fCliente) &
    (df['Data'] <= sliderTemporal )
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
).properties(height=altura_grafico,title="QUANTIDADE VENDIDA POR PRODUTO"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

# ================================================================================
# Gráfico 2: Valor de venda por produto
tab_vendas_margem = df.loc[
    (df['Vendedor'] == fVendedor) & 
    (df['Cliente'] == fCliente) & 
    (df['Produto vendido'] == fProduto) &
    (df['Data'] <= sliderTemporal )
]

graf_valor_venda_produto = alt.Chart(tab1_qte_produto_vendido).mark_bar(
    color=cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusBottomRight=9
).encode(
    x='Produto vendido',
    y='Valor Pedido',
    tooltip=['Produto vendido', 'Valor Pedido']
).properties(height=altura_grafico,title="VALOR TOTAL POR PRODUTO"
).configure_axis(grid=False
).configure_view(strokeWidth=0)

# ================================================================================
# Gráfico 3: Valor de venda por vendedor
tab_vendas_por_vendedor = df.loc[
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente) & 
    (df['Data'] <= sliderTemporal )
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
    (df['Vendedor'] == fVendedor) & 
    (df['Data'] <= sliderTemporal )
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
    (df['Cliente'] == fCliente) & 
    (df['Data'] <= sliderTemporal )
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

#Pagina Principa
total_vendas = round(tab_vendas_margem['Valor Pedido'].sum(), 2)
total_margem = round(tab_vendas_margem['Margem Lucro'].sum(), 2)

# Verifica se total_vendas é zero e fornece um valor alternativo
if total_vendas <= 0:
    st.write("Aviso: O total de vendas é zero ou inválido. Não é possível calcular a margem.")
    porc_margem = 0  # Ou outro valor de fallback
else:
    porc_margem = int(100 * total_margem / total_vendas)

st.header(":bar_chart: dashboard de Vendas")
dst1,dst2,dst3,dst4 = st.columns([1,1,1,2.5])
with dst1:
    st.write("Vendas totais")
    st.info(f'R${total_vendas}')
with dst2:
    st.write("Total de lucro")
    st.info(f'R${total_margem}')
with dst3:
    st.write("Margem de lucro")
    st.info(f'{porc_margem} %')
st.markdown('---')
# ================================================================================
# Exibindo os gráficos no Streamlit
cols1,cols2,cols3 = st.columns([1,1,1])
with cols1:
    st.altair_chart(graf_qte_vendida_produto)
    st.altair_chart(graf_valor_venda_produto)
with cols2:
    st.altair_chart(graf_qte_vendida_cliente)
    st.altair_chart(graf_vendas_mensais)
with cols3:
    st.altair_chart(graf_vendas_por_vendedor + rot2Ve + rot2Vp)
st.write("---")

dst2_1,dst2_2,dst2_3,dst2_4 = st.columns([1,1,1,2.5])
with dst2_1:
    st.write("Vendas totais")
    st.info(f'R${vendas_totais_absolutas}')
with dst2_2:
    st.write("Total de lucro")
    st.info(f'R${lucro_total_empresa}')
with dst2_3:
    st.write("Margem de lucro")
    st.info(f'{porcentagem_total} %')


print(type(max_data),type(min_data))
st.write(max_data,min_data)

