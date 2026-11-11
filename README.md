# PATH: arms trade data entry (Hinson)

Data entry for the Path project, a dashboard of the arms trade between countries in the 19th and early 20th centuries.

## japan/ (complete)
- `workbooks/Japan_Arms_Imports_1860-1914.xlsx`, `Japan_Arms_Exports_1860-1914.xlsx`: one sheet per year. Columns: Type, Imported from / Exported to, Count, Value (JPY). Extracted from 大日本外国貿易年表 (Annual Return of the Foreign Trade of the Empire of Japan).
- `workbooks/blanked-cells.md`: cells left blank and why.
- `reports/Japan Data Entry Report.docx`: write-up of the Japan data entry.
- `sources/`: source volumes and page-by-page verification links.
- `japan-arms-trade-prompts.md`: the prompts and workflow used.

## china/ (in progress, updated automatically)
- `workbooks/China_Arms_Imports_1883-1913.xlsx`, `China_Arms_Exports_1883-1913.xlsx`: one sheet per year. Columns: Type, Raw material, Imported from / Exported to, Port, Quarter, Count, Unit, Value (HK Tls), Entry. Extracted from the Chinese Maritime Customs *Customs Gazette* (quarterly, Statistical Series No. 2), Nos. 66-180. The Coverage sheet shows which quarters are processed, pending or missing from the source set.
- `extraction/EXTRACTION_RULES.md`: what is recorded and how.
- `extraction/staging/No###.json`: the extracted rows for each issue; `build_workbooks.py` rebuilds both workbooks from these.
- `extraction/progress.log`: one line per processed issue.
- `sources/`: lists of Chinese customs sources and scans.

The raw OCR text of the Gazette (Gale) and the scanned PDFs are not included.
