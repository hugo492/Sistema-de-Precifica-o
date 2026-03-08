import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. BANCOS DE DADOS TÉCNICOS COMPLETOS
BASE_REGIONAL = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
    "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "RS - Equatorial": [0.88, 1.03],
    "SC - Celesc": [0.76, 0.98], "PE - Neoenergia": [0.89, 1.08], "CE - Enel": [0.94, 1.10],
    "GO - Equatorial": [0.85, 1.02], "MT - Energisa": [0.96, 1.12], "AM - Amazonas": [1.02, 1.25],
    "PA - Equatorial": [1.05, 1.20], "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01]
}

IMPRESSORAS = {
    "Anycubic": {
        "Kobra 2 Max": [1.0, 500], "Kobra 3 Max": [0.95, 550], "Kobra 2 Plus": [1.05, 450], "Kobra Neo": [1.3, 350]
    },
    "Elegoo": {
        "Neptune 4 Max": [0.95, 500], "Neptune 4 Plus": [0.98, 480], "Neptune 4 Pro": [1.02, 400]
    },
    "Bambu Lab": {
        "X1-Carbon": [0.85, 350], "P1S": [0.88, 350], "A1": [0.92, 300]
    },
    "Creality": {
        "K1 Max": [0.9, 1000], "Ender 3 V3": [1.1, 350], "CR-M4": [0.98, 800]
    }
}

# 3. ACESSO
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    st.info("💡 Corpo interno sempre em branco para melhor reflexão do LED.")

    # --- INÍCIO COM OPÇÕES PADRÃO: TEXTO LETREIRO E SEM LED ---
    texto_preview = st.text_input("Texto do Letreiro", value="TEXTO LETREIRO").upper()
    qtd_letras = len(texto_preview.replace(" ", ""))

    # CSS da Animação
    st.markdown("""
    <style>
        @keyframes rgbCycle {
            0% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
            33% { color: #00ff00; text-shadow: 0 0 15px #00ff00; }
            66% { color: #0000ff; text-shadow: 0 0 15px #0000ff; }
            100% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
        }
        .preview-box {
            background: radial-gradient(circle, #1e293b 0%, #000000 100%);
            padding: 40px; border-radius: 12px; text-align: center;
            border: 3px solid #334155; margin-bottom: 10px;
        }
        .texto-neon {
            font-size: clamp(30px, 6vw, 70px); font-weight: 900; color: white;
            text-transform: uppercase; font-family: 'Segoe UI', arial;
        }
        .led-branco { text-shadow: 0 0 12px #ffffff, 0 0 25px rgba(255,255,255,0.6); color: #fff; }
        .led-rgb { animation: rgbCycle 3s infinite linear; }
    </style>
    """, unsafe_allow_html=True)

    # Inicia com "Sem Iluminação" (index=0)
    led_dict = {"Sem Iluminação": 0, "LED Branco Frio / Quente": 45, "LED RGB (Colorido)": 75}
    led_sel = st.selectbox("Iluminação LED", list(led_dict.keys()), index=0)
    v_led = led_dict[led_sel]

    classe_led = "led-rgb" if v_led == 75 else ("led-branco" if v_led == 45 else "")
    st.markdown(f"""
        <div class="preview-box">
            <div class="texto-neon {classe_led}">{texto_preview if texto_preview else "TEXTO"}</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns([1.5, 1])

    with col1:
        with st.expander("📝 DIMENSÕES E MATERIAIS", expanded=True):
            c1, c2, c3 = st.columns(3)
            h, w, p = c1.number_input("Altura (cm)", 30), c2.number_input("Largura (cm)", 32), c3.number_input("Profundidade (cm)", 5)
            
            m1, m2 = st.columns(2)
            face_dict = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = m1.selectbox("Material da Face", list(face_dict.keys()), index=3)
            
            cor_dict = {"Face Branca (Padrão)": 0, "Face Colorida (+ R$ 20,00)": 20}
            cor_sel = m2.selectbox("Cor da Face", list(cor_dict.keys()))
            
            fundo_dict = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            fundo_sel = st.selectbox("Material do Fundo (Base)", list(fundo_dict.keys()), index=1)
            
            corpo_dict = {"Uso Externo (PETG c/ Proteção UV)": 130, "Uso Interno (PLA)": 100}
            corpo_sel = st.selectbox("Material do Corpo", list(corpo_dict.keys()))

        with st.expander("⚙️ CONFIGURAÇÃO DE MÁQUINA", expanded=True):
            reg_col, marca_col, mod_col = st.columns(3)
            estado = reg_col.selectbox("Localização", list(BASE_REGIONAL.keys()))
            marca = marca_col.selectbox("Marca", list(IMPRESSORAS.keys()))
            modelo = mod_col.selectbox("Modelo", list(IMPRESSORAS[marca].keys()))

    with col2:
        st.subheader("💰 ORÇAMENTO FINAL")
        perfil = st.radio("Perfil de Cliente", ["Cliente Final (100%)", "Terceirização (80%)"], horizontal=True)
        ajuste_manual = st.number_input("Ajuste Manual (%)", value=0)

        # CÁLCULOS
        kwh, mult_m = BASE_REGIONAL[estado]
        fator, watts = IMPRESSORAS[marca][modelo]
        
        v_face = face_dict[face_sel] * mult_m
        v_fundo = fundo_dict[fundo_sel] * mult_m
        v_cor = cor_dict[cor_sel]
        v_mat_corpo = corpo_dict[corpo_sel] * mult_m
        
        preco_corpo = ((h*2) + (w*2)) * p * 0.17808 * fator * (v_mat_corpo / 130)
        energia = ((h + w) / 10) * fator * (watts / 1000) * kwh
        
        valor_unit = preco_corpo + v_face + v_fundo + v_led + v_cor + energia
        
        fator_perfil = 0.8 if "Terceirização" in perfil else 1.0
        valor_unit = valor_unit * fator_perfil * (1 + (ajuste_manual / 100))
        total_geral = valor_unit * qtd_letras

        st.metric("VALOR TOTAL", f"R$ {total_geral:,.2f}")
        st.write(f"**Unitário:** R$ {valor_unit:,.2f}/Un.")
        
        st.divider()
        if st.button("🖨️ Salvar Orçamento em PDF"):
            st.info("Pressione Ctrl + P no navegador.")
else:
    st.sidebar.warning("Aguardando Chave Hugo Pro.")
