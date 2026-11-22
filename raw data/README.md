# Raw data

Unprocessed source files behind the China extraction, copied as-is from the project's shared folder.

## customs-gazette-ocr/
- `Customs_Gazette_<year>_Q<n>_No<###>.txt` (89 files): OCR text from Gale of the Chinese Imperial Maritime Customs *Customs Gazette* (Statistical Series No. 2), Nos. 66-180, 1885-1913. These are the texts the `china/extraction/staging/` rows were extracted from.
- `_mapping.tsv`: maps each renamed file to its original Gale file name (`GALESC…txt`) and the issue's full catalogue title.

## scans/
- `SC5111087997.pdf`, `SC5111094064.pdf`, `SC5111094260.pdf`, `SC5111096391.pdf`: page-image scans from Gale (no text layer), 183-197 pages each. They are stored with Git LFS because each is 230-290 MB, over GitHub's 100 MB file limit. Run `git lfs install` before cloning, or `git lfs pull` afterwards, to download them.
