import pytest
import sqlite3
from rought import create_task_table, add_task, delete_task, edit_task, view_task

@pytest.fixture
def setup_db():
    my_tasks = sqlite3.connect('tasklist.db')
    c = my_tasks.cursor()
    c.execute('DELETE FROM mytasks')
    my_tasks.commit()
    yield my_tasks
    my_tasks.close()

def test_create_task_table():
    create_task_table()
    my_tasks = sqlite3.connect('tasklist.db')
    c = my_tasks.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mytasks'")
    result = c.fetchone()
    my_tasks.close()
    assert result[0] == 'mytasks'

def test_add_task(setup_db):
    add_task('Task 1', 'This is task 1', '2022-04-01', '2022-04-05', 2)
    add_task('Task 2', 'This is task 2', '2022-04-02', '2022-04-06', 1)
    my_tasks = sqlite3.connect('tasklist.db')
    c = my_tasks.cursor()
    c.execute("SELECT COUNT(*) FROM mytasks")
    count = c.fetchone()[0]
    my_tasks.close()
    assert count == 2

def test_delete_task(setup_db):
    add_task('Task 1', 'This is task 1', '2022-04-01', '2022-04-05', 2)
    add_task('Task 2', 'This is task 2', '2022-04-02', '2022-04-06', 1)
    delete_task(1)
    my_tasks = sqlite3.connect('tasklist.db')
    c = my_tasks.cursor()
    c.execute("SELECT COUNT(*) FROM mytasks")
    count = c.fetchone()[0]
    my_tasks.close()
    assert count == 1


def test_edit_task(setup_db):
    # Add a task first
    add_task('Task 1', 'This is task 1', '2022-04-01', '2022-04-05', 2)

    # Edit the task
    edit_task(1, 'New Task 1', 'This is the new task 1', '2022-04-02', '2022-04-06', 1)

    # Check if the task was edited correctly
    my_tasks = sqlite3.connect('tasklist.db')
    c = my_tasks.cursor()
    c.execute("SELECT * FROM mytasks WHERE id=?", (1,))
    result = c.fetchone()
    my_tasks.close()
    assert result[1:] == ('New Task 1', 'This is the new task 1', '2022-04-02', '2022-04-06', 1)

def test_view_task(setup_db):
    # Add some tasks
    add_task('Task 1', 'This is task 1', '2022-04-01', '2022-04-05', 2)
    add_task('Task 2', 'This is task 2', '2022-04-02', '2022-04-06', 1)
    add_task('Task 3', 'This is task 3', '2022-04-03', '2022-04-07', 3)

    # Get all the tasks
    tasks = view_task()

    # Check if the tasks were returned correctly
    assert len(tasks) == 3
    assert tasks[0][1:] == ('Task 1', 'This is task 1', '2022-04-01', '2022-04-05', 2)
    assert tasks[1][1:] == ('Task 2', 'This is task 2', '2022-04-02', '2022-04-06', 1)
    assert tasks[2][1:] == ('Task 3', 'This is task 3', '2022-04-03', '2022-04-07', 3)

pytest.main(["-v", "--tb=line", "-rN", __file__])
