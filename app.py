import sys
import os
import shutil

# Ensure UTF-8 output in Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv, set_key

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def is_valid_openai_key(key):
    if not key:
        return False
    k = key.strip()
    return k.startswith("sk-") and len(k) > 20 and not k.startswith("sk-your")

# Check which AI engines are available
print("=" * 60)
print("[LegalIQ] Initializing Multi-AI Intelligence Engine...")
if is_valid_openai_key(OPENAI_API_KEY):
    print("[OpenAI] Valid API Key loaded successfully!")
else:
    print("[OpenAI] No valid key found yet (use Settings in dashboard or add OPENAI_API_KEY=sk-... to .env)")

if GEMINI_API_KEY:
    print("[Gemini] API Key loaded successfully! (Gemini 3.8 Flash)")
else:
    print("[Gemini] Key not found in .env")
print("=" * 60)

# Optional lazy clients
def get_openai_client(custom_key=None):
    key = custom_key or os.getenv("OPENAI_API_KEY")
    if not is_valid_openai_key(key):
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key.strip())
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return None

def get_gemini_client(custom_key=None):
    key = custom_key or os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=key.strip())
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

# Default dossier loader from project directory
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_FILES = [
    "FIR_042_2023.txt.txt",
    "Complainant_Statement.txt.txt",
    "Witness_Statement_Suresh.txt.txt",
    "Accused_Dossier.txt.txt",
    "case.txt.txt"
]

