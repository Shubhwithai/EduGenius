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
num_questions = st.slider("Number of Questions", 1, 10, 5)
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
custom_hint = st.text_area("Additional Instructions (Optional)")

# Generation and display
if st.button("Generate MCQs"):
    with st.spinner(f"Creating {num_questions} questions about {topic}..."):
        try:
            # Generate questions
            response = client.qna_engine.generate_questions(
                topic=topic,
                num_questions=num_questions,
                difficulty=difficulty,
                additional_instructions=custom_hint
            )
            
            # Check if response is valid and contains questions
            if response and hasattr(response, 'questions') and response.questions:
                st.subheader("Generated Questions")
                
                # Display each question with options, answer, and explanation
                for i, question in enumerate(response.questions, 1):
                    with st.expander(f"Question {i}", expanded=True):
                        st.markdown(f"**Question:** {question.question}")
                        st.write("**Options:**")
                        for j, option in enumerate(question.options, 1):
                            st.write(f"{j}. {option}")
                        st.success(f"**Correct Answer:** {question.answer}")
                        if hasattr(question, 'explanation') and question.explanation:
                            st.info(f"**Explanation:** {question.explanation}")
                
                # Download feature
                try:
                    questions_dict = [
                        {
                            "question": q.question,
                            "options": q.options,
                            "answer": q.answer,
                            "explanation": getattr(q, 'explanation', None)
                        }
                        for q in response.questions
                    ]
                    
                    json_str = json.dumps({"questions": questions_dict}, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="Download Questions",
                        data=json_str,
                        file_name="generated_questions.json",
                        mime="application/json"
                    )
                except Exception as json_error:
                    st.warning("Could not create download file, but questions are displayed above.")
            else:
                st.error("No questions were generated. Please check your inputs and try again.")
                
        except Exception as e:
            st.error("Generation failed. Please check your inputs and try again.")
            st.error(f"Error details: {str(e)}")

# Footer note
st.markdown("---")
st.caption("Note: Generated content should be reviewed by subject matter experts.")
