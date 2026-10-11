from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task
import random


class BomberGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.environment = self.loader.loadModel("models/environment")
        self.environment.reparentTo(self.render)
        self.environment.setScale(0.25)
        self.environment.setPos(-8, 42, -5)

        self.player = Actor("models/panda")  # Placeholder 3D model
        self.player.reparentTo(self.render)
        self.player.setScale(0.2)
        self.player.setPos(0, 0, 0)

        self.bombs = []
        self.accept("arrow_up", self.move_player, [0, 1])
        self.accept("arrow_down", self.move_player, [0, -1])
        self.accept("arrow_left", self.move_player, [-1, 0])
        self.accept("arrow_right", self.move_player, [1, 0])
        self.accept("space", self.place_bomb)

        self.enemy = self.loader.loadModel("models/smiley")
        self.enemy.reparentTo(self.render)
        self.enemy.setScale(0.2)
        self.enemy.setPos(random.randint(-5, 5), random.randint(-5, 5), 0)

    def move_player(self, dx, dy):
        new_pos = self.player.getPos() + Point3(dx, dy, 0)
        self.player.setPos(new_pos)

    def place_bomb(self):
        bomb = self.loader.loadModel("models/misc/sphere")
        bomb.reparentTo(self.render)
        bomb.setScale(0.2)
        bomb.setPos(self.player.getPos())
        self.bombs.append(bomb)
        self.taskMgr.doMethodLater(2, self.explode_bomb, "explode", extraArgs=[bomb], appendTask=True)

    def explode_bomb(self, bomb, task):
        bomb.removeNode()
        self.bombs.remove(bomb)
        return Task.done


if __name__ == "__main__":
    game = BomberGame()
    game.run()
