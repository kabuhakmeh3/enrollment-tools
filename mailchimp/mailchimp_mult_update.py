import os, pickle
from mailchimp3 import MailChimp

# update multiple lists - old way of doing things

def load_key(path, key):
    with open(os.path.join(path, key)) as f:
        return f.read().strip()

def load_pickle(pickle_file):
    with open(pickle_file, 'rb') as handle:
        return pickle.load(handle)

def member_json(subscriber):
    
    try:
        f_name, l_name, email = subscriber.split(',')
    except:
        member_as_list = subscriber.split(',')
        f_name = member_as_list[0]
        l_name = member_as_list[1]
        email = member_as_list[-1]
    
    member_json = {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': f_name,
            'LNAME': l_name,
            },
        }

    return member_json

def add_to_mailchimp(file_to_add, list_id, mc_client):
    with open(file_to_add) as f:
        for line in f:
            if line.startswith('FirstName'):
                pass
            else:
                clean_line = line.strip()
                member_to_add = member_json(clean_line)
                # add to list
                try:
                    mc_client.lists.members.create(list_id, member_to_add)
                    print('Added', clean_line)
                except:
                    print('SKIPPED', clean_line)

def main():
    
    # set all paths
    path_to_apikey = '/home/ubuntu/.apikeys'
    apikey_file = 'mailchimp-list.api'
    mc_user_file = 'mailchimp-user'
    path_to_lists = '/home/ubuntu/path/to/mailing-lists/updates'
    path_to_id_dict = '/home/ubuntu/.apikeys/list_ids.pickle'

    # load keys and data
    apikey = load_key(path_to_apikey, apikey_file)
    mailchimp_user = load_key(path_to_apikey, mc_user_file)
    lists_to_update = os.listdir(path_to_lists)
    list_id_dict = load_pickle(path_to_id_dict)
    
    # initialize mailchimp client
    client = MailChimp(mc_api=apikey, mc_user=mailchimp_user)
    
    # add all new members to mailchimp
    for listfile in lists_to_update:
        file_list_id = list_id_dict[listfile]
        list_to_add = os.path.join(path_to_lists, listfile)
        print('---> Starting List:', listfile)
        add_to_mailchimp(list_to_add, file_list_id, client)

if __name__ == '__main__':
    main()
