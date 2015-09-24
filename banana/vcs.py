from datetime import datetime
from os import path
import git


def repo_info():
    """
    returns: (branch_name, last commit time, last commit message)
    """
    banana_root = path.join(path.dirname(path.realpath(__file__)), '..')
    repo = git.Repo(banana_root)
    commit = repo.rev_parse('HEAD')
    lastlog = commit.summary
    description = repo.git.describe('--tags')
    hexsha, branch = commit.name_rev.split()
    timestamp = datetime.fromtimestamp(commit.committed_date)

    return {
        'branch': branch,
        'hexsha': hexsha,
        'timestamp': timestamp,
        'summary': lastlog,
        'description': description,
    }
