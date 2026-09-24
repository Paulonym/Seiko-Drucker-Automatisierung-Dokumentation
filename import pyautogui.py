import pyautogui
import time
import sys

# ============================================================
# KONFIGURATION – Zeitlimits und Wartezeiten (in Sekunden)
# ============================================================
CONFIG = {
    "min_wait_pcon_step":       2.0,   # Mindestlaufzeit nach pCon-Schritt
    "max_wait_pcon_step":      10.0,   # Maximallaufzeit für pCon-Schritt
    "min_wait_mrconfig_step":   2.0,   # Mindestlaufzeit nach MR Config-Schritt
    "max_wait_switch_window":  10.0,   # Maximallaufzeit für Fensterwechsel
    "wait_after_opstart":       2.0,   # Wartezeit nach opstartmrconfig
    "wait_after_arrow":         1.5,   # Wartezeit nach Pfeil-Klick
    "search_confidence":        0.8,   # Erkennungssicherheit für pyautogui
}

# ============================================================
# CHECKLISTE – Einfach erweiterbar
# ============================================================
CHECKLIST = [
    "Stecker eingesteckt",
    "Handbetrieb eingestellt",
    "MR Config gestartet",
    "Positionsdatei in MR Config geladen",
    "pCon Software gestartet",
    "Positionsdatei in pCon geladen",
    # Weitere Punkte hier einfach hinzufügen:
    # "Neuer Punkt",
]

# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def find_and_click(image_path, timeout=10.0, min_wait=0.0, description=""):
    """
    Sucht ein Bild auf dem Bildschirm und klickt darauf.
    Wartet mindestens min_wait Sekunden, maximal timeout Sekunden.
    Gibt True zurück wenn erfolgreich, False wenn nicht gefunden.
    """
    start_time = time.time()
    print(f"  🔍 Suche nach: {description or image_path}")

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(
                image_path,
                confidence=CONFIG["search_confidence"]
            )
            if location:
                elapsed = time.time() - start_time
                # Mindestlaufzeit einhalten
                if elapsed < min_wait:
                    time.sleep(min_wait - elapsed)
                pyautogui.click(location)
                print(f"  ✅ Gefunden und geklickt: {description or image_path}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)

    print(f"  ❌ FEHLER: '{description or image_path}' nicht gefunden innerhalb von {timeout}s!")
    return False

def is_on_screen(image_path):
    """
    Prüft ob ein Bild auf dem Bildschirm sichtbar ist (ohne zu klicken).
    """
    try:
        location = pyautogui.locateOnScreen(
            image_path,
            confidence=CONFIG["search_confidence"]
        )
        return location is not None
    except pyautogui.ImageNotFoundException:
        return False

def ensure_pcon_active():
    """
    Stellt sicher, dass das pCon-Fenster aktiv ist.
    """
    print("\n  🪟 Prüfe ob pCon-Fenster aktiv ist...")
    if is_on_screen("currentwindowpcon.png"):
        print("  ✅ pCon-Fenster ist bereits aktiv.")
        return True
    else:
        print("  ⚠️  pCon nicht aktiv – suche Icon in Taskleiste...")
        success = find_and_click(
            "pconicon.png",
            timeout=CONFIG["max_wait_switch_window"],
            description="pCon Taskleisten-Icon"
        )
        if not success:
            print("  ❌ KRITISCH: pCon konnte nicht aktiviert werden!")
            sys.exit(1)
        time.sleep(1.0)
        return True

def ensure_mrconfig_active():
    """
    Stellt sicher, dass das MR Config-Fenster aktiv ist.
    """
    print("\n  🪟 Wechsle zu MR Config...")
    if is_on_screen("currentwindowmrconfig.png"):
        print("  ✅ MR Config-Fenster ist bereits aktiv.")
        return True
    else:
        print("  ⚠️  MR Config nicht aktiv – suche Icon in Taskleiste...")
        success = find_and_click(
            "mrconfigicon.png",
            timeout=CONFIG["max_wait_switch_window"],
            description="MR Config Taskleisten-Icon"
        )
        if not success:
            print("  ❌ KRITISCH: MR Config konnte nicht aktiviert werden!")
            sys.exit(1)
        time.sleep(1.0)
        return True

# ============================================================
# SCHRITT-FUNKTIONEN
# ============================================================

def mrconfig_sequence():
    """
    SchrittMRConfig – Die immer gleiche MR Config-Sequenz.
    Wiederverwendbar in SchrittPcon0 und SchrittPcon.
    Alle Pfeil- und OP-Start-Schritte haben Mindestlaufzeiten.
    """
    print("\n  ⚙️  Starte MR Config Sequenz...")

    if not is_on_screen("currentwindowmrconfig.png"):
        print("  ❌ MR Config Fenster nicht erkannt!")
        sys.exit(1)

    if not is_on_screen("pointtableno1.png"):
        print("  ❌ Punkttabelle Nr. 1 nicht gefunden!")
        sys.exit(1)

    # ── Schritt 1: OP Start ──────────────────────────────────
    if not find_and_click(
        "opstartmrconfig.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_mrconfig_step"],
        description="OP Start MR Config (1)"
    ):
        sys.exit(1)
    time.sleep(CONFIG["wait_after_opstart"])

    # ── Schritt 2: Pfeil HOCH ────────────────────────────────
    if not find_and_click(
        "pfeilhoch.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_mrconfig_step"],
        description="Pfeil Hoch"
    ):
        sys.exit(1)
    time.sleep(CONFIG["wait_after_arrow"])

    # ── Schritt 3: OP Start ──────────────────────────────────
    if not find_and_click(
        "opstartmrconfig.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_mrconfig_step"],
        description="OP Start MR Config (2)"
    ):
        sys.exit(1)
    time.sleep(CONFIG["wait_after_opstart"])

    # ── Schritt 4: Pfeil RUNTER ──────────────────────────────
    if not find_and_click(
        "pfeilrunter.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_mrconfig_step"],
        description="Pfeil Runter"
    ):
        sys.exit(1)
    time.sleep(CONFIG["wait_after_arrow"])

    # ── Schritt 5: OP Start (letzter) ───────────────────────
    if not find_and_click(
        "opstartmrconfig.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_mrconfig_step"],
        description="OP Start MR Config (3)"
    ):
        sys.exit(1)
    time.sleep(CONFIG["wait_after_opstart"])

    print("  ✅ MR Config Sequenz abgeschlossen.")

