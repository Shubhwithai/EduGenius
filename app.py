import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_deepseek import ChatDeepSeek

# Streamlit Dark Theme
st.set_page_config(
    page_title="Educhain MCQ Generator",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
    background-color: #0e1117;
    color: white;
    }
     [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    [data-testid="stToolbar"] {
        right: 2rem;
    }
    [data-testid="stTextInput"] > div > div > div {
        background-color: #1f2937;
        color: white;
    }
     [data-testid="stNumberInput"] > div > div > div {
        background-color: #1f2937;
        color: white;
         }
    [data-testid="stNumberInput"] input {
        color: white; /* Fix number input text color */
        }
    [data-testid="stButton"] button {
        background-color: #4CAF50;
        color: white;
    }
    [data-testid="stTextArea"] > div > div > div {
        background-color: #1f2937;
        color: white;
    }
    [data-testid="stSelectbox"] > div > div > div {
        background-color: #1f2937;
        color: white;
    }
     [data-testid="stSidebar"] {
        background-color: #1f2937;
        color: white;
    }
    [data-testid="stSidebar"] h1, h2, h3, h4, h5, h6, p, ul, ol, li {
        color: white;
    }
    [data-testid="stMarkdownContainer"] h1, h2, h3, h4, h5, h6, p, ul, ol, li {
        color: white;
    }
    [data-testid="stMarkdownContainer"] {
        color: white;
    }
   </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("🌌 Educhain MCQ Generator")
st.markdown("Generate Multiple Choice Questions using DeepSeek AI")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    topic_input = st.text_input("Enter Topic", "Solar System")
    num_questions_input = st.number_input("Number of Questions", min_value=1, max_value=20, value=3, step=1)
    generate_button = st.button("Generate Questions")

# Set up the EduChain client with DeepSeek
@st.cache_resource
def setup_educhain():
    llm = ChatDeepSeek(model="deepseek-chat")
    config = LLMConfig(custom_model=llm)
    return Educhain(config)

client = setup_educhain()

# Generate and display questions
if generate_button:
    topic = topic_input
    num_questions = num_questions_input

    with st.spinner(f"Generating {num_questions} questions on '{topic}'..."):
        try:
            # Generate questions
            mcq = client.qna_engine.generate_questions(
                topic=topic,
                num=num_questions,
                question_type="Multiple Choice"
            )

            if mcq and mcq.questions:
                st.success(f"Successfully generated {len(mcq.questions)} questions!")
                for i, q_data in enumerate(mcq.questions, 1):
                    st.markdown("---")
                    st.subheader(f"Question {i}: {q_data.question}")

                    # Display options
                    options_display = ""
                    for idx, option in enumerate(q_data.options, start=1):
                        options_display += f"{chr(64 + idx)}. {option}  \n"
                    st.markdown(f"**Options:**  \n{options_display}")

                    # Display correct answer
                    st.markdown(f"**Correct Answer:** {q_data.correct_answer}")

                    # Display explanation (if available)
                    if hasattr(q_data, "explanation") and q_data.explanation:
                        st.markdown(f"**Explanation:** {q_data.explanation}")

            else:
                st.error("Failed to generate questions. Please check your inputs and try again.")

        except Exception as e:
            st.error(f"An error occurred during question generation: {e}")

# Footer
st.markdown("---")
st.markdown("Powered by Educhain and DeepSeek AI")
