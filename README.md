# Dataset FinSecure Analytics: Dati per RAG e Analisi dei Rischi

Questo repository contiene la base di conoscenza (dataset) utilizzata dall'Agente AI di **FinSecure Analytics** per svolgere le proprie analisi sui rischi finanziari, stress test e audit interattivi.

## Metodologia di Acquisizione: Scraping Automatico
Per simulare in modo realistico il carico di dati di un'azienda del settore assicurando sempre la reperibilità delle fonti, i file presenti in questo repository sono stati estratti tramite **scraping automatizzato**. 

È stato utilizzato uno script Python che utilizza **BeautifulSoupWebReader** di **LlamaIndex** che si connette a pagine enciclopediche e finanziarie altamente specializzate. Lo script elimina il "rumore" di fondo (codice HTML, menu, footer, pubblicità) e restituisce testo puro ottimizzato per l'addestramento e il retrieval (RAG) di modelli LLM come LlamaIndex.

I documenti estratti includono definizioni, case study e framework regolatori su:
* Rischio di Credito, Liquidità, Mercato e Operativo.
* Test di Stress Finanziari, Rischio Sistemico e Cybersecurity in Finanza.
* Normative come Basilea III, Dodd-Frank e Sarbanes-Oxley Act.
* Analisi Macroeconomica, Politiche Monetarie e Strutture della BCE, FED, World Bank e IMF.
* **Profili Corporate:** Dati storici e analisi di business sulle Top 30 aziende globali a maggiore capitalizzazione (Tech, Healthcare, Energy, Finance).

## Elenco delle Fonti (URL)

### Rischio e Regolamentazioni
Questi documenti forniscono all'LLM le regole ferree su cui basare gli audit:
1. https://en.wikipedia.org/wiki/Financial_risk_management
2. https://en.wikipedia.org/wiki/Credit_risk
3. https://en.wikipedia.org/wiki/Basel_III

### Istituzioni e Macroeconomia
Permettono all'agente di comprendere le logiche di mercato, l'inflazione e i tassi di interesse:
4. https://en.wikipedia.org/wiki/European_Central_Bank
5. https://en.wikipedia.org/wiki/Securities_and_Exchange_Commission
6. https://en.wikipedia.org/wiki/Macroeconomics

### Scenari di Crisi e Stress Test
Forniscono lo storico dei dati per prevedere futuri shock di mercato:
7. https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%932008

### Profili Corporate (Tech, Finance, Energy)
Dati storici e logiche di business su aziende reali per simulare l'esposizione del portafoglio clienti:
8. https://en.wikipedia.org/wiki/Apple_Inc. (Tech / Hardware)
9. https://en.wikipedia.org/wiki/JPMorgan_Chase (Banking / Finance)
10. https://en.wikipedia.org/wiki/Saudi_Aramco (Energy / Commodities)
