# Dokumentacja Projektu: Multi-Client Server

Projekt to prosta aplikacja klient-serwer napisana w Pythonie, wykorzystująca gniazda (sockets), wielowątkowość (threading) oraz mechanizmy serializacji danych (pickle). Aplikacja symuluje serwer przechowujący dane o pojazdach oraz klientów, którzy mogą żądać od serwera obiektów określonych klas.

## 🛠 Struktura plików

- **pojazdy.py**: Definicje modeli danych (klasy pojazdów).
- **server.py**: Logika serwera obsługującego limitowanych, współbieżnych klientów.
- **client.py**: Logika klienta komunikującego się z serwerem po TCP.
- **test_app.py**: Zestaw zautomatyzowanych testów jednostkowych, integracyjnych i end-to-end (E2E).

---

## 🚗 1. Modele danych (`pojazdy.py`)
W tym pliku zdefiniowano pustą klasę bazową `Pojazd` oraz trzy klasy po niej dziedziczące: `Samochod`, `Motocykl`, `Rower`.

Każda z klas nadpisuje odpowiednie metody specjalne ("dunder methods"):
- `__init__`: Konstruktor inicjalizujący właściwości obiektu (np. marka, rocznik).
- `__str__`: Zwraca czytelny dla człowieka format tekstowy reprezentacji instancji.
- `__eq__`: Pozwala na logiczne porównanie czy dwa osobne pojazdy (np. w pamięci komputera) mają dokładnie takie same, kluczowe atrybuty.

---

## 🖥 2. Serwer (`server.py`)
Klasa `Server` pełni rolę wielowątkowego serwera TCP opartego o wbudowaną bibliotekę `socket`.
- **Automatyczne dane**: Przy uruchomieniu serwer tworzy słownik (`self.obiekty`) stanowiący jego mapę bazy danych. Wypełnia ją po 4 instancjami każdego typu pojazdu, co daje razem 12 rekordów.
- **Połączenia (Wielowątkowość)**: Serwer bez końca nasłuchuje na wskazanym porcie (5000). Każdy zakwalifikowany klient obsłużony zostaje na odrębnym wątku (za pomocą modułu `threading`), co sprawia, że klienci pobierają dane bez wstrzymywania i blokowania siebie nawzajem.
- **Limit użytkowników (`MAX_CLIENTS = 3`)**: Za pomocą obiektu `threading.Lock()` serwer wysoce bezpiecznie inkrementuje i modyfikuje licznik aktywnych klientów, upewniając się, że współdzielona pamięć nie zgłosi błędu wyścigu. Gdy na serwerze przebywają 3 osoby, serwer zamyka strumień czwartej ze statusem `"REFUSED"`.
- **Wymiana i Serializacja**:
  - Serwer po połączeniu wyłapuje ID klienta. Jeśli go przepuści przez Locka, odsyła `"OK"`.
  - Klient wysyła żądaną klasę (np. `"Samochod"`).
  - Wyszukiwanie: Serwer filtruje swój słownik i ładuje listę. Jeśli klient zapytał o klasę, której w ogóle nie ma - serwer wrzuca przez bibliotekę `pickle` liczbę `404`. W przeciwnym razie - pakuje pełnoprawną listę.
  - Symulacja: Pomiędzy żądaniem a wysłaniem serwer symuluje czas ładowania bazy za pomocą `time.sleep()`.

---

## 💻 3. Klient (`client.py`)
Klasa `Client` odpowiada za wirtualnego użytkownika na stacji roboczej podpinającego się pod serwer.
- **Połączenie**: Otwiera `socket`, przesyła na serwer swój automatycznie wygenerowany (np. `uuid.uuid4()`) 8-znakowy identyfikator i czeka na wpuszczenie. Kiedy otrzyma zwrotne `"REFUSED"`, wie, że na serwerze nie ma miejsc - zamyka się systemowo (`sys.exit()`).
- **Przetwarzanie z błędami (Przypadek Oczekiwany)**: Skrypt uruchamia klienta w pętli 3 razy. Za pierwszymi dwoma klient podaje prawdziwą klasę do wyszukania. Za trzecim razem prosi o klasę `"Samolot"`. Serwer odsyła mu w bajtach przez system **Pickle** czysty Integer (`404`). Klient próbuje na odebranych danych otworzyć strukturę z wyrażeniem generatorowym strumieniując obiekty jeden po drugim, i przez niemożliwość odczytu z Integera kod podrzuca `TypeError`. 
- **Zabezpieczenie**: Klient wyłapuje w zgrabnym bloku `try...except TypeError` ten przypadek i zamiast zatrzymać gwałtownie działanie całej platformy, powiadamia nas o niezgodności typów i łagodnie się zamyka.

---

## ⚙️ 4. Testy (`test_app.py`)
Do napisania zaawansowanych scenariuszy testowych wykorzystano framework `unittest`.
- **Testy Jednostkowe**: Pilnują poprawności klas. Wykorzystano asercje, by sprawdzić sprawność przyrównywania modeli (`__eq__`) oraz dokładną i niezmienną wielkość wygenerowanego słownika instancji (równą 12).
- **Testy Integracyjne**: Wyizolowany test na samym systemie **Pickle**. Symuluje całą ścieżkę wejścia do strumienia bajtów i odszyfrowywania. Używając weryfikacji i w/w modeli przyrównuje, czy w ramach przesyłu sieciowego obiekt nadal zachowuje oryginalny stan i atrybuty.
- **Testy Systemowe E2E (End-to-End)**: Oparty na demograficznym procesie testowania od zera. Narzędzie testowe `setUp` stawia w tle instancję prawdziwego serwera na portach testowych (np. 5005). Test zapętla programowe i połączone z siecią zapytania z czystych obiektów `socket`, tworząc kolejkę 4 żądań pod rząd na obciążonym serwerze. Potwierdza asercją i logiką na twardo, że 4-ty klient zawsze wywala odpowiedź `"REFUSED"`.

---

## 🚀 Jak używać?

Otwórz okno terminala, wejdź w ścieżkę głównego folderu i uruchom nasłuchujący serwer (należy zostawić uruchomiony ten terminal w tle):
```bash
python3 server.py
```
Otwórz drugie okno/kartę z terminalem i zasymuluj żądania klientów (możesz też uruchomić kilka skryptów klienta naraz w wielu terminalach, by wywołać zapełnienie i opóźnienia):
```bash
python3 client.py
```
Aby przeprowadzić automatyczny audyt poprawności i testy:
```bash
python3 test_app.py -v
```