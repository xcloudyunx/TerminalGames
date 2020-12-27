import os, time, pynput

GAMESPEED = 60
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BIKE1 = "\033[1;36;40mx\033[0;37;40m"
TRAIL1 = "\033[1;36;46m \033[0;37;40m"
BIKE2 = "\033[1;31;40mx\033[0;37;40m"
TRAIL2 = "\033[1;31;41m \033[0;37;40m"

class Player:
	def __init__(self, body, direction, width, height):
		self.body = body
		self.direction = direction
		self.gameWidth = width
		self.gameHeight = height
		
	def setDirection(self, direction):
		if (self.direction in (UP, DOWN) and direction not in (UP, DOWN)) or (self.direction in (RIGHT, LEFT) and direction not in (RIGHT, LEFT)):
			self.direction = direction
		
	def getBike(self):
		return self.body[-1]
		
	def getTrail(self):
		return self.body[:-1]
		
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
		self.body.append(newPos)

class Game:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.player1 = Player([(width//3, (height+1)//2)], UP, self.width, self.height)
		self.player2 = Player([(width+1-width//3, (height+1)//2)], DOWN, self.width, self.height)
		self.setupBoard()
		self.gameOver = False
		listener = pynput.keyboard.Listener(on_press=self.updateDirection)
		listener.start()
		
	def setupBoard(self):
		self.board = [[" " for i in range(self.width+2)] for j in range(self.height+2)]
		self.board[0] = ["\033[1;37;47m \033[0;37;40m" for i in range(self.width+2)]
		self.board[self.height+1] = ["\033[1;37;47m \033[0;37;40m" for i in range(self.width+2)]
		for i in range(1, self.height+1):
			self.board[i][0] = "\033[1;37;47m \033[0;37;40m"
			self.board[i][self.width+1] = "\033[1;37;47m \033[0;37;40m"
		
	def updateDirection(self, key):
		if key == pynput.keyboard.Key.up:
			self.player2.setDirection(UP)
		elif key == pynput.keyboard.Key.left:
			self.player2.setDirection(LEFT)
		elif key == pynput.keyboard.Key.down:
			self.player2.setDirection(DOWN)
		elif key == pynput.keyboard.Key.right:
			self.player2.setDirection(RIGHT)
		else:
			key = str(key)[1]
			if key == "w":
				self.player1.setDirection(UP)
			elif key == "a":
				self.player1.setDirection(LEFT)
			elif key == "s":
				self.player1.setDirection(DOWN)
			elif key == "d":
				self.player1.setDirection(RIGHT)
	
	def updatePlayers(self):
		self.player1.step()
		self.player2.step()
	
	def updateBoard(self):
		if len(self.player1.getTrail()) > 1:
			self.board[self.player1.getTrail()[-1][1]][self.player1.getTrail()[-1][0]] = TRAIL1
		if len(self.player2.getTrail()) > 1:
			self.board[self.player2.getTrail()[-1][1]][self.player2.getTrail()[-1][0]] = TRAIL2
			
		if self.board[self.player1.getBike()[1]][self.player1.getBike()[0]] != " ":
			return False
		if self.board[self.player2.getBike()[1]][self.player2.getBike()[0]] != " ":
			return False
		self.board[self.player1.getBike()[1]][self.player1.getBike()[0]] = BIKE1
		self.board[self.player2.getBike()[1]][self.player2.getBike()[0]] = BIKE2
		return True
		
	def render(self):
		os.system("cls")
		for row in self.board:
			for col in row:
				print(col, end="")
			print()
			
	def update(self):
		while not self.gameOver:
			self.updatePlayers()
			if not self.updateBoard():
				self.end()
				break
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