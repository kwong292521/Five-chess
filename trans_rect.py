import pygame

class Trans_rect():
	'''创建透明矩形'''
	def __init__(self,my_settings,screen,trans_rects):
		#初始化设置
		self.my_settings = my_settings
		self.screen = screen
		self.trans_rects = trans_rects
		self.create_trans_rect()
		
	def	create_trans_rect(self):
		'''在屏幕原点创建一个透明矩形，再用循环把它安置在每一个点'''
		#创建透明surface
		surface_trans = self.screen.convert_alpha()
		surface_trans.fill((255,255,255,0))
		
		#创建矩形
		self.rows = int((self.my_settings.screen_width - 
			2*self.my_settings.chessboard_size)
				/self.my_settings.chessboard_size + 1)
		
		self.rect_x,self.rect_y = self.my_settings.chessboard_size,self.my_settings.chessboard_size
		for row in range(1,self.rows+1):
			for row in range(1,self.rows+1):
				self.mode_trans_rect = pygame.draw.rect(surface_trans, (0,255,0,100), 
					pygame.Rect(0,0,self.my_settings.chessboard_size,
					self.my_settings.chessboard_size))
				self.mode_trans_rect.center = (self.rect_x,self.rect_y)
				self.rect_x += self.my_settings.chessboard_size
				self.trans_rects.append(self.mode_trans_rect)
			self.rect_x = self.my_settings.chessboard_size
			self.rect_y += self.my_settings.chessboard_size
