# Code generated as part of AI Semester Project for Course CMSC 671

import random
import sys
from collections import deque

# Defining a class for storing node information.
class SearchNode():
  def __init__(self, location, actions_taken, known_cost):
    super().__init__()

    # Fields to store various node details.
    self.location = location
    self.actions_taken = actions_taken
    self.known_cost = known_cost

  def getEvaluationCost(self):
    """
    Calculates the total evaluation cost when using this node for search.

    Parameters:
      self (SearchNode): This object.

    Returns:
      The evaluation cost to use for inserting into an expansion queue.
    """

    return self.known_cost

def location_contains_heat_source(location):
  # Return True if the location exists and contains any heat sources, False otherwise.
  return heat_source_map.get(location) is not None

def location_contains_cooling_source(location):
  # Return True if the location exists and contains any cooling sources, False otherwise.
  return cooling_source_map.get(location) is not None

def location_contains_water_source(location):
  # Return True if the location exists and contains any water sources, False otherwise.
  return water_source_map.get(location) is not None

def location_contains_container(location):
  # Return True if the location exists and contains any movable containers, False otherwise.
  return container_map.get(location) is not None

location_set = [
  "art studio",
  "bathroom",
  "bedroom",
  "foundry",
  "greenhouse",
  "hallway",
  "kitchen",
  "living room",
  "outside",
  "workshop"
]

location_connections_map = {
  "art studio": [
    "hallway"
  ],
  "bathroom": [
    "kitchen"
  ],
  "bedroom": [
    "hallway"
  ],
  "foundry": [
    "outside"
  ],
  "greenhouse": [
    "hallway",
    "outside"
  ],
  "hallway": [
    "art studio",
    "bedroom",
    "greenhouse",
    "kitchen",
    "living room",
    "workshop"
  ],
  "kitchen": [
    "hallway",
    "outside"
  ],
  "living room": [
    "hallway"
  ],
  "outside": [
    "foundry",
    "greenhouse",
    "kitchen"
  ],
  "workshop": [
    "hallway"
  ]
}

heat_source_map = {
  "foundry": [
    "blast furnace"
  ],
  "kitchen": [
    "oven",
    "stove"
  ]
}

cooling_source_map = {
  "kitchen": [
    "freezer",
    "fridge"
  ],
  "workshop": [
    "ultra cold freezer"
  ]
}

water_source_map = {
  "bathroom": [
    "bathtub",
    "sink",
    "toilet"
  ],
  "foundry": [
    "sink"
  ],
  "greenhouse": [
    "sink"
  ],
  "kitchen": [
    "sink"
  ]
}

container_map = {
  "art studio": [
    "cupboard",
    "wood table",
    "wood cup"
  ],
  "bathroom": [
    "glass cup"
  ],
  "bedroom": [
    "closet",
    "wood table"
  ],
  "foundry": [
    "steel table"
  ],
  "greenhouse": [
    "beehive",
    "flower pot",
    "water jug"
  ],
  "kitchen": [
    "chair",
    "counter",
    "cupboard",
    "glass cup",
    "glass jar",
    "table", # Kitchen refers to generic table.
    "wood bowl",
    "wood cup"
  ],
  "living room": [
    "chair",
    "couch"
  ],
  "outside": [
    "firepit"
  ],
  "workshop": [
    "wood table"
  ]
}

containers_requiring_open_action = [
  "beehive",
  "closet",
  "cupboard",
  "glass jar"
]

heat_sources_requiring_open_action = [
  "blast furnace",
  "oven"
]

cooling_sources_requiring_open_action = [
  "freezer",
  "fridge",
  "ultra cold freezer"
]

def find_shortest_path(starting_location, goal_location):
  # Initialize search algorithm.
  actions_taken = []
  known_cost = 0
  start_node = SearchNode(starting_location, actions_taken, known_cost)

  expansion_queue = deque([])
  expansion_queue.append(start_node)
  solution_path = ""

  # Loop until a path is found or the expansion queue is empty.
  while solution_path == "" and len(expansion_queue) > 0:
    current_node = expansion_queue.popleft()

    # Check if current node satisfies goal.
    path_discovered = check_node_for_goal_satisfaction(current_node.location, goal_location)

    # If goal is not met, expand node.
    if path_discovered:
      # Solution found.
      solution_path = current_node.actions_taken
    else:
      # Solution not found, need to continue expanding.
      new_nodes = generate_expansion_nodes(current_node)

      for node in new_nodes:
        # Since using breath-first search, the nodes should be appended to the end of expansion_queue.
        expansion_queue.append(node)

  return solution_path

