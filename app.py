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
if "responsavel_selecionado" not in st.session_state:
    st.session_state.responsavel_selecionado = None

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

# Fluxo sequencial atualizado com dupla validação (Quem + O que)
fluxo_seguranca = [
    {
        "acao": "Instalar a barreira física de pedestais e correntes ao redor do local para delimitar a área de risco",
        "quem_correto": "Supervisor",
        "o_que_correto": "Isolamento",
        "motivo": "O Supervisor deve garantir que a sinalização e o isolamento de área externa estejam montados para proteger terceiros antes de abrir o acesso."
    },
    {
        "acao": "Instalar garras, cadeados e travas nos disjuntores e válvulas de alimentação do espaço confinado",
        "quem_correto": "Supervisor",
        "o_que_correto": "LOTO",
        "motivo": "O bloqueio mecânico (LOTO) e elétrico é uma etapa de engenharia gerenciada e validada pelo Supervisor antes de qualquer liberação."
    },
    {
        "acao": "Fixar as etiquetas de aviso nos pontos de bloqueio para alertar que o equipamento está impedido",
        "quem_correto": "Supervisor",
        "o_que_correto": "Sinalização",
        "motivo": "A sinalização do LOTO formaliza o travamento e deve ser fixada sob a coordenação do Supervisor de Entrada."
    },
    {
        "acao": "Realizar o teste de resposta (bump test) do detector acoplando-o ao cilindro de gás de calibração",
        "quem_correto": "Supervisor",
        "o_que_correto": "Teste Resposta",
        "motivo": "O Supervisor deve testar e certificar que os sensores do detector de gases estão respondendo com rapidez antes do uso."
    },
    {
        "acao": "Ligar o conjunto mecânico para injetar ar limpo ou exaurir os gases estagnados no fundo do espaço confinado",
        "quem_correto": "Supervisor",
        "o_que_correto": "Ventilação",
        "motivo": "O Supervisor determina e monitora o início da ventilação mecânica prévia para purga de gases e contaminantes."
    },
    {
        "acao": "Introduzir a sonda do detector para efetuar a leitura dos gases (O2, LEL, CO, H2S) em múltiplos níveis",
        "quem_correto": "Supervisor",
        "o_que_correto": "Detector",
        "motivo": "A avaliação atmosférica eletrônica inicial é um dever legal exclusivo e obrigatório do Supervisor de Entrada."
    },
    {
        "acao": "Preencher e assinar os requisitos de liberação da Permissão de Entrada e Trabalho (PET)",
        "quem_correto": "Supervisor",
        "o_que_correto": "Sinalização",  # Usando o botão de documento/sinalização para a PET
        "motivo": "A emissão, preenchimento físico e assinatura de autorização da PET competem unicamente ao Supervisor."
    },
    {
        "acao": "Montar a estrutura metálica de ancoragem e o guincho mecânico sobre o acesso do espaço confinado",
        "quem_correto": "Resgate",
        "o_que_correto": "Tripé",
        "motivo": "A equipe de resposta/salvamento monta o tripé preventivamente para garantir a retenção de queda e o sistema de resgate vertical."
    },
    {
        "acao": "Equipar o cinto de segurança e descer pelo acesso para iniciar a realização da atividade prática interna",
        "quem_correto": "Entrante",
        "o_que_correto": "Isolamento",  # Entrada física na zona isolada
        "motivo": "O entrante (trabalhador autorizado) acessa o interior de risco para executar a tarefa industrial."
    },
    {
        "acao": "Monitorar continuamente a atmosfera interna carregando o detector portátil junto a si durante o trabalho",
        "quem_correto": "Entrante",
        "o_que_correto": "Detector",
        "motivo": "O entrante deve portar o detector no interior para captar variações súbitas de gases durante a jornada técnica."
    },
    {
        "acao": "Permanecer do lado de fora em vigilância constante e comunicação contínua com os trabalhadores",
        "quem_correto": "Vigia",
        "o_que_correto": "Sinalização",  # Comunicação/Monitoramento do posto externo
        "motivo": "O Vigia atua unicamente na área externa mantendo o posto de controle visual e rádio com a equipe interna."
    },
    {
        "acao": "Iniciar o resgate emergencial vertical operando os sistemas mecânicos de içamento após um sinistro",
        "quem_correto": "Resgate",
        "o_que_correto": "Tripé",
        "motivo": "O salvamento técnico e a operação do guincho do tripé para extração rápida de vítimas competem à equipe de resgate."
    }
]

# --- TÍTULO PRINCIPAL ---
st.title("🛡️ Simulador Técnico NR-33: Gestão de Riscos e Bloqueios")
st.write("Execute a sequência operacional correta realizando a **Dupla Validação** (Responsável + Equipamento/Ação).")

