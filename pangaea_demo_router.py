from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

router = APIRouter()

PROPERTIES = {
  "the_lisboans": {
    "project_name": "The Lisboans",
    "country": "Portugal",
    "city": "Lisbon",
    "flag": "🇵🇹",
    "image": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=800",
    "developer": "Oxy Capital",
    "price_range": "€450K – €2.5M",
    "project_type": "Mixed-use",
    "project_stage": "Ready to Move",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "5.5% – 7%",
    "highlight": "Premium hospitality-lifestyle residences in Lisbon's historic core",
    "description": "The Lisboans is a landmark hospitality-residential concept in Alfama, Lisbon's oldest and most iconic district. Developed by Oxy Capital, the project blends boutique hotel services with private residential ownership, offering investors a rare combination of lifestyle asset and Golden Visa eligibility. Located steps from Praça do Comércio and the Tagus riverfront, residents enjoy 5-star amenities, concierge services, and direct access to Lisbon's most sought-after cultural and dining destinations.",
    "specs": [
      { "label": "Location", "value": "Alfama / Baixa-Chiado, Lisbon" },
      { "label": "Developer", "value": "Oxy Capital" },
      { "label": "Units Available", "value": "15 of 20" },
      { "label": "Completion", "value": "December 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — eligible" },
      { "label": "Rental Yield", "value": "5.5% – 7% estimated" },
      { "label": "Price Range", "value": "€450,000 – €2,500,000" }
    ],
    "tags": ["Golden Visa eligible", "Within budget", "Schools & hospitals nearby", "Ready to move in"],
    "match_score": 94,
    "rank": 1,
    "score_reasons": [
      "Portugal matches your geographic preference",
      "Golden Visa program satisfies mandatory residency requirement",
      "Ready-to-move suits conservative timeline",
      "Schools and hospitals within walking distance"
    ]
  },
  "palmares": {
    "project_name": "Palmares Ocean Living & Golf Resort",
    "country": "Portugal",
    "city": "Algarve",
    "flag": "🇵🇹",
    "image": "http://localhost:8000/public/palmares.jpg",
    "developer": "Oxy Capital",
    "price_range": "$199K – $1.1M",
    "project_type": "Mixed-use Resort",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "4% – 6%",
    "highlight": "Golf resort residences on the Algarve coast with Golden Visa access",
    "description": "Palmares Ocean Living & Golf Resort occupies a spectacular position on the Algarve coast near Lagos, set within a world-class golf resort overlooking Meia Praia beach and the Alvor estuary. Developed by Oxy Capital, the project offers branded resort residences with full property management, rental pooling, and Golden Visa eligibility. Algarve's status as Europe's premier golf and lifestyle destination makes this a high-conviction hold for families seeking residency with strong leisure upside.",
    "specs": [
      { "label": "Location", "value": "Lagos / Meia Praia, Algarve" },
      { "label": "Developer", "value": "Oxy Capital" },
      { "label": "Units Available", "value": "450 of 500" },
      { "label": "Completion", "value": "June 2027" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — eligible" },
      { "label": "Rental Yield", "value": "4% – 6% estimated" },
      { "label": "Price Range", "value": "$199,000 – $1,100,000" }
    ],
    "tags": ["Golden Visa eligible", "Resort lifestyle", "Under construction upside", "Algarve coastal"],
    "match_score": 88,
    "rank": 2,
    "score_reasons": [
      "Portugal matches your geographic preference",
      "Golden Visa program satisfies mandatory residency requirement",
      "Resort-managed structure suits family lifestyle",
      "Lowest entry point in the Portuguese Golden Visa market"
    ] 
  },
  "luxeasy": {
    "project_name": "LUX&EASY Thessaloniki",
    "country": "Greece",
    "city": "Thessaloniki",
    "flag": "🇬🇷",
    "image": "http://localhost:8000/public/luxeasy.jpg",
    "developer": "NOVA CONSTRUCTIONS S.A.",
    "price_range": "€120K – €240K",
    "project_type": "Residential",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "5% – 6.5%",
    "highlight": "High-volume branded residences with strong Greek Golden Visa pathway",
    "description": "LUX&EASY Thessaloniki is a large-scale branded residential development by NOVA CONSTRUCTIONS S.A. in Greece's second-largest city. With over 2,300 units across the Thessaloniki Metropolitan Area, the project offers the lowest entry point into the Greek Golden Visa program at €120,000 — well below Athens pricing. Thessaloniki's growing international student population, strong rental demand, and improving transport infrastructure make this a compelling yield-and-residency combination for conservative family investors.",
    "specs": [
      { "label": "Location", "value": "Thessaloniki Metropolitan Area, Greece" },
      { "label": "Developer", "value": "NOVA CONSTRUCTIONS S.A." },
      { "label": "Units Available", "value": "2,141 of 2,300" },
      { "label": "Completion", "value": "March 2027" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — eligible from €120K" },
      { "label": "Rental Yield", "value": "5% – 6.5% estimated" },
      { "label": "Price Range", "value": "€120,000 – €240,000" }
    ],
    "tags": ["Golden Visa eligible", "Lowest entry point", "Central urban location", "Family infrastructure nearby"],
    "match_score": 85,
    "rank": 3,
    "score_reasons": [
      "Greece matches your geographic preference",
      "Golden Visa program satisfies mandatory residency requirement",
      "Lowest entry point in EU Golden Visa market",
      "Urban infrastructure with schools and hospitals nearby"
    ]
  },
  "amoreiras": {
    "project_name": "Amoreiras Prime Residences",
    "country": "Portugal",
    "city": "Lisbon",
    "flag": "🇵🇹",
    "image": "http://localhost:8000/public/amoreiras.jpg",
    "developer": "Vanguard Properties",
    "price_range": "€750K – €3.5M",
    "project_type": "Residential",
    "project_stage": "Ready to Move",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "4.5% – 6%",
    "highlight": "Landmark luxury development in Lisbon's most connected neighbourhood",
    "description": "Amoreiras Prime Residences is a landmark luxury development by Vanguard Properties in the heart of Lisbon's Amoreiras district — home to the Amoreiras Shopping Centre, the Lycée Français Charles Lepierre, and direct access to the Marquês de Pombal business corridor. With only 34 units across a boutique building, the project offers genuine scarcity value, Golden Visa eligibility, and the Vanguard brand guarantee. Ideal for families seeking a premium primary residence with top international school access.",
    "specs": [
      { "label": "Location", "value": "Amoreiras, Lisbon" },
      { "label": "Developer", "value": "Vanguard Properties" },
      { "label": "Units Available", "value": "25 of 34" },
      { "label": "Completion", "value": "December 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — eligible" },
      { "label": "Rental Yield", "value": "4.5% – 6% estimated" },
      { "label": "Price Range", "value": "€750,000 – €3,500,000" }
    ],
    "tags": ["Golden Visa eligible", "French school nearby", "Business district access", "Vanguard luxury brand"],
    "match_score": 82,
    "rank": 4,
    "score_reasons": [
      "Portugal matches your geographic preference",
      "Golden Visa program satisfies mandatory residency requirement",
      "International school (Lycée Français) within walking distance",
      "Ready-to-move suits conservative timeline"
    ]
  },
  "greencrest": {
    "project_name": "Greencrest at Dubai Hills Estate",
    "country": "UAE",
    "city": "Dubai",
    "flag": "🇦🇪",
    "image": "http://localhost:8000/public/greencrest.jpg",
    "developer": "Emaar Properties",
    "price_range": "$1.57M – $3.89M",
    "project_type": "Residential",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "6.5%",
    "highlight": "Emaar luxury residences in Dubai Hills with 6.5% yield and UAE Golden Visa",
    "description": "Greencrest at Dubai Hills Estate is an Emaar Properties development within the master-planned Dubai Hills community — one of Dubai's most family-oriented and infrastructure-rich addresses. The project sits adjacent to King's College Hospital London Dubai, GEMS International School, and Dubai Hills Mall, making it the highest-scoring UAE option for conservative family investors seeking portfolio diversification. UAE's 0% capital gains tax and 0% annual property tax environment adds meaningful after-tax yield advantage.",
    "specs": [
      { "label": "Location", "value": "Dubai Hills Estate, MBR City" },
      { "label": "Developer", "value": "Emaar Properties" },
      { "label": "Units Available", "value": "20 of 195" },
      { "label": "Completion", "value": "June 2029" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — UAE Golden Visa eligible" },
      { "label": "Rental Yield", "value": "6.5% estimated" },
      { "label": "Price Range", "value": "$1,570,000 – $3,890,000" }
    ],
    "tags": ["6.5% rental yield", "UAE Golden Visa", "King's College Hospital nearby", "Emaar brand", "0% capital gains tax"],
    "match_score": 76,
    "rank": 5,
    "score_reasons": [
      "Conservative UAE stability bonus for portfolio diversification",
      "Golden Visa eligible — UAE residency pathway",
      "King's College Hospital and GEMS school on doorstep",
      "Emaar track record reduces developer risk"
    ]
  },
  "laguna": {
    "project_name": "Laguna Lakelands",
    "country": "Thailand",
    "city": "Phuket",
    "flag": "🇹🇭",
    "image": "http://localhost:8000/public/laguna.jpg",
    "developer": "Banyan Group",
    "price_range": "$6.8M – $60M",
    "project_type": "Mixed-use Resort",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": False,
    "rental_yield": "7% – 10%",
    "highlight": "Banyan Group integrated resort residences with professional rental management",
    "description": "Laguna Lakelands is the flagship development within Laguna Phuket — Asia's most successful integrated resort destination, developed and operated by Banyan Group over 30+ years. The mixed-use project combines villa and condo residences with a world-class golf course, beach club, spa, and hotel infrastructure. Professional rental management through Banyan's hospitality arm delivers institutional-grade yield. For opportunistic yield hunters, this is the highest-conviction Thailand play: brand, management, location, and upside in a single asset.",
    "specs": [
      { "label": "Location", "value": "Bang Tao / Laguna Phuket, Phuket" },
      { "label": "Developer", "value": "Banyan Group" },
      { "label": "Units Available", "value": "210 of 6,000" },
      { "label": "Completion", "value": "March 2027" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Not applicable" },
      { "label": "Rental Yield", "value": "7% – 10% estimated" },
      { "label": "Price Range", "value": "$6,800,000 – $60,000,000" }
    ],
    "tags": ["Mixed-use yield play", "Banyan Group managed", "Under construction upside", "Airport & beach access"],
    "match_score": 91,
    "rank": 1,
    "score_reasons": [
      "Thailand matches your geographic preference",
      "Mixed-use structure maximises yield for cash flow investors",
      "Under construction stage suits opportunistic risk appetite",
      "Banyan rental management removes operational burden"
    ]
  },
  "hythe": {
    "project_name": "HYTHE by Botanica",
    "country": "Thailand",
    "city": "Phuket",
    "flag": "🇹🇭",
    "image": "http://localhost:8000/public/hythe.jpg",
    "developer": "Botanica Luxury Phuket Co., Ltd.",
    "price_range": "$10.8M – $165M",
    "project_type": "Residential Villas",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": False,
    "rental_yield": "6% – 9%",
    "highlight": "Ultra-luxury Phuket villas by Botanica with 20+ year development track record",
    "description": "HYTHE by Botanica is an ultra-luxury villa development in Cherngtalay, Phuket's most exclusive residential enclave within Laguna Phuket. Developed by Botanica Luxury — with 20+ years and 15+ delivered projects in Phuket — HYTHE targets high-net-worth investors seeking a trophy lifestyle asset with strong short-term rental upside. Proximity to Bang Tao Beach, Layan Beach, Porto de Phuket, and Phuket International Airport ensures year-round occupancy from the premium international tourist segment.",
    "specs": [
      { "label": "Location", "value": "Cherngtalay / Laguna Phuket, Phuket" },
      { "label": "Developer", "value": "Botanica Luxury Phuket Co., Ltd." },
      { "label": "Units Available", "value": "21 of 276" },
      { "label": "Completion", "value": "December 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Not applicable" },
      { "label": "Rental Yield", "value": "6% – 9% estimated" },
      { "label": "Price Range", "value": "$10,800,000 – $165,000,000" }
    ],
    "tags": ["Phuket luxury villas", "Under construction upside", "20+ year track record", "Beach club proximity"],
    "match_score": 84,
    "rank": 2,
    "score_reasons": [
      "Thailand matches your geographic preference",
      "Under construction stage suits opportunistic risk appetite",
      "Botanica track record: 20+ years, 15+ delivered Phuket projects",
      "Beach and airport proximity drives premium rental occupancy"
    ]
  },
  "noble": {
    "project_name": "Noble Ploenchit",
    "country": "Thailand",
    "city": "Bangkok",
    "flag": "🇹🇭",
    "image": "http://localhost:8000/public/noble.jpg",
    "developer": "Noble Development Public Co., Ltd.",
    "price_range": "$8.5M – $185M",
    "project_type": "Residential",
    "project_stage": "Ready to Move",
    "ownership": "Freehold",
    "golden_visa": False,
    "rental_yield": "5% – 7%",
    "highlight": "Bangkok CBD premium residential with direct BTS access and strong resale liquidity",
    "description": "Noble Ploenchit occupies one of Bangkok's most coveted residential addresses — Phloen Chit Road in Lumphini, Pathum Wan — directly connected to BTS Phloen Chit Station. Developed by Noble Development, a publicly listed Thai developer with multiple delivered projects across Bangkok, the building provides direct access to Central Embassy, Central Chidlom, and Siam Paragon. For yield investors, Bangkok CBD condos at this location command premium rental rates from international executives and diplomats year-round.",
    "specs": [
      { "label": "Location", "value": "Phloen Chit Road, Lumphini, Bangkok" },
      { "label": "Developer", "value": "Noble Development Public Co., Ltd." },
      { "label": "Units Available", "value": "1,223 of 1,444" },
      { "label": "Completion", "value": "December 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Not applicable" },
      { "label": "Rental Yield", "value": "5% – 7% estimated" },
      { "label": "Price Range", "value": "$8,500,000 – $185,000,000" }
    ],
    "tags": ["BTS direct access", "Bangkok CBD", "Premium residential asset", "Strong resale liquidity"],
    "match_score": 78,
    "rank": 3,
    "score_reasons": [
      "Thailand matches your geographic preference",
      "CBD location drives premium rental demand from expats and executives",
      "BTS direct access — highest liquidity corridor in Bangkok",
      "Listed developer with strong delivery track record"
    ]
  },
  "monument": {
    "project_name": "The Monument Thong Lo",
    "country": "Thailand",
    "city": "Bangkok",
    "flag": "🇹🇭",
    "image": "http://localhost:8000/public/monument.jpg",
    "developer": "Sansiri",
    "price_range": "$30M – $150M",
    "project_type": "Residential",
    "project_stage": "Ready to Move",
    "ownership": "Freehold",
    "golden_visa": False,
    "rental_yield": "4% – 6%",
    "highlight": "Sansiri ultra-luxury in Thong Lo — Bangkok's most prestigious lifestyle address",
    "description": "The Monument Thong Lo is Sansiri's flagship ultra-luxury residential tower on Sukhumvit 55, Bangkok's most prestigious lifestyle corridor. Thong Lo commands the highest rental rates in Bangkok from Japanese expats, senior executives, and high-net-worth short-term tenants. Developed by Sansiri — Thailand's most recognised listed developer with 30+ years and hundreds of delivered projects — The Monument represents the apex of Bangkok residential investment: brand, location, and scarcity in one asset.",
    "specs": [
      { "label": "Location", "value": "Thong Lo (Sukhumvit 55), Watthana, Bangkok" },
      { "label": "Developer", "value": "Sansiri" },
      { "label": "Units Available", "value": "10 of 127" },
      { "label": "Completion", "value": "June 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Not applicable" },
      { "label": "Rental Yield", "value": "4% – 6% estimated" },
      { "label": "Price Range", "value": "$30,000,000 – $150,000,000" }
    ],
    "tags": ["Thong Lo prestige", "Ultra-luxury", "Sansiri flagship", "Only 10 units remaining"],
    "match_score": 72,
    "rank": 4,
    "score_reasons": [
      "Thailand matches your geographic preference",
      "Thong Lo commands Bangkok's highest per-sqm rental rates",
      "Sansiri brand reduces execution risk",
      "Only 10 units remaining — genuine scarcity"
    ]
  },
  "infante": {
    "project_name": "Infante Residences",
    "country": "Portugal",
    "city": "Lisbon",
    "flag": "🇵🇹",
    "image": "http://localhost:8000/public/infante.jpg",
    "developer": "Vanguard Properties",
    "price_range": "€399K – €1.01M",
    "project_type": "Residential",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": False,
    "rental_yield": "6%",
    "highlight": "Rehabilitation condominium development in Lisbon's central district",
    "description": "Infante Residences is a rehabilitation condominium development located in the Estrela / Avenida Infante Santo area of Lisbon[cite: 1]. Developed by Vanguard Properties, the project is situated near Jardim da Estrela, LX Factory, Amoreiras, and Hospital CUF Tejo[cite: 1].",
    "specs": [
      { "label": "Location", "value": "Estrela / Avenida Infante Santo, Lisbon" },
      { "label": "Developer", "value": "Vanguard Properties" },
      { "label": "Units Available", "value": "41 of 45" },
      { "label": "Completion", "value": "September 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Not applicable" },
      { "label": "Rental Yield", "value": "6% estimated" },
      { "label": "Price Range", "value": "€399,000 – €1,015,000" }
    ],
    "tags": ["Central location", "Rehabilitation project", "Hospitals nearby"],
    "match_score": 80,
    "rank": 1,
    "score_reasons": [
      "Portugal matches geographic preference",
      "Central access to public transit and embassies",
      "Established developer track record"
    ]
  },
  "one_athens": {
    "project_name": "One Athens",
    "country": "Greece",
    "city": "Athens",
    "flag": "🇬🇷",
    "image": "http://localhost:8000/public/one_athens.jpg",
    "developer": "DIMAND",
    "price_range": "€200K – €4.5M",
    "project_type": "Residential",
    "project_stage": "Ready to Move",
    "ownership": "Freehold",
    "golden_visa": False,
    "rental_yield": "N/A",
    "highlight": "Ready-to-move residential redevelopment in central Athens",
    "description": "One Athens is a residential redevelopment project delivered by DIMAND[cite: 2]. Located in Kolonaki / Athens City Centre, it offers central proximity to the Athens Concert Hall, embassies, luxury retail, and museums[cite: 2].",
    "specs": [
      { "label": "Location", "value": "Kolonaki / Athens City Centre, Athens" },
      { "label": "Developer", "value": "DIMAND" },
      { "label": "Units Available", "value": "180 of 200" },
      { "label": "Completion", "value": "March 2027" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Not applicable" },
      { "label": "Rental Yield", "value": "N/A" },
      { "label": "Price Range", "value": "€200,000 – €4,500,000" }
    ],
    "tags": ["Ready to move in", "City centre", "Luxury retail access"],
    "match_score": 75,
    "rank": 2,
    "score_reasons": [
      "Greece matches geographic preference",
      "Ready-to-move status suits immediate timelines",
      "Prime central location near cultural landmarks"
    ]
  },
  "ellinikon": {
    "project_name": "The Ellinikon – Marina Residences",
    "country": "Greece",
    "city": "Athens",
    "flag": "🇬🇷",
    "image": "http://localhost:8000/public/ellinikon.jpg",
    "developer": "LAMDA Development",
    "price_range": "€1M – €20M",
    "project_type": "Residential",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": False,
    "rental_yield": "N/A",
    "highlight": "Luxury waterfront living within Europe's largest urban regeneration project",
    "description": "The Ellinikon – Marina Residences is part of The Ellinikon masterplan, a massive urban regeneration project led by LAMDA Development[cite: 2, 3]. It provides luxury living on the Athens Riviera coastline, closely situated to the Ellinikon Metropolitan Park, Riviera Galleria, and local marinas[cite: 3].",
    "specs": [
      { "label": "Location", "value": "Elliniko / Agios Kosmas Marina, Athens" },
      { "label": "Developer", "value": "LAMDA Development" },
      { "label": "Units Available", "value": "178 of 200" },
      { "label": "Completion", "value": "June 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Not applicable" },
      { "label": "Rental Yield", "value": "N/A" },
      { "label": "Price Range", "value": "€1,000,000 – €20,000,000" }
    ],
    "tags": ["Waterfront", "Master-planned community", "Under construction"],
    "match_score": 85,
    "rank": 3,
    "score_reasons": [
      "Greece matches geographic preference",
      "Strong upside potential from large-scale urban regeneration",
      "Prime waterfront positioning on the Athens Riviera"
    ]
  },
  "sobha_hartland": {
    "project_name": "Sobha Hartland",
    "country": "UAE",
    "city": "Dubai",
    "flag": "🇦🇪",
    "image": "http://localhost:8000/public/sobha_hartland.jpg",
    "developer": "Sobha Realty",
    "price_range": "$1.2M – $85M",
    "project_type": "Mixed-use",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "6.5%",
    "highlight": "Central luxury mixed-use community in Mohammed Bin Rashid City",
    "description": "Sobha Hartland is a master-planned development by Sobha Realty in Mohammed Bin Rashid City (MBR City), Dubai[cite: 11]. It offers freehold ownership for foreign investors and is centrally located near Downtown Dubai, Burj Khalifa, and Hartland International School[cite: 11].",
    "specs": [
      { "label": "Location", "value": "Mohammed Bin Rashid City (MBR City), Dubai" },
      { "label": "Developer", "value": "Sobha Realty" },
      { "label": "Units Available", "value": "9 of 200" },
      { "label": "Completion", "value": "June 2027" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — UAE Golden Visa eligible" },
      { "label": "Rental Yield", "value": "6.5% estimated" },
      { "label": "Price Range", "value": "$1,200,000 – $85,000,000" }
    ],
    "tags": ["Central location", "UAE Golden Visa", "Schools nearby"],
    "match_score": 88,
    "rank": 4,
    "score_reasons": [
      "UAE stability bonus for portfolio diversification",
      "Golden Visa eligible for UAE residency",
      "Top-tier international schools within the community"
    ]
  },
  "burj_binghatti": {
    "project_name": "Burj Binghatti Jacob & Co Residences",
    "country": "UAE",
    "city": "Dubai",
    "flag": "🇦🇪",
    "image": "http://localhost:8000/public/burj_binghatti.jpg",
    "developer": "Binghatti Developers",
    "price_range": "$8.2M – $752M",
    "project_type": "Residential",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "N/A",
    "highlight": "Ultra-luxury branded residences in Business Bay",
    "description": "Burj Binghatti Jacob & Co Residences is an ultra-luxury residential tower developed by Binghatti Developers in collaboration with the Jacob & Co brand[cite: 11]. Located in Business Bay, it provides central access to Burj Khalifa, Dubai Mall, and the Dubai Opera[cite: 11].",
    "specs": [
      { "label": "Location", "value": "Business Bay, Dubai" },
      { "label": "Developer", "value": "Binghatti Developers" },
      { "label": "Units Available", "value": "40 of 299" },
      { "label": "Completion", "value": "June 2026" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — UAE Golden Visa eligible" },
      { "label": "Rental Yield", "value": "N/A" },
      { "label": "Price Range", "value": "$8,200,000 – $752,000,000" }
    ],
    "tags": ["Branded residences", "Ultra-luxury", "UAE Golden Visa"],
    "match_score": 70,
    "rank": 5,
    "score_reasons": [
      "Trophy asset status for high-net-worth portfolios",
      "Golden Visa eligible for UAE residency",
      "Close proximity to primary business district"
    ]
  },
  "damac_islands": {
    "project_name": "DAMAC Islands",
    "country": "UAE",
    "city": "Dubai",
    "flag": "🇦🇪",
    "image": "http://localhost:8000/public/damac_islands.jpg",
    "developer": "DAMAC Properties",
    "price_range": "$2.25M – $9.5M",
    "project_type": "Mixed-use",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "N/A",
    "highlight": "Emerging mixed-use community with waterfront lagoons in Dubailand",
    "description": "DAMAC Islands is an emerging mixed-use master community located in Dubailand near DAMAC Sun City[cite: 12]. Developed by DAMAC Properties, the development centers around waterfront lagoons and resort amenities with strong connectivity to Emirates Road (E611)[cite: 12].",
    "specs": [
      { "label": "Location", "value": "Dubailand, Dubai" },
      { "label": "Developer", "value": "DAMAC Properties" },
      { "label": "Units Available", "value": "45 of 200" },
      { "label": "Completion", "value": "December 2028" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — UAE Golden Visa eligible" },
      { "label": "Rental Yield", "value": "N/A" },
      { "label": "Price Range", "value": "$2,250,000 – $9,500,000" }
    ],
    "tags": ["Waterfront community", "Resort lifestyle", "UAE Golden Visa"],
    "match_score": 79,
    "rank": 6,
    "score_reasons": [
      "Emerging location offers capital appreciation potential",
      "Golden Visa eligible for UAE residency",
      "Established mega-developer execution"
    ]
  },
  "dubai_creek": {
    "project_name": "Dubai Creek Harbour",
    "country": "UAE",
    "city": "Dubai",
    "flag": "🇦🇪",
    "image": "http://localhost:8000/public/dubai_creek.jpg",
    "developer": "Emaar Properties",
    "price_range": "$1.2M – $15M",
    "project_type": "Mixed-use",
    "project_stage": "Under Construction",
    "ownership": "Freehold",
    "golden_visa": True,
    "rental_yield": "6.5%",
    "highlight": "Emaar's massive waterfront masterplan offering strong rental yields",
    "description": "Dubai Creek Harbour is a major master-planned community by Emaar Properties located in the Ras Al Khor area[cite: 14]. This emerging mixed-use development offers residents access to Creek Marina, Creek Beach, and the Ras Al Khor Wildlife Sanctuary, all while remaining 10-15 minutes from Downtown Dubai[cite: 14].",
    "specs": [
      { "label": "Location", "value": "Dubai Creek Harbour (The Lagoons), Dubai" },
      { "label": "Developer", "value": "Emaar Properties" },
      { "label": "Units Available", "value": "12,000 of 48,500" },
      { "label": "Completion", "value": "December 2028" },
      { "label": "Ownership", "value": "Freehold" },
      { "label": "Golden Visa", "value": "Yes — UAE Golden Visa eligible" },
      { "label": "Rental Yield", "value": "6.5% estimated" },
      { "label": "Price Range", "value": "$1,200,000 – $15,000,000" }
    ],
    "tags": ["Emaar brand", "Waterfront", "6.5% rental yield", "UAE Golden Visa"],
    "match_score": 83,
    "rank": 7,
    "score_reasons": [
      "Emaar track record significantly reduces execution risk",
      "Golden Visa eligible for UAE residency",
      "0% capital gains tax and tax-free rental income in UAE"
    ]
  }
}


# ─── PROFILE DEFINITIONS ─────────────────────────────────────────────────────

PROFILE_1 = {
  "profile_id": "profile_1",
  "profile_name": "Conservative EU Residency Family",
  "survey_answers": {
    "q1": "< 15 Crore", "q2": "Residency",
    "q3": "Medium term (6–24 months)", "q4": "Long (>10 years)",
    "q5": "Mandatory", "q6": "Optional", "q7": "Freehold",
    "q8": "Conservative", "q9": ["Apartments", "Branded residence"],
    "q10": "Primary relocation", "q11": "Family with children",
    "q12": "Owns domestic real estate but not international",
    "q13": ["Portugal", "Greece"], "q14": ["Schools / hospitals", "Airport connectivity"],
    "q15": "High (trophy assets, global brands)"
  },
  "funnel_steps": [
    {
      "label": "Applying budget & legal filters",
      "from_count": 16, "to_count": 11, "eliminated_count": 5,
      "eliminated_names": ["The Monument Thong Lo", "HYTHE by Botanica", "Noble Ploenchit", "Burj Binghatti Jacob & Co Residences", "The Ellinikon – Marina Residences"]
    },
    {
      "label": "Matching geography & residency requirements",
      "from_count": 11, "to_count": 6, "eliminated_count": 5,
      "eliminated_names": ["Sobha Hartland", "DAMAC Islands", "Dubai Creek Harbour", "Laguna Lakelands", "One Athens"]
    },
    {
      "label": "Ranking by lifestyle & proximity fit",
      "from_count": 6, "to_count": 5, "eliminated_count": 1,
      "eliminated_names": ["Infante Residences"]
    }
  ],
  "top_matches": [
    PROPERTIES["the_lisboans"],
    PROPERTIES["palmares"],
    PROPERTIES["luxeasy"],
    PROPERTIES["amoreiras"],
    PROPERTIES["greencrest"]
  ]
}

PROFILE_2 = {
  "profile_id": "profile_2",
  "profile_name": "Aggressive Thailand Yield Hunter",
  "survey_answers": {
    "q1": "< 15 Crore", "q2": "Yield / Cash Flow",
    "q3": "Immediate (0–6 months)", "q4": "Medium (5–10 years)",
    "q5": "Optional", "q6": "Not required", "q7": "Doesn't Matter",
    "q8": "Opportunistic", "q9": ["Villas", "Income-generating (rental-managed)"],
    "q10": "Pure investment", "q11": "Single / couple",
    "q12": "Experienced international investor",
    "q13": ["Thailand"], "q14": ["Airport connectivity", "CBD / leisure proximity"],
    "q15": "Medium"
  },
  "funnel_steps": [
    {
      "label": "Applying budget & yield filters",
      "from_count": 16, "to_count": 10, "eliminated_count": 6,
      "eliminated_names": ["The Monument Thong Lo", "HYTHE by Botanica", "Noble Ploenchit", "Burj Binghatti Jacob & Co Residences", "The Ellinikon – Marina Residences", "Amoreiras Prime Residences"]
    },
    {
      "label": "Matching geography & investment objective",
      "from_count": 10, "to_count": 5, "eliminated_count": 5,
      "eliminated_names": ["The Lisboans", "Infante Residences", "LUX&EASY Thessaloniki", "One Athens", "Palmares Ocean Living & Golf Resort"]
    },
    {
      "label": "Ranking by yield potential & market access",
      "from_count": 5, "to_count": 4, "eliminated_count": 1,
      "eliminated_names": ["Greencrest at Dubai Hills Estate"]
    }
  ],
  "top_matches": [
    PROPERTIES["laguna"],
    PROPERTIES["hythe"],
    PROPERTIES["noble"],
    PROPERTIES["monument"]
  ]
}

# ─── REQUEST / DETECTION ──────────────────────────────────────────────────────

class MatchRequest(BaseModel):
  q1: Any = None
  q2: Any = None
  q3: Any = None
  q4: Any = None
  q5: Any = None
  q6: Any = None
  q7: Any = None
  q8: Any = None
  q9: Any = None
  q10: Any = None
  q11: Any = None
  q12: Any = None
  q13: Any = None
  q14: Any = None
  q15: Any = None
  answers: Any = None


def detect_profile(req: MatchRequest) -> dict:
  if req.answers and isinstance(req.answers, dict):
    q5 = req.answers.get("q5", "")
    q8 = req.answers.get("q8", "")
    q13 = req.answers.get("q13", [])
  else:
    q5 = req.q5 or ""
    q8 = req.q8 or ""
    q13 = req.q13 or []

  if isinstance(q13, str):
    q13 = [q13]

  eu_countries = {"Portugal", "Greece", "portugal", "greece", "PT", "GR"}
  if any(c in eu_countries for c in q13) and str(q5).lower() in ["mandatory", "yes"]:
    return PROFILE_1
  if any(c in ["Thailand", "thailand", "TH"] for c in q13) and str(q8).lower() in ["opportunistic"]:
    return PROFILE_2
  return PROFILE_1


@router.post("/api/match")
def match(req: MatchRequest):
  return detect_profile(req)


@router.post("/api/match/profile")
def match_by_profile_id(body: dict):
  pid = body.get("profile_id", "profile_1")
  return PROFILE_1 if pid == "profile_1" else PROFILE_2
