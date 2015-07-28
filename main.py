#!/usr/bin/python2
#-*- coding: UTF-8 -*-

import pygame
import ai, game

try: import android
except ImportError: android = None

def event():

	ev = pygame.event.wait()

	if android:
			
		if android.check_pause():
			
			android.wait_for_resume()

	return ev

class CResources:

	def rpath(self, resource_relative_path):

		return "resources/%s" % (resource_relative_path)

	def __init__(self):

		self.scr = None
		self.bmp = {}
		self.rect = {}
	
		############################################################################ 
	
		self.bmp["bg"] = pygame.image.load(self.rpath("bg.bmp"))
	
		if android:

			self.scr = pygame.display.set_mode((self.bmp["bg"].get_width(), self.bmp["bg"].get_height()), pygame.FULLSCREEN)

		else:

			self.scr = pygame.display.set_mode((self.bmp["bg"].get_width(), self.bmp["bg"].get_height()), pygame.HWSURFACE | pygame.DOUBLEBUF)
	
		self.bmp["title-bg"] = pygame.image.load(self.rpath("title.bmp"))
		self.bmp["start"] = (pygame.image.load(self.rpath("start_np.bmp")), pygame.image.load(self.rpath("start_p.bmp")))
		self.bmp["enemy"] = pygame.image.load(self.rpath("enemy.bmp"))
		self.bmp["cross-big"] = (pygame.image.load(self.rpath("cross_big_np.bmp")), pygame.image.load(self.rpath("cross_big_p.bmp")))
		self.bmp["null-big"] = (pygame.image.load(self.rpath("null_big_np.bmp")), pygame.image.load(self.rpath("null_big_p.bmp")))
		self.bmp["algo-title"] = pygame.image.load(self.rpath("algo.bmp"))
		self.bmp["algo"] = list(map(lambda u: # Для портирования на Python 3 используется list()
			(
				pygame.image.load(self.rpath("ns_%d.bmp" % (u))),
				pygame.image.load(self.rpath("s_%d.bmp" % (u))),
				pygame.image.load(self.rpath("label_%d.bmp" % (u)))
			), range(0, 4)))
			# ), range(0, 5)))
		self.bmp["null-small"] = (pygame.image.load(self.rpath("null_small.bmp")), pygame.image.load(self.rpath("null_small_win.bmp")))
		self.bmp["cross-small"] = (pygame.image.load(self.rpath("cross_small.bmp")), pygame.image.load(self.rpath("cross_small_win.bmp")))
		self.bmp["line"] = (pygame.image.load(self.rpath("line_h.bmp")), pygame.image.load(self.rpath("line_v.bmp")))
		self.bmp["computer-winner"] = pygame.image.load(self.rpath("computer_winner.bmp"))
		self.bmp["man-winner"] = pygame.image.load(self.rpath("man_winner.bmp"))
		self.bmp["none-winner"] = pygame.image.load(self.rpath("none_winner.bmp"))
		self.bmp["wait"] = list(map(lambda u: # Для портирования на Python 3 используется list()
				pygame.image.load(self.rpath("wait_%d.bmp" % (u))), range(0, 5)))
			# ), range(0, 5)))
	
		self.rect["bg"] = self.bmp["bg"].get_rect()
		self.rect["title-bg"] = pygame.Rect((self.scr.get_width() - self.bmp["title-bg"].get_width()) / 2, 30, self.bmp["title-bg"].get_width(),
				self.bmp["title-bg"].get_height())
		self.rect["start-title"] = pygame.Rect((self.scr.get_width() - self.bmp["start"][0].get_width()) / 2,
				30 + 20 + (self.bmp["title-bg"].get_height() - self.bmp["start"][0].get_height()) / 2, self.bmp["start"][0].get_width(),
				self.bmp["start"][0].get_height())
		self.rect["enemy"] = pygame.Rect(self.scr.get_width() / 2 + 70, 30, self.bmp["enemy"].get_width(), self.bmp["enemy"].get_height())
		self.rect["cross-big"] = pygame.Rect(self.rect["enemy"].x + self.rect["enemy"].width / 4 - 30, 122, self.bmp["null-big"][0].get_width(),
				self.bmp["null-big"][0].get_height())
		self.rect["null-big"] = pygame.Rect(self.rect["enemy"].x + 3 * self.rect["enemy"].width / 4 - 30, 115, self.bmp["null-big"][0].get_width(),
				self.bmp["null-big"][0].get_height())
		self.rect["small"] = self.bmp["null-small"][0].get_rect()
		self.rect["line"] = (self.bmp["line"][0].get_rect(), self.bmp["line"][1].get_rect())
		self.rect["computer-winner"] = self.bmp["computer-winner"].get_rect()
		self.rect["man-winner"] = self.bmp["man-winner"].get_rect()
		self.rect["none-winner"] = self.bmp["none-winner"].get_rect()
		self.rect["wait"] = list(map(lambda u: pygame.Rect(self.bmp["bg"].get_width() - 60 * (6 - u), self.bmp["bg"].get_height() - 85,
			self.bmp["wait"][u].get_width(), self.bmp["wait"][u].get_height()), range(0, 5)))

		############################################################################ 
	
		base_x = 50
		c_height = 200
	
		self.rect["algo-title"] = pygame.Rect(base_x + 30, c_height, self.bmp["algo-title"].get_width(), self.bmp["algo-title"].get_height())
		c_height += self.rect["algo-title"].height + 20
	
		self.rect["algo"] = []
	
		for u in range(0, 4): # 5):
	
			self.rect["algo"].append(
				(
					pygame.Rect(base_x, c_height, self.bmp["algo"][u][0].get_width(), self.bmp["algo"][u][0].get_height()),
					pygame.Rect(base_x + self.bmp["algo"][u][0].get_width() + 10,
						c_height + (self.bmp["algo"][u][0].get_height() - self.bmp["algo"][u][2].get_height()) / 2, self.bmp["algo"][u][2].get_width(),
						self.bmp["algo"][u][2].get_height())
				))
			c_height += self.bmp["algo"][u][0].get_height() + 10
	
		############################################################################ 
	
		self.rect["start-setup"] = pygame.Rect((self.rect["enemy"].x - 70, self.rect["algo"][2][0].y - 140, self.bmp["start"][0].get_width(),
			self.bmp["start"][0].get_height()))
	
		############################################################################ 
	
		self.bmp["title"] = self.scr.copy()
		self.rect["title"] = self.bmp["title"].get_rect()
		for u in ("bg", "title-bg"): self.bmp["title"].blit(self.bmp[u], self.rect[u])
	
		self.bmp["setup"] = self.scr.copy()
		self.rect["setup"] = self.bmp["setup"].get_rect()
		for u in ("bg", "enemy", "algo-title"): self.bmp["setup"].blit(self.bmp[u], self.rect[u])

