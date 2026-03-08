import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. BANCOS DE DADOS TÉCNICOS
BASE_REGIONAL = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
    "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "RS - Equatorial": [0.88, 1.03],
    "SC - Celesc": [0.76, 0.98], "PE - Neoenergia": [0.89, 1.08], "CE - Enel": [0.94, 1.10],
    "GO - Equatorial": [0.85, 1.02], "MT - Energisa": [0.96, 1.12], "AM - Amazonas": [1.02, 1.25],
    "PA - Equatorial": [1.05, 1.20], "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01]
}

IMPRESSORAS = {
    "Anycubic": {"Kobra 2 Max": [1.0, 500], "Kobra 3 Max": [0.95, 550], "Kobra 2 Plus": [1.05, 450]},
    "Elegoo": {"Neptune 4 Max": [0.95, 500]},
    "Bambu Lab": {"X1-Carbon": [0.85, 350]},
    "Creality": {"K1 Max": [0.9, 1000]}
}

# 3. ACESSO
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    # --- TÍTULO ---
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    # --- TEXTO ANIMADO (PREVIEW) ---
    col_pre, _ = st.columns([2, 1])
    with col_pre:
        texto_preview = st.text_input("Texto do Letreiro", value="CLIENTE").upper()
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
                padding: 30px; border-radius: 12px; text-align: center;
                border: 3px solid #334155; margin-bottom: 10px;
            }
            .texto-neon {
                font-size: clamp(30px, 5vw, 60px); font-weight: 900; color: white;
                text-transform: uppercase; font-family: 'Segoe UI', arial;
            }
            .led-branco { text-shadow: 0 0 12px #ffffff, 0 0 25px rgba(255,255,255,0.6); color: #fff; }
            .led-rgb { animation: rgbCycle 3s infinite linear; }
        </style>
        """, unsafe_allow_html=True)

        # Seleção de Iluminação logo abaixo do Texto
        led_dict = {"Sem Iluminação": 0, "LED Branco": 45, "LED RGB (Colorido)": 75}
        led_sel = st.selectbox("Iluminação LED", list(led_dict.keys()))
        v_led = led_dict[led_sel]

        # Lógica visual do Neon
        classe_led = ""
        msg_led = "DESLIGADO"
        if v_led == 75: 
            classe_led = "led-rgb"
            msg_led = "RGB ATIVO"
        elif v_led == 45: 
            classe_led = "led-branco"
            msg_led = "LED BRANCO ATIVO"

        st.markdown(f"""
            <div class="preview-box">
                <div class="texto-neon {classe_led}">{texto_preview if texto_preview else "CLIENTE"}</div>
                <div style="color: #475569; font-size: 11px; margin-top: 10px; letter-spacing: 2px;">{msg_led}</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns([1.5, 1])

    with col1:
        with st.expander("📝 DIMENSÕES E MATERIAIS", expanded=True):
            c1, c2, c3 = st.columns(3)
            h, w, p = c1.number_input("Altura (cm)", 30), c2.number_input("Largura (cm)", 32), c3.number_input("Profundidade (cm)", 5)
            
            face_dict = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = st.selectbox("Material da Face", list(face_dict.keys()), index=3)
            
            fundo_dict = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "ACM 3mm": 30}
            fundo_sel = st.selectbox("Material do Fundo", list(fundo_dict.keys()), index=1)

    with col2:
        st.subheader("💰 ORÇAMENTO")
        estado_sel = st.selectbox("Sua Região", list(BASE_REGIONAL.keys()))
        mod_sel = st.selectbox("Sua Máquina", list(IMPRESSORAS["Anycubic"].keys()))
        
        kwh, mult_m = BASE_REGIONAL[estado_sel]
        fator, watts = IMPRESSORAS["Anycubic"][mod_sel]
        
        # Cálculos de custo
        v_face = face_dict[face_sel] * mult_m
        v_fundo = fundo_dict[fundo_sel] * mult_m
        v_corpo = ((h*2) + (w*2)) * p * 0.17808 * fator * mult_m
        
        u_final = v_corpo + v_face + v_fundo + v_led
        t_final = u_final * qtd_letras

        st.metric("TOTAL", f"R$ {t_final:,.2f}")
        st.write(f"Unitário: R$ {u_final:,.2f}")
        
        if st.button("🖨️ Salvar Orçamento"):
            st.info("Pressione Ctrl+P.")
else:
    st.sidebar.warning("Aguardando Chave Hugo Pro.")
