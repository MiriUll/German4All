JUDGE_PROMPT_FULL = """
You will be given an original text and its paraphrased version. Both are in German.

The paraphrases can be in 5 different complexity levels. We define those levels as:
1. Leichte Sprache (literal translation: Easy Language)
    - Target group: People with reading difficulties, including people with learning disabilities and those who have only recently started to learn German.
    - Characteristics: Very short sentences, only short and frequently used words, direct speech, avoidance of abbreviations, metaphors, or irony.
    - Examples areas: simple instructions, accessible websites.
2. Simple German for beginners
    - Target group: Non-native speakers with basic knowledge of German.
    - Characteristics: Simple sentence structures, basic vocabulary, strong focus on important information, avoidance of culture-specific expressions.
    - Example areas: Language learning materials, introductory web texts.
3. Commonly used language
    - Target group: General public with different levels of education.
    - Characteristics: Clear, structured sentences, focus on comprehensability, avoidance of technical terms.
    - Example areas: Wide-ranging news portals, blogs.
4. Elevated everyday language
    - Target group: Regular readers with a good understanding of the language.
    - Characteristics: More varied vocabulary, occasional technical terminology with explanations, complex sentence structures.
    - Example areas: Specialist blogs, quality newspapers.
5. Academic language
    - Target group: Academics and experts.
    - Characteristics: Complex sentence structures, specialized terminology, use of technical terms.
    - Example areas: Specialist journals, scientific publications.

Your task is to provide an evaluation of the paraphrasing across these aspects:
content_preservation: The paraphrase resembles the content of the original text. Is this true?
information_loss: How often does the paraphrase miss information from the original text?
information_addition: How often does the paraphrase add information that was not present in the original text?
type_of_addition: If you answered 'never' to the previous question, answer with 'NaN' here. Otherwise, what type of additional information was added?
complexity_level: How well does the paraphrase fit for the given complexity level?

Now here is your input:
Original text: {orig}
Paraphrased text: {para}
Paraphrase complexity level: {cl}
"""

JUDGE_PROMPT_FULL_DE = """
Du bekommst einen Originaltext und eine paraphrasierte Version.

Die Paraphrasen können in 5 verschiedenen Schwierigkeitsstufen vorliegen. Wir definieren diese Stufen wie folgt:
1. Leichte Sprache
    - Zielgruppe: Menschen mit Leseschwierigkeiten, einschließlich Menschen mit Lernschwierigkeiten und Menschen, die erst vor kurzem begonnen haben, Deutsch zu lernen.
    - Merkmale: Sehr kurze Sätze, nur kurze und häufig verwendete Wörter, direkte Rede, Vermeidung von Abkürzungen, Metaphern oder Ironie.
    - Beispiele: einfache Anleitungen, barrierefreie Websites.
2. Einfaches Deutsch für Anfänger
    - Zielgruppen: Nicht-Muttersprachler mit Grundkenntnissen der deutschen Sprache.
    - Merkmale: Einfache Satzstrukturen, Grundwortschatz, starke Konzentration auf wichtige Informationen, Vermeidung von kulturspezifischen Ausdrücken.
    - Beispielbereiche: Sprachlernmaterialien, einführende Webtexte.
3. Häufig verwendete Sprache
    - Zielgruppen: Allgemeine Öffentlichkeit mit unterschiedlichen Bildungsniveaus.
    - Merkmale: Klare, strukturierte Sätze, Fokus auf Verständlichkeit, Vermeidung von Fachbegriffen.
    - Beispielbereiche: Breit gefächerte Nachrichtenportale, Blogs.
4. Gehobene Alltagssprache
    - Zielgruppe: Regelmäßige Leser mit guten Sprachkenntnissen.
    - Merkmale: Vielfältigerer Wortschatz, gelegentlich Fachausdrücke mit Erklärungen, komplexe Satzstrukturen.
    - Beispielbereiche: Fachblogs, Qualitätszeitungen.
5. Akademische Sprache
    - Zielgruppe: Akademiker und Experten.
    - Merkmale: Komplexe Satzstrukturen, Fachterminologie, Verwendung von Fachbegriffen.
    - Beispielbereiche: Fachzeitschriften, wissenschaftliche Publikationen.

Deine Aufgabe ist es, eine Bewertung der Paraphrasierung unter diesen Aspekten abzugeben:
content_preservation: Die Paraphrase ähnelt dem Inhalt des Originaltextes. Stimmt das?
information_loss: Wie oft fehlen in der Paraphrase Informationen des Originaltextes?
information_addition: Wie oft fügt die Paraphrase Informationen hinzu, die im Originaltext nicht vorhanden waren?
type_of_addition: Wenn du auf die vorherige Frage mit „nie“ geantwortet hast, antworte hier mit „NaN“. Andernfalls, welche Art von zusätzlicher Information wurde hinzugefügt?
complexity_level: Wie gut passt die Paraphrase zum angegebenen Komplexitätsgrad?

Das sind die Texte, die du evaluieren sollst:
Ursprünglicher Text: {orig}
Paraphrasierter Text: {para}
Komplexitätsgrad der Paraphrase: {cl}
"""

