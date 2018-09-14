from dal import *
import textwrap
import tabulate


def get_users_summary():
    users = []
    for user in User.objects:
        users.append(_summarize_user(user))
    print(tabulate.tabulate(users, headers=['Name', 'TID', 'Rounds']))
    return


def _summarize_user(user):
    rounds = []
    for pair in get_pairs_containing_tid(user.tid):
        if pair.is_active:
            rounds.append(f'{pair.round_num} (IP)')
        else:
            rounds.append(f'{pair.round_num}')
    return [user.name, user.tid, ', '.join(rounds)]


def get_conversation(tid1, tid2, round_num, outfile, delimiter='\n' + '-' * 110 + '\n', stdout=False):
    pair = get_pair_by_tid(tid1, round_num=round_num)

    pair = pair[0]
    header = f'{tid1} with {tid2} for round {round_num}\n\n\n'
    footer = f'\n\n\ntid1 confidence = {pair.confidence1}\ntid2 confidence = {pair.confidence2}'

    thread = [header]
    for msg in Message.objects(pair=pair).order_by('timestamp'):
        if get_name_by_tid(tid1) == msg.sender:
            thread.append(_message_to_string(msg, 'SENDER 1'))
        if get_name_by_tid(tid2) == msg.sender:
            thread.append(_message_to_string(msg, 'SENDER 2', left_pad=55))

    thread.append(footer)
    conversation = delimiter.join(thread)

    with open(outfile, 'w') as out_file:
        out_file.write(conversation)

    if stdout:
        print(conversation)
    return


def _message_to_string(message, sender, msg_width=50, left_pad=None):
    result = message.timestamp.strftime('%I:%M:%S %p') + '\n'
    result += f'{sender}\n'
    result += '\n'.join(textwrap.wrap(message.message, msg_width))

    if left_pad is not None:
        result = textwrap.indent(result, ' ' * left_pad)
    return result
