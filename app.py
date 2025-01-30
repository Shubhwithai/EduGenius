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

# Configuration - all moved to front
st.header("Settings")
topic = st.text_input("Topic", "Artificial Intelligence")
num_questions = st.slider("Number of Questions", 1, 10, 5)
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
custom_hint = st.text_area("Additional Instructions (Optional)")

# Generation and display
if st.button("Generate MCQs"):
    with st.spinner(f"Creating {num_questions} questions about {topic}..."):
        try:
            # Generate questions
            result = client.qna_engine.generate_questions(
                topic=topic,
                num_questions=num_questions,  # Using the actual number from slider
                difficulty=difficulty,
                additional_instructions=custom_hint
            )
            
            # Display results
            st.subheader("Generated Questions")
            
            # Get questions from the MCQList object
            questions = result.questions
            
            # Display all questions
            for i, question in enumerate(questions, 1):
                with st.expander(f"Question {i}", expanded=True):
                    st.markdown(f"**Question:** {question.question}")
                    st.write("**Options:**")
                    for j, opt in enumerate(question.options, 1):
                        st.write(f"{j}. {opt}")
                    st.success(f"**Correct Answer:** {question.answer}")
                    if hasattr(question, 'explanation'):
                        st.info(f"**Explanation:** {question.explanation}")
        
            # Download feature
            if questions:
                questions_dict = [
                    {
                        "question": q.question,
                        "options": q.options,
                        "answer": q.answer,
                        "explanation": getattr(q, 'explanation', '')
                    }
                    for q in questions
                ]
                st.download_button(
                    label="Download Questions",
                    data=json.dumps({"questions": questions_dict}, indent=2),
                    file_name="generated_questions.json",
                    mime="application/json"
                )
            
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
            st.info("Please check your inputs and try again")

st.markdown("---")
st.caption("Note: Generated content should be reviewed by subject matter experts")
