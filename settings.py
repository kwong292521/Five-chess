class Settings():
	'''游戏各种参数设置的类'''
	
	def __init__(self):
		'''游戏静态设置'''
		#屏幕设置
		self.screen_width = 800
		self.screen_height = 800
		self.bg_color = (205,133,63)
		
		#棋子设置
		self.chess_size = 15
		self.black_chess_color = (0,0,0)
		self.white_chess_color = (255,255,255)
		
		#棋盘设置
		self.chessboard_size = 40
		self.chessboard_line_color = (0,0,0)
		
		#下棋顺序，True为白棋，False为黑棋
		self.change = True
		
		#初始化游戏活跃标志
		self.game_active = True
