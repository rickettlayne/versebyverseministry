"""
Chatbot for answering Bible questions using scraped content from 
Verse by Verse Ministry website.

This module provides a chatbot interface that uses the scraped content
to answer Bible-related questions.
"""

import os
import json
from typing import List, Dict, Optional
import re


class VBVMChatbot:
    """Chatbot for Bible questions using VBVM content."""
    
    def __init__(self, content_dir: str = "scraped_content"):
        """
        Initialize the chatbot.
        
        Args:
            content_dir: Directory containing scraped content
        """
        self.content_dir = content_dir
        self.documents = []
        self.load_content()
    
    def load_content(self):
        """Load all scraped content into memory."""
        if not os.path.exists(self.content_dir):
            print(f"Warning: Content directory '{self.content_dir}' not found.")
            print("Please run the scraper first to collect content.")
            return
        
        # Load index if it exists
        index_path = os.path.join(self.content_dir, 'index.json')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
                print(f"Found {len(index)} documents in index.")
        
        # Load all JSON files
        for filename in os.listdir(self.content_dir):
            if filename.endswith('.json') and filename != 'index.json':
                filepath = os.path.join(self.content_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        doc = json.load(f)
                        self.documents.append(doc)
                except json.JSONDecodeError as e:
                    print(f"Error loading {filename}: {e}")
        
        print(f"Loaded {len(self.documents)} documents.")
    
    def search_content(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for relevant content based on query.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of relevant documents with scores
        """
        if not self.documents:
            return []
        
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        # Score each document based on keyword matches
        scored_docs = []
        for doc in self.documents:
            score = 0
            content_lower = (doc.get('title', '') + ' ' + doc.get('content', '')).lower()
            
            # Count occurrences of query words
            for word in query_words:
                if len(word) > 2:  # Ignore very short words
                    score += content_lower.count(word)
            
            # Bonus for title matches
            title_lower = doc.get('title', '').lower()
            for word in query_words:
                if word in title_lower:
                    score += 5
            
            if score > 0:
                scored_docs.append({
                    'document': doc,
                    'score': score
                })
        
        # Sort by score and return top results
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:max_results]
    
    def generate_answer(self, query: str) -> str:
        """
        Generate an answer to a question based on scraped content.
        
        Args:
            query: Question to answer
            
        Returns:
            Answer string
        """
        if not self.documents:
            return ("I don't have any content loaded yet. "
                   "Please run the scraper first to collect Bible study materials.")
        
        # Search for relevant content
        results = self.search_content(query, max_results=3)
        
        if not results:
            return ("I couldn't find any relevant content for your question. "
                   "Try rephrasing your question or asking about a different topic.")
        
        # Build answer from top results
        answer_parts = [
            "Based on the Bible study materials from Verse by Verse Ministry, "
            "here's what I found:\n"
        ]
        
        for i, result in enumerate(results, 1):
            doc = result['document']
            title = doc.get('title', 'Untitled')
            url = doc.get('url', '')
            content = doc.get('content', '')
            
            # Extract relevant excerpt
            excerpt = self._extract_relevant_excerpt(content, query)
            
            answer_parts.append(f"\n{i}. From '{title}':")
            if excerpt:
                answer_parts.append(f"   {excerpt}")
            answer_parts.append(f"   Source: {url}\n")
        
        return '\n'.join(answer_parts)
    
    def _extract_relevant_excerpt(self, content: str, query: str, 
                                  context_chars: int = 300) -> str:
        """
        Extract a relevant excerpt from content based on query.
        
        Args:
            content: Full content text
            query: Search query
            context_chars: Number of characters of context to include
            
        Returns:
            Relevant excerpt
        """
        if not content:
            return ""
        
        query_lower = query.lower()
        content_lower = content.lower()
        query_words = re.findall(r'\w+', query_lower)
        
        # Find the position with the most query word matches
        best_pos = 0
        best_score = 0
        
        for i in range(0, len(content), 50):
            window = content_lower[i:i+context_chars]
            score = sum(window.count(word) for word in query_words if len(word) > 2)
            if score > best_score:
                best_score = score
                best_pos = i
        
        # Extract excerpt around best position
        start = max(0, best_pos - context_chars // 2)
        end = min(len(content), best_pos + context_chars * 3 // 2)
        
        excerpt = content[start:end].strip()
        
        # Add ellipsis if needed
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(content):
            excerpt = excerpt + "..."
        
        return excerpt
    
    def chat(self):
        """Run interactive chat session."""
        print("\n" + "="*60)
        print("Verse by Verse Ministry Bible Study Chatbot")
        print("="*60)
        print("\nAsk questions about the Bible based on Stephen Armstrong's teachings.")
        print("Type 'quit' or 'exit' to end the session.\n")
        
        if not self.documents:
            print("Warning: No content loaded. Please run the scraper first.")
            return
        
        while True:
            try:
                question = input("\nYour question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\nThank you for using the chatbot. Goodbye!")
                    break
                
                if not question:
                    continue
                
                answer = self.generate_answer(question)
                print(f"\nAnswer:\n{answer}")
                
            except KeyboardInterrupt:
                print("\n\nSession ended by user. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")


def main():
    """Main function to run the chatbot."""
    chatbot = VBVMChatbot()
    chatbot.chat()


if __name__ == "__main__":
    main()
