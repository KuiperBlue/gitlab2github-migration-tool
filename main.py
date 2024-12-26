import shutil
from locale import normalize
from time import sleep
from git import Repo
from github import Github
import github
import gitlab
import configparser
import os
import stat

def fetch_projects_from_group(group):
    """

    :param group: gitlab group
    :return: list of projects
    """
    projects = []
    group_projects = group.projects.list(all=True)
    projects.extend(group_projects)
    return projects

def flatten(arr):
    """
    same function as numpy flatten
    :param arr: list object
    :return: flattened list
    """
    return [item for sublist in arr for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]

def normalize_name(repo_name):
    """
    replaces spaces and umlauts with "-"
    :param repo_name: original repository name as a string
    :return: name string
    """
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

def check_repository_exists(name, gh):
    try:
        repo_to_verify = gh.get_user().get_repo(name)
        return True
    except github.GithubException as e:
        return False

def handle_deletion(path):
    """
    deletes everything except the root
    :param path: root directory path
    :return:
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root,name)
            os.chmod(file_path, stat.S_IWRITE)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root,name)
            os.chmod(dir_path, stat.S_IWRITE)
            os.rmdir(dir_path)


def migrate_repository(project, name, gh):
    """
    clones gitlab repository into temporary folder, then creates equivalent github repository and pushes to github origin. Deletes local cloned repo upon completion.

    :param project: gitlab repo object
    :param name: normalized gitlab repo name
    :param gh: github object
    :return: none
    """
    try:
        sleep(2)
        print("Cloning repo ...")
        gitlab_repository = Repo.clone_from(project.http_url_to_repo, ".")
        while(len(os.listdir(tmp_path)) == 0):
            sleep(2)
        print(len(os.listdir(tmp_path)))
        sleep(2)
        print("Migrating repo ...")

        if project.description:
            description = ''.join(ch for ch in project.description if ch.isprintable()),
        else:
            description = ""

        github_repo = gh.get_user().create_repo(
            name = name,
            description = description,
            private = (project.visibility != "public")
        )

        print("Pushing repo ...")
        origin = gitlab_repository.remotes.origin
        origin.set_url(github_repo.clone_url.replace("https://", f"https://{GITHUB_TOKEN}@"))
        origin.push(all=True)
        while(True):
            try:
                github_repo = gh.get_user().get_repo(name)
                print("Push successful ...")
                break
            except github.GithubException as e:
                sleep(2)

        print("Handling deletion of repo files ...")
        while(True):
            try:
                handle_deletion(tmp_path)
                print("Deletion successful ...")
                break
            except:
                sleep(2)
    except Exception as e:
        print(e)
    finally:
        if len(os.listdir(tmp_path)) != 0:
            handle_deletion(tmp_path)
    return

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

# create directory (if not already created) or clean it
dir_path = "E:\\PycharmProjects\\pythonProject"
tmp_path = dir_path + "\\tmp"
if not os.path.isdir(tmp_path):
    os.mkdir(tmp_path)
if len(os.listdir(tmp_path)) != 0:
    print("deleting")
    handle_deletion(tmp_path)
    os.mkdir(tmp_path)
os.chdir(tmp_path)

projects = fetch_projects(exclude)
for project in projects:
    name = normalize_name(project.name)
    if check_repository_exists(name, gh) != True:
        migrate_repository(project, name, gh)