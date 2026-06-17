import streamlit as st
import os

# Configuração da página para aproveitar o espaço horizontal
st.set_page_config(page_title="Portal de Simuladores SST", page_icon="🛡️", layout="wide")

# --- CONTROLE DE ESTADOS (SESSION STATE MULTI-ABA) ---
if "etapa_atual_33" not in st.session_state:
    st.session_state.etapa_atual_33 = 0
if "etapa_atual_35" not in st.session_state:
    st.session_state.etapa_atual_35 = 0
if "erro_33" not in st.session_state:
    st.session_state.erro_33 = False
if "erro_35" not in st.session_state:
    st.session_state.erro_35 = False
if "erros_acumulados_33" not in st.session_state:
    st.session_state.erros_acumulados_33 = 0
if "erros_acumulados_35" not in st.session_state:
    st.session_state.erros_acumulados_35 = 0
if "hist_33" not in st.session_state:
    st.session_state.hist_33 = []
if "hist_35" not in st.session_state:
    st.session_state.hist_35 = []
if "resp_33" not in st.session_state:
    st.session_state.resp_33 = None
if "resp_35" not in st.session_state:
    st.session_state.resp_35 = None

def resetar_33():
    st.session_state.etapa_atual_33 = 0
    st.session_state.erro_33 = False
    st.session_state.erros_acumulados_33 = 0
    st.session_state.hist_33 = []
    st.session_state.resp_33 = None

def resetar_35():
    st.session_state.etapa_atual_35 = 0
    st.session_state.erro_35 = False
    st.session_state.erros_acumulados_35 = 0
    st.session_state.hist_35 = []
    st.session_state.resp_35 = None

# Função com Fallback Visual se a imagem não existir
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

# --- LISTAGENS ---
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
    "Reparo de Telhado Industrial [3 Trabalhadores no topo | Sem Vigia exclusivo]",
    "Montagem de Fachada de Prédio [2 Trabalhadores no topo | Sem Vigia exclusivo]",
    "Substituição de Luminárias em Linha de Poste [1 Trabalhador no topo | Exige 1 Vigia em solo]"
]

acidentes_disponiveis = [
    "Mal Súbito por Asfixia (Falta de Oxigênio)",
    "Intoxicação por Gases com Perda de Consciência",
    "Queda de Altura com Fratura Exposta no Fêmur",
    "Prensamento de Membro com Hemorragia Grave",
    "Queimadura Química por Contato Respiratório",
    "Choque Elétrico por Equipamento Não Aterrado"
]
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
    "Reparo de Telhado Industrial [3 Trabalhadores no topo | Sem Vigia exclusivo]": "Altura_Telhado.png",
    "Montagem de Fachada de Prédio [2 Trabalhadores no topo | Sem Vigia exclusivo]": "Altura_Andaimes.png",
    "Substituição de Luminárias em Linha de Poste [1 Trabalhador no topo | Exige 1 Vigia em solo]": "Altura_Poste.png"
}

# --- CRIAÇÃO DAS ABAS NA INTERFACE SUPERIOR ---
tab_nr33, tab_nr35 = st.tabs(["⚠️ Módulo NR-33 (Espaço Confinado)", "🧗 Módulo NR-35 (Trabalho em Altura)"])

