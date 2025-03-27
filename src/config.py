
keywords = {
    "shared_interest": [
        "love", "like", "enjoy", "passion", "hobby", "interest", "games",
        "sports", "music", "movies", "books", "reading", "art", "drawing",
        "painting", "writing", "creative", "dancing", "theater", "acting",
        "outdoors", "hiking", "camping", "travel", "adventure", "photography",
        "fitness", "exercise", "gym", "technology", "coding", "anime", "gaming",
        "board games", "strategy games", "puzzle", "cooking", "baking"
    ],
    
    "career": [
        "career", "job", "work", "goal", "future", "internship", "education",
        "college", "university", "study", "skills", "learning", "profession",
        "aspiration", "training", "employment", "resume", "interview", "networking",
        "mentorship", "scholarship", "certification", "growth", "promotion",
        "company", "business", "entrepreneur", "freelance", "industry", "field",
        "research", "technology", "engineering", "medical", "law", "finance",
        "science", "teaching", "management", "leadership", "trade", "construction",
        "coding", "startup", "job market", "salary", "income"
    ],
    
    "location": [
        "neighborhood", "city", "state", "close", "near", "distance",
        "same area", "nearby", "local", "region", "town", "village", "suburb",
        "downtown", "urban", "rural", "relocate", "move", "transportation",
        "commute", "drive", "bus", "train", "subway", "car", "bike", "walking",
        "travel time", "home", "apartment", "house", "living situation"
    ],
    
    "family": [
        "single parent", "siblings", "family", "home", "mom", "dad", "guardian",
        "grandparents", "cousins", "aunt", "uncle", "foster", "adoption",
        "step-parent", "step-sibling", "relative", "household", "parents",
        "childhood", "raising", "support system", "home life", "kids", "parenting",
        "family values", "responsibility", "brother", "sister", "niece", "nephew"
    ],
    
    "volunteering": [
        "volunteer", "help", "community", "leadership", "giving back",
        "nonprofit", "charity", "service", "mentor", "tutor", "teaching",
        "fundraising", "social work", "outreach", "activism", "advocacy",
        "awareness", "support", "public service", "coaching", "guidance",
        "mentorship", "helping others", "environmental work", "animal shelter",
        "soup kitchen", "homeless", "donation", "relief work", "medical aid",
        "youth program", "elderly care", "social good", "positive impact",
        "teamwork", "organizing", "initiatives", "volunteer work"
    ]
}

