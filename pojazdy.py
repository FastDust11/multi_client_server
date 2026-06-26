class Pojazd:
    """Pusta klasa bazowa dla pojazdów."""
    pass


class Samochod(Pojazd):
    def __init__(self, marka: str, rocznik: int):
        self.marka = marka
        self.rocznik = rocznik
        
    def __str__(self):
        return f"Samochód: {self.marka} ({self.rocznik})"
        
    def __eq__(self, other):
        if isinstance(other, Samochod):
            return self.marka == other.marka and self.rocznik == other.rocznik
        return False


class Motocykl(Pojazd):
    def __init__(self, marka: str, rocznik: int, pojemnosc_silnika: int = 0):
        self.marka = marka
        self.rocznik = rocznik
        self.pojemnosc_silnika = pojemnosc_silnika
        
    def __str__(self):
        return f"Motocykl: {self.marka} ({self.rocznik}), {self.pojemnosc_silnika}ccm"
        
    def __eq__(self, other):
        if isinstance(other, Motocykl):
            return (self.marka == other.marka and 
                    self.rocznik == other.rocznik and 
                    self.pojemnosc_silnika == other.pojemnosc_silnika)
        return False


class Rower(Pojazd):
    def __init__(self, marka: str, rocznik: int, typ: str = "Miejski"):
        self.marka = marka
        self.rocznik = rocznik
        self.typ = typ
        
    def __str__(self):
        return f"Rower {self.typ}: {self.marka} ({self.rocznik})"
        
    def __eq__(self, other):
        if isinstance(other, Rower):
            return self.marka == other.marka and self.rocznik == other.rocznik and self.typ == other.typ
        return False