def check_node_for_goal_satisfaction(location, goal_location):
  """
  Determines if the specified location matches the goal location.

  Parameters:
    location (string): Location under consideration for goal satisfaction.
    goal_location (string): Terminal location representing end state.

  Returns:
    True if the specified location matches the goal location, False otherwise.
  """

  return location == goal_location

def generate_expansion_nodes(node):
  """
  Generates the set of valid nodes that can be navigated to using one move from the current node.

  Parameters:
    node (SearchNode): Node to use as relative position for expansion.

  Returns:
    A list of search nodes that can be legally reached from the current node using one move.
  """

  expansion_nodes = []

  current_location = node.location

  connected_locations = location_connections_map[current_location]

  for connected_location in connected_locations:
    new_actions_taken = node.actions_taken.copy()
    new_actions_taken.append(connected_location)
    expansion_nodes.append(SearchNode(connected_location, new_actions_taken, node.known_cost + 1))

  # Since we are using breadth-first search, any of the branches are equally valid for ordering.
  random.shuffle(expansion_nodes)

  return expansion_nodes

def generate_path_to_closest_heat_source(starting_location):
  # Initialize search algorithm.
  actions_taken = []
  known_cost = 0
  start_node = SearchNode(starting_location, actions_taken, known_cost)

  expansion_queue = deque([])
  expansion_queue.append(start_node)
  solution_path = ""

  # Loop until a path is found or the expansion queue is empty.
  while solution_path == "" and len(expansion_queue) > 0:
    current_node = expansion_queue.popleft()

    # Check if current node satisfies goal.
    path_discovered = location_contains_heat_source(current_node.location)

    # If goal is not met, expand node.
    if path_discovered:
      # Solution found.
      solution_path = current_node.actions_taken
    else:
      # Solution not found, need to continue expanding.
      new_nodes = generate_expansion_nodes(current_node)

      for node in new_nodes:
        # Since using breath-first search, the nodes should be appended to the end of expansion_queue.
        expansion_queue.append(node)

  return solution_path

def generate_path_to_closest_cooling_source(starting_location):
  # Initialize search algorithm.
  actions_taken = []
  known_cost = 0
  start_node = SearchNode(starting_location, actions_taken, known_cost)

  expansion_queue = deque([])
  expansion_queue.append(start_node)
  solution_path = ""

  # Loop until a path is found or the expansion queue is empty.
  while solution_path == "" and len(expansion_queue) > 0:
    current_node = expansion_queue.popleft()

    # Check if current node satisfies goal.
    path_discovered = location_contains_cooling_source(current_node.location)

    # If goal is not met, expand node.
    if path_discovered:
      # Solution found.
      solution_path = current_node.actions_taken
    else:
      # Solution not found, need to continue expanding.
      new_nodes = generate_expansion_nodes(current_node)

      for node in new_nodes:
        # Since using breath-first search, the nodes should be appended to the end of expansion_queue.
        expansion_queue.append(node)

  return solution_path

def generate_path_to_closest_water_source(starting_location):
  # Initialize search algorithm.
  actions_taken = []
  known_cost = 0
  start_node = SearchNode(starting_location, actions_taken, known_cost)

  expansion_queue = deque([])
  expansion_queue.append(start_node)
  solution_path = ""

  # Loop until a path is found or the expansion queue is empty.
  while solution_path == "" and len(expansion_queue) > 0:
    current_node = expansion_queue.popleft()

    # Check if current node satisfies goal.
    path_discovered = location_contains_water_source(current_node.location)

    # If goal is not met, expand node.
    if path_discovered:
      # Solution found.
      solution_path = current_node.actions_taken
    else:
      # Solution not found, need to continue expanding.
      new_nodes = generate_expansion_nodes(current_node)

      for node in new_nodes:
        # Since using breath-first search, the nodes should be appended to the end of expansion_queue.
        expansion_queue.append(node)

  return solution_path

