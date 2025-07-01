# models/llm_router.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import only Gemini and Flan backends
from models.llm_flan import run_llm as run_flan
from models.llm_gemini import run_llm as run_gemini

# === Read backend preference from .env ===
LLM_BACKEND = os.getenv("LLM_BACKEND", "flan").strip().lower()

def run_llm(context: str, tools: str, question: str, refine_question: bool = False) -> str:
    """
    Routes the LLM inference request to the selected backend model.

    Supported backends:
        - "gemini" : Google Gemini API (cloud inference)
        - "flan"   : Flan-T5 base model (local inference)

    Args:
        context (str): SOP or retrieved context.
        tools (str): Aggregated tool results.
        question (str): Original user query.
        refine_question (bool): Whether to refine the question using retrieval chain.

    Returns:
        str: Generated answer from selected LLM backend.
    """
    print(f"🔍 [LLM Router] Using backend: {LLM_BACKEND}")

    if LLM_BACKEND == "gemini":
        return run_gemini(context, tools, question, refine_question)
    elif LLM_BACKEND == "flan":
        return run_flan(context, tools, question, refine_question)
    else:
        return f"❌ Unsupported LLM_BACKEND: {LLM_BACKEND}. Please choose from 'flan' or 'gemini'."
