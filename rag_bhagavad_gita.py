import os
import pandas as pd
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Dict, Tuple
from google.colab import userdata  # Added for Colab
import warnings
warnings.filterwarnings('ignore')

class BhagavadGitaRAG:
    def __init__(self, csv_file_path: str):
        """Initialize the RAG system for Bhagavad Gita."""
        self.csv_file_path = csv_file_path
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Configure Gemini API - Modified for Colab
        try:
            # Get API key from Colab secrets
            api_key = userdata.get('GOOGLE_API_KEY')
            genai.configure(api_key=api_key)
            print("✅ API key loaded from Colab secrets successfully!")
        except Exception as e:
            print(f"❌ Error loading API key: {e}")
            print("Please make sure you've added GOOGLE_API_KEY to Colab secrets")
            raise
            
        self.llm_model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            is_persistent=True
        ))
        
        self.collection_name = "bhagavad_gita_verses"
        self.collection = None
        self.df = None
        
        # Load and process data
        self.load_data()
        self.setup_vector_store()
    
    def load_data(self):
        """Load the Bhagavad Gita dataset."""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            print(f"Loaded {len(self.df)} verses from the dataset")
            
            # Display dataset info
            print("\nDataset columns:", self.df.columns.tolist())
            print("Sample verse:")
            print(f"Chapter: {self.df.iloc[0]['chapter_title']}")
            print(f"Verse: {self.df.iloc[0]['chapter_verse']}")
            print(f"Translation: {self.df.iloc[0]['translation'][:100]}...")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def create_enhanced_text(self, row):
        """Create enhanced text for better retrieval."""
        return f"""Chapter: {row['chapter_title']}
Verse: {row['chapter_verse']}
Translation: {row['translation']}
Context: This verse from the Bhagavad Gita discusses spiritual wisdom and philosophical teachings."""
    
    def setup_vector_store(self):
        """Setup ChromaDB vector store with embeddings."""
        try:
            # Delete existing collection if it exists
            try:
                self.client.delete_collection(name=self.collection_name)
            except:
                pass
            
            # Create new collection
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            print("Creating embeddings for all verses...")
            
            # Prepare documents
            documents = []
            metadatas = []
            ids = []
            
            for idx, row in self.df.iterrows():
                enhanced_text = self.create_enhanced_text(row)
                documents.append(enhanced_text)
                
                metadatas.append({
                    "chapter_number": row['chapter_number'],
                    "chapter_title": row['chapter_title'],
                    "verse": row['chapter_verse'],
                    "translation": row['translation']
                })
                
                ids.append(f"verse_{idx}")
            
            # Create embeddings
            embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Successfully created vector store with {len(documents)} verses")
            
        except Exception as e:
            print(f"Error setting up vector store: {e}")
            raise
    
    def retrieve_relevant_verses(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant verses based on query."""
        try:
            # Create query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=top_k
            )
            
            # Format results
            relevant_verses = []
            for i in range(len(results['documents'][0])):
                relevant_verses.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            return relevant_verses
            
        except Exception as e:
            print(f"Error retrieving verses: {e}")
            return []
    
    def generate_response(self, query: str, relevant_verses: List[Dict]) -> str:
        """Generate response using Gemini API with retrieved context."""
        try:
            # Prepare context from retrieved verses
            context = "\n\n".join([
                f"**{verse['metadata']['chapter_title']} - {verse['metadata']['verse']}**\n{verse['metadata']['translation']}"
                for verse in relevant_verses
            ])
            
            # Create prompt
            prompt = f"""You are a knowledgeable teacher of the Bhagavad Gita, an ancient Hindu scripture. Based on the relevant verses provided below, answer the user's question with wisdom, clarity, and depth.

**Relevant Verses from Bhagavad Gita:**
{context}

**User Question:** {query}

**Instructions:**
1. Answer based primarily on the provided verses
2. Explain the philosophical concepts clearly
3. Provide practical insights where relevant
4. Reference specific verses when making points
5. Maintain a respectful and spiritual tone
6. If the question cannot be fully answered from the provided verses, acknowledge this

**Answer:**"""

            # Generate response using Gemini
            response = self.llm_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I encountered an error while generating the response. Please try again."
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        """Main query method that combines retrieval and generation."""
        print(f"\nProcessing query: {question}")
        
        # Retrieve relevant verses
        relevant_verses = self.retrieve_relevant_verses(question, top_k)
        
        if not relevant_verses:
            return {
                'answer': "I couldn't find relevant verses for your question. Please try rephrasing.",
                'sources': []
            }
        
        # Generate response
        answer = self.generate_response(question, relevant_verses)
        
        # Format sources
        sources = [
            {
                'chapter': verse['metadata']['chapter_title'],
                'verse': verse['metadata']['verse'],
                'translation': verse['metadata']['translation'],
                'relevance_score': 1 - verse['distance']  # Convert distance to similarity
            }
            for verse in relevant_verses
        ]
        
        return {
            'answer': answer,
            'sources': sources
        }

def main():
    """Demo function to test the RAG system."""
    # Initialize RAG system
    print("Initializing Bhagavad Gita RAG System...")
    rag = BhagavadGitaRAG('bhagavad_gita_verses.csv')
    
    # Example queries
    test_queries = [
        "What does Krishna say about duty and action?",
        "How should one deal with fear and anxiety?",
        "What is the nature of the soul according to the Gita?",
        "What does the Gita teach about meditation?",
        "How can one achieve inner peace?"
    ]
    
    print("\n" + "="*80)
    print("BHAGAVAD GITA RAG SYSTEM - DEMO")
    print("="*80)
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 50)
        
        result = rag.query(query, top_k=3)
        
        print("📝 Answer:")
        print(result['answer'])
        
        print("\n📚 Sources:")
        for i, source in enumerate(result['sources'], 1):
            print(f"{i}. {source['chapter']} - {source['verse']}")
            print(f"   Relevance: {source['relevance_score']:.3f}")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    main()
