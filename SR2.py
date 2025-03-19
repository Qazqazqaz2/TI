import pandas as pd
from collections import Counter

class ShannonFanoEncoder:
    def __init__(self, text):
        self.text = text
        self.char_counts = Counter(text)
        self.total_chars = sum(self.char_counts.values())
        self.char_probs = {char: count / self.total_chars for char, count in self.char_counts.items()}
        self.sorted_chars = sorted(self.char_probs.items(), key=lambda x: x[1], reverse=True)
        self.fano_codes = self._build_fano_codes(self.sorted_chars)

    def _build_fano_codes(self, symbols):
        if len(symbols) == 1:
            return {symbols[0][0]: ""}

        total_prob = sum([prob for _, prob in symbols])
        cumulative_prob = 0
        split_index = 0

        for i, (_, prob) in enumerate(symbols):
            cumulative_prob += prob
            if cumulative_prob >= total_prob / 2:
                split_index = i
                break

        left_part = symbols[:split_index + 1]
        right_part = symbols[split_index + 1:]

        left_codes = self._build_fano_codes(left_part)
        right_codes = self._build_fano_codes(right_part)

        for key in left_codes:
            left_codes[key] = '0' + left_codes[key]
        for key in right_codes:
            right_codes[key] = '1' + right_codes[key]

        left_codes.update(right_codes)
        return left_codes

    def get_fano_codes_df(self):
        df = pd.DataFrame({
            "Символ": [char for char, _ in self.sorted_chars],
            "Частота": [self.char_counts[char] for char, _ in self.sorted_chars],
            "Вероятность": [self.char_probs[char] for char, _ in self.sorted_chars],
            "Код Фано": [self.fano_codes[char] for char, _ in self.sorted_chars]
        })
        return df

    def check_kraft_inequality(self):
        kraft_sum = sum(2 ** -len(code) for code in self.fano_codes.values())
        return "Неравенство Крафта выполняется" if kraft_sum <= 1 else "Неравенство Крафта не выполняется"


class HammingEncoder:
    def __init__(self, char):
        self.char = char
        self.binary_code = format(ord(char), '08b')
        self.hamming_code = self._encode_hamming74(self.binary_code[:4]) + self._encode_hamming74(self.binary_code[4:])
        self.corrected_hamming_code = self._correct_hamming74(self.hamming_code[:7]) + self._correct_hamming74(self.hamming_code[7:])

    def _encode_hamming74(self, data_bits):
        p1 = int(data_bits[0]) ^ int(data_bits[1]) ^ int(data_bits[3])
        p2 = int(data_bits[0]) ^ int(data_bits[2]) ^ int(data_bits[3])
        p3 = int(data_bits[1]) ^ int(data_bits[2]) ^ int(data_bits[3])
        return [p1, p2, int(data_bits[0]), p3, int(data_bits[1]), int(data_bits[2]), int(data_bits[3])]

    def _correct_hamming74(self, encoded_bits):
        p1 = encoded_bits[0] ^ encoded_bits[2] ^ encoded_bits[4] ^ encoded_bits[6]
        p2 = encoded_bits[1] ^ encoded_bits[2] ^ encoded_bits[5] ^ encoded_bits[6]
        p3 = encoded_bits[3] ^ encoded_bits[4] ^ encoded_bits[5] ^ encoded_bits[6]

        error_pos = p1 * 1 + p2 * 2 + p3 * 4

        if error_pos > 0:
            encoded_bits[error_pos - 1] ^= 1
        return encoded_bits

    def get_hamming_df(self):
        df = pd.DataFrame({
            "Бит №": list(range(1, 15)),
            "Код Хэмминга": self.hamming_code,
            "Исправленный код": self.corrected_hamming_code
        })
        return df


class TextProcessor:
    def __init__(self, text):
        self.text = text
        self.fano_encoder = ShannonFanoEncoder(text)
        self.hamming_encoder = HammingEncoder('Б')

    def save_results_to_csv(self):
        self.fano_encoder.get_fano_codes_df().to_csv("fano_code.csv", index=False, encoding="utf-8-sig")
        self.hamming_encoder.get_hamming_df().to_csv("hamming_code.csv", index=False, encoding="utf-8-sig")

    def print_results(self):
        print("\n--- Кодирование Фано ---")
        print(self.fano_encoder.get_fano_codes_df())
        print("\n--- Код Хэмминга ---")
        print(self.hamming_encoder.get_hamming_df())
        print("\nПроверка неравенства Крафта:", self.fano_encoder.check_kraft_inequality())


if __name__ == "__main__":
    text = "Артём Ермолов"
    processor = TextProcessor(text)
    processor.print_results()
    processor.save_results_to_csv()