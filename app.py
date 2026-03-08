import streamlit as st

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - Precificação Pro", layout="wide")

# BANCO DE DADOS COMPLETO (Baseado no teu arquivo original)
BASE_REGIONAL = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
    "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "RS - Equatorial": [0.88, 1.03],
    "SC - Celesc": [0.76, 0.98], "PE - Neoenergia": [0.89, 1.08], "CE - Enel": [0.94, 1.10],
    "GO - Equatorial": [0.85, 1.02], "MT - Energisa": [0.96, 1.12], "AM - Amazonas": [1.02, 1.25],
    "PA - Equatorial": [1.05, 1.20], "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01]
}

IMPRESSORAS = {
    "Anycubic": [
        {"nome": "Kobra 2 Max", "fator": 1.0, "watts": 500},
        {"nome": "Kobra 3 Max", "fator": 0.95, "watts": 550},
        {"nome": "Kobra 2 Plus", "fator": 1.05, "watts": 450},
        {"nome": "Kobra Neo", "fator": 1.3, "watts": 350}
    ],
    "Elegoo": [
        {"nome": "Neptune 4 Max", "fator": 0.95, "watts": 500},
        {"nome": "Neptune 4 Plus", "fator": 0.98, "watts": 480},
        {"nome": "Neptune 4 Pro", "fator": 1.02, "watts": 400}
    ],
    "Bambu Lab": [
        {"nome": "X1-Carbon", "fator": 0.85, "watts": 350},
        {"nome": "P1S", "fator": 0.88, "watts": 350},
        {"nome": "A1", "fator": 0.92, "watts": 300}
    ],
    "Creality": [
        {"nome": "K1 Max", "fator": 0.9, "watts": 1000},
        {"nome": "Ender 3 V3", "fator": 1.1, "watts": 350},
        {"nome": "CR-M4", "fator": 0.98, "watts": 800}
    ]
}

# ACESSO POR SENHA (ASSINATURA)
st.sidebar.title("🔐 Acesso Hugo Pro")
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        texto = st.text_input("Texto do Letreiro").upper()
        qtd_letras = len(texto.replace(" ", ""))
        
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("Altura (cm)", value=30)
        w = c2.number_input("Largura (cm)", value=32)
        p = c3.number_input("Profundidade (cm)", value=5)
        
        marca = st.selectbox("Marca", list(IMPRESSORAS.keys()))
        modelo = st.selectbox("Modelo", [m['nome'] for m in IMPRESSORAS[marca]])
        estado = st.selectbox("Localização", list(BASE_REGIONAL.keys()))
        
        # Lógica de cálculo exata do teu HTML
        maq_data = next(m for m in IMPRESSORAS[marca] if m['nome'] == modelo)
        kwh, mult_mat = BASE_REGIONAL[estado]
        
        preco_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq_data['fator'] * (130 * mult_mat / 130)
        energia = ((h + w) / 10) * maq_data['fator'] * (maq_data['watts'] / 1000) * kwh
        
    with col2:
        st.subheader("Orçamento")
        valor_unit = preco_corpo + energia + 35 # Base de acrílico/LED
        st.metric("TOTAL", f"R$ {valor_unit * qtd_letras:,.2f}")
        st.write(f"Unitário: R$ {valor_unit:,.2f}")
        
else:
    st.warning("Insira a senha de assinante na barra lateral.")