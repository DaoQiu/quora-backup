import os
from quora import Quora, Activity

def json_sync_items(old, new):
    # need to come up with a faster way to do this
    # db implementations will be much faster
    ids = []
    for item in old:
        ids.append(item['id'])
    for item in new:
        if item['id'] not in ids:
            old.append(item)
    return old

def json_backup(new, filepath):
    import json
    if os.path.isfile(filepath):
        with open(filepath) as outfile:
            old = json.load(outfile)
        old = json_sync_items(old, new)
        with open(filepath, 'w') as outfile:
            json.dump(old, outfile)
    else:
        with open(filepath, 'w') as outfile:
          json.dump(new, outfile)

def csv_sync_items(writer, old_ids, new, fieldnames):
    # need to come up with a faster way to do this
    # db implementations will be much faster
    for item in new:
        if item['id'] not in old_ids:
            row = []
            for field in fieldnames:
                if field in item.keys():
                    row.append(item[field].encode('utf8'))
                else:
                    row.append(None)
            writer.writerow(row)

def csv_backup(new, filepath):
    import csv
    fieldnames = ['id', 'published', 'link', 'title', 'summary']
    if os.path.isfile(filepath):
        old_ids = []
        with open(filepath, 'r') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                old_ids.append(row[0])
        with open(filepath, 'a') as fp:
            writer = csv.writer(fp, delimiter=',')
            csv_sync_items(writer, old_ids, new, fieldnames)
    else:
        with open(filepath, 'wb') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(fieldnames)
            for item in new:
                row = []
                for field in fieldnames:
                    if field in item.keys():
                        row.append(item[field].encode('utf8'))
                    else:
                        row.append(None)
                writer.writerow(row)

class QuoraBackup():
    def __init__(self, user):
        quora = Quora()
        self.activity = quora.get_activity(user)

    def backup(self, path, format, type):
        if path is None:
            path = os.getcwd()
        if format == 'json':
            if type == 'answers':
                json_backup(self.activity.answers, os.path.join(path, 'answers.json'))
            elif type == 'questions':
                json_backup(self.activity.questions, os.path.join(path, 'questions.json'))
            elif type == 'upvotes':
                json_backup(self.activity.upvotes, os.path.join(path, 'upvotes.json'))
            elif type == 'question_follows':
                json_backup(self.activity.question_follows, os.path.join(path, 'question_follows.json'))
            # elif type == 'user_follows':
            #     json_backup(self.activity.user_follows, os.path.join(path, 'user_follows.json'))
            else:
                json_backup(self.activity.answers, os.path.join(path, 'answers.json'))
                json_backup(self.activity.questions, os.path.join(path, 'questions.json'))
                json_backup(self.activity.upvotes, os.path.join(path, 'upvotes.json'))
                json_backup(self.activity.question_follows, os.path.join(path, 'question_follows.json'))
        elif format == 'csv':
            if type == 'answers':
                csv_backup(self.activity.answers, os.path.join(path, 'answers.csv'))
            elif type == 'questions':
                csv_backup(self.activity.questions, os.path.join(path, 'questions.csv'))
            elif type == 'upvotes':
                csv_backup(self.activity.upvotes, os.path.join(path, 'upvotes.csv'))
            elif type == 'question_follows':
                csv_backup(self.activity.question_follows, os.path.join(path, 'question_follows.csv'))
            # elif type == 'user_follows':
            #     csv_backup(self.activity.user_follows, os.path.join(path, 'user_follows.csv'))
            else:
                csv_backup(self.activity.answers, os.path.join(path, 'answers.csv'))
                csv_backup(self.activity.questions, os.path.join(path, 'questions.csv'))
                csv_backup(self.activity.upvotes, os.path.join(path, 'upvotes.csv'))
                csv_backup(self.activity.question_follows, os.path.join(path, 'question_follows.csv'))
                # csv_backup(self.activity.user_follows, os.path.join(path, 'user_follows.csv'))
        else:
            print 'Backup format has not yet been implemented.'
