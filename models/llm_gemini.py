import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Truncation limits for long input
MAX_CONTEXT_CHARS = 1000
MAX_TOOL_CHARS = 600

# Load retrieval and synthesis prompts
with open("prompts/retrieval.txt", "r", encoding="utf-8") as f:
    retrieval_prompt = PromptTemplate.from_template(f.read())

with open("prompts/synthesis.txt", "r", encoding="utf-8") as f:
    synthesis_prompt = PromptTemplate.from_template(f.read())
    
    

def gemini_invoke(prompt: str) -> str:
    """
    Invokes the Gemini model with a given text prompt.

    Args:
        prompt (str): The input text prompt.

    Returns:
        str: The model's response, or an error/warning message.
    """
    try:
        response = model.generate_content(prompt)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            return parts[0].text.strip() if parts else "⚠️ Empty response."
        return "⚠️ No output from Gemini."
    except Exception as e:
        return f"⚠️ Gemini error: {e}"
    

def gemini_wrapper_for_synthesis(inputs: dict) -> str:
    """
    Formats the synthesis prompt using provided inputs and invokes Gemini.

    Args:
        inputs (dict): A dictionary with 'context', 'tools', and 'question'.

    Returns:
        str: Synthesized output from Gemini.
    """
    prompt = synthesis_prompt.format(**inputs)
    return gemini_invoke(prompt)



def gemini_wrapper_for_retrieval(inputs: dict) -> str:
    """
    Formats the retrieval prompt using provided inputs and invokes Gemini.

    Args:
        inputs (dict): A dictionary with 'context' and 'question'.

    Returns:
        str: Refined or rephrased question from Gemini.
    """
    prompt = retrieval_prompt.format(**inputs)
    return gemini_invoke(prompt)



# Create LangChain Runnable chains
synthesis_chain = RunnableLambda(gemini_wrapper_for_synthesis)
retrieval_chain = RunnableLambda(gemini_wrapper_for_retrieval)



def run_llm(context: str, tools: str, question: str, refine_question: bool = False) -> str:
    """
    Executes the Gemini model using retrieval-augmented generation.

    Args:
        context (str): Retrieved SOP chunks for the query.
        tools (str): Tool outputs related to the query.
        question (str): User's original question.
        refine_question (bool, optional): Whether to refine the question before answering. Defaults to False.

    Returns:
        str: Final synthesized answer from Gemini.
    """
    try:
        # Optionally refine the question
        if refine_question:
            question = retrieval_chain.invoke({
                "context": context.strip()[:MAX_CONTEXT_CHARS],
                "question": question.strip()
            }).strip()

        # Prepare prompt input
        inputs = {
            "context": context.strip()[:MAX_CONTEXT_CHARS],
            "tools": tools.strip()[:MAX_TOOL_CHARS],
            "question": question.strip()
        }

        # Invoke Gemini for synthesis
        response = synthesis_chain.invoke(inputs).strip()

        # Extract 'Final Answer:' if present
        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()

        return response or "⚠️ I couldn't find a clear answer."

    except Exception as e:
        return f"⚠️ Gemini error: {e}"
