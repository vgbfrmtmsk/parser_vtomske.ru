import pandas as pd
import os

# Укажите полный путь к вашему файлу
file_path = r'D:\work\practice\parser\vtomske\vtomske_titles.csv'  # замените на ваш путь

if os.path.exists(file_path):
    df = pd.read_csv(file_path, sep=';', on_bad_lines='skip')
    
    print(f"Размер: {df.shape}")
    print(f"Колонки: {df.columns.tolist()}")
    print(f"Типы данных:\n{df.dtypes}")
    print(f"Пропущенные значения:\n{df.isnull().sum()}")
    print("\nПервые 5 строк:")
    print(df.head())
else:
    print(f"Файл не найден по пути: {file_path}")