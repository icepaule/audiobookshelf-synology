# Audiobookshelf - Benutzerhandbuch

## Inhaltsverzeichnis

1. [Was ist Audiobookshelf?](#1-was-ist-audiobookshelf)
2. [Erste Schritte](#2-erste-schritte)
3. [iPhone-App einrichten](#3-iphone-app-einrichten)
4. [Zugriff von unterwegs (Tailscale)](#4-zugriff-von-unterwegs-tailscale)
5. [Hoerbuecher durchsuchen und abspielen](#5-hoerbuecher-durchsuchen-und-abspielen)
6. [Einschlaf-Timer](#6-einschlaf-timer)
7. [Offline-Download](#7-offline-download)
8. [Lesezeichen und Fortschritt](#8-lesezeichen-und-fortschritt)
9. [Sammlungen und Serien](#9-sammlungen-und-serien)
10. [Die drei Bibliotheken](#10-die-drei-bibliotheken)
11. [Tipps fuer Einschlaf-Hoerbuecher](#11-tipps-fuer-einschlaf-hoerbuecher)
12. [Haeufige Fragen](#12-haeufige-fragen)

---

## 1. Was ist Audiobookshelf?

Audiobookshelf ist dein persoenlicher Hoerbuch-Server. Er laeuft auf dem
NAS zu Hause und stellt deine gesamte Hoerbuch-Sammlung zum Streamen bereit -
aehnlich wie Spotify, aber fuer deine eigenen Hoerbuecher.

**Vorteile:**
- Alle Hoerbuecher an einem Ort
- Streaming auf iPhone, iPad und im Browser
- Automatische Zusammenfassungen und Genre-Erkennung
- Einschlaf-Timer und Lesezeichen
- Dein Hoerfortschritt wird geraeteuebergreifend synchronisiert
- Sicherer Zugriff von unterwegs ueber Tailscale

---

## 2. Erste Schritte

### Im Browser

1. Oeffne im Browser: `http://<nas-ip>:<port>`
2. Melde dich mit deinem Benutzernamen und Passwort an
3. Du siehst deine Hoerbuch-Bibliotheken

### Zugangsdaten

Deine Zugangsdaten erhaeltst du vom Administrator.
Beim ersten Login wirst du ggf. aufgefordert, dein Passwort zu aendern.

---

## 3. iPhone-App einrichten

### 3.1 App herunterladen

1. Oeffne den **App Store** auf deinem iPhone
2. Suche nach **"Audiobookshelf"**
3. Tippe auf **"Laden"** -- die App ist kostenlos
4. Warte bis die Installation abgeschlossen ist

### 3.2 Server-Verbindung herstellen (im WLAN zu Hause)

1. Oeffne die Audiobookshelf-App
2. Du siehst den Login-Bildschirm mit einem Feld fuer die Server-Adresse
3. Gib als Server-Adresse ein: `http://<nas-ip>:<port>`
4. Gib deinen **Benutzernamen** ein
5. Gib dein **Passwort** ein
6. Tippe auf **"Verbinden"** bzw. **"Login"**

**Wichtig:** Dein iPhone muss mit demselben WLAN wie das NAS verbunden sein,
damit die lokale Adresse funktioniert.

### 3.3 Erste Schritte in der App

Nach dem Login siehst du:

- **Home**: Zuletzt gehoerte und neue Hoerbuecher
- **Bibliothek**: Alle Hoerbuecher als Kacheln oder Liste
- **Suche**: Finde Hoerbuecher nach Titel, Autor oder Genre
- **Downloads**: Deine offline verfuegbaren Hoerbuecher

**Tipp:** Ueber das Hamburger-Menue (drei Striche) oder die untere Navigation
kannst du zwischen den Bibliotheken wechseln, um verschiedene Sammlungen zu sehen.

---

## 4. Zugriff von unterwegs (Tailscale)

Damit du deine Hoerbuecher auch unterwegs (mobiles Netz, fremdes WLAN)
streamen kannst, ist der Server ueber Tailscale erreichbar.

### 4.1 Was ist Tailscale?

Tailscale ist ein sicheres VPN-Netzwerk, das deine Geraete miteinander
verbindet -- egal wo sie sich befinden. Der NAS ist bereits eingerichtet.

### 4.2 Tailscale auf dem iPhone einrichten

1. Oeffne den **App Store** und suche nach **"Tailscale"**
2. Installiere die kostenlose App
3. Oeffne Tailscale und melde dich an (nutze denselben Account
   wie auf der Synology -- den bekommst du vom Administrator)
4. Aktiviere die VPN-Verbindung (Schieberegler auf "Connected")
5. Erlaube die VPN-Konfiguration, wenn iOS danach fragt

### 4.3 Audiobookshelf ueber Tailscale nutzen

Sobald Tailscale aktiv ist, verwende in der Audiobookshelf-App die
Tailscale-Adresse statt der lokalen IP:

```
http://<tailscale-ip>:<port>
```

Diese Adresse bekommst du vom Administrator. Sie funktioniert sowohl
zu Hause im WLAN als auch unterwegs ueber mobiles Netz.

### 4.4 Tipps fuer den mobilen Zugriff

- **"Connect On Demand"** in den iOS-Einstellungen aktivieren
  (Einstellungen > VPN > Tailscale), damit Tailscale sich automatisch verbindet
- Falls du unterwegs wenig Datenvolumen hast: Lade Hoerbuecher vorher zu Hause
  herunter (siehe Abschnitt 7)
- Die Tailscale-Verbindung ist verschluesselt -- du brauchst kein HTTPS

---

## 5. Hoerbuecher durchsuchen und abspielen

### 5.1 Bibliothek durchsuchen

- **Startseite**: Zeigt zuletzt gehoerte und neue Hoerbuecher
- **Bibliothek**: Alle Hoerbuecher in der Uebersicht
- **Suche**: Tippe auf die Lupe und suche nach Titel, Autor oder Genre

### 5.2 Hoerbuch starten

1. Tippe auf ein Hoerbuch-Cover
2. Du siehst die Detailseite mit:
   - Zusammenfassung
   - Genre
   - Einschlaf-Eignung (falls vorhanden)
   - Kapitelstruktur
3. Tippe auf **"Play"** um das Hoerbuch zu starten

### 5.3 Wiedergabe steuern

| Aktion                  | Geste / Button                        |
|-------------------------|---------------------------------------|
| Play / Pause            | Grosser Play-Button                   |
| 30 Sekunden zurueck     | Pfeil-Button links                    |
| 30 Sekunden vor         | Pfeil-Button rechts                   |
| Kapitel wechseln        | Kapitel-Liste oeffnen                 |
| Geschwindigkeit aendern | Speed-Button (0.5x bis 3.0x)         |
| Einschlaf-Timer         | Mond-Symbol                           |

---

## 6. Einschlaf-Timer

Der Einschlaf-Timer ist das Herzstuck fuer naechtliches Hoeren.

### Timer einstellen

1. Waehrend der Wiedergabe auf das **Mond-Symbol** tippen
2. Waehle eine Zeit:
   - **5 Minuten** - Fuer kurzes Einnicken
   - **10 Minuten** - Standard
   - **15 Minuten** - Etwas laengeres Hoeren
   - **30 Minuten** - Fuer laengere Einschlafphasen
   - **45 / 60 Minuten** - Wenn es laenger dauert
   - **Ende des Kapitels** - Stoppt am Kapitelende
3. Die Wiedergabe stoppt automatisch nach der gewaehlten Zeit

### Tipps

- Der Timer blendet die Lautstaerke vor dem Stopp sanft aus
- Wenn du aufwachst und weiterhoeren willst: einfach Play druecken
- Dein Fortschritt wird automatisch gespeichert

---

## 7. Offline-Download

Du kannst Hoerbuecher herunterladen, um sie ohne Internetverbindung zu hoeren -
perfekt fuer Reisen oder wenn das WLAN nachts instabil ist.

### Hoerbuch herunterladen

1. Gehe zur Detailseite eines Hoerbuchs
2. Tippe auf das **Download-Symbol** (Pfeil nach unten)
3. Waehle ob du das komplette Buch oder einzelne Kapitel laden willst
4. Der Download startet im Hintergrund

### Downloads verwalten

- **App > Downloads**: Zeigt alle heruntergeladenen Hoerbuecher
- Zum Loeschen: Auf dem Eintrag nach links wischen
- Heruntergeladene Buecher sind mit einem Haekchen markiert

**Speicherplatz beachten:** Ein typisches Hoerbuch braucht 100-500 MB.

**Tipp fuer unterwegs:** Lade Hoerbuecher zu Hause im WLAN herunter,
dann brauchst du unterwegs kein Tailscale und kein mobiles Datenvolumen.

---

## 8. Lesezeichen und Fortschritt

### Automatischer Fortschritt

- Dein Hoerfortschritt wird automatisch gespeichert
- Beim naechsten Oeffnen wird genau dort fortgesetzt, wo du aufgehoert hast
- Der Fortschritt synchronisiert sich zwischen iPhone und Browser

### Lesezeichen setzen

1. Waehrend der Wiedergabe auf das **Lesezeichen-Symbol** tippen
2. Optional eine Notiz eingeben (z.B. "Spannende Stelle")
3. Tippe auf **"Speichern"**

### Lesezeichen aufrufen

1. Gehe zur Detailseite des Hoerbuchs
2. Oeffne den Tab **"Lesezeichen"**
3. Tippe auf ein Lesezeichen, um dorthin zu springen

---

## 9. Sammlungen und Serien

### Hoerbuch-Serien

Wenn Hoerbuecher zu einer Serie gehoeren, werden sie automatisch gruppiert.
Du findest Serien unter:
- **Bibliothek > Serien**

### Eigene Sammlungen erstellen

Du kannst eigene Sammlungen anlegen, z.B. "Einschlaf-Favoriten":

1. Gehe zu einem Hoerbuch
2. Tippe auf **"Zur Sammlung hinzufuegen"**
3. Waehle eine bestehende Sammlung oder erstelle eine neue

---

## 10. Die drei Bibliotheken

Dein Audiobookshelf hat drei separate Bibliotheken:

| Bibliothek        | Beschreibung                                         |
|-------------------|------------------------------------------------------|
| Eigene Sammlung   | Persoenliche Hoerbuecher, die du selbst hinzugefuegt hast |
| NAS-Sammlung      | Bestehende Sammlung auf dem NAS                      |
| USB-Sammlung      | Hoerbuecher von einer externen USB-Festplatte        |

Du kannst oben in der App oder im Browser zwischen den Bibliotheken wechseln.
Jede Bibliothek hat ihre eigene Suche, Sortierung und Fortschrittsanzeige.

**Neues Hoerbuch hinzufuegen:** Eigene Hoerbuecher koennen ueber den
Samba-Share (Netzwerkfreigabe) in die eigene Sammlung kopiert werden.
Frage den Administrator nach dem Freigabepfad.

---

## 11. Tipps fuer Einschlaf-Hoerbuecher

### Geeignete Genres

Die KI-gesteuerte Metadaten-Anreicherung bewertet jedes Hoerbuch
mit einer **Einschlaf-Eignung**. Generell gilt:

| Genre          | Eignung       | Warum?                                         |
|----------------|---------------|------------------------------------------------|
| Maerchen       | Sehr gut      | Vertraute Geschichten, ruhiger Erzaehlfluss    |
| Klassiker      | Gut           | Oft langsames Tempo, bekannte Handlung         |
| Sachbuch       | Gut           | Gleichmaessiger Vortrag                        |
| Naturdoku      | Sehr gut      | Beruhigende Themen                             |
| Krimi/Thriller | Weniger       | Spannungsbogen haelt wach                      |
| Horror         | Weniger       | Kann Einschlafen erschweren                    |

### Optimale Einstellungen zum Einschlafen

1. **Geschwindigkeit**: 0.8x bis 1.0x (etwas langsamer als normal)
2. **Einschlaf-Timer**: 15-30 Minuten
3. **Lautstaerke**: Etwas leiser als tagsueber
4. **iPhone-Einstellung**: "Nicht stoeren" aktivieren

### Empfohlene Routine

1. Hoerbuch und Kapitel waehlen
2. Timer auf 15-20 Minuten stellen
3. Geschwindigkeit auf 0.9x reduzieren
4. Licht aus, Augen zu, zuhoeren

---

## 12. Haeufige Fragen

### "Die App kann den Server nicht finden"

- Stelle sicher, dass dein iPhone im gleichen WLAN wie das NAS ist
- Pruefe die Server-Adresse: `http://<nas-ip>:<port>`
- Falls du unterwegs bist: Ist Tailscale auf dem iPhone aktiviert?
  Verwende dann die Tailscale-Adresse: `http://<tailscale-ip>:<port>`
- Frage den Administrator, ob der Server laeuft

### "Das Hoerbuch hat keine Beschreibung"

Neue Hoerbuecher werden automatisch vom KI-System beschrieben.
Dies kann einige Minuten dauern. Falls nach einem Tag noch keine
Beschreibung vorhanden ist, wende dich an den Administrator.

### "Der Fortschritt wurde nicht gespeichert"

Der Fortschritt wird alle 10 Sekunden synchronisiert. Wenn du die App
sofort nach dem Stoppen schliesst, koennen die letzten Sekunden verloren gehen.
Warte kurz, bevor du die App beendest.

### "Wie kann ich mein Passwort aendern?"

1. Oeffne die Web-UI im Browser
2. Klicke oben rechts auf deinen Benutzernamen
3. Waehle **"Einstellungen"**
4. Unter **"Passwort aendern"** das neue Passwort eingeben

### "Kann ich Hoerbuecher auch im Auto hoeren?"

Ja! Verbinde dein iPhone per Bluetooth oder CarPlay mit dem Autoradio.
Audiobookshelf erscheint als Audioquelle. Du brauchst dafuer eine
Internetverbindung zum NAS -- aktiviere Tailscale auf dem iPhone,
dann funktioniert es ueber das mobile Netz.
Alternativ: Lade das Hoerbuch vorher herunter (siehe Abschnitt 7).

### "Wie gross ist der Speicherverbrauch der App?"

Die App selbst braucht ca. 50 MB. Heruntergeladene Hoerbuecher
benoetigen zusaetzlichen Platz (100-500 MB pro Buch).

### "Muss Tailscale immer an sein?"

Nein. Tailscale wird nur benoetigt, wenn du von ausserhalb deines
Heim-WLANs auf den Server zugreifen willst. Zu Hause funktioniert
alles ueber die lokale IP-Adresse.

### "Ich brauche Hilfe"

Wende dich an den Administrator oder schaue in die offizielle
Dokumentation: https://www.audiobookshelf.org/docs
