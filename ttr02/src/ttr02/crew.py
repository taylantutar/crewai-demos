from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class Ttr02():
    """Ttr02 crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            output_file='wikipost.txt'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Ttr02 crew"""

            # Create tools
        search_tool = SerperDevTool()
        
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            tools=[search_tool],
            process=Process.sequential,
            verbose=True,
        )
