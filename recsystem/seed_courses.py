"""UITM course catalog — minimum 10 courses per faculty with auto-generated timetables."""

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SLOTS = [
    ("08:00:00", "10:00:00"),
    ("10:00:00", "12:00:00"),
    ("14:00:00", "16:00:00"),
    ("16:00:00", "18:00:00"),
]

LECTURERS = [
    "Dr. Ahmad Faizal bin Mohd Zaid",
    "Prof. Madya Dr. Siti Nurhaliza binti Ahmad",
    "Dr. Hafiz bin Abdullah",
    "Prof. Dr. Mohd Rizal bin Ismail",
    "Dr. Norazlina binti Yusof",
    "Dr. Zulkifli bin Mohd Nor",
    "Dr. Azman bin Sulaiman",
    "Prof. Madya Dr. Nurul Ain binti Hassan",
    "Dr. Farhan bin Mohd Salleh",
    "Dr. Aminah binti Ismail",
    "Dr. Faridah binti Omar",
    "Prof. Dr. Khairul Anuar bin Musa",
    "Dr. Siti Aisyah binti Rahman",
    "Prof. Madya Dr. Hazman bin Yusof",
    "Dr. Roslina binti Mohd Ali",
    "Dr. Kamal bin Hussin",
    "Dr. Nur Izzati binti Zakaria",
    "Dr. Melissa binti Abdullah",
    "Dr. Amirul bin Hakim",
    "Prof. Madya Dr. Sharifah binti Omar",
    "Dr. Ikhwan bin Saad",
    "Dr. Wan Nurul Ain binti Wan Ismail",
    "Dr. Azizah binti Mohd Tahir",
    "Dr. Mohd Firdaus bin Hamzah",
    "Prof. Madya Dr. Salmah binti Karim",
    "Dr. Hisham bin Omar",
    "Dr. Syafiq bin Ramli",
    "Dr. Nadia binti Mohd Yusof",
    "Prof. Madya Dr. Irwan bin Hashim",
    "Dr. Farah Liyana binti Saad",
]

VENUES = {
    "FSKM": ["DK FSKM 1", "DK FSKM 2", "DK FSKM 3", "Makmal CSC 1", "Makmal CSC 2"],
    "FK": ["DK FK 1", "DK FK 2", "DK FK 3", "Makmal EEC", "Bengkel Kejuruteraan"],
    "FPP": ["DK FPP 1", "DK FPP 2", "DK FPP 3", "Bilik Seminar Perniagaan"],
    "FSSSK": ["DK FSSSK 1", "DK FSSSK 2", "DK FSSSK 3", "Bilik Tutorial Sosial"],
    "FSKT": ["Studio FSKT 1", "Studio FSKT 2", "Studio Muzik", "Studio TV", "Galeri Seni"],
    "FPA": ["DK FPA 1", "DK FPA 2", "Makmal FPA 1", "Makmal FPA 2", "Ladang Demo"],
}

