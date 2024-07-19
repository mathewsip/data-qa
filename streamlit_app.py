import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain.callbacks import StreamlitCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent

# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets["OPEN_API_KEY"]



# ------------------- Create Sidebar Chat ----------------------

# Increase the default width of the main area by 50%
st.set_page_config(layout="wide")

st.markdown("")
st.markdown("")
 

with st.sidebar:
  st.markdown("")
  st.markdown(':robot: Text to Analytics')
  st.markdown("")
  st.markdown("")
    # Input fields for battery parameters
  st.subheader('**How to Use:**')
  st.write('''

  1. 📄 Upload your Data.
  2. Click the "Prepare for Analysis" Button.
  3. Ask Questions! 📊.

  ''')
  st.markdown("")


llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
db = SQLDatabase.from_uri("sqlite:///Delta_MUV_May.db")

agent = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

if "messages" not in st.session_state or st.sidebar.button("New Conversation"):
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi Nithin, how can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask me anything!")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        # agentfs = get_fewshot_agent_chain()
        response = agent.run(user_query, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)










    # # Create an OpenAI client.
    # client = OpenAI(api_key=openai_api_key)

    # # Let the user upload a file via `st.file_uploader`.
    # uploaded_file = st.file_uploader(
    #     "Upload a document (.txt or .md)", type=("txt", "md")
    # )

    # # Ask the user for a question via `st.text_area`.
    # question = st.text_area(
    #     "Now ask a question about the document!",
    #     placeholder="Can you give me a short summary?",
    #     disabled=not uploaded_file,
    #)

    # if uploaded_file and question:

    #     # Process the uploaded file and question.
    #     document = uploaded_file.read().decode()
    #     messages = [
    #         {
    #             "role": "user",
    #             "content": f"Here's a document: {document} \n\n---\n\n {question}",
    #         }
    #     ]

    #     # Generate an answer using the OpenAI API.
    #     stream = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=messages,
    #         stream=True,
    #     )

    #     # Stream the response to the app using `st.write_stream`.
    #     st.write_stream(stream)
