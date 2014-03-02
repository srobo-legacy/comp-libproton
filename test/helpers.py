
import os
import yaml

def tla_result_fixture(zone_number, score = 0):
    return {
        "score": score,
        "present": True,
        "disqualified": False,
        "zone": zone_number,
    }

def get_data(data_root, input_name):
    input_file = os.path.join(data_root, input_name)
    output_file = os.path.join(data_root, input_name[:-5] + '.out.yaml')

    assert os.path.exists(output_file), "Missing output expectation '{1}' for input '{0}'.".format(input_name, output_file)

    expected_output = yaml.load(open(output_file).read())
    return input_file, expected_output

def get_input_files(data_root):
    files = os.listdir(data_root)
    outputs = [f for f in files if f.endswith('.out.yaml')]
    inputs = [f for f in files if f.endswith('.yaml') and not f in outputs]

    return inputs