def schritt_pcon0():
    """
    SchrittPcon0 – Wird NUR EINMAL am Anfang ausgeführt.
    Initialisierungsschritt: Erster Schritt + Erster Spaltenpunkt + MR Config.

    ⚠️  Schritt 1 (Schritt in pCon auswählen) wird NUR ausgeführt,
        wenn pos0.png NICHT auf dem Bildschirm gefunden wird.
    """
    print(f"\n{'='*55}")
    print(f"  🚀 SchrittPcon0 – Initialisierung (einmalig)")
    print(f"{'='*55}")

    # 1. pCon aktivieren
    ensure_pcon_active()

    # ── Schritt 1: NUR ausführen wenn pos0.png NICHT sichtbar ──
    print("\n  🔍 Prüfe ob Position 0 bereits aktiv (pos0.png)...")
    if not is_on_screen("pos0.png"):
        print("  ℹ️  pos0.png nicht gefunden → Schritt 1 wird ausgeführt...")
        if not find_and_click(
            "schrittpcon.png",
            timeout=CONFIG["max_wait_pcon_step"],
            min_wait=CONFIG["min_wait_pcon_step"],
            description="Schritt in pCon auswählen (Schritt 1)"
        ):
            sys.exit(1)
    else:
        print("  ✅ pos0.png gefunden → Position bereits aktiv, Schritt 1 wird übersprungen.")

    # ── Schritt 2: Ersten Spaltenpunkt anfahren (IMMER) ────────
    print("\n  📌 Schritt 2: Ersten Spaltenpunkt anfahren...")
    if not find_and_click(
        "schrittpcon.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_pcon_step"],
        description="Erster Spaltenpunkt"
    ):
        sys.exit(1)

    # Mindestlaufzeit vor Fensterwechsel
    time.sleep(CONFIG["min_wait_pcon_step"])

    # ── Schritt 3: Zu MR Config wechseln ───────────────────────
    ensure_mrconfig_active()

    # ── Schritt 4: MR Config Sequenz ausführen ─────────────────
    mrconfig_sequence()

    # ── Schritt 5: Zurück zu pCon ──────────────────────────────
    ensure_pcon_active()

    print(f"\n  ✅ SchrittPcon0 abgeschlossen.")

