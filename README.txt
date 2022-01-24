Implementacja szyfru SNOW2.0

Aby włączyć program należy:

1. należy zainstalować środowisko Python (najlepiej 3.7)
2. następnie uruchomić plik main (komenda: python3 main.py)


wybór trybu testów:
1 - sprawdzenie wektorów testowych 128 bitowych,
2 - sprawdzenie wektorów testowych 256 bitowych
3 - testy średniej szybkości iinicjalizacji
4 - testy średniej szybkości generacji keystreamu
5 - testy średniej szybkości generacji ciphertextu SNOW 2.0.py
6 - testy średniej szybkości generacji ciphertextu RC4.c
7 - testy średniej szybkości generacji ciphertextu Salsa20.c
8 - testy średniej szybkości generacji ciphertextu RC4.py

Aby zmienić metodę testów szyfrowania:
 - należy zmienić wartość zmiennej "tryb" (linia 214)