def load_server_dossier():
    combined = ""
    for fname in DOSSIER_FILES:
        fpath = os.path.join(PARENT_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    doc_label = fname.replace(".txt.txt", ".txt")
                    combined += f"\n[DOCUMENT: {doc_label}]\n{f.read()}\n"
            except Exception:
                pass
    return combined

# Preload server dossier
SERVER_DOSSIER = load_server_dossier()
if SERVER_DOSSIER:
    print(f"[LegalIQ] Preloaded server case dossier ({len(SERVER_DOSSIER)} characters from disk).")

# Ensure logo image is in project directory
PICTURES_LOGO = r"C:\Users\Saran\Pictures\legal iq.jpeg"
LOCAL_LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.jpeg")
if os.path.exists(PICTURES_LOGO) and not os.path.exists(LOCAL_LOGO):
    try:
        shutil.copy2(PICTURES_LOGO, LOCAL_LOGO)
        print("[LegalIQ] Logo image copied to project folder: logo.jpeg")
    except Exception as e:
        pass

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = """
You are LegalIQ, an elite enterprise AI legal copilot and criminal intelligence reasoning assistant.

CRITICAL INSTRUCTIONS FOR EXACT & PRECISE ANSWERS:
1. DIRECT ANSWER FIRST: Always answer the user's question directly, factually, and concisely in the very first 1-2 sentences. Avoid long generic introductions or filler phrases. (For example: If asked "Who is the complainant?", immediately begin: "**The complainant is Shri M. Sundaram, Managing Director of Sri Balaji Garments Pvt Ltd.**" followed by details).
2. EXACT FACTS & FIGURES FROM DOSSIER: Quote exact verified figures and facts:
   - Consideration & Advance: Total contract consideration is ₹25,00,000/-. Advance paid is ₹15,00,000/- via RTGS on 15-June-2023.
   - Overseas Remittance: Rajesh Kumar remitted USD 16,500 (approx. ₹13,65,000) on 22-June-2023 via Telegraphic Transfer (TT) to Heidelberg Tech GMBH in Stuttgart, Germany.
   - Chennai Port Customs Delay: Shipment arrived at Chennai Port on 28-July-2023 under Bill of Entry scrutiny; detained due to revised automated customs regulations.
   - Meeting Discrepancy: Complainant swears dispute meeting occurred on 10-August-2023 at 10:30 AM at Corporate Office. Witness Suresh Natarajan (Accountant) swears meeting occurred on 10-August-2023 at 03:00 PM (15:00 hrs) inside Factory Premises.
   - Cheque Details: ICICI Bank Cheque No. 892110 for ₹5,00,000/- issued on 10-August-2023; returned dishonoured on 12-August-2023 for "Insufficient Funds".
   - Accused Background: Rajesh Kumar (Proprietor, Precision Machines India), zero criminal history (SCRB verified), surrendered passport No. Z-4829101, cooperated under Section 41A CrPC.
   - Legal Provisions: Registered under IPC 420 (Cheating) & 406 (Criminal Breach of Trust). Bail governed under CrPC 437 / BNSS 480. Precedents: Arnesh Kumar (2014), Satishchandra Ratanlal Shah (2019).
3. FORMATTING: Use bold text for key entities, dates, and amounts. Use bullet points for structured comparisons.
4. GENERAL & CHAT QUERIES: If the user says hello or asks broader legal/philosophical questions, respond intelligently, warmly, and helpfully.
"""

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/logo.jpeg")
@app.route("/logo")
@app.route("/legal%20iq.jpeg")
@app.route("/legal iq.jpeg")
def serve_logo():
    if os.path.exists(LOCAL_LOGO):
        return send_file(LOCAL_LOGO, mimetype="image/jpeg")
    elif os.path.exists(PICTURES_LOGO):
        return send_file(PICTURES_LOGO, mimetype="image/jpeg")
    return "", 404

@app.route("/api/status", methods=["GET"])
def status():
    has_openai = is_valid_openai_key(os.getenv("OPENAI_API_KEY"))
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
    return jsonify({
        "status": "online",
        "openai_available": has_openai,
        "gemini_available": has_gemini,
        "active_provider": "openai" if has_openai else ("gemini" if has_gemini else "none")
    })

@app.route("/api/dossier", methods=["GET"])
def get_dossier():
    docs = []
    for fname in DOSSIER_FILES:
        fpath = os.path.join(PARENT_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    label = fname.replace(".txt.txt", ".txt")
                    size_kb = os.path.getsize(fpath) / 1024
                    docs.append({
                        "name": label,
                        "size": f"{size_kb:.1f} KB",
                        "content": f.read()
                    })
            except Exception:
                pass
    return jsonify({"documents": docs})

@app.route("/api/save_key", methods=["POST"])
def save_key():
    try:
        data = request.json or {}
        provider = data.get("provider", "").lower()
        key_val = data.get("key", "").strip()
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        
        if provider == "openai":
            if is_valid_openai_key(key_val):
                os.environ["OPENAI_API_KEY"] = key_val
                set_key(env_path, "OPENAI_API_KEY", key_val)
                return jsonify({"status": "success", "message": "OpenAI API key saved successfully!"})
            else:
                return jsonify({"error": "Invalid OpenAI key format (must start with sk-)"}), 400
        elif provider == "gemini":
            os.environ["GEMINI_API_KEY"] = key_val
            set_key(env_path, "GEMINI_API_KEY", key_val)
            return jsonify({"status": "success", "message": "Gemini API key saved successfully!"})
        return jsonify({"error": "Unknown provider"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        user_message = data.get("message") or data.get("prompt", "")
        user_message = user_message.strip()
        case_context = data.get("context") or data.get("case_context", "")
        case_context = case_context.strip()
        requested_provider = data.get("provider", "auto").lower()
        requested_model = data.get("model", "")
        custom_api_key = data.get("apiKey", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # If client context is missing or too short, enrich with server-side dossier
        effective_context = case_context if len(case_context) > 100 else SERVER_DOSSIER

        # Construct prompt
        if effective_context:
            full_prompt = f"""=== VERIFIED CASE DOSSIER & EVIDENCE ===
{effective_context}

=== USER QUERY ===
{user_message}"""
        else:
            full_prompt = user_message

        # Determine which provider to use
        has_custom_openai = is_valid_openai_key(custom_api_key) if requested_provider == "openai" else False
        has_env_openai = is_valid_openai_key(os.getenv("OPENAI_API_KEY"))
        has_openai = has_custom_openai or has_env_openai

        has_gemini = bool(os.getenv("GEMINI_API_KEY")) or (bool(custom_api_key) if requested_provider == "gemini" else False)

        target_provider = requested_provider
        if target_provider == "auto":
            if has_openai:
                target_provider = "openai"
            elif has_gemini:
                target_provider = "gemini"
            else:
                target_provider = "gemini"

        response_text = ""
        model_used = ""
        provider_used = ""

        # --- 1. OPENAI PATH ---
        if target_provider == "openai":
            if has_openai:
                try:
                    client = get_openai_client(custom_api_key if has_custom_openai else None)
                    if client:
                        model_name = requested_model if requested_model and "gpt" in requested_model else "gpt-4o-mini"
                        completion = client.chat.completions.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": full_prompt}
                            ],
                            temperature=0.2
                        )
                        response_text = completion.choices[0].message.content
                        model_used = model_name
                        provider_used = "OpenAI"
                except Exception as e:
                    print(f"OpenAI call failed: {e}. Falling back to Gemini...")
                    if has_gemini:
                        target_provider = "gemini"
                    else:
                        return jsonify({"error": f"OpenAI error: {str(e)}"}), 500
            else:
                # No valid OpenAI key, fallback to Gemini
                if has_gemini:
                    target_provider = "gemini"
                else:
                    return jsonify({"error": "No valid OpenAI API key provided. Please configure your key in Settings."}), 400

        # --- 2. GEMINI PATH ---
        if target_provider == "gemini":
            client = get_gemini_client(custom_api_key if requested_provider == "gemini" else None)
            if not client:
                return jsonify({"error": "Gemini API key not configured. Add GEMINI_API_KEY to your .env file."}), 500

            # Model resolution (map old/invalid model names to gemini-3.8-flash)
            valid_models = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-flash-latest", "gemini-3.1-flash-lite"]
            if requested_model in valid_models:
                model_name = requested_model
            else:
                model_name = "gemini-3.8-flash"

            response_text = ""
            last_err = None
            import time

            # Try primary model up to 3 times (catches transient 503 or network glitches)
            for attempt in range(3):
                try:
                    gem_response = client.models.generate_content(
                        model=model_name,
                        contents=full_prompt,
                        config={"system_instruction": SYSTEM_PROMPT}
                    )
                    if gem_response and gem_response.text:
                        response_text = gem_response.text
                        model_used = model_name
                        provider_used = "Google Gemini"
                        break
                except Exception as e:
                    last_err = e
                    print(f"[LegalIQ] Gemini attempt {attempt+1} with {model_name} failed: {e}")
                    time.sleep(1)

            # If primary model failed, try modern fallbacks
            if not response_text:
                for fallback_m in ["gemini-3.5-flash", "gemini-flash-latest"]:
                    try:
                        print(f"[LegalIQ] Attempting fallback model: {fallback_m}...")
                        gem_response = client.models.generate_content(
                            model=fallback_m,
                            contents=full_prompt,
                            config={"system_instruction": SYSTEM_PROMPT}
                        )
                        if gem_response and gem_response.text:
                            response_text = gem_response.text
                            model_used = fallback_m
                            provider_used = "Google Gemini"
                            break
                    except Exception as e2:
                        last_err = e2
                        print(f"[LegalIQ] Fallback {fallback_m} failed: {e2}")

            if not response_text:
                return jsonify({"error": f"Gemini error: {str(last_err)}"}), 500

        return jsonify({
            "response": response_text,
            "html": response_text,
            "status": "success",
            "model": model_used,
            "provider": provider_used,
            "citation": f"{provider_used} ({model_used})"
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/<path:filename>")
def static_files(filename):
    if filename.startswith("api/"):
        return jsonify({"error": "Endpoint not found"}), 404
    return send_from_directory(".", filename)

if __name__ == "__main__":
    print("[LegalIQ] Multi-AI Server (OpenAI + Gemini) running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)