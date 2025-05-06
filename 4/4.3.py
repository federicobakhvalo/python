import re
from collections import defaultdict, Counter
from pathlib import Path
from typing import List, Tuple, Dict


class TextProcessor:
    text: str = ""

    @classmethod
    def load_from_file(cls, file_path: Path):
        with open(Path, encoding='utf-8') as f:
            cls.text = f.read()

    @classmethod
    def get_employees_data(cls) -> Dict[str, List[Tuple[str, int]]] or None:

        """
        Возвращает словарь из списков: фамилий, имён, отчеств, телефонов, email, адресов.
        Также добавлена позиция первого вхождения для сортировки.
        """
        if len(cls.text)==0:
            return None

        patterns = {
            "surnames": r"\b[А-ЯЁ][а-яё]+(?=\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)",   # Иванов
            "names": r"(?<=\b)[А-ЯЁ][а-яё]+(?=\s[А-ЯЁ][а-яё]+)",                # Иван
            "patronymics": r"(?<=\b[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s)[А-ЯЁ][а-яё]+",  # Иванович
            "phones": r"\+?\d[\d\s\-()]{7,}\d",  # Простой шаблон телефона
            "emails": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "addresses": r"ул\.\s?[А-ЯЁа-яё\s\d\-]+д\.\s?\d+[А-Яа-я]?"  # Примерный адрес
        }

        result = {}
        for key, pattern in patterns.items():
            matches = [(m.group(), m.start()) for m in re.finditer(pattern, cls.text)]
            result[key] = matches
        return result

    @classmethod
    def keyword_positions(cls, keywords: List[str]) -> Dict[str, List[int]] or None:
        """
        Поиск позиций ключевых слов.
        """
        if len(cls.text)==0:
            return None
        result = defaultdict(list)
        for word in keywords:
            for m in re.finditer(rf'\b{word}\w*', cls.text, re.IGNORECASE):
                result[word].append(m.start())
        return dict(result)

    @classmethod
    def find_numbers(cls, p1: int = 0, p2: int = None) -> List[Tuple[str, int, int]] or None:
        """
        Возвращает кортежи (число, позиция, длина) в диапазоне от p1 до p2.
        """
        if len(cls.text)==0:
            return None
        subtext = cls.text[p1:p2] if p2 else cls.text[p1:]
        return [(m.group(), p1 + m.start(), len(m.group()))
                for m in re.finditer(r'\d+([.,]\d+)?', subtext)]

    @classmethod
    def find_phone_numbers(cls) -> List[Tuple[str, int]] or None:
        """
        Поиск телефонов в тексте.
        """
        if len(cls.text)==0:
            return None
        return [(m.group(), m.start()) for m in re.finditer(r"\+?\d[\d\s\-()]{7,}\d", cls.text)]

    @classmethod
    def extract_sentences(cls) -> List[Tuple[int, int, int, int, str]]:
        """
        Возвращает кортежи (номер, позиция, число слов, число символов, тип предложения)
        """
        sentence_pattern = re.compile(r'([А-ЯЁA-Z][^.!?]*[.!?])', re.M | re.S)
        sentences = []
        for i, m in enumerate(re.finditer(sentence_pattern, cls.text), start=1):
            sentence = m.group().strip()
            pos = m.start()
            word_count = len(re.findall(r'\w+', sentence))
            char_count = len(sentence)
            kind = "повествовательное"
            if sentence.endswith("?"):
                kind = "вопросительное"
            elif sentence.endswith("!"):
                kind = "восклицательное"
            sentences.append((i, pos, word_count, char_count, kind))
        return sentences

    @classmethod
    def named_entity_stats(cls, names: List[str]) -> Dict[str, Tuple[List[int], int]] or None:
        """
        Словарь имён/персонажей -> (позиции, количество упоминаний)
        """
        if len(cls.text)==0:
            return None
        result = {}
        for name in names:
            positions = [m.start() for m in re.finditer(rf'\b{name}\b', cls.text)]
            if positions:
                result[name] = (positions, len(positions))
        return dict(sorted(result.items(), key=lambda x: -x[1][1]))

    @classmethod
    def html_tag_stats(cls) -> Dict[str, Tuple[List[int], List[int], int, int]] or None:
        """
        Возвращает словарь по тегам: открытие, закрытие, количество, длина тегов
        """
        if len(cls.text)==0:
            return None
        tags = defaultdict(lambda: ([], [], 0, 0))
        for m in re.finditer(r'<([a-zA-Z0-9]+)[^>]*>', cls.text):
            tag = m.group(1)
            start = m.start()
            tags[tag][0].append(start)
            tags[tag] = (
                tags[tag][0],
                tags[tag][1],
                tags[tag][2] + 1,
                tags[tag][3] + len(m.group())
            )
        for m in re.finditer(r'</([a-zA-Z0-9]+)>', cls.text):
            tag = m.group(1)
            tags[tag][1].append(m.start())
        return dict(tags)

    @classmethod
    def bag_of_words(cls) -> Dict[str, int] or None:
        if len(cls.text)==0:
            return None
        words = re.findall(r'\b[а-яА-Яa-zA-Z]{3,}\b', cls.text.lower())
        return dict(Counter(words))

    @classmethod
    def word_frequency_dict(cls) -> Dict[str, Tuple[List[int], int]] or None:
        if len(cls.text)==0:
            return None
        freq = defaultdict(list)
        for m in re.finditer(r'\b[а-яА-Яa-zA-Z]{3,}\b', cls.text):
            word = m.group().lower()
            freq[word].append(m.start())
        return dict(sorted({k: (v, len(v)) for k, v in freq.items()}.items(), key=lambda x: -x[1][1]))