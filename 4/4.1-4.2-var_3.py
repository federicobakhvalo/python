from collections import Counter
from pathlib import Path
import re
from typing import Dict
import matplotlib.pyplot as plt


class TextFragment:
    # def __init__(self,file_path:Path):
    #     self.path=file_path

    # def change_file(self):
    #     with open(self.path, 'r', encoding='utf-8') as file:
    #         content = file.read().replace('\n\n', '\n')
    #
    #
    #     with open(self.path, 'w+', encoding='utf-8') as file:
    #         file.write(content)

    @classmethod
    def find_strings_from_2_digits(cls,path:Path):
        text=cls.read_text_from_path(path)
        lines = text.splitlines()


        two_digit_pattern = re.compile(r'\b\d{2}\b')

        matching_lines = '\n'.join([line for line in lines if two_digit_pattern.search(line)])


        return matching_lines


    @classmethod
    def read_text_from_path(cls,path:Path,start_pos=None,end_pos=None):
        with open(path,'r',encoding='utf-8') as file:
            text=file.read()

        if start_pos is not None and end_pos is not None:
            return text[start_pos:end_pos]
        return text

    @classmethod
    def analyze_text(cls,text) ->Dict:
        words = re.findall(r'\b\w+\b', text.lower())
        word_lengths = [len(word) for word in words]
        word_count = len(words)

        length_freq = Counter(word_lengths)

        return {
            'word_count': word_count,
            'word_lengths': word_lengths,
            'length_freq': dict(length_freq),
            'sorted_freq_asc': dict(sorted(length_freq.items())),
            'sorted_freq_desc': dict(sorted(length_freq.items(), reverse=True)),
        }

    @classmethod
    def plot_histogram(cls,freq_dict:Dict, title='Гистограмма'):
        lengths = list(freq_dict.keys())
        frequencies = list(freq_dict.values())

        plt.figure(figsize=(10, 5))
        plt.bar(lengths, frequencies, color='skyblue', edgecolor='black')
        plt.xlabel('Длина слова')
        plt.ylabel('Частота')
        plt.title(title)
        plt.grid(True)
        plt.show()

    @classmethod
    def analyze_sentences(cls,text):
        sentences = re.split(r'[.!?]', text)
        sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences if s.strip()]
        sentence_freq = Counter(sentence_lengths)

        return {
            'sentence_lengths': sentence_lengths,
            'sentence_freq': dict(sentence_freq),
            'sorted_sentence_freq': dict(sorted(sentence_freq.items())),
        }



if __name__=='__main__':
    #text=TextFragment(Path('text.txt')).read_text_from_path()
    text=TextFragment.read_text_from_path(Path('text.txt'))
    strings=TextFragment.find_strings_from_2_digits(Path('text.txt'))
    #print(strings)
    # print("=== Анализ слов ===")


    # word_data=TextFragment.analyze_text(text)
    # # print("Количество слов:", word_data['word_count'])
    # # print(word_data)
    #
    # TextFragment.plot_histogram(word_data['sorted_freq_asc'], title="Частота по длине слова")
    #
    # print("=== Анализ предложений ===")
    # sentence_data = TextFragment.analyze_sentences(text)
    # TextFragment.plot_histogram(sentence_data['sorted_sentence_freq'], title="Частота по длине предложения (в словах)")

