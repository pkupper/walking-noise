import os
import re


#########################
#       DEFINITIONS     #
#########################
LOG_PATH = os.path.abspath("../logs/")
OUT_PATH = os.path.abspath("../logs/compiled.out")
MEASUREMENT_REGEX = r"(?<=INF DATA)(True.*?|False.*?)(?=INF END)"

SLURM_JOB_ID = '12423'

def listdir(path, extension=str()):
    for file_name in os.listdir(path):
        if SLURM_JOB_ID in file_name:
            file_path = os.path.join(path, file_name)
            if file_path.endswith(extension) and os.path.isfile(file_path):
                yield file_path


def extract_inference_measurements(file):
    matches = re.findall(MEASUREMENT_REGEX, file, re.DOTALL)
    return [match.strip() for match in matches]


def export_measurements(measurements, path):
    with open(path, 'w') as file:
        file.write("TrainFirstMulThenAdd,TrainGaussStdMul,TrainGaussStdAdd,InfFirstMulThenAdd,InfGaussStdMul,InfGaussStdAdd,Accuracy\n")
        for measurement in measurements:
            file.write(f"{measurement}\n")


if __name__ == "__main__":
    compilation = []
    
    # Iterate over each log file and
    # parse the inference measurements.
    for file_path in listdir(LOG_PATH, extension=".out"):
        with open(file_path, 'r') as file:
            content = file.read()
            measurements = extract_inference_measurements(content)
            print(measurements)
            compilation.extend(measurements)
    
    # Materialize measurerments into compilation file.
    export_measurements(compilation, OUT_PATH)
    