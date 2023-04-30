import tkinter as tk
import os
import random
import time
import textwrap

FREESTYLE_LEN = 25
USUAL_LEN = 5

def get_content(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()
    return [sentence.strip() for sentence in content]

SENTENCES = {
    "easy": get_content("easy.txt"),
    "medium": get_content("medium.txt"),
    "hard": get_content("hard.txt"),
}

def get_freeride_content(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    return content.split()

def count_mistakes(expected_input, user_input):
    mistakes = 0
    for i in range(min(len(expected_input), len(user_input))):
        if expected_input[i] != user_input[i]:
            mistakes += 1
    mistakes += abs(len(expected_input) - len(user_input))
    return mistakes

def words_and_letters(sentences_list):
    total_words = 0
    total_letters = 0

    for sentence in sentences_list:
        words = sentence.split()
        total_words += len(words)
        total_letters += sum(len(word) for word in words)

    return total_words, total_letters

def freeride_mode():
    words = get_freeride_content("freeride.txt")
    return random.sample(words, FREESTYLE_LEN)

class TypingGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x600")
        self.root.configure(bg="salmon1")
        self.root.title("Typing Game")

        self.setup_level_selection()

        self.root.mainloop()

    def setup_level_selection(self):
        self.title_label = tk.Label(self.root, text="Выберите уровень сложности",
                                    bg="salmon1", fg="white", font=("Helvetica", 16))
        self.title_label.pack(anchor='center')

        for level in ["easy", "medium", "hard", "freeride"]:
            tk.Button(self.root, text=level, command=lambda level=level: self.start_game(level),
                      bg="salmon1", fg="white", font=("Helvetica", 16)).pack(anchor='center')

    def start_game(self, level):
        self.level = level

        for widget in self.root.winfo_children():
            widget.destroy()

        self.sentence_label = tk.Text(self.root, width=100, height=4, borderwidth=2, relief="solid",
                                      bg="salmon1", fg="white", font=("Helvetica", 18))
        self.sentence_label.tag_configure("center", justify='center')
        self.sentence_label.tag_configure("correct", background="green2")
        self.sentence_label.tag_configure("incorrect", background="red")
        self.sentence_label.config(state='disabled')
        
        self.sentence_label.pack(anchor='center')

        self.typing_entry = tk.Entry(self.root, font=("Helvetica", 16), width=100, bg='beige')
        self.typing_entry.bind('<Key>', self.update_entry)
        self.typing_entry.bind('<Return>', self.check_entry)
        self.typing_entry.pack(anchor='center')

        self.total_words = 0
        self.total_letters = 0
        self.mistakes = 0
        self.start_time = time.time()
        self.sentence_index = 0

        if self.level == "freeride":
            self.sentences = freeride_mode()
            self.total_words = len(self.sentences)
            for word in self.sentences:
                self.total_letters += len(word)
        else:
            self.sentences = random.sample(SENTENCES[self.level], USUAL_LEN)
            self.total_words, self.total_letters = words_and_letters(SENTENCES[self.level])

        self.next_sentence()

    def next_sentence(self):
        if self.sentence_index >= len(self.sentences):
            self.end_game()
            return
        self.typing_entry.delete(0, tk.END)
        self.sentence_label.config(state='normal')
        self.sentence_label.delete(1.0, tk.END)
        self.current_sentence = self.sentences[self.sentence_index]
        wrapped_sentence = textwrap.fill(self.current_sentence, 100)
        self.sentence_label.insert(tk.END, wrapped_sentence)
        self.sentence_label.config(state='disabled')
        self.sentence_index += 1

    def update_entry(self, event):
        if event.keysym in ["Return", "Shift_L", "Shift_R", "Control_L", "Control_R"]:
            return
        self.root.after_idle(self.update_highlight)

    def update_highlight(self):
        typed_text = self.typing_entry.get()
        self.sentence_label.config(state='normal')
        for i in range(min(len(typed_text), len(self.current_sentence))):
            if typed_text[i] == self.current_sentence[i]:
                self.sentence_label.tag_add("correct", f"1.0 + {i} chars", f"1.0 + {i+1} chars")
            else:
                self.sentence_label.tag_add("incorrect", f"1.0 + {i} chars", f"1.0 + {i+1} chars")
                self.mistakes += 1
        for tag in self.sentence_label.tag_names():
            self.sentence_label.tag_remove(tag, f"1.0 + {len(typed_text)} chars", tk.END)
        self.sentence_label.config(state='disabled')

    def check_entry(self, event):
        self.mistakes += count_mistakes(self.current_sentence, self.typing_entry.get())
        self.next_sentence()

    def end_game(self):
        elapsed_time = time.time() - self.start_time
        wpm = (self.total_words * 60) / elapsed_time
        lpm = (self.total_letters * 60) / elapsed_time
        result_text = f"""
        Время: {elapsed_time:.2f} секунд
        Слов в минуту: {wpm:.2f}
        Символов в минуту: {lpm:.2f}
        Количество ошибок: {self.mistakes}
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.title_label = tk.Label(self.root, text=result_text,
                                    bg="salmon1", fg="white", font=("Helvetica", 16))
        self.title_label.pack(anchor='center')

if __name__ == "__main__":
    TypingGame()