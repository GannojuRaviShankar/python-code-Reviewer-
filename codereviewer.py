import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyAi9cFdx3psNuBhKlqNIQxpWg1QjCWVDbI")
sys_prompt = """
You are a helpful Python tutor. You can resolve queries related to Python code, review it, and provide feedback on potential 
bugs along with suggestions for fixes. If the code is in any other language, you will ask whether the user wants it converted into Python. 
The application should be user-friendly, efficient, and provide accurate bug reports and fixed code snippets. If someone asks queries that 
are not relevant to Python, politely tell them to ask relevant queries only.
"""

# Initialize the Generative Model
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-exp", 
                              system_instruction=sys_prompt)

# Streamlit UI
st.title("Python Code AI-Reviewer")
st.write("Enter your Python code below to get feedback on potential bugs and suggestions for improvements.")

# Text area for user input
user_prompt = st.text_area("Enter your code:")

# Simple regex pattern to check if the code looks like Python
def looks_like_python(code):
    python_keywords = ["def ", "import ", "print(", "return ", "for ", "while ", "if ", "else:", "elif "]
    return any(keyword in code for keyword in python_keywords)

if st.button("Review-Code"):
    if user_prompt.strip():
        if looks_like_python(user_prompt):
            response = model.generate_content(user_prompt)
            st.markdown(response.text)
        else:
            st.warning(f"This might not be Python code. Do you want me to change it into Python?")
            if st.button("Convert to Python"):
                conversion_prompt = f"Convert the following code into Python:\n\n{user_prompt}"
                conversion_response = model.generate_content(conversion_prompt)
                st.markdown("### Converted Python Code:")
                st.code(conversion_response.text, language="python")
    else:
        st.warning("Please enter some code before submitting.")
