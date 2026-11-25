import os
import time
from dotenv import load_dotenv
from github import Github
from src.sandbox.docker_manager import SandboxManager
from src.agent.graph import build_graph

load_dotenv()

def run(repo_name: str, issue_text: str):
    sb = SandboxManager()
    try:
        print("1. Starting isolated Docker sandbox...")
        sb.start("https://github.com/Chaitanyaurpadhyay/testbug.git", os.getenv("GITHUB_TOKEN"))
        _, files = sb.exec_command("find . -maxdepth 3 -name '*.py'")
        
        print("2. AI agent investigating and fixing the bug...")
        agent = build_graph(sb)
        res = agent.invoke({
            "issue": issue_text,
            "files": files,
            "retries": 0,
            "success": False
        })
        
        if res["success"]:
            branch = f"autofix-{int(time.time())}"
            sb.push_branch(branch, "fix: resolved issue autonomously")
            g = Github(os.getenv("GITHUB_TOKEN"))
            repo = g.get_repo(repo_name)
            pr = repo.create_pull(
                title="AI AutoFix: Resolved Issue",
                body=res["explanation"],
                head=branch,
                base=repo.default_branch
            )
            print("SUCCESS! Pull Request created at:", pr.html_url)
        else:
            print("FAILED to fix the bug. Logs:\n", res["logs"])
    finally:
        sb.cleanup()

if __name__ == "__main__":
    run("Chaitanyaurpadhyay/testbug", "divide function crashes when divided by zero")