# (code, title, description, difficulty, credits, tags, format)
CATALOG: dict[str, list[tuple]] = {
    "FSKM": [
        ("CSC248", "Fundamentals of Data Structure", "Struktur data asas, linked list, stack, queue dan analisis algoritma.", "Intermediate", 3, "struktur-data,algoritma,programming", "In-Person"),
        ("CSC264", "Computer Organization and Architecture", "Organisasi komputer, memory, instruction set dan performance.", "Intermediate", 3, "komputer,architecture,hardware", "Hybrid"),
        ("MAT112", "Algebra", "Algebra linear asas, matriks dan sistem persamaan linear.", "Beginner", 3, "algebra,mathematics,matriks", "In-Person"),
        ("ITS413", "IT Project Management", "Pengurusan projek IT mengikut metodologi industri.", "Advanced", 4, "projek,IT,pengurusan", "Hybrid"),
        ("STA115", "Introduction to Statistics", "Konsep statistik asas, kebarangkalian dan taburan data.", "Beginner", 3, "statistik,probability,data", "In-Person"),
        ("CTU241", "Fundamentals of Islamic Economics", "Ekonomi Islam asas untuk pelajar UITM.", "Beginner", 2, "ekonomi-islam,CTU", "Online"),
        ("CSC126", "Programming Techniques", "Teknik pengaturcaraan berstruktur menggunakan C++.", "Beginner", 3, "programming,c++,asas", "In-Person"),
        ("CSC186", "Database Management", "Pangkalan data, SQL, normalisasi dan reka bentuk DB.", "Intermediate", 3, "database,SQL,rekabentuk", "Hybrid"),
        ("CSC277", "Web Engineering", "Pembangunan web dinamik, API dan keselamatan aplikasi.", "Intermediate", 3, "web,engineering,API", "Hybrid"),
        ("CSC339", "Artificial Intelligence", "AI asas, search algorithm, knowledge representation.", "Advanced", 3, "AI,machine-learning,intelligent", "In-Person"),
        ("ICT707", "Information Security", "Keselamatan maklumat, kriptografi dan audit sistem.", "Advanced", 3, "security,kriptografi,ICT", "Hybrid"),
        ("MAT182", "Calculus for Computer Science", "Kalkulus untuk aplikasi sains komputer.", "Intermediate", 3, "calculus,mathematics,CS", "In-Person"),
    ],
    "FK": [
        ("EEE443", "Electrical Machines", "Mesin elektrik, transformer dan aplikasi kuasa.", "Advanced", 3, "elektrik,mesin,kuasa", "In-Person"),
        ("MEC411", "Thermodynamics", "Termodinamik asas, hukum dan aplikasi kejuruteraan.", "Advanced", 3, "termodinamik,kejuruteraan,mekanikal", "In-Person"),
        ("EEC301", "Circuit Theory", "Teori litar, analisis DC/AC dan komponen elektronik.", "Intermediate", 3, "litar,elektronik,kejuruteraan", "Hybrid"),
        ("CCE404", "Construction Technology", "Teknologi pembinaan moden dan amalan industri.", "Intermediate", 3, "pembinaan,teknologi,sivil", "In-Person"),
        ("EEE240", "Electrical Circuit Analysis", "Analisis litar elektrik dan hukum asas.", "Beginner", 3, "litar,elektrik,asas", "In-Person"),
        ("MEC291", "Engineering Mechanics", "Mekanik kejuruteraan, daya dan gerakan.", "Beginner", 3, "mekanik,daya,kejuruteraan", "In-Person"),
        ("CHE241", "Chemical Process Principles", "Prinsip proses kimia dan operasi unit.", "Intermediate", 3, "kimia,proses,kejuruteraan", "Hybrid"),
        ("CIV209", "Structural Analysis", "Analisis struktur dan reka bentuk asas.", "Intermediate", 3, "struktur,sivil,analisis", "In-Person"),
        ("MEC303", "Fluid Mechanics", "Mekanik bendalir untuk aplikasi kejuruteraan.", "Intermediate", 3, "bendalir,mekanikal,kejuruteraan", "In-Person"),
        ("EEE305", "Power Electronics", "Elektronik kuasa dan sistem penukaran tenaga.", "Advanced", 3, "kuasa,elektronik,tenaga", "Hybrid"),
        ("MEC415", "Machine Design", "Reka bentuk mesin dan pemilihan bahan.", "Advanced", 3, "mesin,reka-bentuk,mekanikal", "In-Person"),
        ("CIV310", "Geotechnical Engineering", "Kejuruteraan geoteknik dan sifat tanah.", "Advanced", 3, "geoteknik,tanah,sivil", "In-Person"),
    ],
    "FPP": [
        ("BBP3203", "Organizational Theory", "Teori organisasi dan tingkah laku dalam perniagaan.", "Intermediate", 3, "organisasi,perniagaan,pengurusan", "In-Person"),
        ("MKT420", "International Marketing", "Pemasaran antarabangsa dan strategi global.", "Advanced", 3, "pemasaran,antarabangsa,perniagaan", "Hybrid"),
        ("FIN302", "Corporate Finance", "Kewangan korporat, pelaburan dan struktur modal.", "Intermediate", 3, "kewangan,korporat,pelaburan", "In-Person"),
        ("ENT600", "Fundamentals of Entrepreneurship", "Asas keusahawanan dan pembangunan perniagaan.", "Advanced", 4, "keusahawanan,startup,perniagaan", "Hybrid"),
        ("ACT797", "Advanced Financial Accounting", "Perakaunan kewangan lanjutan dan pelaporan.", "Advanced", 3, "perakaunan,kewangan,pelaporan", "In-Person"),
        ("MKT340", "Consumer Behaviour", "Tingkah laku pengguna dan analisis pasaran.", "Intermediate", 3, "pengguna,pemasaran,tingkah-laku", "In-Person"),
        ("FIN248", "Fundamentals of Finance", "Asas kewangan, nilai masa wang dan risiko.", "Beginner", 3, "kewangan,asas,pelaburan", "In-Person"),
        ("QBM363", "Business Statistics", "Statistik untuk analisis perniagaan.", "Intermediate", 3, "statistik,perniagaan,analisis", "Hybrid"),
        ("MAN503", "Strategic Management", "Pengurusan strategik dan perancangan organisasi.", "Advanced", 3, "strategi,pengurusan,organisasi", "In-Person"),
        ("BBP561", "Business Ethics", "Etika perniagaan dan tanggungjawab korporat.", "Intermediate", 3, "etika,perniagaan,korporat", "Online"),
        ("HRM310", "Human Resource Management", "Pengurusan sumber manusia dan pembangunan staf.", "Intermediate", 3, "HR,sumber-manusia,pengurusan", "In-Person"),
        ("MKT250", "Principles of Marketing", "Prinsip pemasaran dan strategi asas.", "Beginner", 3, "pemasaran,asas,strategi", "In-Person"),
    ],
    "FSSSK": [
        ("PAD170", "Malaysian Studies", "Pengajian Malaysia dan identiti kebangsaan.", "Beginner", 2, "pengajian-malaysia,CTU", "In-Person"),
        ("SOC101", "Introduction to Sociology", "Pengenalan sosiologi dan analisis masyarakat.", "Beginner", 3, "sosiologi,masyarakat,sains-sosial", "In-Person"),
        ("PSY204", "Developmental Psychology", "Psikologi perkembangan dari kanak-kanak hingga dewasa.", "Intermediate", 3, "psikologi,perkembangan,sains-sosial", "Hybrid"),
        ("LCC401", "English for Professional Communication", "Komunikasi profesional dalam Bahasa Inggeris.", "Intermediate", 3, "bahasa-inggeris,komunikasi,profesional", "In-Person"),
        ("LIS100", "Introduction to Information Studies", "Pengenalan pengajian maklumat dan perpustakaan.", "Beginner", 3, "maklumat,perpustakaan,asas", "In-Person"),
        ("ANT101", "Introduction to Anthropology", "Antropologi budaya dan masyarakat.", "Beginner", 3, "antropologi,budaya,sosial", "In-Person"),
        ("POL101", "Introduction to Political Science", "Sains politik dan sistem kerajaan.", "Beginner", 3, "politik,kerajaan,sosial", "In-Person"),
        ("COM201", "Mass Communication", "Komunikasi massa dan media digital.", "Intermediate", 3, "media,komunikasi,digital", "Hybrid"),
        ("PSY305", "Industrial Psychology", "Psikologi industri dan organisasi kerja.", "Advanced", 3, "psikologi,industri,organisasi", "In-Person"),
        ("HIS101", "World History", "Sejarah dunia dan tamadun global.", "Beginner", 3, "sejarah,tamadun,sosial", "In-Person"),
        ("SOC310", "Social Research Methods", "Kaedah penyelidikan sosial dan analisis data.", "Advanced", 3, "penyelidikan,sosial,kaedah", "Hybrid"),
        ("PAD240", "Islamic Civilization", "Tamadun Islam dan sumbangan kepada dunia.", "Beginner", 2, "islam,tamadun,CTU", "Online"),
    ],
    "FSKT": [
        ("GID3023", "Graphic Design Studio", "Studio reka bentuk grafik dan aplikasi kreatif.", "Intermediate", 3, "reka-bentuk,grafik,kreatif", "In-Person"),
        ("MUS105", "Music Theory Fundamentals", "Teori muzik asas dan notasi.", "Beginner", 3, "muzik,teori,seni", "In-Person"),
        ("TDT473", "Television Production", "Pengeluaran program televisyen dan penyiaran.", "Advanced", 4, "televisyen,penyiaran,media", "Hybrid"),
        ("ARC101", "Introduction to Architecture", "Pengenalan seni bina dan prinsip reka bentuk.", "Beginner", 3, "seni-bina,reka-bentuk,kreatif", "In-Person"),
        ("GID3012", "Typography and Layout", "Tipografi, susun atur dan identiti visual.", "Intermediate", 3, "tipografi,layout,grafik", "In-Person"),
        ("FAS143", "Fundamentals of Drawing", "Asas lukisan dan teknik perwatakan.", "Beginner", 3, "lukisan,seni,asas", "In-Person"),
        ("IND301", "Industrial Design", "Reka bentuk industri dan prototaip produk.", "Intermediate", 3, "industri,reka-bentuk,produk", "Hybrid"),
        ("MUS204", "Music Composition", "Penggubahan muzik dan aransemen.", "Intermediate", 3, "muzik,gubahan,aransemen", "In-Person"),
        ("TDT320", "Digital Media Production", "Pengeluaran media digital dan pasca-produksi.", "Intermediate", 3, "media,digital,produksi", "Hybrid"),
        ("ARC204", "Building Technology", "Teknologi bangunan dan bahan binaan.", "Intermediate", 3, "bangunan,teknologi,seni-bina", "In-Person"),
        ("GID4010", "Advanced Visual Communication", "Komunikasi visual lanjutan dan branding.", "Advanced", 3, "visual,branding,komunikasi", "In-Person"),
        ("FAS210", "Painting Techniques", "Teknik lukisan dan medium seni.", "Intermediate", 3, "lukisan,teknik,seni", "In-Person"),
    ],
    "FPA": [
        ("HFF225", "Food Chemistry", "Kimia makanan dan komposisi nutrien.", "Intermediate", 3, "makanan,kimia,teknologi-makanan", "In-Person"),
        ("LBS101", "Introduction to Plantation Management", "Pengurusan ladang dan asas perladangan.", "Beginner", 3, "perladangan,pengurusan,agroteknologi", "In-Person"),
        ("BIO302", "Plant Biotechnology", "Bioteknologi tumbuhan dan aplikasi pertanian.", "Advanced", 3, "bioteknologi,tumbuhan,pertanian", "Hybrid"),
        ("ANS101", "Animal Anatomy", "Anatomi haiwan asas untuk sains veterinar.", "Beginner", 3, "anatomi,haiwan,veterinar", "In-Person"),
        ("FST200", "Food Microbiology", "Mikrobiologi makanan dan keselamatan makanan.", "Intermediate", 3, "mikrobiologi,makanan,keselamatan", "In-Person"),
        ("AGR101", "Introduction to Agriculture", "Pengenalan pertanian dan sistem tanaman.", "Beginner", 3, "pertanian,tanaman,asas", "In-Person"),
        ("HFF301", "Food Product Development", "Pembangunan produk makanan dan inovasi.", "Advanced", 3, "produk,makanan,inovasi", "Hybrid"),
        ("LBS204", "Oil Palm Management", "Pengurusan ladang kelapa sawit.", "Intermediate", 3, "kelapa-sawit,ladang,perladangan", "In-Person"),
        ("BIO401", "Molecular Biology", "Biologi molekul untuk aplikasi pertanian.", "Advanced", 3, "molekul,biologi,pertanian", "In-Person"),
        ("ANS204", "Animal Nutrition", "Nutrisi haiwan dan formulasi makanan ternakan.", "Intermediate", 3, "nutrisi,haiwan,ternakan", "In-Person"),
        ("AGR310", "Crop Science", "Sains tanaman dan pengurusan hasil.", "Intermediate", 3, "tanaman,hasil,pertanian", "In-Person"),
        ("FST110", "Food Processing Technology", "Teknologi pemprosesan makanan asas.", "Beginner", 3, "pemprosesan,makanan,teknologi", "In-Person"),
    ],
}


