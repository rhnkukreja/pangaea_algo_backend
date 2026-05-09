import requests, pathlib

IMAGES = {
    "lisboans.jpg": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=800",
    "palmares.jpg": "https://images.unsplash.com/photo-1587502537745-84b86da1204f?w=800",
    "luxeasy.jpg":  "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
    "amoreiras.jpg":"https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800",
    "greencrest.jpg":"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800",
    "laguna.jpg":   "https://images.unsplash.com/photo-1506665531195-3566af2b4dfa?w=800",
    "hythe.jpg":    "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800",
    "noble.jpg":    "https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=800",
    "monument.jpg": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800",
}

dest = pathlib.Path(__file__).parent / "public"
dest.mkdir(exist_ok=True)

for name, url in IMAGES.items():
    out = dest / name
    if out.exists():
        print(f"Skipping {name} (already exists)")
        continue
    print(f"Downloading {name} ...", end=" ", flush=True)
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    out.write_bytes(r.content)
    print(f"OK ({len(r.content)//1024} KB)")

print("Done.")
