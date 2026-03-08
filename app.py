import streamlit as st
from fpdf import FPDF

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# BANCO DE DADOS (Fórmulas originais do seu HTML)
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
    "Elegoo": [{"nome": "Neptune 4 Max", "fator": 0.95, "watts": 500}],
    "Bambu Lab": [{"nome": "X1-Carbon", "fator": 0.85, "watts": 350}],
    "Creality": [{"nome": "K1 Max", "fator": 0.9, "watts": 1000}]
}

# INTERFACE DE ACESSO
senha = st.sidebar.text_input("CHAVE DE ACESSO", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([2, 1.3])

    with col1:
        nome_cli = st.text_input("NOME DO CLIENTE", "CLIENTE").upper()
        prazo_prod = st.selectbox("PRAZO DE PRODUÇÃO", ["7 a 10 dias úteis", "10 a 15 dias úteis", "A combinar"])
        
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            texto_p = st.text_input("TEXTO DO LETREIRO", "EXEMPLO").upper()
            qtd_l = len(texto_p.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h, w, p = c1.number_input("ALTURA (cm)", 30), c2.number_input("LARGURA (cm)", 32), c3.number_input("PROFUNDIDADE (cm)", 5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            m1, m2 = st.columns(2)
            face_map = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            f_sel = m1.selectbox("FACE", list(face_map.keys()), index=2)
            
            fundo_map = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            fun_sel = m2.selectbox("FUNDO", list(fundo_map.keys()), index=1)
            
            led_map = {"Sem LED": 0, "LED Branco": 45, "LED RGB": 75}
            l_sel = st.selectbox("ILUMINAÇÃO", list(led_map.keys()))

        with st.expander("⚙️ TÉCNICO", expanded=True):
            est = st.selectbox("LOCALIZAÇÃO", list(BASE_REGIONAL.keys()))
            mrc = st.selectbox("MARCA", list(IMPRESSORAS.keys()))
            mod = st.selectbox("MODELO", [m['nome'] for m in IMPRESSORAS[mrc]])
            maq = next(m for m in IMPRESSORAS[mrc] if m['nome'] == mod)
            kwh, mult_m = BASE_REGIONAL[est]

    # CÁLCULOS E DETALHAMENTO
    with col2:
        st.subheader("💰 DETALHAMENTO DO VALOR")
        
        # Conversão de textos para números antes do cálculo
        v_face = face_map[f_sel] * mult_m
        v_fundo = fundo_map[fun_sel] * mult_m
        v_led = led_map[l_sel]
        v_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq['fator'] * mult_m
        v_energia = ((h + w) / 10) * maq['fator'] * (maq['watts'] / 1000) * kwh
        
        u_final = v_corpo + v_face + v_fundo + v_led + v_energia
        t_final = u_final * qtd_l

        # Painel de Detalhes
        detalhe = st.container(border=True)
        detalhe.write(f"🔹 **Corpo (3D):** R$ {v_corpo:,.2f}")
        detalhe.write(f"🔹 **Face:** R$ {v_face:,.2f}")
        detalhe.write(f"🔹 **Fundo:** R$ {v_fundo:,.2f}")
        detalhe.write(f"🔹 **LED:** R$ {v_led:,.2f}")
        detalhe.write(f"🔹 **Energia:** R$ {v_energia:,.2f}")
        
        st.divider()
        st.metric("VALOR TOTAL", f"R$ {t_final:,.2f}")
        st.write(f"**Unitário:** R$ {u_final:,.2f}")

        # GERADOR DE PDF
        if st.button("📄 GERAR PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "SPP - SISTEMA DE PRECIFICACAO PRO", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            pdf.cell(190, 10, f"CLIENTE: {nome_cli.encode('latin-1', 'ignore').decode('latin-1')}", ln=True)
            pdf.cell(190, 10, f"PROJETO: {texto_p.encode('latin-1', 'ignore').decode('latin-1')}", ln=True)
            pdf.cell(190, 10, f"DIMENSOES: {h}x{w}x{p} cm", ln=True)
            pdf.ln(5)
            pdf.cell(190, 10, f"PRAZO: {prazo_prod}", ln=True)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(190, 15, f"VALOR TOTAL: R$ {t_final:,.2f}", 1, ln=True, align='C')
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 BAIXAR AGORA", pdf_bytes, f"Orcamento_{nome_cli}.pdf", "application/pdf")
else:
    st.warning("Insira a chave na barra lateral.")
