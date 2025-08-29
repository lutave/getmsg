import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

id_model = os.getenv("MODEL_ID")

llm = ChatGroq(
    model = id_model,
    temperature=0.7,
    max_tokens = None,
    timeout = None,
    max_retries = 2
)

def llm_generate(prompt, llm=llm):


    template = ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente de redação de mensagens para contatos e grupos nas redes sociais."),
            ("human", "{prompt}")
        ]
    )

    chain = template | llm | StrOutputParser()

    res = chain.invoke({"prompt": prompt})

    return res

title = "Reescritor.AI"

st.set_page_config(
    page_title= title,
    page_icon="✍🏽"
)

st.title(f"✍🏽 {title}")

st.markdown("Transforme suas mensagens em um contexto personalizado, perfeito para criar textos para grupos de amigos, familiares, estudos, política, notícias e muito mais, de forma espontânea, natural e adequada ao contexto.")
Contexto = st.selectbox("Contexto:", options=['Amigos', 'Família', 'Política', 'Noticias', "Acadêmico"], placeholder="Escolha uma opção")
comprimento = st.selectbox('Tamanho:', options=['Curta', 'Média', 'Longa'])
publico = st.selectbox('Público-alvo:', options=['Geral', 'Familiares', 'Amigos', 'Cidadãos', 'Eleitores', 'Profissional' , 'Desconhecidos'], placeholder="Escolha uma opção")
tom = st.multiselect('Tom:', options=['Respeitoso', 'Informal', 'Engraçado', 'Sarcástico', 'Reflexivo', 'Persuasivo', 'Motivacional'], placeholder="Escolha uma opção")
mensagem = st.text_area("Mensagem:", height=200, placeholder="Ex: Vamos nos encontrar para o churrasco no sábado?")
emoji = st.checkbox('Incluir emojis')

if st.button('Gerar Mensagem'):

    if mensagem:
        prompt = f"""
        Reescreva a mensagem abaixo de forma natural e espontânea, mantendo o sentido original.
        Faça alterações apenas quando necessário para melhorar clareza, fluidez ou adequação ao contexto.

        Mensagem: "{mensagem}"

        Siga os seguintes critérios:
        - Contexto: {Contexto}
        - Tamanho da mensagem: {comprimento}
        {"- Tom: " + ', '.join(tom) if tom else ""}
        - Público-alvo: {publico}

        Importante:
        - Respeite o tom original da mensagem, ajustando apenas quando necessário.
        - Adapte ao contexto (ex.: se for engraçada, preserve o humor).
        - Retorne somente a versão reescrita da mensagem, sem aspas duplas e sem explicações extras.
        - {"Adicione emojis de acordo com o contexto da mensagem. " if emoji else "Não inclua emojis na resposta."}
        """
        res = llm_generate(prompt)
        st.write(res)
        st_copy_to_clipboard(res, before_copy_label="Copiar", after_copy_label="Copiado!")
    else:
        st.warning("Por favor, insira uma mensagem.")
