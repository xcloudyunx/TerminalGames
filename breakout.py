import os, time, pynput, random

GAMESPEED = 10
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
BRICK = ["\033[1;37;41m \033[0;37;40m", "\033[1;37;43m \033[0;37;40m", "\033[1;37;42m \033[0;37;40m", "\033[1;37;46m \033[0;37;40m", "\033[1;37;44m \033[0;37;40m", "\033[1;37;45m \033[0;37;40m"]

class Brick:
	def __init__(self, bodyPos, bodyWidth, colour):
		self.body = []
		self.colour = BRICK[colour]
		for i in range(-(bodyWidth//2), bodyWidth//2+1):
			self.body.append((bodyPos[0]+i, bodyPos[1]))
		
	def getBody(self):
		return self.body
		
	def getColour(self):
		return self.colour
			
class Paddle:
	def __init__(self, bodyPos, bodyWidth, width, height):
		self.body = []
		for i in range(-(bodyWidth//2), bodyWidth//2+1):
			self.body.append((bodyPos[0]+i, bodyPos[1]))
		self.gameWidth = width
		self.gameHeight = height
		
	def getBody(self):
		return self.body
		
	def step(self, direction):
		if direction == LEFT and self.body[0][0] != 1:
			self.body = [(self.body[0][0]-1, self.body[0][1])] + self.body[0:-1]
		elif direction == RIGHT and self.body[-1][0] != self.gameWidth:
			self.body = self.body[1:] + [(self.body[-1][0]+1, self.body[-1][1])]
			
class Ball:
	def __init__(self, width, height):
		self.gameWidth = width
		self.gameHeight = height
		self.resetPosition()
		
	def resetPosition(self):
		self.position = ((self.gameWidth+1)//2, (self.gameHeight+1)//2-2)
		self.direction = [DL, DR][random.randint(0, 1)]
	
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
		self.paddle = Paddle(((width+1)//2, height-2), 9, self.width, self.height)
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
			
		self.setupBricks()
		
	def setupBricks(self):
		self.bricks = []
		for i in range(4, self.width-2, 6):
			for j in range(2, (self.height+1)//2-1, 2):
				self.bricks.append(Brick((i, j), 5, j//2-1))
		
	def movePaddle(self, key):
		key = str(key)[1]
		if key == "a":
			self.paddle.step(LEFT)
		elif key == "d":
			self.paddle.step(RIGHT)
				
	def updateBall(self):
		while True:
			if self.ball.getStepLocation() in self.paddle.getBody()[:4]:
				self.ball.setDirection((LEFT[0], UP[1]))
			elif self.ball.getStepLocation() in self.paddle.getBody()[5:]:
				self.ball.setDirection((RIGHT[0], UP[1]))
			elif self.ball.getStepLocation() == self.paddle.getBody()[4]:
				self.ball.setDirection((self.ball.getDirection()[0], UP[1]))
			elif self.ball.getPosition()[0] == 1 and self.ball.getDirection()[0] == LEFT[0]:
				self.ball.setDirection((RIGHT[0], self.ball.getDirection()[1]))
			elif self.ball.getPosition()[0] == self.width and self.ball.getDirection()[0] == RIGHT[0]:
				self.ball.setDirection((LEFT[0], self.ball.getDirection()[1]))
			elif self.ball.getPosition()[1] == 1 and self.ball.getDirection()[1] == UP[1]:
				self.ball.setDirection((self.ball.getDirection()[0], DOWN[1]))
			elif self.ball.getPosition()[1] == self.height and self.ball.getDirection()[1] == DOWN[1]:
				self.ball.resetPosition()
				time.sleep(1)
			else:
				for brick in self.bricks:
					if self.ball.getStepLocation() in brick.getBody():
						if self.ball.getStepLocation() in (brick.getBody()[0], brick.getBody()[-1]) and (self.ball.getPosition()[0], self.ball.getStepLocation()[1]) not in brick.getBody():
							self.ball.setDirection((-self.ball.getDirection()[0], -self.ball.getDirection()[1]))
						else:
							self.ball.setDirection((self.ball.getDirection()[0], -self.ball.getDirection()[1]))
						self.bricks.remove(brick)
						break
				else:
					self.ball.step()
					break
	
	def updateBoard(self):
		for i in range(1, self.width+1):
			for j in range(1, self.height+1):
				self.board[j][i] = " "
			
		self.updateBall()
		self.board[self.ball.getPosition()[1]][self.ball.getPosition()[0]] = BALL
		
		for pos in self.paddle.getBody():
			self.board[pos[1]][pos[0]] = PADDLE
		
		for brick in self.bricks:
			for pos in brick.getBody():
				self.board[pos[1]][pos[0]] = brick.getColour()
		
	def render(self):
		os.system("cls")
		for row in self.board:
			for col in row:
				print(col, end="")
			print()
			
	def update(self):
		while not self.gameOver:
			if len(self.bricks) == 0:
				self.gameOver = True
				break
			self.updateBoard()
			self.render()
			time.sleep(1/GAMESPEED)
			
	def end(self):
		self.gameOver = True
		print("\033[1;37;40mGAME OVER\033[0;37;40m")
	
def main():
	game = Game(79, 27)
	game.update()
	
if __name__ == "__main__":
	main()