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
# Force num_questions to be 1
num_questions = 1
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
custom_hint = st.text_area("Additional Instructions (Optional)")

# Generation and display
if st.button("Generate MCQs"):
    st.write("Generating...")  # Visual feedback
    try:
        # Generate questions
        result = client.qna_engine.generate_questions(
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty,
            additional_instructions=custom_hint
        )
        
        # Debug print to see what's being returned
        st.write("Debug - Result type:", type(result))
        
        # Display results
        st.subheader("Generated Question")
        
        # Handle different possible return types
        if isinstance(result, list):
            questions = result
        elif hasattr(result, 'questions'):
            questions = result.questions
        else:
            st.error("Unexpected result format")
            st.write("Debug - Result content:", result)
            questions = []
        
        # Only process if we have questions
        if questions:
            question = questions[0]  # Get first question
            with st.expander("Question 1", expanded=True):
                st.markdown(f"**Question:** {question.question}")
                st.write("**Options:**")
                for i, opt in enumerate(question.options, 1):
                    st.write(f"{i}. {opt}")
                st.success(f"**Correct Answer:** {question.answer}")
                if hasattr(question, 'explanation'):
                    st.info(f"**Explanation:** {question.explanation}")
        
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
        else:
            st.error("No questions were generated")
        
    except Exception as e:
        st.error(f"Generation failed: {str(e)}")
        st.write("Debug - Error details:", str(e))
        st.info("Please check your inputs and try again")

st.markdown("---")
st.caption("Note: Generated content should be reviewed by subject matter experts")
