import socket
import threading
import time
import random
import pickle
from pojazdy import Samochod, Motocykl, Rower

MAX_CLIENTS = 3

class Server:
    def __init__(self, host='127.0.0.1', port=5000):
        # Słownik pełniący rolę mapy obiektów
        self.obiekty = {}
        self._wygeneruj_poczatkowe_dane()
        
        # Konfiguracja socketu
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Kontrola limitów i wątków
        self.active_clients = 0
        self.client_lock = threading.Lock()
        
    def _wygeneruj_poczatkowe_dane(self):
        # Pętla generująca po 4 instancje dla każdej z klas
        for i in range(1, 5):
            # Tworzenie samochodów
            klucz_samochod = f"Samochod_{i}"
            self.obiekty[klucz_samochod] = Samochod(marka=f"Toyota_{i}", rocznik=2010 + i)
            
            # Tworzenie motocykli
            klucz_motocykl = f"Motocykl_{i}"
            self.obiekty[klucz_motocykl] = Motocykl(marka=f"Honda_{i}", rocznik=2015 + i, pojemnosc_silnika=500 + i * 100)
            
            # Tworzenie rowerów
            klucz_rower = f"Rower_{i}"
            self.obiekty[klucz_rower] = Rower(marka=f"Trek_{i}", rocznik=2020 + i)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Serwer nasłuchuje na {self.host}:{self.port} (MAX_CLIENTS={MAX_CLIENTS})...")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                
                # Uruchomienie wątku dla każdego klienta, limit kontrolowany wewnątrz handlera
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_thread.start()
        except KeyboardInterrupt:
            print("\nZamykanie serwera...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, address):
        try:
            # Odbiór ID klienta
            client_id = client_socket.recv(1024).decode('utf-8').strip()
            if not client_id:
                client_socket.close()
                return

            with self.client_lock:
                if self.active_clients >= MAX_CLIENTS:
                    print(f"Odrzucono klienta {client_id} ({address}) - limit osiągnięty.")
                    client_socket.sendall(b"REFUSED")
                    client_socket.close()
                    return
                else:
                    self.active_clients += 1
            
            print(f"Zaakceptowano klienta {client_id} ({address}). Aktywni klienci: {self.active_clients}")
            try:
                # Wysłanie OK
                client_socket.sendall(b"OK")
                
                # Odbiór żądanej nazwy klasy
                requested_class = client_socket.recv(1024).decode('utf-8').strip()
                
                # Szukamy odpowiednich obiektów w słowniku
                matched_objects = [obj for key, obj in self.obiekty.items() if key.startswith(requested_class)]
                
                if not matched_objects:
                    # Celowy błąd: wysyłamy inta zamiast zserializowanej listy
                    serialized_data = pickle.dumps(404)
                    print(f"Klient ID: {client_id} zażądał nieistniejącej klasy '{requested_class}'. Wysyłam błąd 404.")
                else:
                    matched_keys = [key for key in self.obiekty.keys() if key.startswith(requested_class)]
                    print(f"Klient ID: {client_id} zażądał klasy '{requested_class}'. Wysyłam obiekty: {matched_keys}")
                    serialized_data = pickle.dumps(matched_objects)
                
                # Symulacja opóźnienia 1-3 sekund
                time.sleep(random.uniform(1, 3))
                
                # Serializacja i wysłanie do klienta
                client_socket.sendall(serialized_data)
                
            finally:
                with self.client_lock:
                    self.active_clients -= 1
                print(f"Zakończono połączenie z {client_id} ({address}). Aktywni klienci: {self.active_clients}")
        except Exception as e:
            print(f"Błąd u klienta {address}: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    serwer = Server()
    serwer.start()
