"""Rebuild China_Arms_Imports / China_Arms_Exports workbooks from staging/No###.json.

Safe to run any number of times: the workbooks are always regenerated in full
from the staging files, so a run never depends on the previous workbook state.
Usage: python3 build_workbooks.py
"""
import json, glob, os, re, datetime, tempfile, shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.comments import Comment

ROOT = "/mnt/project-files"
HERE = os.path.join(ROOT, "china-gazette")
STAGING = os.path.join(HERE, "staging")
OUT = {
    "imports": os.path.join(ROOT, "workbooks", "China_Arms_Imports_1883-1913.xlsx"),
    "exports": os.path.join(ROOT, "workbooks", "China_Arms_Exports_1883-1913.xlsx"),
}
YEARS = list(range(1913, 1882, -1))  # newest first, like the Japan workbooks
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
QLABEL = {"Q1": "Jan-Mar", "Q2": "Apr-Jun", "Q3": "Jul-Sep", "Q4": "Oct-Dec"}
FIRST_ISSUE_YEAR = 1885  # issue No. 66 = 1885 Q2; issue no = 66 + (year-1885)*4 + (q-2)

HEAD_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FONT = Font(bold=True, color="FFFFFF")


def issue_no(year, q):
    return 66 + (year - 1885) * 4 + (int(q[1]) - 2)


def source_files():
    """Map (year, quarter) -> filename for every gazette in the project folder."""
    found = {}
    for p in glob.glob(os.path.join(ROOT, "Customs_Gazette_*_Q*_No*.txt")):
        m = re.search(r"Customs_Gazette_(\d{4})_(Q\d)_No(\d+)\.txt$", p)
        if m:
            found[(int(m.group(1)), m.group(2))] = os.path.basename(p)
    return found


def load_staging():
    data = {}
    for p in sorted(glob.glob(os.path.join(STAGING, "No*.json"))):
        with open(p) as f:
            d = json.load(f)
        data[(int(d["year"]), d["quarter"])] = d
    return data


def header(ws, cols, widths):
    ws.append(cols)
    for i, c in enumerate(ws[1]):
        c.font, c.fill = HEAD_FONT, HEAD_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[c.column_letter].width = widths[i]
    ws.freeze_panes = "A2"


