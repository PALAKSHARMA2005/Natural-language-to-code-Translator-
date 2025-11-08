# Natural Language to Code Translator

A Streamlit web application that converts natural language instructions into Python or JavaScript code using Google's Gemini 2.5 Flash AI model.

## Features

- Convert natural language to Python or JavaScript code
- Syntax validation for Python code
- Code explanation feature
- Clean and intuitive user interface
- Powered by Google Gemini 2.5 Flash AI

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
Replace the `GEMINI_API_KEY` in `app.py` with your API key

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your natural language instruction in the text area
2. Select the target programming language (Python or JavaScript)
3. Click "Generate Code" to convert your instruction into code
4. Use "Explain This Code" to get a detailed explanation of the generated code

## Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Regular Expressions (re)
- Abstract Syntax Trees (ast)