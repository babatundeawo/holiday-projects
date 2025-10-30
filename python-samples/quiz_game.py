# quiz_game.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import time
import os

QUIZ_FILE = "sample_quiz.json"
SCORES_FILE = "scores.json"

SAMPLE = {
    "title":"General Knowledge",
    "questions":[
        {"q":"What is the capital of France?","choices":["Paris","London","Rome","Berlin"],"answer":0},
        {"q":"2 + 2 = ?","choices":["3","4","5","2"],"answer":1},
        {"q":"Which planet is known as the Red Planet?","choices":["Earth","Mars","Jupiter","Venus"],"answer":1}
    ]
}

def ensure_files():
    if not os.path.exists(QUIZ_FILE):
        with open(QUIZ_FILE,'w',encoding='utf-8') as f:
            json.dump(SAMPLE,f,indent=2)
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE,'w',encoding='utf-8') as f:
            json.dump([],f)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        ensure_files()
        self.load_quiz(QUIZ_FILE)
        self.current = 0
        self.score = 0
        self.time_per_question = 20
        self.time_left = self.time_per_question
        self.timer_id = None
        self.build_ui()

    def load_quiz(self, path):
        with open(path,'r',encoding='utf-8') as f:
            self.quiz = json.load(f)

    def build_ui(self):
        frm = ttk.Frame(self.root,padding=10)
        frm.pack(fill='both',expand=True)

        ttk.Label(frm, text=self.quiz.get("title","Quiz"), font=("Helvetica",16)).pack()
        self.q_label = ttk.Label(frm, text="", wraplength=500)
        self.q_label.pack(pady=8)

        self.choice_var = tk.IntVar(value=-1)
        self.choices_frame = ttk.Frame(frm)
        self.choices_frame.pack(fill='x')
        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.choices_frame, text="", variable=self.choice_var, value=i)
            rb.pack(anchor='w', pady=2)
            self.radio_buttons.append(rb)

        self.status = ttk.Label(frm, text="")
        self.status.pack(pady=6)
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill='x')
        ttk.Button(btn_frame, text="Start", command=self.start).pack(side='left')
        ttk.Button(btn_frame, text="Load Quiz", command=self.load_file).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Leaderboard", command=self.show_leaderboard).pack(side='right')

    def start(self):
        self.current = 0
        self.score = 0
        self.next_question()

    def next_question(self):
        if self.current >= len(self.quiz['questions']):
            self.end_quiz()
            return
        q = self.quiz['questions'][self.current]
        self.q_label.config(text=f"Q{self.current+1}: {q['q']}")
        self.choice_var.set(-1)
        for i,choice in enumerate(q['choices']):
            self.radio_buttons[i].config(text=choice, state='normal')
        for j in range(len(q['choices']),4):
            self.radio_buttons[j].config(text="", state='disabled')
        self.time_left = self.time_per_question
        self.update_timer()

    def update_timer(self):
        self.status.config(text=f"Time left: {self.time_left}s  |  Score: {self.score}")
        if self.time_left <= 0:
            self.record_answer(None)
            return
        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def record_answer(self, choice=None):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        q = self.quiz['questions'][self.current]
        chosen = self.choice_var.get()
        correct = q['answer']
        if chosen == correct:
            self.score += 1
        self.current += 1
        self.next_question()

    def end_quiz(self):
        name = simpledialog.askstring("Your name", "Enter your name for the leaderboard:") or "Anonymous"
        self.save_score(name, self.score)
        messagebox.showinfo("Quiz Finished", f"Your score: {self.score}/{len(self.quiz['questions'])}")
        self.status.config(text="Finished")

    def save_score(self, name, score):
        with open(SCORES_FILE,'r',encoding='utf-8') as f:
            scores = json.load(f)
        scores.append({"name":name,"score":score,"time":time.time()})
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:20]
        with open(SCORES_FILE,'w',encoding='utf-8') as f:
            json.dump(scores,f,indent=2)

    def show_leaderboard(self):
        with open(SCORES_FILE,'r',encoding='utf-8') as f:
            scores = json.load(f)
        lines = [f"{i+1}. {s['name']} — {s['score']}" for i,s in enumerate(scores)]
        messagebox.showinfo("Leaderboard", "\n".join(lines) if lines else "No scores yet.")

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if not path:
            return
        try:
            self.load_quiz(path)
            messagebox.showinfo("Loaded", "Quiz loaded successfully. Click Start.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load quiz: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
