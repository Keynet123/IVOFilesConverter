import os

table_files = ["csv", "xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt", "db"]

template = {
    "headers": [],
    "rows": [],
}


class FileConverter:
    def get_file_name(self, path: str):
        """Извлекает имя файла из пути, игнорируя разделители.

        Args:
            path: Путь к файлу.

        Returns:
            Имя файла.
        """
        return os.path.basename(path)

    def get_table(self, path: str, splitter = ","):
        """Извлекает таблицу из файла.

        Args:
            path: Путь к файлу.

        Returns:
            Таблица.
        """
        if path.split(".")[-1] == "csv":
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
                headers = data.split("\n")[0].split(",")
                rows = data.split("\n")[1:]
                template["headers"] = headers
                template["rows"] = rows
                return template

    def set_table(self, path: str, table: dict):
        """Записывает таблицу в файла.

        Args:
            path: Путь к файлу.
            table: Таблица.
        """
        if path.split(".")[-1] == "db":
            import sqlite3

            conn = sqlite3.connect(path)
            cur = conn.cursor()

            headers = table["headers"]
            rows = table["rows"]

            cur.execute(f"CREATE TABLE IF NOT EXISTS test ({headers})")

            for row in rows:
                cur.execute(f"INSERT INTO test ({headers}) VALUES ({row})")

    def convert(self, input_path: str, output_path: str, splitter=","):
        """Конвертирует файлы из IVOfiles в IVOfiles.

        Args:
            input_path: Путь к файлу.
            output_path: Путь к сохраняемому файлу.
        """

        input_path = self.get_file_name(input_path)
        output_path = self.get_file_name(output_path)

        if input_path in table_files:
            print(f"Converting {input_path} to {output_path}")
            table = self.get_table(input_path, splitter)
            
        if output_path in table_files:
            self.set_table(output_path, table)
        
        print("Завершено!")