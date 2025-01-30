import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_deepseek import ChatDeepSeek
import json

# Initialize Educhain with DeepSeek
@st.cache_resource
def initialize_llm():
    llm = ChatDeepSeek(model="deepseek-chat")
    llm_config = LLMConfig(custom_model=llm)
    return Educhain(llm_config)

client = initialize_llm()

# Streamlit UI
st.title("🧠 AI MCQ Generator with DeepSeek")
st.write("Generate multiple-choice questions for educational purposes")

# Configuration
st.header("Settings")
topic = st.text_input("Topic", "Artificial Intelligence")
custom_hint = st.text_area("Additional Instructions (Optional)")

with st.sidebar:
    num_questions = st.slider("Number of Questions", 1, 10, 5)
    # Force num_questions to be 1 regardless of slider value
    num_questions = 1
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# Generation and display
if st.button("Generate MCQs"):
    with st.spinner(f"Creating question about {topic}..."):
        try:
            # Generate questions
            result = client.qna_engine.generate_questions(
                topic=topic,
                num_questions=num_questions,
                difficulty=difficulty,
                additional_instructions=custom_hint
            )
            
            # Display results
            st.subheader("Generated Question")
            # Convert result to list if it's not already
            questions = result if isinstance(result, list) else result.questions
            
            # Only process the first question
            if questions:
                question = questions[0]
                with st.expander("Question 1", expanded=True):
                    st.markdown(f"**{question.question}**")
                    st.write("Options:")
                    for opt in question.options:
                        st.write(f"- {opt}")
                    st.success(f"Answer: {question.answer}")
                    if hasattr(question, 'explanation'):
                        st.info(f"Explanation: {question.explanation}")
            
                # Download feature
                questions_dict = [{
                    "question": question.question,
                    "options": question.options,
                    "answer": question.answer,
                    "explanation": getattr(question, 'explanation', '')
                }]
                st.download_button(
                    label="Download Question",
                    data=json.dumps({"questions": questions_dict}, indent=2),
                    file_name="generated_question.json",
                    mime="application/json"
                )
            
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
            st.info("Please check your inputs and try again")

st.markdown("---")
st.caption("Note: Generated content should be reviewed by subject matter experts")
