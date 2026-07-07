# Dataset FinSecure Analytics: Dati per RAG e Analisi dei Rischi

Questo repository contiene la base di conoscenza (dataset) utilizzata dall'Agente AI di **FinSecure Analytics** per svolgere le proprie analisi sui rischi finanziari, stress test e audit interattivi.

## Metodologia di Acquisizione: Scraping Automatico
Per simulare in modo realistico il carico di dati di un'azienda del settore assicurando sempre la reperibilità delle fonti, i file presenti in questo repository sono stati estratti tramite **scraping automatizzato**. 

È stato utilizzato uno script Python (`web_scraper.py`) che si connette a pagine enciclopediche e finanziarie altamente specializzate. Lo script elimina il "rumore" di fondo (codice HTML, menu, footer, pubblicità) e restituisce testo puro ottimizzato per l'addestramento e il retrieval (RAG) di modelli LLM come LlamaIndex.

I documenti estratti includono definizioni, case study e framework regolatori su:
* Rischio di Credito, Liquidità, Mercato e Operativo.
* Test di Stress Finanziari, Rischio Sistemico e Cybersecurity in Finanza.
* Normative come Basilea III, Dodd-Frank e Sarbanes-Oxley Act.
* Analisi Macroeconomica, Politiche Monetarie e Strutture della BCE, FED, World Bank e IMF.
* **Profili Corporate:** Dati storici e analisi di business sulle Top 30 aziende globali a maggiore capitalizzazione (Tech, Healthcare, Energy, Finance).

## Elenco delle Fonti (URL)
I documenti `.txt` sono stati estratti fedelmente dalle seguenti 70 fonti testuali robuste e sempre accessibili:

### Gestione dei Rischi Finanziari
1. https://en.wikipedia.org/wiki/Financial_risk_management
2. https://en.wikipedia.org/wiki/Credit_risk
3. https://en.wikipedia.org/wiki/Liquidity_risk
4. https://en.wikipedia.org/wiki/Market_risk
5. https://en.wikipedia.org/wiki/Operational_risk
6. https://en.wikipedia.org/wiki/Value_at_risk
7. https://en.wikipedia.org/wiki/Stress_testing_(financial)
8. https://en.wikipedia.org/wiki/Systemic_risk
9. https://en.wikipedia.org/wiki/Interest_rate_risk
10. https://en.wikipedia.org/wiki/Foreign_exchange_risk
11. https://en.wikipedia.org/wiki/Counterparty_risk

### Regolamentazioni e Compliance
12. https://en.wikipedia.org/wiki/Basel_III
13. https://en.wikipedia.org/wiki/Financial_regulation
14. https://en.wikipedia.org/wiki/Compliance_(regulatory)
15. https://en.wikipedia.org/wiki/Corporate_governance
16. https://en.wikipedia.org/wiki/Financial_audit
17. https://en.wikipedia.org/wiki/Internal_audit
18. https://en.wikipedia.org/wiki/Risk_assessment
19. https://en.wikipedia.org/wiki/Dodd%E2%80%93Frank_Wall_Street_Reform_and_Consumer_Protection_Act
20. https://en.wikipedia.org/wiki/Sarbanes%E2%80%93Oxley_Act

### Istituzioni e Macroeconomia
21. https://en.wikipedia.org/wiki/Macroeconomics
22. https://en.wikipedia.org/wiki/Inflation
23. https://en.wikipedia.org/wiki/Monetary_policy
24. https://en.wikipedia.org/wiki/European_Central_Bank
25. https://en.wikipedia.org/wiki/Federal_Reserve
26. https://en.wikipedia.org/wiki/World_Bank
27. https://en.wikipedia.org/wiki/International_Monetary_Fund
28. https://en.wikipedia.org/wiki/Securities_and_Exchange_Commission
29. https://en.wikipedia.org/wiki/Quantitative_easing

### Gestione Portafogli e Mercati
30. https://en.wikipedia.org/wiki/Asset_management
31. https://en.wikipedia.org/wiki/Portfolio_management
32. https://en.wikipedia.org/wiki/Hedge_fund
33. https://en.wikipedia.org/wiki/Private_equity
34. https://en.wikipedia.org/wiki/Environmental,_social,_and_corporate_governance

### Crisi e Tecnologia Finanziaria
35. https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%932008
36. https://en.wikipedia.org/wiki/Subprime_mortgage_crisis
37. https://en.wikipedia.org/wiki/Cybersecurity_in_finance
38. https://en.wikipedia.org/wiki/Algorithmic_trading
39. https://en.wikipedia.org/wiki/High-frequency_trading
40. https://en.wikipedia.org/wiki/Financial_technology

### Top 30 Corporate Insights (Aziende più Capitalizzate al Mondo)
41. https://en.wikipedia.org/wiki/Apple_Inc.
42. https://en.wikipedia.org/wiki/Microsoft
43. https://en.wikipedia.org/wiki/Nvidia
44. https://en.wikipedia.org/wiki/Alphabet_Inc.
45. https://en.wikipedia.org/wiki/Amazon_(company)
46. https://en.wikipedia.org/wiki/Saudi_Aramco
47. https://en.wikipedia.org/wiki/Meta_Platforms
48. https://en.wikipedia.org/wiki/Berkshire_Hathaway
49. https://en.wikipedia.org/wiki/Tesla,_Inc.
50. https://en.wikipedia.org/wiki/Eli_Lilly_and_Company
51. https://en.wikipedia.org/wiki/Broadcom_Inc.
52. https://en.wikipedia.org/wiki/TSMC
53. https://en.wikipedia.org/wiki/JPMorgan_Chase
54. https://en.wikipedia.org/wiki/UnitedHealth_Group
55. https://en.wikipedia.org/wiki/Visa_Inc.
56. https://en.wikipedia.org/wiki/Novo_Nordisk
57. https://en.wikipedia.org/wiki/ExxonMobil
58. https://en.wikipedia.org/wiki/Walmart
59. https://en.wikipedia.org/wiki/Mastercard
60. https://en.wikipedia.org/wiki/Johnson_%26_Johnson
61. https://en.wikipedia.org/wiki/Procter_%26_Gamble
62. https://en.wikipedia.org/wiki/Tencent
63. https://en.wikipedia.org/wiki/Samsung_Electronics
64. https://en.wikipedia.org/wiki/ASML_Holding
65. https://en.wikipedia.org/wiki/Oracle_Corporation
66. https://en.wikipedia.org/wiki/The_Home_Depot
67. https://en.wikipedia.org/wiki/Chevron_Corporation
68. https://en.wikipedia.org/wiki/Merck_%26_Co.
69. https://en.wikipedia.org/wiki/Bank_of_America
70. https://en.wikipedia.org/wiki/The_Coca-Cola_Company
