import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_deepseek import ChatDeepSeek

# Initialize Educhain with DeepSeek
@st.cache_resource
def initialize_llm():
    llm = ChatDeepSeek(model="deepseek-chat")
    llm_config=LLMConfig(custom_model=llm)
    return Educhain(llm_config)

client = initialize_llm()

# Streamlit UI
st.title("🧠 AI MCQ Generator")
st.write("Generate MCQs instantly with DeepSeek")

# Simple configuration
topic = st.text_input("Enter topic", "Artificial Intelligence")
num_questions = st.slider("Number of questions", 1, 5, 3)
difficulty = st.selectbox("Difficulty level", ["Easy", "Medium", "Hard"])

if st.button("Generate Questions"):
    with st.spinner("Creating questions..."):
        try:
            mcqs = client.qna_engine.generate_questions(
                topic=topic,
                num=num_questions,
                question_type="Multiple Choice",
                difficulty_level=difficulty
            )
            
            for i, question in enumerate(mcqs.questions, 1):
                with st.expander(f"Question {i}", expanded=True):
                    st.markdown(f"**{question.question}**")
                    
                    # Display options with letters
                    for j, option in enumerate(question.options, 1):
                        st.write(f"{chr(64+j)}. {option}")
                    
                    # Handle different answer formats
                    if hasattr(question, 'correct_answer'):
                        answer = question.correct_answer
                    elif hasattr(question, 'correct_option'):
                        answer = question.options[question.correct_option-1]
                    else:
                        answer = "Could not determine correct answer"
                    
                    st.success(f"**Answer:** {answer}")
                    
                    if hasattr(question, 'explanation'):
                        st.info(f"*Explanation:* {question.explanation}")

        except Exception as e:
            st.error(f"Failed to generate questions: {str(e)}")
