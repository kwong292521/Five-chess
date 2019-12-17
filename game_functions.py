import pygame
import pygame.font
import sys


def get_rows(my_settings):
	'''计算行数'''
	rows = int((my_settings.screen_width - 2*my_settings.chessboard_size)
		/my_settings.chessboard_size + 1)
	return rows


def create_chessboard(screen,my_settings):
	'''创建一个棋盘'''
	rows = get_rows(my_settings)
	x_start,y_start = my_settings.chessboard_size,my_settings.chessboard_size 
	x_end,y_end = my_settings.screen_width - my_settings.chessboard_size,my_settings.chessboard_size
	start_pos = (x_start,y_start)
	end_pos = (x_end,y_end)
	
	for row in range(1,rows+1):
		#绘制横线
		pygame.draw.line(screen,my_settings.chessboard_line_color,
				start_pos,end_pos, 1)
		y_start += my_settings.chessboard_size
		y_end += my_settings.chessboard_size
		start_pos = (x_start,y_start)
		end_pos = (x_end,y_end)

	x_end = x_start
	y_end = y_start-my_settings.chessboard_size
	x_start,y_start = my_settings.chessboard_size,my_settings.chessboard_size
	start_pos = (x_start,y_start)
	end_pos = (x_end,y_end)
	
	for row in range(1,rows+1):
		#绘制竖线
		pygame.draw.line(screen,my_settings.chessboard_line_color,
				start_pos,end_pos, 1)
		x_start += my_settings.chessboard_size
		x_end += my_settings.chessboard_size
		start_pos = (x_start,y_start)
		end_pos = (x_end,y_end)

	#刷新屏幕
	pygame.display.flip()


def create_dia_win_data(dia_win,my_settings):
	'''生成斜线胜利集合的数据'''
	dia_gather = []
	x = my_settings.chessboard_size
	y = my_settings.chessboard_size
	
	for i in range(1 , int( (my_settings.screen_height-2*my_settings.chessboard_size)/my_settings.chessboard_size - 2 ) ):
		#沿 y = -x 方向的斜线
		#竖方向遍历
		#竖轴移动
		x = my_settings.chessboard_size
		y = i*my_settings.chessboard_size
		for j in range(1 , int( (my_settings.screen_width-2*my_settings.chessboard_size)/my_settings.chessboard_size - 2 ) ):
			#横方向遍历
			#横轴移动
			x = j*my_settings.chessboard_size
			y = i*my_settings.chessboard_size
			for k in range(1,6):
				#五子遍历
				dia_gather.append((x,y))
				x += my_settings.chessboard_size
				y += my_settings.chessboard_size
			#加入一个胜利集合
			dia_win.append(dia_gather)
			#刷新
			dia_gather = []
			
	for i in range(1 , int( (my_settings.screen_height-2*my_settings.chessboard_size)/my_settings.chessboard_size - 2 ) ):
		#沿y = x 方向的斜线
		#竖方向遍历
		#竖轴移动
		x = my_settings.chessboard_size
		y = (4+i)*my_settings.chessboard_size
		for j in range(1 , int( (my_settings.screen_width-2*my_settings.chessboard_size)/my_settings.chessboard_size - 2 ) ):
			#横方向遍历
			#横轴移动
			x = j*my_settings.chessboard_size
			y = (4+i)*my_settings.chessboard_size
			for k in range(1,6):
				#五子遍历
				dia_gather.append((x,y))
				x += my_settings.chessboard_size
				y -= my_settings.chessboard_size
			#加入一个胜利集合
			dia_win.append(dia_gather)
			#刷新
			dia_gather = []
			 
		
def check_rep(chess_rect,black_pos,white_pos):
	'''检查下棋位置是否已经有棋子'''
	rep_sign = False
	for w_pos in white_pos:
		if rep_sign:
			break
		if black_pos:
			#解决一开始黑棋列表为空时产生重复下棋的bug
			for b_pos in black_pos:
				if (chess_rect.centerx,chess_rect.centery) == b_pos or (chess_rect.centerx,chess_rect.centery) == w_pos:
					#一旦重复，标志改变
					rep_sign = True
					break
		else:
			if (chess_rect.centerx,chess_rect.centery) == w_pos:
				rep_sign = True
	return rep_sign
									

