import tiktoken
import os
import json
import pandas as pd


def create_prompt(text):
    prompt = f'''**Kontext**
Es gibt fünf Schwierigkeitsstufen:

1. **Leichte Sprache**
- Zielgruppe: Personen mit Leseschwierigkeiten, inklusive Menschen mit Lernbehinderungen und solche, die erst kürzlich begonnen haben, Deutsch zu lernen.
- Merkmale: Sehr kurze Sätze, nur kurze und häufig verwendete Wörter, direkte Ansprache. Vermeidung von Abkürzungen, Metaphern oder Ironie.
- Beispielbereiche: Einfache Anleitungen, barrierefreie Webseiten.
2. **Einfaches Deutsch für Anfänger**
- Zielgruppe: Nicht-Muttersprachler mit grundlegenden Deutschkenntnissen.
- Merkmale: Einfache Satzstrukturen, Grundwortschatz, klarer Fokus auf wichtige Informationen, Vermeidung kulturspezifischer Ausdrücke.
- Beispielbereiche: Sprachlernmaterialien, einführende Webtexte.
3. **Allgemeinverständliche Sprache**
- Zielgruppe: Öffentlichkeit mit unterschiedlichem Bildungsniveau.
- Merkmale: Klare, strukturierte Sätze, Verständlichkeit steht im Vordergrund, Vermeidung von Fachjargon.
- Beispielbereiche: Breit gefächerte Nachrichtenportale, Blogs.
4. **Gehobene Alltagssprache**
- Zielgruppe: Regelmäßige Leser mit gutem Sprachverständnis.
- Merkmale: Vielfältigeres Vokabular, gelegentlicher Fachjargon mit Erklärungen, komplexe Satzstrukturen.
- Beispielbereiche: Fachblogs, Qualitätszeitungen.
5. **Akademische Sprache**
- Zielgruppe: Akademiker und Experten.
- Merkmale: Komplexe Satzstrukturen, Fachterminologie, Verwendung von Fachbegriffen.
- Beispielbereiche: Fachzeitschriften, wissenschaftliche Publikationen.

**Beispiel**
Text: Die Ortschaft Danbury geht auf die Gründung einer vorchristlichen Wallburg zurück. Funde lassen auf eine erste Siedlung in der Eisenzeit schließen. Nach Römern und Angelsachsen, wurde das Gebiet um Danbury im 11. Jahrhundert von dänischen Stämmen erobert. Nach der Eroberung Englands durch Wilhelm den Eroberer 1066 wurde das Land um Danbury von den Normannen besiedelt. Das älteste, heute noch erhaltene Gebäude, ist die Kirche St. John the Baptist, die im 13. Jahrhundert errichtet wurde.

Paraphrasierungen im json Format:
{{
  "1": "Danbury ist ein Ort. In Danbury gab es früher eine große alte Burg. Viele verschiedene Leute haben dort gelebt. Die ersten Menschen kamen vor sehr langer Zeit. Später kamen Menschen aus Dänemark und dann aus Frankreich. In Danbury steht eine sehr alte Kirche. Sie ist ungefähr 800 Jahre alt.",
  "2": "Danbury ist ein Ort mit einer alten Burg, die noch vor der christlichen Zeit gebaut wurde. Zuerst lebten dort Menschen in der Eisenzeit. Dann kamen Römer, Angelsachsen und später Dänen. Nach einer großen Schlacht kamen Menschen aus Frankreich, die Normannen. Die älteste Kirche dort heißt St. John the Baptist und wurde im Mittelalter gebaut.",
  "3": "Danbury ist bekannt für seine historische Burg, die vor der christlichen Ära errichtet wurde. Die ersten Bewohner kamen während der Eisenzeit. Über die Jahrhunderte hinweg wurde das Gebiet von Römern, Angelsachsen und später von Dänen bewohnt. Nach der normannischen Eroberung Englands im Jahr 1066 wurde Danbury von den Normannen übernommen. Die Kirche St. John the Baptist, die älteste in Danbury, stammt aus dem 13. Jahrhundert.",
  "4": "Danbury besitzt eine lange Geschichte, die mit einer prähistorischen Festung beginnt. Archäologische Funde deuten darauf hin, dass die Region bereits in der Eisenzeit bewohnt war. Nach den Römern und Angelsachsen kamen im 11. Jahrhundert dänische Eroberer. Die normannische Eroberung Englands im Jahr 1066 brachte weitere Veränderungen mit sich, und Danbury fiel in die Hände der Normannen. Die Kirche St. John the Baptist, erbaut im 13. Jahrhundert, ist das älteste noch bestehende Gebäude.",
  "5": "Die historische Entwicklung von Danbury lässt sich bis zu einer prächristlichen Festungsanlage zurückverfolgen. Archäologische Befunde belegen eine frühe Besiedlung während der Eisenzeit. Die Abfolge der Herrschaftswechsel von Römern zu Angelsachsen und später zu dänischen Stämmen im 11. Jahrhundert illustriert die komplexe Sozialstruktur dieser Ära. Mit der normannischen Eroberung Englands im Jahre 1066 wurde Danbury Teil eines erweiterten Herrschaftsgebietes. Die Kirche St. John the Baptist aus dem 13. Jahrhundert dient als architektonisches Zeugnis dieser vielschichtigen Geschichte."
}}

**Aufgabe**
Paraphrasiere den gegebenen Text in fünf unterschiedlichen Schwierigkeitsgraden. Bei der Erstellung der Paraphrasen solltest du schrittweise vorgehen und insbesondere die Zielgruppe sowie die spezifischen Merkmale und Anwendungsbereiche jeder Schwierigkeitsstufe berücksichtigen. Führe diese Aufgabe in Form eines inneren Monologs aus, wobei du nicht deinen Denkprozess darlegst, sondern mir direkt die endgültigen paraphrasierten Texte präsentierst.

Text: {text}

**Antwort im json Format**
{{
"1": "Stufe 1 Text",
"2": "Stufe 2 Text",
"3": "Stufe 3 Text",
"4": "Stufe 4 Text",
"5": "Stufe 5 Text"
}}
'''
    return prompt


