import pygtk
pygtk.require('2.0')
import gtk

buttonPlayed = ['X', 'O']
aiBoard = [[0,0,0],[0,0,0],[0,0,0]]

def emptyAIboard():
	for i in range(3):
		for j in range(3):
			aiBoard[i][j] = 0
	return

# No play = 0, AI = 1, Human = 2
def updateData( buttNum, player ):
	if player == "human":
		playerCode = 2
	else:
		playerCode = 1
	aiBoard[buttNum / 3][buttNum % 3] = playerCode

def decideMove(tilesLeft):
	board = copyBoard(aiBoard)
	#determine if we win
	(i,j) = detWinningRow(1, board, False)
	if not ( i == -1 ):
		return i*3 + j + 1
	#determine if we need to block human
	(i,j) = detWinningRow(2, board, False)
	if not ( i == -1 ):
		return i*3 + j + 1
	
	# Otherwise, determine the best possible move
	(x,y) = pickTile(tilesLeft)
#	for i in range(3):
#		for j in range(3):
#			if board[i][j] == 0:
#				return i * 3 + j + 1
	return x * 3 + y + 1
	
def pickTile(tilesLeft):
	board = copyBoard(aiBoard)
	scoreBoard = [[0,0,0],[0,0,0],[0,0,0]]
	for x in range( 3 ):
		for y in range( 3 ):
			if board[x][y] != 0:
				scoreBoard[x][y] = -100000000
			else:
				score = 0
				board[x][y] = 1
				(wins, losses, ties) = playGame(board, 1, tilesLeft)
				if( losses == 0 and ties == 0):
					score += 10000
				if( losses == 0 ):
					score += 1000
				score += (wins * 2) + (ties * 1) + (losses * -2)
				scoreBoard[x][y] = score
	finalX = 0
	finalY = 0
	biggest = scoreBoard[0][0]
	for x in range(3):
		for y in range(3):
			if( scoreBoard[x][y] > biggest ):
				biggest = scoreBoard[x][y]
				finalX = x
				finalY = y
	return (finalX,finalY)

def playGame( board, player, tilesLeft):
	wins, losses, ties = 0, 0, 0
	prevPlayer = togglePlayerNumber(player)

	(x,y) = detWinningRow(prevPlayer, board, True)
	if not ( x == -1 ):
		if( prevPlayer == 1 ):
			wins += 1
			return (wins, losses, ties)
		else:
			losses += 1
			return (wins, losses, ties)
	if( tilesLeft == 0 ):
		ties += 1
		return (wins, losses, ties)
	
	for i in range(3):
		for j in range(3):
			if( board[i][j] == 0 ):
				nBoard = copyBoard(board)
				nBoard[i][j] = player
				(nWins, nLosses, nTies) = playGame(nBoard, togglePlayerNumber(player), tilesLeft - 1)
				wins += nWins
				losses += nLosses
				ties += nTies
	return (wins, losses, ties)

def copyBoard(toCopy):
	board = [[0,0,0],[0,0,0],[0,0,0]]
	for i in range(3):
		for j in range(3):
			board[i][j] = toCopy[i][j]
	return board
	

def detWinningRow(player, board, checkWin):
	#determine if you're looking for 3 in a row or 2(1 entry is 0)
	if( checkWin ):
		testTile = player
	else:
		testTile = 0

	for i in range(3):
		for j in range(3):
			if( board[i][j] == testTile ):
				if( board[oneAway(i)][j] == player and board[twoAway(i)][j] == player ):
					return (i,j)
				if( board[i][oneAway(j)] == player and board[i][twoAway(j)] == player ):
					return (i,j)
				if( i == j ):
					if( board[oneAway(i)][oneAway(j)] == player and board[twoAway(i)][twoAway(j)] == player ):
						return (i,j)
					if( board[0][2] == player and board[2][0] == player ):
						return (i,j)
				if( i == 0 and j == 2 ):
					if( board[1][1] == player and board[2][0] == player ):
						return (i,j)
				if( i == 2 and j == 0 ):
					if( board[1][1] == player and board[0][2] == player ):
						return (i,j)
	return (-1,-1)
	
def oneAway(n):
	return (n + 1) % 3
def twoAway(n):
	return (n + 2) % 3

