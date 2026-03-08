import streamlit as st
from fpdf import FPDF
import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Hugo Letra Caixa PRO", layout="wide")

# 2. DADOS TÉCNICOS ORIGINAIS
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

# 3. SISTEMA DE ACESSO
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([2, 1.3])

    with col1:
        nome_cliente = st.text_input("Nome do Cliente", "NOME DO CLIENTE / EMPRESA")
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            texto = st.text_input("Texto do Letreiro", "HUGO SANTOS").upper()
            qtd_letras = len(texto.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h = c1.number_input("Altura (cm)", 20)
            w = c2.number_input("Largura (cm)", 15)
            p = c3.number_input("Profundidade (cm)", 5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            m1, m2 = st.columns(2)
            face_opts = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = m1.selectbox("Material da Face", list(face_opts.keys()), index=2)
            v_face_base = face_opts[face_sel]
            
            cor_opts = {"Branca (Padrão)": 0, "Colorida (+ R$ 20,00)": 20}
            cor_sel = m2.selectbox("Cor da Face", list(cor_opts.keys()))
            v_cor = cor_opts[cor_sel]
            
            fundo_opts = {"Sem Fundo (Vazado)": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            fundo_sel = st.selectbox("Material do Fundo (Base)", list(fundo_opts.keys()))
            v_fundo_base = fundo_opts[fundo_sel]

        with st.expander("⚙️ CONFIGURAÇÃO TÉCNICA", expanded=True):
            reg_col, imp_col = st.columns(2)
            estado = reg_col.selectbox("Localização", list(BASE_REGIONAL.keys()), index=6) # Index 6 é SC conforme imagem
            marca = imp_col.selectbox("Marca", list(IMPRESSORAS.keys()))
            modelo = st.selectbox("Modelo", [m['nome'] for m in IMPRESSORAS[marca]], index=1)
            maq_data = next(m for m in IMPRESSORAS[marca] if m['nome'] == modelo)
            kwh, mult_mat = BASE_REGIONAL[estado]

    # 4. DETALHAMENTO DE VALORES
    with col2:
        st.subheader("💰 DETALHAMENTO DO VALOR")
        
        # Cálculos Técnicos
        custo_face = v_face_base * mult_mat
        custo_fundo = v_fundo_base * mult_mat
        custo_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq_data['fator'] * (130 * mult_mat / 130)
        custo_energia = ((h + w) / 10) * maq_data['fator'] * (maq_data['watts'] / 1000) * kwh
        
        # Valor Unitário e Total
        total_unitario = custo_corpo + custo_face + custo_fundo + v_cor
        total_projeto = total_unitario * qtd_letras
        
        # Painel de Detalhes Visual
        container = st.container(border=True)
        container.write(f"🏗️ **Corpo (3D):** R$ {custo_corpo:,.2f}")
        container.write(f"💎 **Face ({face_sel}):** R$ {custo_face:,.2f}")
        container.write(f"📦 **Fundo:** R$ {custo_fundo:,.2f}")
        container.write(f"🎨 **Adicional Cor:** R$ {v_cor:,.2f}")
        container.write(f"⚡ **Energia:** R$ {custo_energia:,.2f}")
        
        st.divider()
        st.metric("VALOR TOTAL", f"R$ {total_projeto:,.2f}")
        st.metric("UNITÁRIO", f"R$ {total_unitario:,.2f}/Un.")

        # GERAÇÃO DO PDF PROFISSIONAL
        if st.button("📄 GERAR ARQUIVO PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "ORÇAMENTO - HUGO LETRA CAIXA PRO", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            pdf.cell(190, 10, f"Cliente: {nome_cliente}", ln=True)
            pdf.cell(190, 10, f"Projeto: {texto} ({qtd_letras} letras)", ln=True)
            pdf.cell(190, 10, f"Dimensões: {h}cm x {w}cm x {p}cm", ln=True)
            pdf.ln(5)
            pdf.cell(190, 10, "DETALHAMENTO TÉCNICO:", ln=True)
            pdf.cell(190, 10, f"- Face: {face_sel} | Fundo: {fundo_sel}", ln=True)
            pdf.cell(190, 10, f"- Máquina: {modelo} ({maq_data['watts']}W)", ln=True)
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(190, 10, f"VALOR UNITÁRIO: R$ {total_unitario:,.2f}", ln=True)
            pdf.cell(190, 10, f"TOTAL DO PROJETO: R$ {total_projeto:,.2f}", ln=True)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(label="📥 CLIQUE PARA BAIXAR PDF", data=pdf_bytes, file_name=f"Orcamento_{texto}.pdf", mime="application/pdf")

else:
    st.warning("⚠️ Insira a chave de acesso na barra lateral.")
