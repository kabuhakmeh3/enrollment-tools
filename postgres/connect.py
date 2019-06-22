## this is a module to connect to postgres db instance ##
import os, json

path_to_auth = '/home/ubuntu/.postgres/login'

permission = {'full-access':'administrator.json',
              'read-only':'ec2read.json'}

def load_credentials(access='read-only', path=path_to_auth):
    ''' Load a file containing login credentials for database
    '''
    
    permissions = {'full-access':'administrator.json',
                   'read-only':'ec2read.json'}
    
    with open(os.path.join(path_to_auth, permissions[access])) as f:
        user = json.load(f)
        return user

def auth_db(credentials=load_credentials()):
    ''' Build a string to authenticate into database
    '''
    user = credentials['username']
    pswd = credentials['password']
    hostname = credentials['host']
    portnum = credentials['port']
    dbname = credentials['database']

    db_string = user+':'+pswd+'@'+hostname+':'+portnum+'/'+dbname
    return 'postgresql://' + db_string
