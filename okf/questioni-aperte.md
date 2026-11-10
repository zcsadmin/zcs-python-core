---
type: Known Issues
title: "Questioni aperte e limiti noti"
description: "Problemi di sicurezza, dipendenze, contatori, rilascio e documenti superati di zcs-python-core, con priorità; incongruenze trovate durante la stesura."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/okf/questioni-aperte.md
tags: [questioni-aperte, sicurezza, dipendenze, rilascio]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-10T17:05:00Z }
sources:
  - { id: tlog, resource: ../app/src/zcs/core/telemetry/logging.py, title: "setup_logging e LokiContextFilter", last_modified: 2026-05-12T08:23:34Z }
  - { id: tel, resource: ../app/src/zcs/core/telemetry/zcs_telemetry.py, title: "ZcsTelemetry", last_modified: 2026-07-23T09:06:44Z }
  - { id: pyproject, resource: ../app/pyproject.toml, title: "Metadati del pacchetto", last_modified: 2025-10-15T08:50:58Z }
  - { id: req, resource: ../app/requirements.txt, title: "Requisiti", last_modified: 2026-07-23T09:06:44Z }
  - { id: readme, resource: ../README.md, title: "README", last_modified: 2025-06-27T08:46:03Z }
  - { id: local, resource: ../docs/LOCAL_DEVELOPMENT.md, title: "Sviluppo locale", last_modified: 2025-06-27T08:46:03Z }
  - { id: publish, resource: ../.github/workflows/publish-tag.yaml, title: "Workflow dei tag", last_modified: 2026-07-23T09:21:16Z }
  - { id: logger, resource: ../app/src/zcs/core/logger/logger.py, title: "Logger", last_modified: 2026-04-03T07:58:22Z }
  - { id: module, resource: ../app/src/zcs/core/session/follia_module.py, title: "FolliaModule", last_modified: 2025-12-04T13:26:01Z }
  - { id: loki, resource: "git grep su origin/main di ml-follia-tesseract, ml-universe e dei consumatori (solo nomi), 2026-11-10", title: "Configurazione di Loki e uso dei contatori" }
  - { id: ingestor, resource: "git grep su origin/main di aip-data-ingestor-webservice e aip-generative-ai-webservice, 2026-11-10", title: "Decodifica del JWT nei middleware dei consumatori" }
  - { id: revisione-gferro, resource: "revisione del bundle, 2026-11-10", title: "Indicazioni di G. Ferro", author: "human:gferro" }
---

# Questioni aperte

Ordine: priorità **alta**, **media**, **bassa**. Per ogni voce: cosa, dove, effetto. Le informazioni "lette" vengono dal codice o dai comandi eseguiti il 10/11/2026; "dedotto" e "da verificare" sono segnati.

## Priorità alta

### 1. Dati personali nei tag Loki

`LokiContextFilter` imposta `auth_tenant_id`, `auth_company_id`, `auth_user_id` e **`auth_user_mail`** come tag dei record inviati a Loki, quando c'è un contesto con `op_code` e un handler Loki attivo (`telemetry/logging.py:28-38`, `:56`, `:72`).[^tlog] L'handler esiste solo se `grafana_loki_url` e `grafana_cloud_api_key` sono valorizzati: **la questione vale solo dove Loki è configurato**.

Lettura del 10/11/2026 (solo nomi, mai valori):[^loki]

| Dove | Cosa risulta |
|---|---|
| ml-follia-tesseract (produzione) | `GRAFANA_LOKI_URL`, `GRAFANA_LOKI_INSTANCE_ID`, `GRAFANA_OTLP_URL`, `GRAFANA_OTLP_INSTANCE_ID` e il segreto `GRAFANA_CLOUD_API_KEY` sono impostati **solo per aip-statistics-webservice** (`apps/05-aip-statistics`). L'indirizzo di Loki ha un valore predefinito non vuoto in `variables.tf`. Nessun'altra app di produzione che usa core imposta queste variabili. |
| ml-universe (develop e staging) | le stesse variabili compaiono solo per aip-mcp-follia (`aipmcpfollia-values.yml`) |
| consumatori (sandbox, locale, CI) | nei file di impostazioni locali e di CI le variabili sono presenti ma vuote; `ALLOY_HOST` è nei valori di sandbox di whatsapp, mcp-follia, mcp-cassiopea e statistics |

