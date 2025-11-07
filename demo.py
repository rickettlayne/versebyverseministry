#!/usr/bin/env python3
"""
Demo script to test the chatbot functionality with sample questions.
"""

from chatbot import VBVMChatbot


def main():
    """Run demo questions through the chatbot."""
    print("="*70)
    print("Verse by Verse Ministry Chatbot - Demo")
    print("="*70)
    
    # Initialize chatbot
    chatbot = VBVMChatbot()
    
    if not chatbot.documents:
        print("\nError: No content loaded.")
        print("Please run 'python main.py scrape' first to collect content.")
        return
    
    # Demo questions
    questions = [
        "What is faith?",
        "Explain the Gospel",
        "What does Romans teach about justification?",
        "How are we saved?"
    ]
    
    for question in questions:
        print(f"\n{'='*70}")
        print(f"Question: {question}")
        print(f"{'='*70}")
        
        answer = chatbot.generate_answer(question)
        print(answer)
        print()


if __name__ == "__main__":
    main()
