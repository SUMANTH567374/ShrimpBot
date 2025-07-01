from models.llm_router import run_llm
from vector_store import ChunkRetriever
from agent import ShrimpBotAgent 

retriever = ChunkRetriever()
agent = ShrimpBotAgent()

def generate_answer(query: str, top_k_chunks: int = 2) -> str:
    """
    Synthesizes an answer by retrieving relevant SOP chunks and tool outputs,
    and sends them to the selected LLM backend.

    Args:
        query (str): User's question.
        top_k_chunks (int): Number of top relevant chunks to retrieve.

    Returns:
        str: Synthesized answer from the LLM.
    """
    # Retrieve vector store context
    sop_chunks = retriever.search(query, top_k=top_k_chunks)
    sop_context = "\n\n".join(chunk.strip() for chunk in sop_chunks if chunk.strip())

    # Route to tools
    tools_output = agent.route_to_tools(query)
    tools_context = "\n".join(tools_output).strip()

    #Fallback message
    if not sop_context and not tools_context:
        return "⚠️ Sorry, I couldn't find relevant hatchery SOP information for your question."

    # Final LLM synthesis
    return run_llm(
        context=sop_context,
        tools=tools_context,
        question=query
    )
