import os
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model='gpt-4o-mini') #Loading GPT4o mini

@CrewBase
class CodeReviewCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def senior_developer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_developer'],
            verbose=True,
            llm=llm
        )
    
    @task
    def analyze_code_quality(self) -> Task: 
        return Task(
            config=self.tasks_config['analyze_code_quality'],
            agent=self.senior_developer_agent(),
        )

    @agent
    def security_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['security_engineer'],
            verbose=True,
            llm=llm,
            tools=[
                SerperDevTool(search_url="https://owasp.org", base_url=os.getenv("DLAI_SERPER_BASE_URL")),
                ScrapeWebsiteTool(),
            ]
        )
    
    @task
    def review_security(self) -> Task: 
        return Task(
            config=self.tasks_config['review_security'],
            agent=self.security_engineer_agent(),
        )

    @agent
    def tech_lead_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['tech_lead'],
            verbose=True,
            llm=llm
        )
    
    @task
    def make_review_decision(self) -> Task: 
        return Task(
            config=self.tasks_config['make_review_decision'],
            agent=self.tech_lead_agent(),
        )
    @crew
    def crew(self) -> Crew:
        """Performs the code review process using multiple agents and tasks."""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )            