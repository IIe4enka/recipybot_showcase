import streamlit as st
from openai import OpenAI
import uuid

LLM_SYSTEM_PROMPT_STRING = '''A client is contacting you to get recommendations on food recipies and ingredients and then buy them through our website.
You must act as a friendly agent that recommends the user food recipies for any dish. Go step by step:
1. If the user specifically asked for a particular dish - write the recipy and all the ingredients
2. If not, give the user general ideas for the dish and ingredients required, but not the recipy itself
3. When the user agrees with your recommendation or asks for a specific dish or course of dishes - write the recipy and all the ingredients

Ask the user additional questions if you are not completely sure what they would like. You can even create new recipies if the client specifically asks for this.
Your job is to make the customer satisfied and help them order the best products for their recipie. Think step by step, iterate and display your thoughts on what to answer.

After you prodive the user with a recipy, at the end of the message add a list of ingridients.
Format it like this: Ингридиенты: ['лук', 'чеснок']

If the user asks to finish or add their recipies to the cart - reply with a following json:
{ 'title': 'Пельмени с говядиной', 'ingridients':['лук', 'чеснок'] }

Do not talk about anything other than culinary, food and recipies. Always respond in Russian language.
'''

def chat_page():    
    st.title("🚀 Добро пожаловать во ВкусоБот! 🚀")
    st.caption("Знакомьтесь, ваш личный кулинарный помощник, который превратит каждый ваш ужин в настоящее кулинарное путешествие! 🍲🌍")
    st.caption("Что умеет ВкусоБот? 🤖")
    st.caption("📜 Подбор Рецептов: Найдет идеальное блюдо на любой вкус и случай, основываясь на ваших предпочтениях и имеющихся продуктах!")
    st.caption("🛒 Список Покупок: Создаст для вас список необходимых ингредиентов и поможет их заказать с доставкой прямо на ваш порог!")
    st.caption("🍲 Кулинарные Советы: Поделится хитростями и секретами приготовления, помогая стать настоящим шеф-поваром у себя дома!")

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    with st.sidebar:
        st.session_state.api_key = st.text_input("Введите ваш OpenAI API Key:")
        
        if st.button("Очистить историю чата"):
            st.session_state.messages = []


    if st.session_state.api_key:
        client = OpenAI(api_key=st.session_state.api_key)

    else:
        st.warning("Пожалуйста, введите ваш OpenAI API Key для начала работы с ВкусоБот.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hello?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            openai_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            openai_msgs.append({"role": "system", "content": LLM_SYSTEM_PROMPT_STRING})
            # openai_msgs.append({"role": "system", "content": retrieved_data})
            for response in client.chat.completions.create(
                model='gpt-4-1106-preview',
                messages=openai_msgs,
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "") 
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            #response = client.chat.completions.create(model=LLM_FASTEST_MODEL,messages=[{"role": "assistant", "content": LLM_PRODUCTS_PROMPT}, {"role": "user", "content": full_response}])
            #retrieved_docs = vector_search(query=response.choices[0].message.content, collection_name="product_table", k_query=1)
            #retrieved_ids = [doc.metadata['id'] for doc in retrieved_docs]

        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == '__main__':
    chat_page()
