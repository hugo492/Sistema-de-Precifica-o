import streamlit as stimport streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA (ESTILO PROFISSIONAL)
st.set_page_config(page_title="SPP - Precificação Pro", layout="wide")

# 2. BANCOS DE DADOS TÉCNICOS (Extraído do seu HTML original)
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
    ],
    "Artillery": [
        {"nome": "Sidewinder X4 Plus", "fator": 0.98, "watts": 500},
        {"nome": "Sidewinder X2", "fator": 1.15, "watts": 350},
        {"nome": "Hornet", "fator": 1.3, "watts": 300}
    ],
    "Prusa": [
        {"nome": "MK4", "fator": 0.9, "watts": 300},
        {"nome": "XL", "fator": 0.85, "watts": 450},
        {"nome": "MK3S+", "fator": 1.05, "watts": 300}
    ]
}

# 3. ACESSO (MODO ASSINATURA)
st.sidebar.title("🔐 Acesso Hugo Pro")
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    st.info("💡 Corpo interno sempre em branco para melhor reflexão do LED.")

    col1, col2 = st.columns([2, 1])

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
            # Material da Face
            face_dict = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = m1.selectbox("Material da Face", list(face_dict.keys()), index=3)
            v_face_base = face_dict[face_sel]

            # Cor da Face
            cor_dict = {"Face Branca (Padrão)": 0, "Face Colorida (+ R$ 20,00)": 20}
            cor_sel = m2.selectbox("Cor da Face", list(cor_dict.keys()))
            v_cor = cor_dict[cor_sel]

            # Material do Fundo
            fundo_dict = {"Sem Fundo (Vazado)": 0, "PVC Expandido 5mm": 15, "PVC Expandido 10mm": 25, "Fundo em Impressão 3D": 12, "ACM 3mm": 30}
            fundo_sel = st.selectbox("Material do Fundo (Base)", list(fundo_dict.keys()), index=1)
            v_fundo_base = fundo_dict[fundo_sel]

            # Iluminação LED
            led_dict = {"Sem Iluminação": 0, "LED Branco Frio / Quente": 45, "LED RGB (Colorido)": 75}
            led_sel = st.selectbox("Iluminação LED", list(led_dict.keys()))
            v_led = led_dict[led_sel]

        with st.expander("⚙️ CONFIGURAÇÃO TÉCNICA", expanded=True):
            reg_col, imp_col = st.columns(2)
            estado = reg_col.selectbox("Localização", list(BASE_REGIONAL.keys()))
            marca = imp_col.selectbox("Marca", list(IMPRESSORAS.keys()))
            modelo = st.selectbox("Modelo da Máquina", [m['nome'] for m in IMPRESSORAS[marca]])
            
            # Material do Corpo
            corpo_dict = {"Uso Externo (PETG c/ Proteção UV)": 130, "Uso Interno (PLA)": 100}
            corpo_sel = st.selectbox("Material do Corpo", list(corpo_dict.keys()))
            v_corpo_base = corpo_dict[corpo_sel]

        with st.expander("👥 PERFIL DE CLIENTE", expanded=True):
            perfil = st.radio("Perfil", ["Cliente Final (100%)", "Terceirização (80%)"], horizontal=True)
            ajuste_manual = st.number_input("Ajuste Manual (%)", value=0)

    # 4. LÓGICA DE CÁLCULO (EXATA DO ORIGINAL)
    with col2:
        st.subheader("💰 ORÇAMENTO")
        
        maq_data = next(m for m in IMPRESSORAS[marca] if m['nome'] == modelo)
        kwh, mult_mat = BASE_REGIONAL[estado]
        
        # Ajuste de custos por região
        v_face = v_face_base * mult_mat
        v_fundo = v_fundo_base * mult_mat
        v_mat_corpo = v_corpo_base * mult_mat
        
        # Cálculo do Corpo e Energia
        preco_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq_data['fator'] * (v_mat_corpo / 130)
        energia = ((h + w) / 10) * maq_data['fator'] * (maq_data['watts'] / 1000) * kwh
        
        # Valor Unitário
        valor_unit = preco_corpo + v_face + v_fundo + v_led + v_cor + energia
        
        # Aplicação de Perfil e Ajuste
        fator_perfil = 0.8 if "Terceirização" in perfil else 1.0
        valor_unit = valor_unit * fator_perfil * (1 + (ajuste_manual / 100))
        
        total_geral = valor_unit * qtd_letras

        st.metric("VALOR TOTAL", f"R$ {total_geral:,.2f}")
        st.write(f"**Unitário:** R$ {valor_unit:,.2f}/Un.")
        st.divider()
        st.write(f"📊 **Resumo:** {qtd_letras} letras | {h}x{w}x{p} cm")
        
        if st.button("🖨️ Salvar Orçamento em PDF"):
            st.info("Dica: Use Ctrl + P no navegador para gerar o PDF profissional.")

else:
    st.warning("⚠️ Insira a Chave de Assinante na barra lateral para liberar o sistema.")
