# ============================================================
# Automatisierungs-Skript für Windows 7
# Erkennt Screenshots auf dem Bildschirm und klickt sie
# ============================================================

import pyautogui
import time
import os
import sys

# ============================================================
# EINSTELLUNGEN - Hier kannst du alles anpassen!
# ============================================================

# Ordner wo deine Screenshots liegen
SCREENSHOT_ORDNER = "screenshots"

# Wartezeit zwischen den Klicks (in Sekunden)
WARTEZEIT_ZWISCHEN_KLICKS = 1.5

# Wie lange soll nach jedem Feld gesucht werden? (in Sekunden)
SUCH_TIMEOUT = 10

# Wie genau muss der Treffer sein? (0.0 - 1.0, empfohlen: 0.8)
GENAUIGKEIT = 0.8

# Wartezeit vor dem Start (Zeit um Fenster zu öffnen)
START_WARTEZEIT = 3

# ============================================================
# REIHENFOLGE DER FELDER - Hier die Reihenfolge festlegen!
# ============================================================

# Trage hier die Dateinamen deiner Screenshots in der
# gewünschten Reihenfolge ein!
FELDER_REIHENFOLGE = [
    "feld1.png",
    "feld2.png",
    "feld3.png",
    # Weitere Felder hier hinzufügen...
]

# ============================================================
# FUNKTIONEN
# ============================================================

def prüfe_screenshots():
    """Prüft ob alle Screenshot Dateien vorhanden sind"""
    print("\n🔍 Prüfe ob alle Screenshots vorhanden sind...")
    alle_vorhanden = True

    for feld in FELDER_REIHENFOLGE:
        pfad = os.path.join(SCREENSHOT_ORDNER, feld)
        if os.path.exists(pfad):
            print(f"  ✅ Gefunden: {feld}")
        else:
            print(f"  ❌ FEHLT:    {feld}")
            alle_vorhanden = False

    return alle_vorhanden

def finde_und_klicke(feld_name, timeout=SUCH_TIMEOUT):
    """
    Sucht ein Feld auf dem Bildschirm und klickt es
    
    Parameter:
        feld_name: Dateiname des Screenshots
        timeout:   Wie lange gesucht wird (Sekunden)
    
    Rückgabe:
        True  = Erfolgreich geklickt
        False = Feld nicht gefunden
    """
    pfad = os.path.join(SCREENSHOT_ORDNER, feld_name)
    start_zeit = time.time()

    print(f"\n🔍 Suche nach: {feld_name}")

    while True:
        # Zeit prüfen
        vergangene_zeit = time.time() - start_zeit
        if vergangene_zeit > timeout:
            print(f"  ⏰ Timeout! '{feld_name}' wurde nicht gefunden!")
            return False

        try:
            # Auf dem Bildschirm suchen
            position = pyautogui.locateOnScreen(
                pfad,
                confidence=GENAUIGKEIT
            )

            if position is not None:
                # Mittelpunkt des gefundenen Bereichs berechnen
                mitte = pyautogui.center(position)

                print(f"  ✅ Gefunden bei Position: X={mitte.x}, Y={mitte.y}")

                # Maus sanft zur Position bewegen
                pyautogui.moveTo(
                    mitte.x,
                    mitte.y,
                    duration=0.5  # Bewegungsdauer in Sekunden
                )

                # Klicken!
                pyautogui.click(mitte.x, mitte.y)
                print(f"  🖱️  Geklickt!")

                return True

        except pyautogui.ImageNotFoundException:
            # Noch nicht gefunden, weiter suchen
            pass
        except Exception as e:
            print(f"  ⚠️  Fehler bei der Suche: {e}")
            return False

        # Kurz warten bevor erneut gesucht wird
        time.sleep(0.5)
        print(f"  ⏳ Suche läuft... ({vergangene_zeit:.0f}s / {timeout}s)")

def starte_automatisierung():
    """Hauptfunktion - Startet die komplette Automatisierung"""

    print("=" * 50)
    print("  🤖 AUTOMATISIERUNGS-SKRIPT GESTARTET")
    print("=" * 50)

    # Schritt 1: Screenshots prüfen
    if not prüfe_screenshots():
        print("\n❌ Fehler: Nicht alle Screenshots gefunden!")
        print("   Bitte lege alle benötigten Screenshots")
        print(f"  in den Ordner: {SCREENSHOT_ORDNER}")
        sys.exit(1)

    # Schritt 2: Countdown vor dem Start
    print(f"\n⏳ Skript startet in {START_WARTEZEIT} Sekunden...")
    print("   Öffne jetzt das gewünschte Programm/Fenster!")

    for i in range(START_WARTEZEIT, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    print("\n🚀 Starte Automatisierung!\n")

    # Schritt 3: Felder der Reihe nach suchen und klicken
    erfolge = 0
    fehler = 0

    for nummer, feld in enumerate(FELDER_REIHENFOLGE, start=1):
        print(f"\n{'=' * 40}")
        print(f"  Schritt {nummer} von {len(FELDER_REIHENFOLGE)}: {feld}")
        print(f"{'=' * 40}")

        # Feld suchen und klicken
        erfolgreich = finde_und_klicke(feld)

        if erfolgreich:
            erfolge += 1
            print(f"  ✅ Schritt {nummer} erfolgreich!")

            # Warten bevor nächstes Feld
            if nummer < len(FELDER_REIHENFOLGE):
                print(f"  ⏳ Warte {WARTEZEIT_ZWISCHEN_KLICKS}s vor nächstem Schritt...")
                time.sleep(WARTEZEIT_ZWISCHEN_KLICKS)
        else:
            fehler += 1
            print(f"  ❌ Schritt {nummer} fehlgeschlagen!")

            # Fragen ob weiter gemacht werden soll
            antwort = input("\n  Trotzdem weitermachen? (j/n): ")
            if antwort.lower() != 'j':
                print("\n⛔ Automatisierung abgebrochen!")
                break

    # Schritt 4: Zusammenfassung
    print("\n" + "=" * 50)
    print("  📊 ZUSAMMENFASSUNG")
    print("=" * 50)
    print(f"  ✅ Erfolgreich: {erfolge} von {len(FELDER_REIHENFOLGE)}")
    print(f"  ❌ Fehlgeschlagen: {fehler} von {len(FELDER_REIHENFOLGE)}")

    if fehler == 0:
        print("\n  🎉 Alle Schritte erfolgreich abgeschlossen!")
    else:
        print("\n  ⚠️  Einige Schritte sind fehlgeschlagen!")

    print("=" * 50)

# ============================================================
# PROGRAMM STARTEN
# ============================================================

if __name__ == "__main__":
    try:
        starte_automatisierung()
    except KeyboardInterrupt:
        print("\n\n⛔ Skript durch Benutzer gestoppt (Strg+C)")
        sys.exit(0)