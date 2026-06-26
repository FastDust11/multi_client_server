# Programowanie zaawansowane – projekt

---

## Skład zespołu i odpowiedzialności
1. **[FastDust11/NameInZipFile 172499]** – Główny i jedyny programista.  
   *Odpowiedzialność:* Projekt architektury klient-serwer, wdrożenie wielowątkowości (w tym synchronizacja wątków i limity `MAX_CLIENTS`), napisanie modeli danych, implementacja serializacji, obsługa błędów (wyjątków), napisanie i przeprowadzenie testów (jednostkowych, integracyjnych i E2E) oraz ostateczne przygotowanie dokumentacji technicznej z wykorzystaniem narzędzi AI.

---

## Instrukcja techniczna

Aplikacja została napisana w języku **Python**. Nie wymaga ręcznej kompilacji (język interpretowany) ani instalowania zewnętrznych frameworków, korzysta wyłącznie z bibliotek wbudowanych (m.in. `socket`, `threading`, `pickle`, `unittest`).

**Wymagania systemowe:** Zainstalowany Python w wersji 3.x.

### 1. Uruchomienie Serwera
Aby uruchomić serwer, otwórz terminal (wiersz poleceń) w głównym katalogu z projektem i wpisz:
```bash
python server.py
# lub zależnie od Twojego systemu operacyjnego: python3 server.py
```
*Uwaga: Serwer nasłuchuje w nieskończonej pętli. Okno terminala musi pozostać otwarte przez cały czas działania serwera.*

### 2. Uruchomienie Klienta
Aby połączyć się jako klient, otwórz nowe (dodatkowe) okno terminala w tym samym katalogu i uruchom skrypt kliencki:
```bash
python client.py
# lub: python3 client.py
```
*Klient wykonuje programowo zaplanowaną sekwencję zapytań (w tym jedno błędne, aby przetestować asercje i logikę) i samoczynnie kończy działanie. Możesz uruchomić ten skrypt wielokrotnie (w pętli lub w kilku terminalach naraz), aby zweryfikować zachowanie serwera dla wartości granicznych i odrzucania nadmiarowych połączeń (limit MAX_CLIENTS).*

### 3. Uruchomienie zautomatyzowanych testów
Aplikacja została wyposażona w dedykowany zestaw testów oparty o moduł `unittest`.  
By uruchomić wszystkie scenariusze (Testy jednostkowe, integracyjne i E2E) oraz wygenerować raport na konsolę, wpisz w terminalu:
```bash
python test_app.py -v
# lub: python3 test_app.py -v
```

---

## Deklaracja użycia sztucznej inteligencji (AI)

Zgodnie z zasadami realizacji projektów na uczelni, oświadczam/y, że podczas tworzenia rozwiązania, pisania kodu i dokumentowania użyto asystentów AI jako pary programistycznej wspierającej projekt.

- **Wykorzystane narzędzia i modele:** 
  Automatyczny agent programistyczny Google zasilany modelem **Gemini 3.1 Pro (High)**.
  
- **Zakres wykorzystania AI w projekcie:** 
  Model sztucznej inteligencji posłużył do napisania logiki i szkieletu całego kodu z udziałem programisty dyktującego warunki (technika Pair-Programmingu z AI). Wdrożono za jego pomocą modele klas, implementację map dla instancji, pełną wielowątkową architekturę serwera i blokady Lock() dla połączeń TCP Socket, serializację obiektów przez bibliotekę wewnętrzną `pickle`, wygenerowanie i odseparowanie testów oraz obrobienie niniejszej dokumentacji README.

- **Przykładowe (kluczowe) prompty, które posłużyły do wygenerowania istotnych fragmentów rozwiązania:**
  1. *"Napisz w Pythonie trzy klasy reprezentujące modele danych (np. Samochod, Motocykl, Rower). Każda z nich musi zawierać metodę inicjalizacyjną `__init__` z minimum dwoma polami [...]"*
  2. *"Rozbuduj klasę Server o obsługę połączeń za pomocą wbudowanego modułu socket (AF_INET, SOCK_STREAM). Zdefiniuj stałą MAX_CLIENTS = 3. Do kontrolowania liczby aktywnych klientów użyj threading.Lock() [...]"*
  3. *"Napisz kod dla Klienta (klasa Client). Klient łączy się z serwerem i wysyła swoje losowe ID jako zwykły tekst. Serwer odpowiada tekstem 'OK' lub 'REFUSED' [...] Jeśli 'OK', klient wysyła string z nazwą żądanej klasy [...]"*
  4. *"Zaimplementuj logikę po stronie klienta. Klient odbiera dane, deserializuje je za pomocą pickle.loads() i przetwarza otrzymaną listę obiektów 'strumieniowo' (użyj pythonowych generatorów). Skrypt musi uruchomić w pętli 3 zapytania, w jednym klient prosi o nieistniejącą klasę [...]"*
  5. *"Wygeneruj testy dla tej aplikacji używając wbudowanego modułu unittest. Zrób trzy sekcje: Testy jednostkowe, Integracyjne oraz E2E (Systemowe) [...]"*

- **Parametry konfiguracyjne modeli:** Domyślne (Default). Kod był implementowany przez ustrukturyzowanego agenta pracującego na temperaturze optymalnej do przewidywania składni języka bez dodatkowych modyfikacji.