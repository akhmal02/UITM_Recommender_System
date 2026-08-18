"""Knowledge base for free-form UITM & system questions."""

UITM_ABOUT = (
    "**Universiti Teknologi MARA (UITM)** is Malaysia's largest public university, "
    "established to provide higher education opportunities through a practical, industry-oriented approach. "
    "UITM has campuses across all Malaysian states and offers diploma, degree, and postgraduate programmes.\n\n"
    "Key facts:\n"
    "• Founded in 1956 (originally RIDA Training Centre)\n"
    "• Main campus: Shah Alam, Selangor\n"
    "• Over 500,000 alumni worldwide\n"
    "• Strong focus on Bumiputera education and professional readiness\n"
    "• Faculties cover science, engineering, business, social sciences, creative arts, and agriculture"
)

SYSTEM_ABOUT = (
    "**UITM CourseRec** is a smart course recommendation system built for UITM students.\n\n"
    "**What it does:**\n"
    "• Recommends courses based on your faculty, skill level, interests, and preferences\n"
    "• Uses **7 rule-based filters** to score and rank courses\n"
    "• Lets you browse **72 courses** across 6 UITM faculties (12 per faculty)\n"
    "• Enforces UITM's **24 credit-hour** semester limit\n"
    "• Auto-generates your **weekly timetable** from enrolled courses\n"
    "• Provides this **AI assistant** for any UITM or system questions\n\n"
    "**Main pages:** Home, For You (recommendations), Courses, Assistant, Schedule, Tune (preferences), Profile"
)

