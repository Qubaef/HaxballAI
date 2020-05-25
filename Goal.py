import pygame
from Post import Post
from Collision import Collision

class Goal( object ):
    def __init__(self, game, color, p_post_x, p_post_y_up, p_post_y_down, width, direction):
        self.game = game
        self.color = color
        self.x = p_post_x
        self.y_up = p_post_y_up
        self.y_down = p_post_y_down
        self.width = width
        self.direction = direction

        # initialize Posts
        self.post_up = Post(self.game, self.x, self.y_up)
        self.post_down = Post(self.game, self.x, self.y_down)


    def goal_collide(self):
        Collision.collide(self.post_up)
        Collision.collide(self.post_down)
        

    def get_px(self):
        return self.x + self.direction * self.width


    def get_py(self):
        return self.y_up


    def get_width(self):
        return self.width


    def get_height(self):
        return self.y_down - self.y_up


    def get_dist(self, position_vector):
        if position_vector.y > self.y_up:
            return (position_vector - self.post_up.p).length()
        elif position_vector.y < self.y_down:
            return (position_vector - self.post_down.p).length()
        else:
            return (position_vector - pygame.math.Vector2(self.x,self.y_up + int(width/2))).length()


    def get_angle(self, ball_p, ball_v):
        # if ball is going towards this goal (with v > 0.5), return 1
        # if ball is going somewhere else, return number based on angle (min is -1)

        vec_post_1 = self.post_up.p - ball_p
        vec_post_2 = self.post_down.p - ball_p

        default = pygame.math.Vector2(1,0)

        a1 = ball_v.angle_to(default)
        a2 = ball_v.angle_to(default)
        b = ball_v.angle_to(ball_v)

        if b > a1 and b < a2:
            return 1
        else:
            return 0



