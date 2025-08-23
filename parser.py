import requests
import concurrent.futures
import time
from typing import Dict, List
from bs4 import BeautifulSoup

class FragmentParser:
    def __init__(self):
        self.base_url = "https://fragment.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def check_username_status(self, username: str) -> Dict:
        """Проверяет доступность на Fragment - ищет только статус Unavailable"""
        url = f"{self.base_url}/username/{username}"
        
        try:
            start_time = time.time()
            response = self.session.get(url, headers=self.headers, timeout=8)
            request_time = time.time() - start_time
            
            if response.status_code == 200:
                html = response.text
                
                # ПРОСТАЯ ПРОВЕРКА: ищем только статус Unavailable
                if 'Unavailable' in html:
                    status = 'Available'
                    reason = 'Свободен (Unavailable)'
                    available = True
                    print(f"   ✅ {username} - СВОБОДЕН ({request_time:.1f}s)")
                else:
                    status = 'Taken'
                    reason = 'Занят (не Unavailable)'
                    available = False
                    print(f"   ❌ {username} - ЗАНЯТ ({request_time:.1f}s)")
                
                result = {
                    'username': username,
                    'status': status,
                    'reason': reason,
                    'available': available,
                    'url': url,
                    'response_time': round(request_time, 2),
                    'success': True
                }
                
                return result
                
            elif response.status_code == 404:
                # 404 обычно означает что юзернейм свободен
                result = {
                    'username': username,
                    'status': 'Available',
                    'reason': 'Страница не найдена (404)',
                    'available': True,
                    'url': url,
                    'response_time': round(request_time, 2),
                    'success': True
                }
                print(f"   ✅ {username} - СВОБОДЕН (404) ({request_time:.1f}s)")
                return result
                
            else:
                result = {
                    'username': username,
                    'status': f'HTTP {response.status_code}',
                    'reason': f'Ошибка HTTP: {response.status_code}',
                    'available': False,
                    'url': url,
                    'response_time': round(request_time, 2),
                    'success': False
                }
                print(f"   ❌ {username} - Ошибка HTTP {response.status_code} ({request_time:.1f}s)")
                return result
                
        except requests.exceptions.Timeout:
            result = {
                'username': username,
                'status': 'Timeout',
                'reason': 'Таймаут запроса',
                'available': False,
                'url': url,
                'response_time': 0,
                'success': False
            }
            print(f"   ⚠️ {username} - Таймаут запроса")
            return result
            
        except requests.exceptions.ConnectionError:
            result = {
                'username': username,
                'status': 'ConnectionError',
                'reason': 'Ошибка подключения',
                'available': False,
                'url': url,
                'response_time': 0,
                'success': False
            }
            print(f"   ⚠️ {username} - Ошибка подключения")
            return result
            
        except Exception as e:
            result = {
                'username': username,
                'status': f'Error: {type(e).__name__}',
                'reason': f'Ошибка: {str(e)}',
                'available': False,
                'url': url,
                'response_time': 0,
                'success': False
            }
            print(f"   ⚠️ {username} - Ошибка: {type(e).__name__}")
            return result

    def check_usernames_batch(self, usernames: List[str], max_workers: int = 15) -> List[Dict]:
        """Многопоточная проверка юзернеймов"""
        start_time = time.time()
        results = []
        
        print(f"🔍 Проверка {len(usernames)} юзернеймов:")
        print("─" * 60)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Отправляем все задачи
            future_to_username = {
                executor.submit(self.check_username_status, username): username 
                for username in usernames
            }
            
            # Собираем результаты по мере готовности
            completed = 0
            for future in concurrent.futures.as_completed(future_to_username):
                username = future_to_username[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1
                    
                    # Прогресс
                    if completed % 5 == 0:
                        elapsed = time.time() - start_time
                        speed = completed / (elapsed / 60)
                        percent = (completed / len(usernames)) * 100
                        print(f"   📊 Прогресс: {completed}/{len(usernames)} ({percent:.0f}%) | Скорость: {speed:.0f}/мин")
                        
                except Exception as e:
                    error_result = {
                        'username': username,
                        'status': f'Future Error: {type(e).__name__}',
                        'reason': f'Ошибка выполнения: {str(e)}',
                        'available': False,
                        'url': f"{self.base_url}/username/{username}",
                        'response_time': 0,
                        'success': False
                    }
                    results.append(error_result)
                    print(f"   ⚠️ {username} - Ошибка выполнения: {type(e).__name__}")
                    completed += 1
        
        total_time = time.time() - start_time
        usernames_per_minute = len(usernames) / (total_time / 60)
        
        print("─" * 60)
        print(f"⏱️  Проверено {len(usernames)} юзернеймов за {total_time:.1f} сек")
        print(f"🚀 Скорость: {usernames_per_minute:.0f} юзернеймов/мин")
        
        return results