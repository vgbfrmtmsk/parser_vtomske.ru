import pandas as pd
from razdel import tokenize
import spacy
from tqdm import tqdm
import re

# Загружаем модель spaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

def preprocess_text(text):
    """Функция предобработки текста"""
    if pd.isna(text):
        return ""
    
    text = str(text)
    text = text.lower()
    text = re.sub(r'[^а-яё0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

file_path = r'D:\work\practice\parser\vtomske\vtomske.csv'
df = pd.read_csv(file_path, sep=';')

def process_texts(texts):
    results = []
    
    # Добавляем прогресс-бар
    for i, text in enumerate(tqdm(texts, desc="Обработка текстов", unit="текст")):
        # ПРЕПРОЦЕССИНГ - обрабатываем текст перед токенизацией
        processed_text = preprocess_text(text)
        
        # Пропускаем пустые тексты после препроцессинга
        if not processed_text:
            tokens = []
            lemmas = []
        else:
            # Обрабатываем текст с помощью spaCy
            doc = nlp(processed_text)
            # Извлекаем токены и леммы
            tokens = [token.text for token in doc]
            lemmas = [token.lemma_ for token in doc]
        
        results.append({
            'text': text,
            'processed': processed_text,
            'tokenized': tokens,
            'lemmatized': lemmas
        })
    
    return results

# Обрабатываем тексты с прогресс-баром
print("Начинаем обработку текстов...")
processed_data = process_texts(df['title'])

# Создаем новый DataFrame только с нужными колонками
result_df = pd.DataFrame(processed_data)

print("\nОбработка завершена!")
print(result_df.head())

# Сохраняем в CSV файл
output_file = r'D:\work\practice\parser\vtomske\vtomske_processed.csv'
result_df.to_csv(output_file, sep=';', index=False, encoding='utf-8-sig')
print(f"\nДанные сохранены в файл: {output_file}")

def result_show():
    # Выводим результаты
    print("\nПримеры обработки:")
    for i, item in enumerate(result_df.head().to_dict('records')):
        print(f"\n--- Текст {i} ---")
        print(f"Text: {item['text']}")
        print(f"Processed: {item['processed']}")
        print(f"Tokenized: {item['tokenized']}")
        print(f"Lemmatized: {item['lemmatized']}")

# Показываем результаты
result_show()

# Дополнительная информация о сохраненном файле
print(f"\nИнформация о сохраненном файле:")
print(f"Количество строк: {len(result_df)}")
print(f"Колонки: {result_df.columns.tolist()}")