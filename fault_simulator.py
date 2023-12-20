from run_circuit_simulation import execute_gate_operation, create_input_vector, generate_binary_vectors, true_value_logic_simulator 
from parse_bench import parse_circuit_with_fanouts,  get_SA_faults, print_circuit_info
import time
import sys
import itertools

def get_potential_fault_list(primary_inputs, gates, fanout_map):
    potential_faults = []

    # Add faults for primary inputs
    for input_id in primary_inputs:
        potential_faults.append({input_id: True})
        potential_faults.append({input_id: False})

    # Add faults for gate outputs
    for gate_id in gates:
        potential_faults.append({gate_id: True})
        potential_faults.append({gate_id: False})

    # Add faults for fanouts
    for fanouts in fanout_map.values():
        for fanout in fanouts:
            potential_faults.append({fanout: True})
            potential_faults.append({fanout: False})

    return potential_faults
def insert_faults_into_circuit(fault_vector, circuit_vector):
    for key in fault_vector:
        if key in circuit_vector:
            circuit_vector[key] = fault_vector[key]

def fault_logic_simulator(circuit_inputs, input_string, circuit_outputs, gates, fanout_map, faults_to_test):
    
    input_vector = create_input_vector(circuit_inputs, input_string)
    if input_vector is None:
        return None
    circuit_location_vector = input_vector.copy()
    insert_faults_into_circuit(faults_to_test, circuit_location_vector)
    for input_id in circuit_inputs:
        if input_id in fanout_map:
            for fanout in fanout_map[input_id]:
                circuit_location_vector[fanout] = input_vector[input_id]
            insert_faults_into_circuit(faults_to_test, circuit_location_vector)

    gates_to_process = list(gates.keys())
    while gates_to_process:
        gate_id = gates_to_process.pop(0)
        gate = gates[gate_id]
        gate_output = execute_gate_operation(gate, circuit_location_vector)
        circuit_location_vector[gate_id] = gate_output
        insert_faults_into_circuit(faults_to_test, circuit_location_vector)
        if gate_id in fanout_map:
            for fanout in fanout_map[gate_id]:
                circuit_location_vector[fanout] = circuit_location_vector[gate_id]
                if fanout in gates:
                    gates_to_process.append(fanout)
            insert_faults_into_circuit(faults_to_test, circuit_location_vector)
    output_vector = {output: circuit_location_vector[output] for output in circuit_outputs}
    return output_vector
def create_multiple_fault_list(dict_list):
    combined_dicts = []

    # Generate combinations starting from length 2 to the length of the dict_list
    for i in range(2, len(dict_list) + 1):
        for combo in itertools.combinations(dict_list, i):
            combined_dict = {}
            skip_combo = False

            for d in combo:
                # Check if the key is already in the combined_dict
                if any(key in combined_dict for key in d):
                    skip_combo = True
                    break
                else:
                    combined_dict.update(d)

            if not skip_combo:
                combined_dicts.append(combined_dict)

    return combined_dicts

def get_fault_coverage(detected_faults, all_faults):
    return str(((len(detected_faults)+0.0)/len(all_faults)) * 100) + "%"
    
def get_fault_efficiency(detected_faults, undetectable_faults, all_faults):
    return str(((len(detected_faults)+0.0)/(len(all_faults) - len(undetectable_faults))) * 100) + "%"
    
def get_simulation_duration(start, end):
    return str(end - start) + " seconds"
    
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
    start_time = time.time()
    single_fault_list = get_potential_fault_list(inputs, gates, fanout_map)
    input_vectors = generate_binary_vectors(inputs)
    true_value_outputs = {}
    for vector in input_vectors:
        true_value_outputs[vector] = true_value_logic_simulator(inputs, vector, outputs, gates, fanout_map)
    detected_faults = []   
    undetectable_faults = []
    for fault in single_fault_list:
        has_not_been_detected = True
        for vector in input_vectors:
            fault_outputs = fault_logic_simulator(inputs, vector, outputs, gates, fanout_map, fault)
            if fault_outputs != true_value_outputs[vector]:
                has_not_been_detected = False
                detected_faults.append(fault)
                break
        if has_not_been_detected:
            undetectable_faults.append(fault)
    
    end_time = time.time()
    print("number of detected faults: "+ str(len(detected_faults)))
    print("detected faults: " + str(detected_faults))
    print("number of undetectable faults: "+ str(len(undetectable_faults)))
    print("undetectable faults: " + str(undetectable_faults))
    print("--------------------------------------------------------------")
    print("Fault Coverage: " + get_fault_coverage(detected_faults, single_fault_list))
    print("Fault Efficiency: " + get_fault_efficiency(detected_faults, undetectable_faults, single_fault_list))
    print("Simulation Duration: " + get_simulation_duration(start_time, end_time))

if __name__ == "__main__":
    main()
"""    
example_circuit_inputs = ['1', '2', '3', '6', '7', '8']
example_input_string = '110000'
example_circuit_outputs = ['19', '20', '21']
example_gates = {
    '17': {'type': 'AND', 'inputs': ['1', '2']},
    '18': {'type': 'OR', 'inputs': ['3', '6_1']},
    '19': {'type': 'NAND', 'inputs': ['17_1', '6_2']},
    '20': {'type': 'OR', 'inputs': ['17_2', '7']},
    '21': {'type': 'NOR', 'inputs': ['17_3', '8']},
}
example_fanout_map = {
    '6': ['6_1','6_2'],
    '17': ['17_1', '17_2', '17_3'],
}
exaple_fault_list = {
    '17': False,
    '17_2': True
}
print(fault_logic_simulator(example_circuit_inputs, example_input_string, example_circuit_outputs, example_gates, example_fanout_map, exaple_fault_list))

# Example usage
example_primary_inputs = ['1', '2']
example_gates = {'17': {'type': 'AND', 'inputs': ['1', '2']}}
example_fanout_map = {'1': ['18'], '2': ['19']}

# Generate potential fault list
potential_fault_list = get_potential_fault_list(example_primary_inputs, example_gates, example_fanout_map)
print(potential_fault_list)
"""
