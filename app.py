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

# App Configuration
use_cases = {
    "Exam Questions": {
        "difficulty": "Hard",
        "hint": "Include common misconceptions as distractors"
    },
    "Practice Quiz": {
        "difficulty": "Medium",
        "hint": "Provide detailed explanations for answers"
    },
    "Custom": {"difficulty": None, "hint": None}
}

# Streamlit UI
st.title("🎓 AI-Powered MCQ Generator")
st.caption("Leverage DeepSeek's AI to create educational multiple-choice questions")

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    topic = st.text_input("Topic", "Artificial Intelligence", help="Enter the subject matter for your questions")
    num_questions = st.slider("Number of Questions", 1, 20, 5, 
                            help="Choose how many questions to generate")
    selected_case = st.selectbox("Question Type", list(use_cases.keys()),
                               help="Select a preset configuration or customize your own")

# Dynamic Configuration Section
with st.sidebar:
    if selected_case != "Custom":
        preset = use_cases[selected_case]
        difficulty = preset["difficulty"]
        custom_hint = preset["hint"]
        
        st.subheader("Preset Configuration")
        st.info(f"**Difficulty Level:** {difficulty}")
        st.info(f"**Generation Strategy:** {custom_hint}")
    else:
        st.subheader("Custom Settings")
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        custom_hint = st.text_area("Special Instructions", 
                                 placeholder="E.g.: 'Focus on historical dates', 'Include diagram-based questions'")

# Question Generation Function
def generate_questions():
    if not topic.strip():
        st.error("Please enter a valid topic")
        return None
    
    try:
        with st.spinner(f"🧠 Generating {num_questions} {difficulty.lower()} questions about {topic}..."):
            result = client.qna_engine.generate_questions(
                topic=topic,
                num_questions=num_questions,
                difficulty=difficulty,
                additional_instructions=custom_hint
            )
            return result.questions if hasattr(result, 'questions') else []
    except Exception as e:
        st.error(f"Generation failed: {str(e)}")
        return None

# Main Interaction Flow
if st.button("Generate Questions", type="primary", use_container_width=True):
    questions = generate_questions()
    
    if questions:
        st.success(f"Successfully generated {len(questions)} questions!")
        st.divider()
        
        # Display Questions
        for i, q in enumerate(questions, 1):
            with st.expander(f"Question #{i}", expanded=True):
                st.markdown(f"#### {q['question']}")
                
                cols = st.columns(2)
                with cols[0]:
                    st.write("**Options:**")
                    for option in q.get('options', []):
                        st.write(f"- {option}")
                
                with cols[1]:
                    st.success(f"**Correct Answer:** {q.get('answer', '')}")
                    if q.get('explanation'):
                        st.info(f"**Explanation:** {q['explanation']}")
        
        # Download Feature
        json_data = json.dumps(
            [{"question": q["question"], 
              "options": q.get("options", []), 
              "answer": q.get("answer", ""), 
              "explanation": q.get("explanation", "")} 
             for q in questions],
            indent=2
        )
        
        st.download_button(
            label="📥 Download Questions",
            data=json_data,
            file_name=f"MCQ_{topic.replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )

# Quality Assurance Note
st.markdown("---")
st.caption("⚠️ Always verify generated content with subject matter experts before use in formal assessments.")
