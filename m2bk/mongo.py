# -*- coding: utf-8 -*-

"""
m2bk.mongo
~~~~~~~~~~~~~~

Database backups via mongodump

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""


from . import log, utils, fs, shell
from .const import PKG_NAME

#
# Constants
#
MONGODB_DEFAULT_MONGODUMP = "mongodump"
MONGODB_DEFAULT_USER = PKG_NAME
MONGODB_DEFAULT_PWD = "pass"
MONGODB_DEFAULT_PORT = 27017
MONGODB_DEFAULT_AUTH = "admin"


def _set_mongodb_host_val(key, default, mongodb_host, mongodb_defaults):
    """
    Set a value in a 'cascade' fashion for mongodb_host[key]

    Within 'mongodb', as a last resort, its hardcoded default value is going to
    be picked.

    :param key: key name
    :param default: default last resort value
    :param mongodb_host: mongodb 'host' entry
    :param mongodb_defaults: mongodb 'defaults' dict
    """
    # If mongodb_host[key] is not already set, its value is going to be picked
    # from mongodb_defaults[key]
    if key not in mongodb_host:
        if key in mongodb_defaults:
            mongodb_host[key] = mongodb_defaults[key]
        else:
            # BUT, if also mongodb_defaults[key] doesn't exist
            # the value picked is going to be 'default' as last resort
            mongodb_host[key] = default
        if key != 'user_name' and key != 'password':
            log.msg_debug("Setting default '{key}'='{value}' "
                          .format(key=key, value=mongodb_host[key]))


def _merge_dbs(default_dbs, host_dbs):
    return list(set(default_dbs + host_dbs))


def make_backup_files(*,
                      mongodump=MONGODB_DEFAULT_MONGODUMP,
                      hosts={},
                      host_defaults={},
                      dry_run=False,
                      **kwargs):
    """
    Backup all specified databases into a gzipped tarball via mongodump

    :param mongodump(str, optional): Path to mongodump executable
    :param hosts(dict, optional): A dict containing hosts info to be backed up
    :param host_defaults(dict, optional): Default values applied to each host
    :param dry_run(bool, optional): Whether to activate dry run mode
    :param \*\*kwargs: arbitrary keyword arguments
    :raises TypeError: if an argument in kwargs does not have the type expected
    :raises ValueError: if an argument within kwargs has an invalid value
    """

    # Output directory
    output_dir = fs.get_output_dir()

    # Type checks
    utils.chkstr(mongodump, 'mongodump')

    # List of mongodb hosts holding databases
    mongodb_hosts = hosts
    if len(mongodb_hosts) == 0:
        raise ValueError("No mongodb 'hosts' specified!")

    # Default values applied to each host if necessary,
    # this setting takes effect on a 'cascade' fashion.
    mongodb_defaults = host_defaults

    # Collected list of files generated by _make_backup_file
    mongodump_files = {}

    # Backup cycle for each mongodb host
    for mongodb_host_name, mongodb_host in mongodb_hosts.items():

        if type(mongodb_host) != dict:
            raise TypeError("mongodb_host '{name}' must be dict"
                            .format(name=mongodb_host_name))

        # For each host, its 'address' is essential
        if 'address' not in mongodb_host:
            raise KeyError("No 'address' specified!")
        utils.chkstr(mongodb_host['address'], 'address')

        """
        For these keys, the value is going to be set in
        in a 'cascade' fashion, if the value is not already set,
        its value is going to be picked from the 'defaults'(mongodb_defaults)
        sub-section within 'mongodb', as a last resort, its hardcoded default
        value is going to be picked.
        """
        # TODO: there has to be something better than this
        _set_mongodb_host_val('user_name', MONGODB_DEFAULT_USER,
                              mongodb_host, mongodb_defaults)
        _set_mongodb_host_val('password', MONGODB_DEFAULT_PWD,
                              mongodb_host, mongodb_defaults)
        _set_mongodb_host_val('port', MONGODB_DEFAULT_PORT,
                              mongodb_host, mongodb_defaults)
        _set_mongodb_host_val('auth_db', MONGODB_DEFAULT_AUTH,
                              mongodb_host, mongodb_defaults)

        """Merge dbs list with that of the host_defaults section (if any)"""
        if 'dbs' in mongodb_defaults:
            if 'dbs' in mongodb_host:
                mongodb_host['dbs'] = _merge_dbs(mongodb_defaults['dbs'],
                                                 mongodb_host['dbs'])
            else:
                mongodb_host['dbs'] = mongodb_defaults['dbs']

        # Add the file name to the list to be returned
        mongodump_files[mongodb_host_name] = _make_backup_file(dry_run=dry_run, mongodump=mongodump,
                                                               output_dir=output_dir, name=mongodb_host_name,
                                                               **mongodb_host)
    # .. and finally, give it
    return mongodump_files


def _log_make_backup_file_settings(mongodb_host):
    host_copy = mongodb_host.copy()
    del host_copy['password']
    log.msg_debug("mongodb host '{name}': {host}"
                  .format(name=host_copy['name'], host=host_copy))


def _make_backup_file(**kwargs):
    # log settings
    _log_make_backup_file_settings(kwargs)

    # Path to the mongodump executable
    mongodump = kwargs.get('mongodump')

    # Host and port
    address = kwargs.get('address')
    port = kwargs.get('port')
    # The user and password for connecting to the databases
    user = kwargs.get('user_name')
    passwd = kwargs.get('password')
    # databases
    dbs = kwargs.get('dbs', [])
    # dry run
    dry_run = kwargs.get('dry_run')
    # name
    name = kwargs.get('name')
    # auth_db
    auth_db = kwargs.get('auth_db')

    # Type checks
    utils.chkstr(name, 'name')
    utils.chkstr(address, 'address')
    utils.chkstr(user, 'user_name')
    utils.chkstr(passwd, 'password')
    utils.chkstr(auth_db, 'auth_db')

    # Check port
    if type(port) != int:
        raise TypeError('port must be int')
    # check valid range in port
    if port < 1 or port > 65535:
        raise ValueError('port must be between 1 and 65535')

    # Check dbs
    if type(dbs) != list or len(dbs) == 0:
        raise ValueError('dbs must at least one value')
    for db in dbs:
        if type(db) != str:
            raise TypeError('all values within dbs must be str')

    # The mongodump directory is going to have a name indicating
    # the UNIX timestamp corresponding to the current creation time
    out_dir = fs.make_tmp_dir("mongodump-{name}".format(name=name))

    # For each database specified, run mongodump on it
    for db in dbs:
        _mongodump_exec(mongodump, address, port, user, passwd, db,
                        out_dir, auth_db, dry_run)
    # After all has been done, make a gzipped tarball from it
    return fs.make_tarball(out_dir)


def _mongodump_exec(mongodump, address, port, user, passwd, db,
                    out_dir, auth_db, dry_run):
    """
    Run mongodump on a database

    :param address: server host name or IP address
    :param port: server port
    :param user: user name
    :param passwd: password
    :param db: database name
    :param out_dir: output directory
    :param auth_db: authentication database
    :param dry_run: dry run mode
    :raises OSError: if mongodump process returns error
    """

    # Log the call
    log.msg("mongodump [{mongodump}] db={db} auth_db={auth_db}" +
            " mongodb://{user}@{host}:{port} > {output}"
            .format(mongodump=mongodump, user=user, host=address,
                    port=port, db=db, auth_db=auth_db, output=out_dir))

    # Prepare the call
    args = "--host {host}:{port} -d {db} -u {user} -p {passwd} " \
           "--authenticationDatabase {auth_db} -o {output}"\
           .format(host=address, port=port, db=db, user=user, passwd=passwd,
                   auth_db=auth_db, output=out_dir)

    if not dry_run:
        # Make the actual call to mongodump
        shell.run(mongodump, args=args)
