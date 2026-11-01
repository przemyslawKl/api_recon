# Ściąga — API security w Pythonie

## Najważniejsze pojęcia

`API` — interfejs komunikacji między systemami.

`Endpoint` — konkretny adres zasobu lub operacji.

`Method` — metoda HTTP określająca typ operacji, na przykład `GET`, `POST`, `PATCH`, `DELETE`.

`Query parameters` — parametry w URL po znaku `?`, zwykle używane do filtrowania lub paginacji.

`Body` — treść żądania, często JSON przy `POST`, `PUT` lub `PATCH`.

`Headers` — metadane żądania, na przykład `Accept`, `Content-Type`, `Authorization`.

`Rate limiting` — ograniczenie liczby zapytań w określonym czasie.

`Pagination` — dzielenie dużego wyniku na wiele stron.

## Najważniejsze kody HTTP

| Kod | Znaczenie | Interpretacja w skrypcie |
|---:|---|---|
| `200` | OK | Dane zostały pobrane |
| `201` | Created | Zasób został utworzony |
| `204` | No Content | Operacja udana, brak body |
| `400` | Bad Request | Błędne parametry lub body |
| `401` | Unauthorized | Brak lub błędne uwierzytelnienie |
| `403` | Forbidden | Brak uprawnień |
| `404` | Not Found | Endpoint lub zasób nie istnieje |
| `409` | Conflict | Konflikt stanu zasobu |
| `429` | Too Many Requests | Przekroczony limit zapytań |
| `500` | Internal Server Error | Błąd po stronie serwera |
| `502` | Bad Gateway | Problem po stronie infrastruktury |
| `503` | Service Unavailable | Usługa niedostępna |
| `504` | Gateway Timeout | Timeout po stronie infrastruktury |

## Minimalny bezpieczny wzorzec `requests`

```python
import requests

try:
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Timeout")
except requests.exceptions.HTTPError as error:
    print(f"HTTP error: {error}")
except requests.exceptions.RequestException as error:
    print(f"Request error: {error}")
except ValueError:
    print("Response is not valid JSON")
```

## Tokeny API

Nie zapisuj tokenu w kodzie:

```python
api_key = "secret"
```

Pobieraj token ze zmiennej środowiskowej:

```python
import os

api_key = os.environ.get("API_KEY")
if not api_key:
    raise SystemExit("Missing API_KEY")
```

## Źródła danych omawiane w lekcji

| Źródło | Typ danych | Klucz API | Uwaga interpretacyjna |
|---|---|---:|---|
| crt.sh | Certyfikaty TLS, nazwy domenowe | Nie | Wynik może być historyczny |
| Shodan | Ekspozycja usług internetowych | Tak | Dane mogą być opóźnione |
| VirusTotal | Reputacja plików, URL-i, domen, IP | Tak | Detekcje wymagają interpretacji |
| NVD | CVE, CVSS, metadane podatności | Zależnie od zasad API | CVE nie oznacza automatycznie podatności w organizacji |
| CISA KEV | Aktywnie wykorzystywane podatności | Nie dla publicznego katalogu | Brak w KEV nie oznacza braku ryzyka |
| GitHub Security Advisories | Podatności open source | Zależnie od użycia API | Wymaga powiązania z zależnościami projektu |
| GreyNoise | Kontekst adresów IP | Zależnie od planu | Klasyfikacja nie jest dowodem incydentu |
| abuse.ch | URL-e, hashe, malware metadata | Zależnie od endpointu | Nie pobierać malware poza izolowanym labem |
| AlienVault OTX | IOC i threat intelligence | Tak | Feed TI wymaga korelacji z lokalnymi logami |

## Security headers sprawdzane w labie

| Nagłówek | Cel |
|---|---|
| `Strict-Transport-Security` | Wymuszanie HTTPS po stronie przeglądarki |
| `Content-Security-Policy` | Ograniczanie źródeł skryptów, stylów i innych zasobów |
| `X-Frame-Options` | Ochrona przed osadzaniem strony w ramkach |
| `X-Content-Type-Options` | Ograniczanie MIME sniffingu |
| `Referrer-Policy` | Kontrola informacji przekazywanych w nagłówku Referer |
| `Permissions-Policy` | Ograniczanie dostępu do funkcji przeglądarki |

Brak nagłówka nie jest automatycznie podatnością. Jest obserwacją wymagającą oceny w kontekście aplikacji.
