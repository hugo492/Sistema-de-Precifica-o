import streamlit as st

# 1. CONFIGURAÇÃO E ESTILO NEON (DARK MODE)
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; }
    .stMetric { background-color: #1a1c23; border: 1px solid #00ffcc; padding: 15px; border-radius: 10px; }
    div[data-testid="stExpander"] { background-color: #1a1c23; border: 1px solid #00ffcc; color: white; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0 0 10px #00ffcc; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; border-radius: 5px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCOS DE DADOS (Seu código original)
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
        {"nome": "Kobra 2 Plus", "fator": 1.05, "watts": 450}
    ],
    "Creality": [{"nome": "K1 Max", "fator": 0.9, "watts": 1000}],
    "Bambu Lab": [{"nome": "X1-Carbon", "fator": 0.85, "watts": 350}]
}

# 3. ACESSO
st.sidebar.title("🔐 Acesso Hugo Pro")
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([2, 1.2])

    with col1:
        with st.expander("📝 TEXTO E DIMENSÕES", expanded=True):
            texto = st.text_input("Texto do Letreiro", placeholder="Ex: HUGO SANTOS").upper()
            qtd_letras = len(texto.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h = c1.number_input("Altura (cm)", value=30)
            w = c2.number_input("Largura (cm)", value=32)
            p = c3.number_input("Profundidade (cm)", value=5)

        with st.expander("🏗️ MATERIAIS E COMPONENTES", expanded=True):
            m1, m2 = st.columns(2)
            face_dict = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = m1.selectbox("Material da Face", list(face_dict.keys()), index=2)
            
            fundo_dict = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            fundo_sel = m2.selectbox("Material do Fundo", list(fundo_dict.keys()), index=1)
            
            led_dict = {"Sem LED": 0, "LED Branco": 45, "LED RGB": 75}
            led_sel = st.selectbox("Iluminação LED", list(led_dict.keys()))

        with st.expander("⚙️ TÉCNICO", expanded=True):
            reg_col, imp_col = st.columns(2)
            estado = reg_col.selectbox("Localização", list(BASE_REGIONAL.keys()))
            marca = imp_col.selectbox("Marca", list(IMPRESSORAS.keys()))
            modelo = st.selectbox("Modelo", [m['nome'] for m in IMPRESSORAS[marca]])
            maq_data = next(m for m in IMPRESSORAS[marca] if m['nome'] == modelo)
            kwh, mult_mat = BASE_REGIONAL[estado]

    # 4. LÓGICA E DETALHAMENTO DE VALOR
    with col2:
        st.subheader("💰 DETALHAMENTO")
        
        # Valores individuais
        custo_face = face_dict[face_sel] * mult_mat
        custo_fundo = fundo_dict[fundo_sel] * mult_mat
        custo_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq_data['fator'] * (130 * mult_mat / 130)
        
        v_unit = custo_corpo + custo_face + custo_fundo + led_dict[led_sel]
        v_total = v_unit * qtd_letras

        # Exibição detalhada
        st.write(f"🟢 **Corpo (3D):** R$ {custo_corpo:,.2f}")
        st.write(f"🟢 **Face:** R$ {custo_face:,.2f}")
        st.write(f"🟢 **Fundo:** R$ {custo_fundo:,.2f}")
        st.write(f"🟢 **LED:** R$ {led_dict[led_sel]:,.2f}")
        
        st.divider()
        st.metric("VALOR TOTAL", f"R$ {v_total:,.2f}")
        st.write(f"**Unitário:** R$ {v_unit:,.2f}")
        
        st.divider()
        if st.button("🖨️ Gerar Orçamento (PDF)"):
            st.info("Pressione **Ctrl + P** para salvar como PDF profissional.")

else:
    st.warning("⚠️ Insira a Chave na barra lateral.")