def check_click_rect(mouse_x, mouse_y,trans_rect,screen,my_settings,black_pos,white_pos,dia_win):
	'''监测鼠标点击透明矩形以创建五子棋'''
	for chess_rect in trans_rect.trans_rects:
		rect_clicked = chess_rect.collidepoint(mouse_x,mouse_y)
		if rect_clicked:
			#创建五子棋
			if my_settings.change:
				#检查下棋位置是否已经有棋子
				if not check_rep(chess_rect,black_pos,white_pos):
					#下白棋
					pygame.draw.circle(screen,my_settings.white_chess_color,
						(chess_rect.centerx,chess_rect.centery),my_settings.chess_size,0)
					pygame.display.flip()
					print('w'+'(' + str(chess_rect.centerx) +',' + str(chess_rect.centery) + ')')
					#改变下棋顺序
					my_settings.change = not my_settings.change
					#存储已下白棋坐标
					white_pos.append((chess_rect.centerx,chess_rect.centery))
			else:
				#检查下棋位置是否已经有棋子
				if not check_rep(chess_rect,black_pos,white_pos):
					#下黑棋
					pygame.draw.circle(screen,my_settings.black_chess_color,
						(chess_rect.centerx,chess_rect.centery),my_settings.chess_size,0)
					pygame.display.flip()
					print('b'+'(' + str(chess_rect.centerx) +',' + str(chess_rect.centery) + ')')
					#改变下棋顺序
					my_settings.change = not my_settings.change
					#存储已下黑棋坐标
					black_pos.append((chess_rect.centerx,chess_rect.centery))
					
	check_win(black_pos,white_pos,my_settings,dia_win,screen)


