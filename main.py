import pandas
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "jdfjsnfksdj"
Bootstrap5(app)


def create_dataframe(file_path):
    every_word = []
    with open(f"{file_path}", "r") as file:
        for line in file:
            every_word.append(line.strip())

    def create_list(start, list):
        index = start
        new_list = []
        loop_amount = int(len(list) / 3 - 1)
        for element in range(loop_amount):
            new_list.append(list[index])
            index += 3
        return new_list

    english_words = create_list(0, every_word)
    german_words = create_list(1, every_word)
    english_description = create_list(2, every_word)

    dict = {
        "english_word": english_words,
        "german_word": german_words,
        "english_desription": english_description
    }

    df = pandas.DataFrame(dict)
    return df


class LernkartenBot():

    def __init__(self):
        self.df = create_dataframe("Data/page1.txt")
        self.order = self.create_order()
        self.language_direction = 2

        self.order_index = 0
        self.order_index_value = self.order[self.order_index]

        self.current_vocab = self.get_vocab()

    def create_order(self):
        row_amount = self.df.shape[0]
        order = []
        while len(order) != (row_amount):
            rand_numb = random.randint(0, row_amount - 1)
            if rand_numb not in order:
                order.append(rand_numb)
            else:
                pass
        print(f"Order created {order}")
        return order

    def get_vocab(self):
        row = self.df.iloc[self.order_index_value]
        dict_list = [{col: row[col]} for col in self.df.columns]
        return dict_list

    def convert_dictlist_to_html_format(self):
        vocab = self.current_vocab
        if self.language_direction == 2:
            random_part = vocab[random.randint(0, 1)]
        else:
            random_part = vocab[self.language_direction]
        front_vocab = list(random_part.values())[0]

        back_vocab = vocab.copy()
        back_vocab.remove(random_part)

        back_one_name = list(back_vocab[0].keys())[0]
        back_one_value = list(back_vocab[0].values())[0]

        back_two_name = list(back_vocab[1].keys())[0]
        back_two_value = list(back_vocab[1].values())[0]

        dict = {
            "front_vocab": front_vocab,
            "back_vocabs": {
                "one": {
                    "name": back_one_name,
                    "value": back_one_value
                },
                "two": {
                    "name": back_two_name,
                    "value": back_two_value
                }

            }
        }
        return dict

    def next_vocab(self):
        print(f"Current Index: {self.order_index}")
        try:
            self.order_index += 1
            self.order_index_value = self.order[self.order_index]
            self.current_vocab = bot.get_vocab()
        except IndexError:
            self.current_vocab = [{"Ende Vokabeln": "Ende Vokabeln"}, {"Ende Vokabeln": "Ende Vokabeln"},
                                  {"Ende Vokabeln": "Ende Vokabeln"}]
            self.order_index -= 1

    def previous_vocab(self):
        print(f"Current Index: {self.order_index}")
        try:
            self.order_index -= 1
            self.order_index_value = self.order[self.order_index]
            self.current_vocab = bot.get_vocab()
        except IndexError:
            self.current_vocab = [{"Ende Vokabeln": "Ende Vokabeln"}, {"Ende Vokabeln": "Ende Vokabeln"},
                                  {"Ende Vokabeln": "Ende Vokabeln"}]
            self.order_index += 1

    def change_vocab(self, pageindex):
        self.df = create_dataframe(f"Data/page{pageindex}.txt")
        self.order_index = 0
        self.order_index_value = self.order[self.order_index]
        self.current_vocab = self.get_vocab()



bot = LernkartenBot()
print("\n")


@app.route("/")
def home():
    data = bot.convert_dictlist_to_html_format()
    return render_template("index.html", data=data)


@app.route("/next")
def next_():
    bot.next_vocab()
    return redirect(url_for("home"))


@app.route("/previous")
def previous():
    bot.previous_vocab()
    return redirect(url_for("home"))

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == 'POST':
        selected_page = request.form.get('vocab_page')
        selected_language = request.form.get("language")
        bot.language_direction = int(selected_language)
        bot.change_vocab(selected_page)
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5003)
