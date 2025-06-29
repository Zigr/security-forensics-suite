import unittest
import os
import shutil
import hashlib
from tempfile import TemporaryDirectory
from tg_abuse.utils.dir_balanced_filename import DirBalancedFilename


class TestDirBalancedFilename(unittest.TestCase):
    def setUp(self):
        # Використовуємо тимчасову директорію для тестів
        self.test_root_dir = TemporaryDirectory().name

    def tearDown(self):
        # Видаляємо тимчасову директорію після тестів
        if os.path.exists(self.test_root_dir):
            shutil.rmtree(self.test_root_dir)

    def test_generate_file_hash(self):
        # Тестуємо генерацію хешу
        file_manager = DirBalancedFilename(self.test_root_dir)
        file_manager.set_rel_filename("test_file.txt")

        user_id = 123
        expected_hash = hashlib.sha256(
            f"{user_id}-test_file.txt".encode("utf-8")
        ).hexdigest()

        file_hash = file_manager.generate_file_hash(user_id, file_manager.rel_filename)

        # Перевіряємо, що згенерований хеш співпадає з очікуваним
        self.assertEqual(file_hash, expected_hash)

    def test_get_full_filename_with_hash(self):
        # Тестуємо отримання шляху до файлу з хешем
        file_manager = DirBalancedFilename(self.test_root_dir)
        file_manager.set_dir_num(1203).set_rel_filename("test_file.txt")

        user_id = 123
        expected_file_hash = hashlib.sha256(
            f"{user_id}-test_file.txt".encode("utf-8")
        ).hexdigest()

        full_path = file_manager.get_full(user_id, create_rel_dir=True)
        expected_full_path = os.path.join(
            self.test_root_dir, "1001-2000", "1203", f"{expected_file_hash}.bin"
        )

        # Перевіряємо, чи правильний повний шлях до файлу
        self.assertEqual(full_path, expected_full_path)

    def test_directory_creation(self):
        # Тестуємо, чи створюються необхідні каталоги
        file_manager = DirBalancedFilename(self.test_root_dir)
        file_manager.set_dir_num(1203).set_rel_filename("test_file.txt")

        user_id = 123
        full_path = file_manager.get_full(user_id, create_rel_dir=True)

        # Перевіряємо, що каталоги були створені
        self.assertTrue(os.path.exists(os.path.dirname(full_path)))

    def test_directory_not_exist(self):
        # Тестуємо випадок, коли каталоги ще не існують
        file_manager = DirBalancedFilename(self.test_root_dir)
        file_manager.set_dir_num(9999).set_rel_filename("new_file.txt")

        user_id = 456
        full_path = file_manager.get_full(user_id, create_rel_dir=True)
        expected_full_path = os.path.join(
            self.test_root_dir, "9001-10000", "9999", "new_file.txt"
        )

        # Перевіряємо, що шлях до файлу був правильно створений
        self.assertEqual(full_path, expected_full_path)
        self.assertTrue(os.path.exists(os.path.dirname(full_path)))


if __name__ == "__main__":
    unittest.main()
