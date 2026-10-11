from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re

@dataclass
class SubjectConfig:
    name: str
    keywords: List[str] # Primary keywords (e.g., "ban", "eng")
    aliases: List[str]   # Full name variations

SUBJECT_DATA = {
    "SSC": {
        "Accounting": SubjectConfig("Accounting", ["acc"], ["accounting"]),
        "Agriculture": SubjectConfig("Agriculture", ["agri"], ["agriculture"]),
        "Bangla 1st & 2nd Paper": SubjectConfig("Bangla 1st & 2nd Paper", ["ban"], ["bangla"]),
        "Bangladesh & Global Studies": SubjectConfig("Bangladesh & Global Studies", ["bgs"], ["global studies"]),
        "Biology": SubjectConfig("Biology", ["bio"], ["biology"]),
        "Business Entrepreneurship": SubjectConfig("Business Entrepreneurship", ["entrepreneur"], ["business entrepreneurship"]),
        "Chemistry": SubjectConfig("Chemistry", ["chem"], ["chemistry"]),
        "Civics & Citizenship": SubjectConfig("Civics & Citizenship", ["civics"], ["citizenship"]),
        "Economics": SubjectConfig("Economics", ["econ"], ["economics"]),
        "English 1st & 2nd Paper": SubjectConfig("English 1st & 2nd Paper", ["eng"], ["english"]),
        "Finance & Banking": SubjectConfig("Finance & Banking", ["fin", "bank"], ["finance", "banking"]),
        "General Science": SubjectConfig("General Science", ["gen sci"], ["general science"]),
        "Geography & Environment": SubjectConfig("Geography & Environment", ["geo"], ["geography"]),
        "Higher Mathematics": SubjectConfig("Higher Mathematics", ["hmath"], ["higher math", "higher mathematics"]),
        "Hindu Religion & Moral Education": SubjectConfig("Hindu Religion & Moral Education", ["hindu"], ["hindu religion"]),
        "History of Bangladesh & World Civilization": SubjectConfig("History of Bangladesh & World Civilization", ["hist"], ["history"]),
        "Home Science": SubjectConfig("Home Science", ["home sci"], ["home science"]),
        "ICT": SubjectConfig("ICT", ["ict"], ["information tech"]),
        "Islam & Moral Education": SubjectConfig("Islam & Moral Education", ["islam"], ["islamic"]),
        "Mathematics": SubjectConfig("Mathematics", ["math"], ["mathematics"]),
        "Vocational Subjects": SubjectConfig("Vocational Subjects", ["voc"], ["vocational"]),
    },
    "HSC": {
        "Bangla 1st & 2nd Paper": SubjectConfig("Bangla 1st & 2nd Paper", ["ban"], ["bangla"]),
        "Biology 1st & 2nd Paper": SubjectConfig("Biology 1st & 2nd Paper", ["bio"], ["biology"]),
        "Business Organization & Management 1st & 2nd Paper": SubjectConfig("Business Organization & Management 1st & 2nd Paper", ["bom"], ["business organization"]),
        "Chemistry 1st & 2nd Paper": SubjectConfig("Chemistry 1st & 2nd Paper", ["chem"], ["chemistry"]),
        "Civics 1st & 2nd Paper": SubjectConfig("Civics 1st & 2nd Paper", ["civics"], ["civics"]),
        "Economics 1st & 2nd Paper": SubjectConfig("Economics 1st & 2nd Paper", ["econ"], ["economics"]),
        "EV Mathematics": SubjectConfig("EV Mathematics", ["evmath"], ["ev math", "english version math"]),
        "Finance, Banking & Insurance 1st & 2nd Paper": SubjectConfig("Finance, Banking & Insurance 1st & 2nd Paper", ["fin", "bank", "ins"], ["finance", "banking", "insurance"]),
        "Geography 1st & 2nd Paper": SubjectConfig("Geography 1st & 2nd Paper", ["geo"], ["geography"]),
        "Higher Mathematics 1st & 2nd Paper": SubjectConfig("Higher Mathematics 1st & 2nd Paper", ["hmath"], ["higher math", "higher mathematics"]),
        "History 1st & 2nd Paper": SubjectConfig("History 1st & 2nd Paper", ["hist"], ["history"]),
        "Home Science 1st & 2nd Paper": SubjectConfig("Home Science 1st & 2nd Paper", ["home sci"], ["home science"]),
        "ICT": SubjectConfig("ICT", ["ict"], ["information tech"]),
        "Islam": SubjectConfig("Islam", ["islam"], ["islamic"]),
        "Islamic History & Culture 1st & 2nd Paper": SubjectConfig("Islamic History & Culture 1st & 2nd Paper", ["ishc"], ["islamic history"]),
        "Logic 1st & 2nd Paper": SubjectConfig("Logic 1st & 2nd Paper", ["logic"], ["logic"]),
        "Mathematics": SubjectConfig("Mathematics", ["math"], ["mathematics"]),
        "Physics 1st & 2nd Paper": SubjectConfig("Physics 1st & 2nd Paper", ["phys"], ["physics"]),
        "Psychology 1st & 2nd Paper": SubjectConfig("Psychology 1st & 2nd Paper", ["psych"], ["psychology"]),
        "Social Work": SubjectConfig("Social Work", ["sw"], ["social work"]),
        "Sociology 1st & 2nd Paper": SubjectConfig("Sociology 1st & 2nd Paper", ["soc"], ["sociology"]),
        "Statistics 1st & 2nd Paper": SubjectConfig("Statistics 1st & 2nd Paper", ["stat"], ["statistics"]),
        "English 1st & 2nd Paper": SubjectConfig("English 1st & 2nd Paper", ["eng"], ["english"]),
    }
}

