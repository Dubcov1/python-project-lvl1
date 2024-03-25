import asyncio
import json
import redis
import pymysql
import pystrix

# Подключения к Asterisk
AMI_HOST = '127.0.0.1'
AMI_PORT = 5038
AMI_USERNAME = 'admin'
AMI_PASSWORD = 'PSWDforMY1!'

# Подключения к Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Подключение к MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'PSWDforMY1!'
MYSQL_DB = 'cdr'

# Функция для регистрации
async def register_sip(phone_number):
    async with pystrix.Asterisk(AMI_HOST, AMI_PORT, AMI_USERNAME, AMI_PASSWORD) as ami:
        response = await ami.sip_peer('SIP/' + phone_number)
        print(response)

# Звонок
async def make_call(phone_number, number_to_call):
    async with pystrix.Asterisk(AMI_HOST, AMI_PORT, AMI_USERNAME, AMI_PASSWORD) as ami:
        response = await ami.originate(
            'SIP/' + phone_number,
            application='Playback',
            data='demo-congrats'
        )
        print(response)

# Обработка задания в Redis
async def handle_callback(redis_conn):
    while True:
        _, task = redis_conn.blpop('callback')
        task_data = json.loads(task)
        phone_number = task_data['phone_number']
        number_to_call = task_data['number_to_call']
        await make_call(phone_number, number_to_call)

# Сохранение CDR в MySQL БД
def save_cdr(cdr_data):
    try:
        connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
        with connection.cursor() as cursor:
            sql = "INSERT INTO cdr_data (caller_id, destination_number, call_duration) VALUES (%s, %s, %s)"
            cursor.execute(sql, (cdr_data['caller_id'], cdr_data['destination_number'], cdr_data['call_duration']))
        connection.commit()
    except pymysql.Error as e:
        print(f"Error during saving CDR to MySQL: {e}")
    finally:
        if connection:
            connection.close()

# Приложение
async def main():
    # Подключение к Redis
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    
    # Запуск задачи обработки колбэков
    callback_task = asyncio.create_task(handle_callback(redis_conn))

    # Ожидание завершения задачи
    await callback_task

# Главная функция приложения
if __name__ == "__main__":
    asyncio.run(main())
