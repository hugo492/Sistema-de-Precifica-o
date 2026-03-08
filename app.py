import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. BANCOS DE DADOS TÉCNICOS (Custo KWh e Multiplicador de Matéria-Prima)
BASE_REGIONAL = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
    "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "RS - Equatorial": [0.88, 1.03],
    "SC - Celesc": [0.76, 0.98], "PE - Neoenergia": [0.89, 1.08], "CE - Enel": [0.94, 1.10],
    "GO - Equatorial": [0.85, 1.02], "MT - Energisa": [0.96, 1.12], "AM - Amazonas": [1.02, 1.25],
    "PA - Equatorial": [1.05, 1.20], "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01]
}

# 3. DICIONÁRIO DE MÁQUINAS (Fator de velocidade e Watts)
IMPRESSORAS = {
    "Anycubic": {
        "Kobra 2 Max": [1.0, 500], "Kobra 3 Max": [0.95, 550], 
        "Kobra 2 Plus": [1.05, 450], "Kobra Neo": [1.3, 350]
    },
    "Creality": {
        "K1 Max": [0.9, 1000], "Ender 3 V3": [1.1, 350], "CR-M4": [0.98, 800]
    },
    "Bambu Lab": {
        "X1-Carbon": [0.85, 350], "P1S": [0.88, 350], "A1": [0.92, 300]
    }
}

# 4. INTERFACE DE ACESSO
st.sidebar.title("🔐 Acesso Hugo Pro")
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([1.5, 1])

    with col1:
        nome_cliente = st.text_input("ORÇAMENTO PARA:", placeholder="NOME DO CLIENTE / EMPRESA").upper()
        
        with st.expander("📝 TEXTO E DIMENSÕES", expanded=True):
            texto = st.text_input("Texto do Letreiro", placeholder="Ex: HUGO SANTOS").upper()
            qtd_letras = len(texto.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h = c1.number_input("Altura (cm)", value=30)
            w = c2.number_input("Largura (cm)", value=32)
            p = c3.number_input("Profundidade (cm)", value=5)

        with st.expander("🏗️ MATERIAIS E COMPONENTES", expanded=True):
            m1, m2 = st.columns(2)
            # Face
            face_dict = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = m1.selectbox("Material da Face", list(face_dict.keys()), index=3)
            # Fundo
            fundo_dict = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            fundo_sel = m2.selectbox("Material do Fundo", list(fundo_dict.keys()), index=1)
            # LED
            led_dict = {"Sem Iluminação": 0, "LED Branco Frio/Quente": 45, "LED RGB (Colorido)": 75}
            led_sel = st.selectbox("Iluminação LED", list(led_dict.keys()))
            # Corpo
            corpo_dict = {"Uso Externo (PETG c/ Proteção UV)": 130, "Uso Interno (PLA)": 100}
            corpo_sel = st.selectbox("Material do Corpo", list(corpo_dict.keys()))

    with col2:
        st.subheader("⚙️ CONFIGURAÇÃO TÉCNICA")
        estado_sel = st.selectbox("Localização", list(BASE_REGIONAL.keys()))
        marca_sel = st.selectbox("Marca da Impressora", list(IMPRESSORAS.keys()))
        modelo_sel = st.selectbox("Modelo", list(IMPRESSORAS[marca_sel].keys()))
        
        perfil = st.radio("Perfil de Venda", ["Cliente Final (100%)", "Terceirização (80%)"], horizontal=True)
        ajuste = st.number_input("Ajuste Manual (%)", value=0)

        # --- LÓGICA DE CÁLCULO ---
        kwh_regiao = BASE_REGIONAL[estado_sel][0]
        mult_material = BASE_REGIONAL[estado_sel][1]
        
        fator_maquina = IMPRESSORAS[marca_sel][modelo_sel][0]
        watts_maquina = IMPRESSORAS[marca_sel][modelo_sel][1]
        
        # Custos Base
        custo_face = face_dict[face_sel] * mult_material
        custo_fundo = fundo_dict[fundo_sel] * mult_material
        custo_corpo_base = corpo_dict[corpo_sel] * mult_material
        
        # Fórmula exata do seu HTML
        preco_corpo = ((h*2) + (w*2)) * p * 0.17808 * fator_maquina * (custo_corpo_base / 130)
        energia = ((h + w) / 10) * fator_maquina * (watts_maquina / 1000) * kwh_regiao
        
        # Valor Unitário
        v_unit = preco_corpo + custo_face + custo_fundo + led_dict[led_sel] + energia
        
        # Aplicar Perfil e Ajuste
        mult_perfil = 0.8 if "Terceirização" in perfil else 1.0
        v_unit = v_unit * mult_perfil * (1 + (ajuste / 100))
        
        v_total = v_unit * qtd_letras

        # --- EXIBIÇÃO DE RESULTADOS ---
        st.divider()
        st.metric("VALOR TOTAL", f"R$ {v_total:,.2f}")
        st.write(f"**Unitário:** R$ {v_unit:,.2f}")
        
        with st.container(border=True):
            st.write(f"📊 **Resumo Técnico**")
            st.write(f"- Letras: {qtd_letras} unidades")
            st.write(f"- Dimensões: {h}x{w}x{p} cm")
            st.write(f"- Material: {face_sel}")

        if st.button("🖨️ Imprimir Orçamento"):
            st.info("Pressione **Ctrl + P** para salvar em PDF.")
else:
    st.warning("⚠️ Insira a Chave de Acesso na barra lateral.")
