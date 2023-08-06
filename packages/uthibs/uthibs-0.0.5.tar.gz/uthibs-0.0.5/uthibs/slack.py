from slacker import Slacker


def get_slack_token(path='slack.token'):
    with open(path, "r") as fichier:
        token = fichier.read()
    return token


def create_slack(slack_api_token):
    slack = Slacker(slack_api_token)
    return slack


def send_message(slack, message, channel='test_channel', username='Thib', emoji=':female-firefighter:'):
    slack.chat.post_message(
        channel=channel,
        text=message,
        username=username,
        icon_emoji=emoji
    )


if __name__ == "__main__":
    path = '/Users/thibaud/Documents/Python_scripts/Fonctions/slack.token'
    token = get_slack_token(path)
    slack = create_slack(token)
    send_message(slack, 'This is a test', channel='aléatoire')
