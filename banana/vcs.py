from datetime import datetime
import time
import git


def repo_info():
    """
    returns: (branch_name, last commit time, last commit message)
    """
    repo = git.Repo(__file__)
    last_commit = repo.commits()[0]
    branch = repo.active_branch
    lastlog = last_commit.summary
    timestamp = datetime.fromtimestamp(time.mktime(last_commit.committed_date))
    hexsha = last_commit.id

    return {
        'branch': branch,
        'hexsha': hexsha,
        'timestamp': timestamp,
        'summary': lastlog,
    }
