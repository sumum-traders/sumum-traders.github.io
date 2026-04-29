#!/usr/bin/env python3
"""
Sumum Traders LLP website generator.

Produces every HTML page required by the four-batch programme from a single
shared template, varying only the body content per page.
"""
import os, json, html

SITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sumum-site"))
CITIES = [
    ("Tumakuru", "Karnataka", "Home base &mdash; Sumum Traders LLP yard, Kyathsandra"),
    ("Bengaluru", "Karnataka", "High-rise and IT-park projects; principal regional corridor from Tumakuru"),
    ("Chennai", "Tamil Nadu", "Coastal construction with severe exposure; durable binders and CRS rebar demand"),
    ("Hyderabad", "Telangana", "Commercial and institutional RCC frames with ductile-grade reinforcement"),
    ("Coimbatore", "Tamil Nadu", "Industrial sheds and textile units; steel sections and pipe fabrication"),
    ("Kochi", "Kerala", "Severe coastal zone; PSC binders and corrosion-resistant rebar preferred"),
    ("Visakhapatnam", "Andhra Pradesh", "Port and petrochemical works; sulphate-resisting binders and industrial electricals"),
    ("Madurai", "Tamil Nadu", "Temple precinct and commercial RCC; general civil supply"),
    ("Vijayawada", "Andhra Pradesh", "Amaravati corridor civil works and infrastructure pours"),
    ("Thiruvananthapuram", "Kerala", "Government and institutional building; durable-binder specifications"),
    ("Mysuru", "Karnataka", "Heritage-sensitive and institutional work; white cement and finishing lines"),
    ("Tiruchirappalli", "Tamil Nadu", "BHEL-belt heavy-engineering foundations and steel fabrication"),
    ("Salem", "Tamil Nadu", "Steel-plant peripheral work and housing construction"),
    ("Kozhikode", "Kerala", "Coastal residential and commercial RCC; severe-exposure specifications"),
    ("Guntur", "Andhra Pradesh", "Agri-cold-storage and commercial RCC; mixed-use development supply"),
    ("Tirunelveli", "Tamil Nadu", "Wind-farm and infrastructure pours requiring low-heat binders"),
    ("Mangaluru", "Karnataka", "Severe coastal zone III; CRS rebar and PSC binders standard"),
    ("Thrissur", "Kerala", "Gulf-remittance residential and commercial construction"),
    ("Warangal", "Telangana", "Tier-2 growth city; residential and educational construction"),
    ("Nellore", "Andhra Pradesh", "Thermal-power and port-adjacent work with sulphate soils"),
    ("Puducherry", "Puducherry", "Coastal tourism and institutional RCC requiring durability binders"),
    ("Kollam", "Kerala", "Backwater-adjacent construction with moderate-heat PSC and PPC"),
    ("Erode", "Tamil Nadu", "Textile and housing RCC; general civil supply"),
    ("Tirupati", "Andhra Pradesh", "Pilgrim-infrastructure and institutional building"),
    ("Rajahmundry", "Andhra Pradesh", "Godavari-basin bridges and river-front RCC"),
    ("Hubballi-Dharwad", "Karnataka", "Twin-city commercial and housing RCC; mixed demand"),
]

def area_served_jsonld():
    return [{"@type": "City", "name": c[0]} for c in CITIES]

def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Sumum Traders LLP",
        "legalName": "Sumum Traders LLP",
        "identifier": "LLPIN AAE-3987",
        "email": "sumum.traders@gmail.com",
        "foundingDate": "2015-12-17",
        "url": "https://sumum-traders.github.io/",
        "logo": "https://sumum-traders.github.io/assets/og.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Kyathsandra",
            "addressLocality": "Tumakuru",
            "addressRegion": "Karnataka",
            "postalCode": "572104",
            "addressCountry": "IN",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 13.313, "longitude": 77.145},
        "founder": [
            {"@type": "Person", "name": "Syed Sumair"},
            {"@type": "Person", "name": "Syed Umair Ulla"},
            {"@type": "Person", "name": "Maha Jabeen"},
        ],
        "areaServed": area_served_jsonld(),
    }

