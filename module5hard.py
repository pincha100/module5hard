import hashlib
import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    def hash_password(self, password):
        """Хэширует пароль с использованием hashlib"""
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)
class UrTube:
    def __init__(self):
        self.users = []  # Список пользователей
        self.videos = []  # Список видео
        self.current_user = None  # Текущий пользователь

     # Метод регистрации
    def register(self, nickname, password, age):
        if self.find_user(nickname):
            print(f"Пользователь {nickname} уже существует")
        else:
            new_user = User(nickname, password, age)
            self.users.append(new_user)
            self.current_user = new_user
            print(f"Пользователь {nickname} зарегистрирован и вошел в систему")
 # Метод авторизации
    def log_in(self, nickname, password):
        user = self.find_user(nickname)
        if user and user.password == User(nickname, password).hash_password(password):
            self.current_user = user
            print(f"Пользователь {nickname} вошел в систему")
        else:
            print("Неверный логин или пароль")

    # Метод выхода из аккаунта
    def log_out(self):
        if self.current_user:
            print(f"Пользователь {self.current_user.nickname} вышел из системы")
            self.current_user = None
        else:
            print("Нет активных сессий для выхода")

    # Поиск пользователя по nickname
    def find_user(self, nickname):
        for user in self.users:
            if user.nickname == nickname:
                return user
        return None

    # Метод добавления видео
    def add(self, *new_videos):
        for video in new_videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f"Видео '{video.title}' добавлено")
            else:
                print(f"Видео '{video.title}' уже существует")

    # Метод поиска видео по ключевому слову
    def get_videos(self, search_term):
        search_term = search_term.lower()
        return [video.title for video in self.videos if search_term in video.title.lower()]

    # Метод просмотра видео
    def watch_video(self, title):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        video = next((v for v in self.videos if v.title == title), None)
        if not video:
            print(f"Видео с названием '{title}' не найдено")
            return

        if video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        print(f"Воспроизведение видео '{video.title}'")
        for second in range(video.time_now + 1, video.duration + 1):
            print(f"Проигрывается секунда {second}")
            time.sleep(1)  # Задержка в 1 секунду для симуляции воспроизведения
        print("Конец видео")
        video.time_now = 0  # Сброс времени просмотра


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0  # Время остановки воспроизведения
        self.adult_mode = adult_mode


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')