# =========================================================================
#                    A B A   N R - 3 3   (ESPAÇO CONFINADO)
# =========================================================================
with tab_nr33:
    st.title("🛡️ Simulador Prático NR-33")
    col_esq_33, col_dir_33 = st.columns([1.1, 1.3], gap="large")
    
    with col_esq_33:
        st.header("📸 Análise do Ambiente")
        st.selectbox("1. Selecione a Atividade Operacional da OS:", servicos_nr33, index=None, key="s_33", on_change=resetar_33)
        st.session_state.servico_selecionado = st.session_state.s_33
        
        st.selectbox("2. Selecione o Risco à Saúde Associado:", acidentes_disponiveis, index=None, key="a_33", on_change=resetar_33)
        st.session_state.acidente_selecionado = st.session_state.a_33
        
        st.markdown("---")
        if st.session_state.servico_selecionado in MAPEAMENTO_CENARIOS_33:
            st.subheader(f"📍 Cenário Industrial: {st.session_state.servico_selecionado}")
            exibir_imagem_repositorio(MAPEAMENTO_CENARIOS_33[st.session_state.servico_selecionado], "Cenário NR-33")
        else:
            tab_f, tab_t = st.tabs(["👁️ Visão Frente", "👁️ Visão Topo"])
            with tab_f: exibir_imagem_repositorio("Esp.Confinado.Frente.png", "Frente")
            with tab_t: exibir_imagem_repositorio("Esp.Confinado.Topo.png", "Topo")
    with col_dir_33:
        st.header("🕹️ Painel de Decisões Técnicas")
        if not st.session_state.servico_selecionado or not st.session_state.acidente_selecionado:
            st.info("Configure os dados da Ordem de Serviço na coluna da esquerda para liberar a simulação.")
        else:
            acidente_33 = st.session_state.acidente_selecionado
            item_medico_33 = "Respirador" if ("Asfixia" in acidente_33 or "Gases" in acidente_33) else "Talas"
            
            fluxo_nr33 = [
                {"acao": "Instalar a barreira física de pedestais e correntes para delimitar a área de risco", "quem": "Supervisor", "oq": "Isolamento", "mot": "O Supervisor deve garantir o isolamento da área antes de abrir o acesso."},
                {"acao": "Instalar garras, cadeados e travas nos disjuntores e válvulas de alimentação", "quem": "Supervisor", "oq": "LOTO", "mot": "O bloqueio mecânico (LOTO) e elétrico é gerenciado e inspecionado pelo Supervisor."},
                {"acao": "Fixar as etiquetas de aviso nos pontos de bloqueio para alertar o impedimento", "quem": "Supervisor", "oq": "Sinalizacao", "mot": "A sinalização do LOTO formaliza o travamento sob coordenação do Supervisor."},
                {"acao": "Realizar o teste de resposta (bump test) do detector acoplando-o ao cilindro de gás", "quem": "Supervisor", "oq": "Teste Resposta", "mot": "O Supervisor deve certificar o detector de gases antes do uso em campo."},
                {"acao": "Ligar o conjunto mecânico para injetar ar limpo ou exaurir os gases estagnados no fundo", "quem": "Supervisor", "oq": "Ventilacao", "mot": "O Supervisor determina e monitora o início da ventilação mecânica prévia."},
                {"acao": "Introduzir a sonda do detector para efetuar a leitura dos gases em múltiplos níveis", "quem": "Supervisor", "oq": "Detector", "mot": "A avaliação atmosférica eletrônica inicial é um dever legal obrigatório do Supervisor."},
                {"acao": "Preencher e assinar os requisitos de liberação da Permissão de Entrada e Trabalho (PET)", "quem": "Supervisor", "oq": "PET", "mot": "A liberação formal por escrito por meio da PET compete unicamente ao Supervisor."},
                {"acao": "Montar e preparar a estrutura de ancoragem e o sistema de vantagem mecânica sobre o acesso", "quem": "Vigia", "oq": "Tripe", "mot": "Na fase preparatória preventiva, cabe ao Vigia estruturar os sistemas de movimentação externos."},
                {"acao": "Equipar o cinto de segurança e descer pelo acesso para iniciar a atividade prática interna", "quem": "Entrante", "oq": "EPI", "mot": "O entrante acessa o interior portando o cinto conectado com segurança à linha de vida."},
                {"acao": "Monitorar continuamente a atmosfera interna carregando o detector portátil junto a si", "quem": "Entrante", "oq": "Detector", "mot": "O entrante deve portar o detector no interior para captar variações súbitas de gases."},
                {"acao": "Permanecer do lado de fora em vigilância constante externa e comunicação contínua", "quem": "Vigia", "oq": "LadoFora", "mot": "O Vigia atua mantendo obrigatoriamente o seu posto de controle fixo do lado de fora da área de risco."},
                {"acao": f"ATENÇÃO! OCORREU UM SINISTRO INTERNO: [{acidente_33}]. Acione o recurso médico correto para o resgate do entrante", "quem": "Resgate", "oq": item_medico_33, "mot": "Na emergência, a Equipe de Resgate assume o salvamento portando o recurso adequado."}
            ]
            
            st.metric(label="⚠️ Desvios / Erros Acumulados (NR-33)", value=st.session_state.erros_acumulados_33)
            
            if st.session_state.erro_33:
                exibir_imagem_repositorio("Alerta_Seguranca.png", "Alerta")
                st.error("🚨 PROCEDIMENTO INCORRETO DETECTADO!")
                st.markdown(f"**Ação que gerou a não-conformidade:** *{fluxo_nr33[st.session_state.etapa_atual_33]['acao']}*")
                c_e1, c_e2 = st.columns(2)
                with c_e1:
                    if st.button("Corrigir Erro (Tentar Novamente) 🛠️", key="c_33", use_container_width=True, type="primary"):
                        st.session_state.erro_33 = False
                        st.session_state.resp_33 = None
                        st.rerun()
                with c_e2:
                    if st.button("Cancelar Procedimento (Reiniciar) ❌", key="r_33", use_container_width=True):
                        resetar_33()
                        st.rerun()
            elif st.session_state.etapa_atual_33 >= len(fluxo_nr33):
                st.balloons()
                st.success("🎉 Simulação de Espaço Confinado Concluída com Sucesso!")
                st.info(f"📊 Desempenho Técnico: Finalizado com **{st.session_state.erros_acumulados_33} desvios**.")
                if st.button("Simular Nova OS (NR-33) 🔄", key="b_rein_33", use_container_width=True):
                    resetar_33()
                    st.rerun()
            else:
                p_33 = fluxo_nr33[st.session_state.etapa_atual_33]
                st.progress(st.session_state.etapa_atual_33 / len(fluxo_nr33))
                st.warning(f"👉 **{p_33['acao']}**")
                
                if st.session_state.resp_33 is None: st.markdown("#### 🟥 **PASSO 1:** Clique no **Responsável** pela tarefa:")
                else: st.markdown(f"#### 🟨 **PASSO 2:** Responsável: **[{st.session_state.resp_33}]**. Clique no **Dispositivo/Ação**:")
                
                def val_33(tipo, val):
                    if tipo == "quem":
                        if val == p_33["quem"]: st.session_state.resp_33 = val
                        else: st.session_state.erros_acumulados_33 += 1; st.session_state.erro_33 = True
                    elif tipo == "oq":
                        if st.session_state.resp_33 is None: return
                        if val == p_33["oq"]:
                            st.session_state.hist_33.append(f"🟩 Concluído: {p_33['acao']} -> [{p_33['quem']}] + [{p_33['oq']}]")
                            st.session_state.etapa_atual_33 += 1
                            st.session_state.resp_33 = None
                        else: st.session_state.erros_acumulados_33 += 1; st.session_state.erro_33 = True
                    st.rerun()
                
                # Interface de Botões Comuns 33
                st.markdown("#### 👥 1. Integrantes da Equipe")
                q1, q2, q3, q4 = st.columns(4)
                with q1: exibir_imagem_repositorio("Supervisor.png", "Supervisor"); st.button("Supervisor", key="q_su", use_container_width=True, on_click=val_33, args=("quem", "Supervisor"))
                with q2: exibir_imagem_repositorio("Entrante.png", "Entrante"); st.button("Entrante", key="q_en", use_container_width=True, on_click=val_33, args=("quem", "Entrante"))
                with q3: exibir_imagem_repositorio("Vigia.png", "Vigia"); st.button("Vigia", key="q_vi", use_container_width=True, on_click=val_33, args=("quem", "Vigia"))
                with q4: exibir_imagem_repositorio("Resgate1.png", "Resgate"); st.button("Equipe Resgate", key="q_re", use_container_width=True, on_click=val_33, args=("quem", "Resgate"))
                
                st.markdown("#### 🔒 2. Isolamento, Bloqueio e Dispositivos")
                w1, w2, w3, w4, w5 = st.columns(5)
                with w1: exibir_imagem_repositorio("Isolamento.png", "Iso"); st.button("Isolamento Área", key="w_is", use_container_width=True, on_click=val_33, args=("o_que", "Isolamento"))
                with w2: exibir_imagem_repositorio("Cadeado.png", "LOTO"); st.button("Cadeado / LOTO", key="w_lo", use_container_width=True, on_click=val_33, args=("o_que", "LOTO"))
                with w3: exibir_imagem_repositorio("Sinalizacao.NaoOpere.png", "Sin"); st.button("Sinalização LOTO", key="w_si", use_container_width=True, on_click=val_33, args=("o_que", "Sinalizacao"))
                with w4: exibir_imagem_repositorio("PET.png", "PET"); st.button("Emitir / Assinar PET", key="w_pe", use_container_width=True, on_click=val_33, args=("o_que", "PET"))
                with w5: exibir_imagem_repositorio("Cilindro_Teste_Resposta.png", "Bump"); st.button("Acionar Bump Test", key="w_bu", use_container_width=True, on_click=val_33, args=("o_que", "Teste Resposta"))
                
                st.markdown("#### ⚙️ 3. Sistemas Atmosféricos e Proteções")
                r1, r2, r3, r4, r5 = st.columns(5)
                with r1: exibir_imagem_repositorio("Ventilacao_Exaustao.png", "Vent"); st.button("Ventilação/Purga", key="r_ve", use_container_width=True, on_click=val_33, args=("o_que", "Ventilacao"))
                with r2: exibir_imagem_repositorio("DetectorGas.png", "Det"); st.button("Medição Gases", key="r_de", use_container_width=True, on_click=val_33, args=("o_que", "Detector"))
                with r3: exibir_imagem_repositorio("Tripe.png", "Tri"); st.button("Tripé Ancoragem", key="r_tr", use_container_width=True, on_click=val_33, args=("o_que", "Tripe"))
                with r4: exibir_imagem_repositorio("Cinto_Seguranca.png", "EPI"); st.button("Cinto / EPI", key="r_ep", use_container_width=True, on_click=val_33, args=("o_que", "EPI"))
                with r5: exibir_imagem_repositorio("Radio_Comunicacao.png", "HT"); st.button("Rádio HT", key="r_ht", use_container_width=True, on_click=val_33, args=("o_que", "Comunicacao"))
                with r1: exibir_imagem_repositorio("Lado_de_fora.png", "Fora"); st.button("Posto Externo", key="r_fo", use_container_width=True, on_click=val_33, args=("o_que", "LadoFora"))
                
                if st.session_state.etapa_atual_33 == (len(fluxo_nr33) - 1):
                    st.markdown("#### 🚑 5. Recursos de Salvamento Disponíveis")
                    m1, m2 = st.columns(2)
