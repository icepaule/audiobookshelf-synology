#!/usr/bin/env python3
"""
Audiobookshelf Metadata Enrichment via Ollama

Findet Hoerbuecher ohne Beschreibung in Audiobookshelf und generiert
via Ollama deutsche Zusammenfassungen, Genre und Schlaf-Eignung.

Konfiguration erfolgt ueber .env-Datei oder Kommandozeilenparameter.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def load_env(env_path=None):
    """Load variables from .env file into environment."""
    if env_path is None:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Do not override already set environment variables
            if key not in os.environ:
                os.environ[key] = value


# Load .env before reading defaults
load_env()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")
ABS_URL = os.environ.get("ABS_URL", "http://localhost:13378")
ABS_API_TOKEN = os.environ.get("ABS_API_TOKEN", "")

PROMPT_TEMPLATE = """Du bist ein Experte fuer deutsche Hoerbuecher.
Fuer das folgende Hoerbuch erstelle bitte:
1. Eine kurze Zusammenfassung (3-4 Saetze)
2. Das Genre (z.B. Krimi, Fantasy, Sachbuch, Klassiker, Maerchen, etc.)
3. Eine Einschaetzung der Eignung als Einschlaf-Hoerbuch (gut/mittel/weniger geeignet)

Titel: {title}
Autor: {author}

Antworte NUR im folgenden JSON-Format, ohne zusaetzlichen Text:
{{"zusammenfassung": "...", "genre": "...", "schlaf_eignung": "..."}}"""


def ollama_generate(prompt, ollama_url, model):
    """Send a prompt to Ollama and return the response."""
    data = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{ollama_url}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("response", "")


def abs_api(abs_url, token, endpoint, method="GET", payload=None):
    """Call the Audiobookshelf API."""
    url = f"{abs_url}{endpoint}"
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_libraries(abs_url, token):
    """Get all libraries from Audiobookshelf."""
    result = abs_api(abs_url, token, "/api/libraries")
    return result.get("libraries", [])


def get_library_items(abs_url, token, library_id):
    """Get all items from a library, handling pagination."""
    items = []
    page = 0
    limit = 50
    while True:
        result = abs_api(
            abs_url, token,
            f"/api/libraries/{library_id}/items?limit={limit}&page={page}"
        )
        items.extend(result.get("results", []))
        total = result.get("total", 0)
        if len(items) >= total:
            break
        page += 1
    return items


def parse_ollama_response(text):
    """Try to parse JSON from Ollama response."""
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    return None


def enrich_item(abs_url, token, item, ollama_url, model, dry_run=False):
    """Enrich a single item with Ollama-generated metadata."""
    metadata = item.get("media", {}).get("metadata", {})
    title = metadata.get("title", "Unbekannt")
    author = metadata.get("authorName", "Unbekannt")
    description = metadata.get("description", "")

    if description and not description.isspace():
        return None

    print(f"  Generiere Metadaten fuer: {title} ({author})")

    prompt = PROMPT_TEMPLATE.format(title=title, author=author)
    response_text = ollama_generate(prompt, ollama_url, model)
    parsed = parse_ollama_response(response_text)

    if not parsed:
        print(f"  WARNUNG: Konnte Antwort nicht parsen fuer '{title}'")
        print(f"  Rohantwort: {response_text[:200]}")
        return None

    zusammenfassung = parsed.get("zusammenfassung", "")
    genre = parsed.get("genre", "")
    schlaf = parsed.get("schlaf_eignung", "")

    new_description = zusammenfassung
    if schlaf:
        new_description += f"\n\nEinschlaf-Eignung: {schlaf}"

    if dry_run:
        print(f"  [DRY RUN] Wuerde setzen:")
        print(f"    Genre: {genre}")
        print(f"    Beschreibung: {new_description}")
        return parsed

    update_payload = {"metadata": {"description": new_description}}
    if genre:
        update_payload["metadata"]["genres"] = [genre]

    abs_api(abs_url, token, f"/api/items/{item['id']}/media", "PATCH", update_payload)
    print(f"  Aktualisiert: {title} -> Genre: {genre}")
    return parsed


def main():
    parser = argparse.ArgumentParser(
        description="Audiobookshelf Metadaten-Anreicherung via Ollama"
    )
    parser.add_argument(
        "--abs-url",
        default=ABS_URL,
        help=f"Audiobookshelf URL (default: {ABS_URL})"
    )
    parser.add_argument(
        "--token",
        default=ABS_API_TOKEN,
        help="Audiobookshelf API Token (default: aus .env)"
    )
    parser.add_argument(
        "--ollama-url",
        default=OLLAMA_URL,
        help=f"Ollama URL (default: {OLLAMA_URL})"
    )
    parser.add_argument(
        "--model",
        default=OLLAMA_MODEL,
        help=f"Ollama Modell (default: {OLLAMA_MODEL})"
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Pfad zur .env-Datei (default: .env im Skript-Verzeichnis)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nur anzeigen, nichts aendern"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Auch Buecher mit bestehender Beschreibung neu generieren"
    )

    args = parser.parse_args()

    if args.env_file:
        load_env(args.env_file)

    ollama_url = args.ollama_url
    model = args.model
    abs_url = args.abs_url
    token = args.token

    if not token:
        print("FEHLER: Kein API-Token angegeben.")
        print("Setze ABS_API_TOKEN in der .env oder nutze --token")
        sys.exit(1)

    # Test Ollama connection
    try:
        req = urllib.request.Request(f"{ollama_url}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            models = json.loads(resp.read().decode("utf-8"))
        print(f"Ollama erreichbar. Verfuegbare Modelle: "
              f"{[m['name'] for m in models.get('models', [])]}")
    except Exception as e:
        print(f"FEHLER: Ollama nicht erreichbar unter {ollama_url}: {e}")
        sys.exit(1)

    # Get libraries
    try:
        libraries = get_libraries(abs_url, token)
    except urllib.error.HTTPError as e:
        print(f"FEHLER: Audiobookshelf API-Fehler: {e.code} {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"FEHLER: Audiobookshelf nicht erreichbar: {e}")
        sys.exit(1)

    if not libraries:
        print("Keine Bibliotheken gefunden.")
        sys.exit(0)

    total_updated = 0
    total_skipped = 0

    for lib in libraries:
        print(f"\nBibliothek: {lib['name']} (ID: {lib['id']})")
        items = get_library_items(abs_url, token, lib["id"])
        print(f"  {len(items)} Eintraege gefunden")

        for item in items:
            metadata = item.get("media", {}).get("metadata", {})
            description = metadata.get("description", "")

            if description and not args.all:
                total_skipped += 1
                continue

            result = enrich_item(abs_url, token, item, ollama_url, model, args.dry_run)
            if result:
                total_updated += 1

    print(f"\nFertig. {total_updated} aktualisiert, {total_skipped} uebersprungen.")


if __name__ == "__main__":
    main()
