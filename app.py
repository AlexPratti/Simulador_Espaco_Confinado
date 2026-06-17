import streamlit as st
import os

# Configuração da página para aproveitar o espaço horizontal
st.set_page_config(page_title="Portal de Simuladores SST", page_icon="🛡️", layout="wide")

# --- NAVEGAÇÃO PRINCIPAL EM ABAS HORIZONTAIS ---
st.markdown("## 🧭 Escolha o Módulo de Treinamento")
modulo = st.radio(
    "Selecione a área operacional para simular os procedimentos:", 
    ["Aba Inicial", "NR-33 (Espaço Confinado)", "NR-35 (Trabalho em Altura)"],
    horizontal=True
)

# --- CONTROLE GLOBAL DE ESTADOS (SESSION STATE) ---
if "etapa_atual" not in st.session_state:
    st.session_state.etapa_atual = 0
if "erro_procedimento" not in st.session_state:
    st.session_state.erro_procedimento = False
if "total_erros" not in st.session_state:
    st.session_state.total_erros = 0
if "servico_selecionado" not in st.session_state:
    st.session_state.servico_selecionado = None
if "acidente_selecionado" not in st.session_state:
    st.session_state.acidente_selecionado = None
if "historico_acoes" not in st.session_state:
    st.session_state.historico_acoes = []
if "responsavel_selecionado" not in st.session_state:
    st.session_state.responsavel_selecionado = None
if "bloqueio_calculo_altura" not in st.session_state:
    st.session_state.bloqueio_calculo_altura = False

# Função unificada de reinício da simulação
def resetar_jogo():
    st.session_state.etapa_atual = 0
    st.session_state.erro_procedimento = False
    st.session_state.total_erros = 0
    st.session_state.historico_acoes = []
    st.session_state.responsavel_selecionado = None
    st.session_state.bloqueio_calculo_altura = False