JUDGE_PROMPT_FULL_SYSTEM = """
Du bekommst einen Originaltext und eine paraphrasierte Version.

Die Paraphrasen können in 5 verschiedenen Schwierigkeitsstufen vorliegen. Wir definieren diese Stufen wie folgt:
1. Leichte Sprache
    - Zielgruppe: Menschen mit Leseschwierigkeiten, einschließlich Menschen mit Lernschwierigkeiten und Menschen, die erst vor kurzem begonnen haben, Deutsch zu lernen.
    - Merkmale: Sehr kurze Sätze, nur kurze und häufig verwendete Wörter, direkte Rede, Vermeidung von Abkürzungen, Metaphern oder Ironie.
    - Beispiele: einfache Anleitungen, barrierefreie Websites.
2. Einfaches Deutsch für Anfänger
    - Zielgruppen: Nicht-Muttersprachler mit Grundkenntnissen der deutschen Sprache.
    - Merkmale: Einfache Satzstrukturen, Grundwortschatz, starke Konzentration auf wichtige Informationen, Vermeidung von kulturspezifischen Ausdrücken.
    - Beispielbereiche: Sprachlernmaterialien, einführende Webtexte.
3. Häufig verwendete Sprache
    - Zielgruppen: Allgemeine Öffentlichkeit mit unterschiedlichen Bildungsniveaus.
    - Merkmale: Klare, strukturierte Sätze, Fokus auf Verständlichkeit, Vermeidung von Fachbegriffen.
    - Beispielbereiche: Breit gefächerte Nachrichtenportale, Blogs.
4. Gehobene Alltagssprache
    - Zielgruppe: Regelmäßige Leser mit guten Sprachkenntnissen.
    - Merkmale: Vielfältigerer Wortschatz, gelegentlich Fachausdrücke mit Erklärungen, komplexe Satzstrukturen.
    - Beispielbereiche: Fachblogs, Qualitätszeitungen.
5. Akademische Sprache
    - Zielgruppe: Akademiker und Experten.
    - Merkmale: Komplexe Satzstrukturen, Fachterminologie, Verwendung von Fachbegriffen.
    - Beispielbereiche: Fachzeitschriften, wissenschaftliche Publikationen.

Deine Aufgabe ist es, eine Bewertung der Paraphrasierung unter diesen Aspekten abzugeben:
content_preservation: Die Paraphrase ähnelt dem Inhalt des Originaltextes. Stimmt das?
information_loss: Wie oft fehlen in der Paraphrase Informationen des Originaltextes?
information_addition: Wie oft fügt die Paraphrase Informationen hinzu, die im Originaltext nicht vorhanden waren?
type_of_addition: Wenn du auf die vorherige Frage mit „nie“ geantwortet hast, antworte hier mit „NaN“. Andernfalls, welche Art von zusätzlicher Information wurde hinzugefügt?
complexity_level: Wie gut passt die Paraphrase zum angegebenen Komplexitätsgrad?
"""

