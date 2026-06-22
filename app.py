import streamlit as st
from datetime import datetime
import json
import os
from collections import Counter

# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(
    page_title="Sistema de Ocorrências Policiais",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ ESTILO CSS PROFISSIONAL ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* ===== VARIÁVEIS DE CORES ===== */
    :root {
        --primary: #1e3a5f;
        --primary-light: #2a4a73;
        --accent: #e63946;
        --accent-hover: #c1121f;
        --success: #2a9d8f;
        --warning: #f4a261;
        --danger: #e63946;
        --info: #457b9d;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --bg-card-hover: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border: #334155;
    }

    /* ===== RESET E BASE ===== */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin: 4px 0 !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.05) !important;
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] .stRadio label[data-selected="true"] {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.4) !important;
    }

    /* ===== TÍTULOS ===== */
    h1 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }

    /* ===== CARDS ===== */
    .card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid var(--border);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        margin-bottom: 16px;
    }

    .card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        border-color: rgba(255,255,255,0.1);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
    }

    .card-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .card-title {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
    }

    .card-subtitle {
        color: var(--text-secondary);
        font-size: 0.85rem;
    }

    /* ===== OCORRÊNCIA CARD ===== */
    .ocorrencia-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        border-left: 4px solid var(--accent);
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }

    .ocorrencia-card:hover {
        transform: translateX(4px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.3);
    }

    .ocorrencia-ativa {
        border-left: 4px solid var(--warning);
        background: linear-gradient(135deg, #1e293b 0%, #2a1810 100%);
    }

    .ocorrencia-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .ocorrencia-id {
        background: rgba(255,255,255,0.1);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    .ocorrencia-prioridade {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .ocorrencia-body {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    .ocorrencia-meta {
        display: flex;
        gap: 16px;
        margin-top: 12px;
        flex-wrap: wrap;
    }

    .ocorrencia-meta-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* ===== BADGES ===== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .badge-pendente {
        background: rgba(230, 57, 70, 0.15);
        color: #ff6b6b;
        border: 1px solid rgba(230, 57, 70, 0.3);
    }

    .badge-andamento {
        background: rgba(244, 162, 97, 0.15);
        color: #f4a261;
        border: 1px solid rgba(244, 162, 97, 0.3);
    }

    .badge-resolvida {
        background: rgba(42, 157, 143, 0.15);
        color: #2a9d8f;
        border: 1px solid rgba(42, 157, 143, 0.3);
    }

    /* ===== PRIORIDADES ===== */
    .prioridade-baixa { background: rgba(42, 157, 143, 0.15); color: #2a9d8f; border: 1px solid rgba(42, 157, 143, 0.3); }
    .prioridade-media { background: rgba(69, 123, 157, 0.15); color: #457b9d; border: 1px solid rgba(69, 123, 157, 0.3); }
    .prioridade-alta { background: rgba(244, 162, 97, 0.15); color: #f4a261; border: 1px solid rgba(244, 162, 97, 0.3); }
    .prioridade-critica { background: rgba(230, 57, 70, 0.15); color: #e63946; border: 1px solid rgba(230, 57, 70, 0.3); animation: pulse 2s infinite; }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    /* ===== BOTÕES ===== */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        border: none !important;
        padding: 12px 24px !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }

    .btn-primary {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%) !important;
        color: white !important;
    }

    .btn-success {
        background: linear-gradient(135deg, var(--success) 0%, #1d7a6e 100%) !important;
        color: white !important;
    }

    .btn-info {
        background: linear-gradient(135deg, var(--info) 0%, #2a5a7a 100%) !important;
        color: white !important;
    }

    /* ===== INPUTS ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.3) !important;
    }

    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    .streamlit-expanderContent {
        background: var(--bg-dark) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }

    /* ===== METRIC CARDS ===== */
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
    }

    /* ===== TIMELINE ===== */
    .timeline {
        position: relative;
        padding-left: 24px;
    }

    .timeline::before {
        content: '';
        position: absolute;
        left: 8px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(180deg, var(--primary) 0%, var(--border) 100%);
    }

    .timeline-item {
        position: relative;
        padding: 12px 0;
        padding-left: 16px;
    }

    .timeline-item::before {
        content: '';
        position: absolute;
        left: -20px;
        top: 16px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--primary);
        border: 2px solid var(--bg-dark);
    }

    .timeline-time {
        font-size: 0.75rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    .timeline-text {
        color: var(--text-primary);
        font-size: 0.9rem;
        margin-top: 4px;
    }

    /* ===== POLICIAL CARD ===== */
    .policial-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.2s ease;
    }

    .policial-card:hover {
        border-color: var(--primary);
        transform: translateX(4px);
    }

    .policial-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: white;
        font-size: 0.9rem;
    }

    .policial-info {
        flex: 1;
    }

    .policial-nome {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 0.95rem;
    }

    .policial-cargo {
        color: var(--text-secondary);
        font-size: 0.8rem;
    }

    /* ===== ALERTAS ===== */
    .alert {
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .alert-success {
        background: rgba(42, 157, 143, 0.1);
        border: 1px solid rgba(42, 157, 143, 0.3);
        color: #2a9d8f;
    }

    .alert-warning {
        background: rgba(244, 162, 97, 0.1);
        border: 1px solid rgba(244, 162, 97, 0.3);
        color: #f4a261;
    }

    .alert-danger {
        background: rgba(230, 57, 70, 0.1);
        border: 1px solid rgba(230, 57, 70, 0.3);
        color: #e63946;
    }

    .alert-info {
        background: rgba(69, 123, 157, 0.1);
        border: 1px solid rgba(69, 123, 157, 0.3);
        color: #457b9d;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border) 50%, transparent 100%);
        margin: 24px 0;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-light);
    }

    /* ===== EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
    }

    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 16px;
        opacity: 0.5;
    }

    .empty-state-title {
        color: var(--text-primary);
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .empty-state-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }

    /* ===== PROGRESS BAR ===== */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: var(--bg-dark);
        border-radius: 4px;
        overflow: hidden;
        margin-top: 8px;
    }

    .progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }

    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 20px;
        color: var(--text-secondary);
        font-size: 0.8rem;
        border-top: 1px solid var(--border);
        margin-top: 40px;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .card {
            padding: 16px;
        }

        .ocorrencia-meta {
            flex-direction: column;
            gap: 8px;
        }
    }

    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============ ESTRUTURA DE DADOS (PILHA) ============
class Ocorrencia:
    def __init__(self, id_ocorrencia, tipo, descricao, local, prioridade, solicitante):
        self.id = id_ocorrencia
        self.tipo = tipo
        self.descricao = descricao
        self.local = local
        self.prioridade = prioridade
        self.solicitante = solicitante
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.status = "Pendente"
        self.policial_responsavel = None
        self.historico_acoes = []
        self.data_resolucao = None

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "local": self.local,
            "prioridade": self.prioridade,
            "solicitante": self.solicitante,
            "data_hora": self.data_hora,
            "status": self.status,
            "policial_responsavel": self.policial_responsavel,
            "historico_acoes": self.historico_acoes,
            "data_resolucao": self.data_resolucao
        }

class PilhaOcorrencias:
    def __init__(self):
        self.items = []
        self.proximo_id = 1

    def push(self, ocorrencia):
        self.items.append(ocorrencia)
        self.proximo_id += 1

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def listar_todos(self):
        return list(reversed(self.items))

    def buscar_por_id(self, id_ocorrencia):
        for item in self.items:
            if item.id == id_ocorrencia:
                return item
        return None

# ============ PERSISTÊNCIA ============
ARQUIVO_DADOS = "dados_ocorrencias.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            pilha = PilhaOcorrencias()
            pilha.proximo_id = dados.get("proximo_id", 1)
            for item in dados.get("ocorrencias", []):
                o = Ocorrencia(
                    item["id"], item["tipo"], item["descricao"],
                    item["local"], item["prioridade"], item["solicitante"]
                )
                o.data_hora = item["data_hora"]
                o.status = item["status"]
                o.policial_responsavel = item["policial_responsavel"]
                o.historico_acoes = item["historico_acoes"]
                o.data_resolucao = item["data_resolucao"]
                pilha.items.append(o)
            return pilha
    return PilhaOcorrencias()

def salvar_dados(pilha):
    dados = {
        "proximo_id": pilha.proximo_id,
        "ocorrencias": [o.to_dict() for o in pilha.items]
    }
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ============ INICIALIZAÇÃO ============
if 'pilha' not in st.session_state:
    st.session_state.pilha = carregar_dados()

if 'policiais' not in st.session_state:
    st.session_state.policiais = ["Sgt. Silva", "Cb. Santos", "Sd. Oliveira", "Ten. Costa", "Sd. Pereira"]

# ============ HELPERS ============
def get_prioridade_class(prioridade):
    return {
        "Baixa": "prioridade-baixa",
        "Média": "prioridade-media",
        "Alta": "prioridade-alta",
        "Crítica": "prioridade-critica"
    }.get(prioridade, "prioridade-media")

def get_status_class(status):
    return {
        "Pendente": "badge-pendente",
        "Em Andamento": "badge-andamento",
        "Resolvida": "badge-resolvida"
    }.get(status, "badge-pendente")

def get_tipo_icon(tipo):
    return {
        "Roubo/Furto": "💰",
        "Agressão": "👊",
        "Acidente": "🚗",
        "Distúrbio": "📢",
        "Tráfico": "💊",
        "Homicídio": "🔪",
        "Desaparecimento": "🔍",
        "Outros": "📋"
    }.get(tipo, "📋")

# ============ HEADER ============
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.markdown("<div style='font-size: 3rem; text-align: center;'>🚔</div>", unsafe_allow_html=True)
with col_title:
    st.title("Sistema de Controle de Ocorrências")
    st.markdown("<p style='color: #94a3b8; margin-top: -8px;'>Gestão inteligente de ocorrências policiais · Estrutura: Pilha (LIFO)</p>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 3rem;'>🚔</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f1f5f9; margin: 8px 0;'>Polícia</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem;'>Sistema de Ocorrências</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)

    menu = st.radio("Menu", [
        "📞 Registrar Ocorrência",
        "👮 Painel Policial",
        "📊 Histórico e Estatísticas",
        "⚙️ Configurações"
    ], label_visibility="collapsed")

    st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)

    # Status rápido
    st.markdown("<p style='color: #94a3b8; font-size: 0.8rem; font-weight: 600; margin-bottom: 12px;'>📊 STATUS RÁPIDO</p>", unsafe_allow_html=True)

    todas = st.session_state.pilha.listar_todos()
    pendentes = sum(1 for o in todas if o.status == "Pendente")
    andamento = sum(1 for o in todas if o.status == "Em Andamento")
    criticas = sum(1 for o in todas if o.prioridade == "Crítica")

    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; margin: 8px 0; padding: 8px 12px; background: rgba(255,255,255,0.03); border-radius: 8px;'>
        <span style='color: #94a3b8; font-size: 0.85rem;'>Total</span>
        <span style='color: #f1f5f9; font-weight: 600; font-size: 0.9rem;'>{st.session_state.pilha.size()}</span>
    </div>
    <div style='display: flex; justify-content: space-between; margin: 8px 0; padding: 8px 12px; background: rgba(255,255,255,0.03); border-radius: 8px;'>
        <span style='color: #94a3b8; font-size: 0.85rem;'>Pendentes</span>
        <span style='color: #ff6b6b; font-weight: 600; font-size: 0.9rem;'>{pendentes}</span>
    </div>
    <div style='display: flex; justify-content: space-between; margin: 8px 0; padding: 8px 12px; background: rgba(255,255,255,0.03); border-radius: 8px;'>
        <span style='color: #94a3b8; font-size: 0.85rem;'>Em Andamento</span>
        <span style='color: #f4a261; font-weight: 600; font-size: 0.9rem;'>{andamento}</span>
    </div>
    <div style='display: flex; justify-content: space-between; margin: 8px 0; padding: 8px 12px; background: rgba(255,255,255,0.03); border-radius: 8px;'>
        <span style='color: #94a3b8; font-size: 0.85rem;'>Críticas</span>
        <span style='color: #e63946; font-weight: 600; font-size: 0.9rem;'>{criticas}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)

    st.markdown("<p style='color: #64748b; font-size: 0.75rem; text-align: center;'>🚔 Sistema Policial v2.0<br>Estrutura: Pilha (Stack)</p>", unsafe_allow_html=True)

