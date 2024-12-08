# README file for DragonFire AI project
Creators: Patricia Delafuente and Marcus McAllister


The CALM-Scienceworld Project is adapted from the CALM project to work with ScienceWorld. ScienceWorld provides a reinforcement learning environment to solve a series of 30 complex, multi-sequence science related tasks. 

CALM-ScienceWorld repository (https://github.com/cognitiveailab/calm-scienceworld) - Contains Python code for training an intelligent agent to solve ScienceWorld tasks using OpenAI GPT-2.  Instructions for training this agent are found in the dedicated README for the CALM-ScienceWorld repository.  Note that the hardware requirements for training the models are significant, so training may take significantly longer on average compute platforms.

ScienceWorld repository (https://github.com/allenai/ScienceWorld) - Contains Python + Scala code for a random agent and human-interactive agent.  Instructions for running these agents are found in the dedicated README for the ScienceWorld repository.

The original CALM project integrates a LLM agent and a DRRN agent to solve multistep tasks in an Interactive Fiction game. 

Both the CALM-ScienceWorld and base CALM project uses the older GPT2 model  This project extends the CALM-ScienceWorld project to add in the Llama3.1-8b-Instruct model, RoBERTA and BERT models and compare the prediction of these three models to the baseline GPT2. 
The DragonFire AI project makes use of multiple existing codebases and datasets.  An inventory of referenced material is listed below:

Hugginface Transformers (https://github.com/huggingface/transformers) - Leverages the Transformers libraries and scripts for training and inference of the RoBERTA and BERT models.

Intent Detection with Wikihow (https://github.com/zharry29/wikihow-intent) is the original inspiration for this project which is to determine an action to take based on a task and environment observations. 
- @misc{zhang2020intent,
    title={Intent Detection with WikiHow},
    author={Li Zhang and Qing Lyu and Chris Callison-Burch},
    year={2020},
    eprint={2009.05781},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
Recommended environment:
Linux with NVIDIA GPU with minimum of 16gb GPU memory.  Batch size should be set at 1 for GPU and 16 for higher end GPUs with additional memory. A laptop with a GPU RTX A5000 with 16GB of GPU memory was used to train the RoBERTA model.  An AI Workstation with two A6000 with 48GB of GPU Memory was used to train the other models.  The CALM-ScienceWorld project originally used 4 A100 GPUs to train the based GPT2 model.  

This project is a fork and derived from the CALM-Scienceworld project.  
@misc{scienceworld2022,
    title={ScienceWorld: Is your Agent Smarter than a 5th Grader?},
    author={Ruoyao Wang and Peter Jansen and Marc-Alexandre C{\^o}t{\'e} and Prithviraj Ammanabrolu},
    year={2022},
    eprint={2203.07540},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2203.07540}

@inproceedings{yao2020calm,
    title={Keep CALM and Explore: Language Models for Action Generation in Text-based Games},
    author={Yao, Shunyu and Rao, Rohan and Hausknecht, Matthew and Narasimhan, Karthik},
    booktitle={Empirical Methods in Natural Language Processing (EMNLP)},
    year={2020}
}


#### Model Training Notes

RoBerta, GPT2 and BERT models can be run in Pytorch and transformer libraries. We used the basic GPT2 script provided in the CALM-ScienceWorld project.  For RoBERTA and BERT models, we used the HuggingFace MultiChoice task and adapted this tutorial https://huggingface.co/docs/transformers/en/tasks/multiple_choice to work with the ScienceWorld data.

To reduce compute for Llama-3.1-8b-Instruct model, we leveraged the NVIDIA NeMo framework which provided a streamlined path to use PEFT Lora.  We specifically adapted this NeMo Lora tutorial https://github.com/NVIDIA/NeMo/blob/main/tutorials/llm/llama-3/sdg-law-title-generation/llama3-sdg-lora-nemofw.ipynb to for the ScienceWorld project. 

### Install Instructions for Development Environment 
#### make project directory and add project files
~mkdir nvdata
cd nvdata 

Because of the size of the data and model files, we have placed the project at https://drive.google.com/drive/folders/17s6qX-p0Js-V97sjHus2YpNrl4CPUMRx?usp=sharing.  We recommend you download as a zip and upload into the nvdata folder. 

Then unzip the folder inside nvdata with the following command:
unzip DragonFire_Phase2_Code.zip

#### NeMo Docker Container
We recommend that you use the NeMo docker container as it contains the transformers, NeMo, pytorch and bulk of the libraries needed for this project.  The NeMo container is freely available at https://catalog.ngc.nvidia.com/orgs/nvidia/containers/nemo.  You will just need to create a free developer account.  We used the latest container nvcr.io/nvidia/nemo:24.07.

This command will pull and run the docker container and mount the nvdata project directory

docker run --gpus all --runtime=nvidia -it --rm -v --shm-size=16g -p 8888:8888 -p 6006:6006 \
 -v ~/nvdata:/workspace/nvdata \
--ulimit memlock=-1 --ulimit stack=67108864 nvcr.io/nvidia/nemo:24.07

Once you are the #sign inside the container, run the following commands
pip install ipywidgets
pip install jupyter_contrib_nbextensions
pip install scienceworld

jupyter nbextension enable --py widgetsnbextension
pip install -U "huggingface_hub[cli]"

#needed for scienceworld environments
apt install default-jre -y

#### Jupyter-lab
Finally, run the following command to spin up a Jupyter-Lab session.
jupyter-lab --allow-root --ip='0.0.0.0' --NotebookApp.token='' --no-browser

Navigate to a browser http://<ip or localhost>:8888/lab to view and run the code.

The needed data files are in the data folder.  

#### Notebook files
The following notebooks are the ones available to train and evaluate the models:  
- Llama3.1-8b-Instruct: df_llama3-lora-nemofw.ipynp
- RoBERTA: df_roberta_multiple_choice.ipynb
- GPT2: basemodelGPT2_training.ipynb
- Optional GPT4o (note, expensive to train): df_gpt4o-df-finetune.ipynb
- 
- DragonFire Google Drive (https://drive.google.com/drive/folders/1EteF1cjATzAdFOUvCkIhObi_1JEJguWd?usp=sharing) - Contains Llama3.1 model and limited GPT-2 model trained on ScienceWorld tasks.  Also includes supporting infrastructure and logs for runs of these models.  

# Additional code files
## subgoal-agent/main.py
### Description
This is a code file that represents a limited agent subgoal planning capability for the tasks of boiling or freezing water.  It generates a sequence of actions that a human player could take to accomplish one of these two tasks using the baseline Scienceworld environment (not CALM or DRRN).  It is capable of generating alternate gold paths for future training.

### Usage
To use the subgoal-agent for planning, use the following command:

`python subgoal-agent/main.py <starting scienceworld location>`.

Ex: `python subgoal-agent/main.py kitchen`

Example output from the subgoal-agent program:
```
Starting location: kitchen
Path to closest container: []
Container options in kitchen: ['chair', 'counter', 'cupboard', 'glass cup', 'glass jar', 'table', 'wood bowl', 'wood cup']
Path to closest water source: []
Water source options in kitchen: ['sink']
Path to closest heat source: []
Heat source options in kitchen: ['oven', 'stove']
Path to closest cooling source: []
Cooling source options in kitchen: ['freezer', 'fridge']
Boil water instructions: ['Pick up chair', 'Activate sink', 'Move chair in inventory to sink', 'Wait', 'Pick up chair', 'Focus on water', 'Activate stove', 'Move chair in inventory to stove', 'Wait', 'Wait', 'Wait']
Freeze water instructions: ['Pick up counter', 'Activate sink', 'Move counter in inventory to sink', 'Wait', 'Pick up counter', 'Focus on water', 'Activate fridge', 'Open fridge', 'Move counter in inventory to fridge', 'Wait', 'Wait', 'Wait']
```

These actions can be utilized with the human-interactive agent provided by the base Scienceworld repository.  Instructions for executing the human-interactive agent are available in the base Scienceworld repository.

Interestingly, a lot of things count as containers for the purpose of holding liquid like `table`, `chair`, `cupboard`, and `beehive`.  Counterintuitively, the `fountain` item located in the `outside` location doesn't work as well as it constantly resets its water supply and appears to prevent steam or ice from building up.