col_esquerda, col_direita = st.columns([1.1, 1.3], gap="large")

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
        st.session_state.responsavel_selecionado = None

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
        st.markdown("❌ **O erro:** Você falhou na sequência de responsabilidade ou uso do dispositivo técnico.")
        st.markdown(f"📖 **O correto pela NR-33:** Essa tarefa exige a ação do **{passo_falho['quem_correto']}** utilizando o recurso de **{passo_falho['o_que_correto']}**.")
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
        
        # --- SISTEMA DE INSTRUÇÃO DINÂMICA (DUPLA VALIDAÇÃO) ---
        if st.session_state.responsavel_selecionado is None:
            st.markdown("#### 🟥 **PASSO 1:** Clique primeiro no **Responsável** pela tarefa abaixo:")
        else:
            st.markdown(f"#### 🟨 **PASSO 2:** Responsável selecionado: `{st.session_state.responsavel_selecionado}`. Agora clique no **Equipamento, Dispositivo ou Documento** correspondente:")

        # Funções de clique para processar a lógica em dois tempos
        def clicar_quem(quem):
            if quem == passo_atual["quem_correto"]:
                st.session_state.responsavel_selecionado = quem
            else:
                st.session_state.erro_procedimento = True
            st.rerun()

        def clicar_o_que(o_que):
            if st.session_state.responsavel_selecionado is None:
                st.warning("⚠️ Violação de Procedimento! Você deve escolher o profissional responsável antes de acionar o dispositivo.")
            elif o_que == passo_atual["o_que_correto"]:
                st.session_state.historico_acoes.append(f"🟩 Concluído: {passo_atual['acao']} -> Executado por: [{passo_atual['quem_correto']}] com: [{passo_atual['o_que_correto']}]")
                st.session_state.etapa_atual += 1
                st.session_state.responsavel_selecionado = None
            else:
                st.session_state.erro_procedimento = True
            st.rerun()

        # Renderização dos Profissionais
        st.markdown("---")
        st.markdown("#### 👥 Integrantes da Equipe (Quem faz?)")
        c1, c2, c3, c4 = st.columns(4)
        
        # Estilização visual se o profissional já foi selecionado para prender a atenção do aluno
        sup_label = "👉 Supervisor" if st.session_state.responsavel_selecionado == "Supervisor" else "Supervisor"
        ent_label = "👉 Entrante" if st.session_state.responsavel_selecionado == "Entrante" else "Entrante"
        vig_label = "👉 Vigia" if st.session_state.responsavel_selecionado == "Vigia" else "Vigia"
        res_label = "👉 Equipe Resgate" if st.session_state.responsavel_selecionado == "Resgate" else "Equipe Resgate"

        with c1:
            exibir_imagem_repositorio("Supervisor.png", "Supervisor")
            if st.button(sup_label, key="b_sup", use_container_width=True, disabled=(st.session_state.responsavel_selecionado is not None)): 
                clicar_quem("Supervisor")
        with c2:
            exibir_imagem_repositorio("Entrante.png", "Entrante")
            if st.button(ent_label, key="b_ent", use_container_width=True, disabled=(st.session_state.responsavel_selecionado is not None)): 
                clicar_quem("Entrante")
        with c3:
            exibir_imagem_repositorio("Vigia.png", "Vigia")
            if st.button(vig_label, key="b_vig", use_container_width=True, disabled=(st.session_state.responsavel_selecionado is not None)): 
                clicar_quem("Vigia")
        with c4:
            exibir_imagem_repositorio("Resgate1.png", "Resgate")
            if st.button(res_label, key="b_res", use_container_width=True, disabled=(st.session_state.responsavel_selecionado is not None)): 
                clicar_quem("Resgate")

        # Renderização dos Equipamentos e Dispositivos
        st.markdown("---")
        st.markdown("#### 🔒 Isolamento e Bloqueio (LOTO)")
        l1, l2, l3, l4 = st.columns(4)
        with l1:
            exibir_imagem_repositorio("Isolamento.png", "Isolamento")
            if st.button("Isolamento Área", key="b_iso", use_container_width=True): clicar_o_que("Isolamento")
        with l2:
            exibir_imagem_repositorio("Cadeado.png", "LOTO")
            if st.button("Bloqueios / LOTO", key="b_loto", use_container_width=True): clicar_o_que("LOTO")
        with l3:
            exibir_imagem_repositorio("Sinalizacao.NaoOpere.png", "Sinalizacao")
            if st.button("Sinalizacao LOTO / PET", key="b_sin", use_container_width=True): clicar_o_que("Sinalizacao")
        with l4:
            exibir_imagem_repositorio("Cilindro_Teste_Resposta.png", "Teste Resposta")
            if st.button("Bump Test", key="b_bt", use_container_width=True): clicar_o_que("Teste Resposta")

        st.markdown("#### ⚙️ Sistemas Atmosféricos e Coletivos")
        e1, e2, e3 = st.columns(3)
        with e1:
            exibir_imagem_repositorio("Ventilacao_Exaustao.png", "Ventilacao")
            if st.button("Ventilacao/Purga", key="b_vent", use_container_width=True): clicar_o_que("Ventilacao")
        with e2:
            exibir_imagem_repositorio("DetectorGas.png", "Detector")
            if st.button("Medicao Gases", key="b_det", use_container_width=True): clicar_o_que("Detector")
        with e3:
            exibir_imagem_repositorio("Tripe.png", "Tripe")
            if st.button("Tripe / Resgate", key="b_tri", use_container_width=True): clicar_o_que("Tripé")

    if st.session_state.historico_acoes:
        st.markdown("---")
        st.write("📋 **Histórico de Passos Concluídos com Sucesso:**")
        for item in st.session_state.historico_acoes:
            st.write(item)
