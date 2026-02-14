import sys
from .topsis_engine import TopsisCalculator


def main():

    if len(sys.argv) != 5:
        print("Usage: topsis <InputFile> <Weights> <Impacts> <OutputFile>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    try:
        calculator = TopsisCalculator(input_file, weights, impacts, output_file)
        calculator.execute()
        print("TOPSIS executed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")
