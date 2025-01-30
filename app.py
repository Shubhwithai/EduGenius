import streamlit as st
import json
from typing import Optional, List, Dict

# Page configuration and title
st.set_page_config(page_title="MCQ Generator", page_icon="🎯", layout="wide")
st.title("📚 Multiple Choice Question Generator")

# Session state initialization
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar for inputs
with st.sidebar:
    st.header("Question Parameters")
    topic = st.text_input("Topic", placeholder="Enter the subject or topic")
    num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5)
    
    # Preset vs Custom Settings
    use_preset = st.checkbox("Use Preset Configuration")
    
    if use_preset:
        preset = st.selectbox(
            "Select Preset",
            ["Academic", "Professional Certification", "Practice Test"]
        )
        
        # Define preset configurations
        presets = {
            "Academic": {
                "difficulty": "Medium",
                "hint": "Focus on fundamental concepts and learning objectives"
            },
            "Professional Certification": {
                "difficulty": "Hard",
                "hint": "Include practical scenarios and industry-specific content"
            },
            "Practice Test": {
                "difficulty": "Easy",
                "hint": "Provide detailed explanations and progressive difficulty"
            }
        }
        
        difficulty = presets[preset]["difficulty"]
        custom_hint = presets[preset]["hint"]
        
        st.subheader("Preset Configuration")
        st.info(f"**Difficulty Level:** {difficulty}")
        st.info(f"**Generation Strategy:** {custom_hint}")
    else:
        st.subheader("Custom Settings")
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        custom_hint = st.text_area(
            "Special Instructions",
            placeholder="E.g.: 'Focus on historical dates', 'Include diagram-based questions'"
        )

def generate_questions() -> Optional[List[Dict]]:
    """Generate questions with error handling and validation."""
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

def display_questions(questions: List[Dict]):
    """Display questions with proper formatting and validation."""
    st.success(f"Successfully generated {len(questions)} questions!")
    st.divider()
    
    for i, q in enumerate(questions, 1):
        with st.expander(f"Question #{i}", expanded=True):
            if not isinstance(q, dict):
                st.warning("Invalid question format")
                continue
            
            # Ensure required fields exist
            q.setdefault('question', 'Question text missing')
            q.setdefault('options', [])
            q.setdefault('answer', 'No answer provided')
            
            st.markdown(f"**{q['question']}**")
            
            if q['options']:
                for j, option in enumerate(q['options'], 1):
                    st.markdown(f"{j}. {option}")
            
            with st.expander("View Answer"):
                st.markdown(f"**Answer:** {q['answer']}")
                if 'explanation' in q:
                    st.markdown(f"**Explanation:** {q['explanation']}")

# Main interaction flow
if st.button("Generate Questions", type="primary", use_container_width=True):
    questions = generate_questions()
    
    if questions:
        display_questions(questions)
        
        # Download feature
        json_data = json.dumps(
            [{
                "question": q["question"],
                "options": q.get("options", []),
                "answer": q.get("answer", ""),
                "explanation": q.get("explanation", "")
            } for q in questions],
            indent=2
        )
        
        st.download_button(
            label="📥 Download Questions",
            data=json_data,
            file_name=f"MCQ_{topic.replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        # Store in history
        st.session_state.history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "questions": questions
        })

# Display generation history
if st.session_state.history:
    with st.expander("Generation History"):
        for entry in st.session_state.history:
            st.markdown(f"**{entry['topic']}** - {entry['timestamp']}")

# Quality assurance note
st.markdown("---")
st.caption("⚠️ Always verify generated content with subject matter experts before use in formal assessments.")
