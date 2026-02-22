# Audiobookshelf - Administrationshandbuch

## Inhaltsverzeichnis

1. [Systemuebersicht](#1-systemuebersicht)
2. [Voraussetzungen](#2-voraussetzungen)
3. [Installation](#3-installation)
4. [Konfiguration](#4-konfiguration)
5. [Bibliotheken und Mount-Punkte](#5-bibliotheken-und-mount-punkte)
6. [Ollama Metadaten-Anreicherung](#6-ollama-metadaten-anreicherung)
7. [Benutzerverwaltung](#7-benutzerverwaltung)
8. [Backup und Wiederherstellung](#8-backup-und-wiederherstellung)
9. [Zugriff von unterwegs (Tailscale)](#9-zugriff-von-unterwegs-tailscale)
10. [Troubleshooting](#10-troubleshooting)
11. [Updates](#11-updates)

---

## 1. Systemuebersicht

### Architektur

```
+------------------+                  +-----------------+       +---------------+
|  iPhone App      | -- Tailscale --> |  Audiobookshelf | <---> |  Ollama       |
|  (Streaming)     |    oder LAN      |  :<port>        |       |  <ollama-ip>  |
+------------------+                  +-----------------+       +---------------+
                                              |
                            +-----------------+-----------------+
                            |                 |                 |
                      /audiobooks       /nas-audiobooks   /usb-audiobooks
                            |                 |                 |
                   Eigene Sammlung      NAS-Sammlung      USB-Sammlung
                    (Samba, r/w)         (read-only)       (read-only)
```

### 3 Bibliotheken

| Bibliothek        | Container-Pfad     | Host-Pfad                   | Zugriff    |
|-------------------|--------------------|-----------------------------|------------|
| Eigene Sammlung   | `/audiobooks`      | `<pfad-zu-eigenen-hoerbuechern>` | Lesen/Schreiben (Samba-Share) |
| NAS-Sammlung      | `/nas-audiobooks`  | `<pfad-zur-nas-sammlung>`   | Nur lesen  |
| USB-Sammlung      | `/usb-audiobooks`  | `<pfad-zur-usb-sammlung>`   | Nur lesen  |

Die eigene Sammlung ist ueber einen Samba-Share zugaenglich, sodass Hoerbuecher
bequem per Windows/Mac kopiert werden koennen. Die NAS- und USB-Sammlungen werden
als separate, schreibgeschuetzte Bibliotheken eingebunden.

### Komponenten

| Komponente        | Beschreibung                                      | Adresse/Pfad                             |
|-------------------|---------------------------------------------------|------------------------------------------|
| Audiobookshelf    | Hoerbuch-Server mit Web-UI und API                | `http://<nas-ip>:<port>`                 |
| Ollama            | KI-Modell-Server fuer Metadaten-Generierung       | `http://<ollama-ip>:<ollama-port>`       |
| enrich_metadata.py| Skript zur automatischen Metadaten-Anreicherung   | `<pfad-zum-projekt>/`                    |
| Tailscale         | VPN-Mesh fuer sicheren Zugriff von unterwegs      | `http://<tailscale-ip>:<port>`           |

---

## 2. Voraussetzungen

- Synology NAS mit Docker / Container Manager
- Docker Compose (bereits vorhanden)
- Python 3.x (fuer das Enrichment-Skript)
- Netzwerkzugriff auf die Ollama-Instanz
- Tailscale auf der Synology installiert (fuer externen Zugriff)
- Ausreichend Speicherplatz fuer Hoerbuecher und Metadaten

---

## 3. Installation

### 3.1 Erstinstallation

```bash
cd <pfad-zum-projekt>

# .env aus Vorlage erstellen
cp .env.example .env

# .env anpassen (Pfade, und nach Ersteinrichtung den ABS_API_TOKEN)
nano .env

# Container starten
docker compose up -d
```

### 3.2 Verzeichnisstruktur

```
<pfad-zum-projekt>/
  docker-compose.yml     # Container-Definition
  .env                   # Sensible Konfiguration (NICHT im Repo)
  .env.example           # Vorlage fuer .env (im Repo)
  .gitignore             # Git-Ausschlussregeln
  enrich_metadata.py     # Ollama-Anreicherungsskript
  config/                # Audiobookshelf-Konfiguration (auto-generiert)
  metadata/              # Audiobookshelf-Metadaten (Covers, etc.)
  docs/
    ADMIN_HANDBUCH.md    # Dieses Dokument
    BENUTZER_HANDBUCH.md # Anleitung fuer Endbenutzer
```

### 3.3 Container pruefen

```bash
# Status pruefen
docker ps --filter name=audiobookshelf

# Logs anzeigen
docker logs audiobookshelf

# Container neustarten
cd <pfad-zum-projekt> && docker compose restart
```

---

## 4. Konfiguration

### 4.1 Umgebungsvariablen (.env)

Alle sensiblen und standortspezifischen Werte stehen in der `.env`-Datei.
Diese Datei wird NICHT ins Git-Repository uebernommen.
Als Vorlage dient die `.env.example` -- dort stehen nur Platzhalter, keine echten Werte.

| Variable             | Beschreibung                          | Platzhalter in .env.example              |
|----------------------|---------------------------------------|------------------------------------------|
| `ABS_PORT`           | Port fuer Web-UI und API              | `13378`                                  |
| `ABS_CONTAINER_NAME` | Docker-Containername                  | `audiobookshelf`                         |
| `ABS_IMAGE`          | Docker-Image                          | `ghcr.io/advplyr/audiobookshelf:latest`  |
| `TZ`                 | Zeitzone                              | `Europe/Berlin`                          |
| `ABS_CONFIG_PATH`    | Pfad fuer Konfiguration auf dem Host  | `<pfad-zum-projekt>/config`              |
| `ABS_METADATA_PATH`  | Pfad fuer Metadaten auf dem Host      | `<pfad-zum-projekt>/metadata`            |
| `ABS_AUDIOBOOKS_PATH`| Eigene Hoerbuecher (Samba-Share)      | `<pfad-zu-eigenen-hoerbuechern>`         |
| `ABS_MOUNT_NAS`      | NAS-Sammlung (read-only)              | `<pfad-zur-nas-sammlung>`                |
| `ABS_MOUNT_USB`      | USB-Sammlung (read-only)              | `<pfad-zur-usb-sammlung>`                |
| `ABS_URL`            | URL des Audiobookshelf-Servers        | `http://localhost:13378`                 |
| `ABS_API_TOKEN`      | API-Token fuer Skript-Zugriff         | *(leer -- aus der Web-UI generiert)*     |
| `OLLAMA_URL`         | URL der Ollama-Instanz                | `http://<ollama-host>:11434`             |
| `OLLAMA_MODEL`       | Ollama-Modell fuer Zusammenfassungen  | `qwen2.5:14b`                            |

### 4.2 API-Token generieren

1. Audiobookshelf Web-UI oeffnen (`http://<nas-ip>:<port>`)
2. Als Root-Admin einloggen
3. **Settings** > **Users** > den Admin-Benutzer auswaehlen
4. Unter **API Token** auf "Generate" klicken
5. Token kopieren und in `.env` bei `ABS_API_TOKEN` eintragen

---

## 5. Bibliotheken und Mount-Punkte

### 5.1 Konzept: 3 separate Bibliotheken

Das System arbeitet mit drei getrennten Bibliotheken, die jeweils als eigener
Mount-Punkt im Docker-Container erscheinen:

1. **Eigene Sammlung** (`/audiobooks`): Persoenliche Hoerbuecher, per Samba-Share
   beschreibbar. Neue Hoerbuecher werden hierueber hochgeladen.
2. **NAS-Sammlung** (`/nas-audiobooks`): Bestehende Sammlung auf dem NAS-Volume,
   schreibgeschuetzt eingebunden.
3. **USB-Sammlung** (`/usb-audiobooks`): Hoerbuecher auf einer externen
   USB-Festplatte, schreibgeschuetzt eingebunden.

### 5.2 Docker-Compose Volumes

```yaml
# docker-compose.yml (Auszug)
volumes:
  # Eigene Hoerbuecher (Samba-Share fuer Uploads von der Workstation)
  - ${ABS_AUDIOBOOKS_PATH}:/audiobooks
  # Bestehende Sammlungen als separate Mount-Punkte (read-only)
  - ${ABS_MOUNT_NAS}:/nas-audiobooks:ro
  - ${ABS_MOUNT_USB}:/usb-audiobooks:ro
  # Konfiguration und Metadaten
  - ${ABS_CONFIG_PATH}:/config
  - ${ABS_METADATA_PATH}:/metadata
```

Jede Sammlung wird in Audiobookshelf als eigene Bibliothek angelegt:
- Bibliothek "Eigene Hoerbuecher" -> Ordner `/audiobooks`
- Bibliothek "NAS-Sammlung" -> Ordner `/nas-audiobooks`
- Bibliothek "USB-Sammlung" -> Ordner `/usb-audiobooks`

### 5.3 Hoerbuecher ueber Samba hochladen

Der Samba-Share fuer die eigene Sammlung ist unter
`\\<nas-ip>\<freigabename>\<ordner>` erreichbar.

1. Verbinde dich per Windows-Explorer oder macOS Finder mit dem Share
2. Erstelle einen Ordner pro Hoerbuch: `<autor> - <buchtitel>/`
3. Kopiere die Audiodateien in den Ordner
4. Optional: Lege ein `cover.jpg` in den Ordner

### 5.4 Ordnerstruktur fuer Hoerbuecher

Audiobookshelf erkennt Hoerbuecher am besten in dieser Struktur:

```
<sammlung>/
  <autor> - <buchtitel>/
    cover.jpg               # Optional: Cover-Bild
    01 - <kapitelname>.mp3
    02 - <kapitelname>.mp3
    ...
```

Alternativ (ohne Autor im Ordnernamen):
```
<sammlung>/
  <buchtitel>/
    01 - <kapitelname>.mp3
    02 - <kapitelname>.mp3
```

### 5.5 Bibliotheks-Scan ausloesen

Nach dem Hinzufuegen neuer Hoerbuecher:

1. Web-UI oeffnen
2. In der Bibliothek auf das **Drei-Punkte-Menue** klicken
3. **"Scan"** oder **"Force Re-Scan"** waehlen

Oder per API:
```bash
source <pfad-zum-projekt>/.env
curl -X POST "http://localhost:${ABS_PORT}/api/libraries/<library-id>/scan" \
  -H "Authorization: Bearer ${ABS_API_TOKEN}"
```

### 5.6 Weitere Sammlungen hinzufuegen

Falls spaeter eine vierte Quelle hinzukommt:

1. Neue Variable in `.env` hinzufuegen (z.B. `ABS_MOUNT_EXTRA=<pfad>`)
2. In `docker-compose.yml` ein neues Volume eintragen:
   ```yaml
   - ${ABS_MOUNT_EXTRA}:/extra-audiobooks:ro
   ```
3. Container neu starten: `docker compose up -d`
4. In Audiobookshelf eine neue Bibliothek mit Ordner `/extra-audiobooks` anlegen

---

## 6. Ollama Metadaten-Anreicherung

### 6.1 Funktionsweise

Das Skript `enrich_metadata.py`:
1. Verbindet sich mit der Audiobookshelf API
2. Listet alle Hoerbuecher ohne Beschreibung auf
3. Sendet Titel und Autor an Ollama
4. Erhaelt eine deutsche Zusammenfassung, Genre und Einschlaf-Eignung
5. Schreibt die Metadaten zurueck in Audiobookshelf

### 6.2 Verwendung

```bash
cd <pfad-zum-projekt>

# Trockenlauf (nichts wird geaendert)
python3 enrich_metadata.py --dry-run

# Alle Buecher ohne Beschreibung anreichern
python3 enrich_metadata.py

# Auch bestehende Beschreibungen neu generieren
python3 enrich_metadata.py --all

# Anderes Modell verwenden
python3 enrich_metadata.py --model <modellname>

# Eigene .env-Datei angeben
python3 enrich_metadata.py --env-file <pfad-zur-env>
```

Alle Parameter koennen auch per Kommandozeile ueberschrieben werden:
```bash
python3 enrich_metadata.py --token <dein-api-token> --ollama-url http://<ollama-host>:11434
```

### 6.3 Verfuegbare Ollama-Modelle

| Modell              | Groesse | Empfehlung                                      |
|---------------------|---------|--------------------------------------------------|
| `qwen2.5:14b`      | 14B     | **Empfohlen** - Beste Balance Qualitaet/Speed    |
| `llama3.1:8b`      | 8B      | Schneller, etwas weniger Qualitaet bei Deutsch   |
| `mistral-nemo:12b`  | 12B     | Gute Alternative                                 |

### 6.4 Automatisierung (Cron)

Fuer regelmaessige Anreicherung neuer Hoerbuecher:

```bash
# Crontab bearbeiten
crontab -e

# Taeglich um 03:00 Uhr neue Buecher anreichern
0 3 * * * cd <pfad-zum-projekt> && python3 enrich_metadata.py >> /var/log/abs-enrich.log 2>&1
```

---

## 7. Benutzerverwaltung

### 7.1 Admin-Benutzer

Ein Root-Admin-Benutzer wurde angelegt und hat vollen Zugriff auf
alle Einstellungen, Bibliotheken und die API.

### 7.2 Weitere Benutzer anlegen

1. Web-UI > **Settings** > **Users**
2. **"Add User"** klicken
3. Benutzername und Passwort vergeben
4. Rolle waehlen:
   - **Admin**: Vollzugriff inklusive Einstellungen
   - **User**: Kann Hoerbuecher hoeren und Fortschritt verwalten
   - **Guest**: Eingeschraenkter Zugriff

### 7.3 Bibliotheks-Zugriff einschraenken

Pro Benutzer kann festgelegt werden, welche der drei Bibliotheken sichtbar sind.
Das ist nuetzlich, wenn verschiedene Familienmitglieder unterschiedliche
Sammlungen sehen sollen.

---

## 8. Backup und Wiederherstellung

### 8.1 Zu sichernde Daten

| Pfad                                 | Inhalt                    | Prioritaet |
|--------------------------------------|---------------------------|------------|
| `<pfad-zum-projekt>/config/`         | Datenbank, Einstellungen  | **Hoch**   |
| `<pfad-zum-projekt>/metadata/`       | Covers, Metadaten-Cache   | Mittel     |
| `<pfad-zum-projekt>/.env`            | Zugangsdaten              | **Hoch**   |
| Alle drei Hoerbuecher-Sammlungen     | Die Audiofiles selbst     | **Hoch**   |

### 8.2 Backup erstellen

```bash
# Manuelles Backup der Konfiguration
tar -czf <backup-pfad>/audiobookshelf-config-$(date +%Y%m%d).tar.gz \
  -C <pfad-zum-projekt> config/ metadata/ .env
```

### 8.3 Wiederherstellung

```bash
# Container stoppen
cd <pfad-zum-projekt> && docker compose down

# Backup einspielen
tar -xzf <backup-pfad>/audiobookshelf-config-YYYYMMDD.tar.gz \
  -C <pfad-zum-projekt>

# Container starten
docker compose up -d
```

---

## 9. Zugriff von unterwegs (Tailscale)

Die Synology ist bereits ueber Tailscale erreichbar. Damit kann Audiobookshelf
sicher von unterwegs genutzt werden, ohne Ports ins Internet zu oeffnen.

### 9.1 Voraussetzung

- Tailscale ist auf der Synology installiert und aktiv
- Die Synology hat eine Tailscale-IP (z.B. `100.x.y.z`)

### 9.2 Tailscale auf dem iPhone einrichten

1. **App Store** oeffnen und **"Tailscale"** installieren
2. Tailscale-App oeffnen und mit demselben Account anmelden,
   der auch auf der Synology verwendet wird
3. Tailscale VPN aktivieren (Schieberegler auf "Connected")
4. Die Tailscale-IP der Synology notieren (sichtbar in der Tailscale-App
   unter "Machines" oder im Tailscale Admin Panel)

### 9.3 Audiobookshelf ueber Tailscale verwenden

In der Audiobookshelf-App als Server-Adresse verwenden:

```
http://<tailscale-ip>:<port>
```

Beispiel: `http://100.x.y.z:13378`

Das funktioniert sowohl im lokalen Netzwerk als auch von unterwegs,
solange Tailscale auf dem iPhone aktiv ist.

### 9.4 Vorteile gegenueber Reverse Proxy / Port-Forwarding

- **Kein offener Port** im Router noetig
- **Kein SSL-Zertifikat** noetig (Tailscale verschluesselt den Traffic)
- **Kein DNS / Domain** noetig
- **Automatisch sicher**: Nur Geraete im eigenen Tailscale-Netzwerk haben Zugriff

### 9.5 Tipps

- Tailscale auf dem iPhone so konfigurieren, dass es immer aktiv bleibt
  (unter iOS-Einstellungen > VPN > Tailscale > "Connect On Demand" aktivieren)
- Falls die Verbindung langsam ist: Tailscale nutzt wenn moeglich eine direkte
  Verbindung (WireGuard), ansonsten ein Relay. Direkte Verbindungen sind schneller.
- Die Tailscale-IP der Synology aendert sich nicht, solange das Geraet
  im selben Tailscale-Netzwerk bleibt

---

## 10. Troubleshooting

### Container startet nicht

```bash
# Logs pruefen
docker logs audiobookshelf

# Container-Status
docker inspect audiobookshelf | grep -i status
```

### Hoerbuecher werden nicht erkannt

1. Ordnerstruktur pruefen (ein Ordner pro Buch)
2. Dateiformate pruefen (unterstuetzt: MP3, M4B, M4A, FLAC, OGG, OPUS)
3. Bibliotheks-Scan manuell ausloesen
4. Pruefen ob der Mount-Punkt korrekt ist:
   ```bash
   docker exec audiobookshelf ls /audiobooks
   docker exec audiobookshelf ls /nas-audiobooks
   docker exec audiobookshelf ls /usb-audiobooks
   ```

### USB-Sammlung nicht verfuegbar

Falls die USB-Festplatte nicht eingebunden ist, startet der Container
moeglicherweise nicht. Pruefen:
```bash
ls <pfad-zur-usb-sammlung>
```
Falls der Pfad nicht existiert, die USB-Platte im DSM pruefen.

### Ollama-Skript meldet Fehler

```bash
# Ollama-Erreichbarkeit testen
curl http://<ollama-host>:11434/api/tags

# Audiobookshelf-API testen
source <pfad-zum-projekt>/.env
curl -H "Authorization: Bearer ${ABS_API_TOKEN}" \
  http://localhost:${ABS_PORT}/api/libraries
```

### Tailscale-Verbindung funktioniert nicht

1. Pruefen ob Tailscale auf der Synology laeuft:
   ```bash
   tailscale status
   ```
2. Pruefen ob Tailscale auf dem iPhone verbunden ist (gruenes Symbol)
3. Ping von einem anderen Tailscale-Geraet testen:
   ```bash
   ping <tailscale-ip>
   ```
4. Audiobookshelf-Port pruefen:
   ```bash
   curl http://<tailscale-ip>:<port>/healthcheck
   ```

---

## 11. Updates

### Audiobookshelf aktualisieren

```bash
cd <pfad-zum-projekt>

# Neues Image ziehen und Container neu starten
docker compose pull
docker compose up -d

# Pruefen ob der Container laeuft
docker ps --filter name=audiobookshelf
```

### Vor dem Update

- Backup erstellen (siehe Abschnitt 8)
- Release Notes pruefen: https://github.com/advplyr/audiobookshelf/releases