def check_win(black_pos,white_pos,my_settings,dia_win,screen):
	'''检测游戏胜利'''
	
	#创建分别储存棋子xy坐标的列表
	black_x = []
	black_y = []
	white_x = []
	white_y = []
	
	#检测黑棋胜利
	
	#检测黑棋横胜利
	xy = 1
	con_chess = 0
	che_sign = my_settings.chessboard_size
	for i in range(1,int((my_settings.screen_width - 2*my_settings.chessboard_size)/my_settings.chessboard_size) + 2):
		for b_pos in black_pos:
			for b_pos_xy in b_pos:
				if xy == 1:
					b_pos_x = b_pos_xy
					black_x.append(b_pos_x)
					xy += 1
				elif xy == 2:
					b_pos_y = b_pos_xy
					black_y.append(b_pos_y)
					xy -= 1
			if b_pos_y != che_sign:
				del black_x[-1]
		black_x.sort()
		for j in range(0,len(black_x) - 1):
			if (black_x[j+1]):
				if(black_x[j+1] - black_x[j]) == my_settings.chessboard_size:
					con_chess += 1
				if(black_x[j+1] - black_x[j]) != my_settings.chessboard_size:
					con_chess = 0
				if con_chess == 4:
					print('Black WIN!!!')
					win_action(my_settings,False,screen)
					break		
		che_sign += my_settings.chessboard_size
		black_x = []
		black_y = []
		
	#检测黑棋竖胜利
	xy = 1
	con_chess = 0
	che_sign = my_settings.chessboard_size
	for i in range(1,int((my_settings.screen_width - 2*my_settings.chessboard_size)/my_settings.chessboard_size) + 2):
		for b_pos in black_pos:
			for b_pos_xy in b_pos:
				if xy == 1:
					b_pos_x = b_pos_xy
					black_x.append(b_pos_x)
					xy += 1
				elif xy == 2:
					b_pos_y = b_pos_xy
					black_y.append(b_pos_y)
					xy -= 1
			if b_pos_x != che_sign:
				del black_y[-1]
		black_y.sort()
		for j in range(0,len(black_y) - 1):
			if (black_y[j+1]):
				if(black_y[j+1] - black_y[j]) == my_settings.chessboard_size:
					con_chess += 1
				if(black_y[j+1] - black_y[j]) != my_settings.chessboard_size:
					con_chess = 0
				if con_chess == 4:
					print('Black WIN!!!')
					win_action(my_settings,False,screen)
					break		
		che_sign += my_settings.chessboard_size
		black_x = []
		black_y = []
		
	#检测黑棋斜胜利
	con_chess = 0
	for dia_gather in dia_win:
		for dia_pos in dia_gather:
			for check_pos in black_pos:
				if check_pos == dia_pos:
					con_chess += 1
					break	
		if con_chess == 5:
			print('Black WIN!!!')
			win_action(my_settings,False,screen)
			break
		con_chess = 0
		
	#检测白棋胜利
	
	#检测白棋横胜利
	xy = 1
	con_chess = 0
	che_sign = my_settings.chessboard_size
	for i in range(1,int((my_settings.screen_width - 2*my_settings.chessboard_size)/my_settings.chessboard_size) + 2):
		for w_pos in white_pos:
			for w_pos_xy in w_pos:
				if xy == 1:
					w_pos_x = w_pos_xy
					white_x.append(w_pos_x)
					xy += 1
				elif xy == 2:
					w_pos_y = w_pos_xy
					white_y.append(w_pos_y)
					xy -= 1
			if w_pos_y != che_sign:
				del white_x[-1]
		white_x.sort()
		for j in range(0,len(white_x) - 1):
			if (white_x[j+1]):
				if(white_x[j+1] - white_x[j]) == my_settings.chessboard_size:
					con_chess += 1
				if(white_x[j+1] - white_x[j]) != my_settings.chessboard_size:
					con_chess = 0
				if con_chess == 4:
					print('White WIN!!!')
					win_action(my_settings,True,screen)
					break		
		che_sign += my_settings.chessboard_size
		white_x = []
		white_y = []
		
	#检测白棋竖胜利
	xy = 1
	con_chess = 0
	che_sign = my_settings.chessboard_size
	for i in range(1,int((my_settings.screen_width - 2*my_settings.chessboard_size)/my_settings.chessboard_size) + 2):
		for w_pos in white_pos:
			for w_pos_xy in w_pos:
				if xy == 1:
					w_pos_x = w_pos_xy
					white_x.append(w_pos_x)
					xy += 1
				elif xy == 2:
					w_pos_y = w_pos_xy
					white_y.append(w_pos_y)
					xy -= 1
			if w_pos_x != che_sign:
				del white_y[-1]
		white_y.sort()
		for j in range(0,len(white_y) - 1):
			if (white_y[j+1]):
				if(white_y[j+1] - white_y[j]) == my_settings.chessboard_size:
					con_chess += 1
				if(white_y[j+1] - white_y[j]) != my_settings.chessboard_size:
					con_chess = 0
				if con_chess == 4:
					print('White WIN!!!')
					win_action(my_settings,True,screen)
					break		
		che_sign += my_settings.chessboard_size
		white_x = []
		white_y = []
		
	#检测白棋斜胜利
	con_chess = 0
	for dia_gather in dia_win:
		for dia_pos in dia_gather:
			for check_pos in white_pos:
				if check_pos == dia_pos:
					con_chess += 1
					break	
		if con_chess == 5:
			print('White WIN!!!')
			win_action(my_settings,True,screen)
			break
		con_chess = 0
	
def win_action(my_settings,who_win,screen):
	'''游戏胜利后响应'''
	my_settings.game_active = False
	
	#图形参数
	w_text_color = (255,255,255)
	b_text_color = (0,0,0)
	button_color = (255,0,0)
	font = pygame.font.SysFont(None, 48)
	b_msg = 'Black WIN'
	w_msg = 'White WIN'
	
	#创建矩形
	screen_rect = screen.get_rect()
	win_rect = pygame.Rect(0,0,200,80)
	win_rect.center = screen_rect.center
	
	#绘制图形
	if who_win:
		win_image = font.render(w_msg, True, w_text_color,button_color)
		win_image_rect = win_image.get_rect()
		win_image_rect.center = win_rect.center
		screen.fill(button_color, win_rect)
		screen.blit(win_image, win_image_rect)
		pygame.display.flip()
	else:
		win_image = font.render(b_msg, True, b_text_color,button_color)
		win_image_rect = win_image.get_rect()
		win_image_rect.center = win_rect.center
		screen.fill(button_color, win_rect)
		screen.blit(win_image, win_image_rect)
		pygame.display.flip()


def check_events(trans_rect,screen,my_settings,black_pos,white_pos,dia_win):
	'''监测键盘鼠标事件'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if my_settings.game_active:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_click_rect(mouse_x, mouse_y,trans_rect,screen,my_settings,black_pos,white_pos,dia_win)
