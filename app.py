import streamlit as st
from datetime import datetime
import json
import os

# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(
    page_title="🚨 Sistema de Ocorrências Policiais",
    page_icon="🚔",
    layout="wide"
)

# ============ ESTILO CSS ============
st.markdown("""
<style>
    .ocorrencia-card {
        background-color: #00008b;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #ff4b4b;
    }
    .ocorrencia-ativa {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .status-pendente { color: #ff4b4b; font-weight: bold; }
    .status-andamento { color: #ffc107; font-weight: bold; }
    .status-resolvida { color: #28a745; font-weight: bold; }
    .policial-card {
        background-color: #e8f4f8;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }
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
        self.status = "Pendente"  # Pendente, Em Andamento, Resolvida
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
    """Implementação da Pilha (Stack) para ocorrências"""
    def __init__(self):
        self.items = []
        self.proximo_id = 1
    
    def push(self, ocorrencia):
        """Adicionar ocorrência no topo da pilha"""
        self.items.append(ocorrencia)
        self.proximo_id += 1
    
    def pop(self):
        """Remover ocorrência do topo (LIFO)"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """Ver ocorrência do topo sem remover"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def listar_todos(self):
        """Listar todos (do topo para a base)"""
        return list(reversed(self.items))
    
    def buscar_por_id(self, id_ocorrencia):
        for item in self.items:
            if item.id == id_ocorrencia:
                return item
        return None

# ============ PERSISTÊNCIA ============
ARQUIVO_DADOS = "dados_ocorrencias.json"

def carregar_dados():
    """Carregar dados salvos"""
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
    """Salvar dados em arquivo"""
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

# ============ INTERFACE ============
st.title("🚨 Sistema de Controle de Ocorrências Policiais")
st.markdown("**Sistema baseado em Pilha (LIFO) - Última a entrar, Primeira a sair**")

# Menu lateral
menu = st.sidebar.radio("📋 Menu", [
    "📞 Registrar Ocorrência",
    "👮 Painel Policial",
    "📊 Histórico e Estatísticas",
    "⚙️ Configurações"
])

# ============================================
# 1. REGISTRAR OCORRÊNCIA (Chamada)
# ============================================
if menu == "📞 Registrar Ocorrência":
    st.header("📞 1. Chamar Ocorrência")
    st.markdown("Registre uma nova ocorrência. Ela será colocada no **topo da pilha**.")
    
    with st.form("form_ocorrencia"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo = st.selectbox("Tipo de Ocorrência", [
                "Roubo/Furto", "Agressão", "Acidente", "Distúrbio", 
                "Tráfico", "Homicídio", "Desaparecimento", "Outros"
            ])
            prioridade = st.select_slider("Prioridade", 
                options=["Baixa", "Média", "Alta", "Crítica"], value="Média")
            solicitante = st.text_input("Nome do Solicitante", placeholder="Quem está ligando?")
        
        with col2:
            local = st.text_input("Local da Ocorrência", placeholder="Endereço completo")
            descricao = st.text_area("Descrição", placeholder="Detalhes da ocorrência...", height=100)
        
        submitted = st.form_submit_button("🚨 REGISTRAR OCORRÊNCIA", use_container_width=True)
        
        if submitted:
            if local and descricao and solicitante:
                nova_ocorrencia = Ocorrencia(
                    st.session_state.pilha.proximo_id,
                    tipo, descricao, local, prioridade, solicitante
                )
                st.session_state.pilha.push(nova_ocorrencia)
                salvar_dados(st.session_state.pilha)
                
                st.success(f"✅ Ocorrência #{nova_ocorrencia.id} registrada com sucesso!")
                st.balloons()
                st.info(f"📍 Posição na pilha: **Topo** (Prioridade: {prioridade})")
            else:
                st.error("⚠️ Preencha todos os campos obrigatórios!")

# ============================================
# 2. PAINEL POLICIAL (Receber e Tratar)
# ============================================
elif menu == "👮 Painel Policial":
    st.header("👮 2. Polícia Receber Ocorrência")
    st.markdown("Visualize o **topo da pilha** (última ocorrência) e assuma o caso.")
    
    # Mostrar o topo da pilha
    topo = st.session_state.pilha.peek()
    
    if topo:
        # Card da ocorrência ativa
        cor_prioridade = {"Baixa": "green", "Média": "blue", "Alta": "orange", "Crítica": "red"}
        cor = cor_prioridade.get(topo.prioridade, "gray")
        
        st.markdown(f"""
        <div class="ocorrencia-card ocorrencia-ativa">
            <h3>🔴 OCORRÊNCIA ATIVA NO TOPO DA PILHA #{topo.id}</h3>
            <p><strong>Tipo:</strong> {topo.tipo} | 
               <strong>Prioridade:</strong> <span style="color:{cor}">● {topo.prioridade}</span></p>
            <p><strong>Local:</strong> {topo.local}</p>
            <p><strong>Descrição:</strong> {topo.descricao}</p>
            <p><strong>Solicitante:</strong> {topo.solicitante} | 
               <strong>Horário:</strong> {topo.data_hora}</p>
            <p><strong>Status:</strong> <span class="status-{topo.status.lower().replace(' ', '-')}">{topo.status}</span></p>
            {f'<p><strong>Policial:</strong> {topo.policial_responsavel}</p>' if topo.policial_responsavel else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # Ações do policial
        st.subheader("🎯 Ações")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not topo.policial_responsavel:
                policial = st.selectbox("Selecione o Policial", st.session_state.policiais)
                if st.button("✋ Assumir Ocorrência", use_container_width=True):
                    topo.policial_responsavel = policial
                    topo.status = "Em Andamento"
                    topo.historico_acoes.append(f"{datetime.now().strftime('%H:%M:%S')} - Assumida por {policial}")
                    salvar_dados(st.session_state.pilha)
                    st.success(f"Ocorrência assumida por {policial}!")
                    st.rerun()
            else:
                st.info(f"Responsável: {topo.policial_responsavel}")
        
        with col2:
            acao = st.text_input("Registrar Ação", placeholder="Ex: Chegada ao local...")
            if st.button("📝 Adicionar Ação", use_container_width=True):
                if acao:
                    topo.historico_acoes.append(f"{datetime.now().strftime('%H:%M:%S')} - {acao}")
                    salvar_dados(st.session_state.pilha)
                    st.success("Ação registrada!")
                    st.rerun()
        
        with col3:
            if st.button("✅ Finalizar Ocorrência", use_container_width=True, type="primary"):
                topo.status = "Resolvida"
                topo.data_resolucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                topo.historico_acoes.append(f"{datetime.now().strftime('%H:%M:%S')} - Ocorrência resolvida")
                
                # Remove do topo da pilha (LIFO)
                st.session_state.pilha.pop()
                # Salvar em histórico separado (opcional)
                salvar_dados(st.session_state.pilha)
                st.success("Ocorrência finalizada e removida da pilha!")
                st.rerun()
        
        # Histórico de ações
        if topo.historico_acoes:
            st.subheader("📜 Histórico de Ações")
            for acao in reversed(topo.historico_acoes):
                st.markdown(f"- {acao}")
    else:
        st.info("📭 Não há ocorrências na pilha. Todas foram resolvidas!")
        st.image("https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif", width=300)

# ============================================
# 3. HISTÓRICO E ESTATÍSTICAS
# ============================================
elif menu == "📊 Histórico e Estatísticas":
    st.header("📊 3. Histórico e Estatísticas")
    
    todas = st.session_state.pilha.listar_todos()
    
    # Estatísticas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total na Pilha", st.session_state.pilha.size())
    col2.metric("Pendentes", sum(1 for o in todas if o.status == "Pendente"))
    col3.metric("Em Andamento", sum(1 for o in todas if o.status == "Em Andamento"))
    col4.metric("Críticas", sum(1 for o in todas if o.prioridade == "Crítica"))
    
    # Visualização da Pilha
    st.subheader("📚 Visualização da Pilha (Topo → Base)")
    
    if not todas:
        st.info("Pilha vazia")
    else:
        for i, ocorrencia in enumerate(todas):
            cor_borda = {"Crítica": "red", "Alta": "orange", "Média": "blue", "Baixa": "green"}
            status_cor = {
                "Pendente": "status-pendente",
                "Em Andamento": "status-andamento", 
                "Resolvida": "status-resolvida"
            }
            
            with st.expander(f"#{ocorrencia.id} - {ocorrencia.tipo} [{ocorrencia.prioridade}] ({ocorrencia.status})"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Local:** {ocorrencia.local}")
                    st.write(f"**Descrição:** {ocorrencia.descricao}")
                    st.write(f"**Solicitante:** {ocorrencia.solicitante}")
                    st.write(f"**Data/Hora:** {ocorrencia.data_hora}")
                    if ocorrencia.policial_responsavel:
                        st.write(f"**Policial:** {ocorrencia.policial_responsavel}")
                with col2:
                    st.write(f"**Posição:** {i+1}º da pilha")
                    if i == 0:
                        st.markdown("🔴 **TOPO**")
                    st.write(f"**Status:** {ocorrencia.status}")
    
    # Gráfico de tipos
    if todas:
        st.subheader("📈 Gráfico por Tipo")
        tipos = {}
        for o in todas:
            tipos[o.tipo] = tipos.get(o.tipo, 0) + 1
        st.bar_chart(tipos)

# ============================================
# 4. CONFIGURAÇÕES
# ============================================
elif menu == "⚙️ Configurações":
    st.header("⚙️ Configurações do Sistema")
    
    with st.expander("👮 Gerenciar Policiais"):
        novo_policial = st.text_input("Adicionar Novo Policial")
        if st.button("Adicionar"):
            if novo_policial:
                st.session_state.policiais.append(novo_policial)
                st.success(f"{novo_policial} adicionado!")
        
        st.write("Policiais cadastrados:")
        for p in st.session_state.policiais:
            col1, col2 = st.columns([4, 1])
            col1.write(f"👮 {p}")
            if col2.button("🗑️", key=f"del_{p}"):
                st.session_state.policiais.remove(p)
                st.rerun()
    
    with st.expander("🗑️ Limpar Dados"):
        st.warning("⚠️ Atenção: Esta ação apaga todas as ocorrências!")
        if st.button("Limpar Todas as Ocorrências", type="secondary"):
            st.session_state.pilha = PilhaOcorrencias()
            if os.path.exists(ARQUIVO_DADOS):
                os.remove(ARQUIVO_DADOS)
            st.success("Dados limpos!")
            st.rerun()

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("**🚔 Sistema Policial v1.0**")
st.sidebar.markdown("Estrutura: Pilha (Stack)")
st.sidebar.markdown(f"Ocorrências ativas: {st.session_state.pilha.size()}")
