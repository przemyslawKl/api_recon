# Oczekiwane rezultaty — Lab 21

## Po etapie 1

Student potrafi:

- wykonać żądanie `GET` przez `requests`,
- odczytać kod statusu,
- sparsować JSON,
- obsłużyć błąd połączenia i błąd parsowania JSON.

## Po etapie 2

Student potrafi:

- przekazać parametry przez `params=`,
- pobrać dane z crt.sh,
- zapisać surową odpowiedź JSON,
- rozróżnić endpoint od parametrów query.

## Po etapie 4

Plik `output/subdomains.txt` powinien zawierać posortowaną, unikalną listę subdomen.

Dla danych przykładowych `sample-crtsh-response.json` oczekiwana lista to:

```text
api.example.com
dev.example.com
www.example.com
```

## Po etapie 6

Plik `output/http-validation.csv` powinien zawierać informację o próbie połączenia dla każdej subdomeny i schematu.

Student nie powinien opisywać hosta jako “nieistniejącego” tylko dlatego, że nie odpowiedział po HTTP/HTTPS.

## Po etapie 7

Plik `output/security-headers.csv` powinien zawierać ocenę obecności wybranych nagłówków bezpieczeństwa.

Wartości powinny być opisowe:

- `present`,
- `missing`,
- `not_checked`.

## Po etapie 8

Raport powinien oddzielać:

- dane surowe,
- obserwacje,
- interpretację,
- ograniczenia,
- rekomendowane dalsze kroki.

## Najważniejsze kryterium jakości

Program nie musi być rozbudowany, ale ma być przewidywalny:

- błędy mają być obsłużone,
- wyniki mają być zapisane,
- sekrety nie mogą występować w kodzie,
- raport nie może nadinterpretować danych z zewnętrznych źródeł.
