import streamlit as st
import os

# Configuração da página para aproveitar o espaço horizontal
st.set_page_config(page_title="Simulador NR-33 Avançado", page_icon="🛡️", layout="wide")

# --- CONTROLE DE ESTADOS ---
if "etapa_atual" not in st.session_state:
    st.session_state.etapa_atual = 0
if "erro_procedimento" not in st.session_state:
    st.session_state.erro_procedimento = False
if "total_erros" not in st.session_state:  # ADICIONADO: Contador global de erros acumulados
    st.session_state.total_erros = 0
if "servico_selecionado" not in st.session_state:
    st.session_state.servico_selecionado = None
if "acidente_selecionado" not in st.session_state:
    st.session_state.acidente_selecionado = None
if "historico_acoes" not in st.session_state:
    st.session_state.historico_acoes = []
if "responsavel_selecionado" not in st.session_state:
    st.session_state.responsavel_selecionado = None

# FUNÇÃO AUTOMATIZADA: Cria um box/botão visual se a imagem não existir
def exibir_imagem_repositorio(nome_arquivo, fallback_texto):
    if os.path.exists(nome_arquivo):
        st.image(nome_arquivo, use_container_width=True)
    else:
        st.markdown(
            f"""
            <div style="background-color: #262730; border: 2px dashed #4b4d5a; 
            border-radius: 8px; padding: 20px; text-align: center; color: #a1a1a1; 
            font-weight: bold; margin-bottom: 10px;">
                📷 [Falta subir: {nome_arquivo}]<br>
                <span style="font-size: 12px; font-weight: normal;">{fallback_texto}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

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

# DICIONÁRIO MAPEANDO O SERVIÇO PARA A SUA IMAGEM DE CENÁRIO
MAPEAMENTO_CENARIOS = {
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

# Relação de tipos de acidentes e problemas de saúde
acidentes_disponiveis = [
    "Mal Súbito por Asfixia (Falta de Oxigênio)",
    "Intoxicação por Gases com Perda de Consciência",
    "Queda de Altura com Fratura Exposta no Fêmur",
    "Prensamento de Membro com Hemorragia Grave",
    "Queimadura Química por Contato Respiratório",
    "Choque Elétrico por Equipamento Não Aterrado"
]

def resetar_jogo():
    st.session_state.etapa_atual = 0
    st.session_state.erro_procedimento = False
    st.session_state.total_erros = 0  # Redefine o contador ao reiniciar
    st.session_state.historico_acoes = []
    st.session_state.responsavel_selecionado = None
# Geração dinâmica do fluxo técnico atualizado
def obter_fluxo_dinamico():
    acidente = st.session_state.acidente_selecionado or "Incidente"
    
    if "Asfixia" in acidente or "Gases" in acidente or "Respiratório" in acidente:
        item_medico_requerido = "Respirador"
    elif "Fratura" in acidente or "Hemorragia" in acidente:
        item_medico_requerido = "Talas"
    else:
        item_medico_requerido = "MacaSked"

    return [
        {
            "acao": "Instalar a barreira física de pedestais e correntes ao redor do local para delimitar a área de risco",
            "quem_correto": "Supervisor",
            "o_que_correto": "Isolamento",
            "motivo": "O Supervisor deve garantir que a sinalização e o isolamento de área externa estejam montados antes de abrir o acesso."
        },
        {
            "acao": "Instalar garras, cadeados e travas nos disjuntores e válvulas de alimentação do espaço confinado",
            "quem_correto": "Supervisor",
            "o_que_correto": "LOTO",
            "motivo": "O bloqueio mecânico (LOTO) e elétrico é gerenciado e inspecionado pelo Supervisor antes de qualquer liberação."
        },
        {
            "acao": "Fixar as etiquetas de aviso nos pontos de bloqueio para alertar que o equipamento está impedido",
            "quem_correto": "Supervisor",
            "o_que_correto": "Sinalizacao",
            "motivo": "A sinalização do LOTO formaliza o travamento e deve ser fixada sob a coordenação do Supervisor de Entrada."
        },
        {
            "acao": "Realizar o teste de resposta (bump test) do detector acoplando-o ao cilindro de gás de calibração",
            "quem_correto": "Supervisor",
            "o_que_correto": "Teste Resposta",
            "motivo": "O Supervisor deve testar e certificar que os sensores do detector de gases estão reagindo com rapidez antes do uso."
        },
        {
            "acao": "Ligar o conjunto mecânico para injetar ar limpo ou exaurir os gases estagnados no fundo do espaço confinado",
            "quem_correto": "Supervisor",
            "o_que_correto": "Ventilacao",
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
            "o_que_correto": "PET",
            "motivo": "A emissão, preenchimento físico e assinatura de autorização da PET competem unicamente ao Supervisor."
        },
        {
            "acao": "Montar e preparar a estrutura metálica de ancoragem, o sistema de vantagem mecânica e/ou movimentadores sobre o acesso",
            "quem_correto": "Vigia",
            "o_que_correto": "Tripe",
            "motivo": "Na fase de preparação preventiva, cabe ao Vigia inspecionar e estruturar o tripé e os sistemas de movimentação externa."
        },
        {
            "acao": "Equipar o cinto de segurança e descer pelo acesso para iniciar a realização da atividade prática interna",
            "quem_correto": "Entrante",
            "o_que_correto": "EPI",
            "motivo": "O entrante acessa o interior portando o cinto paraquedista conectado com segurança à linha de vida."
        },
        {
            "acao": "Monitorar continuamente a atmosfera interna carregando o detector portátil junto a si durante o trabalho",
            "quem_correto": "Entrante",
            "o_que_correto": "Detector",
            "motivo": "O entrante deve portar o detector no interior para captar variações súbitas de gases durante a jornada técnica."
        },
        {
            "acao": "Permanecer do lado de fora em vigilância constante externa e comunicação contínua com os trabalhadores",
            "quem_correto": "Vigia",
            "o_que_correto": "LadoFora",
            "motivo": "O Vigia atua mantendo obrigatoriamente o seu posto de controle fixo do lado de fora da área de risco."
        },
        {
            "acao": f"ATENÇÃO! OCORREU UM SINISTRO INTERNO: [{acidente}]. Mobilize a equipe e acione o recurso médico/salvamento tático correto para o resgate do entrante:",
            "quem_correto": "Resgate",
            "o_que_correto": item_medico_requerido,
            "motivo": f"No momento da emergência de [{acidente}], a Equipe de Resgate deve agir imediatamente portando o recurso de salvamento e primeiros socorros adequado."
        }
    ]

# --- ESTRUTURAÇÃO DO LAYOUT COLABORATIVO ---
col_esquerda, col_direita = st.columns([1.1, 1.3], gap="large")

with col_esquerda:
    st.header("📸 Análise do Espaço Confinado")
    if st.session_state.servico_selecionado in MAPEAMENTO_CENARIOS:
        imagem_cenario = MAPEAMENTO_CENARIOS[st.session_state.servico_selecionado]
        st.subheader(f"📍 Cenário Ativo: {st.session_state.servico_selecionado}")
        exibir_imagem_repositorio(imagem_cenario, f"Cenário técnico para {st.session_state.servico_selecionado}")
    else:
        tab_frente, tab_topo = st.tabs(["👁️ Visão de Frente", "👁️ Visão de Topo"])
        with tab_frente: exibir_imagem_repositorio("Esp.Confinado.Frente.png", "Esp.Confinado.Frente.png")
        with tab_topo: exibir_imagem_repositorio("Esp.Confinado.Topo.png", "Esp.Confinado.Topo.png")

    st.markdown("---")
    st.header("🛠️ Configuração da Missão")
    st.selectbox("1. Selecione o serviço a ser realizado:", servicos_disponiveis, index=None, placeholder="Choose...", on_change=resetar_jogo, key="select_servico")
    st.session_state.servico_selecionado = st.session_state.select_servico
    st.selectbox("2. Selecione o tipo de acidente/risco à saúde:", acidentes_disponiveis, index=None, placeholder="Choose...", on_change=resetar_jogo, key="select_acidente")
    st.session_state.acidente_selecionado = st.session_state.select_acidente
# --- COLUNA DIREITA: MECÂNICA DO SIMULADOR ---
with col_direita:
    st.header("🕹️ Painel de Decisões Técnicas")
    
    if not st.session_state.servico_selecionado or not st.session_state.acidente_selecionado:
        st.info("Selecione a Ordem de Serviço E o Tipo de Acidente na coluna ao lado para gerar os procedimentos da NR-33.")
    else:
        fluxo_seguranca = obter_fluxo_dinamico()
        
        # Exibição do indicador de erros na barra superior do painel técnico
        st.metric(label="⚠️ Desvios / Erros Cometidos na Missão", value=st.session_state.total_erros)
        
        if st.session_state.erro_procedimento:
            exibir_imagem_repositorio("Alerta_Seguranca.png", "Tela de Alerta SST")
            st.error("🚨 ALERTA DE SEGURANÇA: PROCEDIMENTO INCORRETO DETECTADO!")
            passo_falho = fluxo_seguranca[st.session_state.etapa_atual]
            st.markdown(f"**Ação que gerou a não-conformidade:** *{passo_falho['acao']}*")
            st.write("Escolha como o sistema deve tratar este erro operacional:")
            c_erro1, c_erro2 = st.columns(2)
            with c_erro1:
                if st.button("Corrigir Erro (Tentar Novamente esta Etapa) 🛠️", use_container_width=True, type="primary"):
                    st.session_state.erro_procedimento = False
                    st.session_state.responsavel_selecionado = None
                    st.rerun()
            with c_erro2:
                if st.button("Cancelar Procedimento (Reiniciar do Zero) ❌", use_container_width=True):
                    resetar_jogo()
                    st.rerun()
                    
        elif st.session_state.etapa_atual >= len(fluxo_seguranca):
            st.balloons()
            st.success(f"🎉 **Procedimento de '{st.session_state.servico_selecionado}' concluído com sucesso total!**")
            st.write(f"O sinistro de [{st.session_state.acidente_selecionado}] foi controlado preventivamente através das regras corretas da NR-33.")
            st.info(f"📊 **Relatório de Desempenho:** O operador concluiu o treinamento com um total de **{st.session_state.total_erros} erro(s)** cometidos.")
            if st.button("Simular Novo Serviço 🔄", use_container_width=True):
                resetar_jogo()
                st.rerun()
        else:
            passo_atual = fluxo_seguranca[st.session_state.etapa_atual]
            st.write(f"**Serviço:** `{st.session_state.servico_selecionado}` | **Risco:** `{st.session_state.acidente_selecionado}`")
            st.progress(st.session_state.etapa_atual / len(fluxo_seguranca))
            
            st.markdown("### 🎯 Próxima Ação Obrigatória:")
            st.warning(f"👉 **{passo_atual['acao']}**")
            
            if st.session_state.responsavel_selecionado is None:
                st.markdown("#### 🟥 **PASSO 1:** Clique primeiro no botão do **Responsável** pela tarefa:")
            else:
                st.markdown(f"#### 🟨 **PASSO 2:** Responsável definido: **[{st.session_state.responsavel_selecionado}]**. Agora clique no botão do **Equipamento, Dispositivo ou Documento** correspondente:")

            def avaliar_dupla(tipo_clique, valor):
                if tipo_clique == "quem":
                    if valor == passo_atual["quem_correto"]: 
                        st.session_state.responsavel_selecionado = valor
                    else: 
                        st.session_state.total_erros += 1  # Incrementa se errar o responsável
                        st.session_state.erro_procedimento = True
                elif tipo_clique == "o_que":
                    if st.session_state.responsavel_selecionado is None:
                        st.warning("⚠️ Selecione primeiro o integrante da equipe (Passo 1) antes do dispositivo!")
                        return
                    if valor == passo_atual["o_que_correto"]:
                        st.session_state.historico_acoes.append(f"🟩 Concluído: {passo_atual['acao']} -> [{passo_atual['quem_correto']}] + [{passo_atual['o_que_correto']}]")
                        st.session_state.etapa_atual += 1
                        st.session_state.responsavel_selecionado = None
                    else: 
                        st.session_state.total_erros += 1  # Incrementa se errar o dispositivo/ação
                        st.session_state.erro_procedimento = True
                st.rerun()

            # 👥 1. Integrantes da Equipe
            st.markdown("#### 👥 1. Integrantes da Equipe (Quem faz?)")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                exibir_imagem_repositorio("Supervisor.png", "Supervisor")
                if st.button("Selecionar Supervisor", key="b_sup", use_container_width=True): avaliar_dupla("quem", "Supervisor")
            with c2:
                exibir_imagem_repositorio("Entrante.png", "Entrante")
                if st.button("Selecionar Entrante", key="b_ent", use_container_width=True): avaliar_dupla("quem", "Entrante")
            with c3:
                exibir_imagem_repositorio("Vigia.png", "Vigia")
                if st.button("Selecionar Vigia", key="b_vig", use_container_width=True): avaliar_dupla("quem", "Vigia")
            with c4:
                exibir_imagem_repositorio("Resgate1.png", "Resgate")
                if st.button("Selecionar Resgate", key="b_res", use_container_width=True): avaliar_dupla("quem", "Resgate")

            # 🔒 2. Isolamento, Bloqueio e Documentação
            st.markdown("#### 🔒 2. Isolamento, Bloqueio e Documentação (O que utiliza?)")
            l1, l2, l3, l4, l5 = st.columns(5)
            with l1:
                exibir_imagem_repositorio("Isolamento.png", "Isolamento")
                if st.button("Isolamento Área", key="b_iso", use_container_width=True): avaliar_dupla("o_que", "Isolamento")
            with l2:
                exibir_imagem_repositorio("Cadeado.png", "LOTO")
                if st.button("Cadeado / LOTO", key="b_loto", use_container_width=True): avaliar_dupla("o_que", "LOTO")
            with l3:
                exibir_imagem_repositorio("Sinalizacao.NaoOpere.png", "Sinalizacao")
                if st.button("Sinalização LOTO", key="b_sin", use_container_width=True): avaliar_dupla("o_que", "Sinalizacao")
            with l4:
                exibir_imagem_repositorio("PET.png", "PET")
                if st.button("Emitir / Assinar PET", key="b_pet", use_container_width=True): avaliar_dupla("o_que", "PET")
            with l5:
                exibir_imagem_repositorio("Cilindro_Teste_Resposta.png", "Teste Resposta")
                if st.button("Acionar Bump Test", key="b_bt", use_container_width=True): avaliar_dupla("o_que", "Teste Resposta")

            st.markdown("#### ⚙️ 3. Sistemas Atmosféricos e Coletivos")
            e1, e2, e3 = st.columns(3)
            with e1:
                exibir_imagem_repositorio("Ventilacao_Exaustao.png", "Ventilacao")
                if st.button("Acionar Ventilação/Purga", key="b_vent", use_container_width=True): avaliar_dupla("o_que", "Ventilacao")
            with e2:
                exibir_imagem_repositorio("DetectorGas.png", "Detector")
                if st.button("Acionar Medição Gases", key="b_det", use_container_width=True): avaliar_dupla("o_que", "Detector")
            with e3:
                exibir_imagem_repositorio("Tripe.png", "Tripe")
                if st.button("Acionar Tripé / Linha Vida", key="b_tri", use_container_width=True): avaliar_dupla("o_que", "Tripe")

            st.markdown("#### 🪖 4. Segurança Individual e Comunicação")
            epi1, epi2, epi3 = st.columns(3)
            with epi1:
                exibir_imagem_repositorio("Cinto_Seguranca.png", "EPI")
                if st.button("Equipar Cinto / EPIs", key="b_epi", use_container_width=True): avaliar_dupla("o_que", "EPI")
            with epi2:
                exibir_imagem_repositorio("Radio_Comunicacao.png", "Comunicacao")
                if st.button("Iniciar Posto de Comunicação", key="b_com", use_container_width=True): avaliar_dupla("o_que", "Comunicacao")
            with epi3:
                exibir_imagem_repositorio("Lado_de_fora.png", "LadoFora")
                if st.button("Posto Externo (Fora)", key="b_out", use_container_width=True): avaliar_dupla("o_que", "LadoFora")

            if st.session_state.etapa_atual == (len(fluxo_seguranca) - 1):
                st.markdown("---")
                st.markdown("### 🚑 5. Recursos de Atendimento Médico e Resgate Tático (Clique para acionar)")
                
                if "Queda" in st.session_state.acidente_selecionado or "Prensamento" in st.session_state.acidente_selecionado:
                    st.info("💡 **Dica Técnica:** Casos de traumas físicos, quedas de altura ou hemorragias graves exigem a imobilização rápida com **Talas e Ataduras** antes do içamento.")
                elif "Asfixia" in st.session_state.acidente_selecionado or "Gases" in st.session_state.acidente_selecionado:
                    st.info("💡 **Dica Técnica:** Atmosferas perigosas com gases tóxicos ou falta de oxigênio exigem a entrada do resgatista com o **Respirador Autônomo** de circuito fechado.")

                res1, res2, res3, res4 = st.columns(4)
                with res1:
                    exibir_imagem_repositorio("Respirador_Autonomo.png", "Respirador")
                    if st.button("Acionar Respirador Autônomo", key="btn_m1", use_container_width=True): avaliar_dupla("o_que", "Respirador")
                with res2:
                    exibir_imagem_repositorio("Colar_Cervical.png", "MacaRigida")
                    if st.button("Acionar Colar + Maca Rígida", key="btn_m2", use_container_width=True): avaliar_dupla("o_que", "MacaRigida")
                with res3:
                    exibir_imagem_repositorio("Maca_Sked.png", "MacaSked")
