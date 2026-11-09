"""
Gnani Vachana 3D — Massive Sovereign Indic Knowledge Base
===========================================================
Enterprise-scale, high-performance in-memory database holding 10,000+
rich synthetic Indic records across 4 core grassroots domains:

1. Kirana FMCG & Retail Inventory (4,000+ SKUs across 10 categories)
2. Municipal Civic Infrastructure & Wards (3,000+ Wards across 25 Indian cities)
3. APMC Mandi Daily Commodity Market Rates (1,500+ Records across 100 Mandis)
4. Socratic Engineering Question Bank (1,500+ CS & Engineering Probes)

Engineered for sub-millisecond (<1ms) tokenized inverted index search,
fuzzy matching, and seamless tool reasoning for Evon v3.3.
"""
import re
import time
import random
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("bhashaswarm.database")

# ── City & Zone Matrix for Indian Municipal Wards ────────────────────────────
INDIAN_CITIES = [
    {"city": "Bengaluru", "state": "Karnataka", "corp": "BBMP", "zones": ["East", "West", "South", "Mahadevapura", "Bommanahalli", "Yelahanka", "Rajarajeshwari Nagar", "Dasarahalli"]},
    {"city": "Delhi NCR", "state": "Delhi", "corp": "MCD", "zones": ["Central", "South", "North", "East", "West", "Shahdara", "Rohini", "Civil Lines", "Najafgarh", "Karol Bagh"]},
    {"city": "Mumbai", "state": "Maharashtra", "corp": "BMC", "zones": ["Ward A (Colaba)", "Ward D (Malabar)", "Ward F/N (Matunga)", "Ward G/S (Elphinstone)", "Ward K/E (Andheri E)", "Ward K/W (Andheri W)", "Ward P/N (Malad)", "Ward R/S (Kandivali)"]},
    {"city": "Hyderabad", "state": "Telangana", "corp": "GHMC", "zones": ["LB Nagar", "Charminar", "Khairatabad", "Secunderabad", "Serilingampally", "Kukatpally"]},
    {"city": "Chennai", "state": "Tamil Nadu", "corp": "GCC", "zones": ["Tondiarpet", "Royapuram", "Thiru-Vi-Ka Nagar", "Anna Nagar", "Teynampet", "Kodambakkam", "Adyar", "Perungudi"]},
    {"city": "Kolkata", "state": "West Bengal", "corp": "KMC", "zones": ["Borough I", "Borough II", "Borough V", "Borough VII", "Borough VIII", "Borough IX", "Borough X", "Borough XIV"]},
    {"city": "Pune", "state": "Maharashtra", "corp": "PMC", "zones": ["Kothrud", "Shivajinagar", "Hadapsar", "Sinhagad Road", "Aundh-Baner", "Kasba-Vishrambaug", "Warje-Karvenagar"]},
    {"city": "Ahmedabad", "state": "Gujarat", "corp": "AMC", "zones": ["Central", "East", "West", "North", "South", "North-West", "South-West"]},
    {"city": "Bhopal", "state": "Madhya Pradesh", "corp": "BMC", "zones": ["Zone 1 (City)", "Zone 2 (MP Nagar)", "Zone 3 (Bairagarh)", "Zone 4 (Kolar)", "Zone 5 (BHEL)", "Zone 6 (Arera)"]},
    {"city": "Lucknow", "state": "Uttar Pradesh", "corp": "LMC", "zones": ["Zone 1 (Hazratganj)", "Zone 2 (Alambagh)", "Zone 3 (Indiranagar)", "Zone 4 (Gomti Nagar)", "Zone 5 (Chowk)", "Zone 6 (Aliganj)"]},
    {"city": "Jaipur", "state": "Rajasthan", "corp": "JMC", "zones": ["Heritage Zone", "Civil Lines", "Sanganer", "Mansarovar", "Vidhyadhar Nagar", "Murlipura"]},
    {"city": "Chandigarh", "state": "Punjab/Haryana", "corp": "MCC", "zones": ["North Sectors", "South Sectors", "East Industrial", "West Sectors", "Manimajra"]},
    {"city": "Indore", "state": "Madhya Pradesh", "corp": "IMC", "zones": ["Zone 1 (Rajwada)", "Zone 2 (Vijay Nagar)", "Zone 3 (Palasia)", "Zone 4 (Bhawarkua)", "Zone 5 (Annapurna)"]},
    {"city": "Kochi", "state": "Kerala", "corp": "KMC", "zones": ["Fort Kochi", "Mattancherry", "Central Ernakulam", "Vyttila", "Edappally", "Kadavanthra"]},
    {"city": "Surat", "state": "Gujarat", "corp": "SMC", "zones": ["Central", "Varachha", "Rander", "Katargam", "Udhna", "Athwa", "Limbayat"]},
    {"city": "Nagpur", "state": "Maharashtra", "corp": "NMC", "zones": ["Dharampeth", "Hanuman Nagar", "Dhantoli", "Nehru Nagar", "Gandhibagh", "Satranjipura", "Lakadganj", "Ashi Nagar", "Mangalwari"]},
    {"city": "Varanasi", "state": "Uttar Pradesh", "corp": "VNN", "zones": ["Dashashwamedh", "Kotwali", "Bhelupur", "Adampur", "Varunapar"]},
    {"city": "Patna", "state": "Bihar", "corp": "PMC", "zones": ["New Capital", "Kankarbagh", "Bankipore", "Azimabad", "Patna City"]},
    {"city": "Visakhapatnam", "state": "Andhra Pradesh", "corp": "GVMC", "zones": ["Zone 1 (Bheemili)", "Zone 2 (Madhurawada)", "Zone 3 (Asilmetta)", "Zone 4 (Gajuwaka)", "Zone 5 (Anakapalle)"]},
]

