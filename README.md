# Annotation tool
## Spis treści

 - Instalacja
	 - Windows
	 - Linux
 - Instrukcja obsługi

## Instalacja
### Windows

 - Na aktualnej stronie repozytorium znajdź przycisk **Code** → **Download ZIP**
 - Rozpakuj plik, przejdź do katalogu **annotation-tool** znajdującego się w środku
 - Kliknij na pasek ze ścieżką do pliku, wpisz `cmd` i kliknij Enter (screenshot)
 - W terminalu który się otworzy wpisz `python3`
	 - Jeżeli nie masz zainstalowanego Pythona, powinno otworzyć się okno Microsoft Store, w którym będzie go można zainstalować. Po zainstalowaniu nie ma potrzeby uruchamiania Pythona z poziomu Microsoft Store'a i możesz wrócić z powrotem do terminala.
	 - Jeżeli masz zainstalowanego Pythona, wpisz `quit()` i kliknij Enter
 - Wpisz następujące komendy:
	 - `python3 -m pip install -r requirements.txt` - w tym momencie zaczną pobierać się potrzebne pakiety, może to potrwać kilkadziesiąt sekund
	 - `python3 src\gui.py`
 - W tym momencie powinna otworzyć się aplikacja

### Linux

 - Wpisz następujące komendy:
	 - `git clone https://github.com/bazylip/annotation-tool.git && cd annotation-tool` - w tym momencie zacznie się sciągać repozytorium, może to potrwać kilka sekund
	 - `python3 -m venv venv`
	 - `. venv/bin/activate`
	 - `pip install -r requirements.txt` - w tym momencie zaczną pobierać się potrzebne pakiety, może to potrwać kilkadziesiąt sekund
	 - `python3 src/gui.py`
 - W tym momencie powinna otworzyć się aplikacja
## Instrukcja obsługi
Program służy do klasyfikacji leukocytów, które zostały wcześniej ręcznie zaznaczonego na zdjęciach. W pliku annotations/xml znajduje się kilka przygotowanych przeze mnie plików, na których można przetestować działanie programu. Aby to zrobić, wykonaj poniższe instrukcje:

 - Po otwarciu aplikacji kliknij **"Select directory"**, a następnie wybierz folder **annotations → xml**
 - W tym momencie powinna wyświetlić się pierwsza komórka do oznaczenia. Dostępne akcje:
	 - **Oznaczenie komórki**  - za pomocą wciśnięcia klawisza pierwszej litery etykiety:
		 - h - Heterofil
		 - l - Limfocyt
		 - t - Trombofil
		 - e - Eozynofil
		 - b - Bazofil
		 - m - Monocyt
		 - u - Unknown (wszystkie pozostałe)
	- **Przejście do poprzedniego/następnego zdjęcia** - za pomocą strzałek lewo/prawo
	- **Zmiana przybliżenia** - za pomocą klawiszy 1, 2, 3
- Etykieta **"None"** oznacza, że komórka nie została jeszcze oznaczona
- Po zakończeniu pracy prześlij mi zawartość katalogu **annotations → xml** w celu sprawdzenia czy wszystko zapisało się poprawnie
