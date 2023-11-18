import tkinter as tk
import socket
import threading

hair_count = 0
coin_count = 0
clicks_by_user = 0
achieved_first_coin = False

def open_game(ip, port, nickname):
    def update_counter():
        global hair_count, coin_count, clicks_by_user, achieved_first_coin
        hair_count += 1
        clicks_by_user += 1
        label_hair.config(text=f'У чея вырвали {hair_count} волосиков')
        if clicks_by_user % 10 == 0:
            coin_count += 1
            label_coins.config(text=f'Монеты: {coin_count}')
            if coin_count == 1 and not achieved_first_coin:
                client_socket.send(f"Chat: Игрок {nickname} получил достижение - Первые деньги!")
                achieved_first_coin = True
        send_click()

    def send_click():
        client_socket.send("Clicked".encode())

    def send_message(event=None):
        message = entry.get()
        entry.delete(0, tk.END)
        client_socket.send(f"Chat: {nickname}: {message}".encode())

    def receive():
        global hair_count, coin_count
        while True:
            try:
                data = client_socket.recv(1024)
                message = data.decode()
                if message.startswith('Hair count'):
                    hair_count = int(message.split(": ")[1])
                    label_hair.config(text=f'У чея вырвали {hair_count} волосиков')
                elif message.startswith('Chat:'):
                    chat_list.insert(tk.END, message[5:])
            except:
                root.deiconify()
                break

    root = tk.Toplevel(main_window)
    root.title('Многопользовательская игра')

    label_hair = tk.Label(root, text=f'У чея вырвали 0 волосиков', font=('Arial', 18))
    label_hair.pack(pady=20)

    label_coins = tk.Label(root, text='Монеты: 0', font=('Arial', 14))
    label_coins.pack()

    button = tk.Button(root, text='Вырвать волосик', command=update_counter, font=('Arial', 14))
    button.pack(padx=10, pady=10)

    entry = tk.Entry(root, width=40)
    entry.pack(pady=10)
    entry.bind("<Return>", send_message)

    chat_list = tk.Listbox(root, width=60)
    chat_list.pack(padx=10, pady=10)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((ip, port))
        client_socket.send("GetCount".encode())
        client_socket.send(f"Chat: {nickname} присоединился к игре".encode())
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        main_window.withdraw()
    except Exception as e:
        print(e)
        root.destroy()

def connect_to_server():
    ip = ip_entry.get()
    port = int(port_entry.get())
    nickname = nickname_entry.get()  # Получаем введенный никнейм
    open_game(ip, port, nickname)   # Передаем никнейм в функцию open_game()

main_window = tk.Tk()
main_window.title('Главное меню')

ip_label = tk.Label(main_window, text='IP сервера:')
ip_label.pack()
ip_entry = tk.Entry(main_window)
ip_entry.pack()

port_label = tk.Label(main_window, text='Порт:')
port_label.pack()
port_entry = tk.Entry(main_window)
port_entry.pack()

nickname_label = tk.Label(main_window, text='Введите ваш никнейм:')
nickname_label.pack()
nickname_entry = tk.Entry(main_window)
nickname_entry.pack()

connect_button = tk.Button(main_window, text='Подключиться', command=connect_to_server, font=('Arial', 12))
connect_button.pack(pady=10)

main_window.mainloop()
