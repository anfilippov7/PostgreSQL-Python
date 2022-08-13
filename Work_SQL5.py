import psycopg2

with psycopg2.connect(database="work5", user="postgres", password="1234") as conn:
    with conn.cursor() as cur:


#1 Функция, создающая структуру БД (таблицы)

        def information_customers():
            cur.execute("""
            CREATE TABLE IF NOT EXISTS customers(
                id SERIAL PRIMARY KEY,
                name VARCHAR(60) NOT NULL,
                surname VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL UNIQUE
                );
            """)

        information_customers()


        def customers_phone():
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                customers_id INTEGER NOT NULL REFERENCES customers(id),
                phone TEXT
            );
            """)

        customers_phone()

# Функция ввода команд:

        def main():
            command = input("Введите команду, которую необходимо выполнить: \n add - добавить нового клиента; \n ap - "
                            "добавить телефон для существующего клиента; \n u - изменить данные о клиенте;  \n dp - "
                            "удалить телефон для существующего клиента; \n d - удалить существующего клиента; \n s - "
                            "найти существующего клиента \n")
            if command == "add":
                try:
                    id = int(input("Введите число(идентификатор) клиента: "))
                except:
                    print("Введено не число!")
                    return
                name = input("Введите имя клиента: ")
                surname = input("Введите фамилию клиента: ")
                email = input("Введите email клиента: ")
                phone = input("Введите телефон клиента: ")
                if phone:
                    phone = phone
                else:
                    phone = None
                if id and name and surname and email:
                    data_customers(cur, id=id, name=name, surname=surname, email=email, customers_id=id, phone=phone)
                else:
                    print("Введены не все необходимые данные")
            elif command == "ap":
                try:
                    id = int(input("Введите число(идентификатор) клиента: "))
                except:
                    print("Введено не число!")
                    return
                phone = input("Введите дополнительный телефон клиента: ")
                if id:
                    phone_add(cur, phone=phone, customers_id=id)
                else:
                    print("Введены не все необходимые данные")
            elif command == "u":
                try:
                    id = int(input("Введите число(идентификатор) клиента, данные у которого нужно изменить: "))
                except:
                    print("Введено не число!")
                    return
                name = input("Введите имя клиента: ")
                surname = input("Введите фамилию клиента: ")
                email = input("Введите email клиента: ")
                phone = input("Введите телефон клиента: ")
                if phone:
                    phone = phone
                else:
                    phone = None
                if id and name and surname and email:
                    customers_update(cur, id=id, name=name, surname=surname, email=email, id_update=id, customers_id=id, phone=phone)
                else:
                    print("Введены не все необходимые данные")
            elif command == "dp":
                try:
                    id = int(input("Введите число(идентификатор) клиента, у которого нужно удалить телефон: "))
                except:
                    print("Введено не число!")
                    return
                phone = input("Введите телефон клиента, который нужно удалить: ")
                if id and phone:
                    delete_phone(cur, customers_id=id, phone=phone)
                else:
                    print("Введены не все необходимые данные")
            elif command == "d":
                try:
                    id = int(input("Введите число(идентификатор) клиента, которого нужно удалить: "))
                except:
                    print("Введено не число!")
                    return
                if id:
                    customers_delete(cur, id=id, customers_id=id)
                else:
                    print("Введены не все необходимые данные")
            elif command == "s":
                name = input("Введите имя клиента или нажмите Enter для поиска по фамилии: ")
                if name:
                    name = name
                    customers_search(cur, name=name, surname=None, email=None, phone=None)
                    return
                surname = input("Введите фамилию клиента или нажмите Enter для поиска по email: ")
                if surname:
                    surname = surname
                    customers_search(cur, name=None, surname=surname, email=None, phone=None)
                    return
                email = input("Введите email клиента или нажмите Enter для поиска по номеру телефона: ")
                if email:
                    email = email
                    customers_search(cur, name=None, surname=None, email=email, phone=None)
                    return
                phone = input("Введите номер телефона клиента: ")
                if phone:
                    phone = phone
                    customers_search(cur, name=None, surname=None, email=None, phone=phone)
                    return
                else:
                    print("Нет данных для поиска")
            else:
                print("Введена некорректная команда!")

#2 Функция, позволяющая добавить нового клиента

        def data_customers(cur, id, name, surname, email, customers_id, phone=None):
            try:
                cur.execute("""
                INSERT INTO customers (id, name, surname, email) VALUES(%s, %s, %s, %s);
                """, (id, name, surname, email))
                cur.execute("""
                INSERT INTO phone (customers_id, phone) VALUES(%s, %s);
                """, (customers_id, phone))
                conn.commit()
                print("Данные нового клиента записаны")
            except:
                print("Такой id клиента уже существует!")

#3 Функция, позволяющая добавить телефон для существующего клиента

        def phone_add(cur, phone, customers_id):
            try:
                cur.execute("""
                INSERT INTO phone (customers_id, phone) VALUES(%s, %s);
                """, (customers_id, phone))
                conn.commit()
                print("Дополнительный телефон клиента записан")
            except:
                print("Такой id клиента не существует!")

#4 Функция, позволяющая изменить данные о клиенте

        def customers_update(cur, id, name, surname, email, id_update,  customers_id, phone=None):
            try:
                cur.execute("""
                    UPDATE customers SET id=%s, name=%s, surname=%s, email=%s WHERE id=%s;
                    """, (id, name, surname, email, id_update))
                cur.execute("""
                    DELETE FROM phone WHERE customers_id=%s;
                    """, (customers_id,))
                cur.execute("""
                    INSERT INTO phone (customers_id, phone) VALUES(%s, %s);
                    """, (customers_id, phone))
                conn.commit()
                print("Данные о клиенте изменены")
            except:
                print("Этого клиента не существует!")

#5 Функция, позволяющая удалить телефон для существующего клиента

        def delete_phone(cur, customers_id, phone):
                cur.execute("""
                SELECT * FROM phone WHERE customers_id=%s AND phone=%s;
                """, (customers_id, phone))
                if cur.fetchall():
                    cur.execute("""
                    DELETE FROM phone WHERE customers_id=%s AND phone=%s;
                    """, (customers_id, phone))
                    conn.commit()
                    print("Телефон клиента удален")
                else:
                    print("Этого клиента/телефона клиента не существует!")

#6 Функция, позволяющая удалить существующего клиента

        def customers_delete(cur, id, customers_id):
                cur.execute("""
                  SELECT * FROM customers WHERE id=%s;
                  """, (id,))
                if cur.fetchall():
                    cur.execute("""
                    DELETE FROM phone WHERE customers_id=%s;
                    """, (customers_id,))
                    cur.execute("""
                    DELETE FROM customers WHERE id=%s;
                    """, (id,))
                    conn.commit()
                    print("Данные клиента удалены")
                else:
                    print("Этого клиента не существует!")

#7 Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)

        def customers_search(cur, name=None, surname=None, email=None, phone=None):
                if name:
                    cur.execute("""
                    SELECT c.id, name, surname, email, p.phone FROM customers c
                    join phone p on c.id = p.customers_id
                    WHERE name = %s
                    GROUP BY c.id, name, surname, email, p.phone
                    LIMIT 1;
                    """, (name, ))
                elif surname:
                    cur.execute("""
                    SELECT c.id, name, surname, email, p.phone FROM customers c
                    join phone p on c.id = p.customers_id
                    WHERE surname = %s
                    GROUP BY c.id, name, surname, email, p.phone
                    LIMIT 1;
                    """, (surname,))
                elif email:
                    cur.execute("""
                    SELECT c.id, name, surname, email, p.phone FROM customers c
                    join phone p on c.id = p.customers_id
                    WHERE email = %s
                    GROUP BY c.id, name, surname, email, p.phone
                    LIMIT 1;
                    """, (email,))
                elif phone:
                    cur.execute("""
                    SELECT c.id, name, surname, email, p.phone FROM customers c
                    join phone p on c.id = p.customers_id
                    WHERE p.phone = %s
                    GROUP BY c.id, name, surname, email, p.phone
                    LIMIT 1;
                    """, (phone,))
                if cur.fetchall():
                    print("Данные клиента, id, имя, фамилия, email, телефон:", *list(cur.fetchall()))
                else:
                    print("Этого клиента не существует!")

        main()

conn.close()