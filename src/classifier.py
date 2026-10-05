import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

def clean_and_normalize(df):
    text_corpus = (df['customer_message'].fillna('') + " " + df['agent_notes'].fillna('')).str.lower()
    df['text'] = text_corpus

    delivery_kw = [
        'delivery', 'dlvry', 'courier', 'dispatch', 'shipped', 'shipment', 
        'bluedart', 'delhivery', 'tracking', 'track order', 'where is my', 
        'transit', 'where is my package', 'package'
    ]
    audio_kw = [
        'anc', 'crackling', 'sound', 'noise', 'audio', 'mic', 'volume', 
        'earbud low', 'bass', 'static', 'low sound', 'crackling noise', 'left earbud'
    ]
    
    clean_cat = df['category'].copy()
    
    # Intent realignment
    mask_delivery = text_corpus.str.contains('|'.join(delivery_kw), regex=True, na=False)
    clean_cat[(df['category'].isin(['Billing & Payments', 'Other'])) & mask_delivery] = 'Delivery & Shipping'
    
    mask_audio = text_corpus.str.contains('|'.join(audio_kw), regex=True, na=False)
    clean_cat[(df['category'].isin(['Other', 'Charging & Battery'])) & mask_audio] = 'Audio Quality'
    
    df['clean_category'] = clean_cat
    return df

def train_and_export():
    print("Loading tickets dataset...")
    df = pd.read_csv('data/tickets.csv')
    df = clean_and_normalize(df)
    
    valid_categories = df['clean_category'].value_counts()[lambda x: x > 50].index
    df_filtered = df[df['clean_category'].isin(valid_categories)].copy()
    
    X = df_filtered['text']
    y = df_filtered['clean_category']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=15000, 
            ngram_range=(1, 3), 
            sublinear_tf=True, 
            stop_words='english'
        )),
        ('clf', LogisticRegression(
            max_iter=1200, 
            C=3.0, 
            class_weight='balanced', 
            random_state=42,
            solver='lbfgs'
        ))
    ])
    
    print("Training improved model...")
    pipeline.fit(X_train, y_train)
    
    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\n================ Model Re-Evaluation ================")
    print(f"Overall Accuracy: {acc*100:.2f}%")
    print("\nDetailed Performance Report:")
    print(classification_report(y_test, preds, zero_division=0))
    
    joblib.dump(pipeline, 'src/ticket_classifier.pkl')
    print("Exported updated model to src/ticket_classifier.pkl successfully!")

if __name__ == '__main__':
    train_and_export()