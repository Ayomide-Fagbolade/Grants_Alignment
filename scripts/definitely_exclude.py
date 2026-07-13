"""List of publishers that should be excluded from crop/agriculture coverage analysis.

The list is organized by category:
1. Sports bodies / sports media
2. Entertainment / celebrity / reality TV
3. Political parties (self‑publishing PR, not independent journalism)
4. Government self‑publishing / official PR channels
"""

DEFINITELY_EXCLUDE = [
    # --- Sports bodies / sports media ---
    "Confederation of African Football (Egypt)",
    "Ghana Football Association (Accra)",
    "South African Football Association (Johannesburg)",
    "Council of Southern African Football Associations (Johannesburg)",
    "South African Sports Confederation and Olympic Committee (Johannesburg)",
    "South African Music Awards",
    "Kickoff (Cape Town)",
    # --- Entertainment / celebrity / reality TV ---
    "Big Brother Africa (Johannesburg)",
    "Big Brother Mzansi (Johannesburg)",
    "Afrotainment Museke Online Music Awards",
    "Showmax (Johannesburg)",
    "African Women in Cinema (Accra)",
    "Afropop Worldwide (New York)",
    # --- Political parties (self‑publishing PR, not independent journalism) ---
    "African National Congress (Johannesburg)",
    "All Progressives Congress (Lagos)",
    "Economic Freedom Fighters (Johannesburg)",
    "Democratic Alliance (Cape Town)",
    "Inkatha Freedom Party (Durban)",
    "Peoples' Democratic Party (Abuja)",
    "Congress of the People (Johannesburg)",
    "Movement for Democratic Change (Harare)",
    # --- Government self‑publishing / official PR channels ---
    "Aso Rock Villa",
]
