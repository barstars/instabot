from instagrapi import Client
import time
import datetime

class InstaDirectBot:
    def __init__(self):
        username = "login"
        password = "password"
        self.cl = Client()
        self.cl.login(username, password)
        
        self.old_users = []  # Список для отслеживания старых сообщений

        print("Бот начал проверку")

        while True:
            self.respond_to_messages()
            time.sleep(10)  # Задержка перед следующей проверкой

    def message_handler(self,tid, message):
        text = message.lower()
        print(text)
        if ("привет" in text):
            send_text = "Привет как у тебя дела?"
            self.send_message(tid,send_text)
        else:
            send_text = "Не понял"
            self.send_message(tid,send_text)


    def respond_to_messages(self):
        # Получаем последние диалоги
        threads = self.cl.direct_threads()

        for thread in threads:
            # Получаем последнее сообщение в текущем потоке
            last_message = self.cl.direct_messages(thread.id, 1)[0]
            
            # Проверка, является ли сообщение текстовым
            if (last_message.item_type == "text") and (last_message.is_sent_by_viewer == False):
                # Создаем словарь с ID сообщения и временем
                data_message = {"id": last_message.id, "time": last_message.timestamp}

                # Проверяем, если это новое сообщение, добавляем его в список старых
                if not any(item["id"] == data_message["id"] for item in self.old_users):
                    self.old_users.append(data_message)
                    self.message_handler(thread.id,last_message.text)
                else:
                    # Обновляем метку времени, если сообщение уже есть
                    for item in self.old_users:
                        if item["id"] == data_message["id"]:
                            if item["time"] == data_message["time"]:
                                break
                            else:
                                item["time"] = data_message["time"]
                                user = thread.users[0]
                                self.message_handler(thread.id,last_message.text)
                                break


    def send_message(self, tid, text):
        self.cl.direct_send(text, thread_ids=[tid])
# Запускаем бота
InstaDirectBot()
