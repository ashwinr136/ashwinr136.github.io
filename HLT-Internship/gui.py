import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from keybert import KeyBERT
import urllib.parse
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
import streamlit as st

df = pd.read_csv('https://raw.githubusercontent.com/ashwinr136/ashwinr136.github.io/main/HLT-Internship/cleaned_inventions_dataset.csv')
df['text'] = df['Invention'] + " " + df['Description'] + " " + df['Background']
X = df['text']
y = df['Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer_bow = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
X_train_bow = vectorizer_bow.fit_transform(X_train)
X_test_bow = vectorizer_bow.transform(X_test)
nb_bow = MultinomialNB()
nb_bow.fit(X_train_bow, y_train)

def predict_invention_category(title, description, background):

    new_text = title + " " + description + " " + background
    new_counts = vectorizer_bow.transform([new_text])

    predicted_category = nb_bow.predict(new_counts)

    #print(f"Predicted Category: {predicted_category[0]}")
    return predicted_category[0]

def generate_search_links(description, top_n=5):
    # Initialize KeyBERT model
    kw_model = KeyBERT()
    
    # Extract keywords
    keywords = kw_model.extract_keywords(description, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    market_keywords = kw_model.extract_keywords(description, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=2)
    # Generate Google search URL
    google_query = 'market overview ' + ' '.join([kw for kw, _ in keywords])
    google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(google_query)}"
    query = ' '.join([kw for kw, _ in market_keywords])
    # Generate market research report URLs
    websites = [
        ("ResearchGate", f"https://www.researchgate.net/search.Search.html?type=publication&query={urllib.parse.quote(query)}"),
        ("Globe News Wire", f"https://www.globenewswire.com/en/search/keyword/{urllib.parse.quote(query)}?pageSize=50"),
        ("Markets and Markets", f"https://www.marketsandmarkets.com/search.asp?search={urllib.parse.quote(query)}"),
        ("GM Insights", f"https://www.gminsights.com/filters?q={urllib.parse.quote(query)}"),
        ("Mordor Intelligence", f"https://www.mordorintelligence.com/search?q={urllib.parse.quote(query)}"),
        ("Grandview Research", f"https://www.grandviewresearch.com/Filters?search={urllib.parse.quote(query)}&search_submit=+")
    ]
    
    report_links = [(name, url) for name, url in websites if isinstance(name, str) and isinstance(url, str)]
    return keywords, google_search_url, report_links

st.title('Invention Categorizer and Market Research Helper Tool')

# User inputs for Title, Description, and Background
title = st.text_input("Enter Invention Title")
description = st.text_area("Enter Invention Description", height=150)
background = st.text_area("Enter Invention Background", height=150)

if st.button('Generate Keywords and Links'):
    # Concatenate title, description, and background
    combined_text = f"{title} {description} {background}".strip()
    
    if combined_text:
        keywords, google_search_url, report_links = generate_search_links(combined_text)
        pred = predict_invention_category(title, description, background)
        st.subheader('Predicted Category based on Multinomial Naive Bayes using Bag Of Words:')
        st.write(pred)
        st.subheader('Extracted Keywords:')
        for kw, score in keywords:
            st.write(f"- {kw} (Score: {score:.4f})")
        
        st.subheader('Google Search Link:')
        st.write(f"[Google Search]({google_search_url})")
        
        st.subheader('Market Research Report Links:')
        # Safely iterate over report links and ensure they are correctly formatted
        for report in report_links:
            if len(report) == 2:
                name, url = report
                st.write(f"[{name}]({url})")
            else:
                st.write("Error: Invalid report link format.")
    else:
        st.warning("Please enter at least one field.")
