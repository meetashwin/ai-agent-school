# Agent Evals

## What is Agent Evaluation?

Agent Evals (short for "agent evaluations") refers to systematic methods for testing and measuring the performance of AI agents—autonomous or semi-autonomous systems that can take actions, use tools, and work toward goals with varying degrees of independence.

## Common types of Evaluations

* **Assertions** - Comparing the outputs from agents to pre-defined baselines or ground truth.  Evaluation is based on the closeness of actual outputs with expected outputs
* **LLM-as-a-judge** - Use a different LLM to evaluate the agent outputs and score them based on specific criteria
* **Human Evaluations** - Classify or rank outputs manually by reviewing them and comparing against baseline

## Evaluation Frameworks

There are several open-source frameworks to perform Agent Evals.

I will use the [AgentEvals](https://github.com/langchain-ai/agentevals) framework by langchain to demonstrate various types of agent evaluations.

## Evaluators

### Agent Trajectory Evaluator

Agent trajectory match evaluators are used to judge the trajectory of an agent's execution either against an expected trajectory or using an LLM. 

These evaluators expect you to format your agent's trajectory as a list of OpenAI format dicts or as a list of LangChain BaseMessage classes, and handle message formatting under the hood.

* [**Trajectory Match Evaluator**](trajectory-evaluator)
  * AgentEvals offers the **create_trajectory_match_evaluator/createTrajectoryMatchEvaluator** and **create_async_trajectory_match_evaluator**
  * **Strict Match** - "strict" trajectory_match_mode compares two trajectories and ensures that they contain the same messages in the same order with the same tool calls
  * **Unordered Match** -  "unordered" trajectory_match_mode compares two trajectories and ensures that they contain the same tool calls in any order.
  * **Subset / Superset Match** - "subset" and "superset" modes match partial trajectories (ensuring that a trajectory contains a subset/superset of tool calls contained in a reference trajectory)
* [**Trajectory Match Evaluator with LLM-as-judge**](trajectory-evaluator-llm-judge)
  * The LLM-as-judge trajectory evaluator that uses an LLM to evaluate the trajectory. Unlike the trajectory match evaluators, it doesn't require a reference trajectory
* [**Graph Trajectory**](graph-evaluator)
  * For frameworks like LangGraph that model agents as graphs, it can be more convenient to represent trajectories in terms of nodes visited rather than messages. agentevals includes a category of evaluators called graph trajectory evaluators that are designed to work with this format
* [**Graph Trajectory with LLM-as-judge**](graph-evaluator-llm-judge)
  * This evaluator is similar to the trajectory_llm_as_judge evaluator, but it works with graph trajectories instead of message trajectories