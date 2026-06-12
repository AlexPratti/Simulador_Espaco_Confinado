import streamlit as st
import os

# Configuração da página para aproveitar o espaço horizontal
st.set_page_config(page_title="Simulador NR-33 Avançado", page_icon="🛡️", layout="wide")

# --- CONTROLE DE ESTADOS ---
if "etapa_atual" not in st.session_state:
    st.session_state.etapa_atual = 0
if "erro_procedimento" not in st.session_state:
    st.session_state.erro_procedimento = False
if "servico_selecionado" not in st.session_state:
    st.session_state.servico_selecionado = None
if "historico_acoes" not in st.session_state:
    st.session_state.historico_acoes = []

# Função para carregar imagem direto da raiz do repositório
def exibir_imagem_repositorio(nome_arquivo, fallback_texto):
    if os.path.exists(nome_arquivo):
        st.image(nome_arquivo, use_container_width=True)
    else:
        st.code(f"⚠️ [Arquivo {nome_arquivo} não encontrado no repositório]")

# Relação de 10 serviços para seleção do usuário
servicos_disponiveis = [
    "Limpeza Química de Tanque de Combustível",
    "Manutenção de Válvulas em Galeria Subterrânea",
    "Inspeção Estrutural em Silo de Grãos",
    "Reparo de Tubulação de Esgoto Ativo",
    "Soldagem Interna em Caldeira Desativada",
    "Troca de Filtros em Reator Químico",
    "Revestimento Anticorrosivo em Cisterna de Água",
    "Passagem de Cabos em Poço de Visita (PV)",
    "Remoção de Resíduos em Caixa de Decantação",
    "Manutenção Mecânica em Misturador Industrial"
]

# Fluxo sequencial detalhado unindo seus profissionais e equipamentos
fluxo_seguranca = [
    {
        "acao": "Instalar a barreira física de pedestais e correntes ao redor do local para delimitar a área de risco",
        "correto": "Isolamento",
        "motivo": "O isolamento de área protege terceiros e evita queda de objetos na boca de visita antes de abri-la."
    },
    {
        "acao": "Instalar garras, cadeados e travas nos disjuntores e válvulas de alimentação do espaço confinado",
        "correto": "LOTO",
        "motivo": "O bloqueio mecânico (LOTO) e elétrico elimina o risco de liberação acidental de fluidos ou energias perigosas."
    },
    {
        "acao": "Fixar as etiquetas de aviso nos pontos de bloqueio para alertar que o equipamento está impedido",
        "correto": "Sinalização",
        "motivo": "A sinalização é obrigatória por norma para informar a todos os setores que o sistema está travado para manutenção."
    },
    {
        "acao": "Realizar o teste de resposta (bump test) do detector acoplando-o ao cilindro de gás de calibração",
        "correto": "Teste Resposta",
        "motivo": "O teste de resposta garante que os sensores do detector de gases estão reagindo de forma rápida e precisa antes do uso."
    },
    {
        "acao": "Acionar o Supervisor de Entrada para que ele valide os testes de calibração e os bloqueios físicos",
        "correto": "Supervisor",
        "motivo": "É competência legal do Supervisor auditar todas as proteções coletivas e individuais pré-entrada."
    },
    {
        "acao": "Ligar o conjunto mecânico para injetar ar limpo ou exaurir os gases estagnados no fundo do tanque",
        "correto": "Ventilação",
        "motivo": "A ventilação ou exaustão prévia dispersa possíveis contaminantes tóxicos presentes no interior."
    },
    {
        "acao": "Introduzir a sonda do detector para efetuara leitura dos gases (O2, LEL, CO, H2S) em múltiplos níveis",
        "correto": "Detector",
        "motivo": "A atmosfera deve ser avaliada eletronicamente antes de liberar qualquer trabalhador para entrar."
    },
    {
        "acao": "Preencher e assinar a Permissão de Entrada e Trabalho (PET) autorizando o início da tarefa técnica",
        "correto": "Supervisor",
        "motivo": "A emissão formal e encerramento da PET são responsabilidades exclusivas e indelegáveis do Supervisor."
    },
    {
        "acao": "Montar a estrutura metálica de ancoragem e o guincho mecânico sobre o acesso do espaço confinado",
        "correto": "Tripé",
        "motivo": "O tripé com linha de vida garante que o resgate vertical e a retenção de queda estejam prontos preventivamente."
    },
    {
        "acao": "Equipar o cinto e descer com segurança pelo acesso para iniciar a realização da atividade prática",
        "correto": "Entrante",
        "motivo": "O entrante é o profissional capacitado que entra no espaço de risco para executar a atividade industrial."
    },
    {
        "acao": "Permanecer do lado de fora monitorando as condições e mantendo comunicação contínua com quem está dentro",
        "correto": "Vigia",
        "motivo": "O Vigia atua unicamente na área externa vigiando os entrantes e monitorando o entorno."
    },
    {
        "acao": "Iniciar o resgate emergencial vertical operando os sistemas de içamento devido a um incidente na parte interna",
        "correto": "Resgate",
        "motivo": "O salvamento técnico e a retirada rápida de vítimas competem à equipe treinada de resgate."
    }
]

