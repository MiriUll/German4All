# German4All
## Dataset and Models for German Paraphrasing into Different Complexity Levels

![Overview of the dataset curation process](https://github.com/MiriUll/German4All/blob/main/German4All_construction.png)

This repository contains the German4All dataset and code that was used to create it. The [dataset](https://huggingface.co/datasets/tum-nlp/German4All-Corpus) and our fine-tuned model are uploaded to the [HuggingFace hub](https://huggingface.co/collections/tum-nlp/german4all-67477a7e9583754ed0bc3050) for easier loading and usage. You can find further details on how to use these artifacts on their respective pages.

This repository contains the following add-ons:
* Code to reproduce the sample generation
* Code to reproduce the LLM judge annotations
* LLM judge annotations for customized filters of the synthetic dataset
* Predictions of our models on common simplification benchmark datasets ([Stodden et al. 2024](https://aclanthology.org/2024.determit-1.1/))

## Citation
If you use any of our artifacts, please cite our paper as 
```bibtex
@misc{anschuetz2025german4alldatasetmodel,
      title={German4All -- A Dataset and Model for Readability-Controlled Paraphrasing in German}, 
      author={Miriam Anschütz and Thanh Mai Pham and Eslam Nasrallah and Maximilian Müller and Cristian-George Craciun and Georg Groh},
      year={2025},
      eprint={2508.17973},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2508.17973}, 
}
```
