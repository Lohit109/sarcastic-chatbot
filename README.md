# SnarkBot 🙃

A local AI chatbot that combines practical advice with playful sarcasm. Built with Python, Streamlit, and Ollama.

## Features

- **Adjustable tone:** Choose Gentle, Sarcastic, or Roast.
- **Chat mode:** Ask questions and get useful responses with a little attitude.
- **10-minute challenge:** Turn a task into a concrete mission with a clear completion condition.
- **Local inference:** Generate responses through Ollama without a cloud LLM API key.

## Tech Stack

- Python
- Streamlit
- Ollama
- Qwen3 4B Instruct

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Lohit109/sarcastic-chatbot.git
cd sarcastic-chatbot
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Ollama

Install Ollama from https://ollama.com and start it.

Download the model:

```bash
ollama pull qwen3:4b-instruct
```

Make sure the `MODEL` value in `app.py` matches the downloaded model.

### 5. Start SnarkBot

```bash
streamlit run app.py
```

Open the local URL printed in your terminal.

## Example Prompts

- “Explain Python decorators with a simple example.”
- “I keep planning my project instead of building it.”
- “Give me a 10-minute challenge to start writing my README.”

## Project Structure

```text
sarcastic-chatbot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

## Limitations

- Ollama and the model must be available on the machine running the app.
- Response speed depends on your hardware.
- AI responses can be inaccurate.
- The challenge mode suggests tasks; it does not run a timer or verify completion.
