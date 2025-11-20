import streamlit as st
import requests
import calendar
import json
from datetime import datetime, timedelta

st.set_page_config(page_title="Gerenciador de Eventos", page_icon="📅", layout="wide")

API_URL = "http://127.0.0.1:8000"

st.title("📅 Gerenciador de Eventos")
st.markdown("---")

# Abas
tab1, tab2, tab3, tab4 = st.tabs(["➕ Novo Evento", "📋 Listagem", "🗓️ Calendário", "📥 Importar"])

# TAB 1: Novo Evento
with tab1:
    st.header("Adicionar Novo Evento")
    
    with st.form("form_evento"):
        nome = st.text_input("Nome do Evento", placeholder="Ex: Reunião com cliente")
        data = st.date_input("Data")
        hora = st.time_input("Hora")
        
        if st.form_submit_button("💾 Salvar Evento", type="primary"):
            if nome:
                data_hora = datetime.combine(data, hora).isoformat()
                try:
                    response = requests.post(
                        f"{API_URL}/eventos/",
                        json={"nome": nome, "data_hora": data_hora},
                        timeout=5
                    )
                    if response.status_code == 201:
                        st.success(f"✅ Evento '{nome}' criado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"❌ Erro ao criar evento: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Não foi possível conectar à API. Verifique se o backend está rodando.")
            else:
                st.error("❌ Preencha todos os campos!")

# TAB 2: Listagem
with tab2:
    st.header("Listagem de Eventos")
    
    try:
        response = requests.get(f"{API_URL}/eventos/", timeout=5)
        
        if response.status_code == 200:
            eventos = response.json()
            
            if not eventos:
                st.info("📭 Nenhum evento cadastrado.")
            else:
                eventos_ordenados = sorted(eventos, key=lambda e: e["data_hora"])
                
                col_filtro1, col_filtro2 = st.columns(2)
                with col_filtro1:
                    filtro = st.radio("Filtrar por:", ["Todos", "Esta Semana", "Este Mês"], horizontal=True)
                
                agora = datetime.now()
                eventos_filtrados = eventos_ordenados
                
                if filtro == "Esta Semana":
                    inicio_semana = agora.date() - timedelta(days=agora.weekday())
                    fim_semana = inicio_semana + timedelta(days=6)
                    eventos_filtrados = [
                        e for e in eventos_ordenados
                        if inicio_semana <= datetime.fromisoformat(e["data_hora"]).date() <= fim_semana
                    ]
                
                elif filtro == "Este Mês":
                    eventos_filtrados = [
                        e for e in eventos_ordenados
                        if datetime.fromisoformat(e["data_hora"]).month == agora.month
                        and datetime.fromisoformat(e["data_hora"]).year == agora.year
                    ]
                
                st.write(f"**{len(eventos_filtrados)} evento(s)**")
                
                for evento in eventos_filtrados:
                    data_obj = datetime.fromisoformat(evento["data_hora"])
                    data_fmt = data_obj.strftime("%d/%m/%Y %H:%M")
                    status = "⏰ PASSADO" if data_obj < agora else "🔮 FUTURO"
                    
                    with st.expander(f"📌 {evento['nome']} - {data_fmt} {status}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**ID:** {evento['id']}")
                        with col2:
                            st.write(f"**Nome:** {evento['nome']}")
                        with col3:
                            st.write(f"**Data/Hora:** {data_fmt}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button(f"✏️ Editar", key=f"edit_{evento['id']}", use_container_width=True):
                                st.session_state.edit_id = evento['id']
                                st.session_state.edit_nome = evento['nome']
                                st.session_state.edit_data = data_obj.date()
                                st.session_state.edit_hora = data_obj.time()
                                st.rerun()
                        
                        with col_btn2:
                            if st.button(f"🗑️ Deletar", key=f"delete_{evento['id']}", use_container_width=True):
                                try:
                                    del_response = requests.delete(f"{API_URL}/eventos/{evento['id']}", timeout=5)
                                    if del_response.status_code == 204:
                                        st.success(f"✅ Evento deletado!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao deletar evento")
                                except requests.exceptions.ConnectionError:
                                    st.error("❌ Erro de conexão")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Não foi possível conectar à API.")

# Seção de edição
if "edit_id" in st.session_state:
    st.markdown("---")
    st.subheader("✏️ Editar Evento")
    
    with st.form("form_editar"):
        nome_edit = st.text_input("Nome", value=st.session_state.edit_nome)
        data_edit = st.date_input("Data", value=st.session_state.edit_data)
        hora_edit = st.time_input("Hora", value=st.session_state.edit_hora)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.form_submit_button("💾 Atualizar", type="primary", use_container_width=True):
                data_hora_edit = datetime.combine(data_edit, hora_edit).isoformat()
                try:
                    put_response = requests.put(
                        f"{API_URL}/eventos/{st.session_state.edit_id}",
                        json={"nome": nome_edit, "data_hora": data_hora_edit},
                        timeout=5
                    )
                    if put_response.status_code == 200:
                        st.success(f"✅ Evento atualizado!")
                        del st.session_state.edit_id
                        st.rerun()
                    else:
                        st.error("❌ Erro ao atualizar")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Erro de conexão")
        
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                del st.session_state.edit_id
                st.rerun()

# TAB 3: Calendário
with tab3:
    st.header("🗓️ Calendário de Eventos")
    
    col1, col2 = st.columns(2)
    with col1:
        ano = st.number_input("Ano", min_value=2020, max_value=2050, value=datetime.now().year)
    with col2:
        mes = st.selectbox(
            "Mês",
            range(1, 13),
            format_func=lambda x: ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                                   "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"][x],
            index=datetime.now().month - 1
        )
    
    try:
        response = requests.get(f"{API_URL}/eventos/", timeout=5)
        if response.status_code == 200:
            eventos = response.json()
            
            # Filtra eventos do mês
            eventos_mes = {}
            for evento in eventos:
                data_obj = datetime.fromisoformat(evento["data_hora"])
                if data_obj.year == ano and data_obj.month == mes:
                    dia = data_obj.day
                    if dia not in eventos_mes:
                        eventos_mes[dia] = []
                    eventos_mes[dia].append(evento)
            
            # Exibe calendário
            nomes_meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                          "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            
            st.markdown(f"## {nomes_meses[mes]} de {ano}")
            
            cal = calendar.monthcalendar(ano, mes)
            dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
            
            cols = st.columns(7)
            for i, dia_nome in enumerate(dias_semana):
                with cols[i]:
                    st.markdown(f"**{dia_nome}**")
            
            for semana in cal:
                cols = st.columns(7)
                for i, dia in enumerate(semana):
                    with cols[i]:
                        if dia == 0:
                            st.markdown("")
                        else:
                            st.markdown(f"### {dia}")
                            if dia in eventos_mes:
                                for evento in eventos_mes[dia]:
                                    data_obj = datetime.fromisoformat(evento["data_hora"])
                                    hora = data_obj.strftime("%H:%M")
                                    st.markdown(f"📌 **{evento['nome']}**")
                                    st.markdown(f"*{hora}*")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Não foi possível conectar à API.")

# TAB 4: Importar eventos.json
with tab4:
    st.header("📥 Importar Eventos do JSON")
    st.markdown("Utilize a caixa de diálogo abaixo para escolher um arquivo JSON.")
    
    uploaded_file = st.file_uploader("Escolha um arquivo JSON", type=["json"])
    
    if uploaded_file is not None:
        # Carrega dados do arquivo JSON
        try:
            # st.file_uploader retorna um BytesIO, json.load pode ler diretamente
            dados_json = json.load(uploaded_file)
            
            st.subheader("📋 Eventos a Importar")
            
            if not dados_json:
                st.warning("📭 O arquivo JSON está vazio.")
            else:
                st.write(f"**Total de eventos encontrados:** {len(dados_json)}")
                
                # Exibe preview dos eventos
                with st.expander("👁️ Visualizar eventos"):
                    for idx, evento in enumerate(dados_json, 1):
                        try:
                            # Tenta converter data_hora se estiver em formato string
                            if isinstance(evento.get('data_hora'), str):
                                data_obj = datetime.fromisoformat(evento['data_hora'])
                                data_fmt = data_obj.strftime("%d/%m/%Y %H:%M")
                            else:
                                data_fmt = str(evento.get('data_hora', 'Data inválida'))
                            
                            st.markdown(f"**{idx}. {evento.get('nome', 'Evento sem nome')}**")
                            st.markdown(f"   📅 {data_fmt}")
                        except Exception as e:
                            st.warning(f"**{idx}. {evento.get('nome', 'Evento sem nome')}** - ⚠️ Erro ao processar data")
                
                # Botão para importar
                if st.button("✅ Importar Eventos para o Banco de Dados", type="primary", use_container_width=True):
                    importados = 0
                    erros = []
                    
                    for evento in dados_json:
                        try:
                            nome = evento.get('nome', '')
                            data_hora_str = evento.get('data_hora', '')
                            
                            if not nome or not data_hora_str:
                                erros.append(f"Evento sem nome ou data: {evento}")
                                continue
                            
                            # Converte string de data para ISO format se necessário
                            try:
                                data_obj = datetime.fromisoformat(data_hora_str)
                                data_hora_iso = data_obj.isoformat()
                            except (ValueError, TypeError):
                                erros.append(f"Data inválida para '{nome}': {data_hora_str}")
                                continue
                            
                            # Envia para API
                            response = requests.post(
                                f"{API_URL}/eventos/",
                                json={"nome": nome, "data_hora": data_hora_iso},
                                timeout=5
                            )
                            
                            if response.status_code == 201:
                                importados += 1
                            else:
                                erros.append(f"Erro ao importar '{nome}': {response.status_code}")
                        
                        except Exception as e:
                            erros.append(f"Erro processando evento: {str(e)}")
                    
                    # Exibe resultado da importação
                    st.markdown("---")
                    st.subheader("📊 Resultado da Importação")
                    
                    col_result1, col_result2, col_result3 = st.columns(3)
                    
                    with col_result1:
                        st.metric("✅ Importados", importados)
                    with col_result2:
                        st.metric("⚠️ Erros", len(erros))
                    with col_result3:
                        st.metric("📋 Total", len(dados_json))
                    
                    if importados > 0:
                        st.success(f"✅ {importados} evento(s) importado(s) com sucesso!")
                    
                    if erros:
                        with st.expander("🔍 Ver erros"):
                            for erro in erros:
                                st.error(f"❌ {erro}")
        
        except json.JSONDecodeError:
            st.error("❌ Erro ao decodificar o arquivo JSON. Verifique o formato.")
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo: {str(e)}")


st.markdown("---")
st.markdown("<div style='text-align: center'><small>🚀 Gerenciador de Eventos | Full-Stack com SQLAlchemy + FastAPI + Streamlit</small></div>", unsafe_allow_html=True)