from tkinter import *
import random
import time

class Ball: #创建Ball类
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        
        #self.x = 0
        #self.y = -1
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts) #混排
        self.x = starts[0]
        self.y = -2
        
        self.canvas_height = self.canvas.winfo_height() #获取画布当前高度
        self.canvas_width = self.canvas.winfo_width() #获取画布当前宽度

        self.hit_bottom = False; #判断游戏结束

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >=  paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                self.score.hit()
                return True;
        return False;
    
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id) #返回坐标;四个数字组成的列表，左上右下
        if pos[1] <= 0:
            self.y = 3
        elif pos[3] >= self.canvas_height: #触底 结束
            self.hit_bottom = True
        elif self.hit_paddle(pos) == True:
            self.y = -3
        elif pos[0] <= 0:
            self.x = 3
        elif pos[2] >= self.canvas_width:
            self.x = -3
        

class Paddle: #创建球拍Paddle类
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()

        self.started = False
        
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

    def start_game(self, evt):
        self.started = True 

class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        score = 'Score  =%s'
        self.id = canvas.create_text(450, 10, text=score % self.score, fill=color)

    def hit(self):
        self.score += 1
        score = 'Score  =%s'
        self.canvas.itemconfig(self.id, text=score % self.score)
        

tk = Tk()
tk.title("Game")
tk.resizable(0, 0) #窗口的大小不可调整
tk.wm_attributes("-topmost", 1) #画布的窗口放到所有其他窗口之前
canvas = Canvas(tk, width=500, height=400, bd=0,
                highlightthickness=0)#画布之外没有边框
canvas.create_text(100, 70, text='Enter start game',
                   font=('Helvetica', 10))
canvas.pack()
tk.update()

score = Score(canvas, 'green')
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, "red")
game_over_text = canvas.create_text(250, 200, text='GAME OVER',
                                    font=('Helvetica', 20), state='hidden')

while 1:
    if ball.hit_bottom == False and paddle.started == True:
        ball.draw()
        paddle.draw()
    if ball.hit_bottom == True:
        time.sleep(1)
        canvas.itemconfig(game_over_text, state='normal')
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
