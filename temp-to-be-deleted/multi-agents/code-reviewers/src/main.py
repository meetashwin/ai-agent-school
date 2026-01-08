import sys, os
from crew import CodeReviewCrew

code_changes = ""

# Get the absolute path of the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the file name relative to the script's directory
relative_file_path = "test/code_changes.txt"

# Construct the full absolute path
absolute_path = os.path.join(script_dir, relative_file_path)

with open(absolute_path, 'r') as file:
    code_changes = file.read()

def run():
    inputs = {
        "code_changes": code_changes,
    }
    return CodeReviewCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "code_changes": code_changes,
    }
    try:
        CodeReviewCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
    
if __name__ == "__main__":
    print("## Welcome to Code Review Crew")
    print('-------------------------------')
    result = run()
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")
    print(result)