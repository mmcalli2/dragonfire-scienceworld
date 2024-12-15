from lm import *
import jsonlines

model = GPT2LM("temp")

k = 30

overall_count = 0
success_count = 0
failure_count = 0

with jsonlines.open('data/sciworld_formatted_test.jsonl') as reader:
  for obj in reader:
    overall_count += 1

    # Strip trailing [SEP] token from target.
    target = obj["target"].rstrip("[SEP]").strip()

    # Feed input into model to generate actions.
    input = obj["input"]
    actions = model.generate(input, k)

    # Determine if the target action is among the generated actions.
    print(f"Target: {target}")
    if target in actions:
      print(f"Success")
      success_count += 1
    else:
      print(f"Failure")
      print(f"Actions Generated: {actions}")
      failure_count += 1

    if (overall_count % 50) == 0:
      print()
      print(f"Checkpoint {overall_count}")
      print(f"Current number of successes: {success_count}")
      print(f"Current number of failures: {failure_count}")
      print()

print()
print(f"Testing complete!")
print(f"Number of entries: {overall_count}")
print(f"Number of successes: {success_count}")
print(f"Number of failures: {failure_count}")
