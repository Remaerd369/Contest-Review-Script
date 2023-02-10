import plotly.express as px
import requests
import json
import re
import csv

def extract_info(solidity_code):
    # Regular expression to match function signature information
    func_pattern = re.compile(r"function\s+(\w+)\((.*?)\)")
    # Regular expression to match contract definition information
    contract_pattern = re.compile(r"contract\s+(\w+)")

    # Dictionary to store the extracted information
    info = {}

    # Split the Solidity code into lines
    lines = solidity_code.split("\n")

    # Keep track of the current contract
    current_contract = None

    # Loop through the lines
    for line in lines:
        # Try to match the line to the contract definition pattern
        match = re.search(contract_pattern, line)
        if match:
            # Update the current contract name
            current_contract = match.group(1)
            info[current_contract] = {}
            continue

        # Try to match the line to the function signature pattern
        match = re.search(func_pattern, line)

        # If the line matches the pattern
        if match:
            # Extract the function name and parameters
            func_name = match.group(1)
            func_params = match.group(2).split(",")

            # Add the extracted information to the dictionary
            info[current_contract][func_name] = {"params": func_params, "logic": []}

            # Get the start and end lines of the function
            start_line = lines.index(line) + 1
            end_line = start_line
            for i in range(start_line, len(lines)):
                if "}" in lines[i]:
                    end_line = i
                    break

            # Add the logic lines to the dictionary
            for i in range(start_line, end_line):
                info[current_contract][func_name]["logic"].append(lines[i].strip())

    return info

# Example Solidity code
solidity_code = """
"""



# Dictionary to store the mapping of tasks to contract function signatures
contract_mapping = {}

# Get the extracted information from the Solidity code
info = extract_info(solidity_code)

# Loop through the extracted information
for contract_name, contract_info in info.items():
    for func_name, func_info in contract_info.items():
        task_name = f"{contract_name}.{func_name}"
        contract_mapping[task_name] = func_info["params"]

print (contract_mapping)

def extract_info(contract_interface):
  contract_functions = contract_interface['abi']

  # dictionary to store the information
  contract_mapping = {}

  for contract_function in contract_functions:
    function_name = contract_function['name']
    function_inputs = contract_function['inputs']
    function_output = contract_function['outputs']

    # store function inputs and outputs information
    contract_mapping[function_name] = {}
    contract_mapping[function_name]['inputs'] = [{'name': x['name'], 'type': x['type']} for x in function_inputs]
    contract_mapping[function_name]['output'] = [{'name': x['name'], 'type': x['type']} for x in function_output]
    contract_mapping[function_name]['constant'] = contract_function['constant']

  # Add events information
  contract_events = contract_interface['events']
  contract_mapping['events'] = {}
  for contract_event in contract_events:
    event_name = contract_event['name']
    event_inputs = contract_event['inputs']

    contract_mapping['events'][event_name] = [{'name': x['name'], 'type': x['type']} for x in event_inputs]

  return contract_mapping


# Dictionary to store the number of functions in each contract
contract_function_count = {}

# Loop through the extracted information
for contract_name, contract_info in info.items():
    contract_function_count[contract_name] = len(contract_info)

fig = px.bar(contract_function_count.items(), y=[x[0] for x in contract_function_count.items()], x=[x[1] for x in contract_function_count.items()], text=[str(x[1]) for x in contract_function_count.items()])

# Customize the appearance of the graph
fig.update_layout(title="Function Usage in Smart Contract",
                  xaxis_title="Usage Count",
                  yaxis_title="Function Name")

fig.update_traces(marker_color='red', marker_line_color='black',
                  marker_line_width=1.5, opacity=0.6)

# Show the graph
fig.show()




with open('contract_mapping.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Function', 'Arguments'])
    for key, value in contract_mapping.items():
        writer.writerow([key, value])


# Save the dictionary to a file
with open("contract_mapping.txt", "w") as f:
    for task_name, params in contract_mapping.items():
        f.write("{}: {}\n".format(task_name, params))