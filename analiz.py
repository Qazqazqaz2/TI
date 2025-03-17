from collections import Counter
from math import log2
from tabulate import tabulate

# Пути к файлам
artistic_path = r"C:\Users\armian\Downloads\ТИ\ТИ\Художественный текст.txt"
scientific_path = r"C:\Users\armian\Downloads\ТИ\ТИ\Научный текст.txt"


def read_text(file_path):
    """Читает текст из файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def frequency_analysis(text):
    """Анализирует частоты символов в тексте."""
    freq = Counter(text)
    total = sum(freq.values())
    return sorted(((char, count / total) for char, count in freq.items()), key=lambda x: x[1], reverse=True)


def alphabet_redundancy(frequencies):
    """Вычисляет энтропию и избыточность алфавита."""
    if not frequencies:
        return 0, 0
    
    H = -sum(prob * log2(prob) for _, prob in frequencies if prob > 0)
    Hmax = log2(len(frequencies)) if frequencies else 1
    return H, 1 - H / Hmax if Hmax > 0 else 0


def code_analysis(frequencies, codes):
    """Анализирует избыточность кода и вектор Крафта."""
    if not frequencies:
        return 0, 0, 0
    
    avg_length = sum(len(codes.get(char, "")) * prob for char, prob in frequencies)
    H = -sum(prob * log2(prob) for _, prob in frequencies if prob > 0)
    R_code = 1 - H / avg_length if avg_length > 0 else 0
    kraft_sum = sum(2 ** -len(codes.get(char, "")) for char, _ in frequencies)
    
    return avg_length, R_code, kraft_sum


def analyze_text(file_path):
    """Читает текст, анализирует его частоты и характеристики."""
    text = read_text(file_path)
    frequencies = frequency_analysis(text)
    return frequencies, *alphabet_redundancy(frequencies)


# Читаем и анализируем тексты
artistic_freq, H_art, R_alphabet_art = analyze_text(artistic_path)
scientific_freq, H_sci, R_alphabet_sci = analyze_text(scientific_path)

# Генерация кодов (пример — двоичное кодирование последовательности)
example_codes = {char: bin(i)[2:] for i, (char, _) in enumerate(artistic_freq)}

# Анализ кодирования
avg_length_art, R_code_art, kraft_sum_art = code_analysis(artistic_freq, example_codes)
avg_length_sci, R_code_sci, kraft_sum_sci = code_analysis(scientific_freq, example_codes)

# Вывод результатов
for text_type, H, R_alphabet, avg_length, R_code, kraft_sum in [
    ("Художественный текст", H_art, R_alphabet_art, avg_length_art, R_code_art, kraft_sum_art),
    ("Научный текст", H_sci, R_alphabet_sci, avg_length_sci, R_code_sci, kraft_sum_sci)
]:
    print(f"\nАнализ {text_type}:")
    print(tabulate([
        ["Энтропия (H)", H],
        ["Избыточность алфавита (R)", R_alphabet],
        ["Средняя длина кода", avg_length],
        ["Избыточность кода (R)", R_code],
        ["Вектор Крафта", kraft_sum]
    ], headers=["Параметр", "Значение"], tablefmt="pretty"))
