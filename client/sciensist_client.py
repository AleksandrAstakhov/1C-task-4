import requests


class ScientistClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.current_experiment_id = None

    def start_experiment(self):
        response = requests.post(f"{self.server_url}/start_experiment")
        data = response.json()
        print(data)

    def list_clients(self):
        response = requests.get(f"{self.server_url}/clients")
        clients = response.json()
        print("Список участников:")
        for client_id, name in clients.items():
            print(f"{client_id}: {name}")

    def view_leaderboard(self):
        response = requests.get(f"{self.server_url}/leaderboard")
        leaderboard = response.json()
        print("Таблица лидеров:")
        for client_id, attempts in leaderboard.items():
            print(f"Участник {client_id}: {attempts} попыток")

    def run(self):
        while True:
            command = input(
                "Введите команду: \n 1) Начать эксперимент \n 2) Посмотреть список участников \n 3) посмотреть таблицу лидеров \n 4) Выйти: \n"
            )

            if command == "1":
                self.start_experiment()
            elif command == "2":
                self.list_clients()
            elif command == "3":
                self.view_leaderboard()
            elif command == "4":
                break
            else:
                print("Неверный ввод.")


if __name__ == "__main__":
    server_url = "http://localhost:5000"
    scientist = ScientistClient(server_url)
    scientist.run()
