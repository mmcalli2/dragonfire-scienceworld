# README file for DragonFire AI project
Creators: Patricia Delafuente and Marcus McAllister

The DragonFire AI project makes use of multiple existing codebases and datasets.  An inventory of referenced material is listed below:

- ScienceWorld repository (https://github.com/allenai/ScienceWorld) - Contains Python + Scala code for a random agent and human-interactive agent.  Instructions for running these agents are found in the dedicated README for the ScienceWorld repository.

- CALM-ScienceWorld repository (https://github.com/cognitiveailab/calm-scienceworld) - Contains Python code for training an intelligent agent to solve ScienceWorld tasks using OpenAI GPT-2.  Instructions for training this agent are found in the dedicated README for the CALM-ScienceWorld repository.  Note that the hardware requirements for training the models are significant, so training may take significantly longer on average compute platforms.

- Hugginface Transformers (https://github.com/huggingface/transformers) - Leverages the Transformers libraries and scripts for training and inference of the RoBERTA and BERT models.
- 
- Intent Detection with Wikihow (https://github.com/zharry29/wikihow-intent) is the original inspiration for this project which is to determine an action to take based on a task and environment observations. 
- @misc{zhang2020intent,
    title={Intent Detection with WikiHow},
    author={Li Zhang and Qing Lyu and Chris Callison-Burch},
    year={2020},
    eprint={2009.05781},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

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
