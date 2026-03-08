import streamlit as stimport streamlit as st
from fpdf import FPDF

# 1. TÍTULO DO SEU SISTEMA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. BANCO DE DADOS (Suas fórmulas originais)
BASE_REGIONAL = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "SC - Celesc": [0.76, 0.98],
    "RJ - Light": [0.98, 1.02], "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98]
}

IMPRESSORAS = {
    "Anycubic": [{"nome": "Kobra 2 Max", "fator": 1.0, "watts": 500}, {"nome": "Kobra 3 Max", "fator": 0.95, "watts": 550}],
    "Creality": [{"nome": "K1 Max", "fator": 0.9, "watts": 1000}]
}

# 3. ACESSO POR SENHA
senha = st.sidebar.text_input("CHAVE DE ACESSO", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([1.5, 1])

    with col1:
        nome_cli = st.text_input("NOME DO CLIENTE", "CLIENTE").upper()
        prazo_v = st.selectbox("PRAZO DE PRODUÇÃO", ["7 a 10 dias úteis", "10 a 15 dias úteis", "A combinar"])
        
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            txt_p = st.text_input("TEXTO DO LETREIRO", "EXEMPLO").upper()
            qtd_l = len(txt_p.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h, w, p = c1.number_input("ALTURA (cm)", 30), c2.number_input("LARGURA (cm)", 32), c3.number_input("PROFUNDIDADE (cm)", 5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            # MAPA DE VALORES (Isso evita o erro TypeError da sua imagem)
            f_map = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            fun_map = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            led_map = {"Sem LED": 0, "LED Branco": 45, "LED RGB": 75}
            corpo_map = {"Uso Externo (PETG c/ UV)": 130, "Uso Interno (PLA)": 100}

            f_sel = st.selectbox("FACE", list(f_map.keys()), index=2)
            fun_sel = st.selectbox("FUNDO", list(fun_map.keys()), index=1)
            l_sel = st.selectbox("ILUMINAÇÃO", list(led_map.keys()))
            cor_sel = st.selectbox("MATERIAL DO CORPO", list(corpo_map.keys()))

    with col2:
        st.subheader("💰 DETALHAMENTO DE VALOR")
        
        est = st.selectbox("LOCALIZAÇÃO", list(BASE_REGIONAL.keys()))
        mrc = st.selectbox("MARCA", list(IMPRESSORAS.keys()))
        mod = st.selectbox("MODELO", [m['nome'] for m in IMPRESSORAS[mrc]])
        maq = next(m for m in IMPRESSORAS[mrc] if m['nome'] == mod)
        kwh, mult_m = BASE_REGIONAL[est]

        # CÁLCULOS (Usando os valores numéricos dos mapas)
        v_face = f_map[f_sel] * mult_m
        v_fundo = fun_map[fun_sel] * mult_m
        v_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq['fator'] * (corpo_map[cor_sel] * mult_m / 130)
        v_led = led_map[l_sel]
        
        u_final = v_corpo + v_face + v_fundo + v_led
        t_final = u_final * qtd_l

        # PAINEL DE RESULTADOS
        res_box = st.container(border=True)
        res_box.write(f"🔹 **Corpo:** R$ {v_corpo:,.2f}")
        res_box.write(f"🔹 **Face:** R$ {v_face:,.2f}")
        res_box.write(f"🔹 **Fundo:** R$ {v_fundo:,.2f}")
        res_box.write(f"🔹 **LED:** R$ {v_led:,.2f}")
        
        st.divider()
        st.metric("VALOR TOTAL", f"R$ {t_final:,.2f}")
        st.write(f"**Unitário:** R$ {u_final:,.2f}")

        # GERADOR DE PDF
        if st.button("📄 GERAR PDF"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(190, 10, "SPP - SISTEMA DE PRECIFICACAO PRO", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", '', 11)
                pdf.cell(190, 8, f"CLIENTE: {nome_cli}", ln=True)
                pdf.cell(190, 8, f"PROJETO: {txt_p} ({qtd_l} letras)", ln=True)
                pdf.cell(190, 8, f"PRAZO: {prazo_v}", ln=True)
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(190, 12, f"VALOR TOTAL: R$ {t_final:,.2f}", 1, ln=True, align='C')
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button("📥 BAIXAR PDF", pdf_bytes, f"Orcamento_{nome_cli}.pdf", "application/pdf")
            except:
                st.error("Erro técnico no PDF. Evite acentos nos campos de texto.")
else:
    st.sidebar.warning("Insira a Chave de Acesso.")
from fpdf import FPDF

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. BANCO DE DADOS (Mantendo suas fórmulas e máquinas originais)
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
        {"nome": "Kobra 3 Max", "fator": 0.95, "watts": 550}
    ],
    "Elegoo": [{"nome": "Neptune 4 Max", "fator": 0.95, "watts": 500}],
    "Bambu Lab": [{"nome": "X1-Carbon", "fator": 0.85, "watts": 350}],
    "Creality": [{"nome": "K1 Max", "fator": 0.9, "watts": 1000}]
}

# 3. ACESSO POR SENHA
senha = st.sidebar.text_input("CHAVE DE ACESSO", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([1.5, 1])

    with col1:
        nome_cli = st.text_input("NOME DO CLIENTE", "CLIENTE").upper()
        prazo_v = st.selectbox("PRAZO DE PRODUÇÃO", ["7 a 10 dias úteis", "10 a 15 dias úteis", "A combinar"])
        
        with st.expander("📝 DIMENSÕES E TEXTO", expanded=True):
            txt_p = st.text_input("TEXTO DO LETREIRO", "EXEMPLO").upper()
            qtd_l = len(txt_p.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h, w, p = c1.number_input("ALTURA (cm)", 30), c2.number_input("LARGURA (cm)", 32), c3.number_input("PROFUNDIDADE (cm)", 5)

        with st.expander("🏗️ MATERIAIS", expanded=True):
            # Mapeamento para evitar erro de multiplicação de texto
            f_map = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            fun_map = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            led_map = {"Sem LED": 0, "LED Branco": 45, "LED RGB": 75}
            corpo_map = {"Uso Externo (PETG c/ UV)": 130, "Uso Interno (PLA)": 100}

            f_sel = st.selectbox("MATERIAL DA FACE", list(f_map.keys()), index=2)
            fun_sel = st.selectbox("MATERIAL DO FUNDO", list(fun_map.keys()), index=1)
            l_sel = st.selectbox("ILUMINAÇÃO LED", list(led_map.keys()))
            cor_sel = st.selectbox("MATERIAL DO CORPO", list(corpo_map.keys()))

    with col2:
        st.subheader("💰 DETALHAMENTO DE VALOR")
        
        # Seleção de Máquina e Localização
        est = st.selectbox("SUA LOCALIZAÇÃO", list(BASE_REGIONAL.keys()))
        mrc = st.selectbox("MARCA DA MÁQUINA", list(IMPRESSORAS.keys()))
        mod = st.selectbox("MODELO DA MÁQUINA", [m['nome'] for m in IMPRESSORAS[mrc]])
        maq = next(m for m in IMPRESSORAS[mrc] if m['nome'] == mod)
        kwh, mult_m = BASE_REGIONAL[est]

        # CÁLCULOS TÉCNICOS (Lógica Hugo Letra Caixa PRO)
        v_face = f_map[f_sel] * mult_m
        v_fundo = fun_map[fun_sel] * mult_m
        v_corpo_base = corpo_map[cor_sel]
        v_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq['fator'] * (v_corpo_base * mult_m / 130)
        v_led = led_map[l_sel]
        
        u_final = v_corpo + v_face + v_fundo + v_led
        t_final = u_final * qtd_l

        # PAINEL DE RESULTADOS
        res_box = st.container(border=True)
        res_box.write(f"🔹 **Corpo (3D):** R$ {v_corpo:,.2f}")
        res_box.write(f"🔹 **Face:** R$ {v_face:,.2f}")
        res_box.write(f"🔹 **Fundo:** R$ {v_fundo:,.2f}")
        res_box.write(f"🔹 **LED:** R$ {v_led:,.2f}")
        
        st.divider()
        st.metric("VALOR TOTAL DO PROJETO", f"R$ {t_final:,.2f}")
        st.write(f"**Valor por Letra:** R$ {u_final:,.2f}")

        # BOTÃO GERADOR DE PDF
        if st.button("📄 GERAR ORÇAMENTO EM PDF"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(190, 10, "SPP - SISTEMA DE PRECIFICACAO PRO", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", '', 11)
                pdf.cell(190, 8, f"CLIENTE: {nome_cli}", ln=True)
                pdf.cell(190, 8, f"PROJETO: {txt_p} ({qtd_l} letras)", ln=True)
                pdf.cell(190, 8, f"DIMENSOES: {h}cm x {w}cm x {p}cm", ln=True)
                pdf.cell(190, 8, f"PRAZO DE PRODUCAO: {prazo_v}", ln=True)
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(190, 12, f"VALOR TOTAL: R$ {t_final:,.2f}", 1, ln=True, align='C')
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button("📥 CLIQUE PARA BAIXAR PDF", pdf_bytes, f"Orcamento_{nome_cli}.pdf", "application/pdf")
            except:
                st.error("Erro técnico ao gerar PDF. Evite acentos especiais.")
else:
    st.sidebar.warning("⚠️ Aguardando Chave de Acesso Mensal.")

