#!/usr/bin/python2
#-*- coding: UTF-8 -*-

from threading import Thread
from Queue import Queue
from random import randint
from copy import deepcopy

class CMainAI(Thread):

	def __init__(self, field):

		Thread.__init__(self)

		self.field = field.field
		self.width = field.width
		self.height = field.height
		self.man = field.man
		self.computer = field.computer
		self.queue = Queue()

	def run(self):

		self.queue.put(self.turn())

	def score(self, cv, cu, field):

		s = 0

		for v in range(0, self.height):

			for u in range(0, self.width):

				mult = 1 if field[v][u] == self.computer else -1

				if field[v][u] != None:

					ts = 0

					if self.width - u > 1 and field[v][u] == field[v][u + 1]:
						
						if self.width - u > 2 and field[v][u] == field[v][u + 2]:
							
							if self.width - u > 3 and field[v][u] == field[v][u + 3]:
								
								if self.width - u > 4 and field[v][u] == field[v][u + 4]: ts += 10000
								elif self.width - u > 4 and field[v][u + 4] == None: ts += 1000

							elif self.width - u > 3 and field[v][u + 3] == None: ts += 100

						elif self.width - u > 2 and field[v][u + 2] == None: ts += 50

					elif self.width - u > 1 and field[v][u + 1] == None: ts += 10

					s += ts * mult

					############################################################################ 

					ts = 0

					if self.height - v > 1 and field[v][u] == field[v + 1][u]:
						
						if self.height - v > 2 and field[v][u] == field[v + 2][u]:
							
							if self.height - v > 3 and field[v][u] == field[v + 3][u]:
								
								if self.height - v > 4 and field[v][u] == field[v + 4][u]: ts += 10000
								elif self.height - v > 4 and field[v + 4][u] == None: ts += 1000

							elif self.height - v > 3 and field[v + 3][u] == None: ts += 100

						elif self.height - v > 2 and field[v + 2][u] == None: ts += 50

					elif self.height - v > 1 and field[v + 1][u] == None: ts += 10

					s += ts * mult

					############################################################################ 

					ts = 0

					if self.height - v > 1 and self.width - u > 1 and field[v][u] == field[v + 1][u + 1]:
						
						if self.height - v > 2 and self.width - u > 2 and field[v][u] == field[v + 2][u + 2]:
							
							if self.height - v > 3 and self.width - u > 3 and field[v][u] == field[v + 3][u + 3]:
								
								if self.height - v > 4 and self.width - u > 4 and field[v][u] == field[v + 4][u + 4]: ts += 10000
								elif self.height - v > 4 and self.width - u > 4 and field[v + 4][u + 4] == None: ts += 1000

							elif self.height - v > 3 and self.width - u > 3 and field[v + 3][u + 3] == None: ts += 100

						elif self.height - v > 2 and self.width - u > 2 and field[v + 2][u + 2] == None: ts += 50

					elif self.height - v > 1 and self.width - u > 1 and field[v + 1][u + 1] == None: ts += 10

					s += ts * mult

					############################################################################ 

					ts = 0

					if self.height - v > 1 and u > 0 and field[v][u] == field[v + 1][u - 1]:
						
						if self.height - v > 2 and u > 1 and field[v][u] == field[v + 2][u - 2]:
							
							if self.height - v > 3 and u > 2 and field[v][u] == field[v + 3][u - 3]:
								
								if self.height - v > 4 and u > 3 and field[v][u] == field[v + 4][u - 4]: ts += 10000
								elif self.height - v > 4 and u > 3 and field[v + 4][u - 4] == None: ts += 1000

							elif self.height - v > 3 and u > 2 and field[v + 3][u - 3] == None: ts += 100

						elif self.height - v > 2 and u > 1 and field[v + 2][u - 2] == None: ts += 50

					elif self.height - v > 1 and u > 0 and field[v + 1][u - 1] == None: ts += 10

					s += ts * mult

					############################################################################ 

					ts = 0
					size = 5

					for tv in range(v - size if v >= size else 0, v + size if v + size < self.height else self.height - 1):
						
						for tu in range(u - size if u >= size else 0, u + size if u + size < self.width else self.width - 1):

							ts += 1

					s += ts * mult

		return s

############################################################################
# Случайный ход (алгоритм, используемый для отладки приложения)