def title(res):

	is_run = False
	is_pressed = False

	while True:

		res.scr.blit(res.bmp["title"], res.rect["title"])
		res.scr.blit(res.bmp["start"][1 if is_pressed else 0], res.rect["start-title"])
		pygame.display.flip()

		ev = event()

		if ev.type == pygame.MOUSEBUTTONDOWN:
			
			if res.rect["start-title"].collidepoint(pygame.mouse.get_pos()):

				is_pressed = True
			
		elif ev.type == pygame.MOUSEBUTTONUP:
			
			if is_pressed:
				
				is_run = True
				break

		elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
			
			break

	return is_run

def setup(res):
	
	is_cross = True

	def draw_null_cross():

		res.scr.blit(res.bmp["cross-big"][1 if is_cross else 0], res.rect["cross-big"])
		res.scr.blit(res.bmp["null-big"][0 if is_cross else 1], res.rect["null-big"])

	############################################################################ 

	algo_index = 0

	def draw_algo():

		for u in range(0, 4): # 5):

			res.scr.blit(res.bmp["algo"][u][1 if algo_index == u else 0], res.rect["algo"][u][0])
			res.scr.blit(res.bmp["algo"][u][2], res.rect["algo"][u][1])

	#############################################################################

	is_run = False
	is_pressed = False

	while True:

		ev = event()

		res.scr.blit(res.bmp["setup"], res.rect["setup"])
		draw_null_cross()
		draw_algo()
		res.scr.blit(res.bmp["start"][1 if is_pressed else 0], res.rect["start-setup"])
		pygame.display.flip()

		if ev.type == pygame.MOUSEBUTTONDOWN:

			pos = pygame.mouse.get_pos()

			if res.rect["cross-big"].collidepoint(pos): is_cross = True
			elif res.rect["null-big"].collidepoint(pos): is_cross = False
			elif res.rect["start-setup"].collidepoint(pos): is_pressed = True 

			for u in range(0, 4): # 5):

				if res.rect["algo"][u][0].collidepoint(pos):

					algo_index = u
					break

		elif ev.type == pygame.MOUSEBUTTONUP:

			if is_pressed:

				is_run = True
				break

		elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:

			break

	return (is_run, is_cross, algo_index)

def main():

	pygame.init()

	############################################################################ 

	res = CResources()

	if android:
		
		android.init()
		android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

	############################################################################ 

	while title(res):

		is_run = True

		while is_run:

			is_run, is_cross, ai_algo_index = setup(res)

			if is_run:

				field = game.CField(res, is_cross)
				comp = ai.CAI(field, ai_algo_index)

				# Крестики ходят первыми
				if is_cross: field.computer_turn(comp)

				while True:

					field.draw()
					pygame.display.flip()

					ev = event()

					if ev.type == pygame.MOUSEBUTTONDOWN:

						if field.man_turn(pygame.mouse.get_pos()):

							if field.winner(): break
							field.computer_turn(comp)
							if field.winner(): break

					elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:

						break

				if field.winner():

					is_winner_screen = False

					while True:

						if is_winner_screen: field.draw_winner_screen()
						else: field.draw()

						pygame.display.flip()

						ev = event()

						if (ev.type == pygame.MOUSEBUTTONDOWN) or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
							
							if is_winner_screen: break
							else: is_winner_screen = True

if __name__ == "__main__":

	main()

