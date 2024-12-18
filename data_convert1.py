import argparse
import json
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='data/goldpaths-all')
    parser.add_argument('--output_dir', default='data')
    return parser.parse_args()

args = parse_args()
data_dir = args.data_dir
raw_data_list = []

for filename in os.listdir(data_dir):
    with open(os.path.join(data_dir, filename), 'r') as f:
        raw_data_list.append(json.load(f))

train_data = []
val_data = []
test_data = []

def clean(s):
    clean_toks = ['\n', '\t']
    for tok in clean_toks:
        s = s.replace(tok, ' ')
    return s

cnt = 0
for raw_data in raw_data_list:
    
    for task_id in raw_data.keys():
        if cnt == 0:
            cnt = cnt + 1
            curr_task = raw_data[task_id]
            for seq_sample in curr_task['goldActionSequences']:
                task_desc = seq_sample['taskDescription']
                steps = seq_sample['path']
                if len(steps) < 2:
                    continue
                fold = seq_sample['fold']
                obs = steps[0]['observation']
                action = steps[0]['action']
                for i in range(len(steps)-1):
                    if i != 0:
                        prev_step = steps[i-1]
                        curr_step = steps[i]
                        next_step = steps[i+1]

                        prev_action = curr_step['action']
                        curr_action = next_step['action']
                        prev_obs = prev_step['observation']
                        curr_obs = curr_step['observation']
                        look = curr_step['freelook']
                        inventory = curr_step['inventory']

                        if curr_action == 'look around':
                            continue

                        input_str = '[CLS] ' + task_desc + ' [SEP] ' + curr_obs + ' [SEP] ' + inventory + ' [SEP] ' \
                        + look + ' [SEP] '   + prev_obs + ' [SEP] ' + prev_action + ' [SEP]'
                        target = f"{curr_action} [SEP]"



                    else:
                        curr_step = steps[i]
                        next_step = steps[i+1]
                        curr_action = next_step['action']
                        curr_obs = curr_step['observation']
                        look = curr_step['freelook']
                        inventory = curr_step['inventory']

                        if curr_action == 'look around':
                            continue

                        input_str = '[CLS] ' + task_desc + ' [SEP] ' + curr_obs + ' [SEP] ' \
                        + inventory + ' [SEP] ' + look + ' [SEP] ' + '[SEP] [SEP]'
                        target = f"{curr_action} [SEP]"

                    curr_dat = {'input': clean(input_str), 'target':clean(target)}

                    if fold == 'train':
                        train_data.append(curr_dat)
                    elif fold == 'dev':
                        val_data.append(curr_dat)
                    elif fold == 'test':
                        test_data.append(curr_dat)

with open(os.path.join(args.output_dir,"sciworld_formatted_train1.jsonl"), 'w') as f:
    for item in train_data:
        f.write(json.dumps(item) + "\n")

with open(os.path.join(args.output_dir,"sciworld_formatted_val1.jsonl"), 'w') as f:
    for item in val_data:
        f.write(json.dumps(item) + "\n")

with open(os.path.join(args.output_dir,"sciworld_formatted_test1.jsonl"), 'w') as f:
    for item in test_data:
        f.write(json.dumps(item) + "\n")
