"""
Filename: trajectory-eval.py
Author: Ashwin
Created: 2026-01-13
Description: Demonstration of various trajectory evaluations - string, unordered, superset, subset
with sample agent output and reference test data
"""

import reference_outputs

import json
from agentevals.trajectory.match import create_trajectory_match_evaluator

def trajectory_evaluator(output, reference_output, match_mode="strict"):
    """
    Evaluates the passed output against a reference output using a strict evaluator

    Returns the evaluation result which is a JSON string
    """
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode=match_mode
    )

    result = evaluator(
        outputs=output, reference_outputs=reference_output
    )

    return result

## 1. Strict evaluation 
## The "strict" trajectory_match_mode compares two trajectories and 
## ensures that they contain the same messages in the same order with 
## the same tool calls

output_strict = [
    {"role": "user", "content": "What is the weather in SF?"},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "function": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "San Francisco"}),
                }
            },
            {
                "function": {
                    "name": "accuweather_forecast",
                    "arguments": json.dumps({"city": "San Francisco"}),
                }
            }
        ],
    },
    {"role": "tool", "content": "It's 80 degrees and sunny in SF."},
    {"role": "assistant", "content": "The weather in SF is 80 degrees and sunny."},
]

print("Trajectory Evaluator - Strict Match Mode")
print("________________________________________")
print(f"Agent Output: {output_strict}\n")
print(f"Reference Output: {reference_outputs.reference_output_strict}\n")
print(f"Evaluator Result: {trajectory_evaluator(output_strict, reference_outputs.reference_output_strict, "strict")}\n")

## 2. Unordered
##  The "unordered" trajectory_match_mode compares two trajectories 
##  and ensures that they contain the same tool calls in any order. 
##  This is useful if you want to allow flexibility in how an agent obtains 
##  the proper information, but still do care that all information was retrieved.

output_unordered = [
    {"role": "user", "content": "What is the weather in SF and is there anything fun happening?"},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [{
            "function": {
                "name": "get_weather",
                "arguments": json.dumps({"city": "San Francisco"}),
            }
        }],
    },
    {"role": "tool", "content": "It's 80 degrees and sunny in SF."},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [{
            "function": {
                "name": "get_fun_activities",
                "arguments": json.dumps({"city": "San Francisco"}),
            }
        }],
    },
    {"role": "tool", "content": "Nothing fun is happening, you should stay indoors and read!"},
    {"role": "assistant", "content": "The weather in SF is 80 degrees and sunny, but there is nothing fun happening."},
]

print("Trajectory Evaluator - Unordered Match Mode")
print("___________________________________________\n")
print(f"Agent Output: {output_unordered}\n")
print(f"Reference Output: {reference_outputs.reference_output_unordered}\n")
print(f"Evaluator Result: {trajectory_evaluator(output_unordered, reference_outputs.reference_output_unordered, "unordered")}\n")

## 3. Superset / Subset
##  The "subset" and "superset" modes match partial trajectories 
## (ensuring that a trajectory contains a subset/superset of tool calls 
## contained in a reference trajectory).

output_superset = [
    {"role": "user", "content": "What is the weather in SF and London?"},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [{
            "function": {
                "name": "get_weather",
                "arguments": json.dumps({"city": "SF and London"}),
            },
        }, {
            "function": {
                "name": "accuweather_forecast",
                "arguments": json.dumps({"city": "SF and London"}),
            }
        }],
    },
    {"role": "tool", "content": "It's 80 degrees and sunny in SF, and 90 degrees and rainy in London."},
    {"role": "tool", "content": "Unknown."},
    {"role": "assistant", "content": "The weather in SF is 80 degrees and sunny. In London, it's 90 degrees and rainy."},
]

print("Trajectory Evaluator - Superset/Subset Match Mode")
print("_________________________________________________\n")
print(f"Agent Output: {output_superset}\n")
print(f"Reference Output: {reference_outputs.reference_output_superset}\n")
print(f"Evaluator Result: {trajectory_evaluator(output_superset, reference_outputs.reference_output_superset, "superset")}\n")