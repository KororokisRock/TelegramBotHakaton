from mysql.connector import connect, Error
from decouple import config
import uuid
import hashlib

upper_set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
lower_set = set('abcdefghijklmnopqrstuvwxyz')
digit_set = set('1234567890')

#проверка пароля на надежность
def is_valid_password(password):
    
    # Длина строки пароля не менее шести символов.
    if len(password) < 6:
        return False

    password_set = set(password)

    # Содержит хотя бы одну букву в верхнем регистре.
    # Содержит хотя бы одну букву в нижнем регистре.
    # Содержит хотя бы одну цифру.
    # Функция is_valid_password должна вернуть True,
    # если переданный в качестве параметра пароль отвечает требованиям надежности.
    return \
        password_set & upper_set and \
        password_set & lower_set and \
        password_set & digit_set


#создание и хэширование пароля
def hash_password(password):    
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt  

#проверка пароля
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest() 


#подключение к бд, выдаёт False если подключение провалено
def conn():
    try:
        connection = connect(host=config('host'), 
                             user=config('user_name'), 
                             password=config('pass'), 
                             database=config('user_name'), 
                             port=config('port'),
                             charset='utf8',
                             use_unicode = True)
        return connection
    except Error as e:
        print(e)
        return False
    
#строки в бд в виде получение словаря
def get_object(table, column, cell):
    cnct = conn()
    if cnct:
        with cnct.cursor() as cur:
            if cell.isnumeric():
                command = f'''
                SELECT * FROM {table} WHERE {column} = {cell}
                '''
            else:
                command = f'''
                SELECT * FROM {table} WHERE {column} = '{cell}'
                '''
            cur.execute(command)

            res = cur.fetchall()

            if len(res) == 0:
                return False
            
            res1 = [i for i in res[0]]

            command =f'''
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table}';
                '''
            cur.execute(command)
            res2 = [i[0] for i in cur.fetchall()]
            return dict(zip(res2,res1))


#проверка: есть ли юзер в бд
def user_in_db(type,cell):
    cnct = conn()
    if cnct:
        command = f'''
            SELECT * FROM users WHERE {type} = "{cell}"
            '''
        with cnct.cursor() as cur:
            cur.execute(command)
            res = cur.fetchall()
            if len(res) > 0:
                return True
            else: 
                return False

#внесение в бд нового юзера если юзер с таким ником уже есть возвращает False, если у юзера не было tg_id, добавляет 
def user_to_db(user,password,tg_id=0):
    cnct = conn()
    

    if cnct:
        log_user = get_object('users','name', user)
        if log_user:
            if log_user['tg_id']==0:
                command = f'''
                    UPDATE users SET tg_id={tg_id} WHERE name = "{log_user['name']}"
                    '''
            else:
                print('такой юзер уже существует')
                return False


        else:
            command = f'''
                INSERT INTO users(tg_id,name,password,is_admin)
                VALUE({tg_id},'{user}','{hash_password(password)}',false)
                '''
        with cnct.cursor() as cur:
            cur.execute(command)
            cnct.commit()



#внесение в бд нового вопроса
def quest_to_db(user_id,quest):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:


            command = f'''
            INSERT INTO quest(user_id,q_text)
            VALUE({user_id},'{quest}')
            '''
            cur.execute(command)
            cnct.commit()

#внесение в бд нового ответа
def answer_to_db(user_id,q_id,answer):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:
            command = f'''
            INSERT INTO answer(user_id,q_id,ans_text)
            VALUE({user_id},{q_id},{answer})'
            '''
            cur.execute(command)
            
            cnct.commit()

#добавляет или убавляет рейтинг вопроса, rate либо '+' либо '-'
def quest_rate(q_id,rate):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:
            command = f'''
            update quest set rating = rating {rate} 1 where q_text = '{q_id}'
            '''
            cur.execute(command)
            cnct.commit()


#добавляет или убавляет рейтинг юзеру, rate либо '+' либо '-'
def user_rate(name,rate):
    cnct = conn()
    if cnct:
        
        with cnct.cursor() as cur:
            command = f'''
            update users set rating = rating {rate} 1 where name = '{name}'
            '''
            cur.execute(command)
            cnct.commit()

'''
шпакргалка по таблицам:

название          названия колонок
таблицы                  |
  |                      |
 \|/                    \|/
users(     id,   tg_id,   name, password, is_admin, rating)

quest(   q_id, user_id, q_text, rating)

answer(ans_id, user_id,   q_id, ans_text)


'''


'''cnct = conn()
with cnct.cursor() as cur:
    cur.execute('select *  from users;')
    print(cur.fetchall())'''
