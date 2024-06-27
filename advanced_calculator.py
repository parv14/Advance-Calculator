from simple_calculator import SimpleCalculator
from stack import Stack

class AdvancedCalculator(SimpleCalculator):
	def __init__(self):
		"""
		Call super().__init__()
		Instantiate any additional data attributes
		"""
		super().__init__()

	def evaluate_expression(self, input_expression):
		"""
		Evaluate the input expression and return the output as a float
		Return a string "Error" if the expression is invalid
		"""
		tokens = self.tokenize(input_expression)
		if not self.check_brackets(tokens):
			return "Error"
		

		
		result = self.evaluate_list_tokens(tokens)
		self.history.insert(0, (input_expression, result))
		return result


	def tokenize(self, input_expression):
		"""
		convert the input string expression to tokens, and return this list
		Each token is either an integer operand or a character operator or bracket
		"""
		tokens = []
		current_token = ""
		for char in input_expression:
			if char.isdigit() or char == '.':
				current_token += char
			elif char in ['+', '-', '*', '/', '(', ')','{','}']:
				if current_token:
					tokens.append(int(current_token))
					current_token = ""
				tokens.append(char)
		if current_token:
			try:
				tokens.append(int(current_token))
			except:
				tokens.append(current_token)

		return tokens
            	

	def check_brackets(self, list_tokens):
		"""
		check if brackets are valid, that is, all open brackets are closed by the same type 
		of brackets. Also () contain only () brackets.
		Return True if brackets are valid, False otherwise
		"""
		stack = Stack()
		curl=0
		s=0
		for token in list_tokens:
			if token in ['(', '{']:
				stack.push(token)
				if token=='{':
					curl = 1
				if token == '(' and curl==1:
					s=1
			elif token in [')', '}']:
				if stack.is_empty():
					return False
				opening_bracket = stack.pop()
				if (token == ')' and opening_bracket != '(') or (token == '}' and opening_bracket != '{'):
					return False
				if token == '}' and s==0:
					return False

		return stack.is_empty()

	def evaluate_list_tokens(self, list_tokens):
		"""
		Evaluate the expression passed as a list of tokens
		Return the final answer as a float, and "Error" in case of division by zero and other errors
		"""
		for i in range(len(list_tokens)):
			if list_tokens[i] == '{':
				list_tokens[i] = '('
			if list_tokens[i] == '}':
				list_tokens[i] = ')'
		while True:
			if "(" in list_tokens:
				i = list_tokens.index("(")
				c=1
				for j in range(c+1,len(list_tokens)):
					if list_tokens[j]=="(":
						i=j
					if list_tokens[j]==")":
						res=list_tokens[i+1:j]
						res1 = self.evaluate_list_tokens(res)
						if res1=="Error":
							return res1
						list_tokens[:] = list_tokens[:i]+[str(res1)]+list_tokens[j+1:]
						break
			else:
				break
		stack = Stack()
		alpha = {'*': lambda x, y: x*y,
						'/': lambda x, y: x/y}
		operators = {'+': lambda x, y: x+y,
						'-': lambda x, y: x-y}
		if not (str(list_tokens[-1]).isdigit() or '.' in list_tokens[-1]):
			return "Error"
		i=0
		while i<(len(list_tokens)-2):
			if (str(list_tokens[i]).isdigit() or '.' in list_tokens[i]) and (list_tokens[i+1]=="*" or list_tokens[i+1]=="/"):
				try:
					result = alpha[list_tokens[i+1]](float(list_tokens[i]), float(list_tokens[i+2]))
					del list_tokens[i+2]
					del list_tokens[i+1]
					list_tokens[i]=str(result)
					i-=1
				except ZeroDivisionError:
					return "Error"		
			i+=1

		i=0
		while i<(len(list_tokens)):
			if str(list_tokens[i]).isdigit() or '.' in list_tokens[i]:
				stack.push(float(list_tokens[i]))
			elif list_tokens[i] in operators:
				if len(stack) < 1:
					return "Error"
				b= float(list_tokens[i+1])
				a= stack.pop()
				result = operators[list_tokens[i]](a, b)
				stack.push(result)
				i+=1
			else:
				return "Error"
			i+=1

		if len(stack) == 1:
			return stack.pop()
		else:
			return "Error"

	def get_history(self):
		"""
		Return history of expressions evaluated as a list of (expression, output) tuples
		The order is such that the most recently evaluated expression appears first 
		"""
		return self.history
