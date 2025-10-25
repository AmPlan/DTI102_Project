import random
import operator
import time 

TIME_PER_QUESTION = 10 

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

def ask_question(question_number):
    question_str, correct_answer = random_question()
    print(f"\n--- Question {question_number} of 20 ---") 
    print(f"**Time limit: {TIME_PER_QUESTION} seconds!**")
    print(question_str)

    wrong_choices = set()
    while len(wrong_choices) < 3:
        deviation = random.randint(-10, 10)
        if deviation == 0: continue 
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

    start_time = time.time()
    guess_label = None

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = TIME_PER_QUESTION - elapsed_time

        if remaining_time <= 0:
            print(f"\nTime's up! The correct answer was {correct_answer}.")
            return False
        try:
             guess_label = input(f"Enter your choice (A, B, C, D) ({remaining_time:.1f}s left): ").upper()
             
             if guess_label in choice_labels:
                 guess_index = choice_labels.index(guess_label) 
                 guess_answer = choices[guess_index] 
                 break
             else:
                 print("Please enter A, B, C, or D")
        except:
             pass

    end_time = time.time()
    time_taken = end_time - start_time

    if time_taken > TIME_PER_QUESTION:
        print(f"\nToo late! You took {time_taken:.2f} seconds. The time limit was {TIME_PER_QUESTION}s.")
        return False

    if guess_answer == correct_answer:
        print(f"Time taken: {time_taken:.2f} seconds.")
    
    return guess_answer == correct_answer
    
def game():
    score = 0
    total_questions = 20
    print(f"Welcome! Get ready for {total_questions} math questions!")

    for i in range(1, total_questions + 1):
        if ask_question(i) == True: 
            score += 1
            print("Correct!")
        else:
            print("False!") 
    print(f"\n======== GAME OVER ========")
    print(f"You answered {total_questions} questions.")
    print(f"Your final score is **{score}/{total_questions}**")
    
    if score == total_questions:
         print("Perfect Score! You are a Math Genius!")
    elif score >= total_questions * 0.75:
         print("Excellent work!")
    else:
         print("Keep going!!!")

game()