# --- TÍTULO PRINCIPAL ---
st.title("🛡️ Simulador Técnico NR-33: Gestão de Riscos e Bloqueios")
st.write("Execute a sequência operacional correta clicando nos componentes operacionais corretos.")

col_esquerda, col_direita = st.columns([1.1, 1.3], gap="large")

# --- COLUNA ESQUERDA: ANÁLISE VISUAL DO CENÁRIO ---
with col_esquerda:
    st.header("📸 Análise do Espaço Confinado")
    
    tab_frente, tab_topo = st.tabs(["👁️ Visão de Frente", "👁️ Visão de Topo"])
    with tab_frente:
        exibir_imagem_repositorio("Esp.Confinado.Frente.png", "Esp.Confinado.Frente.png")
    with tab_topo:
        exibir_imagem_repositorio("Esp.Confinado.Topo.png", "Esp.Confinado.Topo.png")

    st.markdown("---")
    st.header("🛠️ Ordem de Serviço")
    
    def resetar_jogo():
        st.session_state.etapa_atual = 0
        st.session_state.erro_procedimento = False
        st.session_state.historico_acoes = []

    servico = st.selectbox(
        "Selecione o serviço a ser realizado:", 
        servicos_disponiveis, 
        index=None, 
        placeholder="Escolha uma atividade...",
        on_change=resetar_jogo
    )
    st.session_state.servico_selecionado = servico
    # --- COLUNA DIREITA: MECÂNICA DO SIMULADOR ---
