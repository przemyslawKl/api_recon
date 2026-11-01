import requests
import json
import os
import sys
import csv


# =====================================
# Zapis surowej odpowiedzi crt.sh
# =====================================

def save_raw_json(data):

    os.makedirs("raw", exist_ok=True)

    with open(
        "raw/crtsh-response.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================
# Wyciąganie subdomen
# =====================================

def extract_subdomains(data, domain):

    subdomains = set()

    for record in data:

        name_value = record.get("name_value")

        if not name_value:
            continue

        names = name_value.split("\n")

        for name in names:

            name = name.strip()
            name = name.lower()
            name = name.replace("*.", "")

            if name.endswith(domain):
                subdomains.add(name)

    return sorted(subdomains)


# =====================================
# TXT
# =====================================

def save_subdomains_txt(subdomains):

    with open(
        "output/subdomains.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for subdomain in subdomains:
            f.write(subdomain + "\n")


# =====================================
# CSV subdomains
# =====================================

def save_subdomains_csv(
        subdomains,
        domain
):

    with open(
        "output/subdomains.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "subdomain",
                "source",
                "domain"
            ]
        )

        for subdomain in subdomains:

            writer.writerow(
                [
                    subdomain,
                    "crt.sh",
                    domain
                ]
            )


# =====================================
# HTTP / HTTPS Validation
# =====================================

def validate_http(subdomains):

    http_results = []

    for subdomain in subdomains:

        # HTTPS

        https_url = f"https://{subdomain}"

        try:

            response = requests.get(
                https_url,
                timeout=5
            )

            http_results.append(
                [
                    subdomain,
                    "https",
                    response.status_code,
                    "responded"
                ]
            )

        except requests.exceptions.RequestException:

            http_results.append(
                [
                    subdomain,
                    "https",
                    "",
                    "no_response"
                ]
            )

        # HTTP

        http_url = f"http://{subdomain}"

        try:

            response = requests.get(
                http_url,
                timeout=5
            )

            http_results.append(
                [
                    subdomain,
                    "http",
                    response.status_code,
                    "responded"
                ]
            )

        except requests.exceptions.RequestException:

            http_results.append(
                [
                    subdomain,
                    "http",
                    "",
                    "no_response"
                ]
            )

    return http_results


# =====================================
# HTTP Validation CSV
# =====================================

def save_http_validation(http_results):

    with open(
        "output/http-validation.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "subdomain",
                "scheme",
                "status_code",
                "result"
            ]
        )

        for row in http_results:
            writer.writerow(row)


# =====================================
# Security Headers
# =====================================

def analyze_security_headers(subdomains):

    security_results = []

    for subdomain in subdomains:

        url = f"https://{subdomain}"

        try:

            response = requests.get(
                url,
                timeout=5
            )

            headers = response.headers

            strict_transport_security = (
                "present"
                if "Strict-Transport-Security" in headers
                else "missing"
            )

            content_security_policy = (
                "present"
                if "Content-Security-Policy" in headers
                else "missing"
            )

            x_frame_options = (
                "present"
                if "X-Frame-Options" in headers
                else "missing"
            )

            x_content_type_options = (
                "present"
                if "X-Content-Type-Options" in headers
                else "missing"
            )

            referrer_policy = (
                "present"
                if "Referrer-Policy" in headers
                else "missing"
            )

            permissions_policy = (
                "present"
                if "Permissions-Policy" in headers
                else "missing"
            )

            security_results.append(
                [
                    subdomain,
                    url,
                    response.status_code,
                    strict_transport_security,
                    content_security_policy,
                    x_frame_options,
                    x_content_type_options,
                    referrer_policy,
                    permissions_policy
                ]
            )

        except requests.exceptions.RequestException:
            continue

    return security_results


# =====================================
# Security Headers CSV
# =====================================

def save_security_headers(security_results):

    with open(
        "output/security-headers.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "subdomain",
                "url",
                "status_code",
                "strict_transport_security",
                "content_security_policy",
                "x_frame_options",
                "x_content_type_options",
                "referrer_policy",
                "permissions_policy"
            ]
        )

        for row in security_results:
            writer.writerow(row)


# =====================================
# REPORT
# =====================================

def generate_report(
        domain,
        subdomains
):

    report_path = "output/report.md"

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("# Raport Recon\n\n")

        f.write("## Domena\n\n")
        f.write(f"{domain}\n\n")

        f.write("## Liczba subdomen\n\n")
        f.write(f"{len(subdomains)}\n\n")

        f.write("## Subdomeny\n\n")

        for subdomain in subdomains:
            f.write(f"- {subdomain}\n")

        f.write("\n")

        f.write("## Wygenerowane pliki\n\n")
        f.write("- raw/crtsh-response.json\n")
        f.write("- output/subdomains.txt\n")
        f.write("- output/subdomains.csv\n")
        f.write("- output/http-validation.csv\n")
        f.write("- output/security-headers.csv\n")


# =====================================
# MAIN
# =====================================

def main():

    if len(sys.argv) < 2:
        print("Użycie: python api_recon.py <domena>")
        return

    domain = sys.argv[1].strip()

    if not domain:
        print("Podano pustą domenę.")
        return

    if domain.startswith("http://") or domain.startswith("https://"):
        print("Nie podawaj http:// ani https://")
        return

    print(f"Analizowana domena: {domain}")

    params = {
        "q": f"%.{domain}",
        "output": "json"
    }

    try:

        response = requests.get(
            "https://crt.sh/",
            params=params,
            timeout=15
        )

        print(f"Status: {response.status_code}")

        if response.status_code != 200:
            print(f"Błąd HTTP: {response.status_code}")
            return

        try:
            data = response.json()
        except ValueError:
            print("Błąd: odpowiedź nie jest JSON-em.")
            return

        save_raw_json(data)

        print(
            f"Zapisano {len(data)} rekordów do raw/crtsh-response.json"
        )

        sorted_subdomains = extract_subdomains(
            data,
            domain
        )

        print("\nZnalezione subdomeny:\n")

        for subdomain in sorted_subdomains:
            print(subdomain)

        print(
            f"\nLiczba unikalnych subdomen: {len(sorted_subdomains)}"
        )

        os.makedirs("output", exist_ok=True)

        save_subdomains_txt(sorted_subdomains)
        save_subdomains_csv(
            sorted_subdomains,
            domain
        )

        print("Zapisano output/subdomains.txt")
        print("Zapisano output/subdomains.csv")

        http_results = validate_http(
            sorted_subdomains
        )

        save_http_validation(
            http_results
        )

        print("Zapisano output/http-validation.csv")

        security_results = analyze_security_headers(
            sorted_subdomains
        )

        save_security_headers(
            security_results
        )

        print("Zapisano output/security-headers.csv")

        generate_report(
            domain,
            sorted_subdomains
        )

        print("Zapisano output/report.md")

    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia: {e}")


if __name__ == "__main__":
    main()