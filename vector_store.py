import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class ChunkRetriever:
    """
    Handles retrieval of relevant SOP (Standard Operating Procedure) text chunks using FAISS and HuggingFace embeddings.

    This class builds or loads a FAISS vector store based on a given SOP text file,
    splits the text into manageable chunks, and allows querying for similar chunks.
    """

    def __init__(self, sop_path: str = "sop_docs.txt", chunk_size: int = 300, persist_dir: str = "faiss_index"):
        """
        Initializes the ChunkRetriever with a given SOP file path and configuration.

        Args:
            sop_path (str): Path to the SOP file to load and embed.
            chunk_size (int): The size of each text chunk to split into.
            persist_dir (str): Directory to load/save the FAISS index.
        """
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.persist_dir = persist_dir
        self.chunk_size = chunk_size
        self.sop_path = sop_path

        # Load existing index or create a new one
        if os.path.exists(persist_dir):
            self.vector_store = FAISS.load_local(
                persist_dir,
                self.embeddings,
                allow_dangerous_deserialization=True  # ✅ Trusted loading of serialized FAISS index
            )
        else:
            self.vector_store = self._create_and_save_index()

        # Create retriever object with similarity search
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2}
        )

    def _load_documents(self) -> List[Document]:
        """
        Loads and splits the SOP text file into individual document chunks.

        Returns:
            List[Document]: A list of chunked Document objects.
        """
        with open(self.sop_path, "r", encoding="utf-8") as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        chunks = splitter.split_text(text)
        return [Document(page_content=chunk, metadata={"source": f"chunk_{i}"}) for i, chunk in enumerate(chunks)]

    def _create_and_save_index(self) -> FAISS:
        """
        Creates a FAISS index from SOP document chunks and saves it locally.

        Returns:
            FAISS: The generated FAISS vector store.
        """
        documents = self._load_documents()
        vector_store = FAISS.from_documents(documents, self.embeddings)
        vector_store.save_local(self.persist_dir)
        return vector_store

    def search(self, query: str, top_k: int = 2) -> List[str]:
        """
        Searches for the top-K most relevant document chunks for a given query.

        Args:
            query (str): The search query or user question.
            top_k (int): The number of top relevant chunks to return.

        Returns:
            List[str]: A list of matching chunk texts.
        """
        results = self.retriever.invoke(query)
        return [doc.page_content for doc in results]
