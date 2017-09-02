from question.models import Q_INTEGER
from paper.models import PM_YES

def evaluate_answer(paper, question, answer):

	if question.question_type == Q_INTEGER:
		if answer.int_answer == question.int_answer:
			return question.marks_positive
		else:
			return question.marks_negative

	else:
		submitted_answer = answer.answer_array
		actual_answer = [option[0] for option in options if option[1] == '1']
		num_correct = 0
		num_wrong = 0
		for option in submitted_answer:
			if option in actual_answer:
				num_correct += 1
			else:
				num_wrong += 1

		if num_wrong > 0:
			return question.marks_negative
		elif paper.partial_marking == PM_YES:
			return question.marks_positive * (num_correct / len(actual_answer))
		else:
			return question.marks_positive * (num_correct == len(actual_answer))
