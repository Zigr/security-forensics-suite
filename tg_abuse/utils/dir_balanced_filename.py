import os
import hashlib

DIRS_BALANCE_MAX = 1000

class DirBalancedFilename:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.dir_num = 0
        self.rel_filename = ''

    def set_root_dir(self, root_dir):
        self.root_dir = root_dir
        return self

    def set_dir_num(self, dir_num):
        self.dir_num = dir_num
        return self

    def set_rel_filename(self, rel_filename):
        self.rel_filename = rel_filename
        return self

    def get_rel_filename(self):
        return self.rel_filename

    def get_from_balance(self):
        return ((self.dir_num - 1) // DIRS_BALANCE_MAX) * DIRS_BALANCE_MAX

    def get_rel_dir(self):
        return f"{self.get_from_balance() + 1}-{self.get_from_balance() + DIRS_BALANCE_MAX}"

    def get_full_rel_dir(self):
        return os.path.join(self.get_rel_dir(), str(self.dir_num))

    def get_full_dir(self):
        return os.path.join(self.root_dir, self.get_rel_dir(), str(self.dir_num))

    def generate_file_hash(self, user_id, filename):
        # Створення унікального хешу на основі UserID та імені файлу
        hash_input = f"{user_id}-{filename}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()

    def get_full(self, user_id, create_rel_dir=True):
        # Генерація хешу для файлу
        file_hash = self.generate_file_hash(user_id, self.rel_filename)
        
        # Генерація директорії та шляху для файлу
        rel_dir = self.get_rel_dir()
        full_dir = self.get_full_dir()

        # Створення необхідних директорій
        if create_rel_dir:
            os.umask(0)
            if not os.path.isdir(os.path.join(self.root_dir, rel_dir)):
                os.makedirs(os.path.join(self.root_dir, rel_dir), mode=0o777, exist_ok=True)
            if not os.path.isdir(full_dir):
                os.makedirs(full_dir, mode=0o777, exist_ok=True)

        # Повертаємо повний шлях до файлу з хешем
        return os.path.join(full_dir, f"{file_hash}.bin")

# Usage example:
root_dir = '/path/to/root/directory'
file_manager = DirBalancedFilename(root_dir)
file_manager.set_dir_num(1203).set_rel_filename('example_file.txt')

# Приклад користувача з UserID
user_id = 123
file_path = file_manager.get_full(user_id, create_rel_dir=True)

print(f"Full file path: {file_path}")
