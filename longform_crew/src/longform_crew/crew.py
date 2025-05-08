from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebScraperTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class WebContentCreationCrew():
    """Web Content Creation crew for generating blog posts, LinkedIn content, and newsletters"""
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def content_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['content_manager'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool(), WebScraperTool()]  # Use both Serper for search and WebScraper for detailed content
        )

    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_writer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def linkedin_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_writer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def newsletter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['newsletter_writer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],  # type: ignore[index]
            verbose=True
        )

    @task
    def content_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_planning_task'],  # type: ignore[index]
            output_file='output/content_plan.md'
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],  # type: ignore[index]
            output_file='output/research_brief.md'
        )

    @task
    def blog_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_writing_task'],  # type: ignore[index]
            output_file='output/blog_post.md'
        )

    @task
    def linkedin_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['linkedin_writing_task'],  # type: ignore[index]
            output_file='output/linkedin_post.md'
        )

    @task
    def newsletter_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['newsletter_writing_task'],  # type: ignore[index]
            output_file='output/newsletter_content.md'
        )

    @task
    def blog_editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_editing_task'],  # type: ignore[index]
            output_file='output/blog_post_final.md'
        )

    @task
    def linkedin_editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['linkedin_editing_task'],  # type: ignore[index]
            output_file='output/linkedin_post_final.md'
        )

    @task
    def newsletter_editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['newsletter_editing_task'],  # type: ignore[index]
            output_file='output/newsletter_content_final.md'
        )

    @task
    def final_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_review_task'],  # type: ignore[index]
            output_file='output/final_review.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Web Content Creation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,  # We want the tasks to be executed in sequence
            verbose=True,
        )