# Comprehensive Job Mapping (Based on provided list)
job_attributes = {
    # Students
    "Student: High School": {"rigidity": 1, "fixed_schedule": 0, "income_level": 1, "stability": 1},
    "Student: College": {"rigidity": 1, "fixed_schedule": 0, "income_level": 1, "stability": 2},

    # Medical Professions
    "Medical: Nurse": {"rigidity": 5, "fixed_schedule": 1, "income_level": 4, "stability": 5},
    "Medical: Doctor, Provider": {"rigidity": 5, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Medical: Pharmacist": {"rigidity": 5, "fixed_schedule": 1, "income_level": 4, "stability": 5},
    "Medical: Admin": {"rigidity": 4, "fixed_schedule": 1, "income_level": 3, "stability": 5},
    "Medical: Healthcare Worker": {"rigidity": 5, "fixed_schedule": 1, "income_level": 3, "stability": 4},

    # Business & Finance
    "Business: Marketing": {"rigidity": 3, "fixed_schedule": 1, "income_level": 4, "stability": 4},
    "Business: Sales": {"rigidity": 3, "fixed_schedule": 1, "income_level": 3, "stability": 4},
    "Business: Mgt, Admin": {"rigidity": 4, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Finance": {"rigidity": 4, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Finance: Accountant": {"rigidity": 4, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Finance: Banking": {"rigidity": 4, "fixed_schedule": 1, "income_level": 5, "stability": 5},

    # Self-Employed
    "Self-Employed, Entrepreneur": {"rigidity": 1, "fixed_schedule": 0, "income_level": 3, "stability": 2},
    
    # Law Enforcement
    "Law: Police Officer": {"rigidity": 5, "fixed_schedule": 1, "income_level": 4, "stability": 5},
    "Law: Lawyer": {"rigidity": 5, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Law: Paralegal": {"rigidity": 4, "fixed_schedule": 1, "income_level": 4, "stability": 4},
    "Law: Security Officer": {"rigidity": 4, "fixed_schedule": 1, "income_level": 3, "stability": 3},

    # Retail & Hospitality
    "Retail: Sales": {"rigidity": 2, "fixed_schedule": 0, "income_level": 2, "stability": 2},
    "Retail: Mgt": {"rigidity": 3, "fixed_schedule": 1, "income_level": 3, "stability": 4},
    "Service: Restaurant": {"rigidity": 2, "fixed_schedule": 0, "income_level": 2, "stability": 2},
    "Service: Hotel": {"rigidity": 2, "fixed_schedule": 0, "income_level": 2, "stability": 2},
    
    # Education
    "Education: Teacher": {"rigidity": 4, "fixed_schedule": 1, "income_level": 3, "stability": 5},
    "Education: College Professor": {"rigidity": 4, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Education: Teacher Asst/Aid": {"rigidity": 3, "fixed_schedule": 1, "income_level": 2, "stability": 4},

    # Tech & Engineering
    "Tech: Computer/Programmer": {"rigidity": 3, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Tech: Engineer": {"rigidity": 4, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Tech: Sales, Mktg": {"rigidity": 3, "fixed_schedule": 1, "income_level": 4, "stability": 4},

    # Others
    "Consultant": {"rigidity": 2, "fixed_schedule": 0, "income_level": 4, "stability": 4},
    "Transport: Pilot": {"rigidity": 5, "fixed_schedule": 1, "income_level": 5, "stability": 5},
    "Firefighter": {"rigidity": 5, "fixed_schedule": 1, "income_level": 4, "stability": 5},
    "Journalist/Media": {"rigidity": 3, "fixed_schedule": 1, "income_level": 4, "stability": 4},
    "Agriculture": {"rigidity": 2, "fixed_schedule": 0, "income_level": 2, "stability": 3},
    "Military": {"rigidity": 5, "fixed_schedule": 1, "income_level": 4, "stability": 5},
    "Unemployed": {"rigidity": 1, "fixed_schedule": 0, "income_level": 1, "stability": 1},
    "Retired": {"rigidity": 1, "fixed_schedule": 0, "income_level": 2, "stability": 5},
}

# Default category for unknown occupations
default_attributes = {"rigidity": 3, "fixed_schedule": 1, "income_level": 3, "stability": 3}

# columns to be modified
# todo: remove all "contact" and use _
# these columns are either not relevant for match length or missing enormous amount of values (might use then for eda)
to_be_deleted = [
    "Big Employer/School Census Block Group", "Big Enrollment: Created Date", "Big Acceptance Date",
    "Big Contact: Created Date","Big Days Acceptance to Match", "Big Days Interview to Acceptance","Big Days Interview to Match",
    "Big Contact: Preferred Communication Type", "Big Assessment Uploaded", "Big Enrollment: Created Date",
    "Big Employer", "Big Employer/School Census Block Group", "Big Approved Date", "Big Home Census Block Group", "Big Enrollment: Record Type",

    "Big Contact: Interest Finder - Entertainment","Big Contact: Interest Finder - Hobbies","Big Contact: Interest Finder - Places To Go",
    "Big Contact: Interest Finder - Sports","Little Contact: Interest Finder - Arts","Little Contact: Interest Finder - Career",
    "Little Contact: Interest Finder - Entertainment", "Little Contact: Interest Finder - Hobbies", "Little Contact: Interest Finder - Other Interests",
    "Little Contact: Interest Finder - Outdoors","Little Contact: Interest Finder - Personality","Little Contact: Interest Finder - Places To Go",
    "Little Contact: Interest Finder - Sports","Little Contact: Interest Finder - Three Wishes","Little Other Interests",
    "Little Contact: Language(s) Spoken", "Big Contact: Former Big/Little", "Big Level of Education", "Big: Military",
    "Big Languages", "Big Car Access", "Big Open to Cross-Gender Match", "Big Contact: Volunteer Availability", "Big Contact: Marital Status", "Big Re-Enroll", "Big County",
                    

    "Big ID", "Little ID", "Big Assessment Uploaded", 
    "Little Mailing Address Census Block Group", "Little Interview Date", "Little Acceptance Date", "Little Application Received", "Little Moved to RTBM in MF",
    "Little RTBM Date in MF", "Little RTBM in Matchforce", "Little Moved to RTBM in MF", "Little Interview Date", "Little Acceptance Date", "Little RTBM in Matchforce",
]

