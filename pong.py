import os, time, pynput, random

GAMESPEED = 60
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UL = (-1, -1)
UR = (1, -1)
DL = (-1, 1)
DR = (1, 1)
BALL = "\033[1;37;40mo\033[0;37;40m"
PADDLE = "\033[1;37;47m \033[0;37;40m"

class Paddle:
	def __init__(self, body, width, height):
		self.body = body
		self.gameWidth = width
		self.gameHeight = height
		
	def getBody(self):
		return self.body
		
	def step(self, direction):
		if direction == UP and self.body[0][1] != 1:
			self.body = [(self.body[0][0], self.body[0][1]-1)] + self.body[0:-1]
		elif direction == DOWN and self.body[-1][1] != self.gameHeight:
			self.body = self.body[1:] + [(self.body[-1][0], self.body[-1][1]+1)]
			
class Ball:
	def __init__(self, width, height):
		self.gameWidth = width
		self.gameHeight = height
		self.resetPosition()
		self.direction = [UL, UR, DL, DR][random.randint(0, 3)]
		
	def resetPosition(self):
		self.position = ((self.gameWidth+1)//2, (self.gameHeight+1)//2)
	
	def getStepLocation(self):
		return (self.position[0]+self.direction[0], self.position[1]+self.direction[1])
	
	def step(self):
		self.position = self.getStepLocation()
	
	def getDirection(self):
		return self.direction
		
	def setDirection(self, direction):
		self.direction = direction
	
	def getPosition(self):
		return self.position

class Game:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.player1 = Paddle([(3, (height+1)//2-1), (3, (height+1)//2), (3, (height+1)//2+1)], self.width, self.height)
		self.player2 = Paddle([(width-2, (height+1)//2-1), (width-2, (height+1)//2), (width-2, (height+1)//2+1)], self.width, self.height)
		self.ball = Ball(width, height)
		self.setupBoard()
		self.gameOver = False
		listener = pynput.keyboard.Listener(on_press=self.movePaddle)
		listener.start()
		
	def setupBoard(self):
		self.board = [[" " for i in range(self.width+2)] for j in range(self.height+2)]
		self.board[0] = ["\033[1;37;47m \033[0;37;40m" for i in range(self.width+2)]
		self.board[self.height+1] = ["\033[1;37;47m \033[0;37;40m" for i in range(self.width+2)]
		for i in range(1, self.height+1):
			self.board[i][0] = "\033[1;37;47m \033[0;37;40m"
			self.board[i][self.width+1] = "\033[1;37;47m \033[0;37;40m"
		
	def movePaddle(self, key):
		if key == pynput.keyboard.Key.up:
			self.player2.step(UP)
		elif key == pynput.keyboard.Key.down:
			self.player2.step(DOWN)
		else:
			key = str(key)[1]
			if key == "w":
				self.player1.step(UP)
			elif key == "s":
				self.player1.step(DOWN)
				
	def updateBall(self):
		if self.ball.getPosition()[1] == 1 and self.ball.getDirection()[1] == UP[1]:
			self.ball.setDirection((self.ball.getDirection()[0], DOWN[1]))
		elif self.ball.getPosition()[1] == self.height and self.ball.getDirection()[1] == DOWN[1]:
			self.ball.setDirection((self.ball.getDirection()[0], UP[1]))
		elif self.ball.getStepLocation() in self.player1.getBody():
			self.ball.setDirection((RIGHT[0], self.ball.getDirection()[1]))
		elif self.ball.getStepLocation() in self.player2.getBody():
			self.ball.setDirection((LEFT[0], self.ball.getDirection()[1]))
		elif self.ball.getPosition()[0] == 1 and self.ball.getDirection()[0] == LEFT[0]:
			self.ball.setDirection((RIGHT[0], self.ball.getDirection()[1]))
			self.ball.resetPosition()
			time.sleep(1)
		elif self.ball.getPosition()[0] == self.width and self.ball.getDirection()[0] == RIGHT[0]:
			self.ball.setDirection((LEFT[0], self.ball.getDirection()[1]))
			self.ball.resetPosition()
			time.sleep(1)
		
		self.ball.step()
	
	def updateBoard(self):
		for i in range(1, self.width+1):
			for j in range(1, self.height+1):
				self.board[j][i] = " "
	
		for pos in self.player1.getBody():
			self.board[pos[1]][pos[0]] = PADDLE
		for pos in self.player2.getBody():
			self.board[pos[1]][pos[0]] = PADDLE
			
		self.updateBall()
		self.board[self.ball.getPosition()[1]][self.ball.getPosition()[0]] = BALL
		
	def render(self):
		os.system("cls")
		for row in self.board:
			for col in row:
				print(col, end="")
			print()
			
	def update(self):
		while not self.gameOver:
			self.updateBoard()
			self.render()
			time.sleep(1/GAMESPEED)
			
	def end(self):
		self.gameOver = True
		print("\033[1;37;40mGAME OVER\033[0;37;40m")
	
def main():
	game = Game(75, 25)
	game.update()
	
if __name__ == "__main__":
	main()