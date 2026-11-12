---
type: Consumers
title: "Chi usa zcs-python-core"
description: "Servizi e librerie che dipendono da zcs-python-core: versione richiesta su main, versione richiesta al tag in produzione, versione del servizio in app_versions e moduli importati."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/okf/consumatori.md
tags: [consumatori, versioni, produzione, app-versions]
status: stable
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-12T14:16:38Z }
verified: { by: human:gferro, at: 2026-11-12T14:47:05Z }
sources:
  - { id: lettura, resource: "git grep su origin/main di tutte le repo di Follia_SW e git show dai tag, 2026-11-10", title: "Lettura delle dipendenze dei consumatori" }
  - { id: tfvars, resource: "app/follia.ai/terraform/terraform.tfvars di ml-follia-tesseract (origin/main 30bdc2f, file modificato il 2026-11-05)", title: "Mappa app_versions, letta il 2026-11-10" }
  - { id: maintf, resource: "app/follia.ai/terraform/40_aiplatform/main.tf di ml-follia-tesseract, righe 326-333 e 349-364", title: "Modulo aip-avconsumer commentato" }
  - { id: revisione-gferro, resource: "revisione del bundle, 2026-11-10", title: "Indicazioni di G. Ferro", author: "human:gferro" }
  - { id: agentsind, resource: "zcs-python-genai, tag 1.4.0: git grep zcs.service.storage / zcs.core.logger / document_manager.models in app/src e app/pyproject.toml senza dependencies; zcs-python-agents, origin/main e tag 0.1.0 e 0.1.1: nessun import zcs.core, zcs.service o zcs.python.ms in app/ e tests/ (letto il 12/11/2026)", title: "Uso indiretto da zcs-python-agents tramite zcs-python-genai 1.4.0" }
---

# Chi usa zcs-python-core

