import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'senpai_itech_project.settings')
import django

django.setup()
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User
from senpai.tests import add_user, add_note, add_comment, add_enrollment, add_like, add_module


def populate():
    Joseph_notes = [
        {'mod': 'Programming', 'title': 'Jotest_note1'},
        {'mod': 'Programming', 'title': 'Jotest_note2'},
        {'mod': 'Software Engineering', 'title': 'Jotest_note3'},
        {'mod': 'Software Engineering', 'title': 'Jotest_note4'},
        {'mod': 'Cyber Security', 'title': 'Jotest_note5'},
        {'mod': 'Cyber Security', 'title': 'Jotest_note6'},
        {'mod': 'Cyber Security', 'title': 'Jotest_note7'},
    ]

    Jin_notes = [
        {'mod': 'Programming', 'title': 'Jitest_note1'},
        {'mod': 'Programming', 'title': 'Jitest_note2'},
        {'mod': 'Internet Technology', 'title': 'Jitest_note3'},
        {'mod': 'Internet Technology', 'title': 'Jitest_note4'},
        {'mod': 'Internet Technology', 'title': 'Jitest_note5'},
        {'mod': 'Computer System', 'title': 'Jitest_note6'},
        {'mod': 'Computer System', 'title': 'Jitest_note7'},
        {'mod': 'Computer System', 'title': 'Jitest_note8'},
        {'mod': 'Computer System', 'title': 'Jitest_note9'},
        {'mod': 'Computer System', 'title': 'Jitest_note10'},
    ]

    Marco_notes = [
        {'mod': 'Robotics', 'title': 'Mrtest_note1'},
        {'mod': 'Robotics', 'title': 'Mrtest_note2'},
        {'mod': 'Robotics', 'title': 'Mrtest_note3'},
        {'mod': 'Robotics', 'title': 'Mrtest_note4'},
        {'mod': 'Robotics', 'title': 'Mrtest_note5'},
        {'mod': 'Robotics', 'title': 'Mrtest_note6'},
        {'mod': 'Robotics', 'title': 'Mrtest_note7'},
        {'mod': 'Robotics', 'title': 'Mrtest_note8'},
        {'mod': 'Robotics', 'title': 'Mrtest_note9'},
        {'mod': 'Robotics', 'title': 'Mrtest_note10'},
        {'mod': 'Robotics', 'title': 'Mrtest_note11'},
        {'mod': 'Robotics', 'title': 'Mrtest_note12'},
    ]

    Xiaowei_notes = [
        {'mod': 'Spanish', 'title': 'Xwtest_note1'},
        {'mod': 'Spanish', 'title': 'Xwtest_note2'},
        {'mod': 'Japanese', 'title': 'Xwtest_note3'},
        {'mod': 'Japanese', 'title': 'Xwtest_note4'},
        {'mod': 'Japanese', 'title': 'Xwtest_note5'},
        {'mod': 'Embedded System', 'title': 'Xwtest_note6'},
        {'mod': 'Embedded System', 'title': 'Xwtest_note7'},
        {'mod': 'Embedded System', 'title': 'Xwtest_note8'},
        {'mod': 'Embedded System', 'title': 'Xwtest_note9'},
        {'mod': 'Embedded System', 'title': 'Xwtest_note10'},
    ]

    user_module = [
        {'uname': 'Joseph',
         'module': ['Programming', 'Software Engineering', 'Cyber Security', 'Robotics', 'Advance Manufacturing',
                    'Signal Processing'],
         'notes': Joseph_notes,
         },
        {'uname': 'Jin',
         'module': ['Programming', 'Internet Technology', 'Computer System', 'Robotics', 'Embedded System',
                    'Linear Algebra'],
         'notes': Jin_notes,
         },
        {'uname': 'Marco',
         'module': ['Computer Network', 'Human Computer Interface', 'Computer System', 'Robotics', 'Embedded System',
                    'Signal Processing', 'Japanese'],
         'notes': Marco_notes,
         },
        {'uname': 'Xiaowei',
         'module': ['Artificial Intelligence', 'Big Data', 'Digital Forensics', 'Robotics', 'Japanese', 'Spanish',
                    'Chinese'],
         'notes': Xiaowei_notes,
         },
        {'uname': 'Amy',
         'module': [],
         'notes': [],
         },
        {'uname': 'Betty',
         'module': [],
         'notes': [],
         },
        {'uname': 'Charlotte',
         'module': [],
         'notes': [],
         },
        {'uname': 'Diana',
         'module': [],
         'notes': [],
         },
        {'uname': 'Emma',
         'module': [],
         'notes': [],
         },
        {'uname': 'Faye',
         'module': [],
         'notes': [],
         },
    ]

    note_path = 'example_note.pdf'

    # If you want to add more data, add them to the dictionaries above.
    for um in user_module:
        u = add_user(um['uname'])
        for ms in um['module']:
            m = add_module(ms)
            add_enrollment(m, u)
            # note and comment add tests
            for ns in um['notes']:
                if ns['mod'] == m.name:
                    n = add_note(m, u, ns['title'], note_path)

    # randomly add comments and likes to every note
    for n in Note.objects.all():
        comment_cnt = random.randint(0, 10)
        like_cnt = random.randint(0, 10)
        for i in range(0, len(user_module)):
            u = User.objects.get(username=user_module[i]['uname'])
            if comment_cnt > i:
                add_comment(n, u, u.username + ' says nice note!')
            if like_cnt > i:
                add_like(u, n)

    # Print out all data we have added.
    for u in User.objects.all():
        print(f'User: {u}')

    for m in Module.objects.all():
        print(f'Module: {m}')

    for n in Note.objects.all():
        print(f'Note: {n}')
        print(Comment.objects.filter(note=n).count())


# Start execution here!
if __name__ == '__main__':
    print('Starting Senpai population script...')
    populate()
