#Второе
file1 = "text.txt"
file2 = "analysis_report.txt"

try:
    
    with open(file1, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    num_lines = len(lines)
    num_chars = 0
    num_words = 0
    
    word_count = {}
    
    for line in lines:
        num_chars += len(line)
        
        words = line.split()
        num_words += len(words)
        
        for w in words:
            w = w.strip(".,!?;:()\"'")
            if w:
                word = w.lower()
                word_count[word] = word_count.get(word, 0) + 1
    

    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    top5 = sorted_words[:5]
    
    with open(file2, "w", encoding="utf-8") as report:
        report.write(f"Имя файла: {file1}\n")
        report.write(f"Количество строк: {num_lines}\n")
        report.write(f"Количество слов: {num_words}\n")
        report.write(f"Количество символов: {num_chars}\n")
        report.write("\n5 самых частых слов:\n")
        for word, freq in top5:
            report.write(f"{word}: {freq}\n")
    
    print(f"Строк: {num_lines}, слов: {num_words}, символов: {num_chars}")
    print("Топ-5 слов:")
    for w, f in top5:
        print(f"  {w} - {f}")

except FileNotFoundError:
    print(f"Ошибка: файл '{file1}' не найден. Проверьте, существует ли он.")
except PermissionError:
    print(f"Ошибка: нет прав для чтения или записи.")
except UnicodeDecodeError:
    print("Ошибка: не удалось прочитать файл — возможно, неверная кодировка. Используйте UTF-8.")
except Exception as e:
    print(f"Непредвиденная ошибка: {e}")