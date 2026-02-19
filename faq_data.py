"""
faq_data.py — 15 Institute FAQs with keywords, intents, and synonym groups.
"""

FAQS = [
    {
        "id": 1,
        "question": "What are the college timings?",
        "answer": "The college operates from 9:00 AM to 5:00 PM, Monday through Saturday. The administrative office is open from 9:30 AM to 4:30 PM.",
        "keywords": ["timings", "hours", "schedule", "open", "close", "time"],
        "intent": "general",
        "synonyms": {"timings": ["timing", "hours", "schedule", "open", "close", "working hours"]}
    },
    {
        "id": 2,
        "question": "What are the tuition fees?",
        "answer": "The annual tuition fee is ₹1,20,000 for undergraduate programs and ₹1,50,000 for postgraduate programs. Payment can be made in two installments per year.",
        "keywords": ["fees", "tuition", "payment", "cost", "price", "charge"],
        "intent": "admissions",
        "synonyms": {"fees": ["tuition", "payment", "cost", "price", "charge", "fee structure"]}
    },
    {
        "id": 3,
        "question": "How do I contact the administration?",
        "answer": "You can reach the administration at:\n📧 Email: admin@institute.edu.in\n📞 Phone: +91-22-12345678\n🏢 Office: Ground Floor, Main Building, Room 101",
        "keywords": ["contact", "phone", "email", "address", "reach", "office"],
        "intent": "general",
        "synonyms": {"contact": ["phone", "email", "address", "reach", "call", "office location"]}
    },
    {
        "id": 4,
        "question": "What is the admission process?",
        "answer": "Admissions are based on merit and entrance exam scores. Steps:\n1. Fill the online application form at admissions.institute.edu.in\n2. Upload required documents (marksheets, ID proof, photographs)\n3. Pay the application fee of ₹500\n4. Attend the counseling/interview round\n5. Confirm admission by paying the first installment",
        "keywords": ["admission", "apply", "application", "enroll", "registration", "join"],
        "intent": "admissions",
        "synonyms": {"admission": ["apply", "application", "enroll", "registration", "join", "intake"]}
    },
    {
        "id": 5,
        "question": "When are the exams scheduled?",
        "answer": "Semester exams are held twice a year:\n📅 Winter Semester: November–December\n📅 Summer Semester: April–May\nInternal assessments are conducted in September and February. Detailed date sheets are published 3 weeks before exams on the college website.",
        "keywords": ["exam", "test", "examination", "date", "schedule", "datesheet"],
        "intent": "exams",
        "synonyms": {"exam": ["test", "examination", "paper", "assessment", "datesheet"]}
    },
    {
        "id": 6,
        "question": "Where can I find the timetable?",
        "answer": "The class timetable is available on the student portal at portal.institute.edu.in under the 'Academics' section. It is also displayed on the departmental notice boards. Timetables are updated at the beginning of each semester.",
        "keywords": ["timetable", "schedule", "class", "lecture", "period"],
        "intent": "timetable",
        "synonyms": {"timetable": ["schedule", "class schedule", "lecture", "period", "routine"]}
    },
    {
        "id": 7,
        "question": "Tell me about hostel facilities.",
        "answer": "The institute offers separate hostels for boys and girls with:\n🛏️ Single and shared rooms (AC & Non-AC)\n🍽️ Mess facility with 3 meals + snacks\n📶 24/7 Wi-Fi\n🔒 Security with CCTV and biometric entry\nHostel fee: ₹60,000–₹90,000 per year depending on room type.",
        "keywords": ["hostel", "accommodation", "room", "mess", "dormitory", "stay"],
        "intent": "hostel",
        "synonyms": {"hostel": ["accommodation", "room", "mess", "dormitory", "stay", "residence", "boarding"]}
    },
    {
        "id": 8,
        "question": "What scholarships are available?",
        "answer": "The institute offers multiple scholarships:\n🏅 Merit Scholarship — Top 5% students (50% fee waiver)\n💰 Need-Based Financial Aid — For economically weaker sections\n🎓 Government Scholarships — SC/ST/OBC/Minority schemes\n🏆 Sports Scholarship — State/National level athletes\nApply through the scholarship portal by August 31 each year.",
        "keywords": ["scholarship", "financial", "aid", "merit", "concession", "waiver"],
        "intent": "scholarships",
        "synonyms": {"scholarship": ["financial aid", "merit", "concession", "waiver", "bursary", "grant"]}
    },
    {
        "id": 9,
        "question": "What are the library timings and rules?",
        "answer": "📚 Library Timings: 8:00 AM – 9:00 PM (Mon–Sat), 10:00 AM – 5:00 PM (Sunday)\n📖 Students can borrow up to 4 books for 14 days\n💻 Digital library with access to IEEE, Springer, and JSTOR databases\n⚠️ Late return fine: ₹5/day per book",
        "keywords": ["library", "book", "borrow", "reading", "digital"],
        "intent": "facilities",
        "synonyms": {"library": ["book", "borrow", "reading room", "digital library", "e-library"]}
    },
    {
        "id": 10,
        "question": "Does the college have a placement cell?",
        "answer": "Yes! Our Training & Placement Cell has an excellent track record:\n📊 90%+ placement rate for eligible students\n💼 150+ recruiting companies including TCS, Infosys, Wipro, Amazon, Google\n💰 Highest package: ₹42 LPA | Average package: ₹6.5 LPA\nPlacement drives are conducted from August to March every year.",
        "keywords": ["placement", "job", "recruit", "career", "campus", "company", "package"],
        "intent": "facilities",
        "synonyms": {"placement": ["job", "recruit", "career", "campus recruitment", "company", "package", "hiring"]}
    },
    {
        "id": 11,
        "question": "Are there sports facilities?",
        "answer": "The institute has excellent sports facilities:\n🏏 Cricket ground & football field\n🏸 Indoor courts for badminton, table tennis, and basketball\n🏋️ Modern gym and fitness center\n🏊 Swimming pool (25m)\nAnnual sports meet is held in January. Students can join various sports clubs.",
        "keywords": ["sports", "gym", "ground", "fitness", "games", "play"],
        "intent": "facilities",
        "synonyms": {"sports": ["gym", "ground", "fitness", "games", "play", "athletics", "exercise"]}
    },
    {
        "id": 12,
        "question": "Is there a college bus or transport facility?",
        "answer": "Yes, the college provides bus services on 12 routes across the city.\n🚌 Bus pass fee: ₹15,000/year\n⏰ Pick-up: 7:30 AM – 8:30 AM | Drop: 5:00 PM – 6:00 PM\nRoute details are available at the transport office (Room 105, Admin Block) or on the college app.",
        "keywords": ["bus", "transport", "shuttle", "route", "commute", "travel"],
        "intent": "facilities",
        "synonyms": {"transport": ["bus", "shuttle", "route", "commute", "travel", "conveyance"]}
    },
    {
        "id": 13,
        "question": "How do I access the campus Wi-Fi?",
        "answer": "Campus Wi-Fi (SSID: 'InstituteNet') is available across all academic buildings and hostels.\n📱 Login using your student ID and portal password\n🔗 First-time setup guide: wifi.institute.edu.in/setup\n📞 IT Helpdesk: ext. 555 or ithelpdesk@institute.edu.in",
        "keywords": ["wifi", "internet", "network", "net", "connect", "online"],
        "intent": "facilities",
        "synonyms": {"wifi": ["internet", "network", "net", "connect", "online", "wi-fi", "broadband"]}
    },
    {
        "id": 14,
        "question": "What food options are available on campus?",
        "answer": "The campus has multiple food options:\n🍽️ Main Canteen: 8 AM – 8 PM (breakfast, lunch, dinner)\n☕ Café Coffee Corner: 9 AM – 6 PM\n🥤 Juice bar & snack kiosks near the library\n📱 Online ordering available via the campus app\nAll food outlets maintain FSSAI hygiene standards.",
        "keywords": ["canteen", "food", "cafeteria", "mess", "eat", "lunch", "snack"],
        "intent": "facilities",
        "synonyms": {"canteen": ["food", "cafeteria", "mess", "eat", "lunch", "snack", "restaurant", "dining"]}
    },
    {
        "id": 15,
        "question": "What is the anti-ragging policy?",
        "answer": "The institute has a strict ZERO TOLERANCE policy against ragging.\n🚨 Anti-Ragging Helpline: 1800-180-5522 (24/7)\n📧 Report: antiragging@institute.edu.in\n👮 Anti-Ragging Committee meets monthly\n⚖️ Penalties include suspension, expulsion, and FIR as per UGC regulations.\nAll students must sign an anti-ragging undertaking at the time of admission.",
        "keywords": ["ragging", "bully", "harassment", "complaint", "safety"],
        "intent": "general",
        "synonyms": {"ragging": ["bully", "harassment", "complaint", "safety", "anti-ragging"]}
    }
]

# Flat synonym dictionary built from FAQ synonym groups
SYNONYM_DICT = {}
for faq in FAQS:
    for canonical, synonyms in faq.get("synonyms", {}).items():
        for syn in synonyms:
            SYNONYM_DICT[syn.lower()] = canonical.lower()
        SYNONYM_DICT[canonical.lower()] = canonical.lower()
