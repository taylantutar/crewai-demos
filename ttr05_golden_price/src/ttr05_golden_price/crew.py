from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# Import necessary tools, e.g., from crewai_tools
from crewai_tools import ScrapeWebsiteTool # <-- Uncomment this line

# If using tools, initialize them here
scrape_tool = ScrapeWebsiteTool() # <-- Instantiate the tool

@CrewBase
class Ttr05GoldenPrice():
    """Ttr05GoldenPrice crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def gold_scraper(self) -> Agent: # <-- Metot adı 'gold_scraper'
        return Agent(
            config=self.agents_config['gold_scraper_agent'],
            tools=[scrape_tool], # <-- Add the tool to the agent
            verbose=True
        )

    @agent
    def report_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['report_formatter_agent'],
            verbose=True
        )

    @task
    def scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_gold_price_task'],
            agent=self.gold_scraper()
            # Add context=[list_of_other_tasks] if this task depends on others
        )

    @task
    def format_task(self) -> Task:
        return Task(
            config=self.tasks_config['format_report_task'],
            agent=self.report_formatter(),
            context=[self.scrape_task()], # Make this task depend on the scrape_task
            output_file='gold_prices_report.md' # Ensure output file is set
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Ttr05GoldenPrice crew"""
        return Crew(
            agents=self.agents, # Should include gold_scraper and report_formatter
            tasks=self.tasks,   # Should include scrape_task and format_task
            process=Process.sequential,
            verbose=True,
        )
