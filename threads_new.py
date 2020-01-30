import json
import uuid


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def get_id_by_reply(reply_value, id_list):
    for items in id_list:
        if reply_value == items:
            # print("THERE IT IS", items)
            return items


def get_message_ids(categ):
    message_ids = categ.get('message_id')
    # retrieved_ids.add(message_ids)
    # print("FOUND ID--- ", message_ids, '\n')
    return message_ids


def msg_id_prefix(mess_id):
    s = mess_id.split('@', maxsplit=1)
    if len(s) > 1 and s[1].startswith('public.gmane.org'):
        s_pre = s[0].split('-', maxsplit=1)[0]
        return s_pre if len(s_pre) > 7 and not s_pre.isdigit() else s[0]
    return s[0]


def email_threads():
    def create_should_clause(p):
        return [
            {'prefix': {'headers.message_id.keyword': p}},
            {'prefix': {'headers.in_reply_to.keyword': p}},
            {'prefix': {'headers.references.keyword': p}}
        ]

    curr_retrieved_ids = set()
    references_set = set()
    reply_set = set()
    # id_prefix = msg_id_prefix(message_id)
    # should_clause = create_should_clause(id_prefix)
    for lines in open('export_hardware.json').readlines():
        mails = json.loads(lines)
        headers = mails.get('headers')
        timestamps = mails.get('@timestamp')
        #
        for labels in headers:
            categories = headers.get(labels)
            if categories.get('message_id'):
                tmp = categories.get('message_id')
                curr_retrieved_ids.add(categories['message_id'])
                # print("ID :                 ", categories['message_id'])
                tmp2 = categories.get('in_reply_to')

            if categories.get('in_reply_to'):
                references_set.update(categories['in_reply_to']
                                      if type(categories['in_reply_to']) is list else [categories['in_reply_to']])

                reply_set.update(categories['in_reply_to']
                                 if type(categories['in_reply_to']) is list else [categories['in_reply_to']])
                # print("REPLY :              ", categories['in_reply_to'])
                orig_mail = {}
                for something in curr_retrieved_ids:
                    if categories['in_reply_to'] == something:
                        # print(something, "FOUND")
                        for sec_labels in mails.get('main_content'):
                            if sec_labels == labels:
                                # print(labels)
                                msg_id = categories['message_id']
                                # print("ID :         ", msg_id, '\n')
                                reply_id = categories['in_reply_to']
                                for ab in curr_retrieved_ids:
                                    if reply_id == ab:
                                        # print("YES", ab)
                                        for third_labels in mails['headers']:
                                            temp = mails['headers'][third_labels]
                                            if temp['in_reply_to'] == msg_id:
                                                # print("IN REPLY : ", msg_id)
                                                # print("MAIN_CONTENT : ", mails['main_content'][third_labels])
                                                # print("PLAIN_TEXT : ", mails['text_plain'][third_labels])
                                                orig_mail = {"ID             ": mails['headers'][third_labels]['message_id'],
                                                             "IN REPLY TO    ": mails['headers'][third_labels]['in_reply_to'],
                                                             "AT THIS TIME   ": mails['@timestamp'][third_labels],
                                                             "MAIN CONTENT   ": mails['main_content'][third_labels],
                                                             "PLAIN TEXT     ": mails['text_plain'][third_labels]
                                                             }
                                # print("REPLY_TO_ID :     ", reply_id, '\n')
                                main_cont = mails['main_content'][sec_labels]
                                time = mails['@timestamp'][sec_labels]
                                # print("CONTENT :        ", main_cont, '\n')
                                # working, gets the id, and id of mail that was replied to and shows the content of that
                                new_id = uuid.uuid1().int
                                dat = {"THREAD ID                   ": new_id,
                                       "ID                          ": msg_id,
                                       "IN_REPLY_TO THIS ID         ": reply_id,
                                       # find this ID that and get message info of that
                                       # add next (following) replies in here
                                       "AT TIME                     ": time,
                                       "MESSAGE                     ": main_cont,
                                       "CONNECTED MAIL              ": orig_mail}
                                a = json.dumps(dat, indent=4, cls=SetEncoder)
                                # print(dat)
                                print(a)

            if categories.get('references'):
                references_set.update(categories['references']
                                      if type(categories['references']) is list else [categories['references']])
                # print("REFERENCE :          ")

            matches = set()

            the_text = []
            if mails.get('main_content'):
                for labels_two in mails.get('main_content'):
                    what = mails.get('main_content').get(labels_two)
                    # print(what)
                    the_text.append(what
                                    if type(what) is dict else [what])

            # for stuff in the_text:
                # print("MAIN_CONTENT     ", stuff, '\n')

        for message_id in (references_set - curr_retrieved_ids):
            id_prefix = msg_id_prefix(message_id)
            # print("NEW ID :                 ", id_prefix, '\n')

        match_set = set()
        for reply in reply_set:
            for message_id in curr_retrieved_ids:
                if reply == message_id:
                    # print("FOUND MATCH :        ", message_id, '\n')
                    match_set.add(message_id)


email_threads()
