from datasets import load_dataset
import pandas as pd
from evaluation_structure import *
from evaluation_prompts import *
from tqdm import tqdm
import pandas as pd
from pydantic_core import from_json

from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="-"
)


#german4all_main = load_dataset("../dataset/annotatedmain")
#german4all_corrected = load_dataset("../dataset/corrected")
german4all_annotated = load_dataset("../dataset/annotated")

g4a = {
    #"corrected": german4all_corrected,
    #"main": german4all_main,
    "annotated": german4all_annotated
}

#model_name = "gemma-3-27b-it"
model_name = "phi-4"
#model_name = "Llama-3.3-70B-Instruct"
#model_name = "Qwen2.5-72B-Instruct"

base_path = "judge_outputs/LLM_judge_g4a_few_shot_new"

for g4a_version_name, g4a_version_df in g4a.items():
    all_splits = []
    for split_name in ["train", "validation", "test"]:
        #split_df = pd.melt(g4a_version_df[split_name].to_pandas(), id_vars=["id", "text", "paragraph_id"],
        #                   value_vars=["cl_1", "cl_2", "cl_3", "cl_4", "cl_5"], value_name="paraphrased_text")
        split_df = g4a_version_df[split_name].to_pandas() # use this for annotated data
        all_splits.append(split_df)
    split_df = pd.concat(all_splits)
    #split_df = g4a_version_df
    outpath = f"{base_path}_{g4a_version_name}_{model_name}.csv"
    #    outpath = f"{base_path}_{g4a_version_name}_{split_name}.csv"

    for field in Evaluation.model_fields:
        split_df["LLM_judge_" + field] = ""
    for i, row in tqdm(split_df.iterrows(), total=split_df.shape[0]):
        if row["LLM_judge_complexity_level"] != "" and not pd.isna(row["LLM_judge_complexity_level"]):
            continue
        response = client.chat.completions.create(
            model="tgi",
            messages=[
                {"role": "system",
                 "content": JUDGE_PROMPT_FULL_SYSTEM_NEW.format(json_schema=Evaluation.model_json_schema())},
                {"role": "user",
                 "content": JUDGE_PROMPT_FULL_USER.format(
                     orig="Das Frühmittelalter war eine Periode, in der sich verschiedene christliche Autoren mit den biblischen Speisegeboten beschäftigten:",
                     para="Im Frühmittelalter widmeten sich zahlreiche christliche Gelehrte der Interpretation und Diskussion biblischer Speisegebote.",
                     cl="cl_4")},
                {"role": "assistant",
                 "content": '"content_preservation": "richtig", "information_loss": "nie", '
                            '"information_addition": "selten", "type_of_addition": ["Ausschmückungen"],'
                            '"complexity_level": "passend"'},
                {"role": "user",
                 # "content": JUDGE_PROMPT_FULL_USER_NEW.format(orig=row["text"], para=row["paraphrased_text"],
                 #                                         cl=row["variable"])}
                 #"content": JUDGE_PROMPT_FULL_USER_NEW.format(orig=row["original_texts"], para=row["paraphrased_texts"],
                 #                                         cl=row["cl"])}
                 "content": JUDGE_PROMPT_FULL_USER_NEW.format(orig=row["text"], para=row["original_paraphrase"],
                                                          cl=row["complexity_level"])}
            ],
            response_format={"type": "json_object", "value": Evaluation.model_json_schema()},
            temperature=0,
            stream=False,
            extra_body={"cache_prompt": True}
        )

        evaluation: Evaluation = Evaluation.model_validate(from_json(response.choices[0].message.content))
        for field, value in evaluation.model_dump().items():
            split_df.at[i, "LLM_judge_" + field] = value.value if type(value) != list else f"{[v.value for v in value]}"
        if i % 5 == 0:
            split_df.to_csv(outpath, index=False)
    split_df.to_csv(outpath, index=False)