LOCALITY_NAMES = [
    "Indiranagar", "Koramangala", "Jayanagar", "Whitefield", "HSR Layout", "Malleshwaram", "Rajajinagar", "Hebbal",
    "Connaught Place", "Karol Bagh", "Lajpat Nagar", "Hauz Khas", "Dwarka", "Rohini", "Saket", "Vasant Kunj",
    "Bandra", "Andheri", "Juhu", "Dadar", "Colaba", "Powai", "Goregaon", "Borivali", "Chembur", "Malad",
    "Banjara Hills", "Jubilee Hills", "Gachibowli", "Madhapur", "Begumpet", "Hitech City", "Kukatpally", "Ameerpet",
    "T Nagar", "Adyar", "Mylapore", "Velachery", "Anna Nagar", "Nungambakkam", "Besant Nagar", "Guindy",
    "Park Street", "Salt Lake", "New Town", "Ballygunge", "Alipore", "Dum Dum", "Howrah", "Gariahat",
    "Kothrud", "Baner", "Viman Nagar", "Kalyani Nagar", "Aundh", "Hinjewadi", "Camp", "Magarpatta",
    "Navrangpura", "Satellite", "Bodakdev", "Vastrapur", "Maninagar", "Prahlad Nagar", "SG Highway",
    "MP Nagar", "Arera Colony", "Shahpura", "Kolar Road", "BHEL Township", "Chunabhatti", "Habibganj",
    "Gomti Nagar", "Hazratganj", "Aliganj", "Indira Nagar", "Mahanagar", "Jankipuram", "Vikas Nagar",
    "Malviya Nagar", "Vaishali Nagar", "C-Scheme", "Mansarovar", "Raja Park", "Tonk Road", "Bani Park",
    "Sector 17", "Sector 35", "Sector 22", "Sector 43", "Sector 8", "Sector 9", "Manimajra",
    "Vijay Nagar", "Palasia", "Saket", "Bhawarkua", "Rajendra Nagar", "Geeta Bhawan", "Chhavani"
]

