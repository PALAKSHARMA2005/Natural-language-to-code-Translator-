#app.py
import streamlit as st
import google.generativeai as genai
import ast
import re
from dotenv import load_dotenv
import os

# ----------------------------
# 🔑 Configure Gemini API
# ----------------------------
load_dotenv()  # Load environment variables from .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found in .env file")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)

# ----------------------------
# 🌟 Streamlit UI
# ----------------------------
st.set_page_config(page_title="Natural Language to Code Translator", layout="centered")
st.title("🧠 Natural Language ➡ Code Translator")
st.markdown("Convert natural language instructions into Python or JavaScript code using *Gemini 2.5 Flash* ⚡")

# ----------------------------
# 🧩 Helper Function — Clean Gemini Output
# ----------------------------
def clean_code_output(text: str) -> str:
    # Remove code block markers if present
    text = re.sub(r'^```\w*\n|```$', '', text)
    text = text.strip()
    unwanted_prefixes = [
        "Here is the code:",
        "Sure, here's the code:",
        "Sure! Here's the code:",
        "Output:",
        "Explanation:",
    ]
    for prefix in unwanted_prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    return text

# ----------------------------
# 🧠 Input + Session Handling
# ----------------------------
user_input = st.text_area(
    "💬 Enter your instruction:",
    placeholder="e.g., Create a function that returns the factorial of a number",
    key="user_input",
)

language = st.selectbox("Select target language:", ["Python", "JavaScript"], index=0, key="language")

# Initialize session state to remember generated code
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None

# ----------------------------
# 🚀 Generate Code Button
# ----------------------------
if st.button("Generate Code"):
    if user_input.strip():
        with st.spinner("Generating code..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""
                Convert the following instruction into {language} code:
                Instruction: {user_input}
                Output only valid, properly formatted {language} source code — no explanations or markdown.
                """
                response = model.generate_content(prompt)
                code_output = clean_code_output(response.text)
                st.session_state.generated_code = code_output  # ✅ Store in session

                st.subheader(f"✅ Generated {language} Code:")
                st.code(code_output, language.lower())

                # Validate syntax
                if language == "Python":
                    try:
                        ast.parse(code_output)
                        st.success("✅ No syntax errors detected.")
                    except SyntaxError as e:
                        st.error(f"❌ Syntax error detected: {e}")

            except Exception as e:
                st.error(f"⚠ Error: {e}")
    else:
        st.warning("Please enter an instruction first.")

# ----------------------------
# 💡 Explain This Code Button
# ----------------------------
if st.session_state.generated_code:
    if st.button("💡 Explain This Code"):
        with st.spinner("Analyzing code..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-pro")  # smarter model for explanations
                explain_prompt = f"Explain this {language} code in simple terms:\n{st.session_state.generated_code}"
                explain_response = model.generate_content(explain_prompt)
                st.info(explain_response.text.strip())
            except Exception as e:
                st.error(f"⚠ Error while explaining: {e}")

# ----------------------------
# 🎨 Footer
# ----------------------------
st.markdown("---\n*Built by Team AI Coders 🧩 | Powered by Google Gemini 2.5 Flash + Streamlit*")