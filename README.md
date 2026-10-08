# LegalIQ — AI Legal Assistant

LegalIQ is a web-based legal assistant designed to help users explore case information, ask questions about a case dossier, and access AI-powered legal analysis through supported AI providers.

> **Important:** LegalIQ is an informational support tool, not a substitute for advice from a qualified lawyer. Always verify legal facts, statutes, and citations before relying on them.

## Features

- **Web dashboard** served from `index.html`.
- **Flask API** for the application's backend.
- **AI provider support** for OpenAI and Google Gemini, when valid API keys are configured.
- **Service status endpoint** to check whether the backend is online and which provider is configured.
- **Case dossier support** for the text documents configured in `app.py`.
- **CORS enabled** for frontend/API communication.

## Tech Stack

- Python
- Flask
- Flask-CORS
- python-dotenv
- OpenAI Python SDK (optional)
- Google Gen AI SDK (optional)
- Gunicorn (for production hosting)

## Project Files

- `app.py` — Flask server and API routes.
- `index.html` — frontend dashboard.
- `logo.jpeg` — application logo.
- `generate_sample_pdfs.py` — script for generating sample PDF files.

## Run Locally

### 1. Install Python

Use a supported Python 3 version.

### 2. Install dependencies

```bash
pip install flask flask-cors python-dotenv openai google-genai gunicorn
```

### 3. Configure environment variables

Create a local `.env` file in the project directory:

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_google_gemini_api_key
```

You can configure either provider or both. Keep real API keys private; **never commit `.env` or publish API keys**. Add `.env` to `.gitignore`.

### 4. Start the application

```bash
python app.py
```

Open the local address printed by Flask in your browser.

## Deploy on Render

Create a new **Web Service** connected to this GitHub repository.

- **Runtime:** Python
- **Build command:**
  ```bash
  pip install flask flask-cors python-dotenv openai google-genai gunicorn
  ```
- **Start command:**
  ```bash
  gunicorn app:app --bind 0.0.0.0:$PORT
  ```

In Render's **Environment** settings, add `OPENAI_API_KEY` and/or `GEMINI_API_KEY` as secret environment variables. Do not place secrets in the README or source code.

## API Status Check

After starting the server, visit:

```
/api/status
```

The response reports whether the service is online and whether OpenAI or Gemini is configured.

## Case Documents

The backend looks for these dossier text files relative to the parent directory of the application:

- `FIR_042_2023.txt.txt`
- `Complainant_Statement.txt.txt`
- `Witness_Statement_Suresh.txt.txt`
- `Accused_Dossier.txt.txt`
- `case.txt.txt`

Ensure any documents required by your deployment are included in the project at the expected paths. Only upload documents you are authorized to share, and remove confidential or personal information before publishing a repository.

## Security Notes

- Keep API keys in local environment variables or Render's secret environment settings.
- Add `.env` to `.gitignore` and remove it from version control.
- If a real API key has already been pushed to a public repository, revoke it and create a replacement.
- Avoid publishing confidential case files, personal data, or privileged legal material.

## Disclaimer

LegalIQ provides AI-generated information for general assistance. It may produce inaccurate or incomplete results and does not establish an attorney-client relationship. Consult a qualified legal professional for case-specific advice.
