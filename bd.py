import sqlite3


class DbHandler(object):
    conn = None 
    cur = None

    def __init__(self):
        self.conn = sqlite3.connect('tbot_database_test.db')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    ##################### users #################
    def add_user(self, user_id):
        try:
            self.cur.execute('''INSERT INTO users (user_id)
                                VALUES (?)''', (user_id,))
            self.conn.commit()
        except Exception:
            #print('this id already exists')
            pass

    def add_selected_number(self, user_id, number):
        self.cur.execute('''UPDATE users 
                            SET 
                            selected_number = (?) 
                            WHERE user_id = (?)''', (number, user_id))
        self.conn.commit()

    def get_user(self):
        self.cur.execute('''SELECT user_id
                            FROM users''')
        return self.cur.fetchall()



######################## tasks  ################

    def select_tasks(self, user_id):
        self.cur.execute('''SELECT task, state_id, task_id, deadline 
                            FROM tasks 
                            WHERE user_id = (?)
                            ORDER BY state_id, deadline NULLS LAST ''', (user_id,))
        return self.cur.fetchall()

    def add_gener_num_tasks(self, task_id, number):
        self.cur.execute('''UPDATE tasks
                            SET
                            generated_num = (?)
                            WHERE task_id = (?)''', (number, task_id))
        self.conn.commit()

    def add_task(self, user_id, task):
        self.cur.execute('''INSERT INTO tasks (user_id, task) 
                            VALUES (?, ?)''', (user_id, task))
        self.conn.commit()

    def get_task_generated_num(self, user_id):
        self.cur.execute('''SELECT generated_num
                            FROM tasks
                            WHERE user_id = (?)
                            ORDER BY generated_num''', (user_id,))
        return self.cur.fetchall()

    def delete_task(self, user_id, gen_num):
        self.cur.execute('''DELETE FROM tasks 
                            WHERE user_id = (?) AND generated_num = (?)''', (user_id, gen_num))
        self.conn.commit()


    def add_deadline(self, user_id, date):
        task_id = self.selected_task_id(user_id)
        self.cur.execute('''UPDATE tasks
                            SET
                            deadline = (?)
                            WHERE task_id = (?)''', (date, task_id))
        self.conn.commit()


    def get_deadline(self, task_id):
        self.cur.execute('''SELECT deadline
                            FROM tasks
                            WHERE task_id = (?)''', (task_id,))
        deadline, = self.cur.fetchone()
        if deadline == None:
            deadline = ''
        print(deadline)
        return deadline

    def change_task_state(self, user_id, state_id):
        self.cur.execute('''SELECT tasks.task_id
                            FROM tasks
                                INNER JOIN
                                users
                            WHERE users.user_id = (?) AND users.selected_number = tasks.generated_num''', (user_id,))
        task_id = self.cur.fetchone()
        print(task_id)
        self.cur.execute('''UPDATE tasks 
                            SET 
                            state_id = (?) 
                            WHERE task_id = (?)''', (state_id, task_id[0]))
        self.conn.commit()

    def add_done_date(self, user_id, now):
        task_id = self.selected_task_id(user_id)
        self.cur.execute('''UPDATE tasks 
                            SET completed_when = (?)
                            WHERE task_id = (?)''', (now, task_id))
        self.conn.commit()

    def selected_task_id(self, user_id):
        self.cur.execute('''SELECT tasks.task_id
                            from tasks
                                inner join
                                users
                            where users.user_id = (?) and users.selected_number = tasks.generated_num''', (user_id,))
        task_id = self.cur.fetchone()
        return task_id[0]


    def edit_task(self, user_id, edited_task):
        task_id = self.selected_task_id(user_id)
        self.cur.execute('''UPDATE tasks
                            SET
                            task = (?)
                            WHERE task_id = (?)''', (edited_task, task_id))
        self.conn.commit()



