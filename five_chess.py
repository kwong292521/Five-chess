import pygame

import game_functions as gf
from settings import Settings
from trans_rect import Trans_rect

def run_game():
	#初始化pygame、设置和屏幕对象
	pygame.init()
	my_settings = Settings()
	screen = pygame.display.set_mode(
		(my_settings.screen_width,my_settings.screen_height))
	pygame.display.set_caption("五子棋")
	screen.fill(my_settings.bg_color)
	
	#创建一个存储透明矩形的列表
	trans_rects = []
	
	#分别创建一个存储已下的白棋黑棋坐标元组的列表
	black_pos = []
	white_pos = []
	
	#创建一个斜线胜利所有情况的集合
	dia_win = []
	
	#创建透明检测矩形实例
	trans_rect = Trans_rect(my_settings,screen,trans_rects)
	
	#刷新屏幕
	pygame.display.flip()
	
	#创建棋盘
	gf.create_chessboard(screen,my_settings)
	
	#生成斜线胜利集合的数据
	gf.create_dia_win_data(dia_win,my_settings)
	
	#进入游戏主循环
	while True:
		gf.check_events(trans_rect,screen,my_settings,black_pos,white_pos,dia_win)	
	
run_game()
