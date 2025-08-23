import random
from typing import List

class UsernameGenerator:
    def __init__(self):
        # Словари для генерации (только 4+ символов)
        self.short_words = [
            'apex', 'nova', 'zeno', 'flux', 'core', 'vibe', 'neon', 'luxe', 'maxx', 'prime',
            'echo', 'bolt', 'blaze', 'frost', 'storm', 'shadow', 'phantom', 'ghost', 'stealth',
            'quant', 'cosmic', 'orbit', 'pulse', 'spark', 'flare', 'glitch', 'cyber', 'digital',
            'alpha', 'omega', 'sigma', 'delta', 'gamma', 'nexus', 'vertex', 'matrix', 'proton',
            'photon', 'electron', 'vortex', 'infinity', 'eternity', 'velocity', 'momentum'
        ]
        
        self.medium_words = [
            'quantum', 'cosmic', 'atomic', 'crystal', 'diamond', 'silver', 'golden',
            'platinum', 'premium', 'elite', 'expert', 'master', 'legend', 'mythic',
            'epic', 'rare', 'unique', 'special', 'supreme', 'digital', 'virtual'
        ]
        
        self.prefixes = ['super', 'mega', 'ultra', 'hyper', 'neo', 'pro', 'alpha', 'omega']
        self.suffixes = ['tech', 'net', 'hub', 'lab', 'zone', 'world', 'space', 'time']

    def generate_short_usernames(self, count: int = 20) -> List[str]:
        """Генерация 4-5 символьных юзернеймов"""
        usernames = set()
        
        # Только слова из 4-5 символов
        valid_words = [w for w in self.short_words if 4 <= len(w) <= 5]
        
        for _ in range(count):
            if valid_words and random.random() < 0.7:
                username = random.choice(valid_words)
            else:
                # Генерация 4-5 буквенных комбинаций
                length = random.choice([4, 5])
                username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
            
            usernames.add(username)
        
        return list(usernames)[:count]

    def generate_english_usernames(self, count: int = 20) -> List[str]:
        """Генерация английских слов юзернеймов (4+ символов)"""
        usernames = set()
        
        # Только слова от 4 символов
        short_valid = [w for w in self.short_words if len(w) >= 4]
        medium_valid = [w for w in self.medium_words if len(w) >= 4]
        
        for _ in range(count):
            if random.random() < 0.6 and short_valid:
                username = random.choice(short_valid)
            elif medium_valid:
                username = random.choice(medium_valid)
            else:
                # Запасной вариант
                length = random.randint(4, 6)
                username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
            
            if len(username) >= 4:
                usernames.add(username)
        
        return list(usernames)[:count]

    def generate_combined_usernames(self, count: int = 20) -> List[str]:
        """Генерация комбинированных юзернеймов (6+ символов)"""
        usernames = set()
        
        for _ in range(count):
            if random.random() < 0.5:
                # Префикс + слово
                prefix = random.choice(self.prefixes)
                word = random.choice([w for w in self.short_words if len(w) >= 3])
                username = prefix + word
            else:
                # Слово + суффикс
                word = random.choice([w for w in self.short_words if len(w) >= 3])
                suffix = random.choice(self.suffixes)
                username = word + suffix
            
            # Ограничиваем длину 4-8 символами
            if 8 <= len(username) <= 12:
                usernames.add(username)
        
        return list(usernames)[:count]

    def generate_batch(self, count: int = 50) -> List[str]:
        """Генерация батча юзернеймов"""
        short = self.generate_short_usernames(count // 3)
        english = self.generate_english_usernames(count // 3)
        combined = self.generate_combined_usernames(count // 3)
        
        # Фильтруем только 4+ символьные
        all_usernames = [u for u in short + english + combined if len(u) >= 4]
        all_usernames = list(set(all_usernames))
        random.shuffle(all_usernames)
        
        return all_usernames[:count]