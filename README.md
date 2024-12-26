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
Before running the script, create a secret.config file with the following structure:
```
[gitlab]
url = <your_gitlab_url>
token = <your_gitlab_token>

[github]
token = <your_github_token>
```
This was written on a Windows system. OS commands may need adjustment for other platforms.
### NOTE: EXCLUDE
The script has an exclude list for gitlab groups hardcoded into it. You can pick and choose which groups to include/exclude by adding/removing their names to this list. This was a crude fix to save time.


# Usage
- Set up the configuration file with your GitLab and GitHub credentials.
- Run the script. The tool will migrate all repositories from GitLab (excluding specified groups) to GitHub.
```
python migrate_repositories.py
```
