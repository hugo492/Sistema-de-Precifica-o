import streamlit as st
from fpdf import FPDF

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. DADOS TÉCNICOS (Baseados no seu arquivo original)
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

# 3. ACESSO POR SENHA
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([2, 1.3])

    with col1:
        nome_cliente = st.text_input("NOME DO CLIENTE", "CLIENTE").upper()
        prazo_prod = st.selectbox("PRAZO DE PRODUÇÃO", ["7 a 10 dias úteis", "10 a 15 dias úteis", "A combinar"])
        
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            texto_projeto = st.text_input("TEXTO DO LETREIRO", "EXEMPLO").upper()
            qtd_letras = len(texto_projeto.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h = c1.number_input("ALTURA (cm)", value=30)
            w = c2.number_input("LARGURA (cm)", value=32)
            p = c3.number_input("PROFUNDIDADE (cm)", value=5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            m1, m2 = st.columns(2)
            face_opts = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = m1.selectbox("MATERIAL DA FACE", list(face_opts.keys()), index=2)
            v_face_base = face_opts[face_sel]
            
            fundo_opts = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            fundo_sel = m2.selectbox("MATERIAL DO FUNDO", list(fundo_opts.keys()), index=1)
            v_fundo_base = fundo_opts[fundo_sel]
            
            led_opts = {"Sem LED": 0, "LED Branco Frio/Quente": 45, "LED RGB": 75}
            led_sel = st.selectbox("ILUMINAÇÃO LED", list(led_opts.keys()))
            v_led = led_opts[led_sel]

        with st.expander("⚙️ CONFIGURAÇÃO TÉCNICA", expanded=True):
            reg_col, imp_col = st.columns(2)
            estado = reg_col.selectbox("LOCALIZAÇÃO", list(BASE_REGIONAL.keys()))
            marca = imp_col.selectbox("MARCA", list(IMPRESSORAS.keys()))
            modelo = st.selectbox("MODELO", [m['nome'] for m in IMPRESSORAS[marca]])
            maq_data = next(m for m in IMPRESSORAS[marca] if m['nome'] == modelo)
            kwh, mult_mat = BASE_REGIONAL[estado]

    # 4. DETALHAMENTO DE VALORES
    with col2:
        st.subheader("💰 DETALHAMENTO DE VALOR")
        
        # Cálculos de custo
        custo_face = v_face_base * mult_mat
        custo_fundo = v_fundo_base * mult_mat
        custo_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq_data['fator'] * mult_mat
        
        total_unitario = custo_corpo + custo_face + custo_fundo + v_led
        total_projeto = total_unitario * qtd_letras
        
        # Exibição detalhada
        box = st.container(border=True)
        box.write(f"📦 **Corpo (Impressão 3D):** R$ {custo_corpo:,.2f}")
        box.write(f"💎 **Face ({face_sel}):** R$ {custo_face:,.2f}")
        box.write(f"📐 **Fundo ({fundo_sel}):** R$ {custo_fundo:,.2f}")
        box.write(f"💡 **LED:** R$ {v_led:,.2f}")
        
        st.divider()
        st.metric("VALOR TOTAL", f"R$ {total_projeto:,.2f}")
        st.write(f"**Valor por Letra:** R$ {total_unitario:,.2f}")

        # 5. GERAÇÃO DO PDF (Corrigida para evitar travamentos)
        try:
            pdf = FPDF()
            pdf.add_page()
            # Título principal
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "SPP - SISTEMA DE PRECIFICACAO PRO", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, f"CLIENTE: {nome_cliente}", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.cell(190, 8, f"PROJETO: {texto_projeto} ({qtd_letras} LETRAS)", ln=True)
            pdf.cell(190, 8, f"DIMENSOES: {h}cm (A) x {w}cm (L) x {p}cm (P)", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(190, 8, "ESPECIFICACOES:", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.cell(190, 7, f"- Face: {face_sel}", ln=True)
            pdf.cell(190, 7, f"- Fundo: {fundo_sel}", ln=True)
            pdf.cell(190, 7, f"- Iluminacao: {led_sel}", ln=True)
            pdf.cell(190, 7, f"- Prazo de Producao: {prazo_prod}", ln=True)
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 14)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(190, 12, f"VALOR TOTAL: R$ {total_projeto:,.2f}", 1, ln=True, align='C', fill=True)
            
            # Gerar os bytes do PDF
            pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
            
            st.download_button(
                label="📥 BAIXAR ORÇAMENTO EM PDF",
                data=pdf_output,
                file_name=f"Orcamento_{nome_cliente}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error("Erro ao gerar PDF. Verifique os caracteres especiais.")

else:
    st.warning("⚠️ Insira a Chave de Acesso na barra lateral.")
