import streamlit as st
from fpdf import FPDF
import base64

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - Precificação Pro", layout="wide")

# 2. BANCOS DE DADOS TÉCNICOS (Original)
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

# 3. FUNÇÃO PARA GERAR O PDF
def gerar_pdf(nome_cliente, texto, total, unitario, resumo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ORÇAMENTO - HUGO LETRA CAIXA PRO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Cliente: {nome_cliente}", ln=True)
    pdf.cell(200, 10, f"Texto: {texto}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, resumo)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"VALOR TOTAL: R$ {total:,.2f}", ln=True)
    pdf.cell(200, 10, f"VALOR UNITÁRIO: R$ {unitario:,.2f}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# 4. ACESSO
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([2, 1.2])

    with col1:
        nome_cliente = st.text_input("Nome do Cliente", "NOME DO CLIENTE / EMPRESA")
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            texto = st.text_input("Texto do Letreiro").upper()
            qtd_letras = len(texto.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h, w, p = c1.number_input("Altura (cm)", 30), c2.number_input("Largura (cm)", 32), c3.number_input("Profundidade (cm)", 5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            f1, f2 = st.columns(2)
            face_dict = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            v_face_base = face_dict[f1.selectbox("Material da Face", list(face_dict.keys()), index=3)]
            
            fundo_dict = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            v_fundo_base = fundo_dict[f2.selectbox("Material do Fundo", list(fundo_dict.keys()), index=1)]
            
            led_dict = {"Sem LED": 0, "Branco Frio/Quente": 45, "RGB Colorido": 75}
            v_led = led_dict[st.selectbox("Iluminação LED", list(led_dict.keys()))]

        with st.expander("⚙️ TÉCNICO", expanded=True):
            estado = st.selectbox("Localização", list(BASE_REGIONAL.keys()))
            marca = st.selectbox("Marca", list(IMPRESSORAS.keys()))
            modelo = st.selectbox("Modelo", [m['nome'] for m in IMPRESSORAS[marca]])
            maq_data = next(m for m in IMPRESSORAS[marca] if m['nome'] == modelo)
            kwh, mult_mat = BASE_REGIONAL[estado]

    # 5. CÁLCULO E DETALHAMENTO
    with col2:
        st.subheader("💰 DETALHES DO VALOR")
        
        # Custos individuais
        custo_face = v_face_base * mult_mat
        custo_fundo = v_fundo_base * mult_mat
        custo_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq_data['fator'] * (130 * mult_mat / 130)
        custo_energia = ((h + w) / 10) * maq_data['fator'] * (maq_data['watts'] / 1000) * kwh
        
        v_unit = custo_corpo + custo_face + custo_fundo + v_led
        v_total = v_unit * qtd_letras
        
        # Painel de Detalhes
        st.write(f"🔹 **Corpo (3D):** R$ {custo_corpo:,.2f}")
        st.write(f"🔹 **Face:** R$ {custo_face:,.2f}")
        st.write(f"🔹 **Fundo:** R$ {custo_fundo:,.2f}")
        st.write(f"🔹 **LED:** R$ {v_led:,.2f}")
        st.write(f"🔹 **Energia:** R$ {custo_energia:,.2f}")
        
        st.divider()
        st.metric("TOTAL GERAL", f"R$ {v_total:,.2f}")
        st.metric("UNITÁRIO", f"R$ {v_unit:,.2f}")

        # BOTÃO DE PDF REAL
        resumo_texto = f"Detalhes: {qtd_letras} letras, Dimensões {h}x{w}x{p}cm, Maquina {modelo}"
        pdf_bytes = gerar_pdf(nome_cliente, texto, v_total, v_unit, resumo_texto)
        
        st.download_button(
            label="📩 BAIXAR ORÇAMENTO EM PDF",
            data=pdf_bytes,
            file_name=f"Orcamento_{nome_cliente}.pdf",
            mime="application/pdf"
        )
else:
    st.warning("⚠️ Insira a senha na barra lateral.")
