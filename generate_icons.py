import os

DOCTORS_DIR     = os.path.join("static", "images", "doctors")
DEPARTMENTS_DIR = os.path.join("static", "images", "departments")

os.makedirs(DOCTORS_DIR, exist_ok=True)
os.makedirs(DEPARTMENTS_DIR, exist_ok=True)

departments = [
    {"id": 1, "slug": "cardiology",       "label": "Cardiology",       "abbr": "CA", "bg": "#0D47A1", "accent": "#0A3880", "light": "#1565C0"},
    {"id": 2, "slug": "neurology",        "label": "Neurology",        "abbr": "NE", "bg": "#1A237E", "accent": "#141a5e", "light": "#283593"},
    {"id": 3, "slug": "pediatrics",       "label": "Pediatrics",       "abbr": "PE", "bg": "#01579B", "accent": "#013f72", "light": "#0277BD"},
    {"id": 4, "slug": "general_medicine", "label": "General Medicine", "abbr": "GM", "bg": "#006064", "accent": "#004a4d", "light": "#00838F"},
]

doctors = [
    {"filename": "dr_ahmed_alrashid",  "initials": "AA", "dept_id": 1},
    {"filename": "dr_sarah_mitchell",  "initials": "SM", "dept_id": 1},
    {"filename": "dr_omar_yildiz",     "initials": "OY", "dept_id": 1},
    {"filename": "dr_layla_hassan",    "initials": "LH", "dept_id": 2},
    {"filename": "dr_james_carter",    "initials": "JC", "dept_id": 2},
    {"filename": "dr_fatima_alzahra",  "initials": "FZ", "dept_id": 2},
    {"filename": "dr_emily_chen",      "initials": "EC", "dept_id": 3},
    {"filename": "dr_hassan_alamin",   "initials": "HA", "dept_id": 3},
    {"filename": "dr_sophia_muller",   "initials": "SM", "dept_id": 3},
    {"filename": "dr_anna_kowalski",   "initials": "AK", "dept_id": 4},
    {"filename": "dr_mehmet_kaya",     "initials": "MK", "dept_id": 4},
    {"filename": "dr_rachel_green",    "initials": "RG", "dept_id": 4},
]

def get_dept(dept_id):
    return next(d for d in departments if d["id"] == dept_id)

def generate_doctor_svg(initials, dept):
    bg     = dept["bg"]
    light  = dept["light"]
    accent = dept["accent"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="100" fill="{bg}"/>
  <circle cx="160" cy="40" r="70" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="28"/>
  <circle cx="100" cy="100" r="90" fill="none" stroke="rgba(255,255,255,0.10)" stroke-width="1.5"/>
  <ellipse cx="100" cy="172" rx="54" ry="9" fill="{accent}" opacity="0.5"/>
  <text x="100" y="108" font-family="Arial, Helvetica, sans-serif" font-size="64" font-weight="700" fill="white" fill-opacity="0.95" text-anchor="middle" dominant-baseline="middle" letter-spacing="5">{initials}</text>
</svg>"""

def generate_department_svg(dept):
    bg     = dept["bg"]
    light  = dept["light"]
    accent = dept["accent"]
    label  = dept["label"]
    abbr   = dept["abbr"]

    words = label.split()
    if len(words) == 1:
        line1, line2 = label, None
    elif len(words) == 2:
        line1, line2 = words[0], words[1]
    else:
        mid   = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])

    if line2:
        name_svg = f"""  <text x="200" y="86" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="white" fill-opacity="0.96" text-anchor="middle" dominant-baseline="middle">{line1}</text>
  <text x="200" y="118" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="white" fill-opacity="0.96" text-anchor="middle" dominant-baseline="middle">{line2}</text>"""
    else:
        name_svg = f"""  <text x="200" y="102" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="white" fill-opacity="0.96" text-anchor="middle" dominant-baseline="middle">{line1}</text>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <rect width="400" height="200" rx="16" fill="{bg}"/>
  <circle cx="370" cy="100" r="90" fill="{light}" fill-opacity="0.30"/>
  <circle cx="370" cy="100" r="60" fill="{light}" fill-opacity="0.20"/>
  <rect x="18" y="18" width="40" height="40" rx="8" fill="rgba(255,255,255,0.15)"/>
  <rect x="34" y="24" width="8" height="28" rx="2" fill="white" fill-opacity="0.9"/>
  <rect x="24" y="34" width="28" height="8" rx="2" fill="white" fill-opacity="0.9"/>
  <text x="38" y="74" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="700" fill="white" fill-opacity="0.70" text-anchor="middle">{abbr}</text>
{name_svg}
  <rect x="120" y="156" width="160" height="2.5" rx="1.5" fill="rgba(255,255,255,0.22)"/>
</svg>"""

print("Generating doctor avatars...")
for doc in doctors:
    dept = get_dept(doc["dept_id"])
    svg  = generate_doctor_svg(doc["initials"], dept)
    path = os.path.join(DOCTORS_DIR, f"{doc['filename']}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  ✓  {doc['filename']}.svg  ({dept['label']})")

print("\nGenerating department icons...")
for dept in departments:
    svg  = generate_department_svg(dept)
    path = os.path.join(DEPARTMENTS_DIR, f"{dept['slug']}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  ✓  {dept['slug']}.svg")

print(f"\nDone.")
print(f"  {len(doctors)} doctor avatars  → {DOCTORS_DIR}/")
print(f"  {len(departments)} department icons → {DEPARTMENTS_DIR}/")