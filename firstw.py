#Первое
import csv

filename = "sales.csv"

try:

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        
        header = next(reader)
    
        products = []
        total = 0
        
        for row in reader:
            
            if len(row) != 3:
                print(f"Пропущена строка: {row} (неверное количество данных)")
                continue
            
            name = row[0]
            
            try:
                quantity = int(row[1])
                price = float(row[2])
            except ValueError:
                print(f"Пропущена строка: {row} (не числа)")
                continue
            
            cost = quantity * price
            products.append([name, quantity, price, cost])
            total += cost
        
        print(f"{'Товар':<15} {'Количество':<10} {'Цена':<10} {'Стоимость':<10}")
        print("-" * 45)
        for p in products:
            print(f"{p[0]:<15} {p[1]:<10} {p[2]:<10.2f} {p[3]:<10.2f}")
        print("-" * 45)
        print(f"{'ИТОГО':<15} {'':<10} {'':<10} {total:<10.2f}")

except FileNotFoundError:
    print(f"Ошибка: Файл не найден.")
except PermissionError:
    print(f"Ошибка: Нет прав для чтения файла.")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")