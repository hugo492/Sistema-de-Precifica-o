import streamlit as st
from fpdf import FPDF

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. BANCOS DE DADOS (VALORES TÉCNICOS)
BASE_REGIONAL = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
    "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "SC - Celesc": [0.76, 0.98]
}

# MAPAS DE PREÇO (Isso impede o erro TypeError)
FACE_PRECOS = {"Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
FUNDO_PRECOS = {"PVC 5mm": 15, "PVC 10mm": 25, "ACM 3mm": 30, "Impressão 3D": 12}
CORPO_PRECOS = {"PETG UV (Externo)": 130, "PLA (Interno)": 100}

# 3. ACESSO
senha = st.sidebar.text_input("CHAVE DE ACESSO MENSAL", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([1.5, 1])

    with col1:
        nome_cli = st.text_input("NOME DO CLIENTE", "CLIENTE").upper()
        
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            texto_p = st.text_input("TEXTO DO LETREIRO", "EXEMPLO").upper()
            qtd_l = len(texto_p.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h = c1.number_input("ALTURA (cm)", value=30)
            w = c2.number_input("LARGURA (cm)", value=32)
            p = c3.number_input("PROFUNDIDADE (cm)", value=5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            f_sel = st.selectbox("MATERIAL DA FACE", list(FACE_PRECOS.keys()))
            fun_sel = st.selectbox("MATERIAL DO FUNDO", list(FUNDO_PRECOS.keys()))
            cor_sel = st.selectbox("MATERIAL DO CORPO", list(CORPO_PRECOS.keys()))

    with col2:
        st.subheader("💰 VALORES DETALHADOS")
        
        estado = st.selectbox("LOCALIZAÇÃO", list(BASE_REGIONAL.keys()))
        kwh, mult_mat = BASE_REGIONAL[estado]
        
        # BUSCA DOS VALORES NUMÉRICOS (AQUI ESTÁ A CORREÇÃO)
        v_face = FACE_PRECOS[f_sel] * mult_mat
        v_fundo = FUNDO_PRECOS[fun_sel] * mult_mat
        v_corpo_base = CORPO_PRECOS[cor_sel]
        
        # CÁLCULO DO CORPO (Fórmula original 0.17808)
        custo_corpo = ((h*2) + (w*2)) * p * 0.17808 * (v_corpo_base * mult_mat / 130)
        
        unitario = custo_corpo + v_face + v_fundo
        total_geral = unitario * qtd_l

        # PAINEL VISUAL
        detalhe = st.container(border=True)
        detalhe.write(f"🔹 **Corpo:** R$ {custo_corpo:,.2f}")
        detalhe.write(f"🔹 **Face:** R$ {v_face:,.2f}")
        detalhe.write(f"🔹 **Fundo:** R$ {v_fundo:,.2f}")
        
        st.divider()
        st.metric("VALOR TOTAL", f"R$ {total_geral:,.2f}")
        st.write(f"**Unitário:** R$ {unitario:,.2f}")

        # PDF SEM ACENTOS PARA NÃO TRAVAR
        if st.button("📄 GERAR ORÇAMENTO EM PDF"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(190, 10, "SPP - SISTEMA DE PRECIFICACAO PRO", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", '', 12)
                pdf.cell(190, 10, f"CLIENTE: {nome_cli}", ln=True)
                pdf.cell(190, 10, f"PROJETO: {texto_p}", ln=True)
                pdf.cell(190, 10, f"VALOR TOTAL: R$ {total_geral:,.2f}", ln=True)
                
                pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button("📥 BAIXAR PDF", pdf_output, f"Orcamento_{nome_cli}.pdf", "application/pdf")
            except:
                st.error("Erro ao gerar PDF. Evite acentos nos campos.")
else:
    st.sidebar.warning("Aguardando Chave de Acesso.")