class CRandomAI(CMainAI):

	def __init__(self, field):

		CMainAI.__init__(self, field)

	def turn(self):

		all_cell = []

		for u in range(0, self.height):

			for v in range(0, self.width):

				if self.field[u][v] == None: all_cell.append((u, v))

		return all_cell[randint(0, len(all_cell) - 1)]

############################################################################ 
# Мини - макс

class CMinMaxAI(CMainAI):

	def __init__(self, field):

		CMainAI.__init__(self, field)

	def turn(self):

		def step(cv, cu, nxt, field, depth):

			if depth == 0: return (self.score(cv, cu, field), 0, 0)
			
			best = float("-inf")
			best_v = -1
			best_u = -1
			range_v = range(self.height / 2, self.height) + range(0, self.height / 2)
			range_u = range(self.width / 2, self.width) + range(0, self.width / 2)

			for v in range_v:

				for u in range_u:

					if field[v][u] == None:

						field[v][u] = nxt
						(current, _, _) = step(v, u, self.computer if nxt == self.man else self.man, field, depth - 1)
						current = - current
						field[v][u] = None

						if current > best: best, best_v, best_u = current, v, u

			return (best, best_v, best_u)

		(_, v, u) = step(self.height / 2, self.width / 2, self.computer, deepcopy(self.field), 2)

		return (v, u)

############################################################################ 
# Альфа - бета - отсечение

class CAlphaBetaAI(CMainAI):

	def __init__(self, field):

		CMainAI.__init__(self, field)

	def turn(self):

		def step(cv, cu, nxt, field, depth, alpha, beta):

			if depth == 0: return (self.score(cv, cu, field), 0, 0)
			
			best = alpha
			best_v = -1
			best_u = -1
			range_v = range(self.height / 2, self.height) + range(0, self.height / 2)
			range_u = range(self.width / 2, self.width) + range(0, self.width / 2)

			try:

				for v in range_v:

					for u in range_u:

						if field[v][u] == None:

							field[v][u] = nxt
							(current, _, _) = step(v, u, self.computer if nxt == self.man else self.man, field, depth - 1, - beta, - best)
							current = - current
							field[v][u] = None

							if current > best:

								best = current
								best_v = v
								best_u = u

								if best >= beta: raise

			except:

				pass

			return (best, best_v, best_u)

		(_, v, u) = step(self.height / 2, self.width / 2, self.computer, deepcopy(self.field), 2, float("-inf"), float("inf"))

		return (v, u)

############################################################################ 
# Метод ветвей и границ

class CBBAI(CMainAI):

	def __init__(self, field):

		CMainAI.__init__(self, field)

	def turn(self):

		def step(cv, cu, nxt, field, depth, bound):

			if depth == 0: return (self.score(cv, cu, field), 0, 0)
			
			best = float("-inf")
			best_v = -1
			best_u = -1
			range_v = range(self.height / 2, self.height) + range(0, self.height / 2)
			range_u = range(self.width / 2, self.width) + range(0, self.width / 2)

			try:

				for v in range_v:

					for u in range_u:

						if field[v][u] == None:

							field[v][u] = nxt
							(current, _, _) = step(v, u, self.computer if nxt == self.man else self.man, field, depth - 1, - best)
							current = - current
							field[v][u] = None

							if current > best:

								best = current
								best_v = v
								best_u = u

								if best >= bound: raise

			except:

				pass

			return (best, best_v, best_u)

		(_, v, u) = step(self.height / 2, self.width / 2, self.computer, deepcopy(self.field), 2, float("inf"))

		return (v, u)

#############################################################################

class CAI():

	def __init__(self, field, ai_algo_index):

		self.field = field
		self.ai = None
		self.ai_algo_index = ai_algo_index

	def turn(self):

		if self.ai_algo_index == 0: self.ai = CRandomAI(self.field)
		elif self.ai_algo_index == 1: self.ai = CMinMaxAI(self.field)
		elif self.ai_algo_index == 2: self.ai = CAlphaBetaAI(self.field)
		elif self.ai_algo_index == 3: self.ai = CBBAI(self.field)
		else: pass # TODO

		self.ai.start()

	def is_alive(self):

		return self.ai.is_alive()

	def result(self):

		return self.ai.queue.get()

