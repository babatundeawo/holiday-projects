"""
Grade Analyzer Project
----------------------
This program reads a list of students' grades from a file or user input,
calculates their average scores, assigns letter grades, and provides
a class performance summary.
"""

# Function to calculate letter grade
def get_letter_grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    else:
        return "F"

# Function to calculate average score
def calculate_average(grades):
    return sum(grades) / len(grades)

# Function to analyze grades
def analyze_grades(students):
    print("===== GRADE ANALYSIS REPORT =====")
    total_scores = []
    for name, scores in students.items():
        avg = calculate_average(scores)
        letter = get_letter_grade(avg)
        total_scores.append(avg)
        print(f"\nStudent: {name}")
        print(f"Scores: {scores}")
        print(f"Average: {avg:.2f}")
        print(f"Letter Grade: {letter}")
    
    class_avg = calculate_average(total_scores)
    print("\n===== CLASS SUMMARY =====")
    print(f"Class Average: {class_avg:.2f}")
    print(f"Highest Average: {max(total_scores):.2f}")
    print(f"Lowest Average: {min(total_scores):.2f}")

# Option 1: Load grades manually
def manual_input_mode():
    students = {}
    num_students = int(input("Enter number of students: "))
    for _ in range(num_students):
        name = input("\nEnter student name: ")
        scores = list(map(float, input("Enter grades separated by spaces: ").split()))
        students[name] = scores
    analyze_grades(students)

# Option 2: Load from file
def file_input_mode(filename):
    students = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            name = parts[0]
            scores = list(map(float, parts[1:]))
            students[name] = scores
    analyze_grades(students)

# Main Program
if __name__ == "__main__":
    print("===== GRADE ANALYZER =====")
    print("1. Enter grades manually")
    print("2. Load grades from file (CSV format)")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        manual_input_mode()
    elif choice == "2":
        filename = input("Enter the CSV filename (e.g., grades.csv): ")
        file_input_mode(filename)
    else:
        print("Invalid choice. Exiting program.")