Lettura del **10/11/2026**: `git grep` su `origin/main` di ogni repo di `Follia_SW`, repo per repo; versioni al tag con `git show <tag>`; mappa `app_versions` da `terraform.tfvars` di ml-follia-tesseract (`origin/main` al commit `30bdc2f`, file modificato per l'ultima volta il 05/11/2026).[^lettura][^tfvars] Le colonne "core su main" e "core al tag" sono la riga `zcs-python-core==...` nei requisiti del consumatore.

## Servizi in produzione

| Repo | Chiave in `app_versions` | Tag in prod | core su main | core al tag in prod | Cosa importa |
|---|---|---|---|---|---|
| aip-generative-ai-webservice | `genai` | 6.10.2 | 0.11.0 | 0.11.0 | session (`request_context` ovunque, `RequestState`, `AuthInfo`, `FolliaModule`, `QaInfo`), logger (`ZcsLogging`, `EndpointFilter`), `ZcsException`, `ZcsTelemetry` |
| aip-document-manager-webservice | `docmanager` | 2.16.3 | 0.11.4 | 0.11.4 | session (`request_context`, `RequestState`, `AuthInfo`, `FolliaModule`), `ZcsLogging`, `ZcsException` |
| aip-whatsapp-service | `whatsapp` | 0.9.3 | 0.11.3 | 0.11.3 | session, `ZcsLogging`, `ZcsException`, telemetria (`setup_logging`, `set_trace_attributes`, `ZcsTelemetry`, contatori con `label_names`) |
| aip-statistics-webservice | `statistics` | 0.10.0 | 0.11.0 | 0.11.0 | session, `FolliaModule`, `ZcsLogging`, `EndpointFilter`, `ZcsException`, telemetria |
| aip-data-ingestor-webservice | `ingestor` | 3.2.2 | 0.11.1 | 0.11.1 | session, `ZcsLogging`, `EndpointFilter`, `ZcsException` |
| aip-data-extraction-consumer | `dextraction` | 3.0.0 | 0.11.1 | 0.11.1 | session, `ZcsLogging`, `ZcsException` |
| aip-document-assistance-consumer | `docassistance` | 2.3.0 | 0.11.1 | 0.11.1 | session, `ZcsLogging`, `EndpointFilter`, `ZcsException` |
| aip-mcp-follia-server | `mcp_follia` | 0.2.0 | 0.11.0 | 0.11.0 | session, `ZcsLogging`, `EndpointFilter`, `ZcsException`, telemetria (`setup_logging`, `ZcsTelemetry`) |
| aip-mcp-cassiopea-server | `mcp_cassiopea` | 0.1.0 | 0.11.0 | 0.11.0 | session, `ZcsLogging`, `EndpointFilter`, telemetria (`setup_logging`, `ZcsTelemetry`) |
| aip-mcp-teseo-server | `mcp_teseo` | 0.13.0 | 0.10.1 | 0.10.1 | session, `ZcsLogging`, `EndpointFilter`, `ZcsException` |
| aip-file-storage-service | `file_storage` | 2.4.0 | 0.10.1 | 0.10.1 | session (`request_context`, `RequestState`, `AuthInfo`), `ZcsLogging`, `ZcsException` |
| aip-data-scraper-consumer | `scraper` | 2.2.1 | 0.10.2 | 0.10.2 | `ZcsLogging`, `ZcsException` |
| aip-erp-ai-webservice | `erpai` | 0.7.0 | 0.4.1 | 0.4.1 | `ZcsLogging`, `EndpointFilter`, `ZcsException` |
| aip-data-storage-consumer | `dsconsumer` | 2.10.0 | 0.3.0 | 0.3.0 | `ZcsLogging`, `EndpointFilter`, `ZcsException` |
| aip-audio-service | `audio_service` | 0.2.2 | 0.2.0 | 0.2.0 | `ZcsLogging` |

**Nove versioni diverse di core in produzione**, da 0.2.0 a 0.11.4: 0.2.0, 0.3.0, 0.4.1, 0.10.1, 0.10.2, 0.11.0, 0.11.1, 0.11.3, 0.11.4. Rischio di rilascio: vedi [comportamenti](comportamenti.md) e [questioni aperte](questioni-aperte.md).

## Servizi non in produzione

| Repo | Stato | core su main | core al tag |
|---|---|---|---|
| aip-audio-video-consumer | **Non in produzione**: il modulo `aip-avconsumer` è commentato in `40_aiplatform/main.tf` (r.349-364); la chiave `avconsumer = "1.4.3"` è ancora in `app_versions`.[^maintf][^revisione-gferro] | 0.11.1 | 0.2.0 (tag 1.4.3) |
| aip-xml-invoice-consumer | **Non in produzione**: il modulo `aip-xmlconsumer` è commentato in `40_aiplatform/main.tf` (r.326-333); la chiave `xmlconsumer = "1.8.0"` è ancora in `app_versions`. Letto anche nelle schede di aip-follia-knowledge (verifica con `gcloud` del 9/11/2026). | 0.2.0 | 0.2.0 (tag 1.8.0) |
| aip-follia-voip | **Non è in `app_versions`**. Il suo `main` richiede `0.11.0-rc1` (una rc, non una versione stabile). | 0.11.0-rc1 | 0.11.0 (tag 0.0.1) |

I servizi non in produzione sono elencati perché importano la libreria, non perché i loro tag siano rilasciati.

## Altre librerie

Non hanno una versione in `app_versions` (sono pacchetti, non servizi).

| Libreria | core su main | core all'ultimo tag | Cosa importa |
|---|---|---|---|
| zcs-python-genai | 0.10.2 | 0.10.2 (6.19.1) | `ZcsLogging`, `request_context`, `RequestState` |
| zcs-python-service-connectors | 0.10.2 | 0.10.2 (7.4.1) | `ZcsLogging`, `request_context`, `RequestState` |
| zcs-python-stats | 0.7.2 | 0.7.2 (1.4.1) | `FolliaModule` |
| zcs-python-auth | 0.10.1 | 0.10.1 (3.1.0) | `ZcsException` |
| zcs-python-agents | 0.2.0 | 0.2.0 (0.1.1) | solo il logger, in modo **indiretto**: il suo codice non importa `zcs.core`; lo fa zcs-python-genai 1.4.0 (`zcs.core.logger`, 12 import in `app/src`). Nei requisiti c'è il commento `# logger`[^agentsind] |

Il tag `0.7.2` richiesto da zcs-python-stats non esiste nella repo di core (tag `0.7.0`, `0.7.1`, `0.8.0`): vedi [questioni aperte](questioni-aperte.md).

## La nominano soltanto, senza importarla

| Repo | Dove |
|---|---|
| ml-sopdu-scripts | script del radar delle librerie e relativo storico |
| aip-follia-knowledge | schede `okf/librerie/` di zcs-python-genai, zcs-python-service-connectors e zcs-python-stats |
| aip-audio-service, aip-audio-video-consumer, aip-data-scraper-consumer, aip-follia-voip, aip-mcp-follia-server, aip-statistics-webservice, aip-generative-ai-webservice | testi dei propri bundle OKF o documenti (versione di core, esempi, diagnostica) |
| aip-mcp-teseo-server | `docs/CROSS_TENANT_RACE_FIX_VIA_REQUEST_STATE.md`: progetto di correzione che usa `RequestState` e `request_context`; è un documento di progetto |

## Non la usano (nessuna occorrenza su `origin/main`)

aip-config-api, aip-agents-api, aip-conversational-middleware, agent-chat-server, aip-frontend, aip-auth-server, zcs-python-ms-connectors, aip-data-models-lib.

[^lettura]: Lettura del 10/11/2026.
[^tfvars]: `terraform.tfvars`, mappa `app_versions`.
[^maintf]: `40_aiplatform/main.tf` r.349-364.
[^revisione-gferro]: Indicazione di G. Ferro del 10/11/2026: aip-audio-video-consumer non è in produzione; aip-follia-voip non è in `app_versions`.
[^agentsind]: Uso indiretto da zcs-python-agents tramite zcs-python-genai 1.4.0
