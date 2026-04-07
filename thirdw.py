import json
import csv
import os

LOG_FILE = "converter_log.txt"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Ошибка: неверный формат JSON.")
        return None
    except:
        print("Ошибка: не удалось прочитать JSON.")
        return None

def load_csv(path):
    data = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                print("Ошибка: в CSV нет заголовков (первая строка).")
                return None
            rows = list(reader)
            if len(rows) == 0:
                print("Ошибка: в CSV только заголовки, нет строк с данными.")
                return None
            for i, row in enumerate(rows, start=2):
                if len(row) != len(reader.fieldnames):
                    print(f"Ошибка: строка {i} содержит {len(row)} полей, ожидалось {len(reader.fieldnames)}.")
                    return None
            data = rows
        return data
    except Exception as e:
        print(f"Ошибка чтения CSV: {e}")
        return None

def load_txt(path):
    data = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print("Ошибка: файл TXT пуст.")
            return None
        headers = lines[0].strip().split('\t')
        if not headers:
            print("Ошибка: первая строка TXT не содержит заголовков.")
            return None
        if len(lines) == 1:
            print("Ошибка: в TXT только заголовки, нет данных.")
            return None
        for i, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line:
                continue
            vals = line.split('\t')
            if len(vals) != len(headers):
                print(f"Ошибка: строка {i} содержит {len(vals)} полей, ожидалось {len(headers)}.")
                return None
            data.append({headers[j]: vals[j] for j in range(len(headers))})
        if not data:
            print("Ошибка: в TXT нет корректных строк с данными.")
            return None
        return data
    except Exception as e:
        print(f"Ошибка чтения TXT: {e}")
        return None

def save_json(data, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        print("Ошибка записи JSON.")
        return False

def save_csv(data, path):
    if not data:
        print("Нет данных для сохранения.")
        return False
    try:
        with open(path, "w", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True
    except:
        print("Ошибка записи CSV.")
        return False

def save_txt(data, path):
    if not data:
        print("Нет данных для сохранения.")
        return False
    try:
        with open(path, "w", encoding="utf-8") as f:
            headers = list(data[0].keys())
            f.write('\t'.join(headers) + '\n')
            for row in data:
                f.write('\t'.join(str(row.get(h, "")) for h in headers) + '\n')
        return True
    except:
        print("Ошибка записи TXT.")
        return False

def convert(in_path, out_path, in_fmt, out_fmt):
    if in_fmt == "json":
        data = load_json(in_path)
    elif in_fmt == "csv":
        data = load_csv(in_path)
    else:
        data = load_txt(in_path)
    
    if data is None:
        return False
    
    if in_fmt == "json":
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            data = [{"value": str(data)}]
        elif data and not isinstance(data[0], dict):
            data = [{"value": str(x)} for x in data]
    
    if out_fmt == "json":
        return save_json(data, out_path)
    elif out_fmt == "csv":
        return save_csv(data, out_path)
    else:
        return save_txt(data, out_path)

def main():
    print("Конвертер: json, csv, txt")
    in_fmt = input("Входной формат(например: json, csv, txt): ").strip().lower()
    out_fmt = input("Выходной формат(например: json, csv, txt): ").strip().lower()
    if in_fmt == out_fmt:
        print("Форматы одинаковы, конвертация не нужна.")
        return
    in_path = input("Входной файл(например: j1.json, c1.csv, t.txt): ").strip()
    out_path = input("Выходной файл(например: j1.json, c1.csv, t.txt): ").strip()
    
    if not os.path.exists(in_path):
        print("Файл не найден.")
        return
    
    if convert(in_path, out_path, in_fmt, out_fmt):
        print("Конвертация выполнена успешно.")
        log(f"OK: {in_fmt} -> {out_fmt}")
    else:
        print("Конвертация не удалась.")
        log(f"FAIL: {in_fmt} -> {out_fmt}")

if __name__ == "__main__":
    main()