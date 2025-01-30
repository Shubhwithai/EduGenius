# In the question generation section:
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
                    
                    # Display options with letters
                    options = qna.options
                    for j, option in enumerate(options, 1):
                        st.markdown(f"{chr(64+j)}. {option}")
                    
                    # Check response structure
                    if hasattr(qna, 'correct_option'):
                        # If using index-based correct answer
                        correct_answer = options[qna.correct_option-1]
                        st.success(f"**Correct Answer:** {correct_answer}")
                    elif hasattr(qna, 'answer'):
                        # If using direct answer text
                        st.success(f"**Correct Answer:** {qna.answer}")
                    else:
                        st.error("Could not find correct answer in response")
                    
                    if qna.explanation:
                        st.info(f"**Explanation:** {qna.explanation}")
