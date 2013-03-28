import monetdb.control


status_map = {
    1: 'running',
    2: '?',
    3: 'under maintenance',
}


def monetdb_list(host, port, passphrase):
    """
    returns a list of MonetDB databases
    """
    monetdb_control = monetdb.control.Control(host, port, passphrase)
    statuses = monetdb_control.status()

    for status in statuses:
        status['status'] = status_map[status['state']]

    return statuses

