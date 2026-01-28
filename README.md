# 📅 Urlaubsplan Transformation Tool

Ein Streamlit-basiertes Web-Tool zur Transformation von Excel-Urlaubsplänen in konsolidierte CSV-Formate mit zusammenhängenden Abwesenheitsblöcken.

## 🎯 Funktionen

- **Automatische Konsolidierung**: Fasst zusammenhängende Abwesenheitstage automatisch zu Blöcken zusammen
- **Mehrmonats-Verarbeitung**: Verarbeitet Excel-Dateien mit mehreren Monats-Tabellenblättern
- **Deutsches Datumsformat**: Ausgabe im Format `Tag.Monat.Jahr` (z.B. `28.1.2026`)
- **Interaktive Vorschau**: Zeigt die transformierten Daten vor dem Download an
- **Detaillierte Statistiken**: Bietet Einblicke in Abwesenheitsarten und Verteilungen
- **Benutzerfreundlich**: Einfaches Drag & Drop Interface

## 🚀 Live Demo

Die App ist verfügbar unter: [Ihr Streamlit Cloud Link]

## 📋 Verwendung

### 1. Excel-Datei vorbereiten

Die Excel-Datei sollte folgende Struktur haben:

- **Mehrere Tabellenblätter**: Ein Blatt pro Monat (z.B. "Januar", "Februar", "Januar 2027")
- **Zeile 1**: Datumsangaben (ab Spalte C oder später)
- **Spalte A**: Personalnummer (Pers.Nr)
- **Spalte B**: Name (optional)
- **Ab Spalte C**: Abwesenheiten für jeden Tag

**Beispiel:**

| Spalte A | Spalte B | Spalte C | Spalte D | Spalte E |
|----------|----------|----------|----------|----------|
| Heute ist |  | 1.1.2026 | 2.1.2026 | 3.1.2026 |
| 3 | Becker, Matthias | U |  | K |
| 35 | Korb, Thomas |  | U | U |
| 80 | Piur, Thomas | K | K |  |

### 2. Datei hochladen

- Öffnen Sie die Streamlit-App
- Laden Sie Ihre Excel-Datei (.xlsx oder .xls) hoch
- Die App verarbeitet automatisch alle Tabellenblätter

### 3. Ergebnis prüfen

- **Vorschau-Tab**: Überprüfen Sie die transformierten Daten
- **Statistik-Tab**: Sehen Sie sich Verteilungen und Metriken an
- **Verarbeitungsdetails**: Überprüfen Sie, welche Tabellenblätter verarbeitet wurden

### 4. CSV herunterladen

- Klicken Sie auf den Download-Button
- Die CSV-Datei wird mit Zeitstempel benannt (z.B. `urlaubsplan_consolidated_20260128_120000.csv`)

## 🔄 Transformation

### Vorher (Input):
```
1418,K,27.1.2026,27.1.2026
1418,K,28.1.2026,28.1.2026
1418,K,29.1.2026,29.1.2026
```

### Nachher (Output):
```
1418,K,27.1.2026,29.1.2026
```

Die App konsolidiert automatisch zusammenhängende Abwesenheitstage desselben Typs für jeden Mitarbeiter.

## 🛠️ Lokale Installation

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

### Installation

```bash
# Repository klonen
git clone https://github.com/IhrUsername/urlaubsplan-transformation.git
cd urlaubsplan-transformation

# Virtuelle Umgebung erstellen (optional, empfohlen)
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten
streamlit run streamlit_app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

## ☁️ Deployment auf Streamlit Cloud

1. **Repository auf GitHub veröffentlichen**
   - Erstellen Sie ein neues Repository auf GitHub
   - Laden Sie alle Dateien hoch (`streamlit_app.py`, `requirements.txt`, `README.md`)

2. **Mit Streamlit Cloud verbinden**
   - Gehen Sie zu [share.streamlit.io](https://share.streamlit.io)
   - Melden Sie sich mit Ihrem GitHub-Account an
   - Klicken Sie auf "New app"

3. **App konfigurieren**
   - **Repository**: Wählen Sie Ihr GitHub Repository
   - **Branch**: `main` (oder Ihr Standard-Branch)
   - **Main file path**: `streamlit_app.py`
   - Klicken Sie auf "Deploy"

4. **Fertig!**
   - Die App wird innerhalb weniger Minuten bereitgestellt
   - Sie erhalten eine öffentliche URL zum Teilen

## 📦 Abhängigkeiten

- **streamlit**: Web-Framework für die App
- **pandas**: Datenverarbeitung und -transformation
- **openpyxl**: Excel-Datei-Unterstützung (.xlsx)
- **xlrd**: Legacy Excel-Unterstützung (.xls)

## 📊 Unterstützte Abwesenheitsarten

Die App erkennt verschiedene Abwesenheitsarten, darunter:

- **U**: Urlaub
- **K**: Krank
- **KG**: Krankengeld
- **EZ**: Elternzeit
- **Ü**: Überstunden
- **Ho**: Home Office
- **BS**: Bildschirmarbeitsplatz
- Und weitere...

## 🔒 Datenschutz

- **Keine Datenspeicherung**: Alle Daten werden nur im Browser verarbeitet
- **Keine Server-seitige Speicherung**: Hochgeladene Dateien werden nicht dauerhaft gespeichert
- **Lokal verwendbar**: Die App kann auch komplett lokal ohne Internetverbindung genutzt werden

## 🤝 Beiträge

Beiträge sind willkommen! So können Sie helfen:

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

## 📝 Lizenz

Dieses Projekt ist Open Source und steht unter der MIT-Lizenz zur Verfügung.

## 👤 Autor

**Pete** - Marketing Director @ E+SERVICE+CHECK GmbH

## 🐛 Fehler melden

Wenn Sie Fehler finden oder Verbesserungsvorschläge haben, öffnen Sie bitte ein [Issue](https://github.com/IhrUsername/urlaubsplan-transformation/issues) auf GitHub.

## 📧 Kontakt

Für Fragen oder Unterstützung:
- GitHub Issues: [https://github.com/IhrUsername/urlaubsplan-transformation/issues](https://github.com/IhrUsername/urlaubsplan-transformation/issues)

---

**Entwickelt für E+SERVICE+CHECK GmbH | Januar 2026**