class GameBoard:
	human = "X"
	ai = "O"

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def buttonReleased(self, widget, event, data=None):
		if widget.get_label() in buttonPlayed:
			return
		else:
			self.tilesLeft -= 1
			widget.set_label(self.currPlayer)
			updateData(int(widget.get_name()), "human")
			(a,b) = detWinningRow(2, aiBoard, True)
			if( a != -1 ):
				self.WINdow("user")
			elif( self.tilesLeft == 0 ):
				self.WINdow("tie")
			else:
				buttNum = decideMove(self.tilesLeft)
				self.tilesLeft -= 1
				updateData(buttNum - 1, "ai")
				self.currPlayer = togglePlayer(self.currPlayer)
				self.updateButton(buttNum)
				(a,b) = detWinningRow(1, aiBoard, True)
				if( a != -1 ):
					self.WINdow("ai")
				elif( self.tilesLeft == 0 ):
					self.WINdow("tie")
				else:
					self.currPlayer = togglePlayer(self.currPlayer)
	
	def updateButton(self, buttNo):
		if( buttNo == 1 ):
			self.b1.set_label(self.currPlayer)	
		if( buttNo == 2 ):
			self.b2.set_label(self.currPlayer)	
		if( buttNo == 3 ):
			self.b3.set_label(self.currPlayer)	
		if( buttNo == 4 ):
			self.b4.set_label(self.currPlayer)	
		if( buttNo == 5 ):
			self.b5.set_label(self.currPlayer)	
		if( buttNo == 6 ):
			self.b6.set_label(self.currPlayer)	
		if( buttNo == 7 ):
			self.b7.set_label(self.currPlayer)	
		if( buttNo == 8 ):
			self.b8.set_label(self.currPlayer)	
		if( buttNo == 9 ):
			self.b9.set_label(self.currPlayer)
		return

	def exitButtonPressed(self, widget, event, data=None):
		gtk.main_quit()

	def WINdow(self, player):
		if( player == "user" ):
			result = "won!"
		elif ( player == "ai" ):
			result = "lost."
		else:
			result = "tied."
		self.quitWin = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.quitWin.set_position(gtk.WIN_POS_CENTER)
		self.quitFrame = gtk.VBox(homogeneous=False, spacing=10)
		self.quitLabel = gtk.Label("You have " + result )
		self.buttonRow = gtk.HButtonBox()
		self.quitB = gtk.Button("Quit.")
		
		self.buttonRow.add(self.quitB)
		self.quitWin.add(self.quitFrame)
		self.quitFrame.add(self.quitLabel)
		self.quitFrame.add(self.buttonRow)

		self.quitWin.show()
		self.quitFrame.show()
		self.quitLabel.show()
		self.buttonRow.show()
		self.quitB.show()

		self.quitB.connect("button_press_event", self.quitCallback)
	
	def playAgainCallback(self, widget, event, data=None):
		self.clearGameboard()
		self.quitWin.destroy()

	def quitCallback(self, widget, event, data=None):
		gtk.main_quit()


	def clearGameboard(self):
		self.b1.set_label("")
		self.b2.set_label("")
		self.b3.set_label("")
		self.b4.set_label("")
		self.b5.set_label("")
		self.b6.set_label("")
		self.b7.set_label("")
		self.b8.set_label("")
		self.b9.set_label("")
		self.currPlayer = self.human
		emptyAIboard()

	def __init__(self):
		self.currPlayer = "X"
		self.tilesLeft = 9
		# Window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_border_width(10)
		self.window.set_resizable(False)
		self.window.set_title("Smart Tic-Tac-Toe!")
		# Frame
		self.frame = gtk.Frame( label="X plays first.  You are X." )
		# Total window canvas for ttt board and Menu
		self.canvas = gtk.HBox( homogeneous=False, spacing=20 )
		# Tic-Tac-Toe Board
		self.board = gtk.VBox( homogeneous=True, spacing=0 )
		self.row1 = gtk.HButtonBox()
		self.row2 = gtk.HButtonBox()
		self.row3 = gtk.HButtonBox()
		self.row1.set_layout(gtk.BUTTONBOX_START)
		self.row2.set_layout(gtk.BUTTONBOX_START)
		self.row3.set_layout(gtk.BUTTONBOX_START)
		# Menu
		self.menu = gtk.VBox( homogeneous=True, spacing=10)
		

		# Tic-Tac-Toe Buttons
		self.b1 = gtk.Button()
		self.b2 = gtk.Button()
		self.b3 = gtk.Button()
		self.b4 = gtk.Button()
		self.b5 = gtk.Button()
		self.b6 = gtk.Button()
		self.b7 = gtk.Button()
		self.b8 = gtk.Button()
		self.b9 = gtk.Button()
		
		self.b1.set_name("0")
		self.b2.set_name("1")
		self.b3.set_name("2")
		self.b4.set_name("3")
		self.b5.set_name("4")
		self.b6.set_name("5")
		self.b7.set_name("6")
		self.b8.set_name("7")
		self.b9.set_name("8")

		self.exitButton = gtk.Button("Exit")
		
		
		# Add all objects to their respective containers
		self.row1.add(self.b1)
		self.row1.add(self.b2)
		self.row1.add(self.b3)
		self.row2.add(self.b4)
		self.row2.add(self.b5)
		self.row2.add(self.b6)
		self.row3.add(self.b7)
		self.row3.add(self.b8)
		self.row3.add(self.b9)
		self.menu.add(self.exitButton)
		self.board.add(self.row1)
		self.board.add(self.row2)
		self.board.add(self.row3)
		self.canvas.add(self.board)
		self.canvas.add(self.menu)
		self.frame.add(self.canvas)
		self.window.add_with_properties(self.frame, )
		# Show all Objects
		self.b1.show()
		self.b2.show()
		self.b3.show()
		self.b4.show()
		self.b5.show()
		self.b6.show()
		self.b7.show()
		self.b8.show()
		self.b9.show()
		self.exitButton.show()
		self.row1.show()
		self.row2.show()
		self.row3.show()
		self.board.show()
		self.menu.show()
		self.canvas.show()
		self.frame.show()
		self.window.show()

		self.window.connect("destroy", self.destroy)
		self.b1.connect("button_release_event", self.buttonReleased) 
		self.b2.connect("button_release_event", self.buttonReleased) 
		self.b3.connect("button_release_event", self.buttonReleased) 
		self.b4.connect("button_release_event", self.buttonReleased) 
		self.b5.connect("button_release_event", self.buttonReleased) 
		self.b6.connect("button_release_event", self.buttonReleased) 
		self.b7.connect("button_release_event", self.buttonReleased) 
		self.b8.connect("button_release_event", self.buttonReleased) 
		self.b9.connect("button_release_event", self.buttonReleased) 
	
		self.exitButton.connect("button_press_event", self.exitButtonPressed)
	
	def main(self):
		gtk.main()



def togglePlayer(player):
	if( player == "X" ):
		return "O"
	else:
		return "X"

def togglePlayerNumber(player):
	if( player == 1 ):
		return 2
	else:
		return 1
	
#print __name__
if __name__ == "__main__":
	gBoard = GameBoard()
	gBoard.main()
