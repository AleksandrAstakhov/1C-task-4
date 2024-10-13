from flask import Flask, request, jsonify
import random

app = Flask(__name__)


class InMemoryDatabase:
    def __init__(self):
        self.clients = {}
        self.experiments = {}
        self.leaderboard = {}
        self.experiment_started = False

    def add_client(self, client_id, name):
        self.clients[client_id] = {"name": name, "guesses": []}
        self.leaderboard[client_id] = 0

    def remove_client(self, client_id):
        if client_id in self.clients:
            del self.clients[client_id]
            del self.leaderboard[client_id]

    def add_guess(self, client_id, guess):
        if client_id in self.clients:
            self.clients[client_id]["guesses"].append(guess)
            self.leaderboard[client_id] += 1

    def get_clients(self):
        return {client_id: data["name"] for client_id, data in self.clients.items()}
    
    def get_experiment(self, experiment_id):
        return self.experiments.get(experiment_id, None)

    def start_experiment(self):
        self.experiment_started = True
        secret_number = random.randint(1, 100)
        experiment_id = len(self.experiments) + 1
        self.experiments[experiment_id] = {"secret_number": secret_number}
        return secret_number, experiment_id

    def get_leaderboard(self):
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1])
        return {client_id: attempts for client_id, attempts in sorted_leaderboard}


database = InMemoryDatabase()


@app.route("/register_client", methods=["POST"])
def register_client():
    name = request.json["name"]
    client_id = len(database.clients) + 1
    database.add_client(client_id, name)
    return jsonify({"message": "Клиент зарегистрирован", "id": client_id})


@app.route("/start_experiment", methods=["POST"])
def initiate_experiment():
    database.started_experiment = True
    secret_number, experiment_id = database.start_experiment()
    return jsonify(
        {
            "message": "Эксперимент начат.",
            "secret_number": secret_number,
            "experiment_id": experiment_id,
        }
    )


@app.route("/clients", methods=["GET"])
def list_clients():
    return jsonify(database.get_clients())


@app.route("/get_history", methods=["POST"])
def get_history():
    client_id = request.json["client_id"]
    return jsonify(database.clients[client_id])


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    leaderboard = database.get_leaderboard()
    return jsonify(leaderboard)


@app.route("/experiment_started", methods=["GET"])
def experiment_started():
    return jsonify({"started": database.experiment_started})

@app.route("/end", methods=["POST"])
def end():
    data = request.json
    return database.remove_client(data['client_id'])


@app.route("/check_guess", methods=["POST"])
def check_guess():
    data = request.json
    client_id = int(data["client_id"])
    guess = int(data["guess"])
    print(guess)

    experiment = database.get_experiment(len(database.experiments))
    if not experiment:
        return jsonify({"message": "Эксперимент не найден."}), 404

    secret_number = experiment["secret_number"]
    result = ""

    if guess < secret_number:
        result = "Ваше число меньше загаданного."
    elif guess > secret_number:
        result = "Ваше число больше загаданного."
    else:
        result = "Поздравляем! Вы угадали число."

    return jsonify({"client_id": client_id, "result": result})


if __name__ == "__main__":
    app.run(port=5000)
