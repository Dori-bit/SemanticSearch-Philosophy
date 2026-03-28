import pandas as pd
import pymorphy3
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

morph = pymorphy3.MorphAnalyzer()
rus_stop_w = stopwords.words('russian')

def preprocess_text(t):
    """
    Очищает текст от пунктуации и приводит слова к начальной форме (лемматизация).
    Убирает стоп-слова, чтобы алгоритм не отвлекался на предлоги и союзы.
    """
    words = re.findall(r'[а-яё]+', t.lower())
    lemmas = [morph.parse(w)[0].normal_form for w in words if w not in rus_stop_w]
    return " ".join(lemmas)

def run_search():
    """
    Основная функция: строит векторное пространство текстов и запускает цикл поиска релевантных абзацев по косинусному расстоянию.
    """
    df = pd.read_csv('data/corpus.csv')

    vectorizer = TfidfVectorizer(preprocessor = preprocess_text)

    tfidf_matr = vectorizer.fit_transform(df['text'].values.astype('U'))

    print("Напишите 'exit' для выхода из программы.")

    while True:
        q = input("\nО чем хочешь спросить философов?: ")
        if q.lower() == 'exit': break

        q_vec = vectorizer.transform([q])
        
        simil = cosine_similarity(q_vec, tfidf_matr).flatten()
        top_indices = simil.argsort()[-3:][::-1]

        if simil[top_indices[0]] <= 0.05:
            print("Мои философы об этом молчат...")
            continue

        for i in top_indices:
            score = simil[i]
            if score > 0.05:
                print(f"\n[Сходство: {score:.4f}] | Источник: {df.iloc[i]['book']}")
                print(f"Текст: {df.iloc[i]['text'][:400]}...")

if __name__ == "__main__":
    run_search()