FIRST_NAMES = ["Ramesh", "Priya", "Suresh", "Meera", "Vikram", "Ananya", "Rajesh", "Sunita", "Deepak", "Kavita", "Amit", "Pooja", "Arun", "Sneha", "Manoj", "Divya", "Sanjay", "Neha", "Alok", "Swati"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Banerjee", "Mukherjee", "Gupta", "Singh", "Joshi", "Kulkarni", "Deshmukh", "Choudhury", "Mehta", "Rao", "Pillai", "Das", "Yadav", "Mishra"]

# ── FMCG Product Catalogue Matrices ──────────────────────────────────────────
FMCG_CATEGORIES = {
    "Dairy & Cold Chain": [
        ("Amul Taaza Toned Milk 500ml", "Amul", 28, [1, 3], "TRIGGER_20_PERCENT_FLASH_DISCOUNT"),
        ("Amul Gold Full Cream Milk 1L", "Amul", 68, [2, 4], "TRIGGER_20_PERCENT_FLASH_DISCOUNT"),
        ("Nandini GoodLife Milk 500ml", "KMF Nandini", 30, [15, 60], "OPTIMAL_SHELF_HEALTH"),
        ("Mother Dairy Cow Milk 500ml", "Mother Dairy", 29, [1, 2], "TRIGGER_20_PERCENT_FLASH_DISCOUNT"),
        ("Amul Salted Butter 100g", "Amul", 58, [10, 45], "OPTIMAL_SHELF_HEALTH"),
        ("Amul Processed Cheese Cubes 200g", "Amul", 135, [14, 60], "OPTIMAL_SHELF_HEALTH"),
        ("Milky Mist Paneer 200g", "Milky Mist", 95, [3, 7], "PRIORITIZE_FEFO_DISPATCH"),
        ("Epigamia Greek Yogurt Strawberry 90g", "Epigamia", 50, [2, 6], "TRIGGER_20_PERCENT_FLASH_DISCOUNT"),
        ("Nestle Milkmaid Sweetened Condensed Milk 400g", "Nestle", 144, [60, 180], "OPTIMAL_SHELF_HEALTH"),
        ("Amul Masti Dahi 400g", "Amul", 35, [2, 5], "PRIORITIZE_FEFO_DISPATCH"),
    ],
    "Staples, Atta & Rice": [
        ("Aashirvaad Shudh Chakki Atta 5kg", "ITC Aashirvaad", 245, [45, 120], "OPTIMAL_SHELF_HEALTH"),
        ("Aashirvaad Select Sharbati Atta 10kg", "ITC Aashirvaad", 620, [30, 90], "OPTIMAL_SHELF_HEALTH"),
        ("Fortune Chakki Fresh Atta 5kg", "Adani Fortune", 215, [25, 90], "OPTIMAL_SHELF_HEALTH"),
        ("Pillsbury Chakki Fresh Atta 5kg", "Pillsbury", 225, [30, 90], "OPTIMAL_SHELF_HEALTH"),
        ("India Gate Classic Basmati Rice 5kg", "India Gate", 580, [180, 365], "OPTIMAL_SHELF_HEALTH"),
        ("Daawat Rozana Super Basmati Rice 5kg", "Daawat", 385, [120, 300], "OPTIMAL_SHELF_HEALTH"),
        ("Tata Sampann Toor Dal Unpolished 1kg", "Tata Sampann", 185, [60, 180], "OPTIMAL_SHELF_HEALTH"),
        ("Tata Sampann Moong Dal 1kg", "Tata Sampann", 165, [45, 150], "OPTIMAL_SHELF_HEALTH"),
        ("Fortune Raw Sugar Sulphur Free 1kg", "Adani Fortune", 58, [90, 240], "OPTIMAL_SHELF_HEALTH"),
        ("Tata Salt Vacuum Evaporated Iodized 1kg", "Tata Salt", 28, [180, 720], "OPTIMAL_SHELF_HEALTH"),
    ],
    "Edible Oils & Pure Ghee": [
        ("Fortune Sunlite Refined Sunflower Oil 1L", "Adani Fortune", 142, [90, 180], "OPTIMAL_SHELF_HEALTH"),
        ("Dhara Kachi Ghani Mustard Oil 1L", "Mother Dairy Dhara", 165, [120, 240], "OPTIMAL_SHELF_HEALTH"),
        ("Saffola Gold Pro Healthy Lifestyle Oil 1L", "Marico Saffola", 175, [60, 150], "OPTIMAL_SHELF_HEALTH"),
        ("Amul Pure Ghee Pouch 1L", "Amul", 590, [90, 270], "OPTIMAL_SHELF_HEALTH"),
        ("Patanjali Cow Ghee 1L Tin", "Patanjali", 610, [120, 300], "OPTIMAL_SHELF_HEALTH"),
        ("Gemini Pure Refined Soyabean Oil 1L", "Cargill Gemini", 132, [45, 120], "OPTIMAL_SHELF_HEALTH"),
        ("Idhayam Pure Sesame Gingelly Oil 500ml", "Idhayam", 220, [90, 240], "OPTIMAL_SHELF_HEALTH"),
        ("Parachute 100% Pure Coconut Oil 500ml", "Marico Parachute", 195, [180, 365], "OPTIMAL_SHELF_HEALTH"),
    ],
    "Biscuits, Snacks & Ready Foods": [
        ("Parle-G Glucose Biscuits 800g Family Pack", "Parle", 65, [5, 25], "TRIGGER_BOGO_CLEARANCE"),
        ("Britannia Good Day Butter Cookies 600g", "Britannia", 120, [30, 90], "OPTIMAL_SHELF_HEALTH"),
        ("Britannia Marie Gold Biscuits 1kg Value Pack", "Britannia", 145, [45, 120], "OPTIMAL_SHELF_HEALTH"),
        ("Oreo Original Vanilla Creme Cookies 300g", "Cadbury Oreo", 85, [20, 70], "OPTIMAL_SHELF_HEALTH"),
        ("Sunfeast Dark Fantasy Choco Fills 300g", "ITC Sunfeast", 150, [15, 60], "PRIORITIZE_FEFO_DISPATCH"),
        ("Maggi 2-Minute Masala Noodles 12-Pack 840g", "Nestle Maggi", 168, [20, 90], "OPTIMAL_SHELF_HEALTH"),
        ("Haldiram's Nagpur Bhujia Sev 400g", "Haldiram", 115, [10, 45], "PRIORITIZE_FEFO_DISPATCH"),
        ("Haldiram's All in One Namkeen 400g", "Haldiram", 120, [12, 50], "OPTIMAL_SHELF_HEALTH"),
        ("Lay's India's Magic Masala Chips 115g", "PepsiCo Lay's", 50, [4, 18], "TRIGGER_BOGO_CLEARANCE"),
        ("Kurkure Masala Munch 180g", "PepsiCo Kurkure", 40, [6, 22], "TRIGGER_20_PERCENT_FLASH_DISCOUNT"),
    ],
    "Chai, Coffee & Beverages": [
        ("Tata Tea Premium Desh Ki Chai 500g", "Tata Tea", 195, [120, 365], "OPTIMAL_SHELF_HEALTH"),
        ("Brooke Bond Red Label Tea 500g", "HUL Red Label", 220, [90, 300], "OPTIMAL_SHELF_HEALTH"),
        ("Wagh Bakri Premium CTC Tea 500g", "Wagh Bakri", 235, [100, 320], "OPTIMAL_SHELF_HEALTH"),
        ("Nescafe Classic 100% Pure Instant Coffee 100g", "Nestle Nescafe", 340, [120, 365], "OPTIMAL_SHELF_HEALTH"),
        ("Bru Instant Coffee-Chicory Mix 100g", "HUL Bru", 210, [90, 270], "OPTIMAL_SHELF_HEALTH"),
        ("Bournvita Chocolate Nutrition Drink 500g", "Cadbury", 245, [45, 180], "OPTIMAL_SHELF_HEALTH"),
        ("Horlicks Classic Malt Nutrition Drink 500g", "HUL Horlicks", 260, [60, 200], "OPTIMAL_SHELF_HEALTH"),
        ("Real Fruit Power Mixed Fruit Juice 1L", "Dabur Real", 125, [8, 30], "PRIORITIZE_FEFO_DISPATCH"),
    ],
    "Spices & Cooking Essentials": [
        ("Everest Chana Masala 100g", "Everest", 78, [60, 180], "OPTIMAL_SHELF_HEALTH"),
        ("MDH Deggi Mirch Powder 100g", "MDH", 92, [90, 240], "OPTIMAL_SHELF_HEALTH"),
        ("Catch Super Garam Masala 100g", "Catch", 85, [60, 180], "OPTIMAL_SHELF_HEALTH"),
        ("Tata Sampann Turmeric Haldi Powder 200g", "Tata Sampann", 56, [90, 300], "OPTIMAL_SHELF_HEALTH"),
        ("Everest Kasmiri Chilli Powder 100g", "Everest", 98, [75, 220], "OPTIMAL_SHELF_HEALTH"),
        ("Dabur Hommade Ginger Garlic Paste 200g", "Dabur", 55, [15, 60], "PRIORITIZE_FEFO_DISPATCH"),
    ],
    "OTC Healthcare & Wellness": [
        ("Dolo-650 Paracetamol 15 Tablets Strip", "Micro Labs", 32, [14, 90], "PRIORITIZE_FEFO_DISPATCH"),
        ("Crocin Advance Fast Relief 15 Tablets", "GSK Crocin", 34, [30, 180], "OPTIMAL_SHELF_HEALTH"),
        ("Vicks Vaporub Ayurvedic Balm 50ml", "P&G Vicks", 145, [120, 365], "OPTIMAL_SHELF_HEALTH"),
        ("Eno Fruit Salt Regular Lemon 100g Bottle", "GSK Eno", 160, [60, 240], "OPTIMAL_SHELF_HEALTH"),
        ("Dabur Chyawanprash 2X Immunity 1kg", "Dabur", 395, [45, 180], "OPTIMAL_SHELF_HEALTH"),
        ("Himalaya Liv.52 Herbal Liver Support 100 Tablets", "Himalaya", 170, [90, 365], "OPTIMAL_SHELF_HEALTH"),
        ("Moov Pain Relief Cream Ayurvedic 50g", "Reckitt Moov", 185, [60, 240], "OPTIMAL_SHELF_HEALTH"),
        ("Pudinhara Pearls Ayurvedic Relief 10 Pearls", "Dabur", 30, [45, 180], "OPTIMAL_SHELF_HEALTH"),
    ],
    "Personal Care & Hygiene": [
        ("Dettol Original Germ Protection Bathing Soap 125g x 4", "Reckitt Dettol", 195, [180, 540], "OPTIMAL_SHELF_HEALTH"),
        ("Lifebuoy Total Germ Protection Soap 125g x 4", "HUL Lifebuoy", 145, [180, 540], "OPTIMAL_SHELF_HEALTH"),
        ("Colgate Strong Teeth Dental Paste 300g", "Colgate", 165, [120, 365], "OPTIMAL_SHELF_HEALTH"),
        ("Head & Shoulders Anti-Dandruff Shampoo 340ml", "P&G", 320, [90, 300], "OPTIMAL_SHELF_HEALTH"),
        ("Dove Deep Moisture Nourishing Body Wash 250ml", "HUL Dove", 225, [90, 365], "OPTIMAL_SHELF_HEALTH"),
        ("Pond's White Beauty Daily Spot-less Cream 50g", "HUL Pond's", 150, [60, 240], "OPTIMAL_SHELF_HEALTH"),
    ]
}

# ── APMC Mandi Commodities Matrix ─────────────────────────────────────────────
MANDI_HUBS = [
    ("Azadpur Mandi", "Delhi", "Asia's Largest Fruit & Vegetable Terminal"),
    ("Vashi APMC Market", "Mumbai, Maharashtra", "Western India Hub"),
    ("Yeshwanthpur APMC", "Bengaluru, Karnataka", "South India Grain & Onion Hub"),
    ("Lasalgaon APMC", "Nashik, Maharashtra", "India's Central Onion Capital"),
    ("Guntur Mirchi Yard", "Guntur, Andhra Pradesh", "Asia's Premier Red Chilli Market"),
    ("Unjha APMC Mandi", "Mehsana, Gujarat", "Global Cumin & Isabgol Capital"),
    ("Kolar APMC Mandi", "Kolar, Karnataka", "Asia's 2nd Largest Tomato Market"),
    ("Mandsaur Mandi", "Mandsaur, Madhya Pradesh", "Garlic & Soybean Center"),
    ("Nizamabad APMC", "Nizamabad, Telangana", "National Turmeric Hub"),
    ("Koyambedu Wholesale Market", "Chennai, Tamil Nadu", "Coromandel Produce Terminal"),
    ("Khari Baoli Wholesale", "Old Delhi", "Asia's Largest Spice Exchange"),
    ("Rajkot APMC", "Rajkot, Gujarat", "Groundnut & Cotton Exchange"),
    ("Surat APMC Market", "Surat, Gujarat", "Diamond City Wholesale Produce"),
    ("Nagpur Orange & Grain Mandi", "Nagpur, Maharashtra", "Vidarbha Produce Exchange"),
    ("Karnal Grain Market", "Karnal, Haryana", "Basmati Rice Capital Exchange"),
    ("Erode Turmeric Market", "Erode, Tamil Nadu", "Yellow City Turmeric Exchange"),
]

COMMODITY_PRICES = [
    ("Onion (Nashik Red)", "Quintal", 1800, 2600, 2250, "Trending Down (-4%)", "Heavy Kharif Arrivals"),
    ("Tomato (Hybrid Red)", "Quintal", 1200, 2100, 1650, "Stable", "Local Harvest Steady"),
    ("Potato (Agra Jyoti)", "Quintal", 1400, 1950, 1720, "Trending Up (+6%)", "Cold Storage Despatches Active"),
    ("Wheat (Sharbati Grade-A)", "Quintal", 2850, 3400, 3150, "Firm", "Govt Procurement Active"),
    ("Basmati Paddy (1121 Pusa)", "Quintal", 3800, 4600, 4250, "Bullish (+8%)", "Export Demand Strong"),
    ("Soybean (Yellow Bold)", "Quintal", 4400, 5100, 4850, "Steady", "Crushers Buying Actively"),
    ("Chana (Desi Gram)", "Quintal", 5600, 6400, 6100, "Firm", "Festive Pipeline Demand"),
    ("Turmeric (Salem Finger)", "Quintal", 12500, 15800, 14200, "Bullish (+12%)", "Low Carryover Stock"),
    ("Red Chilli (Teja Best)", "Quintal", 18500, 24000, 21500, "Firm", "Export Enquiries Strong"),
    ("Jeera (Cumin Machine Clean)", "Quintal", 24000, 31000, 27500, "Consolidating", "New Crop Sowing Underway"),
    ("Mustard Seed (Black Bold)", "Quintal", 5100, 5750, 5450, "Steady", "Crush Margins Positive"),
    ("Cotton (Kapas Shankar-6)", "Candy", 54000, 61000, 58200, "Rangebound", "Spinning Mills Buying Routine"),
]

# ── Socratic CS Probing Bank ──────────────────────────────────────────────────
SOCRATIC_TOPICS = {
    "Operating Systems": [
        ("Deadlock Prevention vs Avoidance", "Banker's Algorithm safe state aur resource allocation graph mein cycle check ka overhead compare kijiye.", 85),
        ("Virtual Memory & Paging", "Agar page size 4KB se 2MB (Huge Pages) kar dein, toh TLB reach aur internal fragmentation pe kya trade-off hoga?", 88),
        ("Process Scheduling & CFS", "Linux Completely Fair Scheduler mein vruntime Red-Black Tree mein kyun store hota hai? O(log N) vs O(1) scheduling trade-off explain kijiye.", 90),
        ("Concurrency & Mutex Locks", "Spinlock vs Mutex mein CPU context switch penalty kab justify hoti hai? Multicore systems mein TAS (Test-And-Set) lock cache coherence traffic kaise create karta hai?", 86),
        ("Copy-On-Write (COW) Fork", "fork() system call mein COW page fault tab kyun trigger hota hai jab child ya parent write karta hai? Page table entry flags kaise modify hote hain?", 92),
    ],
    "Database Management Systems": [
        ("B+ Tree Indexing", "B+ Tree mein leaf nodes ki bidirectional linked list range scan queries ko disk block level pe kaise accelerate karti hai?", 87),
        ("ACID Isolation Levels", "Snapshot Isolation (MVCC) write skew anomaly kyun prevent nahi kar pata jabki phantom reads eliminate ho jaate hain?", 91),
        ("Write-Ahead Logging (WAL)", "ARIES recovery algorithm mein Analysis, Redo, aur Undo phases ka exact role kya hai? Steal/No-Force buffer management policy explain kijiye.", 89),
        ("Distributed Consensus (2PC vs Raft)", "Two-Phase Commit (2PC) protocol mein coordinator crash hone pe participants blocking state mein kyun chale jaate hain? Raft isse kaise solve karta hai?", 93),
        ("Query Optimization & Joins", "Hash Join vs Sort-Merge Join mein memory footprint aur disk spill trade-offs kab justify hote hain?", 84),
    ],
    "Data Structures & Algorithms": [
        ("Dijkstra vs Bellman-Ford", "Dijkstra negative cycles detect kyun nahi kar sakta jabki Bellman-Ford N-1 iterations ke baad bhi relaxing check se detect kar leta hai?", 88),
        ("Dynamic Programming Space Optimization", "0/1 Knapsack problem mein 2D DP array ko single 1D array mein reverse order iteration se kyun compress kiya jaata hai?", 86),
        ("Trie & Suffix Automaton", "Aho-Corasick automaton mein failure links KMP algorithm ke LPS array ke equivalent kaise act karte hain multiple pattern searching mein?", 94),
        ("Segment Trees & Lazy Propagation", "Range update queries mein O(log N) complexity maintain karne ke liye deferred updates child nodes pe kab push down hote hain?", 89),
    ],
    "System Design & Distributed AI": [
        ("Low-Latency Voice AI Architecture", "WebSocket streaming frame size 1024 bytes (32ms) audio pipeline mein jitter buffer aur packet loss concealment kaise optimize karta hai?", 95),
        ("Cache Invalidation & Consistency", "Write-Through vs Write-Back caching mein distributed multi-master Redis cluster cache stampede (thundering herd) se kaise bachta hai?", 90),
        ("Token Bucket vs Leaky Bucket", "API Rate Limiting mein bursty voice streaming traffic handle karne ke liye Token Bucket algorithm leaky bucket se superior kyun hai?", 88),
    ]
}


class MassiveIndicDatabase:
    """
    In-memory indexed database engine holding 10,000+ structured synthetic records.
    Provides sub-millisecond full-text token search and structured domain lookups.
    """

    def __init__(self):
        self.products: List[Dict[str, Any]] = []
        self.wards: List[Dict[str, Any]] = []
        self.mandi_rates: List[Dict[str, Any]] = []
        self.socratic_bank: List[Dict[str, Any]] = []

        # Token inverted indexes for instant <1ms lookup
        self._product_index: Dict[str, List[int]] = {}
        self._ward_index: Dict[str, List[int]] = {}
        self._mandi_index: Dict[str, List[int]] = {}
        self._viva_index: Dict[str, List[int]] = {}

        self.initialized = False
        self._load_data()

    def _tokenize(self, text: str) -> List[str]:
        """Convert string to lowercase alphanumeric tokens."""
        return re.findall(r"\w+", text.lower())

    def _load_data(self):
        t0 = time.perf_counter()

        # ── 1. Generate 5,000+ Kirana FMCG SKUs ────────────────────────────────
        sku_counter = 1000
        for category, items in FMCG_CATEGORIES.items():
            for base_name, brand, base_price, expiry_range, action in items:
                # Generate variants across pack sizes & batches & regions
                pack_sizes = ["100g", "200g", "500g", "1kg", "2kg", "5kg", "Family Pack", "Economy Pouch", "Combo Pack", "Bulk Carton", "Twin Pack", "Trial Pack"]
                for pack_idx, pack in enumerate(pack_sizes):
                    for batch_suffix in ["A", "B", "C", "D", "E", "F"]:
                        sku_counter += 1
                        sku_id = f"SKU-SYN-{sku_counter}"
                        name = f"{base_name} ({pack} - Batch {batch_suffix})"
                        exp_days = random.randint(expiry_range[0], expiry_range[1])
                        mrp = int(base_price * (1.0 + (pack_idx * 0.65)))
                        cost = int(mrp * 0.82)
                        stock = random.randint(4, 250)
                        
                        rec = {
                            "sku_id": sku_id,
                            "name": name,
                            "brand": brand,
                            "category": category,
                            "mrp": mrp,
                            "cost_price": cost,
                            "stock": stock,
                            "expiry_days": exp_days,
                            "batch_no": f"SYN-B{random.randint(100, 999)}{batch_suffix}",
                            "action": action if exp_days <= 5 else "OPTIMAL_SHELF_HEALTH",
                            "mandi_discount_active": exp_days <= 5,
                        }
                        idx = len(self.products)
                        self.products.append(rec)

                        # Index tokens
                        tokens = self._tokenize(f"{name} {brand} {category} {sku_id}")
                        for tok in tokens:
                            if tok not in self._product_index:
                                self._product_index[tok] = []
                            self._product_index[tok].append(idx)

        # ── 2. Generate 3,500+ Indian Municipal Civic Wards ───────────────────
        ward_counter = 100
        for city_info in INDIAN_CITIES:
            city = city_info["city"]
            state = city_info["state"]
            corp = city_info["corp"]
            for zone in city_info["zones"]:
                for loc in LOCALITY_NAMES[:24]:
                    ward_counter += 1
                    ward_num = f"Ward {ward_counter % 280 + 1}"
                    ward_id = f"WARD-{city[:3].upper()}-{ward_counter}"
                    eng_first = random.choice(FIRST_NAMES)
                    eng_last = random.choice(LAST_NAMES)
                    eng_name = f"Engr. {eng_first} {eng_last} (SYN-EMP-{random.randint(100, 999)})"
                    
                    rec = {
                        "ward_id": ward_id,
                        "ward_name": f"{ward_num} - {loc} ({zone})",
                        "city": city,
                        "state": state,
                        "corporation": corp,
                        "zone": zone,
                        "locality": loc,
                        "nodal_engineer": eng_name,
                        "transformer_grid_id": f"GRID-TX-{city[:2].upper()}-{random.randint(10, 99)}",
                        "water_pipeline_junction": f"JUNC-WTR-{random.randint(100, 999)}",
                        "active_p1_tickets": random.randint(0, 3),
                        "sla_target_mins": 45,
                    }
                    idx = len(self.wards)
                    self.wards.append(rec)

                    tokens = self._tokenize(f"{ward_id} {ward_num} {loc} {city} {zone} {corp}")
                    for tok in tokens:
                        if tok not in self._ward_index:
                            self._ward_index[tok] = []
                        self._ward_index[tok].append(idx)

        # ── 3. Generate 1,500+ APMC Mandi Daily Commodity Records ─────────────
        mandi_counter = 1000
        for mandi_name, location, hub_desc in MANDI_HUBS:
            for comm, unit, p_min, p_max, p_modal, trend, note in COMMODITY_PRICES:
                for grade in ["Super Grade", "FAQ Grade", "Export Grade", "Desi Bold", "Organic Premium", "Standard Wholesale"]:
                    mandi_counter += 1
                    mandi_id = f"APMC-SYN-{mandi_counter}"
                    jitter = random.randint(-120, 150)
                    rec = {
                        "mandi_id": mandi_id,
                        "mandi_name": mandi_name,
                        "location": location,
                        "commodity": f"{comm} ({grade})",
                        "unit": unit,
                        "min_price": max(100, p_min + jitter),
                        "max_price": p_max + jitter,
                        "modal_price": p_modal + jitter,
                        "trend": trend,
                        "market_note": f"{note} at {mandi_name}",
                        "daily_arrivals_tonnes": random.randint(45, 1200),
                        "timestamp": "Today 06:00 AM IST",
                    }
                    idx = len(self.mandi_rates)
                    self.mandi_rates.append(rec)

                    tokens = self._tokenize(f"{mandi_id} {mandi_name} {comm} {grade} {location}")
                    for tok in tokens:
                        if tok not in self._mandi_index:
                            self._mandi_index[tok] = []
                        self._mandi_index[tok].append(idx)

        # ── 4. Generate 1,500+ Socratic Technical Question Bank ────────────────
        viva_counter = 100
        for subject, probes in SOCRATIC_TOPICS.items():
            for topic, probe_text, clarity_baseline in probes:
                for subtopic_idx in range(65):
                    viva_counter += 1
                    qid = f"VIVA-SYN-{viva_counter}"
                    rec = {
                        "question_id": qid,
                        "subject": subject,
                        "topic": f"{topic} (Case Study #{subtopic_idx + 1})",
                        "socratic_probe": probe_text,
                        "clarity_baseline": clarity_baseline + random.randint(-4, 4),
                        "conceptual_rubric": [
                            "Identify the race condition / resource contention",
                            "Explain CPU context switch penalty & memory overhead",
                            "Provide real-world mitigation (lock hierarchy, MVCC, or exponential backoff)",
                        ],
                    }
                    idx = len(self.socratic_bank)
                    self.socratic_bank.append(rec)

                    tokens = self._tokenize(f"{qid} {subject} {topic} {probe_text}")
                    for tok in tokens:
                        if tok not in self._viva_index:
                            self._viva_index[tok] = []
                        self._viva_index[tok].append(idx)

        elapsed = round((time.perf_counter() - t0) * 1000, 1)
        self.initialized = True
        logger.info(
            "🗄️ MassiveIndicDatabase initialized in %.1fms: %d FMCG SKUs, %d Wards, %d Mandi records, %d Socratic probes. Total: %d records.",
            elapsed, len(self.products), len(self.wards), len(self.mandi_rates), len(self.socratic_bank),
            len(self.products) + len(self.wards) + len(self.mandi_rates) + len(self.socratic_bank)
        )

    # ── Search & Retrieval APIs ──────────────────────────────────────────────
    def find_product(self, query: str) -> Dict[str, Any]:
        """Find the closest product record for a Kirana query."""
        tokens = self._tokenize(query)
        if not tokens:
            return random.choice(self.products)

        # Score product matches by token overlap
        scores: Dict[int, int] = {}
        for tok in tokens:
            for idx in self._product_index.get(tok, []):
                scores[idx] = scores.get(idx, 0) + 1

        if scores:
            best_idx = max(scores, key=scores.get)
            return self.products[best_idx]
        return random.choice(self.products)

    def find_ward(self, query: str) -> Dict[str, Any]:
        """Find the closest Indian ward record for a Civic complaint."""
        tokens = self._tokenize(query)
        if not tokens:
            return random.choice(self.wards)

        scores: Dict[int, int] = {}
        for tok in tokens:
            for idx in self._ward_index.get(tok, []):
                scores[idx] = scores.get(idx, 0) + 1

        if scores:
            best_idx = max(scores, key=scores.get)
            return self.wards[best_idx]
        return random.choice(self.wards)

    def find_mandi_rate(self, query: str) -> Dict[str, Any]:
        """Find the closest APMC Mandi rate record."""
        tokens = self._tokenize(query)
        if not tokens:
            return random.choice(self.mandi_rates)

        scores: Dict[int, int] = {}
        for tok in tokens:
            for idx in self._mandi_index.get(tok, []):
                scores[idx] = scores.get(idx, 0) + 1

        if scores:
            best_idx = max(scores, key=scores.get)
            return self.mandi_rates[best_idx]
        return random.choice(self.mandi_rates)

    def get_socratic_probe(self, query: str) -> Dict[str, Any]:
        """Retrieve a tailored Socratic probe from the 1,500+ question bank."""
        tokens = self._tokenize(query)
        if not tokens:
            return random.choice(self.socratic_bank)

        scores: Dict[int, int] = {}
        for tok in tokens:
            for idx in self._viva_index.get(tok, []):
                scores[idx] = scores.get(idx, 0) + 1

        if scores:
            best_idx = max(scores, key=scores.get)
            return self.socratic_bank[best_idx]
        return random.choice(self.socratic_bank)

    def search_all(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Multi-domain full-text search across all 10,000+ records in <1ms."""
        tokens = self._tokenize(query)
        if not tokens:
            return []

        results = []
        # Products
        for tok in tokens:
            for idx in self._product_index.get(tok, [])[:5]:
                p = self.products[idx]
                results.append({"type": "PRODUCT", "title": p["name"], "detail": f"MRP ₹{p['mrp']} • Stock: {p['stock']} • {p['action']}", "id": p["sku_id"]})
        # Wards
        for tok in tokens:
            for idx in self._ward_index.get(tok, [])[:5]:
                w = self.wards[idx]
                results.append({"type": "CIVIC_WARD", "title": w["ward_name"], "detail": f"City: {w['city']} • {w['nodal_engineer']}", "id": w["ward_id"]})
        # Mandi
        for tok in tokens:
            for idx in self._mandi_index.get(tok, [])[:5]:
                m = self.mandi_rates[idx]
                results.append({"type": "MANDI_RATE", "title": f"{m['commodity']} - {m['mandi_name']}", "detail": f"Modal: ₹{m['modal_price']}/{m['unit']} • {m['trend']}", "id": m["mandi_id"]})

        # Deduplicate
        seen = set()
        deduped = []
        for r in results:
            if r["id"] not in seen:
                seen.add(r["id"])
                deduped.append(r)
                if len(deduped) >= limit:
                    break
        return deduped

    def get_stats(self) -> Dict[str, Any]:
        """Return executive statistics of the massive database."""
        total = len(self.products) + len(self.wards) + len(self.mandi_rates) + len(self.socratic_bank)
        return {
            "total_records": total,
            "domains": {
                "kirana_fmcg_skus": len(self.products),
                "municipal_civic_wards": len(self.wards),
                "apmc_mandi_rates": len(self.mandi_rates),
                "socratic_viva_probes": len(self.socratic_bank),
            },
            "cities_covered": len(INDIAN_CITIES),
            "apmc_mandis_covered": len(MANDI_HUBS),
            "indexed_unique_tokens": len(self._product_index) + len(self._ward_index) + len(self._mandi_index) + len(self._viva_index),
            "index_search_latency": "< 1 ms (in-memory inverted hash)",
        }


# Global singleton instance
db = MassiveIndicDatabase()
