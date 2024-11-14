
import streamlit as st
import re
from typing import Dict, List, Tuple
import random
from datetime import datetime

class GitaBot:
    def __init__(self):
        # Knowledge base of Gita verses and their themes
        self.verses = {
            "karma": [
                ("Chapter 2, Verse 47", "You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions. Never consider yourself to be the cause of the results, and never be motivated by inaction."),
                ("Chapter 3, Verse 19", "Therefore, without attachment, perform always the work that has to be done, for by performing work without attachment, one attains the Supreme."),
            ],
            "dharma": [
                ("Chapter 2, Verse 31", "Considering your dharma (duty), you should not waver. Indeed, for a warrior, there is nothing better than a battle fought on principles of dharma."),
                ("Chapter 18, Verse 47", "It is better to perform one's own duties imperfectly than to perform another's duties perfectly. By fulfilling the obligations born of one's nature, one never incurs sin."),
            ],
            "mind_control": [
                ("Chapter 6, Verse 35", "The mind is restless, turbulent, obstinate and very strong, O Krishna, and to subdue it is more difficult than controlling the wind."),
                ("Chapter 6, Verse 36", "But it is possible by suitable practice and detachment."),
            ],
            "knowledge": [
                ("Chapter 4, Verse 33", "Superior to the sacrifice of material possessions is the sacrifice of knowledge, O Arjuna. All actions in their entirety culminate in knowledge."),
                ("Chapter 4, Verse 34", "Learn the Truth by approaching a spiritual master. Inquire from him with reverence, and render service unto him."),
            ],
            "peace": [
                ("Chapter 2, Verse 66", "One who is not in transcendental consciousness can have neither a controlled mind nor steady intelligence, without which there is no possibility of peace. And how can there be any happiness without peace?"),
                ("Chapter 5, Verse 29", "A person in full consciousness of Me, knowing Me to be the ultimate beneficiary of all sacrifices and austerities, the Supreme Lord of all planets and demigods, and the benefactor and well-wisher of all living entities, attains peace from the pangs of material miseries."),
            ]
        }
        
        self.keywords = {
            "karma": ["action", "work", "duty", "results", "fruits", "deeds", "karma", "doing"],
            "dharma": ["duty", "righteousness", "dharma", "responsibility", "obligation", "right"],
            "mind_control": ["mind", "control", "meditation", "focus", "concentration", "thoughts"],
            "knowledge": ["knowledge", "wisdom", "learning", "understanding", "truth", "awareness"],
            "peace": ["peace", "happiness", "tranquility", "calm", "serenity", "contentment"]
        }

    def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def identify_themes(self, question: str) -> List[str]:
        question = self.preprocess_text(question)
        words = question.split()
        
        identified_themes = []
        for theme, theme_keywords in self.keywords.items():
            if any(keyword in words for keyword in theme_keywords):
                identified_themes.append(theme)
        
        return identified_themes or ["karma"]

    def get_response(self, question: str) -> Dict:
        themes = self.identify_themes(question)
        selected_theme = random.choice(themes)
        verse_reference, verse_text = random.choice(self.verses[selected_theme])
        
        response = {
            "theme": selected_theme.capitalize(),
            "reference": verse_reference,
            "verse": verse_text,
            "explanation": f"Based on your question, I've shared this verse about {selected_theme}. "
                         f"The Bhagavad Gita teaches us that {self._get_theme_explanation(selected_theme)}"
        }
        
        return response

    def _get_theme_explanation(self, theme: str) -> str:
        explanations = {
            "karma": "we should perform our duties without attachment to the results.",
            "dharma": "following one's righteous duty is the path to spiritual growth.",
            "mind_control": "controlling the mind through practice and detachment is essential for spiritual progress.",
            "knowledge": "true knowledge is the highest form of spiritual practice.",
            "peace": "true peace comes from understanding our relationship with the divine."
        }
        return explanations.get(theme, "this wisdom can guide us in our spiritual journey.")

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'bot' not in st.session_state:
        st.session_state.bot = GitaBot()

def main():
    st.set_page_config(
        page_title="Bhagavad Gita Wisdom Bot",
        page_icon="🕉️",
        layout="centered"
    )

    initialize_session_state()

    # Header
    st.title("🕉️ Bhagavad Gita Wisdom Bot")
    st.markdown("""
    Welcome to the Bhagavad Gita Wisdom Bot! Ask any question about life, duty, peace, 
    or spiritual growth, and receive guidance from the sacred text of the Bhagavad Gita.
    """)

    # Sidebar with available themes
    with st.sidebar:
        st.header("Available Themes")
        themes = ["Karma (Action)", "Dharma (Duty)", "Mind Control", 
                 "Knowledge", "Peace"]
        for theme in themes:
            st.markdown(f"• {theme}")
        
        st.markdown("---")
        st.markdown("""
        ### How to Use
        1. Type your question in the text box
        2. Press Enter or click 'Ask'
        3. Receive wisdom from the Gita
        """)

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                st.markdown(f"**{message['reference']}**")
                st.markdown(f"*{message['verse']}*")
                st.markdown(message["explanation"])

    # User input
    if question := st.chat_input("Ask your question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Get bot response
        response = st.session_state.bot.get_response(question)
        
        # Add bot response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "reference": response["reference"],
            "verse": response["verse"],
            "explanation": response["explanation"]
        })
        
        # Rerun to update the chat display
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        "Made with ❤️ | "
        "Remember: The Gita's wisdom is vast and deep. "
        "These are selected verses for guidance, but please consult spiritual teachers for deeper understanding."
    )

if __name__ == "__main__":
    main()