def generate_path_to_closest_container(starting_location):
  # Initialize search algorithm.
  actions_taken = []
  known_cost = 0
  start_node = SearchNode(starting_location, actions_taken, known_cost)

  expansion_queue = deque([])
  expansion_queue.append(start_node)
  solution_path = ""

  # Loop until a path is found or the expansion queue is empty.
  while solution_path == "" and len(expansion_queue) > 0:
    current_node = expansion_queue.popleft()

    # Check if current node satisfies goal.
    path_discovered = location_contains_container(current_node.location)

    # If goal is not met, expand node.
    if path_discovered:
      # Solution found.
      solution_path = current_node.actions_taken
    else:
      # Solution not found, need to continue expanding.
      new_nodes = generate_expansion_nodes(current_node)

      for node in new_nodes:
        # Since using breath-first search, the nodes should be appended to the end of expansion_queue.
        expansion_queue.append(node)

  return solution_path

def acquire_container_subgoal(starting_location):
  # Generate path to the closest location with a container.
  path_to_closest_container = generate_path_to_closest_container(starting_location)

  # Identify the final location that is visited.
  final_location = starting_location
  if len(path_to_closest_container) > 0:
    final_location = path_to_closest_container[-1]

  # Pick up a random container from the final location.
  container = random.choice(container_map[final_location])

  # Generate instructions for accomplishing subgoal.
  instructions = []
  for location in path_to_closest_container:
    instructions.append(f"Open door to {location}")
    instructions.append(f"Move to {location}")

  # Add instruction to acquire container.
  instructions.append(f"Pick up {container}")

  # Need to provide instructions and final location for future processing.
  return (instructions, container, final_location)

def put_water_in_container_subgoal(starting_location, container):
  # Generate path to the closest location with a water source.
  path_to_closest_water_source = generate_path_to_closest_water_source(starting_location)

  # Identify the final location that is visited.
  final_location = starting_location
  if len(path_to_closest_water_source) > 0:
    final_location = path_to_closest_water_source[-1]

  # Choose a random water source at the location.
  water_source = random.choice(water_source_map[final_location])

  # Generate instructions for accomplishing subgoal.
  instructions = []
  for location in path_to_closest_water_source:
    instructions.append(f"Open door to {location}")
    instructions.append(f"Move to {location}")

  # Add instruction to activate water source.
  instructions.append(f"Activate {water_source}")

  # Determine if the container needs to be opened.
  if container in containers_requiring_open_action:
    instructions.append(f"Open {container}")

  # Add the container to the water source.
  instructions.append(f"Move {container} in inventory to {water_source}")

  # Wait for water to appear.
  instructions.append(f"Wait")

  # Add instruction to reacquire container with water.
  instructions.append(f"Pick up {container}")

  # Add instruction to focus on the water.
  instructions.append(f"Focus on water")

  # Need to provide instructions and final location for future processing.
  return (instructions, container, final_location)

def apply_heat_source_to_water_subgoal(starting_location, container):
  # Generate path to the closest location with a heat source.
  path_to_closest_heat_source = generate_path_to_closest_heat_source(starting_location)

  # Identify the final location that is visited.
  final_location = starting_location
  if len(path_to_closest_heat_source) > 0:
    final_location = path_to_closest_heat_source[-1]

  # Choose a random heat source at the location.
  heat_source = random.choice(heat_source_map[final_location])

  # Generate instructions for accomplishing subgoal.
  instructions = []
  for location in path_to_closest_heat_source:
    instructions.append(f"Open door to {location}")
    instructions.append(f"Move to {location}")

  # Add instruction to activate heat source.
  instructions.append(f"Activate {heat_source}")

  # Determine if the heat source needs to be opened.
  if heat_source in heat_sources_requiring_open_action:
    instructions.append(f"Open {heat_source}")

  # Add the container to the heat source.
  instructions.append(f"Move {container} in inventory to {heat_source}")

  # Wait for steam to appear.
  instructions.append(f"Wait")
  instructions.append(f"Wait")
  instructions.append(f"Wait")

  return instructions