NAV = """<header class="site-header">
<div class="brand"><a href="index.html">Sumum Traders LLP</a></div>
<nav class="site-nav" aria-label="Primary">
<a href="index.html">Home</a>
<a href="categories.html">Categories</a>
<a href="blog.html">Blog</a>
<a href="technical.html">Technical</a>
<a href="brands.html">Brands</a>
<a href="faq.html">FAQ</a>
<a href="glossary.html">Glossary</a>
<a href="contact.html">Contact</a>
</nav>
</header>"""

FOOTER = """<footer class="site-footer">
<p>Sumum Traders LLP &middot; LLPIN AAE-3987 &middot; Kyathsandra, Tumakuru, Karnataka 572104 &middot; <a href="mailto:sumum.traders@gmail.com">sumum.traders@gmail.com</a></p>
<p>Designated partners: Syed Sumair, Syed Umair Ulla and Maha Jabeen. Incorporated 17 December 2015 with the Registrar of Companies, Bangalore.</p>
</footer>"""

def footprint_section():
    rows = "\n".join(
        f"<tr><td>{c}</td><td>{s}</td><td>{r}</td></tr>" for c, s, r in CITIES
    )
    return f"""<section id="footprint">
<h2>South India service footprint</h2>
<table>
<caption>South India cities we regularly serve</caption>
<thead><tr><th>City</th><th>State or UT</th><th>Relevance</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</section>"""

def contact_cta():
    return """<section class="contact-cta" id="contact">
<h2>Contact Sumum Traders LLP</h2>
<p>For a quote, a BOQ review or a site despatch, write to <a href="mailto:sumum.traders@gmail.com">sumum.traders@gmail.com</a>. The Kyathsandra yard sits at <a href="https://www.google.com/maps/search/?api=1&amp;query=13.313,77.145" target="_blank" rel="noopener noreferrer">13.313 N, 77.145 E</a> on Google Maps.</p>
</section>"""

def head(title, desc, filename, og_type="article", extra_jsonld=None):
    canonical = f"https://sumum-traders.github.io/{filename}"
    blocks = [
        json.dumps(org_jsonld(), separators=(",", ":")),
        json.dumps({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "url": canonical,
            "inLanguage": "en",
        }, separators=(",", ":")),
    ]
    if extra_jsonld:
        for b in extra_jsonld:
            blocks.append(json.dumps(b, separators=(",", ":")))
    jsonld_html = "\n".join(
        f'<script type="application/ld+json">{b}</script>' for b in blocks
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#ffffff">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/assets/styles.css">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Sumum Traders LLP">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://sumum-traders.github.io/assets/og.png">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://sumum-traders.github.io/assets/og.png">
<meta name="geo.region" content="IN-KA">
<meta name="geo.placename" content="Tumakuru, Karnataka">
<meta name="geo.position" content="13.313;77.145">
<meta name="ICBM" content="13.313, 77.145">
{jsonld_html}
</head>
<body>
{NAV}
<main>"""

def breadcrumb(items):
    parts = []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f"<span>{label}</span>")
    return '<nav aria-label="Breadcrumb">' + " &rsaquo; ".join(parts) + "</nav>"

def breadcrumb_jsonld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             "item": f"https://sumum-traders.github.io/{href}" if href else ""}
            for i, (label, href) in enumerate(items)
        ],
    }

def close_page():
    return f"{footprint_section()}\n{contact_cta()}\n</main>\n{FOOTER}\n</body>\n</html>\n"

def write(filename, content):
    path = os.path.join(SITE, filename)
    os.makedirs(os.path.dirname(path) if "/" in filename else SITE, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return len(content)

os.makedirs(SITE, exist_ok=True)
os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
print("Generator loaded.")
