def n_input_and_gate(*inputs):
    """N-input AND gate."""
    return all(inputs)
def n_input_or_gate(*inputs):
    """N-input OR gate."""
    return any(inputs)
def n_input_nand_gate(*inputs):
    """N-input NAND gate."""
    return not all(inputs)
def n_input_nor_gate(*inputs):
    """N-input NOR gate."""
    return not any(inputs)
def n_input_xor_gate(*inputs):
    """N-input XOR gate. Returns True if an odd number of inputs are True."""
    return sum(inputs) % 2 == 1
def n_input_xnor_gate(*inputs):
    """N-input XNOR gate. Returns True if an even number of inputs are True (including zero)."""
    return sum(inputs) % 2 == 0
def not_gate(input_value):
    """Single-input NOT gate."""
    return not input_value
def buff_gate(input_value):
    """Single-input buffer gate."""
    return input_value

def execute_gate_operation(gate, input_vector):
    # gate is expected to be a dictionary with keys 'type' and 'inputs', e.g., {'type': 'AND', 'inputs': ['1', '2']}

    # Mapping gate type to the corresponding function, including NOT and BUFF gates
    gate_type_to_function = {
        'AND': n_input_and_gate,
        'OR': n_input_or_gate,
        'NAND': n_input_nand_gate,
        'NOR': n_input_nor_gate,
        'XOR': n_input_xor_gate,
        'XNOR': n_input_xnor_gate,
        'NOT': not_gate,
        'BUFF': buff_gate
    }

    # Retrieve the gate function based on the gate type
    gate_function = gate_type_to_function.get(gate['type'])
    if gate_function is None:
        return None

    # Prepare the inputs for the gate from the input vector
    gate_inputs = [input_vector.get(inp) for inp in gate['inputs']]

    # For NOT and BUFF gates, which are single-input gates, pass only the first input
    if gate['type'] in ['NOT', 'BUFF']:
        return gate_function(gate_inputs[0])
    
    # Execute the gate function with the prepared inputs
    return gate_function(*gate_inputs)
    
def create_input_vector(primary_inputs, input_string):


    # Check if the length of input_string matches the number of primary inputs
    if len(input_string) != len(primary_inputs):
        return None

    # Create the input vector
    input_vector = {}
    for i, input_id in enumerate(primary_inputs):
        input_vector[input_id] = input_string[i] == '1'

    return input_vector

def true_value_logic_simulator(circuit_inputs, input_string, circuit_outputs, gates, fanout_map):
    input_vector = create_input_vector(circuit_inputs, input_string)
    if input_vector is None:
        return None
    circuit_location_vector = input_vector.copy()
    for input_id in circuit_inputs:
        if input_id in fanout_map:
            for fanout in fanout_map[input_id]:
                circuit_location_vector[fanout] = input_vector[input_id]

    gates_to_process = list(gates.keys())
    while gates_to_process:
        gate_id = gates_to_process.pop(0)
        gate = gates[gate_id]
        gate_output = execute_gate_operation(gate, circuit_location_vector)
        circuit_location_vector[gate_id] = gate_output
        if gate_id in fanout_map:
            for fanout in fanout_map[gate_id]:
                circuit_location_vector[fanout] = gate_output
                if fanout in gates:
                    gates_to_process.append(fanout)
    output_vector = {output: circuit_location_vector[output] for output in circuit_outputs}
    return output_vector
def generate_binary_vectors(input_list):
    num_inputs = len(input_list)
    num_combinations = 2 ** num_inputs
    binary_vectors = []

    for i in range(num_combinations):
        # Convert the number to binary and format it to fit the input length
        binary_str = format(i, f'0{num_inputs}b')
        binary_vectors.append(binary_str)

    return binary_vectors
"""
## Testing the generate_binary_vectors function
example_inputs = ['1', '2', '3','293']
all_binary_vectors = generate_binary_vectors(example_inputs)
print(all_binary_vectors)

##test the true_value_logic_simulator function
example_circuit_inputs = ['1', '2', '3', '6', '7', '8']
example_input_string = '110101'
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
print(true_value_logic_simulator(example_circuit_inputs, example_input_string, example_circuit_outputs, example_gates, example_fanout_map))

## Testing the execute_gate_operation function
example_gate = {'type': 'NOT', 'inputs': ['1']}
example_input_vector = {'1': True, '2': False, '7': True}


print(execute_gate_operation(example_gate, example_input_vector))

## Testing the create_input_vector function

primary_inputs_example = ['1', '2', '3', '6', '7']
input_string_example = '11011'

input_vec = create_input_vector(primary_inputs_example, input_string_example)
print(input_vec)

##test each gate
and_result = n_input_and_gate(True, True, False)  # Should return False
or_result = n_input_or_gate(True, True, False) # Should return True
nand_result = n_input_nand_gate(True, True, False)  # Should return True
nor_result = n_input_nor_gate(False, False, False)  # Should return True
xor_result = n_input_xor_gate(True, True, True)    # Should return True
xnor_result = n_input_xnor_gate(True, True, True)   # Should return False
not_result = not_gate(True)  # Should return False
buff_result = buff_gate(True)  # Should return True
print(and_result)
print(or_result)
print(nand_result)
print(nor_result)
print(xor_result)
print(xnor_result)
print(not_result)
print(buff_result)
"""



