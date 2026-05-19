from datetime import timezone

from core.settings import LOCAL_TZ
from core.astronomy import CLOSE_APPROACH_LIMIT_DEG, group_best


def utc_to_local(dt):
    return dt.replace(tzinfo=timezone.utc).astimezone(LOCAL_TZ)


def event_title(event):
    satellite_emoji = event.get("satellite_emoji", "🚀")
    satellite_name = event.get("satellite_name", "ISS")

    return (
        f"{satellite_emoji} {satellite_name} → "
        f"{event['emoji']} {event['name']}"
    )


def build_stats_text(stats):
    text = "📋 Corpi controllati:\n"

    for name, s in stats.items():
        text += f"{s['emoji']} {name}: "

        parts = []

        if s["transits"] > 0:
            parts.append(f"{s['transits']} transito/i")
        else:
            parts.append("nessun transito")

        if s["close_enabled"]:
            if s["close_approaches"] > 0:
                parts.append(
                    f"{s['close_approaches']} avvicinamento/i "
                    f"entro {CLOSE_APPROACH_LIMIT_DEG}°"
                )
            else:
                parts.append(
                    f"nessun avvicinamento entro {CLOSE_APPROACH_LIMIT_DEG}°"
                )

        text += ", ".join(parts) + "\n"

    return text


def build_diagnostics_text(diagnostics):
    if diagnostics["fine_used"]:
        mode = (
            f"scansione veloce {diagnostics['coarse_step_km']} km "
            f"+ rifinitura locale {diagnostics['fine_step_km']} km"
        )
    else:
        mode = f"scansione veloce {diagnostics['coarse_step_km']} km"

    satellites_text = "\n".join(
        f"- {name}" for name in diagnostics.get("satellites_checked", [])
    )
    
    return (
        "🧪 Diagnostica ricerca:\n"
        f"Modalità: {mode}\n"
        f"Punti griglia grossolana: {diagnostics['coarse_grid_points']}\n"
        f"Candidati grossolani: {diagnostics['coarse_hits']}\n"
        f"Centri rifiniti: {diagnostics['fine_centers']}\n\n"
        "🛰 Satelliti controllati:\n"
        f"{satellites_text}\n"
    )


def build_message(settings, transits, close_approaches, stats, diagnostics):
    grouped_transits = group_best(transits, 60)
    grouped_close = group_best(close_approaches, 180)

    text = "🚀 Transit Bot\n\n"
    text += "Controllo giornaliero completato ✅\n\n"

    if not grouped_transits:
        text += (
            "Nessun transito davanti a Sole, Luna, Giove o Saturno "
            f"entro {settings['radius_km']} km "
            f"nelle prossime {settings['search_hours']} ore.\n\n"
        )
    else:
        text += "🔹 Transiti trovati:\n"

        for i, e in enumerate(grouped_transits, 1):
            local_time = utc_to_local(e["time"])
            start_local = utc_to_local(e["start_time"])
            end_local = utc_to_local(e["end_time"])

            maps_url = (
                f"https://www.google.com/maps?q="
                f"{e['lat']:.6f},{e['lon']:.6f}"
            )

            text += (
                f"\n{i}. {event_title(e)}\n"
                f"Tipo: {e['type']}\n"
                f"Data/ora migliore: "
                f"{local_time.strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Inizio: {start_local.strftime('%H:%M:%S')}\n"
                f"Fine: {end_local.strftime('%H:%M:%S')}\n"
                f"Durata: {e['duration_seconds']:.1f} s\n"
                f"Percorso: {e['path_description']}\n"
                f"Entrata disco: {e['entry_pos']:.2f} r\n"
                f"Massimo avvicinamento: {e['closest_pos']:.2f} r\n"
                f"Uscita disco: {e['exit_pos']:.2f} r\n"
                f"Distanza dal centro: {e['dist_km']:.1f} km\n"
                f"Separazione: {e['sep']:.4f}°\n"
                f"Alt satellite: {e['iss_alt']:.1f}°\n"
                f"Alt {e['name']}: {e['body_alt']:.1f}°\n"
                f"Mappa evento: {maps_url}\n"
            )

        text += "\n"

    text += build_stats_text(stats)

    if grouped_close:
        text += "\n🔭 Avvicinamenti interessanti:\n"

        for i, e in enumerate(grouped_close[:5], 1):
            local_time = utc_to_local(e["time"])

            maps_url = (
                f"https://www.google.com/maps?q="
                f"{e['lat']:.6f},{e['lon']:.6f}"
            )

            text += (
                f"\n{i}. {event_title(e)}\n"
                f"Data/ora: "
                f"{local_time.strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Separazione: {e['sep']:.4f}°\n"
                f"Distanza dal centro: {e['dist_km']:.1f} km\n"
                f"Alt satellite: {e['iss_alt']:.1f}°\n"
                f"Alt {e['name']}: {e['body_alt']:.1f}°\n"
                f"Mappa evento: {maps_url}\n"
            )

    text += "\n" + build_diagnostics_text(diagnostics)

    text += (
        "\n📍 Posizione centrale:\n"
        f"Lat: {settings['lat']:.6f}\n"
        f"Lon: {settings['lon']:.6f}\n"
        f"Raggio ricerca: {settings['radius_km']} km\n"
        f"Finestra ricerca: {settings['search_hours']} ore"
    )

    return text
