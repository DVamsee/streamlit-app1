import yaml

def is_admin(config, username):
    """
    Check if user is admin
    """
    return username in config['roles']['admin']

def is_staff(config, username):
    """
    Check if user is staff
    """
    return username in config['roles']['staff']

def is_user(config, username):
    """
    Check if user is user
    """
    return username in config['roles']['user']


def get_user_data(config, username):
    """
    Get user data
    """
    user_data = config.get('credentials').get('usernames').get(username)
    return user_data

def dump_config(config, file):
    """
    Update the config file
    """
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    return True