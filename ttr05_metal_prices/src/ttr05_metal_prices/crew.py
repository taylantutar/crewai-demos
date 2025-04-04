from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool

# Import custom tool
from ttr05_metal_prices.tools import file_write_tool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Ttr05MetalPrices():
    """Ttr05MetalPrices crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Instantiate tools
    scrape_tool = ScrapeWebsiteTool()
    # file_write_tool is already instantiated in tools/__init__.py

    @agent
    def web_scraper_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scraper_agent'],
            tools=[self.scrape_tool],
            verbose=True
        )

    @agent
    def data_extractor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_extractor_agent'],
            verbose=True
            # No specific tool needed here, relies on LLM capabilities and context
        )

    @agent
    def report_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer_agent'],
            tools=[file_write_tool], # Use the imported instance
            verbose=True
        )

    @task
    def scrape_websites_task(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_websites'],
            agent=self.web_scraper_agent(),
            async_execution=True # Match YAML config
        )

    @task
    def extract_prices_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_prices'],
            agent=self.data_extractor_agent(),
            context=[self.scrape_websites_task()] # Depends on scrape_websites output
        )

    @task
    def write_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_report'],
            agent=self.report_writer_agent(),
            context=[self.extract_prices_task()] # Depends on extract_prices output
            # output_file is handled by the tool based on input variable
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Ttr05MetalPrices crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential, # Tasks will run sequentially
            verbose=True,
        )
