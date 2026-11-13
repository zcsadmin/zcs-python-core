---
okf_version: "0.2"
---

# Bundle OKF di zcs-python-core

Schede che descrivono la libreria Python `zcs-python-core` vista da chi la usa: cosa offre, come si comporta, chi la usa e come si rilascia. Le schede sono scritte da un agente e controllate da chi porta la modifica su `main`: data e autore di ogni modifica stanno nella storia git (`git log -- okf/`).

* [Panoramica della libreria](libreria.md) - cosa offre, installazione, dipendenze e dove guardare
* [Comportamenti da conoscere](comportamenti.md) - contesto assente, effetti globali del logger, errori dei contatori, campi inviati a Loki
* [Chi usa la libreria](consumatori.md) - servizi e librerie, versioni richieste e in produzione
* [Storia delle versioni](versioni.md) - tag dal 2025 e modifiche non retrocompatibili
* [Questioni aperte](questioni-aperte.md) - problemi noti con priorità

## Sezioni

* [API](api/index.md) - sessione, logger, eccezioni, telemetria
* [Flussi](flussi/index.md) - ciclo di vita del contesto della richiesta
* [Operatività](operativita/index.md) - configurazione e rilascio
