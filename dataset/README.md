---
task_categories:
- text2text-generation
- text-classification
language:
- de
pretty_name: German4All Corpus
size_categories:
- 10K<n<100K
tags:
- synthetic
- simplification
- paraphrasing
---
# Dataset Card for the German4All Corpus of datasets
## Corpus Overview
German4All is a synthetic data corpus consisting of 3 datasets. Each dataset consists of German Wikipedia paragraphs that are paraphrased in five different complexity levels. The 3 datasets are:
* German4All-Main (subfolder "main"): The main synthetic dataset containing 25,459 elements, each featuring an
original text along with its five-level paraphrases. 
* German4All-Main-old (subfolder "main-old"): The original version of German4All-Main, containing 26,337 samples. Due to a small error in the original logic for filtering out poor-quality samples, around 100 poor-quality samples were not removed from this dataset, and some acceptable samples were removed. In addition, an LLM-Judge was used to remove erroneous and non-meaning-preserving samples.
* The corrected version of the dataset is German4All-Main.
* German4All-Corrected (subfolder "corrected"): 150 synthetic samples that were manually checked and corrected by two annotators.
* German4All-Annotated (subfolder "annotated"): The original paraphrase and a corrected paraphrase for each instance in German4All-Corrected that was manually modified.

## Usage
```
from datasets import load_dataset

# Load the different datasets with the `data_dir` parameter
german4all_main = load_dataset("*anonymized*/German4All-Corpus", data_dir="main")
german4all_corrected = load_dataset("*anonymized*/German4All-Corpus", data_dir="corrected")

print(german4all_corrected)
```
Outputs the dataset features:
```
DatasetDict({
    train: Dataset({
        features: ['id', 'title', 'text', 'url', 'wiki_id', 'views', 'paragraph_id', 'langs', 'text_length', 'word_count', 'prompt_token_count', 'cl_1', 'cl_2', 'cl_3', 'cl_4', 'cl_5', 'cl_LS'],
        num_rows: 100
    })
    validation: Dataset({
        features: ['id', 'title', 'text', 'url', 'wiki_id', 'views', 'paragraph_id', 'langs', 'text_length', 'word_count', 'prompt_token_count', 'cl_1', 'cl_2', 'cl_3', 'cl_4', 'cl_5', 'cl_LS'],
        num_rows: 20
    })
    test: Dataset({
        features: ['id', 'title', 'text', 'url', 'wiki_id', 'views', 'paragraph_id', 'langs', 'text_length', 'word_count', 'prompt_token_count', 'cl_1', 'cl_2', 'cl_3', 'cl_4', 'cl_5', 'cl_LS'],
        num_rows: 30
    })
})
```

## Background Information

### Complexity Levels Overview
The five complexity levels for this dataset are:
1. Easy Language
2. Simple German for beginners
3. Commonly used language
4. Elevated everyday language
5. Academic language
The full definitions of these complexity levels can be found at the end of this dataset card.

