import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - Precificação Pro", layout="wide")

# 2. BANCOS DE DADOS COMPLETOS
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
    ]
}

# 3. ACESSO (SENHA)
st.sidebar.title("🔐 Acesso Hugo Pro")
senha = st.sidebar.text_input("Chave Mensal", type="password")

if senha == "HUGO2026":
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("📝 DADOS DO PROJETO", expanded=True):
            texto = st.text_input("Texto do Letreiro").upper()
            qtd_letras = len(texto.replace(" ", ""))
            c1, c2, c3 = st.columns(3)
            h = c1.number_input("Altura (cm)", value=30)
            w = c2.number_input("Largura (cm)", value=32)
            p = c3.number_input("Profundidade (cm)", value=5)

        with st.expander("🏗️ MATERIAIS E COMPONENTES", expanded=True):
            f1, f2 = st.columns(2)
            # Material da Face
            face_opcoes = {"Nenhum": 0, "Acrílico 2mm": 15, "Acrílico 3mm": 25, "Policarbonato 2mm": 35, "Policarbonato 3mm": 45}
            face_sel = f1.selectbox("Material da Face", list(face_opcoes.keys()), index=3)
            
            # Cor da Face
            cor_opcoes = {"Branca (Padrão)": 0, "Colorida (+R$20)": 20}
            cor_sel = f2.selectbox("Cor da Face", list(cor_opcoes.keys()))
            
            # Material do Fundo
            fundo_opcoes = {"Sem Fundo": 0, "PVC 5mm": 15, "PVC 10mm": 25, "Impressão 3D": 12, "ACM 3mm": 30}
            fundo_sel = st.selectbox("Material do Fundo (Base)", list(fundo_opcoes.keys()), index=1)
            
            # Iluminação
            led_opcoes = {"Sem LED": 0, "Branco Frio/Quente": 45, "RGB Colorido": 75}
            led_sel = st.selectbox("Iluminação LED", list(led_opcoes.keys()))

        with st.expander("⚙️ CONFIGURAÇÃO TÉCNICA", expanded=True):
            est_col, imp_col = st.columns(2)
            estado = est_col.selectbox("Localização", list(BASE_REGIONAL.keys()))
            marca = imp_col.selectbox("Marca", list(IMPRESSORAS.keys()))
            modelo = st.selectbox("Modelo", [m['nome'] for m in IMPRESSORAS[marca]])
            
            # Material do Corpo
            corpo_opcoes = {"PETG UV (Externo)": 130, "PLA (Interno)": 100}
            corpo_sel = st.selectbox("Material do Corpo", list(corpo_opcoes.keys()))

        with st.expander("👥 PERFIL DE CLIENTE", expanded=True):
            perfil = st.radio("Tipo de Venda", ["Cliente Final (100%)", "Terceirização (80%)"], horizontal=True)
            ajuste = st.slider("Ajuste Manual (%)", -50, 100, 0)

    # 4. LÓGICA DE CÁLCULO (EXATA DO ORIGINAL)
    with col2:
        st.subheader("💰 ORÇAMENTO")
        
        # Recuperar dados técnicos
        maq_data = next(m for m in IMPRESSORAS[marca] if m['nome'] == modelo)
        kwh, mult_mat = BASE_REGIONAL[estado]
        
        # Valores dos itens selecionados
        v_face = face_opcoes[face_sel] * mult_mat
        v_cor = cor_opcoes[cor_sel]
        v_fundo = fundo_opcoes[fundo_sel] * mult_mat
        v_led = led_opcoes[led_sel]
        v_mat_corpo = corpo_sel * mult_mat
        
        # Cálculo do Corpo e Energia
        preco_corpo = ((h*2) + (w*2)) * p * 0.17808 * maq_data['fator'] * (v_mat_corpo / 130)
        energia = ((h + w) / 10) * maq_data['fator'] * (maq_data['watts'] / 1000) * kwh
        
        # Valor Unitário Base
        valor_unit = preco_corpo + v_face + v_fundo + v_led + v_cor + energia
        
        # Aplicar Perfil e Ajuste
        fator_perfil = 0.8 if "Terceirização" in perfil else 1.0
        valor_unit = valor_unit * fator_perfil * (1 + (ajuste / 100))
        
        total_geral = valor_unit * qtd_letras

        st.metric("VALOR TOTAL", f"R$ {total_geral:,.2f}")
        st.write(f"**Unitário:** R$ {valor_unit:,.2f}/Un.")
        st.divider()
        st.info(f"Quantidade: {qtd_letras} letras")
        
        if st.button("🖨️ IMPRIMIR ORÇAMENTO"):
            st.write("Dica: Use o atalho Ctrl+P no navegador para salvar em PDF.")

else:
    st.warning("⚠️ Insira a Chave de Acesso na barra lateral.")
