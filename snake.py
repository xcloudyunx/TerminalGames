import os, time, pynput, random

GAMESPEED = 60
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
HEAD = "\033[1;37;40mx\033[0;37;40m"
BODY = "\033[1;37;40mo\033[0;37;40m"
APPLE = "\033[1;31;40m*\033[0;37;40m"

class Snake:
	def __init__(self, body, direction, width, height):
		self.body = body
		self.direction = direction
		self.gameWidth = width
		self.gameHeight = height
		self.evolved = False
		
	def setDirection(self, direction):
		if (self.direction in (UP, DOWN) and direction not in (UP, DOWN)) or (self.direction in (RIGHT, LEFT) and direction not in (RIGHT, LEFT)):
			self.direction = direction
		
	def getHead(self):
		return self.body[-1]
		
	def getBody(self):
		return self.body[:-1]
		
	def evolve(self):
		self.evolved = True
		
	def step(self):
		newX = self.body[-1][0]+self.direction[0]
		if newX == self.gameWidth+1:
			newX = 1
		elif newX == 0:
			newX = self.gameWidth
		newY = self.body[-1][1]+self.direction[1]
		if newY == self.gameHeight+1:
			newY = 1
		elif newY == 0:
			newY = self.gameHeight
		newPos = (newX, newY)
		if newPos in self.body:
			return False
		self.body.append(newPos)
		if self.evolved:
			self.evolved = False
		else:
			self.body = self.body[1:]
		return True

class Apple:
	def __init__(self, width, height):
		self.gameWidth = width
		self.gameHeight = height
		self.position = None
		
	def generateNewApple(self):
		self.position = (random.randint(1, self.gameWidth), random.randint(1, self.gameHeight))
	
	def reset(self):
		self.position = None
	
	def getPosition(self):
		return self.position

class Game:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.snake = Snake([((width+1)//2, (height+1)//2)], UP, self.width, self.height)
		self.apple = Apple(width, height)
		self.setupBoard()
		self.gameOver = False
		listener = pynput.keyboard.Listener(on_press=self.updateDirection)
		listener.start()
		
	def setupBoard(self):
		self.board = [[" " for i in range(self.width+2)] for j in range(self.height+2)]
		self.board[0] = ["\033[1;32;40m-\033[0;37;40m" for i in range(self.width+2)]
		self.board[self.height+1] = ["\033[1;32;40m-\033[0;37;40m" for i in range(self.width+2)]
		for i in range(1, self.height+2):
			self.board[i][0] = "\033[1;32;40m|\033[0;37;40m"
			self.board[i][self.width+1] = "\033[1;32;40m|\033[0;37;40m"
		self.board[0][0] = "\033[1;32;40m+\033[0;37;40m"
		self.board[0][self.width+1] = "\033[1;32;40m+\033[0;37;40m"
		self.board[self.height+1][0] = "\033[1;32;40m+\033[0;37;40m"
		self.board[self.height+1][self.width+1] = "\033[1;32;40m+\033[0;37;40m"
		
	def updateDirection(self, key):
		key = str(key)[1]
		if key == "w":
			self.snake.setDirection(UP)
		elif key == "a":
			self.snake.setDirection(LEFT)
		elif key == "s":
			self.snake.setDirection(DOWN)
		elif key == "d":
			self.snake.setDirection(RIGHT)
	
	def updateSnake(self):
		return self.snake.step()
	
	def updateBoard(self):
		for i in range(1, self.width+1):
			for j in range(1, self.height+1):
				self.board[j][i] = " "
		
	
		for pos in self.snake.getBody():
			self.board[pos[1]][pos[0]] = BODY
		self.board[self.snake.getHead()[1]][self.snake.getHead()[0]] = HEAD
		
		if self.apple.getPosition() == None:
			self.apple.generateNewApple()
			while self.apple.getPosition() in self.snake.getBody()+[self.snake.getHead()]:
				self.apple.generateNewApple()
			self.board[self.apple.getPosition()[1]][self.apple.getPosition()[0]] = APPLE
		elif self.board[self.apple.getPosition()[1]][self.apple.getPosition()[0]] == HEAD:
			self.snake.evolve()
			self.apple.reset()
		else:
			self.board[self.apple.getPosition()[1]][self.apple.getPosition()[0]] = APPLE
		
	def render(self):
		os.system("cls")
		for row in self.board:
			for col in row:
				print(col, end="")
			print()
			
	def update(self):
		while not self.gameOver:
			if not self.updateSnake():
				self.end()
				break
			self.updateBoard()
			self.render()
			time.sleep(1/GAMESPEED)
			
	def end(self):
		self.gameOver = True
		print("\033[1;37;40mGAME OVER\033[0;37;40m")
	
def main():
	game = Game(50, 25)
	game.update()
	
if __name__ == "__main__":
	main()