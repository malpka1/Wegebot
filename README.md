# Chatbot do wyszukiwania wegańskich przepisów

## Opis projektu

Chatbot do wyszukiwania wegańskich przepisów kulinarnych na podstawie zadanych przez użytkownika składników, preferencji oraz kategorii dań. Projekt wykorzystuje technologię NLP (przetwarzanie języka naturalnego) do analizy zapytań i umożliwia przeglądanie przepisów, w tym wyświetlanie składników oraz instrukcji przygotowania.

## Struktura projektu

projekt-chatbot/
+-- chatbot/
|   +-- chatbot_logic.py  # Logika chatbota
+-- data/
|   +-- recipes_df.csv  # Plik CSV z przetworzonymi danymi przepisów
|   +-- ervegan_recipes_with_categories (1).csv  # Przepisy z Ervegan
|   +-- recipes_with_categories (1).csv  # Przepisy z Jadłonomii
+-- notebooks/
|   +-- jadlonomia_scraping.ipynb  # Skrapowanie danych z przepisami ze strony Jadłonomia
|   +-- ervegan_scraping.ipynb  # Skrapowanie danych z przepisami ze strony Ervegan
|   +-- recipes_df.ipynb  # Czyszczenie i łączenie danych
+-- requirements.txt  # Lista wymaganych bibliotek
+-- README.md  # Dokumentacja projektu

## Wymagania

Aby uruchomić projekt, należy zainstalować wymagane zależności:

- Python 3.7+
- Biblioteki wymienione w `requirements.txt`

## Instalacja zależności

Aby zainstalować wymagane zależności, uruchom poniższe polecenie:

pip install -r requirements.txt


## Uruchamianie chatbota

1. Upewnij się, że w folderze `data/` znajduje się plik `recipes_df.csv`.
2. Uruchom plik z logiką chatbota:

python chatbot/chatbot_logic.py


## Dane wejściowe

Użytkownik podaje składniki rozdzielone przecinkami, na przykład:

"pomidor, awokado, ciecierzyca"


Następnie chatbot pyta o kategorię dań, takie jak "śniadanie", "obiad" lub "kolacja", i umożliwia przeglądanie przepisów na podstawie wprowadzonych danych.

## Dane wyjściowe

Chatbot zwraca listę przepisów pasujących do zadanych kryteriów, zawierającą:

- Nazwę przepisu
- Krótkie streszczenie
- Składniki
- Instrukcje przygotowania
- Link do obrazu (jeśli dostępny)

## Dodatkowe informacje

- **jadlonomia_scraping.ipynb** – skrypt do skrapowania danych z przepisami ze strony Jadłonomia
- **ervegan_scraping.ipynb** – skrypt do skrapowania danych z przepisami ze strony Ervegan
- **recipes_df.ipynb** – skrypt do czyszczenia i łączenia danych
- **recipes_df.csv** – przetworzony plik CSV z danymi, który jest używany do działania chatbota.

Projekt ten jest częścią mojego projektu związanego z NLP i wykorzystaniem przetwarzania języka naturalnego do interakcji z użytkownikami.