# Função automatizada com Fallback Visual para Caixas de Imagens Faltantes
def exibir_imagem_repositorio(nome_arquivo, fallback_texto):
    if os.path.exists(nome_arquivo):
        st.image(nome_arquivo, use_container_width=True)
    else:
        st.markdown(
            f"""
            <div style="background-color: #262730; border: 2px dashed #4b4d5a; 
            border-radius: 8px; padding: 20px; text-align: center; color: #a1a1a1; 
            font-weight: bold; margin-bottom: 10px;">
                📷 [Falta subir no GitHub: {nome_arquivo}]<br>
                <span style="font-size: 12px; font-weight: normal;">{fallback_texto}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

# --- LISTAGENS GERAIS DE ORDENS DE SERVIÇO ---
servicos_nr33 = [
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

servicos_nr35 = [
    "Montagem de Fachada [2 Trabalhadores no topo | Sem Vigia exclusivo]",
    "Reparo de Telhado [3 Trabalhadores no topo | Sem Vigia exclusivo]",
    "Troca de Lâmpadas em Poste [1 Trabalhador no topo | Exige 1 Vigia em solo por tráfego de veículos]",
    "Pintura Externa de Silo Elevado [2 Trabalhadores no topo | Exige 1 Vigia em solo por área pública externa]"
]

acidentes_disponiveis = [
    "Mal Súbito por Asfixia (Falta de Oxigênio)",
    "Intoxicação por Gases com Perda de Consciência",
    "Queda de Altura com Fratura Exposta no Fêmur",
    "Prensamento de Membro com Hemorragia Grave",
    "Queimadura Química por Contato Respiratório",
    "Choque Elétrico por Equipamento Não Aterrado"
]

# Mapeamento estrito de arquivos PNG para os cenários
MAPEAMENTO_CENARIOS_33 = {
    "Limpeza Química de Tanque de Combustível": "Tanque_Combustivel.png",
    "Manutenção de Válvulas em Galeria Subterrânea": "Galeria_Subterr.png",
    "Inspeção Estrutural em Silo de Grãos": "Silo_Graos.png",
    "Reparo de Tubulação de Esgoto Ativo": "Tubulacao_Esgoto.png",
    "Soldagem Interna em Caldeira Desativada": "Caldeira.png",
    "Troca de Filtros em Reator Químico": "Reator.png",
    "Revestimento Anticorrosivo em Cisterna de Água": "Cisterna.png",
    "Passagem de Cabos em Poço de Visita (PV)": "Poco_Visita.png",
    "Remoção de Resíduos em Caixa de Decantação": "Caixa_Decant.png",
    "Manutenção Mecânica em Misturador Industrial": "Misturador.png"
}

MAPEAMENTO_CENARIOS_35 = {
    "Montagem de Fachada [2 Trabalhadores no topo | Sem Vigia exclusivo]": "Altura_Andaimes.png",
    "Reparo de Telhado [3 Trabalhadores no topo | Sem Vigia exclusivo]": "Altura_Telhado.png",
    "Troca de Lâmpadas em Poste [1 Trabalhador no topo | Exige 1 Vigia em solo por tráfego de veículos]": "Altura_Poste.png",
    "Pintura Externa de Silo Elevado [2 Trabalhadores no topo | Exige 1 Vigia em solo por área pública externa]": "Altura_Poste.png"
}
# --- GERADORES DINÂMICOS DOS FLUXOS DE ATIVIDADE ---
def obter_fluxo_nr33():
    acidente = st.session_state.acidente_selecionado or "Incidente"
    
    if "Asfixia" in acidente or "Gases" in acidente or "Respiratório" in acidente:
        item_medico_requerido = "Respirador"
    elif "Fratura" in acidente or "Hemorragia" in acidente:
        item_medico_requerido = "Talas"
    else:
        item_medico_requerido = "MacaSked"

    return [
        {"acao": "Instalar a barreira física de pedestais e correntes para delimitar a área de risco", "quem_correto": "Supervisor", "o_que_correto": "Isolamento", "motivo": "O Supervisor deve garantir o isolamento externo antes de abrir o acesso."},
        {"acao": "Instalar garras, cadeados e travas nos disjuntores e válvulas de alimentação", "quem_correto": "Supervisor", "o_que_correto": "LOTO", "motivo": "O bloqueio mecânico (LOTO) e elétrico é gerenciado e inspecionado pelo Supervisor."},
        {"acao": "Fixar as etiquetas de aviso nos pontos de bloqueio para alertar o impedimento", "quem_correto": "Supervisor", "o_que_correto": "Sinalizacao", "motivo": "A sinalização do LOTO formaliza o travamento sob coordenação do Supervisor."},
        {"acao": "Realizar o teste de resposta (bump test) do detector acoplando-o ao cilindro de gás", "quem_correto": "Supervisor", "o_que_correto": "Teste Resposta", "motivo": "O Supervisor deve certificar o detector de gases antes do uso em campo."},
        {"acao": "Ligar o conjunto mecânico para injetar ar limpo ou exaurir os gases estagnados no fundo", "quem_correto": "Supervisor", "o_que_correto": "Ventilacao", "motivo": "O Supervisor determina e monitora o início da ventilação mecânica prévia."},
        {"acao": "Introduzir a sonda do detector para efetuar a leitura dos gases em múltiplos níveis", "quem_correto": "Supervisor", "o_que_correto": "Detector", "motivo": "A avaliação atmosférica eletrônica inicial é um dever legal obrigatório do Supervisor."},
        {"acao": "Preencher e assinar os requisitos de liberação da Permissão de Entrada e Trabalho (PET)", "quem_correto": "Supervisor", "o_que_correto": "PET", "motivo": "A liberação formal por escrito por meio da PET compete unicamente ao Supervisor."},
        {"acao": "Montar e preparar a estrutura de ancoragem e o sistema de vantagem mecânica sobre o acesso", "quem_correto": "Vigia", "o_que_correto": "Tripe", "motivo": "Na fase preparatória preventiva, cabe ao Vigia estruturar os sistemas de movimentação externos."},
        {"acao": "Equipar o cinto de segurança e descer pelo acesso para iniciar a atividade prática interna", "quem_correto": "Entrante", "o_que_correto": "EPI", "motivo": "O entrante acessa o interior portando o cinto conectado com segurança à linha de vida."},
        {"acao": "Monitorar continuamente a atmosfera interna carregando o detector portátil junto a si", "quem_correto": "Entrante", "o_que_correto": "Detector", "motivo": "O entrante deve portar o detector no interior para captar variações súbitas de gases."},
        {"acao": "Permanecer do lado de fora em vigilância constante externa e comunicação contínua", "quem_correto": "Vigia", "o_que_correto": "LadoFora", "motivo": "O Vigia atua mantendo obrigatoriamente o seu posto de controle fixo do lado de fora da área de risco."},
        {"acao": f"ATENÇÃO! OCORREU UM SINISTRO INTERNO: [{acidente}]. Mobilize a equipe e acione o recurso médico/salvamento correto para o resgate do entrante", "quem_correto": "Resgate", "o_que_correto": item_medico_requerido, "motivo": "Na emergência, a Equipe de Resgate assume o salvamento portando o EPI respiratório ou de primeiros socorros adequado."}
    ]

def obter_fluxo_nr35():
    acidente = st.session_state.acidente_selecionado or "Incidente"
    servico = st.session_state.servico_selecionado or ""
    
    precisa_vigia = "Exige" in servico
    monitor_externo = "Vigia" if precisa_vigia else "Entrante"
    texto_monitor = "Vigia em solo" if precisa_vigia else "Trabalhador parceiro de equipe no topo"

    if "Asfixia" in acidente or "Gases" in acidente or "Respiratório" in acidente:
        item_medico_requerido = "Respirador"
    elif "Fratura" in acidente or "Hemorragia" in acidente:
        item_medico_requerido = "Talas"
    else:
        item_medico_requerido = "MacaSked"

    return [
        {"acao": "Elaborar e validar a Análise Preliminar de Risco (APR) listando os perigos da atividade em altura", "quem_correto": "Supervisor", "o_que_correto": "APR", "motivo": "O Supervisor deve garantir que a análise de risco e os recursos de segurança estejam corretos antes da subida."},
        {"acao": "Isolar fisicamente a área de solo correspondente à projeção de queda de materiais", "quem_correto": "Supervisor", "o_que_correto": "Isolamento", "motivo": "Cabe ao Supervisor assegurar o isolamento de periferia na base da estrutura."},
        {"acao": "Emitir formalmente a assinatura de liberação da Permissão de Trabalho (PT) em altura", "quem_correto": "Supervisor", "o_que_correto": "PET", "motivo": "A auditoria técnica final e assinatura de liberação da PT competem ao Supervisor."},
        {"acao": "Ajustar os cintos de segurança paraquedistas de todos os envolvidos e checar as fivelas", "quem_correto": "Entrante", "o_que_correto": "EPI", "motivo": "Os executantes devem realizar a inspection e ajuste do próprio cinto em dupla antes de iniciar."},
        {"acao": "Conectar o gancho do Talabarte duplo em Y ou o dispositivo Trava-quedas na linha de vida estrutural", "quem_correto": "Entrante", "o_que_correto": "Talabarte_Y" if "Arnês" in acidente else "TravaQuedas", "motivo": "O trabalhador deve se ancorar fixamente à linha de vida antes de iniciar os trabalhos técnicos."},
        {"acao": "Iniciar a subida e executar a atividade técnica no topo da estrutura conforme o quantitativo da OS", "quem_correto": "Entrante", "o_que_correto": "Ventilacao", "motivo": "Após a liberação e ancoragem, a equipe técnica inicia a execução dos serviços em altura."},
        {"acao": "Garantir o monitoramento constante das condições de risco e manter a prontidão do rádio HT. (Quem monitora nesta OS?)", "quem_correto": monitor_externo, "o_que_correto": "Comunicacao", "motivo": f"Conforme definido na APR para esta atividade específica, o monitoramento é feito pelo [{texto_monitor}]."},
        {"acao": f"ALERTA! OCORREU UMA QUEDA COM SUSPENSÃO: [{acidente}]. Lance imediatamente o recurso de alívio circulatório contra a Síndrome do Arnês", "quem_correto": monitor_externo, "o_que_correto": "Fita_AntiTrauma", "motivo": "O encarregado do monitoramento deve agir rápido para prover a fita de suspensão e evitar o choque circulatório."},
        {"acao": "Mobilizar a brigada, acessar o trabalhador suspenso por cordas e operar o sistema mecânico de descida vertical", "quem_correto": "Resgate", "o_que_correto": "Tripe", "motivo": "Em caso de sinistro na altura, a Equipe de Resgate assume a operação técnica de polias e descida tática da vítima."},
        {"acao": "Estabilizar a cervical e realizar a imobilização completa do acidentado no solo antes do transporte técnico", "quem_correto": "Resgate", "o_que_correto": "MacaRigida" if "Coluna" in acidente else item_medico_requerido, "motivo": "O time de resgate presta os primeiros socorros imobilizando o trauma no solo conforme o diagnóstico do acidente."}
    ]
# --- CONSTRUÇÃO DO LAYOUT EM DUAS COLUNAS ---
col_esquerda, col_direita = st.columns([1.1, 1.3], gap="large")

with col_esquerda:
    st.header("📸 Análise de Cenário")
    
    # 1. Fluxo Visual Exclusivo se a Aba selecionada for NR-33
    if modulo == "NR-33 (Espaço Confinado)":
        if st.session_state.servico_selecionado in MAPEAMENTO_CENARIOS_33:
            st.markdown(f"### 📍 Cenário: {st.session_state.servico_selecionado}")
            exibir_imagem_repositorio(MAPEAMENTO_CENARIOS_33[st.session_state.servico_selecionado], st.session_state.servico_selecionado)
        else:
            st.markdown("### 📍 Cenário Operacional (Espaço Confinado)")
            tab_f1, tab_t1 = st.tabs(["👁️ Frente", "👁️ Topo"])
            with tab_f1: exibir_imagem_repositorio("Esp.Confinado.Frente.png", "Esp.Confinado.Frente.png")
            with tab_t1: exibir_imagem_repositorio("Esp.Confinado.Topo.png", "Esp.Confinado.Topo.png")
            
        st.markdown("---")
        st.header("🛠️ Configuração da Ordem de Serviço")
        st.selectbox("1. Escolha a atividade industrial:", servicos_nr33, index=None, placeholder="Selecione...", on_change=resetar_jogo, key="sel_s_33")
        st.session_state.servico_selecionado = st.session_state.sel_s_33
        st.selectbox("2. Escolha o sinistro potencial:", acidentes_disponiveis, index=None, placeholder="Selecione...", on_change=resetar_jogo, key="sel_a_33")
        st.session_state.acidente_selecionado = st.session_state.sel_a_33

    # 2. Fluxo Visual Exclusivo se a Aba selecionada for NR-35
    if modulo == "NR-35 (Trabalho em Altura)":
        st.selectbox("1. Escolha a atividade industrial em altura:", servicos_nr35, index=None, placeholder="Selecione...", on_change=resetar_jogo, key="sel_s_35")
        st.session_state.servico_selecionado = st.session_state.sel_s_35
        st.selectbox("2. Escolha o risco à saúde associado:", acidentes_disponiveis, index=None, placeholder="Selecione...", on_change=resetar_jogo, key="sel_a_35")
        st.session_state.acidente_selecionado = st.session_state.sel_a_35
        if st.session_state.servico_selecionado:
            if st.session_state.servico_selecionado in MAPEAMENTO_CENARIOS_35:
                st.markdown(f"### 📍 Cenário: {st.session_state.servico_selecionado}")
                exibir_imagem_repositorio(MAPEAMENTO_CENARIOS_35[st.session_state.servico_selecionado], st.session_state.servico_selecionado)
            else:
                st.markdown("### 📍 Cenário Operacional (Trabalho em Altura)")
                exibir_imagem_repositorio("Altura_Andaimes.png", "Cenário de Altura Padrão")
            
            st.markdown("### 📐 Painel de Engenharia de Queda (NR-35)")
            h_cenario = st.number_input("Altura total do cenário (metros):", min_value=1.0, max_value=50.0, value=4.0, step=0.5)
            dist_topo_anc = st.number_input("Distância do topo do cenário até o ponto de ancoragem (metros):", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
            zlq_talabarte = st.number_input("Zona Livre de Queda (ZLQ) requerida pelo Talabarte Y (metros):", min_value=1.0, max_value=15.0, value=5.0, step=0.1)
            
            fq_analise = ""
            if "Telhado" in st.session_state.servico_selecionado:
                fq_analise = "FQ = 2 (Crítico - Ancoragem nos pés/topo do telhado)"
            elif "Fachada" in st.session_state.servico_selecionado or "Calhas" in st.session_state.servico_selecionado:
                fq_analise = "FQ = 1 (Médio - Ancoragem na linha do peito/ombro)"
            elif "Poste" in st.session_state.servico_selecionado or "Silo" in st.session_state.servico_selecionado:
                fq_analise = "FQ < 1 (Ideal - Ancoragem acima da cabeça do trabalhador)"
                
            st.info(f"📋 **Fator de Queda Estimado pela APR:** {fq_analise}")
            zlq_local = h_cenario + dist_topo_anc
            st.markdown(f"#### 📐 ZLQ Calculada do Local: **{zlq_local:.2f} m**")
            st.markdown(f"#### 🏷️ ZLQ Fornecida do Equipamento: **{zlq_talabarte:.2f} m**")
            
            if zlq_local >= zlq_talabarte:
                st.success("🟢 **ATIVIDADE LIBERADA:** A distância até o chão é suficiente para o talabarte reter a queda sem colisão física!")
                st.session_state.bloqueio_calculo_altura = False
            else:
                st.error("🔴 **ATIVIDADE SUSPENSA CRITICAMENTE:** Em caso de queda, o trabalhador colidirá contra o chão! Aumente a ancoragem ou reduza o tamanho do talabarte.")
                st.session_state.bloqueio_calculo_altura = True

# --- COLUNA DIREITA: MECÂNICA DO SIMULADOR INTEGRADO ---
with col_direita:
    st.header("🕹️ Painel de Decisões Técnicas")
    
    if modulo == "Aba Inicial":
        st.info("👋 Bem-vindo ao Portal Corretivo! Selecione a aba da NR-33 ou NR-35 acima para carregar o simulador prático.")
    
    elif not st.session_state.servico_selecionado or not st.session_state.acidente_selecionado:
        st.info("Configure os parâmetros da Ordem de Serviço à esquerda para liberar o painel da norma.")
    
    elif modulo == "NR-35 (Trabalho em Altura)" and st.session_state.get("bloqueio_calculo_altura", False):
        st.warning("⚠️ **PAINEL BLOQUEADO:** Corrija os parâmetros de Engenharia de Queda na coluna da esquerda. A atividade está suspensa devido ao risco de impacto contra o chão.")
        
    elif st.session_state.erro_procedimento:
        exibir_imagem_repositorio("Alerta_Seguranca.png", "Alerta SST")
        st.error("🚨 ALERTA DE SEGURANÇA: PROCEDIMENTO INCORRETO DETECTADO!")
        fluxo_ativo = obter_fluxo_nr33() if modulo == "NR-33 (Espaço Confinado)" else obter_fluxo_nr35()
        st.markdown(f"**Ação violada:** *{fluxo_ativo[st.session_state.etapa_atual]['acao']}*")
        
        c_e1, c_e2 = st.columns(2)
        with c_e1:
            if st.button("Corrigir Erro (Tentar Novamente)", use_container_width=True, type="primary"):
                st.session_state.erro_procedimento = False
                st.session_state.responsavel_selecionado = None
                st.rerun()
        with c_e2:
            if st.button("Cancelar Procedimento (Reiniciar)", use_container_width=True):
                resetar_jogo()
                st.rerun()
        else:
            fluxo_seguranca = obter_fluxo_nr33() if modulo == "NR-33 (Espaço Confinado)" else obter_fluxo_nr35()
            st.metric(label="⚠️ Desvios / Erros Cometidos na Missão", value=st.session_state.total_erros)
            
            if st.session_state.etapa_atual >= len(fluxo_seguranca):
                st.balloons()
                st.success(f"🎉 **Missão concluída com sucesso no módulo {modulo}!**")
                st.info(f"📊 **Resultado Operacional:** Treinamento finalizado com **{st.session_state.total_erros} desvios** acumulados.")
                if st.button("Iniciar Nova Simulação 🔄", use_container_width=True):
                    resetar_jogo()
                    st.rerun()
            else:
                passo_atual = fluxo_seguranca[st.session_state.etapa_atual]
                st.write(f"**OS Ativa:** `{st.session_state.servico_selecionado}`")
                st.progress(st.session_state.etapa_atual / len(fluxo_seguranca))
                st.warning(f"👉 **{passo_atual['acao']}**")
                
                if st.session_state.responsavel_selecionado is None:
                    st.markdown("#### 🟥 **PASSO 1:** Clique primeiro no **Responsável** pela tarefa:")
                else:
                    st.markdown(f"#### 🟨 **PASSO 2:** Responsável: **[{st.session_state.responsavel_selecionado}]**. Clique na **Imagem/Equipamento**:")

                def avaliar_dupla(tipo, valor):
                    if tipo == "quem":
                        if valor == passo_atual["quem_correto"]: st.session_state.responsavel_selecionado = valor
                        else:
                            st.session_state.total_erros += 1
                            st.session_state.erro_procedimento = True
                    elif tipo == "o_que":
                        if st.session_state.responsavel_selecionado is None: return
                        if valor == passo_atual["o_que_correto"]:
                            st.session_state.historico_acoes.append(f"🟩 Concluído: {passo_atual['acao']} -> [{passo_atual['quem_correto']}] + [{passo_atual['o_que_correto']}]")
                            st.session_state.etapa_atual += 1
                            st.session_state.responsavel_selecionado = None
                        else:
                            st.session_state.total_erros += 1
                            st.session_state.erro_procedimento = True
                    st.rerun()

                # Renderização Dinâmica das Equipes
                st.markdown("#### 👥 1. Integrantes da Equipe (Quem faz?)")
                ocultar_vigia = (modulo == "NR-35 (Trabalho em Altura)") and ("Sem Vigia" in st.session_state.servico_selecionado)
                colunas_equipe = st.columns(3 if ocultar_vigia else 4)
                
                with colunas_equipe:
                    exibir_imagem_repositorio("Supervisor.png", "Supervisor")
                    if st.button("Selecionar Supervisor", key="k_sup", use_container_width=True): avaliar_dupla("quem", "Supervisor")
                with colunas_equipe:
                    exibir_imagem_repositorio("Entrante.png", "Trabalhador")
                    if st.button("Selecionar Trabalhador", key="k_ent", use_container_width=True): avaliar_dupla("quem", "Entrante")
                    
                if not ocultar_vigia:
                    with colunas_equipe:
                        exibir_imagem_repositorio("Vigia.png", "Vigia Externo")
                        if st.button("Selecionar Vigia", key="k_vig", use_container_width=True): avaliar_dupla("quem", "Vigia")
                    with colunas_equipe:
                        exibir_imagem_repositorio("Resgate1.png", "Equipe Resgate")
                        if st.button("Selecionar Resgate", key="k_res", use_container_width=True): avaliar_dupla("quem", "Resgate")
                else:
                    with colunas_equipe:
                        exibir_imagem_repositorio("Resgate1.png", "Equipe Resgate")
                        if st.button("Selecionar Resgate", key="k_res", use_container_width=True): avaliar_dupla("quem", "Resgate")

                # Dispositivos Comuns e Técnicos
                st.markdown("#### 🔒 2. Isolamento, Bloqueio e Gestão Organizacional")
                m1, m2, m3, m4, m5, m6 = st.columns(6)
                with m1:
                    exibir_imagem_repositorio("Isolamento.png", "Isolamento")
                    if st.button("Isolamento Área", key="k_iso", use_container_width=True): avaliar_dupla("o_que", "Isolamento")
                with m2:
                    exibir_imagem_repositorio("Cadeado.png", "LOTO")
                    if st.button("Cadeado / LOTO", key="k_loto", use_container_width=True): avaliar_dupla("o_que", "LOTO")
                with m3:
                    exibir_imagem_repositorio("Sinalizacao.NaoOpere.png", "Sinalizacao")
                    if st.button("Sinalização LOTO", key="k_sin", use_container_width=True): avaliar_dupla("o_que", "Sinalizacao")
                with m4:
                    exibir_imagem_repositorio("PET.png", "Documentação")
                    if st.button("Assinar PET / PT", key="k_pet", use_container_width=True): avaliar_dupla("o_que", "PET")
                with m5:
                    exibir_imagem_repositorio("Cilindro_Teste_Resposta.png", "Bump Test")
                    if st.button("Acionar Bump Test", key="k_bt", use_container_width=True): avaliar_dupla("o_que", "Teste Resposta")
                with m6:
                    exibir_imagem_repositorio("APR.png", "Análise de Risco")
                    if st.button("Validar APR", key="k_apr", use_container_width=True): avaliar_dupla("o_que", "APR")

                st.markdown("#### ⚙️ 3. Sistemas Atmosféricos, Coletivos e Linhas de Vida")
                n1, n2, n3, n4, n5 = st.columns(5)
                with n1:
                    exibir_imagem_repositorio("Ventilacao_Exaustao.png", "Ventilacao")
                    if st.button("Ventilação/Purga", key="k_vent", use_container_width=True): avaliar_dupla("o_que", "Ventilacao")
                with n2:
                    exibir_imagem_repositorio("DetectorGas.png", "Detector")
                    if st.button("Medição Gases", key="k_det", use_container_width=True): avaliar_dupla("o_que", "Detector")
                with n3:
                    exibir_imagem_repositorio("Tripe.png", "Tripé")
                    if st.button("Tripé / Roldanas", key="k_tri", use_container_width=True): avaliar_dupla("o_que", "Tripe")
                with n4:
                    exibir_imagem_repositorio("Talabarte_Y.png", "Talabarte Y")
                    if st.button("Acionar Talabarte Y", key="k_ty", use_container_width=True): avaliar_dupla("o_que", "Talabarte_Y")
                with n5:
                    exibir_imagem_repositorio("TravaQuedas.png", "TravaQuedas")
                    if st.button("Acionar Trava-Quedas", key="k_tq", use_container_width=True): avaliar_dupla("o_que", "TravaQuedas")

                st.markdown("#### 🪖 4. Equipamentos Individuais e Proteção de Trauma")
                o1, o2, o3, o4 = st.columns(4)
                with o1:
                    exibir_imagem_repositorio("Cinto_Seguranca.png", "EPI")
                    if st.button("Equipar Cinto/EPI", key="k_epi", use_container_width=True): avaliar_dupla("o_que", "EPI")
                with o2:
                    exibir_imagem_repositorio("Radio_Comunicacao.png", "HT")
                    if st.button("Rádio HT", key="k_com", use_container_width=True): avaliar_dupla("o_que", "Comunicacao")
                with o3:
                    exibir_imagem_repositorio("Lado_de_fora.png", "Posto Externo")
                    if st.button("Posto Externo (Fora)", key="k_out", use_container_width=True): avaliar_dupla("o_que", "LadoFora")
                with o4:
                    exibir_imagem_repositorio("Fita_AntiTrauma.png", "Fita Alívio")
                    if st.button("Fita Anti-Trauma", key="k_fat", use_container_width=True): avaliar_dupla("o_que", "Fita_AntiTrauma")

                # 🚑 5. Emergência Tática Final Integrada
                if st.session_state.etapa_atual == (len(fluxo_seguranca) - 1):
                    st.markdown("---")
                    st.markdown("### 🚑 5. Recursos Médicos para Sinistros (Clique para acionar)")
                    if "Arnês" in st.session_state.acidente_selecionado or "Asfixia" in st.session_state.acidente_selecionado:
                        st.info("💡 **Dica Técnico-Médica:** Riscos respiratórios ou suspensões inertes prolongadas exigem o uso imediato do **Respirador** ou manobras táticas rápidas para oxigenação das pernas.")
                    else:
                        st.info("💡 **Dica Técnico-Médica:** Quedas estruturais ou prensamentos com suspeitas de fraturas graves exigem a imobilização local firme com **Talas/Ataduras** ou **Maca Rígida** antes do içamento.")

                    f1, f2, f3, f4 = st.columns(4)
                    with f1:
                        exibir_imagem_repositorio("Respirador_Autonomo.png", "Respirador")
                        if st.button("Respirador Autônomo", key="f_m1", use_container_width=True): avaliar_dupla("o_que", "Respirador")
                    with f2:
                        exibir_imagem_repositorio("Colar_Cervical.png", "Maca Rígida")
                        if st.button("Maca Rígida + Colar", key="f_m2", use_container_width=True): avaliar_dupla("o_que", "MacaRigida")
                    with f3:
                        exibir_imagem_repositorio("Maca_Sked.png", "Maca Sked")
                        if st.button("Maca Sked Envelope", key="f_m3", use_container_width=True): avaliar_dupla("o_que", "MacaSked")
                    with f4:
                        exibir_imagem_repositorio("Talas_Ataduras.png", "Talas")
                    if st.button("Talas e Ataduras", key="f_m4", use_container_width=True): 
                        avaliar_dupla("o_que", "Talas")

        if st.session_state.historico_acoes:
            st.markdown("---")
            st.write("📋 **Histórico de Passos Concluídos com Sucesso:**")
            for item in st.session_state.historico_acoes: 
                st.write(item)
