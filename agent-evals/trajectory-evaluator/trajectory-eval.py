"""
Filename: trajectory-eval.py
Author: Ashwin
Created: 2026-01-13
Description: Demonstration of various trajectory evaluations with sample agent output 
            and reference test data
"""

import reference_outputs

import json
from agentevals.trajectory.match import create_trajectory_match_evaluator

## Trajectory Evaluator - Strict

## "strict" is useful is if you want to ensure that tools are always 
## called in the same order for a given query (e.g. a company policy lookup tool before a tool that requests vacation time for an employee).

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
##   Creating a Sample Agent output which is a JSON that will be evaluated against a
##   reference output using "strict" evaluation mode

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
##   Creating a Sample Agent output which is a JSON that will be evaluated against a
##   reference output using "unordered" evaluation mode

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
print("________________________________________")
print(f"Agent Output: {output_unordered}\n")
print(f"Reference Output: {reference_outputs.reference_output_unordered}\n")
print(f"Evaluator Result: {trajectory_evaluator(output_unordered, reference_outputs.reference_output_unordered, "unordered")}\n")