# (trigger phrases, answer, suggestions)
KNOWLEDGE_ENTRIES: list[tuple[list[str], str, list[str]]] = [
    (
        ["what is uitm", "what uitm", "tell me about uitm", "uitm adalah", "apakah uitm", "about uitm"],
        UITM_ABOUT,
        ["UITM faculties", "What is CourseRec?", "FSKM courses", "How to enroll"],
    ),
    (
        ["what is courserc", "what is this system", "what does this do", "about this app",
         "what is this website", "purpose of system", "explain system", "system ni"],
        SYSTEM_ABOUT,
        ["How recommendations work", "Show faculties", "My credit hours", "How to enroll"],
    ),
    (
        ["what is fskm", "fakulti sains komputer", "fskm faculty", "fskm adalah"],
        "**FSKM** — Fakulti Sains Komputer dan Matematik\n\n"
        "Offers programmes in computer science, mathematics, statistics, and IT. "
        "Sample courses: CSC248 (Data Structure), CSC186 (Database), CSC339 (AI), MAT112 (Algebra), ICT707 (Info Security).\n\n"
        "12 courses available in this system.",
        ["FSKM courses", "Set faculty to FSKM", "CSC248", "My recommendations"],
    ),
    (
        ["what is fk", "fakulti kejuruteraan", "engineering faculty"],
        "**FK** — Fakulti Kejuruteraan\n\n"
        "Covers electrical, mechanical, civil, and chemical engineering. "
        "Sample courses: EEE443 (Electrical Machines), MEC411 (Thermodynamics), EEC301 (Circuit Theory).\n\n"
        "12 courses available in this system.",
        ["FK courses", "EEE443", "My recommendations"],
    ),
    (
        ["what is fpp", "fakulti perniagaan", "business faculty"],
        "**FPP** — Fakulti Perniagaan dan Pengurusan\n\n"
        "Business, finance, marketing, entrepreneurship, and management programmes. "
        "Sample courses: FIN302 (Corporate Finance), MKT420 (International Marketing), ENT600 (Entrepreneurship).\n\n"
        "12 courses available in this system.",
        ["FPP courses", "How to enroll", "My credit hours"],
    ),
    (
        ["what is fsssk", "social science", "fakulti sains sosial"],
        "**FSSSK** — Fakulti Sains Sosial dan Sains Kemanusiaan\n\n"
        "Psychology, sociology, communication, political science, and Malaysian studies. "
        "Sample courses: PAD170 (Malaysian Studies), PSY204 (Developmental Psychology), SOC101 (Sociology).\n\n"
        "12 courses available in this system.",
        ["FSSSK courses", "PAD170", "My recommendations"],
    ),
    (
        ["what is fskt", "creative", "fakulti seni kreatif", "art faculty"],
        "**FSKT** — Fakulti Seni Kreatif dan Teknologi\n\n"
        "Graphic design, architecture, music, television production, and fine arts. "
        "Sample courses: GID3023 (Graphic Design), TDT473 (TV Production), ARC101 (Architecture).\n\n"
        "12 courses available in this system.",
        ["FSKT courses", "GID3023", "My recommendations"],
    ),
    (
        ["what is fpa", "agriculture", "fakulti perladangan", "plantation"],
        "**FPA** — Fakulti Perladangan dan Agroteknologi\n\n"
        "Agriculture, food science, plantation management, animal science, and biotechnology. "
        "Sample courses: LBS101 (Plantation Management), HFF225 (Food Chemistry), BIO302 (Plant Biotech).\n\n"
        "12 courses available in this system.",
        ["FPA courses", "LBS101", "My recommendations"],
    ),
    (
        ["campus", "shah alam", "where is uitm", "lokasi uitm", "uitm location"],
        "UITM's **main campus** is in **Shah Alam, Selangor**. UITM also has branch campuses "
        "in every Malaysian state including Johor, Penang, Sabah, Sarawak, Kelantan, and more. "
        "Each state campus offers programmes aligned with local industry needs.",
        ["What is UITM?", "UITM faculties", "Show faculties"],
    ),
    (
        ["recommendation", "how recommend", "matching", "match score", "how does it work",
         "rule based", "filtering engine", "bagaimana cadangan"],
        "**How recommendations work:**\n\n"
        "The engine applies **7 rules** to every course in your faculty:\n"
        "1. **Faculty match** — must be your UITM faculty\n"
        "2. **Difficulty** — your level ±1 stretch\n"
        "3. **Duration** — Short/Medium/Long preference\n"
        "4. **Format** — Online, In-Person, Hybrid, or Any\n"
        "5. **Credit limit** — must fit your remaining 24-hour budget\n"
        "6. **Interest tags** — bonus for keyword matches\n"
        "7. **Rating** — quality boost from student ratings\n\n"
        "Each course gets a match % and reasons. Set preferences in **Tune** to improve results.",
        ["My recommendations", "Set preferences", "My credit hours"],
    ),
    (
        ["difficulty", "beginner", "intermediate", "advanced", "skill level", "tahap"],
        "**Difficulty levels:**\n"
        "• **Beginner** — foundation courses, no prior knowledge needed\n"
        "• **Intermediate** — builds on basics, some prerequisites expected\n"
        "• **Advanced** — specialised, project-based or research-oriented\n\n"
        "The system recommends courses at your level and one step above as stretch goals.",
        ["Set preferences", "My recommendations", "Browse courses"],
    ),
    (
        ["interest tag", "tags", "keyword", "minat"],
        "**Interest tags** are comma-separated keywords you set in **Preferences** "
        "(e.g. `programming, statistik, pemasaran`).\n\n"
        "When a course's tags overlap with your interests, it gets a **bonus match score**. "
        "This helps surface courses aligned with your personal goals beyond just faculty and level.",
        ["Set preferences", "My recommendations", "FSKM courses"],
    ),
    (
        ["lecturer", "professor", "pensyarah", "instructor", "siapa pengajar"],
        "All courses in this system are taught by **UITM lecturers** with Malay honorific names "
        "(Dr., Prof. Madya Dr., etc.). Each course card shows the assigned lecturer. "
        "Example: Dr. Ahmad Faizal bin Mohd Zaid teaches CSC248.",
        ["CSC248", "FSKM courses", "Browse courses"],
    ),
    (
        ["who can use", "who is this for", "siapa boleh guna", "for student"],
        "This system is designed for **UITM students** who want help choosing semester courses. "
        "Create a free account, set your faculty and preferences, and get personalised recommendations "
        "with enrollment and timetable management.",
        ["How to enroll", "Create account", "What is UITM?"],
    ),
    (
        ["dashboard", "home page", "main page"],
        "The **Dashboard** shows your stats: courses in your faculty, matched recommendations, "
        "enrollment count, and credit hours used. It also displays your top 4 recommended courses "
        "and recent enrollments.",
        ["My recommendations", "My credit hours", "Top recommendations"],
    ),
    (
        ["profile", "account", "akaun"],
        "Your **Profile** page shows your name, email, member since date, current preferences, "
        "credit hours enrolled, and full enrollment history.",
        ["My enrollments", "Edit preferences", "My credit hours"],
    ),
    (
        ["logout", "sign out", "keluar"],
        "Click **Exit** in the bottom dock menu to log out. Your enrollments and preferences are saved in the database.",
        ["My enrollments", "Dashboard"],
    ),
    (
        ["semester", "credit hour", "jam kredit uitm", "berapa kredit"],
        "UITM students typically register **up to 24 credit hours** per semester in this system. "
        "Each course is 2–4 credits. The system blocks enrollment if you exceed the limit. "
        "Check your balance anytime by asking *'My credit hours'*.",
        ["My credit hours", "My enrollments", "How to enroll"],
    ),
    (
        ["online", "hybrid", "in person", "format", "mode belajar"],
        "**Delivery formats:**\n"
        "• **In-Person** — face-to-face at campus\n"
        "• **Online** — fully remote\n"
        "• **Hybrid** — mix of both\n"
        "• **Any** — no preference, all formats considered\n\n"
        "Set your preference in **Tune** to improve recommendation accuracy.",
        ["Set preferences", "My recommendations"],
    ),
    (
        ["bye", "goodbye", "see you", "selamat tinggal"],
        "Goodbye! Feel free to come back anytime. Good luck with your studies at UITM!",
        ["Show faculties", "My recommendations"],
    ),
]