##################### habits ################
    def select_habits(self, user_id):
        self.cur.execute('''
                            SELECT * 
                            FROM habits 
                            WHERE user_id = (?)''',(user_id,))
        return self.cur.fetchall()

    def add_gener_num_habits(self, habit_id, number):
        self.cur.execute('''UPDATE habits
                            SET
                            generated_num = (?)
                            WHERE habit_id = (?)''', (number, habit_id))
        self.conn.commit()

    def add_habit(self, user_id, habit):
        self.cur.execute("SELECT habit FROM habits WHERE user_id = ?", (user_id,))
        massive = [i for i in self.cur.fetchall()]
        if (habit,) not in massive:
            self.cur.execute('''INSERT INTO habits
                            (user_id, habit) 
                            VALUES (?, ?)''', (user_id, habit))
            self.conn.commit()

    def get_habit_generated_num(self, user_id):
        self.cur.execute('''SELECT generated_num
                            FROM habits
                            WHERE user_id = (?)
                            ORDER BY generated_num''', (user_id,))
        return self.cur.fetchall()

    def delete_habit(self, user_id, gen_num):
        self.cur.execute('''DELETE FROM habits 
                            WHERE generated_num = (?) AND user_id=(?)''',(gen_num, user_id))
        self.conn.commit()


    def change_progress_habit(self, user_id, gen_num):
        self.cur.execute('''SELECT is_done
                            FROM habits
                            WHERE generated_num = (?) AND user_id = (?)''',(gen_num, user_id))
        if self.cur.fetchone() == (1,):
            is_done = 0
        else:
            is_done = 1
        self.cur.execute('''UPDATE habits
                            SET is_done = (?)
                            WHERE generated_num = (?) AND user_id = (?)''', (is_done, gen_num, user_id))
        self.conn.commit()

    def edit_habit(self, user_id, edited_habit):
        self.cur.execute('''SELECT habits.habit_id
                            FROM habits
                                INNER JOIN
                                users
                            WHERE users.user_id = (?) AND users.selected_number = habits.generated_num''', (user_id,))
        habit_id, = self.cur.fetchone()
        self.cur.execute('''UPDATE habits
                            SET
                            habit = (?)
                            WHERE habit_id = (?)''', (edited_habit, habit_id))
        self.conn.commit()

    def what_progress_habits(self, user_id):
        self.cur.execute('''SELECT is_done 
                               FROM habits
                               WHERE user_id = ?''', (user_id,))
        self.conn.commit()
        return self.cur.fetchall()

    def progress_habits(self,date,user_id, progress):
        self.cur.execute('''INSERT INTO habit_progress
                            (date,user_id, progress) VALUES (?,?,?)''',(date,user_id, progress))
        self.conn.commit()

    def zero_habits(self):
        self.cur.execute('''UPDATE habits
                            SET is_done = ?''', (0,))
        self.conn.commit()

    def get_progress_for_habits(self, user_id):
        self.cur.execute('''SELECT date, progress 
                            FROM habit_progress
                            WHERE user_id = ?''',(user_id,))
        self.conn.commit()
        return self.cur.fetchall()



#####################  goals  ###############
    def select_goals(self, user_id):
        self.cur.execute('''SELECT * 
                            FROM goals 
                            WHERE user_id = (?)''',(user_id,))
        return self.cur.fetchall()

    def add_gener_num_goals(self, goal_id, number):
        self.cur.execute('''UPDATE goals
                            SET
                            generated_num = (?)
                            WHERE goal_id = (?)''', (number, goal_id))
        self.conn.commit()

    def add_goal(self, user_id, goal):
        self.cur.execute("SELECT goal FROM goals WHERE user_id = ?", (user_id,))
        massive = [i for i in self.cur.fetchall()]
        if (goal,) not in massive:
            self.cur.execute('''INSERT INTO goals
                            (user_id, goal) 
                            VALUES (?, ?)''', (user_id, goal))
            self.conn.commit()

    def get_goal_generated_num(self, user_id):
        self.cur.execute('''SELECT generated_num
                            FROM goals
                            WHERE user_id = (?)
                            ORDER BY generated_num''', (user_id,))
        return self.cur.fetchall()

    def delete_goal(self, user_id, gen_num):
        self.cur.execute('''DELETE FROM goals 
                            WHERE generated_num = ? AND user_id=(?)''',(gen_num, user_id))
        self.conn.commit()

    def change_progress_goal(self, user_id, gen_num):
        self.cur.execute('''SELECT is_done
                            FROM goals
                            WHERE generated_num = (?) AND user_id = (?)''',(gen_num, user_id))

        if self.cur.fetchone() == (1,):
            is_done = 0
        else:
            is_done = 1
        self.cur.execute('''UPDATE goals
                            SET is_done = ?
                            WHERE generated_num = ? AND user_id = (?)''', (is_done, gen_num, user_id))
        self.conn.commit()

    def edit_goal(self, user_id, edited_goal):
        self.cur.execute('''SELECT goals.goal_id
                            FROM goals
                                INNER JOIN
                                users
                            WHERE users.user_id = (?) AND users.selected_number = goals.generated_num''', (user_id,))
        goal_id, = self.cur.fetchone()
        self.cur.execute('''UPDATE goals
                            SET
                            goal = (?)
                            WHERE goal_id = (?)''', (edited_goal, goal_id))
        self.conn.commit()