def get_all_courses() -> list[dict]:
    courses = []
    lecturer_idx = 0
    for faculty, items in CATALOG.items():
        for item in items:
            code, title, desc, diff, credits, tags, fmt = item
            courses.append({
                "code": code,
                "title": title,
                "description": desc,
                "faculty": faculty,
                "difficulty": diff,
                "duration_weeks": 14,
                "format": fmt,
                "credits": credits,
                "tags": tags,
                "rating": round(4.0 + (lecturer_idx % 7) * 0.08, 2),
                "instructor": LECTURERS[lecturer_idx % len(LECTURERS)],
            })
            lecturer_idx += 1
    return courses


def schedule_for_course(course_index: int, faculty: str, code: str) -> list[dict]:
    day = DAYS[course_index % len(DAYS)]
    slot = SLOTS[(course_index // len(DAYS)) % len(SLOTS)]
    venue = VENUES[faculty][course_index % len(VENUES[faculty])]
    session = "Tutorial" if course_index % 4 == 3 else "Kuliah"
    return [{
        "day": day,
        "start_time": slot[0],
        "end_time": slot[1],
        "venue": venue,
        "session_type": session,
    }]


def seed_database(conn) -> dict:
    courses = get_all_courses()
    with conn.cursor() as cur:
        for i, c in enumerate(courses):
            cur.execute(
                """INSERT INTO courses
                   (code, title, description, faculty, difficulty, duration_weeks,
                    format, credits, tags, rating, instructor)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    c["code"], c["title"], c["description"], c["faculty"],
                    c["difficulty"], c["duration_weeks"], c["format"],
                    c["credits"], c["tags"], c["rating"], c["instructor"],
                ),
            )
            course_id = cur.lastrowid
            for sched in schedule_for_course(i, c["faculty"], c["code"]):
                cur.execute(
                    """INSERT INTO course_schedules
                       (course_id, day, start_time, end_time, venue, session_type)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (
                        course_id, sched["day"], sched["start_time"],
                        sched["end_time"], sched["venue"], sched["session_type"],
                    ),
                )

    conn.commit()
    by_faculty = {}
    for c in courses:
        by_faculty[c["faculty"]] = by_faculty.get(c["faculty"], 0) + 1
    return {"total": len(courses), "by_faculty": by_faculty}
