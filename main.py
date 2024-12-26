from locale import normalize

from github import Github
import github
import gitlab
import configparser
import os

def fetch_projects_from_group(group):
    projects = []
    group_projects = group.projects.list(all=True)
    projects.extend(group_projects)
    return projects

def flatten(arr):
    return [item for sublist in arr for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]

def normalize_name(repo_name):
    # Mapping of German umlauts to their ASCII equivalents
    umlaut_mapping = {
        'ä': '-',
        'ö': '-',
        'ü': '-',
        'Ä': '-',
        'Ö': '-',
        'Ü': '-',
        'ß': '-'
    }
    if repo_name:
        for umlaut, replacement in umlaut_mapping.items():
            repo_name = repo_name.replace(umlaut, replacement)

        repo_name = repo_name.replace(' ', '-')

    return repo_name

def fetch_projects(exclude):
    """
    Fetches repos by id from groups associated with gitlab object.
    :param exclude: list of groups (by name string) to exclude from project fetch
    :return: list of gitlab projects
    """
    result = []
    keep_groups = []

    groups = gl.groups.list(all=True)

    for group in groups:
        if group.name not in exclude:
            keep_groups.append(group)

    projects = []
    for group in keep_groups:
        projects.append(fetch_projects_from_group(group))
    projects = flatten(projects)


    for project in projects:
        gl_project = gl.projects.get(project.id)
        result.append(gl_project)
    return result

def check_repository_exists(gitlab_repository, gh):
    try:
        repo_to_verify = gh.get_user().get_repo(normalize(gitlab_repository.name))
        print(f"{repo_to_verify.name} does not exist")
        return True
    except github.GithubException as e:
        print(e)
        print(f"{gitlab_repository.name} already exists")
        return False


config = configparser.ConfigParser()
config.read("secret.config")

# Configuration from environment variables
GITLAB_URL = config['gitlab']['url']
GITLAB_TOKEN = config['gitlab']['token']
GITHUB_TOKEN = config['github']['token']

gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
gh = Github(GITHUB_TOKEN)

exclude = ["PE1-SE1 Wintersemester 2023-24", "PE2 Sommersemester (Gref)", "PE2 Vorlesung Code", "Projects",
               "CodingSpace", "Zusatzaufgaben", "Vorlesung",
               "Übung", "WEB", "1. Semester", "Projekte", "Übung SS2025"]

projects = fetch_projects(exclude)

for project in projects:
    if check_repository_exists(project, gh):
        print(f"Project {project.name} already exists")
