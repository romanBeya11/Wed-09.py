# Created by: Mr. Coxall
# Created on: Sep 2016
# Created for: ICS3U
# Updated by: Roman Beya
# Updated on: 4-Oct-2017
# Updated for: ICS3U
# Updated by: Roman Beya
# Updated on: 11-Oct-2017
# Updated for: ICS3U
# Updated by: Roman Beya
# Updated on: 18-Oct-2017
# Updated for: ICS3U
# Updated by: Roman Beya
# Updated on: 25-Oct-2017
# Updated for: ICS3U
# Updated by: Roman Beya
# Updated on: 1-Nov-2017
# Updated for: ICS3U
# This scene shows the main game.

from scene import *
import ui
from numpy import random

class GameScene(Scene):
    def setup(self):
        # this method is called, when user moves to this scene
        
        # updated to not use deepcopy
        self.size_of_screen_x = self.size.x
        self.size_of_screen_y = self.size.y
        self.screen_center_x = self.size_of_screen_x/2
        self.screen_center_y = self.size_of_screen_y/2
        
        self.left_button_down = False
        self.right_button_down = False
        self.ship_move_speed = 20.0
        self.missiles = []
        self.aliens = []
        self.alien_attack_rate = 1  
        self.alien_attack_speed = 20.0
        self.scale_size = 0.75
        
        # add background color
        background_position = Vector2(self.screen_center_x, 
                                      self.screen_center_y)
        self.background = SpriteNode('./assets/sprites/star_background.PNG',
                                     position = background_position, 
                                     parent = self, 
                                     size = self.size)
                                     
        spaceship_position = Vector2()
        spaceship_position.x = self.screen_center_x
        spaceship_position.y = 100
        self.spaceship = SpriteNode('./assets/sprites/spaceship.PNG',
                                    parent = self,
                                    position = spaceship_position,
                                    scale = self.scale_size)
                                       
        left_button_position = Vector2()
        left_button_position.x = 100
        left_button_position.y = 100
        self.left_button = SpriteNode('./assets/sprites/left_button.PNG',
                                      parent = self,
                                      position = left_button_position,
                                      alpha = 0.5,
                                      scale = self.scale_size)
                                       
        right_button_position = Vector2()
        right_button_position.x = 300
        right_button_position.y = 100
        self.right_button = SpriteNode('./assets/sprites/right_button.PNG',
                                       parent = self,
                                       position = right_button_position,
                                       alpha = 0.5,
                                       scale = self.scale_size)
                                       
        fire_button_position = Vector2()
        fire_button_position.x = self.size_of_screen_x - 100
        fire_button_position.y = 100
        self.add_alien()
        self.fire_button = SpriteNode('./assets/sprites/red_button.PNG',
                                      parent = self,
                                      position = fire_button_position,
                                      alpha = 0.5,
                                      scale = self.scale_size)
        
        self.score_position.x = 100
        self.score_position.y = self.size_of_screen_y - 50
        self.score_label = LabelNode(text = 'Score: 0',
                                     font=('Helvetica', 40),
                                     parent = self,
                                     position = self.score_position)
        
        
    def update(self):
        # this method is called, hopefully, 60 times a second
        
        # move spaceship if button down
        if self.left_button_down == True:
            spaceshipMove = Action.move_by(-1*self.ship_move_speed, 
                                           0.0, 
                                           0.1)
            self.spaceship.run_action(spaceshipMove)
        
        if self.right_button_down == True:
            spaceshipMove = Action.move_by(self.ship_move_speed, 
                                           0.0, 
                                           0.1)
            self.spaceship.run_action(spaceshipMove)
        
        # every update, randomly check if a new alien should be created
        alien_create_chance = random.randint(1, 120)
        if alien_create_chance <= self.alien_attack_rate:
            self.add_alien()
            
        # check every update if a missile is off screen
        for missile in self.missiles:
            if missile.position.y > self.size_of_screen_y + 50:
                missile.remove_from_parent()
                self.missiles.remove(missile)
                
        
        # check every update if an alien is off screen
        
        for alien in self.aliens:
            if alien.position.y < -50:
                alien.remove_from_parent()
                self.aliens.remove(alien)
                
        
        # check every update to see if a missile has touched a space alien
        if len(self.aliens) > 0 and len(self.missiles) > 0:
            
            for alien in self.aliens:
                for missile in self.missiles:
                    if alien.frame.contains_rect(missile.frame):
                        missile.remove_from_parent()
                        self.missiles.remove(missile)
                        alien.remove_from_parent()
                        self.aliens.remove(alien)
                        self.score = self.score + 1
                        
        else:
            pass
            
        
        # check every update to see alien touches spaceship
        if len(self.aliens) > 0:
            
            for alien_hit in self.aliens:
                if alien_hit.frame.intersects(self.spaceship.frame):
                    self.spaceship.remove_from_parent()
                    alien_hit.remove_from_parent()
                    self.aliens.remove(alien_hit)
                  
        else:
            pass
    
    def touch_began(self, touch):
        # this method is called, when user touches the screen
        
        # check if left or right button is down
        if self.left_button.frame.contains_point(touch.location):
            self.left_button_down = True
        
        if self.right_button.frame.contains_point(touch.location):
            self.right_button_down = True
    
    def touch_moved(self, touch):
        # this method is called, when user moves a finger around on the screen
        pass
    
    def touch_ended(self, touch):
        # this method is called, when user releases a finger from the screen
        
        # if start button is pressed, goto game scene
        if self.fire_button.frame.contains_point(touch.location):
              self.create_new_missile()
        else:
            # if I removed my finger, then no matter what spaceship
            #    should not be moving any more
            self.left_button_down = False
            self.right_button_down = False
    
    def did_change_size(self):
        # this method is called, when user changes the orientation of the screen
        # thus changing the size of each dimension
        pass
    
    def pause(self):
        # this method is called, when user touches the home button
        # save anything before app is put to background
        pass
    
    def resume(self):
        # this method is called, when user place app from background 
        # back into use. Reload anything you might need.
        pass
    
    def create_new_missile(self):
        # when the user hits the fire button
        
        missile_start_position = Vector2()
        missile_start_position.x = self.spaceship.position.x
        missile_start_position.y = 100
        
        missile_end_position = Vector2()
        missile_end_position.x = missile_start_position.x
        missile_end_position.y = self.size_of_screen_y + 100
        
        self.missiles.append(SpriteNode('./assets/sprites/missile_image.PNG',
                             position = missile_start_position,
                             parent = self))
        
        # make missile move forward
        missileMoveAction = Action.move_to(missile_end_position.x, 
                                           missile_end_position.y + 100, 
                                           5.0)
        self.missiles[len(self.missiles)-1].run_action(missileMoveAction)
        
    def add_alien(self):
        # add a new alien to come down
        
        alien_start_position = Vector2()
        alien_start_position.x = random.randint(100, 
                                         self.size_of_screen_x - 100)
        alien_start_position.y = self.size_of_screen_y + 100
        
        alien_end_position = Vector2()
        alien_end_position.x = random.randint(100, 
                                        self.size_of_screen_x - 100)
        alien_end_position.y = -100
        
        self.aliens.append(SpriteNode('./assets/sprites/alien.PNG',
                             position = alien_start_position,
                             parent = self))
        
        # make missile move forward
        alienMoveAction = Action.move_to(alien_end_position.x, 
                                         alien_end_position.y, 
                                         self.alien_attack_speed,
                                         TIMING_SINODIAL)
        self.aliens[len(self.aliens)-1].run_action(alienMoveAction)
