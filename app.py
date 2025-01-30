import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_deepseek import ChatDeepSeek

def main():
    st.set_page_config(
        page_title="Advanced MCQ Generator",
        page_icon="🧠",
        layout="centered"
    )
    
    st.title("📚 AI-Powered MCQ Generator")
    st.markdown("Generate advanced multiple-choice questions using DeepSeek AI")
    
    # Initialize models and client
    llm = ChatDeepSeek(model="deepseek-chat")
    deepseek_config = LLMConfig(custom_model=llm)
    client = Educhain(config=deepseek_config)
    
    # Input parameters
    with st.sidebar:
        st.header("Configuration")
        topic = st.text_input("Topic", value="AI Agents")
        num_questions = st.number_input("Number of Questions", 
                                      min_value=1, max_value=10, value=3)
        difficulty = st.select_slider("Difficulty Level", 
                                    options=["Easy", "Medium", "Hard"], value="Hard")
        custom_instructions = st.text_area("Custom Instructions", 
                                         value="Include recent discoveries")
    
    # Main content area
    if st.button("✨ Generate Questions", use_container_width=True):
        with st.spinner("Generating advanced MCQs..."):
            try:
                advanced_mcq = client.qna_engine.generate_questions(
                    topic=topic,
                    num=num_questions,
                    question_type="Multiple Choice",
                    difficulty_level=difficulty,
                    custom_instructions=custom_instructions
                )
                
                st.success("Successfully generated questions!")
                st.divider()
                
                # Display results in tabs
                tab1, tab2 = st.tabs(["Structured Format", "JSON Format"])
                
                with tab1:
                    st.subheader("Structured Questions")
                    st.write(advanced_mcq.show())
                
                with tab2:
                    st.subheader("JSON Output")
                    st.json(advanced_mcq.json())
            
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")

if __name__ == "__main__":
    main()
