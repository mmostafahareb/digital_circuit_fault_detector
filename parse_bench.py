import sys
def parse_circuit_with_fanouts(contents):
    inputs, outputs, gates = [], [], {}
    fanout_map = {}
    fanout_counter = {}

    # First pass: Identify inputs, outputs, and gate definitions
    for line in contents.split('\n'):
        line = line.strip()
        if line.startswith('INPUT'):
            inputs.append(line.split('(')[1].split(')')[0])
        elif line.startswith('OUTPUT'):
            outputs.append(line.split('(')[1].split(')')[0])
        elif '=' in line:
            gate_name, gate_def = line.split('=')
            gate_type, gate_inputs = gate_def.split('(')
            gate_inputs = gate_inputs.split(')')[0].split(', ')
            gates[gate_name.strip()] = {'type': gate_type.strip(), 'inputs': gate_inputs}

    # Determine fanout counts for each input/gate output
    for gate in gates.values():
        for inp in gate['inputs']:
            if inp not in fanout_counter:
                fanout_counter[inp] = 0
            fanout_counter[inp] += 1

    # Second pass: Update gates for fanouts and build fanout map
    for gate_name, gate_info in gates.items():
        for i, inp in enumerate(gate_info['inputs']):
            if fanout_counter[inp] > 1:
                if inp not in fanout_map:
                    fanout_map[inp] = []
                    counter = 1
                else:
                    counter = len(fanout_map[inp]) + 1
                fanout_id = f"{inp}_{counter}"
                gate_info['inputs'][i] = fanout_id
                fanout_map[inp].append(fanout_id)

    return inputs, outputs, gates, fanout_map




def get_SA_faults(inputs, gates, fanout_map):
    num_primary_inputs = len(inputs)
    num_gates = len(gates)
    total_fanouts = sum(len(fanouts) for fanouts in fanout_map.values())

    return 2 * num_primary_inputs + 2 * num_gates + 2 * total_fanouts




def print_circuit_info(inputs, outputs, gates, fanout_map, sa_faults):
    print("Inputs:", inputs)
    print("Number of inputs: ", str(len(inputs)))
    print("Outputs:", outputs)
    print("Number of outputs: ", str(len(outputs)))
    print("Gates:")
    for gate, details in gates.items():
        print(f"  {gate} = {details}")
    print("Number of gates: ", str(len(gates)))    
    print("Fanout Map:", fanout_map)
    print("Total Single Stuck-at Faults:", sa_faults)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py path_to_bench_file")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            circuit_description = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    inputs, outputs, gates, fanout_map = parse_circuit_with_fanouts(circuit_description)
    sa_faults = get_SA_faults(inputs, gates, fanout_map)
    print_circuit_info(inputs, outputs, gates, fanout_map, sa_faults)

if __name__ == "__main__":
    main()
