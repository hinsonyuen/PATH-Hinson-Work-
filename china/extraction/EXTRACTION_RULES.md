# China arms trade extraction: rules for each scheduled run

Source: Chinese Maritime Customs, *Customs Gazette* (Statistical Series No. 2), quarterly, raw OCR text in
`/mnt/project-files/Customs_Gazette_<YEAR>_<Q>_No<NNN>.txt`. Each line of a file is roughly one printed page
(line 1 is a Gale disclaimer; line 2 is the title). Files are 200–900 KB, so never read a whole file at once.

## What one run does
1. Find the issue to process: the **oldest** file in your assigned year range that has no
   `staging/No<NNN>.json` yet (NNN = the 3-digit issue number in the filename).
   If none is left, your range is finished (see "When the range is done").
2. Locate arms entries with grep (case-insensitive) and read only the matching pages (`sed -n '<line>p' file | fold -w 400`).
   Keywords, allowing for OCR damage: arms, fire-arms/firearms, rifle, musket, gun (but not "gunny"), revolver, pistol,
   cannon, ordnance, cartridge, ammunition, munition, percussion cap, shot, shell, gunpowder/powder, dynamite,
   explosive, detonator, fuse, torpedo, sword, bayonet, military stores, saltpetre/saltpeter/nitre, sulphur/sulfur,
   nitrate, chlorate. Read the surrounding table heading to know which port and which table the entry belongs to.
3. Record every entry (rules below) in `staging/No<NNN>.json`, then run `python3 build_workbooks.py`
   (it rebuilds BOTH workbooks from all staging files, so never edit the .xlsx files by hand).
4. Append one line to `progress.log`: date/time, issue, rows imports/exports, anything doubtful.

5. Push to GitHub: `bash /mnt/project-files/china-gazette/sync_repo.sh "China: Customs Gazette No. <NNN> (<YEAR> <Q>), <n> import rows, <m> export rows"`.
   It copies the workbooks, staging files and log into the repo hinsonyuen/PATH-Hinson-Work- and pushes to main.
   If it prints PUSH FAILED, note that in progress.log and post one short message in the thread.

## What to record
- **Manufactured** (Raw material = false): firearms of any kind and their parts, cannon/ordnance, swords/bayonets,
  cartridges/ammunition/shot/shells, percussion caps, gunpowder, dynamite and other explosives, detonators, fuses, torpedoes, military stores.
- **Raw materials** (Raw material = true): saltpetre (nitre), sulphur, and other explicit gunpowder/explosive
  ingredients (nitrates, chlorate of potash). Do NOT include lead, iron, steel, copper or other general metals.
- **Exclude**: "Gunpowder" tea (a kind of green tea in the tea tables), "gunny" bags, fireworks/crackers
  (record them only if the table explicitly classes them as explosives), and OCR words that merely look similar.
- **Tables**: imports tables -> `imports`; exports tables -> `exports`; re-exports tables -> the matching list
  with `"entry": "Re-export"`. Arms, ammunition, explosives, saltpetre or sulphur listed in **Fines and
  Confiscations** -> `"entry": "Seizure"` (imports list unless the offence was attempting to export). Trade-table rows use `"entry": "Trade"`. Stock held in the Shanghai bonded warehouse tables that did not arrive or leave in the quarter -> `"entry": "Bonded stock"` (arrivals in bond during the quarter are imports, "Trade").
- **Current year only**: tables print the same quarter for the previous 3 years as comparison columns.
  Take only the column for the issue's own year. Never sum or copy the earlier-year columns.
- **Port**: the Customs port whose return the entry appears in (e.g. "Shanghai", "Tientsin", "Canton"),
  normalised to the spelling used in the Gazette heading.
- **Partner**: the foreign country only if the Gazette names it for that entry (e.g. a "Countries from which imported" table,
  or the vessel's origin in a seizure). If the table says "Foreign Countries and Chinese Ports" or gives none, use null
  (shown as "Not specified"). Map provinces/cities to their country unless a colony (Hongkong stays "Hongkong").
- **Count / unit**: the quantity and unit as printed (pieces, piculs, boxes, catties, cases). null if not given.
- **Value**: Haikwan Taels as printed, never converted. null if not given. For seizures use the value of goods
  confiscated if printed (not the fine).
- **Doubtful readings**: enter the best reading and say so in `note` (e.g. "OCR: 3,852 or 3,352").
  If a whole table is unreadable, add an `issue_notes` line saying which port/table.
- **Seizure rows**: one row per item per case; put case number, date and vessel flag in `note`. Leave value null
  (the 'amount realised' is per case, not per item). If a quantity is unreadable, use null and quote the OCR reading
  in `note`. 'Brimstone' -> type "Sulphur (brimstone)". The vessel's flag is not the country of origin.
  See staging/No066.json for a worked example.
- Merge nothing across ports; one row per item per port per entry type.

## staging/No<NNN>.json format
```json
{
  "issue": 180, "year": 1913, "quarter": "Q4",
  "file": "Customs_Gazette_1913_Q4_No180.txt",
  "processed_at": "2026-11-11 03:10 UTC", "processed_by": "Task A or Task B",
  "imports": [
    {"type": "Saltpetre", "raw_material": true, "partner": null, "port": "Shanghai",
     "count": 320, "unit": "piculs", "value_hktls": null, "entry": "Trade",
     "source": "file line 40, Shanghai II. Imports, principal articles", "note": ""}
  ],
  "exports": [],
  "issue_notes": ["Anything a reader of the workbook should know about this issue, or 'No arms entries found.'"]
}
```
If an issue has no arms entries at all, still write the file with empty lists and an issue note saying so,
so the run is not repeated.

## When the range is done
Post one short message in the thread saying the range is complete with the row totals, then delete your own
scheduled task (list_triggers, find yours by name, delete_trigger).
