import git
import datetime


def repo_info():
    """
    returns: (branch_name, last commit time, last commit message)
    """
    repo = git.Repo(__file__)
    branch = repo.active_branch
    lastlog = branch.log()[0]
    timestamp = datetime.datetime.fromtimestamp(lastlog.time[0])
    return {
        'branch_name': branch.name,
        'log_timestamp': timestamp,
        'log_message': lastlog.message,
    }
