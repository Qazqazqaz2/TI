from collections import Counter
from heapq import heappop, heappush
import matplotlib.pyplot as plt
import pandas as pd

# Пути к файлам
artistic_path = r"C:\Users\armian\Downloads\ТИ\ТИ\Художественный текст.txt"
scientific_path = r"C:\Users\armian\Downloads\ТИ\ТИ\Научный текст.txt"

# Чтение текстов
with open(artistic_path, "r", encoding="utf-8") as file:
    artistic_text = file.read()

with open(scientific_path, "r", encoding="utf-8") as file:
    scientific_text = file.read()

print("Художественный текст загружен. Длина:", len(artistic_text))
print("Научный текст загружен. Длина:", len(scientific_text))

def frequency_analysis(text):
    freq = Counter(text)
    total = sum(freq.values())
    probabilities = {char: count / total for char, count in freq.items()}
    sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    return sorted_probabilities

def shannon_fano_coding(symbols):
    def recursive_shannon_fano(symbols, code_dict, prefix=""):
        if len(symbols) == 1:
            code_dict[symbols[0][0]] = prefix or "0"
            return

        total_prob = sum(prob for _, prob in symbols)
        split_index = 0
        sum_prob = 0

        for i, (_, prob) in enumerate(symbols):
            sum_prob += prob
            if sum_prob >= total_prob / 2:
                split_index = i + 1
                break

        recursive_shannon_fano(symbols[:split_index], code_dict, prefix + "0")
        recursive_shannon_fano(symbols[split_index:], code_dict, prefix + "1")

    code_dict = {}
    recursive_shannon_fano(symbols, code_dict)
    return code_dict

def huffman_coding(symbols):
    heap = [[prob, [char, ""]] for char, prob in symbols]

    while len(heap) > 1:
        first = heappop(heap)
        second = heappop(heap)
        for pair in first[1:]:
            pair[1] = "0" + pair[1]
        for pair in second[1:]:
            pair[1] = "1" + pair[1]
        heappush(heap, [first[0] + second[0]] + first[1:] + second[1:])

    return {char: code for char, code in heappop(heap)[1:]}

def plot_histogram(frequencies, title, color):
    chars, probs = zip(*frequencies)
    chars = [c if c != '\n' else '\\n' for c in chars]

    plt.figure(figsize=(14, 7))
    plt.bar(chars, probs, color=color)
    plt.xlabel("Символы")
    plt.ylabel("Вероятность")
    plt.title(title)
    plt.xticks(rotation=0, fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()

# Анализ художественного текста
artistic_freq = frequency_analysis(artistic_text)
artistic_freq_sorted = sorted(artistic_freq, key=lambda x: x[1], reverse=True)
shannon_fano_artistic = shannon_fano_coding(artistic_freq_sorted)
huffman_artistic = huffman_coding(artistic_freq_sorted)

# Анализ научного текста
scientific_freq = frequency_analysis(scientific_text)
scientific_freq_sorted = sorted(scientific_freq, key=lambda x: x[1], reverse=True)
shannon_fano_scientific = shannon_fano_coding(scientific_freq_sorted)
huffman_scientific = huffman_coding(scientific_freq_sorted)

# Создание DataFrame для художественного текста
artistic_data = []
for char, prob in artistic_freq_sorted:
    artistic_data.append({
        'Символ': char if char != '\n' else '\\n',
        'Частота': artistic_text.count(char),
        'Вероятность': prob,
        'Шеннон-Фано': shannon_fano_artistic[char],
        'Хаффман': huffman_artistic[char]
    })

# Создание DataFrame для научного текста
scientific_data = []
for char, prob in scientific_freq_sorted:
    scientific_data.append({
        'Символ': char if char != '\n' else '\\n',
        'Частота': scientific_text.count(char),
        'Вероятность': prob,
        'Шеннон-Фано': shannon_fano_scientific[char],
        'Хаффман': huffman_scientific[char]
    })

# Создание Excel файла с двумя листами
with pd.ExcelWriter('анализ_текстов.xlsx') as writer:
    pd.DataFrame(artistic_data).to_excel(writer, sheet_name='Художественный текст', index=False)
    pd.DataFrame(scientific_data).to_excel(writer, sheet_name='Научный текст', index=False)

print("\nДанные сохранены в файл 'анализ_текстов.xlsx'")

# Построение графиков
plot_histogram(artistic_freq, "Вероятность символов в художественном тексте", "blue")
plot_histogram(scientific_freq, "Вероятность символов в научном тексте", "red") 