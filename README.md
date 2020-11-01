# Annotation tool

## Instalacja
### Windows

 - Na aktualnej stronie repozytorium znajdź przycisk **Code** → **Download ZIP**
 - Rozpakuj plik, przejdź do katalogu **annotation-tool** znajdującego się w środku
 - Kliknij na pasek ze ścieżką do pliku, wpisz `cmd` i kliknij Enter (screenshot)
 - W terminalu który się otworzy wpisz `python3`
	 - Jeżeli nie masz zainstalowanego Pythona, powinno otworzyć się okno Microsoft Store, w którym będzie go można zainstalować
	 - Jeżeli masz zainstalowanego Pythona, wpisz `quit()` i kliknij Enter
 - Wpisz następujące komendy:
	 - `python3 -m pip install -r requirements.txt`
	 - `python3 src\gui.py`
 - W tym momencie powinna otworzyć się aplikacja

### Linux

 - Wpisz następujące komendy:
	 - `git clone https://github.com/bazylip/annotation-tool.git && cd annotation-tool`
	 - `python3 -m venv venv`
	 - `. venv/bin/activate`
	 - `pip install -r requirements.txt`
	 - `python3 src/gui.py`
 - W tym momencie powinna otworzyć się aplikacja
## Instrukcja obsługi
Program służy do klasyfikacji leukocytów, które zostały wcześniej ręcznie zaznaczonego na zdjęciach. W pliku annotations/xml znajduje się kilka przygotowanych przeze mnie plików, na których można przetestować działanie programu. Aby to zrobić, wykonaj poniższe instrukcje:

 - Po otwarciu aplikacji kliknij **"Select directory"**, a następnie wybierz folder **annotations/xml**
 - W tym momencie powinna wyświetlić się pierwsza komórka do oznaczenia. Dostępne akcje:
	 - **Oznaczenie komórki**  - za pomocą wciśnięcia pierwszej litery etykiety:
		 - h - Heterofil
		 - l - Limfocyt
		 - t - Trombofil
		 - e - Eozynofil
		 - b - Bazofil
		 - m - Monocyt
		 - u - Unknown (brak pewności/inny rodzaj komórki)
	- **Przejście do poprzedniego/następnego zdjęcia** - za pomocą strzałek lewo/prawo
- Etykieta **"None"** oznacza, że komórka nie została jeszcze oznaczona
- Po zakończeniu pracy prześlij mi zawartość katalogu **annotations/xml** w celu sprawdzenia czy wszystko dobrze działa