def apply_cooling_source_to_water_subgoal(starting_location, container):
  # Generate path to the closest location with a cooling source.
  path_to_closest_cooling_source = generate_path_to_closest_cooling_source(starting_location)

  # Identify the final location that is visited.
  final_location = starting_location
  if len(path_to_closest_cooling_source) > 0:
    final_location = path_to_closest_cooling_source[-1]

  # Choose a random cooling source at the location.
  cooling_source = random.choice(cooling_source_map[final_location])

  # Generate instructions for accomplishing subgoal.
  instructions = []
  for location in path_to_closest_cooling_source:
    instructions.append(f"Open door to {location}")
    instructions.append(f"Move to {location}")

  # Add instruction to activate cooling source.
  instructions.append(f"Activate {cooling_source}")

  # Determine if the cooling source needs to be opened.
  if cooling_source in cooling_sources_requiring_open_action:
    instructions.append(f"Open {cooling_source}")

  # Add the container to the cooling source.
  instructions.append(f"Move {container} in inventory to {cooling_source}")

  # Wait for ice to appear.
  instructions.append(f"Wait")
  instructions.append(f"Wait")
  instructions.append(f"Wait")

  return instructions

def task_boil_water(starting_location):
  (acquire_container_instructions, container, container_location) = acquire_container_subgoal(starting_location)
  (put_water_in_container_instructions, container, water_source_location) = put_water_in_container_subgoal(container_location, container)
  apply_heat_source_to_water_instructions = apply_heat_source_to_water_subgoal(water_source_location, container)
  instructions = acquire_container_instructions + put_water_in_container_instructions + apply_heat_source_to_water_instructions

  return instructions

def task_freeze_water(starting_location):
  (acquire_container_instructions, container, container_location) = acquire_container_subgoal(starting_location)
  (put_water_in_container_instructions, container, water_source_location) = put_water_in_container_subgoal(container_location, container)
  apply_cooling_source_to_water_instructions = apply_cooling_source_to_water_subgoal(water_source_location, container)
  instructions = acquire_container_instructions + put_water_in_container_instructions + apply_cooling_source_to_water_instructions

  return instructions

def debug(location):
  # Debug container acquisition.
  path_to_closest_container = generate_path_to_closest_container(location)
  print(f"Path to closest container: {path_to_closest_container}")

  final_container_location = location
  if len(path_to_closest_container) > 0:
    final_container_location = path_to_closest_container[-1]

  container_options = container_map[final_container_location]
  print(f"Container options in {final_container_location}: {container_options}")

  # Debug water source.
  path_to_closest_water_source = generate_path_to_closest_water_source(location)
  print(f"Path to closest water source: {path_to_closest_water_source}")

  final_water_source_location = location
  if len(path_to_closest_water_source) > 0:
    final_water_source_location = path_to_closest_water_source[-1]

  water_source_options = water_source_map[final_water_source_location]
  print(f"Water source options in {final_water_source_location}: {water_source_options}")

  # Debug heat source.
  path_to_closest_heat_source = generate_path_to_closest_heat_source(location)
  print(f"Path to closest heat source: {path_to_closest_heat_source}")

  final_heat_source_location = location
  if len(path_to_closest_heat_source) > 0:
    final_heat_source_location = path_to_closest_heat_source[-1]

  heat_source_options = heat_source_map[final_heat_source_location]
  print(f"Heat source options in {final_heat_source_location}: {heat_source_options}")

  # Debug cooling source.
  path_to_closest_cooling_source = generate_path_to_closest_cooling_source(location)
  print(f"Path to closest cooling source: {path_to_closest_cooling_source}")

  final_cooling_source_location = location
  if len(path_to_closest_cooling_source) > 0:
    final_cooling_source_location = path_to_closest_cooling_source[-1]

  cooling_source_options = cooling_source_map[final_cooling_source_location]
  print(f"Cooling source options in {final_cooling_source_location}: {cooling_source_options}")

def main():
  args = sys.argv[1:]

  starting_location = args[0]

  print(f"Starting location: {starting_location}")

  debug(starting_location)

  boil_water_instructions = task_boil_water(starting_location)
  print(f"Boil water instructions: {boil_water_instructions}")

  freeze_water_instructions = task_freeze_water(starting_location)
  print(f"Freeze water instructions: {freeze_water_instructions}")

if __name__=="__main__":
  main()