def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4-turbo")
    tokens = encoding.encode(text)
    return len(tokens)


def create_tasks(subsamples_df, start_index=None, end_index=None, failed_array=None, model="gpt-4-turbo-2024-04-09", temperature=1):
    if start_index is None:
        start_index = 0
    if end_index is None:
        end_index = len(subsamples_df) - 1
    tasks = []
    categorize_system_prompt = "Du bist ein Experte für die Anpassung von Texten an verschiedene Verständlichkeitsniveaus."
    if failed_array is None:
        iteration = subsamples_df[start_index:end_index+1].iterrows()
    else:
        iteration = subsamples_df.iloc[failed_array].iterrows()
    for index, row in iteration:
        text = row['text']
        prompt = create_prompt(text)
        task = {
            "custom_id": f"task-{row['id']}-{index}", 
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model,
                "temperature": temperature,
                "response_format": {
                    "type": "json_object"
                },
                "messages": [
                    {
                        "role": "system",
                        "content": categorize_system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            }
        }

        tasks.append(task)
    return tasks


def create_batch_file(tasks, input_file_path):
    os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
    with open(input_file_path, "w", encoding='utf-8') as f:
        for obj in tasks:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
        print(f"Created input file: {input_file_path}")


def create_output_file(output_file_path, result):
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "wb") as file:
        file.write(result)
        print(f"Created output file: {output_file_path}")


def load_results(output_file_path):
    results = []
    with open(output_file_path, 'r', encoding="utf-8") as file:
        for line in file:
            # Parsing the JSON string into a dict and appending to the list of results
            json_object = json.loads(line.strip())
            results.append(json_object)
    return results


def append_results_to_df(results, failed_tasks_file, subsamples_df, model_name=None):
    if not os.path.exists(failed_tasks_file):
        failed_tasks = []
    else:
        with open(failed_tasks_file, 'r', encoding="utf-8") as file:
            failed_tasks = json.load(file)
    new_rows = []

    for res in results:
        task_id = res['custom_id']
        # print(f"task_id : {task_id}")
        index = int(task_id.split('-')[-1])
        result = res['response']['body']['choices'][0]['message']['content']
        # print(result)
        try: 
            result_dict = json.loads(result)
        except Exception as e: 
            print(f"Error in parsing result: {result}, error {e}")
            if index not in failed_tasks:
                failed_tasks.append(index)
            continue
        keys = result_dict.keys()
        if set(keys) != {'1', '2', '3', '4', '5'}:
            print(f"Incorrect keys in result: {result}")
            print(f"Keys: {keys}")
            if index not in failed_tasks:
                failed_tasks.append(index)
            continue 
        if index in failed_tasks:
            failed_tasks.remove(index)
        
        # Copy existing row and create new row 
        if model_name: 
            new_row = subsamples_df.loc[index].copy()
            new_row['id'] = f"{new_row['id']}-{model_name}"
            if new_row['id'] in subsamples_df['id'].values:
                print(f"ID {new_row['id']} already exists in the dataframe.")
                continue
        for key, value in result_dict.items():
            column_name = f"cl_{key}"
            if column_name not in subsamples_df.columns:
                subsamples_df[column_name] = ""
            
            if model_name:
                new_row[column_name] = value
            else:
                subsamples_df.at[int(index), column_name] = value
        if model_name:
            new_rows.append(new_row)
    if model_name:
        subsamples_df = pd.concat([subsamples_df, pd.DataFrame(new_rows)], ignore_index=True)
    os.makedirs(os.path.dirname(failed_tasks_file), exist_ok=True)
    with open(failed_tasks_file, "w", encoding="utf-8") as f:
        json.dump(failed_tasks, f, indent=4)

    return subsamples_df