JUDGE_PROMPT_FULL_SYSTEM_NEW = """
Du bekommst einen Originaltext und eine paraphrasierte Version.

Die Paraphrasen können in 5 verschiedenen Schwierigkeitsstufen vorliegen. Wir definieren diese Stufen wie folgt:
1. Leichte Sprache
    - Zielgruppe: Menschen mit Leseschwierigkeiten, einschließlich Menschen mit Lernschwierigkeiten und Menschen, die erst vor kurzem begonnen haben, Deutsch zu lernen.
    - Merkmale: Sehr kurze Sätze, nur kurze und häufig verwendete Wörter, direkte Rede, Vermeidung von Abkürzungen, Metaphern oder Ironie.
    - Beispiele: einfache Anleitungen, barrierefreie Websites.
2. Einfaches Deutsch für Anfänger
    - Zielgruppen: Nicht-Muttersprachler mit Grundkenntnissen der deutschen Sprache.
    - Merkmale: Einfache Satzstrukturen, Grundwortschatz, starke Konzentration auf wichtige Informationen, Vermeidung von kulturspezifischen Ausdrücken.
    - Beispielbereiche: Sprachlernmaterialien, einführende Webtexte.
3. Häufig verwendete Sprache
    - Zielgruppen: Allgemeine Öffentlichkeit mit unterschiedlichen Bildungsniveaus.
    - Merkmale: Klare, strukturierte Sätze, Fokus auf Verständlichkeit, Vermeidung von Fachbegriffen.
    - Beispielbereiche: Breit gefächerte Nachrichtenportale, Blogs.
4. Gehobene Alltagssprache
    - Zielgruppe: Regelmäßige Leser mit guten Sprachkenntnissen.
    - Merkmale: Vielfältigerer Wortschatz, gelegentlich Fachausdrücke mit Erklärungen, komplexe Satzstrukturen.
    - Beispielbereiche: Fachblogs, Qualitätszeitungen.
5. Akademische Sprache
    - Zielgruppe: Akademiker und Experten.
    - Merkmale: Komplexe Satzstrukturen, Fachterminologie, Verwendung von Fachbegriffen.
    - Beispielbereiche: Fachzeitschriften, wissenschaftliche Publikationen.

Deine Aufgabe ist es, eine Bewertung der Paraphrasierung unter folgenden Aspekten abzugeben:

- content_preservation: Wie gut stimmt der Inhalt der Paraphrase mit dem Originaltext überein? Achte besonders darauf, ob Bedeutungen verändert oder vereinfacht wurden, sodass Nuancen verloren gehen oder neue Bedeutungen entstehen.
- information_loss: Fehlen in der Paraphrase Informationen, die im Original vorkommen?
- information_addition: Enthält die Paraphrase zusätzliche Informationen, die im Original nicht vorkommen? Dazu zählen auch erklärende Umschreibungen oder Beispiele, die neue Bedeutungselemente einführen.
- type_of_addition: Wenn du auf die vorherige Frage mit „nie“ geantwortet hast, antworte hier mit „NaN“. Andernfalls, wenn zusätzliche Informationen enthalten sind, gib an, um welche Art es sich handelt: z.B. Erklärungen, Ausschmückungen, korrekte oder inkorrekte Fakten.
- complexity_level: Wie gut passt die Paraphrase zum angegebenen Schwierigkeitsgrad? Beachte dabei die sprachlichen Merkmale der jeweiligen Stufe, nicht nur den Inhalt.

**WICHTIG:**
- Wenn abstrakte Begriffe (z.B. „universalist“) durch einfache Umschreibungen ersetzt werden (z.B. „für alle Menschen“), bewerte dies als zusätzliche Erklärung.
- Wenn die Umschreibung eine inhaltliche Verschiebung erzeugt (z.B. von ideologischem Konzept zu einfacher Aussage), kann dies eine *Faktisch inkorrekte Information* darstellen.
- Die Bewertung muss ausschließlich im folgenden JSON-Format erfolgen und diesem Schema entsprechen:
{json_schema}

Gib **nur** das JSON-Objekt zurück – ohne weiteren Text.
"""

JUDGE_PROMPT_FULL_USER_NEW = """
Evaluiere diesen Text:
Ursprünglicher Text: {orig}
Paraphrasierter Text: {para}
Komplexitätsgrad der Paraphrase: {cl}

Achte besonders darauf, ob durch Vereinfachungen Bedeutungen verloren gehen oder verändert werden.
"""

JUDGE_PROMPT_FULL_USER = """
Evaluiere diesen Text:
Ursprünglicher Text: {orig}
Paraphrasierter Text: {para}
Komplexitätsgrad der Paraphrase: {cl}
"""

JUDGE_PROMPT_COMPARE_SYSTEM = """
Du bist ein Evaluationsassistent. Deine Aufgabe ist es zwei Texte, Paraphrasierungen A und B, zu vergleichen und zu sagen welcher Text leichter verständlich ist.
Ergänze dafür den Satz 'Paraphrasierung A ist von der Schwierigkeit her ... Paraphrasierung B.'
Du hast folgende Antwortmöglichkeiten:
'viel einfacher als', 'etwas einfacher als', 'gleich wie', 'etwas komplizierter als' und 'viel komplizierter als'.
"""

JUDGE_PROMPT_COMPARE_USER = """
Hier sind zwei Paraphrasierungen:
Paraphrasierung A: {paraA}
Paraphrasierung B: {paraB}
Ergänze dafür den Satz 'Paraphrasierung A ist von der Schwierigkeit her ... Paraphrasierung B.'
"""