"""
Filename: reference_outputs.py
Author: Ashwin
Created: 2026-01-13
Description: Constants file for various reference outputs for evaluation.  Consider 
            this as a unit test data for the agent evals
"""

import json

reference_output_strict = [
    {"role": "user", "content": "What is the weather in San Francisco?"},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "function": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "San Francisco"}),
                }
            }
        ],
    },
    {"role": "tool", "content": "It's 80 degrees and sunny in San Francisco."},
    {"role": "assistant", "content": "The weather in SF is 80˚ and sunny."},
]

reference_output_unordered = [
    {"role": "user", "content": "What is the weather in SF and is there anything fun happening?"},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "function": {
                    "name": "get_fun_activities",
                    "arguments": json.dumps({"city": "San Francisco"}),
                }
            },
            {
                "function": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "San Francisco"}),
                }
            },
        ],
    },
    {"role": "tool", "content": "Nothing fun is happening, you should stay indoors and read!"},
    {"role": "tool", "content": "It's 80 degrees and sunny in SF."},
    {"role": "assistant", "content": "In SF, it's 80˚ and sunny, but there is nothing fun happening."},
]