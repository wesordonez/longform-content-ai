from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import SerperDevTool, WebScraperTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
import os
import json
from datetime import datetime


@CrewBase
class WebContentCreationCrew():
    """Web Content Creation crew for generating blog posts, LinkedIn content, and newsletters"""
    agents: List[BaseAgent]
    tasks: List[Task]
    
    @before_kickoff
    def before_kickoff_function(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare the environment before starting the content creation process.
        - Creates output directory if it doesn't exist
        - Logs the start of the process
        - Enhances the inputs with additional metadata
        """
        print(f"🚀 Starting content creation process for topic: {inputs.get('topic', 'Unknown')}")
        print(f"⏱️ Process started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Enhance inputs with additional metadata
        enhanced_inputs = inputs.copy()
        enhanced_inputs["timestamp"] = datetime.now().isoformat()
        enhanced_inputs["content_id"] = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save inputs for reference
        with open(f"output/content_request_{enhanced_inputs['content_id']}.json", "w") as f:
            json.dump(enhanced_inputs, f, indent=4)
            
        print(f"✅ Environment prepared. Content ID: {enhanced_inputs['content_id']}")
        return enhanced_inputs

    @after_kickoff
    def after_kickoff_function(self, result: Any) -> Any:
        """
        Post-process the results after the content creation is complete.
        - Organizes final output files
        - Generates a summary report
        - Logs completion
        """
        print(f"🏁 Content creation process completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Extract the content ID from the final result if available
        content_id = "unknown"
        if hasattr(result, "get") and callable(result.get):
            if "content_id" in result:
                content_id = result.get("content_id")
        
        # Create a summary of all generated files
        summary = {
            "completion_time": datetime.now().isoformat(),
            "content_id": content_id,
            "generated_files": []
        }
        
        # List all generated files in the output directory
        for filename in os.listdir("output"):
            file_path = os.path.join("output", filename)
            if os.path.isfile(file_path):
                file_info = {
                    "filename": filename,
                    "size_bytes": os.path.getsize(file_path),
                    "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                }
                summary["generated_files"].append(file_info)
        
        # Save summary report
        with open(f"output/content_summary_{content_id}.json", "w") as f:
            json.dump(summary, f, indent=4)
            
        print(f"✅ Generated {len(summary['generated_files'])} content files:")
        for file_info in summary["generated_files"]:
            print(f"  - {file_info['filename']}")
        
        print("\n📋 Content creation summary saved to:")
        print(f"  output/content_summary_{content_id}.json")
        
        return result


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