class CategorizationEngine:
    def __init__(self):
        self.config = SUBJECT_DATA

    def normalize(self, text: str) -> str:
        text = text.lower()
        # Replace underscores/hyphens with spaces to allow keyword matching
        text = re.sub(r'[_\-]', ' ', text)
        return text

    def detect(self, filename: str, relative_path: str = "") -> Dict:
        full_context = f"{relative_path} {filename}"
        norm_context = self.normalize(full_context)
        
        level = None
        if "ssc" in norm_context:
            level = "SSC"
        elif "hsc" in norm_context:
            level = "HSC"
            
        if not level:
            return {"level": None, "subject": None, "confidence": 0, "status": "review_required", "reason": "Could not detect SSC or HSC"}

        level_subjects = self.config[level]
        best_subject = None
        max_score = 0
        
        # Handle EV Math first for HSC as it's a specific case
        if level == "HSC":
            if "evmath" in norm_context.replace(" ", "") or "ev math" in norm_context:
                return {"level": "HSC", "subject": "EV Mathematics", "confidence": 1.0, "status": "categorized", "reason": "Matched EV Math"}
            
        # Prioritize longer keywords/aliases to prevent "Math" matching "Higher Math"
        sorted_subjects = sorted(level_subjects.items(), key=lambda x: len(x[0]), reverse=True)
        
        for sub_name, sub_cfg in sorted_subjects:
            # Check short keywords first with strict boundaries (e.g. _ban_ or ban )
            # We add boundaries to prevent 'ban' matching 'bandana'
            score = 0
            for kw in sub_cfg.keywords:
                pattern = rf"\b{kw}\b"
                if re.search(pattern, norm_context):
                    score = 1.0
                    break
            
            if score < 1.0:
                for alias in sub_cfg.aliases:
                    if alias in norm_context:
                        score = 0.8
                        break
            
            if score > max_score:
                max_score = score
                best_subject = sub_name
                if score == 1.0: break

        if not best_subject:
            return {"level": level, "subject": None, "confidence": 0, "status": "uncategorized", "reason": "Subject not recognized"}
            
        if max_score < 0.8:
            return {"level": level, "subject": best_subject, "confidence": max_score, "status": "review_required", "reason": "Low confidence match"}

        return {
            "level": level,
            "subject": best_subject,
            "confidence": max_score,
            "status": "categorized",
            "reason": "Matched subject"
        }
