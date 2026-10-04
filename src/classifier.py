import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

def load_and_prep_data(filepath='data/tickets.csv'):
    df = pd.read_csv(filepath)
    
    df['text'] = df['customer_message'].fillna('') + " " + df['agent_notes'].fillna('')
    
    logistics_keywords = ['dlvry', 'delivery', 'courier', 'dispatch', 'crr partner', 'shipped', 'tracking', 'order status', 'shipment']
    mask_logistics = df['text'].str.lower().str.contains('|'.join(logistics_keywords), na=False)
    
    df['clean_category'] = df['category']
    df.loc[(df['category'] == 'Billing & Payments') & mask_logistics, 'clean_category'] = 'Delivery & Shipping'
    
    return df

def train_model():
    print("Loading tickets dataset...")
    df = load_and_prep_data()
    
    valid_categories = df['clean_category'].value_counts()[lambda x: x > 50].index
    df_filtered = df[df['clean_category'].isin(valid_categories)].copy()
    
    X = df_filtered['text']
    y = df_filtered['clean_category']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples...")
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))),
        ('clf', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    
    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\n================ Model Evaluation ================")
    print(f"Overall Accuracy: {acc*100:.2f}%")
    print("\nDetailed Performance Report:")
    print(classification_report(y_test, preds, zero_division=0))
    
    joblib.dump(pipeline, 'src/ticket_classifier.pkl')
    print("Model saved successfully to src/ticket_classifier.pkl")
    return pipeline

if __name__ == '__main__':
    train_model()