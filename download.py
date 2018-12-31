# -*- coding: utf-8 -*-

import click
import json
import os
import requests
import time
from datetime import datetime


SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]


def get_channel_list():
    url = 'https://slack.com/api/channels.list'
    params = {
        'token': SLACK_API_TOKEN
    }
    res = requests.get(url, params=params)
    res.encoding = 'Shift_JIS'
    return res.text


def get_channel_hist(channel_id):
    url = 'https://slack.com/api/channels.history'
    one_year_ago = datetime.strptime('2018-01-01', '%Y-%m-%d')
    oldest_ts = None

    all_messages = []
    while True:
        params = {
            'token': SLACK_API_TOKEN,
            'channel': channel_id,
            'latest': oldest_ts,
            'count': 1000
        }
        res = requests.get(url, params=params)
        res.encoding = 'Shift_JIS'
        res = json.loads(res.content)
        all_messages.extend(res['messages'])

        if res['has_more']:
            time.sleep(1)
            oldest_ts = res['messages'][-1]['ts']
            if datetime.fromtimestamp(float(oldest_ts)) < one_year_ago:
                break
        else:
            break
    return all_messages


@click.group()
def cmd():
    pass


@click.command()
@click.option('-o', default='user_list', help='output file name')
def user_list(o):
    url = 'https://slack.com/api/users.list'
    params = {
        'token': SLACK_API_TOKEN
    }
    res = requests.get(url, params=params)
    res.encoding = 'Shift_JIS'
    #TODO: error handling
    with open(o, 'w') as f:
        f.write(res.text)


@click.command()
@click.option('-o', default='channel_list', help='output file name')
def channel_list(o):
    res = get_channel_list()
    #TODO: error handling
    with open(o, 'w') as f:
        f.write(res.text)


@click.command()
def all_channel_hist():
    try:
        with open('channel_list', 'r') as f:
            channel_list = next(f).rstrip()
    except:
        channel_list = get_channel_list()

    dn = 'all_channel_hist_' + datetime.now().strftime('%Y%m%d')
    if not os.path.exists(dn):
        os.mkdir(dn)

    channel_list = json.loads(channel_list)
    for channel in channel_list['channels']:
        channel_id = channel['id']
        channel_name = channel['name']
        channel_hist = get_channel_hist(channel_id)
        fn = dn + '/' + channel_name
        with open(fn, 'w') as f:
            f.write(str(channel_hist))
        break


cmd.add_command(user_list)
cmd.add_command(channel_list)
cmd.add_command(all_channel_hist)


def main():
    cmd()


if __name__ == '__main__':
    main()
