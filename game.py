#!/usr/bin/python2
#-*- coding: UTF-8 -*-

import pygame

class CField:

	def __init__(self, res, is_cross):

		self.res = res
		self.width = 10 # 33
		self.height = 10 # 21
		self.field = list(map(lambda _: list(map(lambda _: None, range(0, self.width))), range(0, self.height)))
		self.man = 1
		self.computer = -1
		self.win = []
		self.cell_size = (30, 30)
		self.base_point = (res.bmp["bg"].get_width() / 2 - self.width / 2 * self.cell_size[0], res.bmp["bg"].get_height() / 2 - self.height / 2 * self.cell_size[1]) # (20, 20)

		self.computer_chip = "cross" if is_cross else "null"
		self.man_chip = "null" if is_cross else "cross"

	def main_draw(self):

		self.res.scr.blit(self.res.bmp["bg"], self.res.rect["bg"])

		c_x, c_y = self.base_point
		c_x += self.cell_size[0]
		c_y += self.cell_size[1]

		for u in range(1, self.height):

			self.res.scr.blit(self.res.bmp["line"][0], pygame.Rect(self.base_point[0], c_y, self.res.rect["line"][0].width,
				self.res.rect["line"][0].height))

			c_y += self.cell_size[1]

		for v in range(1, self.width):

			self.res.scr.blit(self.res.bmp["line"][1], pygame.Rect(c_x, self.base_point[1], self.res.rect["line"][1].width,
				self.res.rect["line"][1].height))

			c_x += self.cell_size[0]

		c_y = self.base_point[1] + 13

		for u in range(0, self.height):

			c_x = self.base_point[0] + 11

			for v in range(0, self.width):

				if self.field[u][v]:

					name = "%s-small" % (self.man_chip if self.field[u][v] == self.man else self.computer_chip)
					self.res.scr.blit(self.res.bmp[name][1 if (u, v) in self.win else 0],
							pygame.Rect(c_x, c_y, self.res.rect["small"].width, self.res.rect["small"].height))

				c_x += self.cell_size[0]

			c_y += self.cell_size[1]

	def draw(self):

		self.main_draw()
		pygame.display.flip()

	def draw_winner_screen(self):

		if self.win == []: name = "none-winner"
		elif self.field[self.win[0][0]][self.win[0][1]] == self.computer: name = "computer-winner"
		else: name = "man-winner"

		self.res.scr.blit(self.res.bmp[name], self.res.rect[name])

	def man_turn(self, pos):

		u = (pos[1] - self.base_point[1]) / self.cell_size[1]
		v = (pos[0] - self.base_point[0]) / self.cell_size[0]
		
		if (u < 0) or (v < 0) or (u >= self.height) or (v >= self.width): return False

		if not self.field[u][v]:
	
			self.field[(pos[1] - self.base_point[1]) / self.cell_size[1]][(pos[0] - self.base_point[0]) / self.cell_size[0]] = self.man
			return True

		return False

	def computer_turn(self, comp):

		comp.turn()

		u = 0

		while comp.is_alive():
			
			self.main_draw()

			for v in range(0, u + 1):

				self.res.scr.blit(self.res.bmp["wait"][v], self.res.rect["wait"][v])

			pygame.display.flip()
			pygame.time.wait(200)

			u = (u + 1) % 5

		p = comp.result()
		self.field[p[0]][p[1]] = self.computer

		pygame.event.clear()

	def winner(self):

		current = None

		def begin():

			global current

			self.win = []
			current = None

		def body():
			
			global current

			# Отрицательные индексы в списках - странно, но все работает
			if (current == self.field[u][v]) and (current != None):
					
				self.win.append((u + (self.height if u < 0 else 0), v + (self.width if v < 0 else 0)))

			else:
					
				self.win = [(u + (self.height if u < 0 else 0), v + (self.width if v < 0 else 0))]
				current = self.field[u][v]

			return len(self.win) == 5

		def end():

			return len(self.win) == 5

		############################################################################ 
		# Проверка на ничью

		begin()

		if not any(None in tf for tf in self.field): return True

		############################################################################ 
		# Вертикали

		for u in range(0, self.height):

			begin()

			for v in range(0, self.width):
				
				if body(): break

			if end(): break

		if len(self.win) == 5: return True

		############################################################################ 
		# Горизонтали

		for v in range(0, self.width):

			begin()
			
			for u in range(0, self.height):

				if body(): break

			if end(): break

		if len(self.win) == 5: return True

		############################################################################ 
		# Диагонали

		for tv in range(- self.width, self.width):

			begin()

			for (v, u) in zip(range(tv, self.width), range(0, self.height)):

				if body(): break

			if end(): break

			begin()

			for (v, u) in zip(range(tv, - self.width, -1), range(0, self.height)):

				if body(): break

			if end(): break

		if len(self.win) == 5: return True

		############################################################################ 

		self.win = []
		return False
		