- **In produzione, quindi, Loki è configurato per aip-statistics-webservice.** Che il segreto `GRAFANA_CLOUD_API_KEY` sia valorizzato non è verificabile da questi file: da verificare.
- aip-statistics-webservice compila `AuthInfo.user_email` con il claim `user_email` del token, oppure `"NOT-SET"` se manca (`app/src/config/fastapi.py:101`, `:116`). Dedotto: con Loki attivo, l'indirizzo (o `NOT-SET`) va nel tag `auth_user_mail`. Se i token di quel servizio abbiano il claim è da verificare. Gli altri consumatori letti non valorizzano `user_email` (righe commentate nei middleware di ingestor, genai e document manager).
- Dedotto: se la libreria `logging_loki` trasforma i tag in etichette dello stream (non letto, la libreria non è nel repo), ogni utente produce un flusso distinto. Da verificare con chi gestisce Loki; da decidere se `user_email` debba restare.

## Priorità media

### 2. Nota per i consumatori: il JWT è decodificato senza verificare la firma

**Core non decodifica nulla**: `AuthInfo` è un dataclass senza controlli ([sessione](api/sessione.md)). Ciò che contiene lo decide il servizio. Occorrenze lette il 10/11/2026 su `origin/main`:[^ingestor]

| Servizio | Dove | Cosa ne ricava |
|---|---|---|
| aip-data-ingestor-webservice | `app/src/config/api/register_middleware.py:41` | `tenant`, `sub`, `azp`, `custom-data` per il contesto |
| aip-generative-ai-webservice | `app/src/config/api/register_middleware.py:83` | anche `company`, `channel`, `swd_app`, `origin` |
| aip-generative-ai-webservice | `app/src/config/auth/service_token.py:47` | token di servizio appena ottenuto da Keycloak: lo decodifica solo per confrontare tenant, company e dati e scrivere avvisi nel log; non lo usa per decidere |
| aip-statistics-webservice | `app/src/config/fastapi.py:101` | `tenant`, `company`, `sub`, `user_email`, `azp` per il contesto (non richiesto: trovato durante il controllo) |

- Le rotte del gateway `/api/openai/` di genai validano comunque il token con `keycloak_client.get_user_info` (`controller/openai_gateway/auth.py:47`) prima di leggere `AuthInfo`.
- **Da verificare nei bundle dei servizi**: se la firma è verificata a monte (ingress, gateway, Keycloak) e se il servizio è raggiungibile senza passarne. Questa scheda non lo afferma né lo esclude, e non corregge i bundle di quei servizi.

### 3. `counter_add` e `counter_create` sollevano `ValueError` non gestiti

Provato in locale in modalità Alloy: etichette non dichiarate, mancanti o su un contatore senza etichette sollevano `ValueError` da `counter_add` (`zcs_telemetry.py:121`, `:123`); la registrazione doppia dello stesso nome solleva `ValueError` da `counter_create` (`:92`, protetto solo da `ImportError`). Dettaglio in [comportamenti](comportamenti.md). Effetto: una chiamata sbagliata può interrompere la richiesta, se il chiamante non la protegge (dedotto).

**Controllo sui consumatori** (`git grep` su `origin/main`, 10/11/2026):[^loki]

| Consumatore | Chiamate a `counter_create` / `counter_add` | Esito |
|---|---|---|
| aip-whatsapp-service | `config/telemetry/custom_telemetry.py`: tre contatori con etichette (`display_phone_number`, `sender`, `webhook_type`) e due senza | Le etichette passate a `counter_add` sono esattamente quelle dichiarate; i contatori senza etichette sono chiamati senza dati. **Nessun errore trovato.** `setup_custom_telemetry` è chiamata da `api.py:123` e ogni nome è creato una volta nel file letto; il numero di invocazioni a runtime non è verificato |
| aip-generative-ai-webservice, aip-mcp-follia-server, aip-mcp-cassiopea-server, aip-statistics-webservice | nessuna chiamata a `counter_create` o `counter_add` | Non toccati |

