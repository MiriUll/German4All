from pydantic import BaseModel
from enum import Enum

class ContentPreservation(Enum):
    FALSCH = "falsch"
    UNGEFAEHR = "ungefaehr"
    RICHTIG = "richtig"

class InformationLevel(Enum):
    NIE = "nie"
    SELTEN = "selten"
    MANCHMAL = "manchmal"
    HAEUFIG = "haeufig"

class TypeOfAddition(Enum):
    AUSSCHMUECKUNGEN = "Ausschmueckungen"
    #ERKLAERUNGEN = "Erklaerungen / Definitionen"
    ERKLAERUNGEN = "Erklaerungen/Definitionen"
    #FAKTISCH_INKORREKT = "Faktisch inkorrekte Informationen"
    FAKTISCH_INKORREKT = "Faktisch_inkorrekte_Informationen"
    #FAKTISCH_KORREKT = "Faktisch korrekte Informationen"
    FAKTISCH_KORREKT = "Faktisch_korrekte_Informationen"
    ANDERE = "Andere"
    NAN = "NaN"

class ComplexityLevel(Enum):
    #ZU_EINFACH = "zu einfach"
    ZU_EINFACH = "zu_einfach"
    #ETWAS_ZU_EINFACH = "etwas zu einfach"
    ETWAS_ZU_EINFACH = "etwas_zu_einfach"
    PASSEND = "passend"
    #ETWAS_ZU_KOMPLIZIERT = "etwas zu kompliziert"
    ETWAS_ZU_KOMPLIZIERT = "etwas_zu_kompliziert"
    #ZU_KOMPLIZIERT = "zu kompliziert"
    ZU_KOMPLIZIERT = "zu_kompliziert"

class Evaluation(BaseModel):
    content_preservation: ContentPreservation
    information_loss: InformationLevel
    information_addition: InformationLevel
    type_of_addition: list[TypeOfAddition]  # List allows multiple selections
    complexity_level: ComplexityLevel


eval_mapping = {
    "Die Paraphrasierung gibt den Inhalt des Originaltexts ... wieder.": "content_preservation",
    "Wie häufig wurden Informationen aus dem Originaltext in der Paraphrasierung ausgelassen? ": "information_loss",
    "Wie oft wurden zusätzliche Informationen in der Paraphrasierung hinzugefügt, die im Originaltext nicht vorhanden waren?": "information_addition",
    """Überspringe diese Frage, falls du in der vorherigen Frage "nie" ausgewählt hast.
Welche Arten von zusätzlichen Informationen wurden hinzugefügt? Mehrere Optionen können ausgewählt werden.""": "type_of_addition",
    "Die Paraphrasierung ist für die gewünschte Schwierigkeitsstufe ...": "complexity_level",
    "compared_to_lower": "compared_complexity_level",
}

mapping_content_preservation = {
    "falsch": 1, "wrong": 1,
    "ungefähr": 2, "ungefaehr": 2, "approximately": 2,
    "richtig": 3, "correct": 3
}

# question 2 and 3
mapping_information = {
    "nie": 1, "never": 1,
    "selten": 2, "seldom": 2,
    "manchmal": 3, "sometimes": 3,
    "häufig": 4, "haeufig": 4, "often": 4
}

# question 5
mapping_complexity = {
    "zu einfach": 1, "zu_einfach": 1, "too easy": 1,
    "etwas zu einfach": 2, "etwas_zu_einfach": 2, "a little too easy": 2,
    "passend": 3, "suitable": 3,
    "etwas zu kompliziert": 4, "etwas_zu_kompliziert": 4, "a little too complicated": 4,
    "zu kompliziert": 5, "zu_kompliziert": 5, "too complicated": 5
}

class ComplexityCompare(Enum):
    VIEL_EINFACHER_ALS = "viel_einfacher_als"
    ETWAS_EINFACHER_ALS = "etwas_einfacher_als"
    GLEICH_WIE = "gleich_wie"
    ETWAS_KOMPLIZIERTER_ALS = "etwas_komplizierter_als"
    VIEL_KOMPLIZIERTER_ALS = "viel_komplizierter_als"

class Comparison(BaseModel):
    compared_complexity_level: ComplexityCompare

# question 6 (for all complexity levels except 1)
mapping_compare = {
    "viel einfacher als": 1, "viel_einfacher_als": 1,
    "etwas einfacher als": 2, "etwas_einfacher_als": 2,
    "gleich wie": 3, "gleich_wie": 3,
    "etwas komplizierter als": 4, "etwas_komplizierter_als": 4,
    "viel komplizierter als": 5, "viel_komplizierter_als": 5,
}

metric_mapping = {
    "content_preservation": mapping_content_preservation,
    "information_loss": mapping_information,
    "information_addition": mapping_information,
    "complexity_level": mapping_complexity,
    "compared_complexity_level": mapping_compare,
}