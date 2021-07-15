from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"
#INSERT_INITIAL_DATA = "./data/db/init_data.sql"
INSERT_INITIAL_DATA = ""

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)
    if isfile(INSERT_INITIAL_DATA):
        scriptexec(INSERT_INITIAL_DATA)


def commit():
    cxn.commit()


def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))


def close():
    cxn.close()


def field(command, *values):
    cur.execute(command, values)
    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cur.execute(command, values)
    return cur.fetchone()


def record_(command):
    cur.execute(command)
    return cur.fetchone()


def records(command, *values):
    cur.execute(command, values)
    return cur.fetchall()


def records_(command):
    cur.execute(command)
    return cur.fetchall()


def column(command, *values):
    cur.execute(command, values)
    return [item[0] for item in cur.fetchall()]


def column_(command):
    cur.execute(command)
    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, values)
    commit()


def execute_(command):
    cur.execute(command)
    commit()


def multiexec(command, valueset):
    cur.executemany(command, valueset)
    commit()


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())
