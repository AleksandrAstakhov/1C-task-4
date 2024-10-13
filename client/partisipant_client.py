import requests


class ScientistClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.current_experiment_id = None

    def register(self, name):
        response = requests.post(
            f"{self.server_url}/register_client", json={"name": name}
        ).json()
        self.client_id = int(response["id"])

    def guess(self):
        guess = int(input("предположите число "))
        response = requests.post(
            f"{self.server_url}/check_guess",
            json={"guess": guess, "client_id": self.client_id},
        ).json()
        print(response["result"])

    def wait(self):
        while True:
            response = requests.get(f"{self.server_url}/experiment_started").json()
            response = response["started"]
            if response:
                return

    def get_history(self):
        response = requests.post(
            f"{self.server_url}/get_history", json={"client_id": self.client_id}
        ).json()
        print(response["guesses"])

    def end(self):
        response =  requests.post(f"{self.server_url}/end", json={"clinet_id" : self.client_id}).json()

    def run(self):
        name = input("Введите имя: ")
        self.register(name)
        print("Ожидайте начала эксперимента")
        self.wait()
        print("эксперимент начался")

        while True:
            command = input(
                "Введите команду: \n 1) предположить число \n 2) получить свою историю запросов \n 3) завершить участие \n"
            )

            if command == "1":
                self.guess()
            elif command == "2":
                self.get_history()
            elif command == "3":
                self.end()
                break
            else:
                print("неверный ввод")


if __name__ == "__main__":
    server_url = "http://localhost:5000"
    scientist = ScientistClient(server_url)
    scientist.run()
