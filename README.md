# GitLab to GitHub Repository Migration Tool
This Python script automates the migration of repositories from GitLab to GitHub. It uses the GitHub API and GitLab API to fetch repositories from a specified GitLab group, clones them locally, and pushes them to GitHub. The tool also handles the cleaning up of temporary files after migration.

# Reason for Creation
This tool was created to automate the migration of repositories from a GitLab instance to GitHub after the expiration of access to my university GitLab repositories.

# Features
- Fetch GitLab repositories from a group
- Normalize repository names (handling spaces and German umlauts)
- Clone GitLab repositories locally
- Create equivalent repositories on GitHub
- Push cloned repositories to GitHub
- Clean up temporary files post-migration

# Requirements
- Python 3.x
- gitpython library (pip install gitpython)
- github library (pip install PyGithub)
- python-gitlab library (pip install python-gitlab)

# Configuration
In a `secret.config` file (create it before running the script), write down the following:
```
[gitlab]
url = <your_gitlab_url>
token = <your_gitlab_token>

[github]
token = <your_github_token>
```
To generate your tokens go to your github settings -> developer settings and generate a classic token. Make sure to include repo admin permissions. Do the same process in your gitlab account.

Further, the script was written to be native to Windows systems. Some lines may need adjusting for other OS, though the code was kept as OS-agnostic as possible.

### NOTE: EXCLUDE
The script has an exclude list ([line 172](https://github.com/KuiperBlue/gitlab2github-migration-tool/blob/0913379e6e78e35750a2cb02fc08d20648ecb2d3/main.py#L172))for gitlab groups hardcoded into it. You should change this list depending on your own groups. Include/exclude them during the migration process by adding/removing their names to this list. This was a crude fix to save time.

# Usage
- Set up the configuration file with your GitLab and GitHub credentials.
- Run the script. The tool will migrate all repositories from GitLab (excluding specified groups) to GitHub.
```
python migrate_repositories.py
```
