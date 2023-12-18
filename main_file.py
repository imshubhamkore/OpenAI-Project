import streamlit as st
import openai
import os
import json
import time
from streamlit_chat import message
from streamlit_lottie import st_lottie

openai_api_key =st.secrets['openai_api_key']
st.set_page_config(page_title='Fashion Advisor', page_icon='👕', layout="centered")


def new_session():
    st.session_state['text']=''
    del st.session_state.messages
    del st.session_state.past
    del st.session_state.generated
    file = 'database.json'
    with open (file,'w') as f:
        f.seek(0)
        f.truncate()


if 'chat_history' not in st.session_state:                                                                                  # Creating a list -chat history  in session state if not existed
    st.session_state.chat_history=[]

if "messages" not in st.session_state:                                                                                      # Creating messages list in session state if not existed
    st.session_state.messages = []

if 'past' not in st.session_state:
    st.session_state.past=[]
if 'generated' not in st.session_state:
    st.session_state.generated=[]

with st.sidebar:
    st.header("Fashion Advisor App ")
    st_lottie("https://lottie.host/4d4294dc-1860-48ba-bd3d-19f1cfc46e8c/aMrPD1XmyY.json",quality="high")

    st.header("About")
    st.markdown("Elevate your style with our Fashion Advisor WebApp! Discover personalized fashion recommendations tailored to your taste and preferences. From trendy outfits to timeless classics, our app curates the perfect looks for every occasion. Stay effortlessly chic and explore a world of fashion at your fingertips!")
    
    st.write("For Reference")
    st.write('''-[Streamlit](https://streamlit.io/) 
            -  [OpenAI](https://platform.openai.com/docs/models)''')


def main():
    st.header("Welcome to Your Personal Fashion Advisor",divider='rainbow')
    options=st.chat_input("Enter your response ")
    
   
    if options == None:
            st.markdown("Hi, How can I Help You")
      
   
    else:   
        
        with st.spinner("Bot is working"):
            
            chat_response=get_chat_response(options)
         
        chat_placeholder = st.empty()
        
        with chat_placeholder.container():    
            for i in range(len(st.session_state['generated'])):                
                message(message='You : '+st.session_state['past'][i], is_user=True, key=f"{i}_user",avatar_style="thumbs",seed="Aneka")
                message(message='Bot : '+
                    st.session_state['generated'][i], 
                    key=f"{i}",avatar_style="bottts-neutral",seed="Aneka")
    st.button("End Chat",on_click=new_session,help="To start over")
def get_chat_response(user_message):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})

    # Send to ChatGpt/OpenAi

       
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )

    parsed_gpt_response = gpt_response['choices'][0]['message']['content']

    # Save messages
    save_messages(user_message, parsed_gpt_response)

    return parsed_gpt_response

def load_messages():
    messages = []
    options=''
    name=''
    file = 'database.json'

    empty = os.stat(file).st_size == 0

    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {"role": "system", "content": f"""You are a fashion advisor for a People. When a user asks for any fashion advice, guide them in the best way possible.
                                            Remember to greet the user with 'Hi welcome to your Fashion Advisor App, how can I help you?' if the user asks 'hi' or 'hello' or 'hey'.
                                            follow up questions and frame accordingly.
                                            Don't ask multiple questions at time, one question at a time.
                                            Adapt the 'Always Be Closing' principle carefully for chatbot use. Another theory is when selling anything, everything should be framed within the idea of YES. Always compliment. Always confirm. Always be optimistic.
                                            """}
        )
    return messages


def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.past.append(user_message)
    messages.append({"role": "assistant", "content": gpt_response})
    st.session_state.messages.append({"role": "assistant", "content": gpt_response})
    st.session_state.generated.append(gpt_response)
    with open(file, 'w') as f:
        json.dump(messages, f)



if __name__ == '__main__':
    main()
    