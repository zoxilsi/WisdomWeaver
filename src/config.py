"""
Configuration management for different environments.
"""

import os

def get_api_key():
    """Get API key from environment or Colab."""
    try:
        # Try Colab first
        from google.colab import userdata
        return userdata.get('GOOGLE_API_KEY')
    except ImportError:
        # Fall back to environment variable
        return os.getenv('GOOGLE_API_KEY')

# Default paths
DATA_PATH = 'bhagavad_gita_verses.csv'
CHROMA_DIR = './chroma_db'
