# AGENTS.md — zcs-python-core

> Prima versione scritta da `setup-repo` il 2026-11-17, non ancora controllata da chi conosce il servizio:
> `/pre-pr` propone di correggerla quando sbaglia. Chi la controlla toglie questa riga.

Libreria Python di base dei servizi Follia (pacchetto `zcs-python-core`, moduli `zcs.core.*`): contesto della
richiesta, logger, `ZcsException`, telemetria. Non gira da sola e non ha deploy: la importano una quindicina di
servizi in produzione e altre librerie `zcs-python-*`, ognuno con la propria versione fissata (`==`). Dettagli in
`okf/index.md`; chi la usa e con quale versione in `okf/consumatori.md`.

## Come si lavora

- Test: `./run.sh -t` (serve Docker; costruisce l'immagine `dev`, installa `app/requirements.txt`, fa
  `python -m build`, installa la libreria in modalità editabile e lancia `pytest`).
- `./run.sh -i`: costruisce l'immagine `dist` e lancia `pytest` dentro, come fa la CI sulle PR verso `main`.
- `./run.sh -s`: shell nel container; `-v` verbose, `-h` aiuto.
- Le immagini partono da `zcscompany/python:3.13-dev` e `-dist` (`.build/dockerfiles/Dockerfile`).
- Repo senza `sandbox`: si lavora su branch da `main` e la PR va solo verso `main`.
- Rilascio: un tag (`X.Y.Z`, rc `X.Y.Z-rcN`, senza `v`) lancia `publish-tag.yaml`, che scrive la versione in
  `app/pyproject.toml` (nel repo resta `0.dev0`) e carica la wheel su Artifact Registry. Ogni tag pubblica, anche
  le rc. Un push su `main` non lancia nulla. Vedi `okf/operativita/rilascio.md` e la skill `tagga`.

## Dove stanno le cose

- `app/src/zcs/core/session/`: `RequestState`, `request_context`, `AuthInfo`, `QaInfo`, `FolliaModule`
  (`okf/api/sessione.md`, `okf/flussi/ciclo-di-vita-contesto-richiesta.md`).
- `app/src/zcs/core/logger/`: `ZcsLogging`, formatter JSON e console, `EndpointFilter` (`okf/api/logger.md`).
- `app/src/zcs/core/exception/`: `ZcsException` (`okf/api/eccezioni.md`).
- `app/src/zcs/core/telemetry/` e `settings/`: `ZcsTelemetry`, `setup_logging`, `set_trace_attributes`,
  `TelemetrySettings` (`okf/api/telemetria.md`, `okf/operativita/configurazione.md`).
- `app/tests/zcs/core/`: test (`pytest`), pochi: vedi `okf/questioni-aperte.md` §14.
- `app/requirements.txt`: dipendenze dell'immagine di sviluppo e prova, **non** del pacchetto installato.

## Attenzione

- Ogni modifica tocca tutti i consumatori che aggiornano la versione: firme pubbliche, nomi dei campi di
  `RequestState`/`AuthInfo`/`QaInfo` e formato JSON del logger sono un contratto. Un cambio non retrocompatibile
  vuole `!` nel commit (precedente: `datasource_id` → `datasource_ids` in 0.8.0 senza `!`, `okf/versioni.md`).
- `pyproject.toml` non dichiara `dependencies`: chi installa la libreria non riceve niente di terzo. Un import
  nuovo di una libreria esterna va protetto (`try/except ImportError`) o reso noto ai consumatori
  (`okf/libreria.md`, sezione Dipendenze).
- Effetti all'import: `zcs.core.logger` sostituisce la `LogRecordFactory` del processo, `zcs.core.settings` legge
  ambiente e `settings/telemetry-settings.env` all'import (`okf/comportamenti.md`).
- `LokiContextFilter` manda a Loki anche `auth_user_mail`: non aggiungere altri dati personali ai tag
  (`okf/questioni-aperte.md` §1).
- `counter_add`/`counter_create` possono sollevare `ValueError` verso il chiamante (`okf/comportamenti.md`).
- Il workflow dei tag ha un id di step sbagliato (`check-prerelease` contro `check_prerelease`): le rc non risultano
  pre-release su GitHub (`okf/questioni-aperte.md` §6).
- Le schede `okf/` si aggiornano nella stessa PR del codice (es. un campo nuovo di `RequestState` va in
  `okf/api/sessione.md` e `okf/versioni.md`).
