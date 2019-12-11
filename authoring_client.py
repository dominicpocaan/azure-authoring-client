from reader import read_for_qna, read_for_luis



def qna(file_name, dispatcher):
	qna = read_for_qna(file_name, dispatcher)
	for q in qna:
		print(q)
		q.update()

	return qna

def luis(file_name):
	luis = read_for_luis(file_name)
	for l in luis:
		print(l)
		l.update()

	return luis

def main():
	file_name = input('File name: ')
	dispatch_model = input('Dispatch model: ')

	qna_tasks = qna(file_name, dispatch_model)
	luis_tasks = luis(file_name)

	if len(qna_tasks) > 0:
		qna_tasks[0].publish()

	if len(luis_tasks) > 0:
		luis_tasks[0].publish()

if __name__ == '__main__':
	main()