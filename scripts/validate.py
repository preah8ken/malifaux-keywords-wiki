#!/usr/bin/env python3 import sys, re, pathlib

REQUIRED_H2 = {"Summary", "How to win", "How to lose", "Table"} TABLE_HEADER = ["Unit", "Cost", "Role", "Notable abilities", "Synergies", "Counters"]

def normalize_header_row(row): return [c.strip().lower() for c in row.strip().strip("|").split("|")]

def check_file(path: pathlib.Path): errs = [] text = path.read_text(encoding="utf-8")
# H2s: must be exactly the required set (order not enforced)
h2s = set(m.group(2).strip() for m in re.finditer(r"^##\s+(.+)$", text, flags=re.M))
if h2s != REQUIRED_H2:
    errs.append(f"{path}: H2s must be exactly {sorted(REQUIRED_H2)}; found {sorted(h2s) or 'none'}.")

# Disallow H3+ (no ###)
if re.search(r"^#{3,}\s+", text, flags=re.M):
    errs.append(f"{path}: Only H1 and the required H2 sections are allowed (no ### or deeper).")

# Table header under '## Table'
m = re.search(r"^##\s+Table\s*\n(.*?)(\n##\s+|$\Z)", text, flags=re.M | re.S)
table_ok = False
if m:
    block = m.group(1)
    for line in block.splitlines():
        if "|" in line and line.strip().startswith("|"):
            cells = normalize_header_row(line)
            if cells == [c.lower() for c in TABLE_HEADER]:
                table_ok = True
                break
if not table_ok:
    errs.append(f"{path}: Table header must be exactly: | " + " | ".join(TABLE_HEADER) + " |")

return errs
def main(): root = pathlib.Path("docs/keywords") if not root.exists(): print("docs/keywords not found.", file=sys.stderr) return 1 problems = [] for md in root.glob("*.md"): if md.name.startswith("_"): continue problems += check_file(md) if problems: print("\n".join(problems), file=sys.stderr) return 1 print("Validation passed.") return 0

if name == "main": sys.exit(main())

