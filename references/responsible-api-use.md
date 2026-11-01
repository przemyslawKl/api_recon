# Zasady odpowiedzialnego użycia API i źródeł OSINT

## Zakres

Pracuj wyłącznie na:

- domenach wskazanych przez prowadzącego,
- własnych domenach,
- środowiskach laboratoryjnych,
- publicznych endpointach przeznaczonych do testów, takich jak `httpbin.org`.

Publicznie widoczna informacja nie oznacza automatycznie zgody na dalsze testowanie, masowe pobieranie danych ani aktywne sprawdzanie wrażliwych ścieżek.

## Tempo zapytań

Każdy skrypt powinien:

- używać `timeout`,
- ograniczać liczbę zapytań,
- obsługiwać `429 Too Many Requests`,
- nie wykonywać nieskończonych pętli retry,
- umożliwiać zatrzymanie działania,
- zapisywać częściowe wyniki.

## Sekrety

Klucze API:

- pobieraj ze zmiennych środowiskowych,
- nie zapisuj w kodzie,
- nie zapisuj w logach,
- nie commituj do repozytorium,
- nie wklejaj do raportu,
- nie udostępniaj w materiałach szkoleniowych.

## Dane zewnętrzne

Dane z API security są obserwacją, nie dowodem końcowym.

Poprawne sformułowania:

- “Subdomena występuje w logach CT.”
- “Host był widoczny w zewnętrznym źródle.”
- “Hash ma detekcje w źródle reputacyjnym.”
- “CVE znajduje się w katalogu KEV.”

Niepoprawne sformułowania bez dodatkowej walidacji:

- “Subdomena jest aktywna.”
- “Host jest obecnie podatny.”
- “Plik jest na pewno malware.”
- “Brak wyniku oznacza brak ryzyka.”

## Malware

W tym labie nie pobieramy próbek malware. Praca z abuse.ch, VirusTotal lub innymi źródłami malware powinna ograniczać się do metadanych, hashy, URL-i i opisów.

Pobieranie próbek wymaga osobnego, izolowanego środowiska, procedur bezpieczeństwa i zgody prowadzącego.
