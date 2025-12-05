import csv
import re
from pathlib import Path
import os

table_files = ["csv", "xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt", "db"]

template = {
    "name": "",
    "headers": [],
    "rows": [],
}

class FileConverter:
    def get_absolute_path(self, relative_path: str):
        """Возвращает абсолютный путь исходя из текущей рабочей директории."""
        return (Path(os.getcwd()) / relative_path).resolve()

    def sanitize_header(self, header):
        """Удаляет/заменяет неподдерживаемые символы в заголовках таблицы для SQLite."""
        return re.sub(r'\W|^(?=\d)', '_', header)

    def get_table(self, path: str):
        """Извлекает таблицу из CSV-файла с учетом сложных значений."""
        if path.split(".")[-1] == "csv":
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                headers = next(reader)  # Первая строка - заголовки
                headers = [self.sanitize_header(header) for header in headers]  # Преобразуем заголовки
                rows = [row for row in reader]  # Остальные строки - данные

                # Сохраняем имя файла без расширения и заменяем точки на нижние подчеркивания
                template["name"] = Path(path).stem.replace(".", "_")
                template["headers"] = headers
                template["rows"] = rows
                return template

    def set_table(self, path: str, table: dict):
        """Записывает таблицу в SQLite базу данных."""
        if path.split(".")[-1] == "db":
            import sqlite3

            conn = sqlite3.connect(path)
            cur = conn.cursor()

            headers = ", ".join(table["headers"])
            name = template["name"]
            placeholders = ", ".join(["?" for _ in table["headers"]])

            # Создаем таблицу, если она не существует
            cur.execute(f"CREATE TABLE IF NOT EXISTS {name} ({headers})")

            for row in table["rows"]:
                # Если строка короче заголовков, заполняем недостающие элементы None
                if len(row) < len(table["headers"]):
                    row += [None] * (len(table["headers"]) - len(row))
                cur.execute(f"INSERT INTO {name} ({headers}) VALUES ({placeholders})", row)

            conn.commit()
            conn.close()

    def convert(self, input_path: str, output_path: str):
        """Конвертирует файлы из IVOfiles в IVOfiles.

        Args:
            input_path: Путь к файлу.
            output_path: Путь к сохраняемому файлу.
        """
        # Преобразуем относительные пути в абсолютные
        input_path = self.get_absolute_path(input_path)
        output_path = self.get_absolute_path(output_path)
        table = None
        print(input_path.suffix[1:])
        if input_path.suffix[1:] in table_files:  # suffix возвращает расширение с точкой
            print(f"Converting {input_path} to {output_path}")
            table = self.get_table(str(input_path))

        if output_path.suffix[1:] in table_files:
            self.set_table(str(output_path), table)

        print("Завершено!")

# Пример вызова
FileConverter().convert(r"C:\Users\Home\PycharmProjects\projects\IvoFilesConverter\src\tests\example_2.5kb.csv", "test.db")