Nessun consumatore sbaglia le etichette: priorità media.

### 4. Nove versioni di core in produzione

0.2.0, 0.3.0, 0.4.1, 0.10.1, 0.10.2, 0.11.0, 0.11.1, 0.11.3, 0.11.4 (lettura del 10/11/2026, [consumatori](consumatori.md)). Rischio di rilascio: un fix o un cambio di comportamento (es. `message` sostituito dall'eccezione, contatori, `datasource_ids`) vale solo per i servizi che hanno aggiornato la dipendenza. Servizi con core molto vecchio: aip-audio-service (0.2.0), aip-data-storage-consumer (0.3.0), aip-erp-ai-webservice (0.4.1).

### 5. Il tag `0.11.2` ha meno codice del suo `-rc2`

`0.11.2` punta a `3438808` (stesso commit di `0.11.1`) e non contiene `label_names`, presente in `0.11.2-rc1`, `-rc2` e `0.11.3`. Per i numeri di versione `0.11.2 > 0.11.2-rc2`. Chi fissa `==0.11.2` riceve il comportamento senza il fix. Letto il 10/11/2026: **nessun consumatore lo richiede** e nessun consumatore usa intervalli di versione su core (tutti i requisiti sono `==`). Vedi [versioni](versioni.md).

### 6. Workflow dei tag: identificativo dello step diverso (r.64 contro r.77)

`id: check-prerelease` a r.64 e `steps.check_prerelease` a r.77: i nomi non coincidono.[^publish] Letto: la release `0.11.4` non è marcata pre-release; `0.11.2` e `0.11.3` (versioni finali) lo sono. Dedotto: una rc creata con il workflow attuale non sarebbe marcata pre-release. Dettaglio in [rilascio](operativita/rilascio.md).

### 7. Effetti globali del logger

La factory dei record si sostituisce all'import (`logger.py:9`, `:32`); il costruttore di `ZcsLogging` rimpiazza gli handler dei logger che ne hanno già (`:132-137`); con eccezione allegata il campo `message` del JSON diventa il testo dell'eccezione (`:39-40`).[^logger] Effetti e versioni in [comportamenti](comportamenti.md).

### 8. Rinomina non retrocompatibile senza `!` (0.8.0)

`QaInfo.datasource_id` è diventato `datasource_ids` (lista) nel tag 0.8.0, commit `60b5fae` senza `!`. Un consumatore che costruisce `QaInfo(datasource_id=...)` si rompe all'aggiornamento (letto nel diff). Vedi [versioni](versioni.md).

### 9. zcs-python-stats richiede `zcs-python-core==0.7.2`, che non è un tag

I tag della repo sono `0.7.0`, `0.7.1` e `0.8.0`: `0.7.2` non esiste come tag (letto). Da verificare se è nel registro dei pacchetti (non ho accesso) o se il requisito è errato. Vedi [consumatori](consumatori.md). Da portare nel bundle di zcs-python-stats (AP-5321).

### 10. Consumatori non in produzione e su rc

aip-audio-video-consumer e aip-xml-invoice-consumer hanno il modulo commentato in `main.tf` (r.349-364 e r.326-333) ma le chiavi `avconsumer` e `xmlconsumer` restano in `app_versions`; il tag 1.4.3 di audio-video richiede core 0.2.0 e il suo `main` 0.11.1, il tag 1.8.0 di xml-invoice richiede 0.2.0. aip-follia-voip richiede `0.11.0-rc1` (una rc) e non è in `app_versions`.[^revisione-gferro]

## Priorità bassa

### 11. Dipendenze non dichiarate

- `pyproject.toml` non ha `dependencies`;[^pyproject] `requirements.txt` elenca `pydantic_settings` e `prometheus_client` ma non è letto da chi installa il pacchetto.[^req] Stessa situazione descritta per zcs-python-genai.
- `logging_loki` è importato dentro `setup_logging` solo se `has_loki_config`, a `telemetry/logging.py:57`, **senza `try`**: se la libreria manca e Loki è configurato, `setup_logging` solleva `ImportError`. Gli altri import opzionali (OpenTelemetry, `prometheus_client`) sono protetti.
- `zcs.core.telemetry` richiede `pydantic_settings` anche se la telemetria non si usa, perché `TelemetrySettings` è importata e istanziata all'import.
- Effetto: ogni servizio deve aggiungere da sé `pydantic_settings`, `opentelemetry-*`, `logging_loki`, `prometheus_client`; una versione di core non indica cosa serve.

### 12. README superato (ultimo commit 27/06/2025)

Letto il 10/11/2026, confrontato con il codice del 23/07/2026:[^readme]

| Frase del README | Cosa dice il codice |
|---|---|
| "The library doesn't require directly third party dependencies. This will let you install only the requirements needed by the utils you will effectively use." | Vero per `session`, `exception`, `logger`; non più per la telemetria (dal tag 0.11.0): `pydantic_settings` all'import, OpenTelemetry e `prometheus_client` per le funzioni |
| Esempi d'uso: solo `ZcsException` e `ZcsLogging` | Mancano `RequestState`, `request_context`, `AuthInfo`, `FolliaModule`, `QaInfo` (dal tag 0.4.0) e `ZcsTelemetry`, `setup_logging`, `set_trace_attributes` (0.11.0) |
| Nessun cenno ai campi di `RequestState` | `channel` (0.11.1), `attempts` (0.10.0), `custom_data` (0.10.1), `job_id`/`file_id` (0.9.0), `size`/`total_pages` (0.8.0), `doc_type` (0.7.1), `qa_info` (0.7.0) non compaiono |

`docs/LOCAL_DEVELOPMENT.md` (stessa data) descrive `./run.sh -t` e `-i`, che esistono ancora in `run.sh`: nessuna frase superata.[^local]

### 13. Altre incongruenze di nome e tipo (da verificare)

- `delta_ns` e `total_ns` sono in secondi (`logger.py:68-69`).
- `log_level` annotato `str`, valore predefinito intero (`logger.py:117`).
- `FolliaModule` ha la docstring "Data class" ma è una `StrEnum` (`follia_module.py:4-8`).[^module]
- `EndpointFilter` usa una lista mutabile come valore predefinito (`endpoint_filter.py:11`).
- `alloy_metrics_port` e `_build_alloy_metrics_endpoint` non sono usati ([configurazione](operativita/configurazione.md)).

### 14. Copertura dei test

Tre file di test (76 righe totali, `app/tests/zcs/core/`): impostazioni e contatori della telemetria (3 test), una `ZcsException`, e un test del logger che si limita a creare `ZcsLogging`. Nessun test per `RequestState`, `request_context`, i formatter, `EndpointFilter` o `setup_logging` (letto).

## Incongruenze trovate durante la stesura (da verificare)

Nessuna correzione al codice o ai documenti è stata fatta da questo bundle. Le voci 2, 9, 11, 12 e 13 riguardano la repo di core o i bundle dei consumatori e vanno decise da una persona (correzioni in rami separati).

[^loki]: Lettura su `origin/main` del 10/11/2026; nei file sono stati guardati solo i nomi delle variabili.
[^ingestor]: Lettura su `origin/main` del 10/11/2026.
[^tlog]: `telemetry/logging.py`.
[^pyproject]: `pyproject.toml`.
[^req]: `requirements.txt`.
[^publish]: `publish-tag.yaml` r.64 e r.77.
[^logger]: `logger.py`.
[^readme]: `README.md`.
[^local]: `docs/LOCAL_DEVELOPMENT.md`.
[^module]: `follia_module.py`.
[^revisione-gferro]: Indicazione di G. Ferro del 10/11/2026.
