---
type: Library
title: "zcs-python-core: panoramica"
description: "Libreria Python di base per i servizi Follia: contesto della richiesta, logger, eccezioni e telemetria; come si installa, dove si pubblica e cosa non dichiara."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/README.md
tags: [libreria, python, core, contesto-richiesta, logger, telemetria]
esposizione: libreria
generated: { by: claude-code/claude-sonnet-5-5 }
sources:
  - { id: readme, resource: ../README.md, title: "README della repo", last_modified: 2025-06-27T08:46:03Z }
  - { id: pyproject, resource: ../app/pyproject.toml, title: "Metadati del pacchetto", last_modified: 2025-10-15T08:50:58Z }
  - { id: req, resource: ../app/requirements.txt, title: "Requisiti di sviluppo e dipendenze usate", last_modified: 2026-07-23T09:06:44Z }
  - { id: publish, resource: ../.github/workflows/publish-tag.yaml, title: "Pubblicazione del pacchetto sul tag", last_modified: 2026-07-23T09:21:16Z }
  - { id: telemetria, resource: ../app/src/zcs/core/telemetry/zcs_telemetry.py, title: "ZcsTelemetry", last_modified: 2026-07-23T09:06:44Z }
---

# zcs-python-core

`zcs-python-core` è la libreria Python di base dei servizi Follia. Non gira da sola: i servizi la importano (`zcs.core.*`) per quattro cose.

| Cosa offre | Modulo | Scheda |
|---|---|---|
| Contesto della richiesta (`RequestState`, `request_context`, `AuthInfo`, `QaInfo`, `FolliaModule`) | `zcs.core.session` | [sessione](api/sessione.md) |
| Logger con formato JSON per Cloud Logging o formato console, filtro per gli endpoint di servizio | `zcs.core.logger` | [logger](api/logger.md) |
| Eccezione applicativa `ZcsException` | `zcs.core.exception` | [eccezioni](api/eccezioni.md) |
| Telemetria (tracce, metriche, log verso Grafana o Alloy) | `zcs.core.telemetry`, `zcs.core.settings` | [telemetria](api/telemetria.md) |

Il bundle descrive la libreria **vista da chi la usa**. I servizi che la importano sono elencati in [consumatori](consumatori.md), ma come sono fatti dentro sta nei loro bundle.

## Esposizione

`esposizione: libreria`. Non ha API per i clienti né guida in `docs/integrazione.md`. L'ha scelta chi verifica insieme alla struttura del bundle (conferma in chat del 10/11/2026).

## Installazione

- Il pacchetto si chiama `zcs-python-core` e si pubblica su Artifact Registry (`python`, europe-west1, progetto `ai-accounting-405809`) quando si spinge un tag.[^publish]
- Nel `requirements.txt` del consumatore serve la riga `--extra-index-url https://europe-west1-python.pkg.dev/ai-accounting-405809/python/simple/` e poi `zcs-python-core==<versione>`.[^readme]
- Il formato dei tag è `X.Y.Z` senza `v`, con rc `X.Y.Z-rcN`. Il workflow scrive il nome del tag nel campo `version` di `pyproject.toml` (che nel repo resta `0.dev0`) prima di costruire la wheel.[^publish][^pyproject]

## Dipendenze

- `pyproject.toml` non ha la sezione `dependencies`: installare il pacchetto **non porta nessuna libreria di terze parti**.[^pyproject]
- `app/requirements.txt` elenca `build`, `pytest`, `pydantic_settings` e `prometheus_client`, ma è il file dell'immagine di sviluppo e di prova, non è letto da chi installa il pacchetto.[^req]
- Cosa serve a chi usa ogni modulo:

| Modulo | Serve al consumatore | Come si vede nel codice |
|---|---|---|
| `session`, `exception`, `logger` | niente di terzo | usano solo la libreria standard |
| `settings`, `telemetry` | `pydantic_settings` | `TelemetrySettings` è importata e istanziata all'import |
| `telemetry` (metriche, tracce, log OTLP) | pacchetti `opentelemetry-*` | importati solo dentro `ZcsTelemetry`, con `except ImportError` che disattiva la telemetria e scrive un avviso[^telemetria] |
| `telemetry` (contatori in modalità Alloy) | `prometheus_client` | import protetto da `except ImportError` |
| `telemetry.setup_logging` con Loki | `logging_loki` | **import non protetto**, vedi [questioni aperte](questioni-aperte.md) |

Il README dice che la libreria "non richiede direttamente dipendenze di terze parti": è vero per `session`, `exception` e `logger`, non per la telemetria (vedi [questioni aperte](questioni-aperte.md)).

## Dove guardare

| Cerchi | Vai a |
|---|---|
| Come si imposta e si legge il contesto della richiesta | [flusso del contesto](flussi/ciclo-di-vita-contesto-richiesta.md), [sessione](api/sessione.md) |
| Cosa succede in errore, con contesto assente, valori predefiniti | [comportamenti](comportamenti.md) |
| Chi la usa e con quale versione | [consumatori](consumatori.md) |
| Cosa è cambiato in ogni tag | [versioni](versioni.md) |
| Variabili d'ambiente | [configurazione](operativita/configurazione.md) |
| Come si pubblica e si prova | [rilascio](operativita/rilascio.md) |
| Problemi noti | [questioni aperte](questioni-aperte.md) |

[^publish]: Workflow `publish-tag.yaml`: carica la wheel con `twine` su Artifact Registry.
[^readme]: README, sezione "Usage".
[^pyproject]: `pyproject.toml`: nome, `version = "0.dev0"` e nessuna sezione `dependencies`.
[^telemetria]: `ZcsTelemetry._import_telemetry_modules` (r.258-271): in caso di `ImportError` torna `None` e la telemetria non si inizializza.
