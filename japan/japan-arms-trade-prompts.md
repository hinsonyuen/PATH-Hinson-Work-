# Japan arms trade data (Path project): prompts and workflow

A reference for extracting arms trade data for another country, compiled 6 Nov 2026 from Hinson's work on the Japan dataset for the Path project.

The Japan work produced two Excel workbooks, `Japan_Arms_Imports` and `Japan_Arms_Exports`, with one sheet per year (1882–1892, 1895–1896 and 1899–1914 filled in), extracted from scanned Japanese annual trade returns and checked against the national totals in the same volumes.

**What's below**
1. The prompts, verbatim and in order, with a short note on what each produced
2. The workflow, and how it could be adapted for Germany
3. Lessons learned

Prompts are copied exactly as typed, typos included. Automatic system text (timezone stamps and similar) has been removed.

---

## 1. Prompts in order

### Phase 1: the original claude.ai chat, "Japan arm trade data extraction" (12–18 Oct 2026)

Hinson attached 20 PDFs downloaded from HathiTrust (the full scanned volumes of 大日本外国貿易年表 / *Annual Return of the Foreign Trade of the Empire of Japan*).

**Prompt 1: the main spec** (12 Oct)

> I am currently working of a project called Path. This project seeks to create a dashboard for historians to visualize the arm trade across countries during the 19th and early 20th century.
>
> My role in Path is complete the trade data for Japan. The attached pdfs are 大日本外国貿易年表 from years 1882 to 1912. With the first document being for 1912 and in descending order of attachment. Beware that 1882-84, 1885-86, 1887-88, 1891-92, and 1895-96 are in combined documents where one attachment contains data from multiple years.
>
> You will parse through all these documents and extract critical data on the import and export of Arms. The following are the data you will extract:{Import Data:[
> Year, Type of weapons(ex. musket, canon cartriges), Amount(if given), value(in yen),  where it is imported from(ex. United Kingdom, France)],
> Export data:[Year, Type of weapons(ex. musket, canon cartriges), Amount(if given), value(in yen),  where it is exported to(ex. United Kingdom, France)]
>
> After parsing, you will create two excel spread files:
> File one: Create one spreadsheet for each year for import data. Contain the following columns in this order: Type, imported from, count(N/A if not given), value (JPY)
> File two: Create one spreadsheet for each year for export data. Contain the following columns in this order: Type, Exported to, count(N/A if not given), value (JPY)

*Result:* Claude checked the PDFs, found they were image scans, and started locating the arms entries year by year. It noted that the set actually ran 1882–1911 (the first file was 1911, not 1912) and that 1893, 1894 and 1897 were missing.

**Prompt 2**

> only parse the 1911 document

*Result:* Two workbooks for 1911 only, each with a "1911" sheet in the requested columns and a Notes sheet. It flagged that the Imperial Army & Navy's own purchases appear only as a national figure with no country ("Not specified"), that Japan exported no arms of its own (only re-exports of foreign goods), that units were pieces for guns and kin (斤) for explosives, and that ambiguous digits (3 vs 8) were resolved against the national totals and flagged in cell comments.

**Prompt 3**

> do 1910

*Result:* 1910 workbooks in the same layout. Every country breakdown matched the national totals (one item off by 5 yen from rounding); nine hard-to-read figures were flagged.

**Prompt 4: one file, plus a country-mapping rule**

> combine the years in to one file, from now we will work on the documents one by one, when you are done add to the existing documents. Also for provinces, put the country they belong to unless they are a colony (ex. Kwantung Province -> China)

*Result:* One imports file and one exports file, one sheet per year, newest first, with a shared Notes sheet. Provinces were mapped to their country with the original name kept in a cell comment; colonies (e.g. British India, Canada) kept as listed. Claude asked how to label Korea after 1910 (left open).

**Prompts 5–8: working through the volumes**

> do 1909 and 1908

> do 1907, 1906

> 1905,1904

> 1903, 1902

> 1901, 1900, 1899

*Result:* Each batch added sheets for those years, with a short report per year: largest items and suppliers, Army & Navy "special import" totals, and any figure that didn't add up (e.g. 1899 dynamite printed ¥55,000 above the national total, kept as printed and flagged). Rows that mapped to the same country and item were merged, with the source lines noted. The 1904–05 volumes list no military purchases (Russo-Japanese War), which was recorded as missing data, not zero. When the return's categories changed (1906 and earlier group guns more broadly), the original wording was kept.

**Prompt 9**

> 1898,1897

*Result:* Interrupted. Claude found that about half the 1898 scan's value column was cut off at the binding and there was no 1897 volume, and asked whether to enter those years with gaps or skip them.

**Prompts 10–13: understanding the sources** (useful questions to ask about any country's returns)

> explain the special imports,

*Result:* Explained the appendix 特別輸出入品表 (from 1900): Army & Navy purchases of arms and warships, given as one national value each, not included in the country tables, and worth millions of yen against tens of thousands in commercial arms imports. Included a year-by-year table and caveats (1904–05 not listed; 1899 has no appendix; 1898's "Imports by the Government" is already inside the main tables, so adding it would double count).

> so are the special imports from foreign countries but simply undocumented?

*Result:* Yes: the value is recorded but not the origin or quantity. Suggested recovering origins from partner-country ("mirror") statistics and warship records, and keeping any reconstructed origins as separate rows marked "attributed from [source]".

> So you are saying that the Okursho does not track imports and exports in the army and navy and only keep track of commercial goods

*Result:* A correction: the Ōkurashō (Finance Ministry) did track them, but in a separate appendix. The real split is ordinary customs declaration vs. special procedures. Claude noted this was inferred from the table layout and suggested reading each volume's introductory notes (凡例) to cite the ministry's own definition.

> do you know if the country of origin and destination is documented in any other official document

*Result:* A list of sources to check (from Claude's own knowledge, not verified in the session): Army and Navy Ministry records on JACAR, ministry annual reports, war expenditure accounts, partner-country trade returns (including Germany's *Statistik des Deutschen Reichs*), and arms-maker archives (Vickers, Armstrong, Krupp).

**Prompt 14: new uploads**

> There are the same document from different  years. Hold on to them until I ask you to add to the excel.

*Result:* Claude found the 17 files were single title pages only (HathiTrust had downloaded the current page, not the whole book), and explained how to download the full volumes.

**Prompt 15**

> add 1912, 13, 14

*Result:* Couldn't be done until the full volumes were re-downloaded.

**Prompt 16: handoff to Claude Code**

> copy eveything in this chat so that I can move to claude code

*Result:* A zip with a `CLAUDE.md` handoff note (the spec, every decision made, each year's status, open questions), the current workbooks, per-year data files, and scripts to rebuild the workbooks and check sums against the national totals.

### Phase 2: Claude Code session (18 Oct 2026)

Hinson continued in Claude Code on their own PC, which filled in 1882–1896 and 1912–1914. Most of that session's prompts weren't carried over into this project, so they can't be quoted here. The one that survives:

> download the files

### Phase 3: this project (22 Oct – 4 Nov 2026)

**Prompt 17: resuming work**

> I'd like to continue the work from session [earlier Claude Code session]. Please read that session, catch up on its full context, then summarize what it was doing, what's done, and what's next, and be ready to pick up where it left off.

*Result:* A summary: 29 years done (1882–1892, 1895–96, 1899–1914), the few small unreconciled gaps, and what was left (1893–94, 1897–98, 1915 onward).

**Prompt 18: finding earlier sources**

> I want to incude the data for years from 1860 to what we have now, find the correct documents and inform me of them.

*Result:* [source-volumes-1860-1898.md](../sources/source-volumes-1860-1898.md): links for the missing years (1893, 1894, 1897 at the National Diet Library; 1898 on HathiTrust), the Finance Ministry's 1868–1894 comparison tables (national totals, probably no country breakdown), and the British consular reports for 1862–67. No published source was found for 1860–61.

**Prompt 19: verification**

> give me a link and the pages of the data you extracted. The purpose is so that I can verify your work.

*Result:* [verification-pages.md](../sources/verification-pages.md): every row for 1882–84 with a link to its HathiTrust page, and for later years the volume and national-total pages.

> include verifications for years before 1882

*Result:* Claude explained nothing before 1882 had been extracted yet, so there was nothing to verify.

**Prompts 20–22: correcting the value column**

> These are the most updated versions, the Value(JPY) are all wrong as they are two digits short. Fix this by adding 2 zeros after the current numbers.
> For example, if it shows as 120, edit to 12000

*Result:* Claude misread this as applying to every sheet. It checked against the source and argued the values were already in yen, and repaired only the 1882 sheet.

> did you make edits to to years before 1882?

> You have mistaken my prompt, I have fixed the 1882 sheets on both excels. However, all the other sheets post 1882 are missing 2 digits in the value. You will add them back for example, 120 -> 12000. Return 2 excels with the updated values

*Result:* Every value from 1883–1914 multiplied by 100 (766 import cells, 237 export cells), with 1882 and the Count column left as they were. Claude noted that the column header might need a unit note.

**Prompt 23: no guessed values**

> While verifying 1882 for Germany, the value in the raw document is completely unreadable. However, you gave a guess on the value. Update the excel so that the values with ambigious raw data will be empty

*Result:* 109 cells blanked across both workbooks: every figure that was illegible, cut off, or "adjusted to reconcile" with the national total. Legible figures that don't add up were kept. Each blank is listed with its page in [blanked-cells.md](../workbooks/blanked-cells.md).

---

## 2. The workflow, and adapting it for Germany

### What worked for Japan

1. **Get full scans of the official annual returns.** Japan's came from HathiTrust (University of California copies) and the National Diet Library. Download the *whole item*, not the current page. Full volumes are tens of MB.
2. **Write one precise spec up front** (Prompt 1): the fields to extract, the exact columns and their order, one sheet per year, how to show missing counts ("N/A").
3. **Run one volume first** (Prompt 2), check it, then go in batches of two or three years (Prompts 5–8). Big batches are harder to check.
4. **Keep one file per flow**, one sheet per year, and a Notes sheet that records the source volume and pages for each year.
5. **Check every year against the national totals** printed in the same volume. A country breakdown that adds up to the total is the best evidence the reading is right.
6. **Decide the rules early and write them down:** country mapping (provinces to their country, colonies kept as listed), units, how to treat categories that change over time.
7. **Don't let the model guess.** Blank illegible figures and list them (Prompt 23). A figure "adjusted to reconcile" with the total is still a guess.
8. **Ask for page references for every row** (Prompt 19) so a person can spot-check the scans.
9. **Ask about the source's structure** (Prompts 10–13). For Japan, the biggest arms purchases weren't in the country tables at all.

### Adapting the spec for Germany

A starting prompt could follow Prompt 1, with these changes:

- **Source series.** Germany's main source is likely the *Statistik des Deutschen Reichs* (Imperial Statistical Office), with the monthly *Monatliche Nachweise über den auswärtigen Handel* as a supplement; before the Reich series, the Zollverein's statistics. Check which years have a breakdown by country for arms. Many volumes are on HathiTrust and in German digital libraries.
- **Currency and units.** Values in Mark (ℳ) rather than yen; quantities usually by weight (Doppelzentner = 100 kg, or kg) rather than pieces. Name the unit in the column header (e.g. "Value (Mark)") and confirm it from each volume's header. The Japan files hit a unit problem late on (Prompts 20–22) that a clear header would have avoided.
- **Direction of trade.** Japan was almost only an importer and re-exporter of arms. Germany was a major exporter (Krupp, Mauser and others), so the export file will likely be the larger one, and the question of whether state arms deals appear in the ordinary tables matters most on the export side.
- **Country names and borders.** Agree a mapping rule like Prompt 4's, and decide how to treat colonies, protectorates, and changing borders (e.g. Austria-Hungary, Ottoman Empire, Sweden & Norway until 1905).
- **Customs territory.** Check what the statistics cover. Hamburg and Bremen stayed outside the German customs area until 1888, which may affect what earlier returns count.
- **Fraktur type.** German volumes of the period are often printed in Fraktur, and the column headings will be in German. Ask Claude to flag uncertain readings in the same way as the 3/8 and 5/6 problem in the Japanese scans.
- **Mirror check with Japan.** The Japan workbooks list imports from Germany every year. Comparing them with Germany's recorded exports to Japan is a useful cross-check for both datasets (expect differences from valuation, timing and transit through third countries).

---

## 3. Lessons learned

- **Say exactly which sheets or years a correction applies to.** Prompt 20 was read as "all sheets", when it meant "all sheets except 1882". Naming the range ("1883–1914 only") avoids a round trip.
- **Treat "reconciled" figures with care.** Matching the national total is a good check, but a value chosen to make the total match is not a reading. Ask for these to be flagged or blanked from the start.
- **Check downloads before uploading.** Single-page downloads from HathiTrust look like full volumes but contain only a title page.
- **Long chats lose context.** Before moving tools, ask for a handoff file (Prompt 16) that records the spec, the decisions and each year's status.
- **Treat Claude's citations from memory as leads.** The archive and statistics suggestions in Prompt 13 were not checked during the session and should be verified before citing.

---

## Related files in this project

- [source-volumes-1860-1898.md](../sources/source-volumes-1860-1898.md): sources for the earlier and missing years
- [verification-pages.md](../sources/verification-pages.md): page links for checking each figure
- [blanked-cells.md](../workbooks/blanked-cells.md): the 109 figures left blank and why
- `workbooks/Japan_Arms_Imports_1860-1914.xlsx` and `workbooks/Japan_Arms_Exports_1860-1914.xlsx`: the current workbooks
