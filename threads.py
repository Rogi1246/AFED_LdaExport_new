import json
# import sys
# import email
# from email.message import EmailMessage
import objectpath

# let's start
# extract the headers and timestamps from the mails

with open("export_TEST.json") as datafile: data = json.load(datafile)
tree = objectpath.Tree(data['headers'])
from_ = tuple(tree.execute('$..from'))
in_reply_to_ = tuple(tree.execute('$..in_reply_to'))
msg_id = tuple(tree.execute('$..message_id'))

# print("FROM : ", from_, "IN_REPLY : ", in_reply_to_, "ID : ", msg_id)
print("-------------------------------------------------------------")


# going through the message-headers to filter out
# non-null values and attaching the right number to them


def get_msg_id():
    list_of_ids = []
    n = 0
    count = 0
    for msg in msg_id:
        if msg is not None:
            list_of_ids.append(msg)
            print(list_of_ids, "LIST ::::::: ")
            print("----------------", msg, " = MSG ID", n)
            count+=1
            # which_reply_header(msg)
            is_reply(count)
        n = n + 1
        print(count)
    # for a in in_reply_to_:
    #    if a is not None:
    #        repl = a
    #        full = idh+repl
    #        print("merged: ", full)

# retrieve the id and reply-header separately, return these values as list
# iterate over list in separate method and join them together


def which_reply_header(message):
    if message in in_reply_to_ is not None:
        reply = message
        print(message)
        full = idh+reply
        print(full)


def is_reply(counter):
    list_of_replies = []
    n = 0
    counter_two = 0
    for msg in in_reply_to_:
        if msg is not None:
            list_of_replies.append(msg)
            print(msg, " = IN REPLY", n)
            counter_two+=1
            print(list_of_replies)
            print("------------", list_of_replies[counter], "------------")
        if msg is None or msg == "":
            list_of_replies.append('<None>')
            counter_two += 1
        n = n + 1
    print(counter_two)




get_msg_id()
is_reply()
