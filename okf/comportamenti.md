---
type: Behaviors
title: "Comportamenti da conoscere"
description: "Cosa succede davvero quando un servizio usa la libreria: contesto assente, effetti globali del logger, errori dei contatori, campi inviati a Loki, importazioni con effetti."
resource: https://github.com/zcsadmin/zcs-python-core/tree/main/app/src/zcs/core
tags: [comportamenti, logger, contatori, loki, contesto]
generated: { by: claude-code/claude-sonnet-5-5 }
sources:
  - { id: logger, resource: ../app/src/zcs/core/logger/logger.py, title: "Logger e formatter", last_modified: 2026-04-03T07:58:22Z }
  - { id: tel, resource: ../app/src/zcs/core/telemetry/zcs_telemetry.py, title: "ZcsTelemetry", last_modified: 2026-07-23T09:06:44Z }
  - { id: tlog, resource: ../app/src/zcs/core/telemetry/logging.py, title: "setup_logging e LokiContextFilter", last_modified: 2026-05-12T08:23:34Z }
  - { id: sett, resource: ../app/src/zcs/core/settings/telemetry_settings.py, title: "TelemetrySettings", last_modified: 2026-05-12T08:23:34Z }
  - { id: ctx, resource: ../app/src/zcs/core/session/request_context.py, title: "request_context", last_modified: 2025-10-15T08:50:58Z }
  - { id: prova, resource: "prova locale in un ambiente temporaneo, 2026-11-10 (prometheus_client 0.25.0)", title: "Prova dei contatori in modalità Alloy, senza modificare la repo" }
---

# Comportamenti da conoscere

Per ogni voce: dove sta nel codice, da quale versione e chi ne è toccato. Le voci con "prova" sono state provate in locale; quelle con "dedotto" no.

## Contesto della richiesta

### Contesto assente

`request_context` ha `default=None`: fuori dal middleware, o nelle rotte che il middleware salta, `request_context.get()` restituisce `None`.[^ctx]

| Chi legge | Cosa succede con `None` |
|---|---|
| Logger (JSON e console), `LokiContextFilter`, `set_trace_attributes` | gestiscono `None`: omettono i campi del contesto |
| Codice dei servizi che scrive `request_context.get().getAuthInfo()` | `AttributeError`. Caso letto: aip-generative-ai-webservice, `controller/openai_gateway/auth.py:59`. In quella rotta il contesto è sempre impostato: il middleware lo imposta a r.61 per ogni richiesta tranne quelle il cui URL finisce con `/health` o il cui percorso è `/metrics` (`config/api/register_middleware.py:51`), e le rotte `/api/openai/` non sono tra queste. Prima, a r.47, il token è validato con `keycloak_client.get_user_info`. Da verificare: che la rotta non sia mai chiamata fuori dalla richiesta HTTP. |

Da quale versione: `request_context` dal tag 0.4.0. Servizi toccati: tutti quelli di [consumatori](consumatori.md) che leggono il contesto.

### Thread e contesto

Un thread creato da un consumer parte con un contesto vuoto, salvo copia esplicita del contesto: è il comportamento standard di `contextvars` (dedotto). Nei consumer che usano thread non è stato verificato (da verificare).

### Il logger aggiorna il checkpoint

A ogni riga di log con contesto presente, il logger chiama `setCheckpointNs` (`logger.py:65`, `logger.py:108`): il tempo "delta" è sempre relativo all'ultimo log, di qualunque componente.[^logger] Il contesto è modificato da chi scrive il log, non solo letto.

## Logger (`ZcsLogging`)

| Comportamento | Dove | Da quale tag | Note |
|---|---|---|---|
| **La `LogRecordFactory` si sostituisce all'import** del modulo `zcs.core.logger`: `logging.setLogRecordFactory(record_factory)` a livello di modulo | `logger.py:9`, `logger.py:32` | 0.2.0 | Vale per tutti i logger del processo, anche senza creare `ZcsLogging`. La factory aggiunge `error_code` e `original_exception` a ogni record. |
| **Il costruttore sostituisce i gestori degli altri logger**: per ogni logger già registrato imposta il livello e, se ha già almeno un handler, lo rimpiazza con quello nuovo | `logger.py:132-137` | da verificare | I logger senza handler restano senza. Va creato dopo che gli altri hanno configurato i propri. |
| `logging.basicConfig(level, handlers=[...])` sul root | `logger.py:146-149` | da verificare | Non ha effetto se il root ha già degli handler (comportamento standard di `basicConfig`, dedotto). |
| **`delta_ns` e `total_ns` sono in secondi**, non in nanosecondi: il valore è diviso per `1e9` | `logger.py:68-69` (JSON) | 0.4.0 | Il nome è fuorviante. Nel formato console i tempi sono "s" (`logger.py:109-110`). |
| **Con un'eccezione allegata, `message` diventa il testo dell'eccezione**, non il messaggio del log | `logger.py:39-40` | 0.2.0 | Succede se `exc_info` è presente e il record contiene un'eccezione. Il messaggio originale non compare nel JSON; resta il testo dell'eccezione e il traceback. |
| **`ConsoleCustomFormatter.format` modifica `record.msg`**: ci aggiunge il prefisso `[OP_CODE:..][REQ_ID:..]` e il suffisso dei tempi | `logger.py:109-110` | 0.4.0 | Il record modificato è lo stesso passato agli altri handler: con più handler sullo stesso record il prefisso si ripete (dedotto). |
| Il tipo di `log_level` è annotato `str` ma il valore predefinito è `logging.INFO` (intero) | `logger.py:117` | da verificare | Il codice usa il valore così com'è, quindi accetta sia interi sia nomi dei livelli. |
| `EndpointFilter` ha come predefinito una lista mutabile e cerca `GET <endpoint>` nel messaggio | `endpoint_filter.py:11`, `endpoint_filter.py:23` | 0.3.0 | Non filtra metodi diversi da GET. |

