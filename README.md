# KG-A2C
This repository contains a reference implementation CALM as mentioned in [Keep CALM and Explore: Language Models for Action Generation in Text-based Games](https://arxiv.org/abs/2010.02903), that has been modified for use with the [ScienceWorld](https://www.github.com/allenai/ScienceWorld) environment.

## Quickstart
Clone the repository:
```bash
git clone git@github.com:cognitiveailab/calm-scienceworld.git
cd calm-scienceworld
```

Install Dependencies:
```bash
conda create --name calm-scienceworld python=3.9
conda activate calm-scienceworld
pip install -r requirements.txt
```
You may want to install the Pytorch manually if your GPU does not support CUDA 11.

### Pretrain GPT2

Raw ScienceWorld gold path data generated by the oracle agent can be found by:
```bash
cd data
unzip goldpaths-all.zip
cd ..
```
Run
```bash
python data_convert.py
```
to generate formatted data for GPT2 training. You can skip this step because we already include the formatted data in this repository. You can unzip the formatted gold path data files in the data folder by
```bash
cd data
unzip sciworld_formatted_data.zip
cd ..
```
Train the GPT2 model by
```bash
python train_gpt2.py --bs 8 --train_data data/sciworld_formatted_train.jsonl --val_data data/sciworld_formatted_val.jsonl --num_train_epochs 20 --save_dir_root gpt2_lm
```
Here:
- **bs:** batch size
- **train_data:** train data file name
- **val_data:** validation data file name
- **num_train_epochs:** the maximum training epochs

We train the GPT2 model with this setting using four Nvidia A100 GPUs.

### Train the CALM-GPT2 agent

Train the CALM agent on scienceworld:
```bash
python train.py --lm_path gpt2_lm --num_envs 8 --output_dir logs --task_num 0 --max_steps 100000 --eval_freq 1000 --env_step_limit 100 --stuck_step_limit 200 --seed 0 --simplification_str easy --max_histories_per_file 1000
```

Here:
- **lm_path** Path the path pretrained GPT2 model checkpoint folder
- **num_envs:** The number of environment threads to simultaneously use during training (8 is a common number)
- **output_dir:** output directory
- **task_num:** The ScienceWorld task index (0-29). *See **task list** below*
- **max_steps:** the maximum number of steps
- **eval_freq:** the number of steps between evaluations
- **env_step_limit:** the maximum valid steps per episode
- **stuck_step_limit:** the maxium steps (both valid and invalid) per episode
- **seed:** random seed
- **simplification_str:** The ScienceWorld simplification string
- **max_histories_per_file:** the maxium histories saved per history log file

## ScienceWorld Task List
```
TASK LIST: 
    0: 	                                                 task-1-boil  (30 variations)
    1: 	                        task-1-change-the-state-of-matter-of  (30 variations)
    2: 	                                               task-1-freeze  (30 variations)
    3: 	                                                 task-1-melt  (30 variations)
    4: 	             task-10-measure-melting-point-(known-substance)  (436 variations)
    5: 	           task-10-measure-melting-point-(unknown-substance)  (300 variations)
    6: 	                                     task-10-use-thermometer  (540 variations)
    7: 	                                      task-2-power-component  (20 variations)
    8: 	   task-2-power-component-(renewable-vs-nonrenewable-energy)  (20 variations)
    9: 	                                   task-2a-test-conductivity  (900 variations)
   10: 	             task-2a-test-conductivity-of-unknown-substances  (600 variations)
   11: 	                                          task-3-find-animal  (300 variations)
   12: 	                                    task-3-find-living-thing  (300 variations)
   13: 	                                task-3-find-non-living-thing  (300 variations)
   14: 	                                           task-3-find-plant  (300 variations)
   15: 	                                           task-4-grow-fruit  (126 variations)
   16: 	                                           task-4-grow-plant  (126 variations)
   17: 	                                        task-5-chemistry-mix  (32 variations)
   18: 	                task-5-chemistry-mix-paint-(secondary-color)  (36 variations)
   19: 	                 task-5-chemistry-mix-paint-(tertiary-color)  (36 variations)
   20: 	                             task-6-lifespan-(longest-lived)  (125 variations)
   21: 	         task-6-lifespan-(longest-lived-then-shortest-lived)  (125 variations)
   22: 	                            task-6-lifespan-(shortest-lived)  (125 variations)
   23: 	                               task-7-identify-life-stages-1  (14 variations)
   24: 	                               task-7-identify-life-stages-2  (10 variations)
   25: 	                       task-8-inclined-plane-determine-angle  (168 variations)
   26: 	             task-8-inclined-plane-friction-(named-surfaces)  (1386 variations)
   27: 	           task-8-inclined-plane-friction-(unnamed-surfaces)  (162 variations)
   28: 	                    task-9-mendellian-genetics-(known-plant)  (120 variations)
   29: 	                  task-9-mendellian-genetics-(unknown-plant)  (480 variations)
```

## Citing

If this CALM-GPT2 agent is helpful in your work, please cite the following:

Bibtex
```
@inproceedings{yao2020calm,
    title={Keep CALM and Explore: Language Models for Action Generation in Text-based Games},
    author={Yao, Shunyu and Rao, Rohan and Hausknecht, Matthew and Narasimhan, Karthik},
    booktitle={Empirical Methods in Natural Language Processing (EMNLP)},
    year={2020}
}
```