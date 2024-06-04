import logging
import os

from git import Repo

import app_config as config


def create_or_update_repos(no_update: bool = False):
    if not os.path.exists(config.WORKDIR_PATH):
        os.mkdir(config.WORKDIR_PATH)

    repos = []

    for repo_entity in config.REPOS:
        repo_url = repo_entity["url"]
        repo_name = repo_url.split('/')[-1]
        repo_path = str(os.path.join(config.WORKDIR_PATH, repo_name))
        logging.debug(f"Creating/Updating content for repo {repo_name}")
        repo: Repo = None
        if not os.path.exists(repo_path):
            repo = Repo.clone_from(repo_url, repo_path)
            logging.info(f"Cloned repo {repo_url} to {repo_path}")
        else:
            repo = Repo(repo_path)
            logging.info(f"Loaded existing repo {repo_url}")
            if not no_update:
                repo.git.reset('--hard')
                repo.remotes.origin.pull()
                logging.info(f"Pulled changes for repo {repo_url}")
        repos.append({"url": repo_url, "name": repo_name, "path": repo_path})

    return repos
