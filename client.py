import socket
import sys
import uuid
import pickle
import random
import time

class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.client_id = str(uuid.uuid4())[:8] # Losowe 8-znakowe ID
        
    def run(self, requested_class="Samochod"):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.host, self.port))
            
            # 1. Wysyłanie ID klienta jako tekst
            print(f"[{self.client_id}] Łączenie z serwerem i wysyłanie ID...")
            client_socket.sendall(self.client_id.encode('utf-8'))
            
            # 2. Odbieranie odpowiedzi OK lub REFUSED
            response = client_socket.recv(1024).decode('utf-8').strip()
            print(f"[{self.client_id}] Odpowiedź serwera: {response}")
            
            if response == "REFUSED":
                print(f"[{self.client_id}] Połączenie odrzucone. Kończę działanie (sys.exit).")
                sys.exit()
            elif response == "OK":
                # 3. Wysyłanie nazwy żądanej klasy
                print(f"[{self.client_id}] Wysyłanie żądania o klasę: {requested_class}")
                client_socket.sendall(requested_class.encode('utf-8'))
                
                # 4. Odbieranie zserializowanych obiektów
                # Używamy pętli, aby upewnić się, że obierzemy cały strumień danych
                data = b""
                while True:
                    packet = client_socket.recv(4096)
                    if not packet:
                        break
                    data += packet
                    
                if data:
                    obiekty = pickle.loads(data)
                    try:
                        # Przetwarzanie 'strumieniowe' za pomocą wyrażenia generatorowego
                        strumien_obiektow = (obj for obj in obiekty)
                        print(f"[{self.client_id}] Otrzymano obiekty. Poniżej ich zawartość:")
                        for obj in strumien_obiektow:
                            print(f" -> {obj}")
                    except TypeError:
                        print(f"[{self.client_id}] BŁĄD TYPU DANYCH! Oczekiwano listy pojazdów, a otrzymano nieiterowalny obiekt: {obiekty}")
                else:
                    print(f"[{self.client_id}] Serwer nie zwrócił żadnych danych.")
                    
        except Exception as e:
            print(f"[{self.client_id}] Wystąpił błąd: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    dostepne_klasy = ["Samochod", "Motocykl", "Rower"]
    
    # Skrypt uruchamia 3 zapytania w pętli
    for i in range(3):
        print(f"\n--- ZAPYTANIE {i+1} ---")
        klient = Client()
        
        # W jednym z zapytań pytamy o nieistniejącą klasę "Samolot"
        if i == 2:
            wybrana_klasa = "Samolot"
        else:
            wybrana_klasa = random.choice(dostepne_klasy)
            
        klient.run(wybrana_klasa)
        time.sleep(1) # krótka przerwa między zapytaniami
