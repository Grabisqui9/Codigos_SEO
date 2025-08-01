import streamlit as st
from datetime import datetime
import io

def gerar_sitemap_xml_completo(urls, changefreq, priority):
    """
    Gera o conteúdo de um arquivo sitemap.xml a partir de uma lista de URLs,
    incluindo todos os campos: loc, lastmod, changefreq, e priority.

    Args:
        urls (list): A lista de URLs a serem incluídas no sitemap.
        changefreq (str): O valor para a tag <changefreq>.
        priority (float): O valor para a tag <priority>.

    Returns:
        str: O conteúdo completo do arquivo sitemap.xml como uma string.
    """
    # Pega a data e hora atuais em UTC no formato completo (YYYY-MM-DDTHH:MM:SS+00:00)
    lastmod_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    for url in urls:
        # Limpa a URL de espaços em branco para garantir um XML válido
        clean_url = url.strip()
        if not clean_url:
            continue
            
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{clean_url}</loc>')
        xml_parts.append(f'    <lastmod>{lastmod_date}</lastmod>')
        xml_parts.append(f'    <changefreq>{changefreq}</changefreq>')
        xml_parts.append(f'    <priority>{priority:.1f}</priority>') # Formata a prioridade para uma casa decimal
        xml_parts.append('  </url>')

    # Adiciona a tag de fechamento do urlset
    xml_parts.append('</urlset>')

    
    return "\n".join(xml_parts)

# --- Interface do Streamlit ---

st.set_page_config(page_title="Gerador de Sitemap", page_icon="📝")

st.title("Gerador de Sitemap")
st.markdown(
    "Faça o upload de um arquivo `.txt` (com uma URL por linha), defina as configurações e baixe seu `sitemap.xml`."
)

st.subheader("1. Carregue sua Lista de URLs")
uploaded_file = st.file_uploader(
    "Escolha um arquivo .txt",
    type=["txt"],
    label_visibility="collapsed"
)

st.subheader("2. Defina as Configurações do Sitemap")
col1, col2 = st.columns(2)
with col1:
    changefreq = st.selectbox(
        "Frequência de Alteração (`changefreq`)",
        options=["daily", "weekly", "monthly", "yearly", "always", "hourly", "never"],
        index=0 # 'daily' como padrão
    )
with col2:
    priority = st.slider(
        "Prioridade (`priority`)", 
        min_value=0.1, 
        max_value=1.0, 
        value=1.0, # Padrão 1.0 como solicitado
        step=0.1
    )

st.markdown("---")


if uploaded_file is not None:
    try:
        string_data = uploaded_file.getvalue().decode("utf-8")
        urls = [line.strip() for line in string_data.splitlines() if line.strip()]

        st.info(f"Arquivo `{uploaded_file.name}` carregado com **{len(urls)} URLs**.")

        if not urls:
            st.warning("O arquivo parece estar vazio. Verifique o conteúdo.")
        else:
            st.subheader("3. Gere e Baixe seu Arquivo")
            
            # Botão para gerar o sitemap
            if st.button("Gerar Sitemap XML", type="primary"):
                with st.spinner("Construindo seu sitemap..."):
                    sitemap_xml_content = gerar_sitemap_xml_completo(urls, changefreq, priority)
                    st.session_state.sitemap_gerado = sitemap_xml_content
                
                st.success("Sitemap gerado com sucesso!")

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
        st.error("Por favor, verifique se o arquivo está no formato UTF-8 e contém uma URL válida por linha.")


if "sitemap_gerado" in st.session_state and st.session_state.sitemap_gerado:
    st.subheader("4. Renomeie e Baixe") # Nova subseção

    # Campo para o usuário inserir o nome do arquivo
    file_name_input = st.text_input(
        "Nome do arquivo para download:",
        value="sitemap.xml",
        help="Insira o nome do arquivo desejado. A extensão .xml será adicionada se não estiver presente."
    )

   
    if not file_name_input.endswith('.xml'):
        download_file_name = f"{file_name_input}.xml"
    else:
        download_file_name = file_name_input

    st.download_button(
       label="📥 Baixar sitemap.xml",
       data=st.session_state.sitemap_gerado,
       file_name=download_file_name, # Usa o nome do arquivo do campo de texto
       mime="application/xml"
    )
    
    st.subheader("Prévia do XML Gerado")
    st.code(st.session_state.sitemap_gerado, language='xml', line_numbers=True)


st.markdown("---")
st.markdown("Desenvolvido por Giovanni Grabski.")