def schritt_pcon(spalten_nummer):
    """
    SchrittPcon – Wird für JEDE weitere Spalte wiederholt.
    Fährt den nächsten Spaltenpunkt an und führt MR Config Sequenz aus.
    """
    print(f"\n{'='*55}")
    print(f"  🔁 SchrittPcon – Spalte {spalten_nummer}")
    print(f"{'='*55}")

    # 1. pCon aktivieren
    ensure_pcon_active()

    # 2. Nächsten Spaltenpunkt anfahren
    print(f"\n  📌 Spaltenpunkt {spalten_nummer} anfahren...")
    if not find_and_click(
        "schrittpcon.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_pcon_step"],
        description=f"Spaltenpunkt {spalten_nummer}"
    ):
        sys.exit(1)

    # Mindestlaufzeit vor Fensterwechsel
    time.sleep(CONFIG["min_wait_pcon_step"])

    # 3. Zu MR Config wechseln
    ensure_mrconfig_active()

    # 4. MR Config Sequenz ausführen
    mrconfig_sequence()

    # 5. Zurück zu pCon
    ensure_pcon_active()

    print(f"\n  ✅ SchrittPcon für Spalte {spalten_nummer} abgeschlossen.")

def schritt_pcon_abschluss():
    """
    SchrittPconAbschluss – Wird NUR EINMAL ganz am Ende ausgeführt.
    Wiederholt einen letzten pCon-Schritt nach der finalen MR Config Sequenz.
    """
    print(f"\n{'='*55}")
    print(f"  🏁 SchrittPconAbschluss – Letzter pCon-Schritt")
    print(f"{'='*55}")

    # 1. pCon aktivieren
    ensure_pcon_active()

    # 2. Letzten pCon-Schritt ausführen
    print("\n  📌 Letzten pCon-Schritt ausführen...")
    if not find_and_click(
        "schrittpcon.png",
        timeout=CONFIG["max_wait_pcon_step"],
        min_wait=CONFIG["min_wait_pcon_step"],
        description="Letzter pCon-Schritt (Abschluss)"
    ):
        sys.exit(1)

    # Mindestlaufzeit nach letztem Schritt
    time.sleep(CONFIG["min_wait_pcon_step"])

    print(f"\n  ✅ Abschlussschritt in pCon erfolgreich ausgeführt.")

# ============================================================
# CHECKLISTE ABFRAGEN
# ============================================================

def run_checklist():
    """
    Fragt die Ausgangsbedingungen ab.
    Gibt erst frei wenn alle Punkte bestätigt wurden.
    Gibt die Anzahl der Spalten zurück.
    """
    print("\n" + "="*55)
    print("   SEIKO DRUCKER AUTOMATISIERUNG – STARTCHECKLISTE")
    print("="*55)
    print("Bitte alle Punkte prüfen und mit 'j' bestätigen.\n")

    for i, item in enumerate(CHECKLIST, start=1):
        while True:
            answer = input(f"  [{i}/{len(CHECKLIST)}] {item} – Bereit? (j/n): ").strip().lower()
            if answer == 'j':
                print(f"  ✅ Bestätigt: {item}\n")
                break
            elif answer == 'n':
                print(f"  ⚠️  Bitte zuerst '{item}' erledigen und dann erneut bestätigen.\n")
            else:
                print("  Bitte 'j' für Ja oder 'n' für Nein eingeben.")

    # Anzahl Spalten abfragen
    while True:
        try:
            anzahl = int(input("\n  Wie viele Spalten sollen verarbeitet werden? "))
            if anzahl > 0:
                print(f"  ✅ Anzahl Spalten: {anzahl}\n")
                break
            else:
                print("  Bitte eine positive Zahl eingeben.")
        except ValueError:
            print("  Bitte eine gültige Zahl eingeben.")

    print("\n✅ Checkliste vollständig – Automatisierung startet!\n")
    return anzahl

# ============================================================
# HAUPTPROGRAMM
# ============================================================

def main():
    # 1. Checkliste abfragen → gibt Anzahl Spalten zurück
    anzahl_spalten = run_checklist()

    # 2. SchrittPcon0 – NUR EINMAL zur Initialisierung
    #    (fährt Spalte 1 bereits an!)
    schritt_pcon0()

    # 3. SchrittPcon – Nur für verbleibende Spalten (ab Spalte 2)
    verbleibende_spalten = anzahl_spalten - 1

    if verbleibende_spalten > 0:
        for spalte in range(2, anzahl_spalten + 1):
            schritt_pcon(spalte)
    else:
        print("\n  ℹ️  Nur 1 Spalte angegeben – SchrittPcon entfällt.")

    # 4. Abschlussschritt – Letzter pCon-Schritt VOR dem Ende
    schritt_pcon_abschluss()

    print("\n" + "="*55)
    print("  🎉 Automatisierung erfolgreich abgeschlossen!")
    print("="*55)

if __name__ == "__main__":
    main()