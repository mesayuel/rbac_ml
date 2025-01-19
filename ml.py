# ml.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import re

# Training data sederhana
TRAINING_DATA = [
    ("Can I edit this document?", "edit_document"),
    ("I want to edit the document", "edit_document"),
    ("Let me edit this file", "edit_document"),
    ("Need to modify this document", "edit_document"),
    
    ("Can I view this document?", "view_document"),
    ("I want to see the document", "view_document"),
    ("Show me this file", "view_document"),
    ("Let me read this document", "view_document"),
    
    ("Can I delete this document?", "delete_document"),
    ("I want to remove this file", "delete_document"),
    ("Delete this document", "delete_document"),
    ("Remove this file", "delete_document"),
]

# Permission mapping
INTENT_PERMISSION_MAP = {
    'edit_document': ['edit_document'],
    'view_document': ['view_document'],
    'delete_document': ['delete_document'],
}

def preprocess_text(text):
    """Simple text preprocessing"""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

class IntentDetector:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(preprocessor=preprocess_text)),
            ('clf', MultinomialNB())
        ])
        self._train()

    def _train(self):
        texts, labels = zip(*TRAINING_DATA)
        self.pipeline.fit(texts, labels)

    def detect(self, text):
        try:
            intent = self.pipeline.predict([text])[0]
            return intent if intent in INTENT_PERMISSION_MAP else None
        except Exception as e:
            print(f"Error in intent detection: {str(e)}")
            return None

# Initialize detector
intent_detector = IntentDetector()