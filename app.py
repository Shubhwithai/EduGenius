import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_deepseek import ChatDeepSeek

# Set up the EduChain client with DeepSeek
@st.cache_resource
def setup_educhain():
    llm = ChatDeepSeek(model="deepseek-chat")
    config = LLMConfig(custom_model=llm)
    return Educhain(config)

client = setup_educhain()

# Streamlit UI
st.title("🌌 EduChain MCQ Generator")
st.subheader("Generate Multiple Choice Questions using DeepSeek AI")

# User inputs
topic = st.text_input("Enter a topic:", "Solar System")
num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=3)

# Generate button
if st.button("Generate Questions"):
    with st.spinner("Generating questions..."):
        try:
            # Generate questions
            mcq = client.qna_engine.generate_questions(
                topic=topic,
                num=num_questions,
                question_type="Multiple Choice"
            )
            
            # Display questions
            st.success("Generated Questions:")
            for i, question in enumerate(mcq.questions, 1):  # Adjust based on actual response structure
                with st.expander(f"Question {i}: {question.text}"):
                    st.write("Options:")
                    for option in question.options:
                        st.write(f"- {option}")
                    st.markdown(f"**Correct Answer:** {question.correct_answer}")
                    
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
