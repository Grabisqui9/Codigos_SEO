import streamlit as st
from datetime import datetime
import io
# Não precisamos mais do pandas!

def gerar_sitemap_xml_completo(urls, changefreq, priority):
    """
    Gera o conteúdo de um arquivo sitemap.xml a partir de uma lista de URLs.
    """
    lastmod_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in urls:
        clean_url = url.strip()
        if not clean_url:
            continue
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{clean_url}</loc>')
        xml_parts.append(f'    <lastmod>{lastmod_date}</lastmod>')
        xml_parts.append(f'    <changefreq>{changefreq}</changefreq>')
        xml_parts.append(f'    <priority>{priority:.1f}</priority>')
        xml_parts.append('  </url>')
    xml_parts.append('</urlset>')
    return "\n".join(xml_parts)

# --- Interface do Streamlit ---

st.set_page_config(page_title="Gerador de Sitemap", page_icon="📝")

st.title("Gerador de Sitemap")
st.markdown(
    "Forneça sua lista de URLs (colando ou via upload), defina as configurações e baixe seu `sitemap.xml`."
)

urls = []

st.subheader("1. Forneça sua Lista de URLs")

# --- ALTERAÇÃO: Simplificado para duas abas (Colar e TXT) ---
tab1, tab2 = st.tabs(["📋 Colar URLs", "📄 Upload de TXT"])

with tab1:
    st.markdown("Cole as URLs abaixo, uma por linha.")
    pasted_urls = st.text_area("Cole suas URLs aqui", height=250, label_visibility="collapsed")
    if pasted_urls:
        urls = [line.strip() for line in pasted_urls.splitlines() if line.strip()]

with tab2:
    st.markdown("Faça o upload de um arquivo `.txt` com uma URL por linha.")
    uploaded_txt = st.file_uploader("Escolha um arquivo .txt", type=["txt"], label_visibility="collapsed")
    if uploaded_txt:
        string_data = uploaded_txt.getvalue().decode("utf-8")
        urls = [line.strip() for line in string_data.splitlines() if line.strip()]

st.subheader("2. Defina as Configurações do Sitemap")
col1, col2 = st.columns(2)
with col1:
    changefreq = st.selectbox("Frequência (`changefreq`)", ["daily", "weekly", "monthly", "yearly", "always", "hourly", "never"], index=0)
with col2:
    priority = st.slider("Prioridade (`priority`)", 0.1, 1.0, 1.0, 0.1)

st.markdown("---")

if urls:
    st.info(f"**{len(urls)} URLs** foram carregadas e estão prontas para serem processadas.")
    
    st.subheader("3. Gere seu Arquivo")
    if st.button("Gerar Sitemap XML", type="primary"):
        with st.spinner("Construindo seu sitemap..."):
            sitemap_xml_content = gerar_sitemap_xml_completo(urls, changefreq, priority)
            st.session_state.sitemap_gerado = sitemap_xml_content
            # Define o nome de arquivo padrão no estado da sessão
            st.session_state.final_filename = "sitemap.xml" 
        st.success("Sitemap gerado com sucesso!")
else:
    st.warning("Aguardando lista de URLs. Por favor, cole ou faça o upload de um arquivo em uma das abas acima.")

# --- ALTERAÇÃO PRINCIPAL: Lógica de renomear e baixar com botão de salvar ---
if "sitemap_gerado" in st.session_state and st.session_state.sitemap_gerado:
    st.subheader("4. Renomeie e Baixe")

    # Usamos colunas para alinhar o campo de texto e o botão de salvar
    col_input, col_button = st.columns([3, 1])

    with col_input:
        # O campo de texto para o novo nome
        new_name_input = st.text_input(
            "Nome do arquivo para download:",
            value=st.session_state.final_filename, # Mostra o nome já salvo
            label_visibility="collapsed"
        )

    with col_button:
        # O botão que salva o nome no estado da sessão
        if st.button("Salvar Nome", use_container_width=True):
            if not new_name_input.strip().endswith('.xml'):
                st.session_state.final_filename = f"{new_name_input.strip()}.xml"
            else:
                st.session_state.final_filename = new_name_input.strip()
            st.toast(f"Nome salvo: {st.session_state.final_filename}")

    # O botão de download agora é simples e sempre usa o nome salvo
    st.download_button(
       label=f"📥 Baixar {st.session_state.final_filename}", # O rótulo é dinâmico!
       data=st.session_state.sitemap_gerado,
       file_name=st.session_state.final_filename, # Usa sempre o nome correto
       mime="application/xml",
       use_container_width=True
    )
    
    st.subheader("Prévia do XML Gerado")
    st.code(st.session_state.sitemap_gerado, language='xml', line_numbers=True)

st.markdown("---")
st.markdown("Desenvolvido por Giovanni Grabski.")
