import os

import yaml


# open yaml to dict
def read_config_yaml() -> dict:
    """
    :return: setting dict
    """
    with open('./config/yt-dlp.yml') as f:
        return yaml.safe_load(f)


def write_config_yml(dict_var):
    """
    write yt-dlp.yml
    :param dict_var: setting dict
    :return:
    """
    with open("./config/yt-dlp.yml", 'w') as f:
        yaml.dump(dict_var, f, default_flow_style=False)


def generate_config_yml():
    """
    init yt-dlp.yml
    :return:
    """
    if not os.getenv("USERPROFILE"):
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    else:
        base_path = os.getenv("USERPROFILE")
    path = os.path.normpath(os.path.join(base_path, 'Videos\\Youtube')).replace('\\', '/')
    '''
    also you con set path for example:
        'paths': {'home': path, 'temp': os.path.join(path, Temp)}
    
    if have ffmpeg and aria2c
    example filed:
        'format': "bv*+ba/b",
        'external_downloader': 'aria2c',
        'external_downloader_args': '['-x', '16', '-s', '16', '-j', '16', '-k', '2M']'
        ...
    '''
    dict_var_eg = {
        'settings': {
            'proxy': None,
            'match_filter': None,
            'ratelimit': None,
            'paths': {
                "home": path,
                'temp': os.path.join(path, 'Temp').replace('\\', '/'),
                "subtitle": os.path.join(path, 'Subs').replace('\\', '/'),
                "thumbnail": os.path.join(path, 'Thumbnails').replace('\\', '/'),
            },
            'format': "bv+ba/b",
            'external_downloader': None,
            'external_downloader_args': None
        }
    }
    write_config_yml(dict_var_eg)