with col_direita:
    st.header("🕹️ Painel de Decisões Técnicas")
    
    if not st.session_state.servico_selecionado:
        st.info("Aguardando seleção do tipo de serviço na coluna ao lado para iniciar as etapas.")
        
    elif st.session_state.erro_procedimento:
        st.error("🚨 ATIVIDADE INTERROMPIDA POR ERRO DE PROCEDIMENTO!")
        passo_falho = fluxo_seguranca[st.session_state.etapa_atual]
        st.markdown(f"**Falha Crítica na Ação:** *{passo_falho['acao']}*")
        st.markdown(f"❌ **O erro:** Você acionou o elemento ou profissional incorreto para este momento.")
        st.markdown(f"📖 **O correto pela NR-33:** O alvo correto deveria ser: **{passo_falho['correto']}**.")
        st.info(f"💡 *Justificativa:* {passo_falho['motivo']}")
        
        if st.button("Reiniciar Atividade Operacional 🔄", type="primary", use_container_width=True):
            resetar_jogo()
            st.rerun()
            
    elif st.session_state.etapa_atual >= len(fluxo_seguranca):
        st.balloons()
        st.success(f"🎉 **Serviço de '{st.session_state.servico_selecionado}' concluído com 100% de conformidade legal!**")
        if st.button("Simular Novo Serviço 🔄", use_container_width=True):
            resetar_jogo()
            st.rerun()
            
    else:
        passo_atual = fluxo_seguranca[st.session_state.etapa_atual]
        st.write(f"**Serviço Industrial Ativo:** `{st.session_state.servico_selecionado}`")
        st.progress(st.session_state.etapa_atual / len(fluxo_seguranca))
        
        st.markdown("### 🎯 Próxima Ação Obrigatória:")
        st.warning(f"👉 **{passo_atual['acao']}**")
        st.write("Clique na imagem ou no botão do responsável por agir nesta etapa:")
        
        def avaliar_escolha(escolha_usuario):
            if escolha_usuario == passo_atual["correto"]:
                st.session_state.historico_acoes.append(f"🟩 Concluído: {passo_atual['acao']} ({passo_atual['correto']})")
                st.session_state.etapa_atual += 1
            else:
                st.session_state.erro_procedimento = True
            st.rerun()

        st.markdown("#### 👥 Integrantes da Equipe")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            exibir_imagem_repositorio("Supervisor.png", "Supervisor")
            if st.button("Supervisor", key="b_sup", use_container_width=True): avaliar_escolha("Supervisor")
        with c2:
            exibir_imagem_repositorio("Entrante.png", "Entrante")
            if st.button("Entrante", key="b_ent", use_container_width=True): avaliar_escolha("Entrante")
        with c3:
            exibir_imagem_repositorio("Vigia.png", "Vigia")
            if st.button("Vigia", key="b_vig", use_container_width=True): avaliar_escolha("Vigia")
        with c4:
            exibir_imagem_repositorio("Resgate1.png", "Resgate")
            if st.button("Equipe Resgate", key="b_res", use_container_width=True): avaliar_escolha("Resgate")

        st.markdown("#### 🔒 Isolamento e Bloqueio (LOTO)")
        l1, l2, l3, l4 = st.columns(4)
        with l1:
            exibir_imagem_repositorio("Isolamento.png", "Isolamento")
            if st.button("Isolamento Area", key="b_iso", use_container_width=True): avaliar_escolha("Isolamento")
        with l2:
            exibir_imagem_repositorio("Cadeado.png", "LOTO")
            if st.button("Bloqueios / LOTO", key="b_loto", use_container_width=True): avaliar_escolha("LOTO")
        with l3:
            exibir_imagem_repositorio("Sinalizacao.NaoOpere.png", "Sinalizacao")
            if st.button("Sinalizacao LOTO", key="b_sin", use_container_width=True): avaliar_escolha("Sinalização")
        with l4:
            exibir_imagem_repositorio("Cilindro_Teste_Resposta.png", "Teste Resposta")
            if st.button("Bump Test", key="b_bt", use_container_width=True): avaliar_escolha("Teste Resposta")

        st.markdown("#### ⚙️ Sistemas Atmosféricos e Coletivos")
        e1, e2, e3 = st.columns(3)
        with e1:
            exibir_imagem_repositorio("Ventilacao_Exaustao.png", "Ventilacao")
            if st.button("Ventilacao/Purga", key="b_vent", use_container_width=True): avaliar_escolha("Ventilação")
        with e2:
            exibir_imagem_repositorio("DetectorGas.png", "Detector")
            if st.button("Medicao Gases", key="b_det", use_container_width=True): avaliar_escolha("Detector")
        with e3:
            exibir_imagem_repositorio("Tripe.png", "Tripe")
            if st.button("Tripe / Resgate", key="b_tri", use_container_width=True): avaliar_escolha("Tripé")

    if st.session_state.historico_acoes:
        st.markdown("---")
        st.write("📋 **Histórico de Passos Concluídos com Sucesso:**")
        for item in st.session_state.historico_acoes:
            st.write(item)
