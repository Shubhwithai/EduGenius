import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_deepseek import ChatDeepSeek

# Initialize Educhain with DeepSeek
@st.cache_resource
def initialize_llm():
    llm = ChatDeepSeek(model="deepseek-chat")
    return Educhain(llm_config=LLMConfig(custom_model=llm))

client = initialize_llm()

# Streamlit UI
st.title("🧠 AI MCQ Generator with DeepSeek")
st.write("Generate advanced multiple-choice questions for various educational use cases")

# Use Case Selection
use_case = st.sidebar.selectbox("Select Use Case", [
    "Academic Exams",
    "Student Practice",
    "Corporate Training",
    "Research Evaluation",
    "Custom Scenario"
])

# Configuration Panel
st.sidebar.header("Configuration")
topic = st.sidebar.text_input("Topic", "AI Agents")
num_questions = st.sidebar.slider("Number of Questions", 1, 10, 3)
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
custom_instructions = st.sidebar.text_area("Custom Instructions", "Include recent discoveries")

# Use Case Descriptions
use_cases = {
    "Academic Exams": {
        "desc": "Generate high-quality exam questions with detailed distractors",
        "params": {"difficulty": "Hard", "custom": "Include common misconceptions"}
    },
    "Student Practice": {
        "desc": "Create practice questions with instant feedback capability",
        "params": {"difficulty": "Medium", "custom": "Include step-by-step explanations"}
    },
    "Corporate Training": {
        "desc": "Develop technical assessments for employee training",
        "params": {"difficulty": "Hard", "custom": "Focus on real-world applications"}
    },
    "Research Evaluation": {
        "desc": "Create evaluation metrics for research comprehension",
        "params": {"difficulty": "Hard", "custom": "Include recent publications"}
    },
    "Custom Scenario": {
        "desc": "Configure your own parameters for specialized needs",
        "params": {}
    }
}

# Display selected use case description
st.header(f"Use Case: {use_case}")
st.write(use_cases[use_case]["desc"])

# Apply use case presets
if use_case != "Custom Scenario":
    preset = use_cases[use_case]["params"]
    difficulty = preset["difficulty"]
    custom_instructions = preset["custom"]

# Generate Questions
if st.button("Generate Questions"):
    with st.spinner("Generating advanced MCQs..."):
        try:
            mcqs = client.qna_engine.generate_questions(
                topic=topic,
                num=num_questions,
                question_type="Multiple Choice",
                difficulty_level=difficulty,
                custom_instructions=custom_instructions
            )
            
            st.success("Generated Questions:")
            for i, qna in enumerate(mcqs.questions, 1):
                with st.expander(f"Question {i}: {qna.question}", expanded=True):
                    st.markdown(f"**Question:** {qna.question}")
                    for j, option in enumerate(qna.options, 1):
                        st.markdown(f"{j}. {option}")
                    st.success(f"**Correct Answer:** {qna.correct_answer}")
                    if qna.explanation:
                        st.info(f"**Explanation:** {qna.explanation}")
            
            st.download_button(
                label="Download as JSON",
                data=mcqs.json(),
                file_name="generated_questions.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")

# Use Case Examples
st.sidebar.header("Example Use Cases")
st.sidebar.markdown("""
1. **University Professors**: Create exam banks
2. **EdTech Platforms**: Generate quiz content
3. **HR Departments**: Technical screening tests
4. **Researchers**: Validate comprehension of papers
5. **Students**: Create study guides
""")
