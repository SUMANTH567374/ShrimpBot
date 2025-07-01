🦐 ShrimpBot – Hatchery SOP Assistant

ShrimpBot is an interactive terminal-based AI assistant that answers questions related to shrimp hatchery Standard Operating Procedures (SOPs). It combines retrieval-augmented generation (RAG), domain-specific tools, and LLMs (Flan-T5 or Gemini) to provide accurate and actionable responses.

📌 Features

🔍 Contextual SOP Retrieval using FAISS & MiniLM

⚙️ Keyword-based Tool Routing for specialized insights

🧠 LLM-Powered Response Synthesis (local or cloud)

🔁 Supports Flan-T5 (local) and Gemini (cloud) inference

💬 Easy-to-use CLI chatbot interface

🗂️ Project Structure


ShrimpBot/
├── main.py                     # CLI entry point
├── llm_synthesis.py           # Combines SOP, tools, and question to generate response
├── vector_store.py            # Handles SOP chunking and FAISS vector search
├── tools/                     # Custom tool functions (e.g., water quality, temperature)
├── tool_registry.json         # Maps tool names to their function paths
├── models/
│   ├── llm_router.py          # Routes to Flan or Gemini backend
│   ├── llm_flan.py            # Local Flan-T5 inference
│   ├── llm_gemini.py          # Cloud-based Gemini inference
├── prompts/
│   ├── retrieval.txt          # Prompt for optional question refinement
│   └── synthesis.txt          # Prompt template for final answer
└── sop_docs.txt               # SOP knowledge base text file

🚀 How It Works

User Query: You ask a question in the terminal.

main.py: Handles input/output and calls the generation function.

llm_synthesis.py:

Retrieves relevant SOP chunks from FAISS.

Calls relevant tools based on keywords.

Sends all inputs to the selected LLM backend.

LLM Inference:

Either models/llm_flan.py (local) or models/llm_gemini.py (cloud).

Response: The synthesized answer is displayed with timing info.


🧠 Model Selection and Evaluation Note

For local inference, I used google/flan-t5-base, suitable for my system (8GB RAM, Intel i3 11th Gen @ 3.00GHz).

I tested larger models like Mistral 7B and Microsoft Phi-2, but they couldn’t run due to hardware constraints.

To validate both functionality and quality, I integrated Gemini as a cloud-based LLM backend.

Both Flan-T5 and Gemini were tested to ensure smooth end-to-end performance.

💡 Future Improvements

🔄 Add feedback loops and evaluation metrics

🚀 Use 4-bit or 8-bit quantized models to run larger LLMs locally

🧠 Consider fine-tuning Flan-T5 on domain-specific data for better accuracy

🖥️ Upgrade to 16–32 GB RAM + GPU to handle larger models efficiently