## Contatori (`ZcsTelemetry`)

Provati in locale con `prometheus_client` 0.25.0 (la versione di `requirements.txt`), modalità solo Alloy (nessun meter OTLP), senza modificare la repo.[^prova]

`counter_add` non ha nessun `try/except` (`zcs_telemetry.py:96-123`): il ramo Prometheus chiama `labels(**attributes).inc(amount)` (r.121) o `inc(amount)` (r.123) e ogni errore sale al chiamante.[^tel]

| Chiamata | Esito |
|---|---|
| etichette dichiarate in `counter_create`, tutte presenti | nessuna eccezione |
| etichetta **non dichiarata** (`{"b": ...}` su un contatore con `["a"]`) | `ValueError: Incorrect label names` |
| contatore con etichette, `counter_add(nome)` senza dati (o con `{}`) | `ValueError: counter metric is missing label values` |
| contatore **senza** etichette, `counter_add(nome, {"a": ...})` | `ValueError: No label names were set when constructing counter` |
| contatore senza etichette, senza dati | nessuna eccezione |
| `{"value": 3, "a": "y"}` | nessuna eccezione: `value` è la quantità, il resto sono etichette |

- Se sono attivi **anche** i meter OTLP, il ramo OTLP incrementa prima (r.112-113): quando il ramo Prometheus fallisce, l'incremento OTLP è già avvenuto.
- Con **solo OTLP** non ci sono contatori Prometheus e le etichette non dichiarate non sollevano errori.
- **Registrazione doppia**: `counter_create` con lo stesso nome una seconda volta, sulla stessa istanza o su un'altra, solleva `ValueError: Duplicated timeseries in CollectorRegistry` (provato). Il costruttore del contatore Prometheus (r.92) è protetto solo da `except ImportError`. Anche `a.b` e `a-b` collidono, perché diventano `a_b` (r.91). Con solo OTLP non si verifica.
- `counter_create` non fa nulla, con un avviso, se la telemetria non è attiva o se non c'è nessun meter e nemmeno Alloy (r.75-82); `counter_add` su un contatore mai creato avvisa e ritorna (r.114-116).

Da quale versione: `label_names` dal tag 0.11.3, vedi [versioni](versioni.md). Servizi toccati: aip-whatsapp-service (contatori con etichette, 0.11.3); letto il 10/11/2026: le etichette che passa coincidono con quelle dichiarate. Gli altri consumatori della telemetria non chiamano `counter_create` né `counter_add` ([questioni aperte](questioni-aperte.md)).

## Telemetria e Loki

- L'inizializzazione non solleva eccezioni se manca la configurazione o mancano i pacchetti: scrive un avviso e `is_telemetry_enabled()` resta `False` (`zcs_telemetry.py:132`, `:258-271`). Un servizio può quindi partire senza telemetria senza accorgersene, salvo leggere i log.
- **Campi inviati a Loki.** `LokiContextFilter` è aggiunto solo all'handler Loki, che esiste solo con `grafana_loki_url` e `grafana_cloud_api_key` valorizzati (`telemetry/logging.py:56`, `:72`).[^tlog] Se nel contesto c'è un `RequestState` con `op_code`, il filtro imposta i tag dinamici `request_op_code`, `request_request_id`, `request_follia_module`, `auth_client_id`, `auth_tenant_id`, `auth_company_id`, `auth_user_id` e **`auth_user_mail`** (r.28-38); i campi di `AuthInfo` sono `None` se `AuthInfo` non è impostata. Se c'è uno span valido, aggiunge `trace_id` e `span_id` (r.41-46).
- Il filtro non rimuove nulla: se `user_email` è valorizzato in `AuthInfo`, finisce nei tag. Se i tag diventino etichette dello stream di Loki dipende dalla libreria `logging_loki`, che non è nel repo (da verificare). Vedi [questioni aperte](questioni-aperte.md).

## Importazioni con effetti

- `zcs.core.settings.telemetry_settings` crea `telemetry_settings = TelemetrySettings()` all'import (r.36): chi importa `zcs.core.telemetry` o `ZcsTelemetry` legge subito le variabili d'ambiente e il file `settings/telemetry-settings.env`.[^sett]
- `zcs.core.logger` sostituisce la factory dei record (vedi sopra).

## Rischio di rilascio: tante versioni diverse in produzione

I servizi in produzione usano **nove** versioni diverse di core, da 0.2.0 a 0.11.4 (lettura del 10/11/2026, vedi [consumatori](consumatori.md)). Un fix della libreria non raggiunge un servizio finché quel servizio non cambia la dipendenza e viene rilasciato; ciò che vale in una sezione di questa scheda dipende dalla versione richiesta dal servizio. Per ogni tag, cosa contiene: [versioni](versioni.md).

[^ctx]: `request_context.py` r.3.
[^logger]: `logger.py`.
[^tel]: `zcs_telemetry.py`.
[^tlog]: `telemetry/logging.py`.
[^sett]: `telemetry_settings.py` r.4-36.
[^prova]: Script temporaneo, eseguito fuori dalla repo. Esito riportato nella tabella.
