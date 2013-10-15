from datetime import datetime
import git


def repo_info():
    """
    returns: (branch_name, last commit time, last commit message)
    """
    repo = git.Repo(__file__)
    commit = repo.rev_parse('HEAD')
    lastlog = commit.summary
    hexsha, branch = commit.name_rev.split()
    timestamp = datetime.fromtimestamp(commit.committed_date)

    return {
        'branch': branch,
        'hexsha': hexsha,
        'timestamp': timestamp,
        'summary': lastlog,
    }
