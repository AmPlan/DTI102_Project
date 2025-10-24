import random
import operator

# ฟังก์ชันสร้างคำถาม (ไม่มีการเปลี่ยนแปลง)
def random_question():
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul
    }
    first_num = random.randint(1, 10)
    second_num = random.randint(1, 10)
    third_num = random.randint(1, 10)

    operation_symbol1 = random.choice(list(operators.keys()))
    operation_func1 = operators.get(operation_symbol1)
    operation_symbol2 = random.choice(list(operators.keys()))
    operation_func2 = operators.get(operation_symbol2)
    result_step1 = operation_func1(first_num, second_num)
    answer = operation_func2(result_step1, third_num)

    question_str = f"{first_num} {operation_symbol1} {second_num} {operation_symbol2} {third_num} = ?"
    return question_str, answer

def ask_question():
    question_str, correct_answer = random_question()
    print("\n" + question_str)

    wrong_choices = set()

    while len(wrong_choices) < 3:
        
        deviation = random.randint(-10, 10)
        if deviation == 0:
            continue  
            
        wrong_choice = correct_answer + deviation
        
        if wrong_choice != correct_answer and wrong_choice not in wrong_choices:
            wrong_choices.add(wrong_choice)
    choices = list(wrong_choices)
    choices.append(correct_answer)
    
    random.shuffle(choices)
    choice_labels = ["A", "B", "C", "D"]
    
    print("-------------------------")
    for label, choice in zip(choice_labels, choices):
        print(f"({label}) {choice}")
    print("-------------------------")

    while True:
        guess_label = input("Enter your choice (A, B, C, D): ").upper()
        if guess_label in choice_labels:
            guess_index = choice_labels.index(guess_label) 
            guess_answer = choices[guess_index] 
            break
        else:
            print("Invalid input. Please enter A, B, C, or D.")
    
    return guess_answer == correct_answer
def game():
    score = 0
    while True:
        if ask_question() == True:
            score += 1
            print("Correct!")
        else:
            print("False!")
            break 
    print(f"\n======== GAME OVER ========")
    print(f"Your final score is **{score}**")
    print("Keep going!!")

game()