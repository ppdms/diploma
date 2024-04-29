import json
import genanki
import html
import random

def convert_data(data):
    categories = {}
    for question in data[3]["data"]:
        if question[3] != 1 or question[1] in [4, 5]:  # Skip non-Greek questions, and last two categories
            continue
        category_name = question[7].split(" ")[0]
        if category_name not in categories:
            categories[category_name] = []
        question_obj = {
            "QuestionCode": question[0],
            "QuestionText": question[4],
            "QuestionPhoto": question[5],
            "Answers": []
        }
        for answer in data[0]["data"]:
            if answer[0] == question[0]: # you will tell me this is inefficient, I will tell you I don't care
                question_obj["Answers"].append(answer[2])
                if answer[3]:
                    question_obj["CorrectAnswer"] = len(question_obj["Answers"]) - 1
        categories[category_name].append(question_obj)
    return categories

def generate_anki_deck(data, img_folder):
    # Define your model
    my_model = genanki.Model(
        random.randint(10**9, 10**10 - 1),
        'Κ.Ο.Κ',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])
    
    # Collect media files
    media_files = []

    # Create a set to store unique questions
    seen_questions = set()

    decks = []

    # Add notes to the deck
    for category, questions in data.items():
        deck = genanki.Deck(random.randint(10**9, 10**10 - 1), "Κ.Ο.Κ::"+category)
        decks.append(deck)
        for question in questions:
            # Generate the question text
            question_text = f"{html.escape(question['QuestionText'])}<ul>"
            for i, answer in enumerate(question['Answers']):
                question_text += f"<li>{i+1}. {html.escape(answer)}</li>"
            question_text += "</ul>"
            # Add the image if it exists
            if question['QuestionPhoto'] and question['QuestionPhoto'] != "0":
                img_path = f"{img_folder}/{question['QuestionPhoto']}.JPG"
                question_text += f"<img src=\"{question['QuestionPhoto']}.JPG\">"
                media_files.append(img_path)
            # Generate the answer text
            answer_text = f"<ul><li>{question['CorrectAnswer']+1}. {html.escape(question['Answers'][question['CorrectAnswer']])}</li></ul>"
            # Skip this question if we've seen it before. One has to wonder why this is happening, alas...
            # edit: I suspect it's because the same question is in multiple categories. thankfully, I don't care.
            if (question_text, answer_text) in seen_questions:
                continue
            seen_questions.add((question_text, answer_text))
            # Create a note with the question and answer and add it to the deck
            my_note = genanki.Note(
                model=my_model,
                fields=[question_text, answer_text])
            deck.add_note(my_note)

    # Create a package and add media files
    my_package = genanki.Package(decks)
    my_package.media_files = media_files

    # Save the deck to a file. Of course, this needs some cleaning up, but I will leave it up to you to do as you like.
    my_package.write_to_file('KOK.apkg')


if __name__ == "__main__":
    with open('ExerBase.json', 'r') as f:
        data = json.load(f)
    converted_data = convert_data(data)
    #with open('converted_data.json', 'w') as f:
    #    json.dump(converted_data, f, indent=4, ensure_ascii=False)
    generate_anki_deck(converted_data, "extracted")
