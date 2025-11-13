import pandas as pd
from razdel import tokenize




file_path = r'D:\work\practice\parser\vtomske\vtomske.csv'  # замените на ваш путь
df = pd.read_csv(file_path, sep=';')

texts = df['title']

token_data = []
for i, text in enumerate(texts):
    print(f'Текст номер {i}')
    tokens = [token.text for token in tokenize(text)]
    print(tokens)
    token_data.append({
        'number': i,
        'tokens': tokens
    })
    if i > 3:
        break


print(token_data[0])