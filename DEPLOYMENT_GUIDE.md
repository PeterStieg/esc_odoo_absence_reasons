# 🚀 Deployment Guide - Streamlit Cloud

Dieser Guide erklärt Schritt für Schritt, wie Sie die Urlaubsplan Transformation App auf Streamlit Cloud bereitstellen.

## Voraussetzungen

- GitHub Account (kostenlos)
- Streamlit Cloud Account (kostenlos, verbindet sich mit GitHub)

## Schritt 1: GitHub Repository erstellen

### 1.1 Neues Repository anlegen

1. Gehen Sie zu [github.com](https://github.com)
2. Klicken Sie oben rechts auf das **+** Symbol
3. Wählen Sie **"New repository"**
4. Füllen Sie die Felder aus:
   - **Repository name**: z.B. `urlaubsplan-transformation`
   - **Description**: `Tool zur Transformation von Excel-Urlaubsplänen`
   - **Visibility**: `Public` (für kostenlose Streamlit Cloud Nutzung)
   - ✅ **Add a README file** (kann später überschrieben werden)
5. Klicken Sie auf **"Create repository"**

### 1.2 Dateien hochladen

Es gibt zwei Möglichkeiten:

#### Option A: Via GitHub Web Interface (einfacher)

1. Klicken Sie im Repository auf **"Add file"** > **"Upload files"**
2. Laden Sie folgende Dateien hoch:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README.md`
   - `LICENSE`
   - `.gitignore`
3. Optional: Ordner `.streamlit/` mit `config.toml`
4. Commit-Message: `Initial commit - Urlaubsplan Transformation Tool`
5. Klicken Sie auf **"Commit changes"**

#### Option B: Via Git Command Line (für Git-Nutzer)

```bash
# Repository klonen
git clone https://github.com/IhrUsername/urlaubsplan-transformation.git
cd urlaubsplan-transformation

# Dateien kopieren (aus dem Verzeichnis wo Sie die Dateien gespeichert haben)
cp /pfad/zu/streamlit_app.py .
cp /pfad/zu/requirements.txt .
cp /pfad/zu/README.md .
cp /pfad/zu/LICENSE .
cp /pfad/zu/.gitignore .

# Optional: .streamlit Ordner erstellen
mkdir .streamlit
cp /pfad/zu/config.toml .streamlit/

# Dateien hinzufügen und committen
git add .
git commit -m "Initial commit - Urlaubsplan Transformation Tool"
git push origin main
```

## Schritt 2: Streamlit Cloud Setup

### 2.1 Streamlit Cloud Account erstellen

1. Gehen Sie zu [share.streamlit.io](https://share.streamlit.io)
2. Klicken Sie auf **"Sign up"** oder **"Continue with GitHub"**
3. Autorisieren Sie Streamlit für Ihren GitHub Account
4. Akzeptieren Sie die Nutzungsbedingungen

### 2.2 App bereitstellen

1. Klicken Sie auf **"New app"** (oder das **+** Symbol)
2. Wählen Sie:
   - **Repository**: Ihr gerade erstelltes Repository auswählen
   - **Branch**: `main` (Standard)
   - **Main file path**: `streamlit_app.py`
3. **Optional**: Erweiterte Einstellungen
   - **App URL**: Passen Sie die URL an (z.B. `urlaubsplan-transform`)
   - **Python version**: 3.11 (empfohlen, oder 3.10)
4. Klicken Sie auf **"Deploy!"**

### 2.3 Warten auf Deployment

- Der Deployment-Prozess dauert 2-5 Minuten
- Sie sehen live Logs während der Installation
- Bei Erfolg: ✅ **"Your app is live!"**
- Sie erhalten eine URL wie: `https://urlaubsplan-transform.streamlit.app`

## Schritt 3: App testen

1. Öffnen Sie die bereitgestellte URL
2. Testen Sie die Funktionalität:
   - ✅ Datei-Upload funktioniert
   - ✅ Verarbeitung läuft durch
   - ✅ Vorschau wird angezeigt
   - ✅ Download funktioniert
3. Prüfen Sie auf verschiedenen Geräten:
   - Desktop/Laptop
   - Tablet
   - Smartphone

## Schritt 4: App teilen

### Öffentliche URL

Ihre App ist jetzt unter folgender URL erreichbar:
```
https://ihre-app-name.streamlit.app
```

### URL anpassen (optional)

1. Gehen Sie zu Streamlit Cloud Dashboard
2. Klicken Sie auf Ihre App
3. Settings > General
4. Ändern Sie die **"App URL"**
5. Speichern

### App in README verlinken

Aktualisieren Sie die README.md im Repository:

```markdown
## 🚀 Live Demo

Die App ist verfügbar unter: https://ihre-app-name.streamlit.app
```

## Troubleshooting

### Problem: Deployment schlägt fehl

**Lösung 1**: Überprüfen Sie die Logs
- Gehen Sie zu Streamlit Cloud Dashboard
- Klicken Sie auf Ihre App > "Manage app" > "Logs"
- Suchen Sie nach Fehlermeldungen

**Lösung 2**: Requirements prüfen
- Stellen Sie sicher, dass alle Pakete in `requirements.txt` verfügbar sind
- Versuchen Sie spezifische Versionen anzugeben

**Lösung 3**: Python Version
- Streamlit Cloud unterstützt Python 3.8-3.11
- Ändern Sie die Version in den App-Einstellungen

### Problem: App lädt nicht richtig

**Lösung**: Browser-Cache leeren
- Drücken Sie `Ctrl + Shift + R` (Windows/Linux)
- Drücken Sie `Cmd + Shift + R` (Mac)

### Problem: Upload-Fehler

**Lösung**: Dateigrößen-Limit
- Standard-Limit: 200 MB
- Kann in `.streamlit/config.toml` angepasst werden:
  ```toml
  [server]
  maxUploadSize = 200
  ```

### Problem: App ist langsam

**Lösung**: Streamlit Cloud Ressourcen
- Kostenlose Version: Begrenzte Ressourcen
- Upgrade auf Streamlit Cloud Teams für mehr Performance

## Updates und Wartung

### App aktualisieren

1. **Änderungen im Code machen**
   ```bash
   git add .
   git commit -m "Update: Neue Funktion XYZ"
   git push origin main
   ```

2. **Automatisches Redeployment**
   - Streamlit Cloud erkennt automatisch Updates
   - Die App wird innerhalb von 1-2 Minuten neu bereitgestellt

### Manuelles Redeployment

Falls erforderlich:
1. Gehen Sie zu Streamlit Cloud Dashboard
2. Klicken Sie auf Ihre App
3. Klicken Sie auf ⋮ (drei Punkte) > **"Reboot"**

## Best Practices

### ✅ Empfohlene Vorgehensweise

- **Branches nutzen**: Testen Sie neue Features in separaten Branches
- **Versionen taggen**: Nutzen Sie Git Tags für Releases
- **Secrets verwenden**: Für API-Keys nutzen Sie Streamlit Secrets
- **Monitoring**: Überprüfen Sie regelmäßig die Logs
- **Backups**: GitHub ist Ihr Backup - committen Sie regelmäßig

### ⚠️ Zu vermeiden

- ❌ Große Dateien ins Repository committen (nutzen Sie `.gitignore`)
- ❌ Sensible Daten im Code (nutzen Sie Streamlit Secrets)
- ❌ Direkt auf `main` pushen ohne Tests

## Erweiterte Konfiguration

### Custom Domain (Optional)

1. Upgrade auf Streamlit Cloud Teams
2. Fügen Sie eine Custom Domain hinzu
3. Konfigurieren Sie DNS-Einträge

### Monitoring und Analytics

1. **Streamlit Cloud Metrics**: Automatisch verfügbar
2. **Google Analytics**: Kann hinzugefügt werden
3. **Custom Logging**: Via Python logging

## Support

### Hilfe bekommen

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: In Ihrem Repository

### Weitere Ressourcen

- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Best Practices](https://docs.streamlit.io/knowledge-base/tutorials/deploy)

---

**Viel Erfolg mit Ihrer App! 🚀**
