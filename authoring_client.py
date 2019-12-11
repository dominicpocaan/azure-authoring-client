from reader import read_for_qna, read_for_luis

import threading



def qna(file_name):
	qna = read_for_qna(file_name)
	for q in qna:
		print(q)
		q.update()

def luis(file_name):
	luis = read_for_luis(file_name)
	for l in luis:
		print(l)
		l.update()

def main():
	file_name = input('File name: ')

	qna_thread = threading.Thread(target = qna(file_name))
	# luis_thread = threading.Thread(target = luis(file_name))

	qna_thread.start()
	# luis_thread.start()

	qna_thread.join()
	# luis_thread.join()

if __name__ == '__main__':
	main()