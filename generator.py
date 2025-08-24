import random
import string
from typing import List, Set

class UsernameGenerator:
    def __init__(self):
        self.used_usernames: Set[str] = set()
        
        # Популярные английские слова
        self.popular_words = [
            'time', 'space', 'code', 'data', 'tech', 'byte', 'bit', 'net', 'web',
            'cloud', 'game', 'play', 'fun', 'cool', 'nice', 'good', 'best', 'fast',
            'quick', 'smart', 'clever', 'wise', 'bold', 'brave', 'calm', 'dark',
            'light', 'fire', 'water', 'earth', 'air', 'wind', 'wave', 'star',
            'moon', 'sun', 'love', 'life', 'live', 'free', 'true', 'real', 'pure',
            'nova', 'zen', 'flux', 'core', 'vibe', 'neo', 'lux', 'max', 'prime',
            'echo', 'bolt', 'blaze', 'frost', 'storm', 'shadow', 'ghost', 'pulse',
            'spark', 'flare', 'glitch', 'cyber', 'digital', 'alpha', 'omega'
        ]
        
        self.prefixes = ['super', 'mega', 'ultra', 'hyper', 'neo', 'pro', 'alpha', 'omega']
        self.suffixes = ['tech', 'net', 'hub', 'lab', 'zone', 'world', 'space', 'time']

    def generate_4char_usernames(self, count: int) -> List[str]:
        """Генерация 4-символьных юзернеймов"""
        usernames = []
        attempts = 0
        
        while len(usernames) < count and attempts < 1000:
            # 1. Случайные буквы
            if random.random() < 0.6:
                username = ''.join(random.choices(string.ascii_lowercase, k=4))
            # 2. Короткие слова
            else:
                short_words = [w for w in self.popular_words if len(w) == 4]
                if short_words:
                    username = random.choice(short_words)
                else:
                    username = ''.join(random.choices(string.ascii_lowercase, k=4))
            
            if username not in self.used_usernames:
                self.used_usernames.add(username)
                usernames.append(username)
            
            attempts += 1
        
        return usernames

    def generate_5char_usernames(self, count: int) -> List[str]:
        """Генерация 5-символьных юзернеймов"""
        usernames = []
        attempts = 0
        
        while len(usernames) < count and attempts < 1000:
            # 1. Случайные буквы
            if random.random() < 0.5:
                username = ''.join(random.choices(string.ascii_lowercase, k=5))
            # 2. Короткие слова
            elif random.random() < 0.7:
                short_words = [w for w in self.popular_words if len(w) == 5]
                if short_words:
                    username = random.choice(short_words)
                else:
                    username = ''.join(random.choices(string.ascii_lowercase, k=5))
            # 3. Префикс + буква
            else:
                prefix = random.choice(self.prefixes)
                if len(prefix) == 4:
                    username = prefix + random.choice(string.ascii_lowercase)
                else:
                    username = ''.join(random.choices(string.ascii_lowercase, k=5))
            
            if username not in self.used_usernames:
                self.used_usernames.add(username)
                usernames.append(username)
            
            attempts += 1
        
        return usernames

    def generate_english_words(self, count: int) -> List[str]:
        """Генерация английских слов"""
        usernames = []
        attempts = 0
        
        while len(usernames) < count and attempts < 1000:
            # Берем популярные слова разной длины
            word = random.choice(self.popular_words)
            
            if word not in self.used_usernames and 4 <= len(word) <= 8:
                self.used_usernames.add(word)
                usernames.append(word)
            
            attempts += 1
        
        return usernames

    def generate_batch(self, count: int, category: str = "4char") -> List[str]:
        """Генерация батча юзернеймов по категории"""
        if category == "4char":
            usernames = self.generate_4char_usernames(count)
        elif category == "5char":
            usernames = self.generate_5char_usernames(count)
        elif category == "english":
            usernames = self.generate_english_words(count)
        else:
            usernames = self.generate_4char_usernames(count)
        
        print(f"🎲 Сгенерировано {len(usernames)} юзернеймов (категория: {category})")
        if usernames:
            print(f"📋 Примеры: {', '.join(usernames[:3])}...")
        
        return usernames

    def clear_used_usernames(self):
        """Очистка истории использованных юзернеймов"""
        self.used_usernames.clear()
        print("🧹 История юзернеймов очищена")