# ============ 1. REGISTRAR OCORRÊNCIA ============
if menu == "📞 Registrar Ocorrência":
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon" style="background: linear-gradient(135deg, #e63946 0%, #c1121f 100%);">📞</div>
            <div>
                <div class="card-title">Registrar Nova Ocorrência</div>
                <div class="card-subtitle">Preencha os dados abaixo. A ocorrência será colocada no topo da pilha.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_ocorrencia"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;'>📋 INFORMAÇÕES DA OCORRÊNCIA</p>", unsafe_allow_html=True)
            tipo = st.selectbox("Tipo de Ocorrência", [
                "Roubo/Furto", "Agressão", "Acidente", "Distúrbio", 
                "Tráfico", "Homicídio", "Desaparecimento", "Outros"
            ], label_visibility="collapsed")

            prioridade = st.select_slider("Prioridade", 
                options=["Baixa", "Média", "Alta", "Crítica"], value="Média")

            solicitante = st.text_input("Nome do Solicitante", placeholder="Quem está ligando?")

        with col2:
            st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;'>📍 LOCAL E DETALHES</p>", unsafe_allow_html=True)
            local = st.text_input("Local da Ocorrência", placeholder="Endereço completo")
            descricao = st.text_area("Descrição", placeholder="Detalhes da ocorrência...", height=120)

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            submitted = st.form_submit_button("🚨 REGISTRAR OCORRÊNCIA", use_container_width=True)

        if submitted:
            if local and descricao and solicitante:
                nova_ocorrencia = Ocorrencia(
                    st.session_state.pilha.proximo_id,
                    tipo, descricao, local, prioridade, solicitante
                )
                st.session_state.pilha.push(nova_ocorrencia)
                salvar_dados(st.session_state.pilha)

                st.markdown(f"""
                <div class="alert alert-success">
                    <span style="font-size: 1.2rem;">✅</span>
                    <div>
                        <strong>Ocorrência #{nova_ocorrencia.id} registrada com sucesso!</strong><br>
                        <span style="font-size: 0.85rem; opacity: 0.8;">Posição na pilha: <strong>TOPO</strong> · Prioridade: {prioridade}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown("""
                <div class="alert alert-danger">
                    <span style="font-size: 1.2rem;">⚠️</span>
                    <div><strong>Preencha todos os campos obrigatórios!</strong></div>
                </div>
                """, unsafe_allow_html=True)

# ============ 2. PAINEL POLICIAL ============
elif menu == "👮 Painel Policial":
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon" style="background: linear-gradient(135deg, #f4a261 0%, #e76f51 100%);">👮</div>
            <div>
                <div class="card-title">Painel Policial</div>
                <div class="card-subtitle">Visualize o topo da pilha e gerencie ocorrências ativas.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    topo = st.session_state.pilha.peek()

    if topo:
        prioridade_class = get_prioridade_class(topo.prioridade)
        status_class = get_status_class(topo.status)
        tipo_icon = get_tipo_icon(topo.tipo)

        st.markdown(f"""
        <div class="ocorrencia-card ocorrencia-ativa">
            <div class="ocorrencia-header">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.5rem;">{tipo_icon}</span>
                    <div>
                        <div style="color: #f1f5f9; font-weight: 700; font-size: 1.1rem;">OCORRÊNCIA ATIVA #{topo.id}</div>
                        <div style="color: #94a3b8; font-size: 0.85rem;">{topo.tipo}</div>
                    </div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span class="badge {prioridade_class}">● {topo.prioridade}</span>
                    <span class="badge {status_class}">{topo.status}</span>
                </div>
            </div>
            <div class="ocorrencia-body">
                <p><strong style="color: #f1f5f9;">Descrição:</strong> {topo.descricao}</p>
            </div>
            <div class="ocorrencia-meta">
                <div class="ocorrencia-meta-item">
                    <span>📍</span> {topo.local}
                </div>
                <div class="ocorrencia-meta-item">
                    <span>👤</span> {topo.solicitante}
                </div>
                <div class="ocorrencia-meta-item">
                    <span>🕐</span> {topo.data_hora}
                </div>
                {f'<div class="ocorrencia-meta-item"><span>👮</span> {topo.policial_responsavel}</div>' if topo.policial_responsavel else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #f1f5f9; font-size: 1.1rem; margin-bottom: 16px;'>🎯 Ações Disponíveis</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            if not topo.policial_responsavel:
                st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;'>✋ ASSUMIR OCORRÊNCIA</p>", unsafe_allow_html=True)
                policial = st.selectbox("Selecione o Policial", st.session_state.policiais, label_visibility="collapsed")
                if st.button("✋ Assumir Ocorrência", use_container_width=True):
                    topo.policial_responsavel = policial
                    topo.status = "Em Andamento"
                    topo.historico_acoes.append(f"{datetime.now().strftime('%H:%M:%S')} - Assumida por {policial}")
                    salvar_dados(st.session_state.pilha)
                    st.rerun()
            else:
                st.markdown(f"""
                <div class="policial-card">
                    <div class="policial-avatar">{topo.policial_responsavel[0]}</div>
                    <div class="policial-info">
                        <div class="policial-nome">{topo.policial_responsavel}</div>
                        <div class="policial-cargo">Responsável pela ocorrência</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;'>📝 REGISTRAR AÇÃO</p>", unsafe_allow_html=True)
            acao = st.text_input("Registrar Ação", placeholder="Ex: Chegada ao local...", label_visibility="collapsed")
            if st.button("📝 Adicionar Ação", use_container_width=True):
                if acao:
                    topo.historico_acoes.append(f"{datetime.now().strftime('%H:%M:%S')} - {acao}")
                    salvar_dados(st.session_state.pilha)
                    st.rerun()

        with col3:
            st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;'>✅ FINALIZAR</p>", unsafe_allow_html=True)
            if st.button("✅ Finalizar Ocorrência", use_container_width=True, type="primary"):
                topo.status = "Resolvida"
                topo.data_resolucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                topo.historico_acoes.append(f"{datetime.now().strftime('%H:%M:%S')} - Ocorrência resolvida")
                st.session_state.pilha.pop()
                salvar_dados(st.session_state.pilha)
                st.rerun()

        if topo.historico_acoes:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #f1f5f9; font-size: 1.1rem; margin-bottom: 16px;'>📜 Histórico de Ações</h3>", unsafe_allow_html=True)

            st.markdown("<div class='timeline'>", unsafe_allow_html=True)
            for acao in reversed(topo.historico_acoes):
                hora, texto = acao.split(" - ", 1)
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-time">{hora}</div>
                    <div class="timeline-text">{texto}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <div class="empty-state-title">Pilha Vazia</div>
            <div class="empty-state-text">Não há ocorrências na pilha. Todas foram resolvidas!</div>
        </div>
        """, unsafe_allow_html=True)

# ============ 3. HISTÓRICO E ESTATÍSTICAS ============
elif menu == "📊 Histórico e Estatísticas":
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon" style="background: linear-gradient(135deg, #457b9d 0%, #1d3557 100%);">📊</div>
            <div>
                <div class="card-title">Histórico e Estatísticas</div>
                <div class="card-subtitle">Visualize dados e métricas do sistema.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    todas = st.session_state.pilha.listar_todos()

    # Métricas
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 700; color: #f1f5f9;">{st.session_state.pilha.size()}</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Total na Pilha</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        pendentes = sum(1 for o in todas if o.status == "Pendente")
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 700; color: #ff6b6b;">{pendentes}</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Pendentes</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        andamento = sum(1 for o in todas if o.status == "Em Andamento")
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 700; color: #f4a261;">{andamento}</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Em Andamento</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        criticas = sum(1 for o in todas if o.prioridade == "Crítica")
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 700; color: #e63946;">{criticas}</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Críticas</div>
        </div>
        """, unsafe_allow_html=True)

    # Visualização da Pilha
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f1f5f9; font-size: 1.1rem; margin-bottom: 16px;'>📚 Visualização da Pilha (Topo → Base)</h3>", unsafe_allow_html=True)

    if not todas:
        st.markdown("""
        <div class="empty-state" style="padding: 40px 20px;">
            <div class="empty-state-icon">📚</div>
            <div class="empty-state-title">Pilha Vazia</div>
            <div class="empty-state-text">Nenhuma ocorrência registrada.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, ocorrencia in enumerate(todas):
            prioridade_class = get_prioridade_class(ocorrencia.prioridade)
            status_class = get_status_class(ocorrencia.status)
            tipo_icon = get_tipo_icon(ocorrencia.tipo)

            with st.expander(f"#{ocorrencia.id} - {ocorrencia.tipo} [{ocorrencia.prioridade}] ({ocorrencia.status})"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div style="color: #f1f5f9; line-height: 1.8;">
                        <p><strong>Local:</strong> {ocorrencia.local}</p>
                        <p><strong>Descrição:</strong> {ocorrencia.descricao}</p>
                        <p><strong>Solicitante:</strong> {ocorrencia.solicitante}</p>
                        <p><strong>Data/Hora:</strong> {ocorrencia.data_hora}</p>
                        {f'<p><strong>Policial:</strong> {ocorrencia.policial_responsavel}</p>' if ocorrencia.policial_responsavel else ''}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 16px; background: rgba(255,255,255,0.03); border-radius: 12px;">
                        <div style="font-size: 2rem; font-weight: 700; color: #f1f5f9;">{i+1}º</div>
                        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Posição</div>
                        {f'<div style="margin-top: 8px; padding: 4px 12px; background: #e63946; color: white; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">🔴 TOPO</div>' if i == 0 else ''}
                    </div>
                    """, unsafe_allow_html=True)

    # Gráfico
    if todas:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #f1f5f9; font-size: 1.1rem; margin-bottom: 16px;'>📈 Distribuição por Tipo</h3>", unsafe_allow_html=True)

        tipos = Counter(o.tipo for o in todas)
        st.bar_chart(tipos, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #f1f5f9; font-size: 1.1rem; margin-bottom: 16px;'>📈 Distribuição por Prioridade</h3>", unsafe_allow_html=True)

        prioridades = Counter(o.prioridade for o in todas)
        st.bar_chart(prioridades, use_container_width=True)

# ============ 4. CONFIGURAÇÕES ============
elif menu == "⚙️ Configurações":
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon" style="background: linear-gradient(135deg, #6c757d 0%, #495057 100%);">⚙️</div>
            <div>
                <div class="card-title">Configurações do Sistema</div>
                <div class="card-subtitle">Gerencie policiais e dados do sistema.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("👮 Gerenciar Policiais"):
        st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 12px;'>Adicione ou remova policiais do sistema.</p>", unsafe_allow_html=True)

        novo_policial = st.text_input("Nome do Novo Policial", placeholder="Ex: Sgt. Souza")
        if st.button("➕ Adicionar Policial", use_container_width=True):
            if novo_policial:
                st.session_state.policiais.append(novo_policial)
                st.markdown(f"""
                <div class="alert alert-success">
                    <span style="font-size: 1.2rem;">✅</span>
                    <div><strong>{novo_policial}</strong> adicionado com sucesso!</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;'>Policiais Cadastrados</p>", unsafe_allow_html=True)

        for p in st.session_state.policiais:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="policial-card">
                    <div class="policial-avatar">{p[0]}</div>
                    <div class="policial-info">
                        <div class="policial-nome">{p}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_{p}"):
                    st.session_state.policiais.remove(p)
                    st.rerun()

    with st.expander("🗑️ Limpar Dados"):
        st.markdown("""
        <div class="alert alert-danger">
            <span style="font-size: 1.2rem;">⚠️</span>
            <div>
                <strong>Atenção:</strong> Esta ação apaga todas as ocorrências permanentemente!<br>
                <span style="font-size: 0.85rem; opacity: 0.8;">Esta operação não pode ser desfeita.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Limpar Todas as Ocorrências", use_container_width=True):
            st.session_state.pilha = PilhaOcorrencias()
            if os.path.exists(ARQUIVO_DADOS):
                os.remove(ARQUIVO_DADOS)
            st.markdown("""
            <div class="alert alert-success">
                <span style="font-size: 1.2rem;">✅</span>
                <div><strong>Dados limpos com sucesso!</strong></div>
            </div>
            """, unsafe_allow_html=True)
            st.rerun()
