import streamlit as st
import textstat
import language_tool_python

# Initialize language tool (no Java needed if using offline mode)
tool = language_tool_python.LanguageTool('en-US')  # Optional: offline mode

st.title("Toughest AI Essay Grader")

# --- User input ---
essay = st.text_area("Paste your essay here:", height=300)

if st.button("Grade Essay"):
    if not essay.strip():
        st.warning("Please enter an essay first!")
    else:
        # --- Grade based on readability ---
        flesch_score = textstat.flesch_reading_ease(essay)
        grade_level = textstat.text_standard(essay, float_output=False)

        # --- Constructive feedback ---
        matches = tool.check(essay)
        feedback = [f"{m.ruleId}: {m.message}" for m in matches]

        # --- Display results ---
        st.subheader("📊 Grading Results")
        st.write(f"**Flesch Reading Ease Score:** {flesch_score}")
        st.write(f"**Estimated Grade Level:** {grade_level}")

        st.subheader("📝 Constructive Feedback")
        if feedback:
            for i, f in enumerate(feedback, 1):
                st.write(f"{i}. {f}")
        else:
            st.write("No issues detected — excellent work!")
