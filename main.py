import pandas


def create_csv():
    every_word = []
    with open("Data/data.txt", "r") as file:
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

    print(english_words, german_words, english_description)

    #TODO: Create Pandas Dataframe / CSV File from the three lists


create_csv()