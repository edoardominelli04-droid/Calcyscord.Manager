# Correzione multi-provider Calcyscord.Manager

Estrai dalla cartella del progetto:

```bash
unzip -o ~/Downloads/calcyscord_multisource_fix.zip -d .
```

Verifica che `.env` contenga `FOOTBALL_DATA_API_KEY`, quindi esegui il normale aggiornamento database.
Se una corrispondenza è incerta, l'aggiornamento si ferma senza salvare i club. Inserisci la corrispondenza verificata in `data/config/club_provider_overrides.json`, per esempio:

```json
{"IT1":{"46":108}}
```

Verifica sintassi e risultato:

```bash
python3 -m py_compile services/identity/club_identity_service.py services/providers/football_data_provider.py services/mappers/club_mapper.py services/importers/competition_importer.py services/importers/club_importer.py services/importers/player_importer.py services/game/club_selection_service.py tools/audit_provider_alignment.py
python3 tools/audit_provider_alignment.py
```

Audit live completo, senza modificare i dataset:

```bash
python3 tools/audit_live_provider_alignment.py
```

Prima dell'aggiornamento crea un commit o una copia di `data/datasets`.
