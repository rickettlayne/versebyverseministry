"""
RAG-based chatbot that uses PDF content to answer questions
"""

import os
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import config
from pdf_processor import PDFProcessor


# Load environment variables
load_dotenv()


class VBVMChatbot:
    """Chatbot that answers questions based on PDF content"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the chatbot
        
        Args:
            openai_api_key: OpenAI API key (optional, can use env variable)
        """
        # Set API key
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY') or config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file or pass as parameter")
        
        os.environ['OPENAI_API_KEY'] = self.api_key
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
        self.vector_store = None
        self.qa_chain = None
        
        # Create vector database directory
        os.makedirs(config.VECTOR_DB_DIR, exist_ok=True)
    
    def load_pdfs(self, reindex: bool = False):
        """
        Load and index PDF documents
        
        Args:
            reindex: If True, re-index all documents even if database exists
        """
        # Check if vector database already exists
        db_path = os.path.join(config.VECTOR_DB_DIR, "chroma.sqlite3")
        
        if os.path.exists(db_path) and not reindex:
            print("Loading existing vector database...")
            self._load_vector_store()
            return
        
        print("Indexing PDF documents...")
        
        # Process PDFs
        processor = PDFProcessor()
        documents = processor.process_all_pdfs()
        
        if not documents:
            raise ValueError("No PDF documents found. Run the scraper first.")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
        
        texts = []
        metadatas = []
        
        for doc in documents:
            chunks = text_splitter.split_text(doc['content'])
            texts.extend(chunks)
            metadatas.extend([{
                'source': doc['filename'],
                'filepath': doc['filepath']
            } for _ in chunks])
        
        print(f"Created {len(texts)} text chunks from {len(documents)} documents")
        
        # Create vector store
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            collection_name=config.COLLECTION_NAME,
            persist_directory=config.VECTOR_DB_DIR
        )
        
        print("Vector database created and saved")
        self._initialize_qa_chain()
    
    def _load_vector_store(self):
        """Load existing vector store"""
        self.vector_store = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=config.VECTOR_DB_DIR
        )
        self._initialize_qa_chain()
    
    def _initialize_qa_chain(self):
        """Initialize the QA chain"""
        # Create custom prompt
        template = """You are a knowledgeable assistant for Verse by Verse Ministry.
You answer questions based ONLY on the content from the ministry's PDF documents.

If the answer is not in the provided context, say "I don't have enough information from the available documents to answer that question."
Do not make up information or use knowledge outside of the provided context.

Context from documents:
{context}

Question: {question}

Answer:"""
        
        QA_PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Initialize language model
        llm = ChatOpenAI(
            model_name=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": config.TOP_K_RESULTS}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_PROMPT}
        )
    
    def ask(self, question: str, show_sources: bool = True) -> str:
        """
        Ask a question to the chatbot
        
        Args:
            question: The question to ask
            show_sources: Whether to show source documents
            
        Returns:
            The answer from the chatbot
        """
        if not self.qa_chain:
            raise ValueError("Chatbot not initialized. Call load_pdfs() first.")
        
        result = self.qa_chain({"query": question})
        
        answer = result['result']
        
        if show_sources and result.get('source_documents'):
            sources = set()
            for doc in result['source_documents']:
                if 'source' in doc.metadata:
                    sources.add(doc.metadata['source'])
            
            if sources:
                answer += f"\n\nSources: {', '.join(sources)}"
        
        return answer
    
    def chat(self):
        """Interactive chat mode"""
        print("\n" + "="*60)
        print("Verse by Verse Ministry Chatbot")
        print("="*60)
        print("Ask questions about the ministry's teachings.")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("="*60 + "\n")
        
        while True:
            try:
                question = input("\nYou: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not question:
                    continue
                
                print("\nAssistant: ", end="")
                answer = self.ask(question)
                print(answer)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")


if __name__ == "__main__":
    # Example usage
    chatbot = VBVMChatbot()
    chatbot.load_pdfs()
    chatbot.chat()
