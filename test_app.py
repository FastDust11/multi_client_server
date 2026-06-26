import unittest
import threading
import time
import socket
import pickle

# Importowanie modeli i logiki
from pojazdy import Samochod, Motocykl, Rower
from server import Server
from client import Client

class TestUnit(unittest.TestCase):
    def test_modele_eq(self):
        """Przetestuj, czy metoda __eq__ w modelach działa poprawnie."""
        # Test samochodów
        s1 = Samochod(marka="Toyota", rocznik=2010)
        s2 = Samochod(marka="Toyota", rocznik=2010)
        s3 = Samochod(marka="Honda", rocznik=2012)
        
        self.assertEqual(s1, s2, "Obiekty Samochod o tych samych parametrach powinny być równe.")
        self.assertNotEqual(s1, s3, "Obiekty Samochod o różnych parametrach nie powinny być równe.")
        
        # Test motocykli z większą liczbą parametrów
        m1 = Motocykl(marka="Yamaha", rocznik=2015, pojemnosc_silnika=600)
        m2 = Motocykl(marka="Yamaha", rocznik=2015, pojemnosc_silnika=600)
        self.assertEqual(m1, m2, "Obiekty Motocykl o tych samych parametrach powinny być równe.")
        
    def test_server_generuje_12_obiektow(self):
        """Przetestuj, czy słownik serwera generuje dokładnie 12 obiektów."""
        serwer = Server()
        self.assertEqual(len(serwer.obiekty), 12, "Po inicjalizacji serwera słownik self.obiekty powinien zawierać dokładnie 12 instancji.")

class TestIntegration(unittest.TestCase):
    def test_serializacji_pickle(self):
        """Test mechanizmu serializacji i deserializacji pickle dla obiektów."""
        oryginalna_lista = [
            Samochod(marka="Fiat", rocznik=2000),
            Motocykl(marka="Kawasaki", rocznik=2020, pojemnosc_silnika=1000),
            Rower(marka="Kross", rocznik=2019, typ="Górski")
        ]
        
        # Serializacja (jak po stronie serwera)
        dane_zserializowane = pickle.dumps(oryginalna_lista)
        
        # Deserializacja (jak po stronie klienta)
        odtworzona_lista = pickle.loads(dane_zserializowane)
        
        # Weryfikacja
        self.assertEqual(len(odtworzona_lista), 3)
        self.assertEqual(odtworzona_lista[0], oryginalna_lista[0])
        self.assertEqual(odtworzona_lista[1], oryginalna_lista[1])
        self.assertEqual(odtworzona_lista[2], oryginalna_lista[2])

class TestE2E(unittest.TestCase):
    def setUp(self):
        """Uruchomienie testowego serwera w tle."""
        # Używamy portu 5005, by zminimalizować ryzyko konfliktów
        self.test_port = 5005
        self.serwer = Server(port=self.test_port)
        
        # Wątek musi działać w tle (daemon)
        self.server_thread = threading.Thread(target=self.serwer.start)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Opóźnienie na poprawne postawienie gniazda przez serwer
        time.sleep(0.5)
        
    def test_limit_czwartego_klienta(self):
        """Połącz 4 klientów programowo i upewnij się asercją, że czwarty klient otrzymuje błąd 'REFUSED'."""
        gniazda = []
        odpowiedzi = []
        
        for i in range(4):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # 1. Połączenie
                sock.connect(('127.0.0.1', self.test_port))
                
                # 2. Wysłanie wygenerowanego ID (jak robi to nasz skrypt client.py)
                klient_id = f"Test_{i}"
                sock.sendall(klient_id.encode('utf-8'))
                
                # 3. Odbiór odpowiedzi (OK / REFUSED)
                odpowiedz = sock.recv(1024).decode('utf-8').strip()
                odpowiedzi.append(odpowiedz)
                
                gniazda.append(sock)
                
            except Exception as e:
                self.fail(f"Połączenie klienta Test_{i} niespodziewanie rzuciło wyjątek: {e}")
                
        # Asercje
        self.assertEqual(odpowiedzi[0], "OK")
        self.assertEqual(odpowiedzi[1], "OK")
        self.assertEqual(odpowiedzi[2], "OK")
        self.assertEqual(odpowiedzi[3], "REFUSED", "Czwarty klient powinien zostać odrzucony przez limit na serwerze.")
        
        # Sprzątanie połączeń testowych
        for sock in gniazda:
            sock.close()

if __name__ == "__main__":
    unittest.main()
