from functools import reduce
from datetime import datetime

class Book:
    def __init__(self, code: str, title: str, author: str, genre: str, year: int, borrowings: int):
            self.__code = code
            self.title = title
            self.author = author
            self.genre = genre
            self.year = year
            self.borrowings = borrowings

    @property
    def code(self):
        return self.__code

    def __str__(self):
        return f"Kód knihy: {self.code:5} | Názov: {self.title:20} | Autor: {self.author:20} | Žáner: {self.genre:10}  | Počet výpožičiek: {self.borrowings:>3}"

class FileHandler:
    @staticmethod
    def read_alltime_stats():
        try:
            with open("audit_stats.txt", encoding="utf-8-sig") as file:
                for line in file:
                    line = line.strip().split(" ")
                return int(line[1])
        except FileNotFoundError:
             return 0

    @staticmethod
    def write_alltime_stats(number):
        with open("audit_stats.txt", "w", encoding="utf-8") as file:
            file.write(f"alltime_stats {number}")
        return True
        
    @staticmethod
    def read_bookfile(filename):
        year = datetime.now().year
        new_list = []
        try:
            with open(filename, encoding="utf-8-sig") as file:
                is_file_valid = True
                for line in file:
                    line = line.strip().split(",")
                    line[4] = int(line[4])
                    line[5] = int(line[5])
                    if line[4] > year or line[5] < 0:
                        is_file_valid = False
                        break
                    book = (line[0], line[1], line[2], line[3], line[4], line[5])
                    new_list.append(book)
            
            if is_file_valid:
                return new_list
            return False    
        
        except FileNotFoundError:
            print("Súbor sa nenašiel")
                                              

class Library:
    total_processed_books_counter = 0

    def __init__(self):
        self.books = {}

    def get_alltime_stats(self):
        Library.total_processed_books_counter = FileHandler.read_alltime_stats()

    def save_alltime_stats(self):
        saved = FileHandler.write_alltime_stats(Library.total_processed_books_counter)
        if saved:
            return True

    def process_bookfile(self, file):
        book_list = FileHandler.read_bookfile(file)
        if book_list:
            for item in book_list:
                self.books[item[0]] = Book(item[0], item[1], item[2], item[3], item[4], item[5])
                Library.total_processed_books_counter += 1
            print("Knihy úspešne zaevidované.")
        else:
            print("Súbor obsahuje nesprávný rok alebo záporný počet výpožičiek. Knihy neboli zaevidované.")

    def find_books_by_genre(self, searched_genre: str):
        return list(filter(lambda book: book.genre.lower() == searched_genre.lower(), self.books.values()))

    def count_total_borrowings(self):
        return reduce(lambda total, book: total + book.borrowings, self.books.values() , 0)

   
class App:
    def __init__(self):
        self.library = Library()

    def welcome(self):
        print("=== AUDIT KNIŽNICE ===")
        print("1 - Načítať súbor kníh")
        print("2 - Vyhľadať knihy podľa žánru")
        print("3 - Zobraziť celkovú bilanciu výpožičiek")
        print("4 - Zobraziť všetky zaevidované knihy zo súboru")
        print("0 - Ukončiť program")
        print("")

    def execute(self):
        self.library.get_alltime_stats()
        self.welcome()

        while True:
            command = input("Zadajte príkaz: ")
               
            if command == "0":
                if self.library.save_alltime_stats():
                    print("Dáta úspešne zálohované do audit_stats.txt. Program sa ukončuje.")
                    print(f"Historicky spracovaných kníh od prvého spustenia: {Library.total_processed_books_counter}")
                    break

            elif command == "1":
                file = input("Názov súboru: ")
                self.library.process_bookfile(file)
                print("")

            elif command == "2":
                genre = input("Zadajte žáner: ")
                found_books = self.library.find_books_by_genre(genre)
                print("=== ZOZNAM NÁJDENÝCH KNÍH ===")
                for book in found_books:
                    print(f"Kniha: {book.title.upper():20} | Vypožičané: {book.borrowings}-krát")
                print("")

            elif command == "3":
                print(f"Celkový počet výpožičiek všetkých kníh v aktuálnej pamäti: {self.library.count_total_borrowings()}")
                print("")

            elif command == "4":
                if self.library.books:
                    for book in self.library.books.values():
                        print(book)
                else:
                    print("V pamäti sa momentálne nenachádzajú žiadne knihy. Načítajte naprv súbor.")



App().execute()
