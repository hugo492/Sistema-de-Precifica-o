import streamlit as st
from fpdf import FPDF

# 1. CONFIGURAÇÃO (NOME CORRETO DO SISTEMA)
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. DADOS TÉCNICOS (Baseados no seu histórico e arquivos)
BASE_REGIONAL = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "SC - Celesc": [0.76, 0.98],
    "RJ - Light": [0.98, 1.02], "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98]
}

IMPRESSORAS = {
    "Anycubic": [{"nome": "Kobra 2 Max", "fator": 1.0, "watts": 500}, {"nome": "Kobra 3 Max", "fator": 0.95, "watts": 550}],
    "Creality": [{"nome": "K1 Max", "fator": 0.9, "watts": 1000}]
}

# 3. ACESSO
senha = st.sidebar.text_input("CHAVE DE ACESSO MENSAL", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([1.5, 1])

    with col1:
        nome_cli = st.text_input("NOME DO CLIENTE", "CLIENTE").upper()
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            txt_p = st.text_input("TEXTO DO LETREIRO", "EXEMPLO").upper()
            qtd_l = len(txt_p.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h, w, p = c1.number_input("ALTURA (cm)", 30), c2.number_input("LARGURA (cm)", 32), c3.number_input("PROFUNDIDADE (cm)", 5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            # TRADUÇÃO DE TEXTO PARA NÚMERO (Resolve o TypeError da sua imagem)
            f_map = {"Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            fun_map = {"PVC 5mm": 15, "PVC 10mm": 25, "ACM 3mm": 30}
            corpo_map = {"PETG UV": 130, "PLA": 100}

            f_sel = st.selectbox("FACE", list(f_map.keys()))
            fun_sel = st.selectbox("FUNDO", list(fun_map.keys()))
            cor_sel = st.selectbox("CORPO", list(corpo_map.keys()))

    with col2:
        st.subheader("💰 VALORES DETALHADOS")
        est = st.selectbox("ESTADO", list(BASE_REGIONAL.keys()))
        mod = st.selectbox("MÁQUINA", [m['nome'] for m in IMPRESSORAS["Anycubic"]])
        maq = next(m for m in IMPRESSORAS["Anycubic"] if m['nome'] == mod)
        kwh, mult_m = BASE_REGIONAL[est]

        # CÁLCULO SEGURO (Apenas números)
        v_face = f_map[f_sel] * mult_m
        v_fundo = fun_map[fun_sel] * mult_m
        v_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq['fator'] * (corpo_map[cor_sel] * mult_m / 130)
        
        u_final = v_corpo + v_face + v_fundo
        t_final = u_final * qtd_l

        st.container(border=True).write(f"🔹 Corpo: R$ {v_corpo:,.2f} | 🔹 Face: R$ {v_face:,.2f}")
        st.metric("VALOR TOTAL", f"R$ {t_final:,.2f}")

        # PDF SEM ACENTOS PARA NÃO TRAVAR
        if st.button("📄 GERAR ORÇAMENTO PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "SPP - SISTEMA DE PRECIFICACAO PRO", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            pdf.cell(190, 10, f"CLIENTE: {nome_cli}", ln=True)
            pdf.cell(190, 10, f"VALOR TOTAL: R$ {t_final:,.2f}", ln=True)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 BAIXAR PDF", pdf_bytes, f"Orcamento.pdf", "application/pdf")
else:
    st.sidebar.warning("Aguardando Chave de Acesso.")
