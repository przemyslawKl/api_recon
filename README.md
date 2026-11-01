1. API Recon - Certificate Transparency Reconnaissance Tool
Opis projektu

API Recon jest narzędziem napisanym w języku Python służącym do pasywnego rozpoznania infrastruktury internetowej domeny na podstawie danych Certificate Transparency.

Program pobiera informacje o certyfikatach SSL/TLS z serwisu crt.sh, identyfikuje powiązane subdomeny, sprawdza ich dostępność przez HTTP i HTTPS, analizuje podstawowe nagłówki bezpieczeństwa oraz generuje raport podsumowujący wyniki.

Projekt został przygotowany jako ćwiczenie z obszaru OSINT (Open Source Intelligence), Reconnaissance oraz podstaw automatyzacji procesów bezpieczeństwa aplikacji webowych.



2. Cele projektu

Projekt realizuje następujące zadania:

pobieranie danych z publicznego źródła Certificate Transparency,
ekstrakcja subdomen dla wskazanej domeny,
deduplikacja i normalizacja wyników,
walidacja dostępności usług HTTP/HTTPS,
analiza wybranych nagłówków bezpieczeństwa,
generowanie raportów i plików wynikowych.


3. Wykorzystane technologie:
Python 3.x
requests
json
csv
os
sys


4. Architektura rozwiązania

Program składa się z kilku głównych etapów:

    1. Pobieranie danych z publicznego źródła Certificate Transparency (crt.sh)
    2. Ekstrakcja subdomen dla wskazanej domeny
    3. Deduplikacja i normalizacja wyników
    4. Walidacja dostępności usług HTTP/HTTPS
    5. Analiza wybranych nagłówków bezpieczeństwa
    6. Generowanie raportów i plików wynikowych


Użytkownik
    │
    ▼
crt.sh
    │
    ▼
Pobranie danych JSON
    │
    ▼
Ekstrakcja subdomen
    │
    ▼
Zapis danych
    │
    ├── subdomains.txt
    ├── subdomains.csv
    │
    ▼
Walidacja HTTP/HTTPS
    │
    ├── http-validation.csv
    │
    ▼
Analiza nagłówków
    │
    ├── security-headers.csv
    │
    ▼
Raport końcowy
    │
    └── report.md



Funkcjonalności
6. Pobieranie danych Certificate Transparency

Program wysyła zapytanie do:
https://crt.sh/
 
wykorzystując parametr:
output=json

oraz filtr:
.example.com

Dzięki temu możliwe jest pobranie informacji o certyfikatach wystawionych dla analizowanej domeny.

7. Ekstrakcja subdomen

Program:

odczytuje pole name_value,
rozdziela wiele wpisów zapisanych w jednym rekordzie,
usuwa wildcardy (*.),
normalizuje wielkość liter,
usuwa duplikaty.

Przykład:

*.example.com
WWW.EXAMPLE.COM
api.example.com

zostanie przekształcony do:

api.example.com
example.com
www.example.com


8. Walidacja HTTP i HTTPS

Dla każdej wykrytej subdomeny wykonywane są zapytania:

https://subdomain

oraz:

http://subdomain

Zapisywane są:

protokół,
kod odpowiedzi HTTP,
informacja, czy host odpowiedział.


9. Analiza nagłówków bezpieczeństwa

Program sprawdza obecność następujących nagłówków:

Strict-Transport-Security
Content-Security-Policy
X-Frame-Options
X-Content-Type-Options
Referrer-Policy
Permissions-Policy

Każdy nagłówek oznaczany jest jako:

present
lub:
missing
 
10. Generowanie raportu

Na końcu tworzony jest raport:
report.md

zawierający:

nazwę domeny,
liczbę znalezionych subdomen,
listę subdomen,
listę wygenerowanych plików.


11. Struktura projektu


project/
│
├── api_recon.py
│
├── raw/
│   └── crtsh-response.json
│
├── output/
│   ├── subdomains.txt
│   ├── subdomains.csv
│   ├── http-validation.csv
│   ├── security-headers.csv
│   └── report.md
│
└── README.md


12. Utworzenie środowiska wirtualnego

Linux:
python3 -m venv .venv
source .venv/bin/activate

Windows:
python -m venv .venv
.venv\Scripts\activate

Instalacja zależności

pip install requests
lub:
pip install -r requirements.txt

Uruchomienie
Przykład:
python api_recon.py learnit.com.pl


Przykładowy wynik


Analizowana domena: learnit.com.pl
 
Status: 200
 
Liczba unikalnych subdomen: 13
 
Zapisano output/subdomains.txt
Zapisano output/subdomains.csv
Zapisano output/http-validation.csv
Zapisano output/security-headers.csv
Zapisano output/report.md


13. Pliki wynikowe


subdomains.txt
Lista wykrytych subdomen.

Przykład:

lms.example.com
api.example.com
www.example.com

==============================================

subdomains.csv
Lista subdomen w formacie CSV.

CSV
subdomain,source,domain
www.example.com,crt.sh,example.com
 
==============================================

http-validation.csv
Status dostępności usług HTTP i HTTPS.

CSV
subdomain,scheme,status_code,result
www.example.com,https,200,responded

==============================================

security-headers.csv
Wyniki analizy nagłówków bezpieczeństwa.

CSV
subdomain,url,status_code,strict_transport_security
www.example.com,https://www.example.com,200,present

==============================================

report.md
Raport końcowy generowany automatycznie po wykonaniu programu.

14. Ograniczenia
Program korzysta wyłącznie z publicznie dostępnych danych.
Wyniki zależą od aktualnej zawartości bazy Certificate Transparency.
Brak odpowiedzi hosta nie musi oznaczać jego niedostępności (może blokować ruch ICMP/HTTP lub wymagać specyficznych nagłówków).
Analiza nagłówków obejmuje wyłącznie podstawowy zestaw kontroli bezpieczeństwa.


15. Autor
Projekt wykonany w celach edukacyjnych jako ćwiczenie z zakresu:

OSINT
Reconnaissance
Web Security
Python Automation
Certificate Transparency Analysis