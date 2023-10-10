from gamemodel import *
from graphics import *


class GameGraphics:
    def __init__(self, game):
        self.game = game

        # open the window
        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)
        
        Line(Point(-110,0), Point(110,0)).draw(self.win)

        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None]

    def drawCanon(self,playerNr):
        player = self.game.getPlayers()[playerNr]
        playerCannon = Rectangle(Point(player.getX() - player.game.getCannonSize()/2, 0), Point(player.getX() + player.game.getCannonSize()/2, player.game.getCannonSize()))

        playerCannon.setFill(player.getColor())
        playerCannon.draw(self.win)
        # draw the cannon
        # TODO: draw a square with the size of the cannon with the color
        # and the position of the player with number playerNr.
        # After the drawing, return the rectangle object.
        return playerCannon

    def drawScore(self,playerNr):
        player = self.game.getPlayers()[playerNr]
        scoreText = Text(Point(player.getX(), -5), "Score: " + str(player.getScore()))
        scoreText.setSize(15)
        scoreText.draw(self.win)
        # draw the score
        # TODO: draw the text "Score: X", where X is the number of points
        # for player number playerNr. The text should be placed under
        # the corresponding cannon. After the drawing,
        # return the text object.
        return scoreText

    def fire(self, angle, vel):
        player = self.game.getCurrentPlayer()
        proj = player.fire(angle, vel)
        circle = self.draw_projs[self.game.getCurrentPlayerNumber()]

        circle_X = proj.getX()
        circle_Y = proj.getY()
       
        if circle is not None:
            circle.undraw()
        
        circle = Circle(Point(proj.getX(), proj.getY()), self.game.getBallSize())
        circle.setFill(player.getColor())
        circle.draw(self.win)

        while proj.isMoving():
            proj.update(1/50)

            # move is a function in graphics. It moves an object dx units in x direction and dy units in y direction
            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            circle_Y = proj.getY()

            update(50)

        self.draw_projs[self.game.getCurrentPlayerNumber()] = circle
        return proj

    def updateScore(self,playerNr):
        self.draw_scores[playerNr].undraw()
        self.draw_scores[playerNr] = self.drawScore(playerNr)

    def play(self):
        while True:
            
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()

            # InputDialog(self, angle, vel, wind) is a class in gamegraphics
            inp = InputDialog(oldAngle,oldVel,wind)
            # interact(self) is a function inside InputDialog. It runs a loop until the user presses either the quit or fire button
            if inp.interact() == "Fire!": 
                angle, vel = inp.getValues()
                inp.close()
            elif inp.interact() == "Quit":
                exit()
            
            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)

            if distance == 0.0:
                player.increaseScore()
                self.explode()
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.game.newRound()

            self.game.nextPlayer()

    def explode(self):
        circleRadius = self.game.getBallSize()
        circle = None

        while circleRadius < 2 * self.game.getCannonSize():
            if circle is not None:
                circle.undraw()

            circle = Circle(Point(self.game.getOtherPlayer().getX(), 0), circleRadius)
            circle.setFill(self.game.getCurrentPlayer().getColor())
            circle.draw(self.win)

            circleRadius += 1
            update(50)
        
        circle.undraw()


class InputDialog:
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11,3)).play()
