import os
import json
from openai import OpenAI, RateLimitError
import pandas as pd
import sys
import argparse
import time

sys.path.insert(0, '../')


from utils import count_tokens, create_tasks, append_results_to_df, create_batch_file, create_output_file, load_results



def chunk(subsamples_df, token_limit=90000):
    # Chunk the dataframe into smaller parts
    # Current limit: 90,000 enqueued tokens
    categorize_system_prompt = "Du bist ein Experte für die Anpassung von Texten an verschiedene Verständlichkeitsniveaus."
    categorize_system_token_count = count_tokens(categorize_system_prompt)
    start_index = 0
    end_index = 0
    prompt_token_count = 0
    indices_limit = []
    for index, row in subsamples_df.iterrows():
        tmp_prompt_token_count = prompt_token_count + row['prompt_token_count'] + categorize_system_token_count
        if tmp_prompt_token_count > token_limit:
            print(f"Chunk from {start_index} to {end_index}, prompt token count: {prompt_token_count}")
            indices_limit.append({"start_index": start_index, "end_index": end_index, "tokten_count": prompt_token_count, "processed": False, "status": ""})
            start_index = end_index + 1
            prompt_token_count = 0
        else:
            prompt_token_count += row['prompt_token_count'] + categorize_system_token_count
            end_index += 1
    print(f"Chunk from {start_index} to {end_index}, prompt token count: {prompt_token_count}")
    indices_limit.append({"start_index": start_index, "end_index": end_index, "token_count": prompt_token_count, "processed": False, "status": ""})
    return indices_limit

def choose_chunk(indices_limit):
    start_index = -1
    end_index = -1
    nth_batch = -1
    for idx, batch in enumerate(indices_limit):
        processed = batch['processed']
        if not processed:
            start_index = batch['start_index'] 
            end_index = batch['end_index']
            nth_batch = idx
            break
    # If both indices are -1 we are done with batching requests
    print(f"For batch {nth_batch} start index: {start_index}, end index: {end_index}")
    return start_index, end_index, nth_batch

def process_batch(batch_job):
    while True:           
        batch_job = client.batches.retrieve(batch_job.id)
        status = batch_job.status
        if status == 'completed':
            print(f"Batch job finished with status: {batch_job.status}")

            return batch_job
        elif status == 'validating' or status == 'in_progress' or status == 'finalizing' or status == 'cancelling':
            print("Batch job is still processing...")
            time.sleep(60) 
        else:
            raise Exception(f"Batch job failed with status: {batch_job.status}, batch job: {batch_job}")

        

if __name__ == "__main__":
    print("Run script")
    parser = argparse.ArgumentParser(description='Generate samples with Batch OpenAI API')
    parser.add_argument('--input-file', type=str, help='Input file name to generate samples')

    args = parser.parse_args()

    file_name = args.input_file

    client = OpenAI(api_key=os.environ.get("MA-PARAPHRASING-LEVELS-KEY"))

    original_dataset_path = f"../dataset/subset/{file_name}.csv"
    working_dataset_path = f"subset/{file_name}.csv"

    if not os.path.exists(working_dataset_path):
        os.makedirs(os.path.dirname(working_dataset_path), exist_ok=True)
        # Copy original dataset to new one
        subsamples_df = pd.read_csv(original_dataset_path)
        subsamples_df.to_csv(working_dataset_path, index=False)
        print(f"File saved: {working_dataset_path}")
    else:
        print(f"File already exists: {working_dataset_path}")
        subsamples_df = pd.read_csv(working_dataset_path)
    
    print(f"Dataframe shape: {subsamples_df.shape}")

    print("Chunk dataframe into smaller parts if indices_limit file does not exist yet")
    indices_limit_json_file_path = f"indices_limit/{file_name}_indices_limit.json"
    if not os.path.exists(indices_limit_json_file_path):
        print(f"Create new indices limit file: {indices_limit_json_file_path}")
        indices_limit = chunk(subsamples_df)
    
        os.makedirs(os.path.dirname(indices_limit_json_file_path), exist_ok=True)

        with open(indices_limit_json_file_path, "w", encoding="utf-8") as f:
            json.dump(indices_limit, f, indent=4)

    else:
        print(f"Indices limit file already exists: {indices_limit_json_file_path}")
        with open(indices_limit_json_file_path, "r", encoding="utf-8") as f:
            indices_limit = json.load(f)

    while True:
        print("Choose chunk to process")
        start_index, end_index, nth_batch = choose_chunk(indices_limit)
        if start_index == -1 and end_index == -1:
            print("All batches are processed.")
            break
        
        tasks = create_tasks(subsamples_df, start_index, end_index)
        batch_name = f"{file_name}_{nth_batch}_{start_index}_{end_index}"
        input_file_path = f"batch_input_files/{batch_name}.jsonl"

        print(f"Create input file: {input_file_path}")
        create_batch_file(tasks, input_file_path)


        print("Upload input file...")
        batch_file = client.files.create(file=open(input_file_path, "rb"), purpose="batch")

        print("Create batch job...")
        batch_job = client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )

        print("Wait for batch job to finish...")
        try:
            batch_job = process_batch(batch_job)
        except Exception as e:
            print(f"Break out of loop due to error while batch processing: {e}")
            break

        # batch_job = client.batches.retrieve("batch_afysFyzoasCMK1dpTWJtbJyZ")
        
        print("Download output file...")
        result_file_id = batch_job.output_file_id
        result = client.files.content(result_file_id).content
        print(f"Downloaded output file with id: {result_file_id}")

        print("Create output file...")
        output_file_path = f"batch_output_files/{batch_name}.jsonl"
        create_output_file(output_file_path, result)

        print("Load results...")
        results = load_results(output_file_path)

        print("Append results to dataframe...")
        failed_tasks_file = f"failed_tasks/{file_name}_failed_tasks.json"

        subsamples_df = append_results_to_df(results, failed_tasks_file, subsamples_df)
        subsamples_df.to_csv(working_dataset_path, index=False)

        with open(failed_tasks_file, "r", encoding="utf-8") as f:
            failed_tasks = json.load(f)

        indices_limit[nth_batch]['processed'] = True
        indices_limit[nth_batch]['n_failed_tasks'] = len(failed_tasks)
        indices_limit[nth_batch]['input_file_id'] = batch_job.input_file_id
        indices_limit[nth_batch]['output_file_id'] = batch_job.output_file_id
        indices_limit[nth_batch]['batch_id'] = batch_job.id
        indices_limit[nth_batch]['status'] = batch_job.status
        
        with open(indices_limit_json_file_path, "w", encoding="utf-8") as f:
            json.dump(indices_limit, f, indent=4)
        
        # print("Debugging: only do one iteration and then break")
        # break
        



