from difflib import context_diff
from pickle import FALSE
from mcp.server.fastmcp import FastMCP
from typing import Any,Optional
from mcp.client.streamable_http import streamablehttp_client
import git 
from pydantic import BaseModel,Field


app = FastMCP("github_agent",stateless_http = False)

DEFAULT_CONTEXT_LINES = 3

class GitStatus(BaseModel):
    repo_path:str

class GitDiffUnstagged(BaseModel):
    repo_path:str
    context_lines:int = DEFAULT_CONTEXT_LINES

class GitDiffStagged(BaseModel):
    repo_path:str
    context_lines:int = DEFAULT_CONTEXT_LINES

class GitCommit(BaseModel):
    repo_path:str
    message:str

class GitDiff(BaseModel):
    repo_path:str
    context_lines:int = DEFAULT_CONTEXT_LINES
    target:str



@app.tool()
async def git_status(repo_path:str):
    """This tool get the status of repo
        Args:
            repo_path: path of the repo . path should be from local machine via clonned repository"""
    repo = git.Repo(repo_path)
    content = repo.git.status()
    return {"message":content}

@app.tool(description = "Shows the differences between the working directory and the index (unstaged changes) in a unified diff format with the specified number of context lines.")
async def git_diff_unstagged(repo_path:str,context_lines:int = DEFAULT_CONTEXT_LINES) -> str:
    repo = git.Repo(repo_path)
    return repo.git.diff(f"--unified--={context_lines}")

@app.tool(description="Shows staged changes in a unified diff format with the specified number of context lines.")
async def git_diff_stagged(repo_path: str, context_lines: int = DEFAULT_CONTEXT_LINES) -> str:
    repo = git.Repo(repo_path)
    return repo.git.diff(f"--unified={context_lines}", "--cached")


@app.tool()
async def git_commit(repo_path:str,message:str) -> str:
    repo = git.Repo(repo_path)
    commit = repo.index.commit(message)
    return f"Changes successfully commited to repo with hash {commit.hexsha}"

@app.tool()
async def git_diff(repo_path:str, target:str, context_lines:int = DEFAULT_CONTEXT_LINES):
    repo = git.Repo(repo_path)
    return repo.git.diff(f"--unified={context_lines}",target)

@app.tool()
async def git_add(repo_path:str,files:list[str])-> str:
    repo = git.Repo(repo_path)
    repo.index.add(files)
    return "files stagged successfully"

@app.tool()
async def git_reset(repo_path:str) -> str:
    repo = git.Repo(repo_path)
    repo.index.reset()
    return f"All changes are reset"

@app.tool()
async def git_log(repo_path:str,max_count:int = 10) -> list[str]:
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits(max_count = max_count))
    log = []

    for commit in commits:
        log.append(
        f"Commit: {commit.hexsha!r}\n"
        f"Author: {commit.author!r}\n"
        f"Date: {commit.authored_datetime!r}\n"
        f"Message: {commit.message!r}\n"
        )
    return log


@app.tool()
async def git_checkout(repo_path :str, branch_name: str) -> str:
    repo = git.Repo(repo_path)
    repo.git.checkout(branch_name)
    return f"Switched to branch '{branch_name}'"

@app.tool()
async def git_push(repo_path: str, remote_name: str = "origin", branch_name: str = "main") -> str:
    """
    Pushes committed changes to the remote repository.

    Args:
        repo_path: Path of the repo (must be a cloned local repository).
        remote_name: The name of the remote (default: origin).
        branch_name: The branch to push (default: main).
    """
    try:
        repo = git.Repo(repo_path)

        # Ensure the remote exists
        if remote_name not in [r.name for r in repo.remotes]:
            return f"Remote '{remote_name}' not found in repo."

        remote = repo.remote(remote_name)
        push_result = remote.push(branch_name)

        # Collect push results
        messages = []
        for res in push_result:
            if res.flags & res.ERROR:
                messages.append(f"❌ Push failed: {res.summary}")
            else:
                messages.append(f"✅ Push successful: {res.summary}")

        return "\n".join(messages) if messages else "Push executed, no messages returned."

    except Exception as e:
        return f"⚠️ Error while pushing: {str(e)}"

@app.tool()
async def git_pull(repo_path: str, remote_name: str = "origin", branch_name: str = "main") -> str:
    """
    Pulls the latest changes from the remote repository.
    Useful before pushing to avoid conflicts.
    """
    try:
        repo = git.Repo(repo_path)

        if remote_name not in [r.name for r in repo.remotes]:
            return f"Remote '{remote_name}' not found."

        remote = repo.remote(remote_name)
        pull_result = remote.pull(branch_name)

        messages = [f"✅ Pulled: {res}" for res in pull_result]
        return "\n".join(messages) if messages else f"No changes fetched from {remote_name}/{branch_name}."

    except Exception as e:
        return f"⚠️ Error while pulling: {str(e)}"



github_app = app.streamable_http_app()