The corrected corpus also features Leichte Sprache version that complies with the [DIN SPEC 33429: Guidance for German Easy Language](https://www.dinmedia.de/de/technische-regel/din-spec-33429/387728031).
It was created with [EasyJon](https://easy-jon.de/) with an `anthropic/claude-3.5-sonnet` backend. All samples were manually revised and corrected by a German Leichte Sprache expert.

### Dataset Creation
All paraphrases were synthetically generated with the LLM `gpt-4-turbo-2024-04-09` using a 1-shot prompting approach.
The source dataset for the Wikipedia paragraphs is [Wikipedia-22-12](https://huggingface.co/datasets/Cohere/wikipedia-22-12).

## Dataset Structure

### Data Splits
German4All-Main(-old) is **not** split into train, validation, and test sets.
It consists of a single file `train.csv` that contains all samples.

German4All-Corrected and German4All-Annotated are each split into train, validation, and test sets. The sizes of the splits are as follows:

| Dataset | Train  | Validation | Test  |
|---------|--------|------------|-------|
| German4All-Main | 25,459 | - | - |
| German4All-Main-old | 26,337 | - | - |
| German4All-Corrected | 100 | 30 | 20 |
| German4All-Annotated | 39 | 35 | 58 |

Note: German4All-Annotated is not a pure subset of German4All-Corrected. It contains rows of original and corrected paraphrases together with annotations for the modifications. The differences in the data fields are described below.

### Data Fields
All 3 datasets contain the following fields form the [Wikipedia Source Dataset]((https://huggingface.co/datasets/Cohere/wikipedia-22-12)): 
* `id`: Wikipedia paragraph id
* `title`: Title of the Wikipedia article
* `text`: Original text of the Wikipedia paragraph
* `url`: URL of the Wikipedia article
* `wiki_id`: Wikipedia identifier of the article
* `views`: Number of views of the article in 2022 (on a log scale as described [here](https://huggingface.co/datasets/Cohere/wikipedia-22-12))
* `paragraph_id`: Identifier of the paragraph within the article
* `langs`: Number of available languages of the article at the time of scraping


#### German4All-Main & German4All-Corrected
German4All-Main and German4All-Corrected contain the following additional fields:
* `text_length`: Length of the original text in characters
* `word_count`: Number of words in the original text
* `prompt_token_count`: Number of tokens in the prompt for synthesizing the paraphrases
* `cl_1`: Paraphrase of the original text at complexity level 1
* `cl_2`: Paraphrase of the original text at complexity level 2
* `cl_3`: Paraphrase of the original text at complexity level 3
* `cl_4`: Paraphrase of the original text at complexity level 4
* `cl_5`: Paraphrase of the original text at complexity level 5
* `cl_LS` (only in the corrected corpus): Paraphrase of the original text in German Leichte Sprache


#### German4All-Annotated
German4All-Annotated contains the following additional fields:
* `original_paraphrase`: The original paraphrase
* `corrected_paraphrase`: The corrected paraphrase
* `complexity_level`: The number of the complexity level of the paraphrase that was corrected (1-5)
* `removed_info`: Indicates if information was removed during the correction process
* `added_info`: Indicates if information was added during the correction process
* `corrected_info`: Indicates if information was changed/corrected during the correction process
* `adjusted_complexity`: Indicates if the complexity of the text was adjusted during the correction process
* `corrected_language`: Indicates if the language of the text was corrected during the correction process
* `hallucination`: Indicates if the original paraphrase contains hallucinations

The boolean features `removed_info`,
`added_info`, `corrected_info`, `adjusted_complexity`, `corrected_language`, and `hallucination` in origin
are set to True if a specific type of correction was applied to the original text.

## Complexity Levels
English translation of the complexity levels we used for the synthetic data generation:
1. Leichte Sprache (literal translation: Easy Language)
    * Target group: People with reading difficulties, including people with learning disabilities and those who have only recently started to learn German.
    * Characteristics: Very short sentences, only short and frequently used words, direct speech, avoidance of abbreviations, metaphors, or irony.
    * Examples areas: simple instructions, accessible websites.
2. Simple German for beginners
   * Target group: Non-native speakers with basic knowledge of German.
   * Characteristics: Simple sentence structures, basic vocabulary, strong focus on important information, avoidance of culture-specific expressions.
   * Example areas: Language learning materials, introductory web texts.
3. Commonly used language
    * Target group: General public with different levels of education.
    * Characteristics: Clear, structured sentences, focus on comprehensability, avoidance of technical terms.
    * Example areas: Wide-ranging news portals, blogs.
4. Elevated everyday language
    * Target group: Regular readers with a good understanding of the language.
    * Characteristics: More varied vocabulary, occasional technical terminology with explanations, complex sentence structures.
    * Example areas: Specialist blogs, quality newspapers.
5. Academic language
    * Target group: Academics and experts.
    * Characteristics: Complex sentence structures, specialized terminology, use of technical terms.
    * Example areas: Specialist journals, scientific publications.

## Citation Information
[TBD after publishing]