def build(kind, files, staged):
    partner = "Imported from" if kind == "imports" else "Exported to"
    cols = ["Type", "Raw material", partner, "Port", "Quarter", "Count", "Unit", "Value (HK Tls)", "Entry"]
    widths = [46, 12, 24, 16, 10, 12, 12, 16, 12]
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    notes_rows = []

    for y in YEARS:
        ws = wb.create_sheet(str(y))
        header(ws, cols, widths)
        missing_q = [q for q in QUARTERS if (y, q) not in files]
        have_q = [q for q in QUARTERS if (y, q) in files]
        if not have_q:
            ws.append(["No data: no Customs Gazette issues for this year are in the source set",
                       "", "Not specified", "", "", "N/A", "", "N/A", "Missing"])
            ws.cell(row=2, column=1).font = Font(italic=True, color="808080")
            notes_rows.append((str(y), f"Missing year: none of the four quarterly issues (Nos. {issue_no(y,'Q1')}-{issue_no(y,'Q4')}) are in the source set. Sheet left empty on purpose; missing data is not zero trade."))
            continue
        if missing_q:
            notes_rows.append((str(y), "Partial year: issue(s) for " + ", ".join(f"{q} ({QLABEL[q]}, No. {issue_no(y,q)})" for q in missing_q) +
                               " are not in the source set, so this sheet covers only " + ", ".join(have_q) + "."))
        rows = []
        for q in have_q:
            d = staged.get((y, q))
            if not d:
                continue
            for r in d.get(kind, []):
                rows.append((q, r))
        rows.sort(key=lambda t: (t[0], str(t[1].get("port") or ""), str(t[1].get("type") or "")))
        for q, r in rows:
            cnt = r.get("count")
            val = r.get("value_hktls")
            ws.append([r.get("type"), "Yes" if r.get("raw_material") else "No",
                       r.get("partner") or "Not specified", r.get("port") or "Not specified", q,
                       cnt if cnt not in (None, "") else "N/A", r.get("unit") or "",
                       val if val not in (None, "") else "N/A", r.get("entry") or "Trade"])
            row = ws.max_row
            for c in (6, 8):
                if isinstance(ws.cell(row=row, column=c).value, (int, float)):
                    ws.cell(row=row, column=c).number_format = "#,##0.##"
            src = r.get("source") or ""
            note = r.get("note") or ""
            text = f"Source: Customs Gazette No. {d_issue(staged, y, q)} ({y} {q}); {src}" + (f"\n{note}" if note else "")
            ws.cell(row=row, column=1).comment = Comment(text, "Claude")
        if len(have_q) and not any((y, q) in staged for q in have_q):
            ws.append(["Pending: issues for this year not yet processed", "", "", "", "", "", "", "", "Pending"])
            ws.cell(row=ws.max_row, column=1).font = Font(italic=True, color="808080")

    # Notes sheet
    ns = wb.create_sheet("Notes")
    header(ns, ["Year", "Note"], [10, 140])
    general = [
        ("All", "Source: China, Imperial Maritime Customs, I. Statistical Series No. 2, Customs Gazette (quarterly), Nos. 66-180 (Apr 1885 - Dec 1913), raw OCR text from Gale. One sheet per year; the Quarter column says which issue a row comes from."),
        ("All", "Values are in Haikwan Taels (HK Tls) as printed, never converted. N/A means the Gazette gives no figure. Count is in the unit printed in the Unit column (pieces, piculs, boxes, etc.)."),
        ("All", "Each issue prints the same quarter for the previous three years as comparison columns. Only the current-year column is entered, so nothing is counted twice."),
        ("All", "Port = the Customs port whose return lists the entry. Imported from / Exported to = the foreign country only where the Gazette names it; otherwise 'Not specified' (most quarterly port tables lump 'Foreign Countries and Chinese Ports' together)."),
        ("All", "Entry = 'Trade' for rows from the trade tables; 'Seizure' for arms, ammunition and explosives listed in the Fines and Confiscations tables (contraband, not legal trade, but evidence of flows). 'Re-export' for re-export tables."),
        ("All", "Raw material = Yes for saltpetre, sulphur and other gunpowder/explosive ingredients; No for manufactured arms, ammunition, explosives and parts."),
        ("All", "'Gunpowder' in the tea tables is a kind of green tea and is excluded. Ambiguous OCR digits are entered as best read and flagged in the cell comment on the Type column."),
    ]
    for r in general:
        ns.append(r)
    for r in notes_rows:
        ns.append(r)
    for (y, q), d in sorted(staged.items(), reverse=True):
        for n in d.get("issue_notes", []):
            ns.append((f"{y} {q}", n))
    for row in ns.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")

    # Coverage sheet
    cs = wb.create_sheet("Coverage")
    header(cs, ["Year", "Quarter", "Issue No.", "Source file", "Status", "Rows (this workbook)"], [8, 10, 10, 40, 34, 18])
    for y in reversed(YEARS):
        for q in QUARTERS:
            n = issue_no(y, q)
            f = files.get((y, q))
            d = staged.get((y, q))
            if not f:
                status = "Missing from source set"
            elif d:
                status = f"Processed {d.get('processed_at','')}"
            else:
                status = "Pending"
            cs.append([y, q, n, f or "", status, len(d.get(kind, [])) if d else ""])
    return wb


def d_issue(staged, y, q):
    return staged[(y, q)].get("issue", issue_no(y, q))


def main():
    files, staged = source_files(), load_staging()
    for kind, path in OUT.items():
        wb = build(kind, files, staged)
        fd, tmp = tempfile.mkstemp(suffix=".xlsx", dir=HERE)
        os.close(fd)
        wb.save(tmp)
        shutil.move(tmp, path)  # replace in one step so a reader never sees a half-written file
        print("wrote", path)
    print(f"{len(staged)} of {len(files)} issues processed")


if __name__ == "__main__":
    main()
