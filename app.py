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
st.write("Generate multiple-choice questions for your educational needs.")

# Sidebar Configuration
with st.sidebar:
    st.header("Settings")
    topic = st.text_input("Topic", "Artificial Intelligence")
    num_questions = st.slider("Number of Questions", 1, 10, 5)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    
    use_cases = {
        "Exam Questions": {"difficulty": "Hard", "hint": "Include common misconceptions"},
        "Practice Quiz": {"difficulty": "Medium", "hint": "Add explanations"},
        "Custom": {"difficulty": difficulty, "hint": ""}
    }
    selected_case = st.selectbox("Use Case", list(use_cases.keys()))

# Apply use case presets
if selected_case != "Custom":
    difficulty = use_cases[selected_case]["difficulty"]
    custom_hint = use_cases[selected_case]["hint"]
else:
    custom_hint = st.text_area("Additional Instructions")

# Function to Generate MCQs
def generate_mcqs(client, topic, num_questions, difficulty, custom_hint):
    try:
        result = client.qna_engine.generate_questions(
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty,
            additional_instructions=custom_hint
        )
        return result
    except Exception as e:
        st.error(f"Error during generation: {e}")
        st.info("Please check your inputs, network, and try again later.")
        return None

# Generate and Display MCQs
if st.button("Generate MCQs"):
    with st.spinner(f"Creating {num_questions} {difficulty} questions about {topic}..."):
        result = generate_mcqs(client, topic, num_questions, difficulty, custom_hint)
        if result:
            st.subheader("Generated Questions")
            for i, question in enumerate(result.questions, 1):
                with st.expander(f"Question {i}", expanded=True):
                    st.markdown(f"**{question['question']}**")
                    st.write("Options:")
                    for opt in question.get("options", []):
                        st.write(f"- {opt}")
                    st.success(f"Answer: {question.get('answer', '')}")
                    if question.get("explanation"):
                        st.info(f"Explanation: {question['explanation']}")

            # Download feature
            if result.questions:
                st.download_button(
                    label="Download Questions",
                    data=json.dumps(result.__dict__, indent=2),
                    file_name="generated_questions.json",
                    mime="application/json"
                )

st.markdown("---")
st.caption("Ensure a subject matter expert reviews the generated content for accuracy and relevance.")
