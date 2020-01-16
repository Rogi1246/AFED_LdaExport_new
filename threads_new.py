import json
import datetime

# LOOK IN THE EXPLORER.PY !!!

head_labels = []

id_list = []
from_mail_list = []
in_reply_list = []
ref_list = []
timestamp_list = []


def get_from_email(categ):
    from_mail = categ.get('from_email')
    print("FOUND MAIL ADDRESS--- ", from_mail, '\n')
    from_mail_list.append(from_mail)
    return from_mail


def get_message_ids(categ):
    message_ids = categ.get('message_id')
    id_list.append(message_ids)
    print("FOUND ID--- ", message_ids, '\n')
    return message_ids


def get_in_reply_to(categ):
    in_reply = categ.get('in_reply_to')
    in_reply_list.append(in_reply)
    if in_reply is not None:
        print("FOUND REPLY--- ", in_reply, '\n')
    return in_reply


def get_references(categ):
    references = categ.get('references')
    ref_list.append(references)
    if references is not None:
        print("FOUND REF--- ", references, '\n')
    return references


def get_timestamps(timest, label):
    stamps = timest.get(label)
    timestamp_list.append(stamps)
    print("STAMPS : ", stamps, '\n')


def get_mails():
    mail_val = 0
    for lines in open('export_hardware.json').readlines():
        mails = json.loads(lines)
        headers = mails.get('headers')
        timestamps = mails.get('@timestamp')
        for labels in headers:
            categories = headers.get(labels)
            print(categories, '\n')
            mail_address = get_from_email(categories)
            msg_id = get_message_ids(categories)
            tmp_reply = get_in_reply_to(categories)
            refer = get_references(categories)
            mail_val += 1
            print(mail_val)
        # for labels in timestamps:
            # get_timestamps(timestamps, labels)
    for i in msg_id:
        get_reply_by_id(i)


def get_reply_by_id(mess_id):
    for j in in_reply_list:
        if mess_id == j:
            print("found one", mess_id, '\n')
            return j


get_mails()
# sorted timestamp list
timestamps_new = sorted(timestamp_list)

# find the ids that match with the in_reply header
id_reply_time_list = []

for item in id_list:
    replies = get_reply_by_id(item)
    if replies is not None:
        id_reply_time_list.append(item + " " + replies)

# for u in id_reply_time_list:
    # print(u, '\n')