# =========================================================================
#                    A B A   N R - 3 5   (TRABALHO EM ALTURA)
# =========================================================================
with tab_nr35:
    st.title("🧗 Simulador Prático NR-35")
    col_esq_35, col_dir_35 = st.columns([1.1, 1.3], gap="large")
    
    with col_esq_35:
        st.header("📸 Configuração e Engenharia do Cenário")
        st.selectbox("1. Selecione a Atividade de Trabalho em Altura:", servicos_nr35, index=None, key="s_35", on_change=resetar_35)
        st.session_state.servico_selecionado_35 = st.session_state.s_35
        
        st.selectbox("2. Selecione o Cenário de Acidente Potencial:", acidentes_disponiveis, index=None, key="a_35", on_change=resetar_35)
        st.session_state.acidente_selecionado_35 = st.session_state.a_35
        
        st.markdown("---")
        
        # --- ENGENHARIA DE DADOS DA ZONA LIVRE DE QUEDA (ZLQ) SOLICITADA ---
        if st.session_state.servico_selecionado_35:
            servico_atual = st.session_state.servico_selecionado_35
            
            # Autopreenchimento de Fator de Queda e sugestão de valores lógicos conforme seu critério
            if "Telhado" in servico_atual:
                fq_sugerido = "FQ = 2 (Ancoragem nos pés / Topo do cenário)"
                alt_sug, anc_sug, zlq_t_sug = 5.0, 0.0, 5.5
            elif "Fachada" in servico_atual:
                fq_sugerido = "FQ = 1 (Ancoragem na linha do peito/ombro)"
                alt_sug, anc_sug, zlq_t_sug = 6.0, 1.0, 4.5
            else:
                fq_sugerido = "FQ < 1 (Ancoragem acima da cabeça)"
                alt_sug, anc_sug, zlq_t_sug = 8.0, 2.0, 3.5
                
            st.markdown(f"### 📐 Parâmetros Técnicos do Cenário:\n**Análise Geométrica Automática:** `{fq_sugerido}`")
            
            # Inputs manuais para o Engenheiro/Técnico simular
            h_cenario = st.number_input("Altura Total do Cenário (metros até o chão):", min_value=1.0, max_value=30.0, value=alt_sug, step=0.5)
            h_ancoragem = st.number_input("Distância do Topo do Cenário até o Ponto de Ancoragem (metros):", min_value=0.0, max_value=5.0, value=anc_sug, step=0.1)
            zlq_talabarte = st.number_input("Zona Livre de Queda (ZLQ) Requerida pelo Fabricante do Talabarte (metros):", min_value=1.0, max_value=10.0, value=zlq_t_sug, step=0.1)
            
            # Cálculo exato unificado conforme sua correção
            zlq_local = h_cenario + h_ancoragem
            
            st.markdown("---")
            st.markdown(f"#### 📊 Memorial de Cálculo Técnico:")
            st.markdown(f"🔹 **ZLQ do Local de Trabalho:** `{zlq_local:.2f} metros` (Espaço real disponível até colidir com o chão)")
            st.markdown(f"🔹 **ZLQ Exigida pelo Equipamento:** `{zlq_talabarte:.2f} metros` (Extensão do talabarte + Absorvedor aberto + Estatura + Zona de segurança)")
            
            # Validação Crítica de Segurança Operacional
            if zlq_local >= zlq_talabarte:
                st.success("🟩 **ANÁLISE DE RISCO APROVADA:** A ZLQ do local é suficiente. O trabalhador NÃO colidirá com o chão em caso de queda. Atividade liberada para execução.")
                atividade_suspensa = False
            else:
                st.error("🟥 **FALHA CRÍTICA DE SEGURANÇA: OPERAÇÃO SUSPENSA!** A ZLQ local é menor que a requerida pelo equipamento. Em caso de queda, o trabalhador impactará contra o solo. Reduza o fator de queda, eleve a ancoragem ou use trava-quedas retrátil!")
                atividade_suspensa = True
                
            st.markdown("---")
            if servico_atual in MAPEAMENTO_CENARIOS_35:
                st.subheader(f"📍 Cenário Ativo: {servico_atual}")
                exibir_imagem_repositorio(MAPEAMENTO_CENARIOS_35[servico_atual], "Cenário NR-35")
                    with col_dir_35:
        st.header("🕹️ Painel de Operações Técnicas")
        if not st.session_state.servico_selecionado_35 or not st.session_state.acidente_selecionado_35:
            st.info("Configure a Ordem de Serviço e Risco à esquerda para liberar o painel da NR-35.")
        elif atividade_suspensa:
            st.warning("⚠️ Painel de Decisões Bloqueado! Corrija os parâmetros de engenharia à esquerda (aumente a altura ou diminua a ZLQ do talabarte) para viabilizar a liberação segura da atividade.")
        else:
            acidente_35 = st.session_state.acidente_selecionado_35
            servico_35 = st.session_state.servico_selecionado_35
            
            # Ocultação dinâmica do Vigia solicitada: Se disser 'Sem Vigia', esconde o papel
            ocultar_vigia_35 = "Sem Vigia" in servico_35
            monitor_35 = "Entrante" if ocultar_vigia_35 else "Vigia"
            
            item_medico_35 = "MacaRigida" if "Coluna" in acidente_35 else "Talas"
            
            fluxo_nr35 = [
                {"acao": "Elaborar e validar a Análise Preliminar de Risco (APR) listando os perigos da atividade em altura", "quem": "Supervisor", "oq": "APR", "mot": "O Supervisor deve certificar que os riscos e recursos estão corretos antes da liberação."},
                {"acao": "Isolar fisicamente a área de solo correspondente à projeção de queda de materiais", "quem": "Supervisor", "oq": "Isolamento", "mot": "Cabe ao Supervisor assegurar o isolamento de periferia na base da estrutura."},
                {"acao": "Emitir formalmente a assinatura de liberação da Permissão de Trabalho (PT) em altura", "quem": "Supervisor", "oq": "PET", "mot": "A auditoria técnica final e assinatura de liberação da PT competem ao Supervisor."},
                {"acao": "Ajustar os cintos de segurança paraquedistas de todos os envolvidos e checar as fivelas em dupla", "quem": "Entrante", "oq": "EPI", "mot": "Os trabalhadores executantes devem realizar a inspeção e ajuste do próprio cinto antes de subir."},
                {"acao": "Conectar o gancho do Talabarte duplo em Y ou dispositivo Trava-quedas na linha de vida", "quem": "Entrante", "oq": "Talabarte_Y" if "Arnês" in acidente_35 else "TravaQuedas", "mot": "O trabalhador deve se ancorar fixamente à linha de vida antes de iniciar os trabalhos técnicos."},
                {"acao": "Iniciar a subida e executar a atividade técnica no topo da estrutura conforme o quantitativo da OS", "quem": "Entrante", "oq": "Ventilacao", "mot": "Após a liberação e ancoragem, a equipe técnica inicia a execução dos serviços em altura."},
                {"acao": "Garantir o monitoramento constante das condições de risco e manter a prontidão do rádio HT", "quem": monitor_35, "oq": "Comunicacao", "mot": "O encarregado do monitoramento acompanha os riscos climáticos ao redor."},
                {"acao": f"ALERTA! OCORREU UMA QUEDA COM SUSPENSÃO: [{acidente_35}]. Lance imediatamente o recurso de alívio circulatório contra a Síndrome do Arnês", "quem": monitor_35, "oq": "Fita_AntiTrauma", "mot": "O encarregado do monitoramento deve agir rápido para prover a fita de suspensão e evitar o choque circulatório."},
                {"acao": "Mobilizar a brigada, acessar o trabalhador suspenso por cordas e operar o sistema mecânico de descida vertical", "quem": "Resgate", "oq": "Tripe", "mot": "Em caso de sinistro na altura, a Equipe de Resgate assume a operação técnica de polias e descida tática da vítima."},
                {"acao": "Estabilizar a cervical e realizar a imobilização completa do acidentado no solo antes do transporte técnico", "quem": "Resgate", "oq": item_medico_35, "mot": "O time de resgate presta os primeiros socorros imobilizando o trauma no solo conforme o diagnóstico do acidente."}
            ]
            
            st.metric(label="⚠️ Desvios / Erros Acumulados (NR-35)", value=st.session_state.erros_acumulados_35)
            
            if st.session_state.erro_35:
                exibir_imagem_repositorio("Alerta_Seguranca.png", "Alerta")
                st.error("🚨 PROCEDIMENTO INCORRETO DETECTADO!")
                st.markdown(f"**Ação violada:** *{fluxo_nr35[st.session_state.etapa_atual_35]['acao']}*")
                c_y1, c_y2 = st.columns(2)
                with c_y1:
                    if st.button("Corrigir Erro (Tentar Novamente) 🛠️", key="c_35", use_container_width=True, type="primary"):
                        st.session_state.erro_35 = False; st.session_state.resp_35 = None; st.rerun()
                with c_y2:
                    if st.button("Cancelar Procedimento (Reiniciar) ❌", key="r_35", use_container_width=True):
                        resetar_35(); st.rerun()
            elif st.session_state.etapa_atual_
