import asyncio
import platform
import pygame
import random
from pygame.locals import *
import math
def load_words(topic):
    if topic.lower()=='a':
        filename="animals.txt" #Change "animals.txt" to wherever your "animals.txt" is located
    elif topic.lower()=='f':
        filename="fruits.txt" #Change "fruits.txt" to wherever your "fruits.txt" is located
    else:
        return None
    try:
        with open(filename,"r") as f:
            return f.read().split()
    except FileNotError:
        print(f"Error: {filename} not found!")
        return None
pygame.init()
initial_width,initial_height=1440,1020
clock=pygame.time.Clock()
font=pygame.font.Font(None,50)
big_font=pygame.font.Font(None,200)
try:
    original_hang_images=[
        pygame.image.load("Open.png"), #Change "Open.png" to wherever your "Open.png" is located
        pygame.image.load("OpenHead.png"), #Change "OpenHead.png" to wherever your "OpenHead.png" is located
        pygame.image.load("OpenHeadBody.png"), #Change "OpenHeadBody.png" to wherever your "OpenHeadBody.png" is located
        pygame.image.load("OpenHeadBodyLArm.png"), #Change "OpenHeadBodyLArm.png" to wherever your "OpenHeadBodyLArm.png" is located
        pygame.image.load("OpenHeadBodyBothArms.png"), #Change "OpenHeadBodyBothArms.png" to wherever your "OpenHeadBodyBothArms.png" is located
        pygame.image.load("OpenHeadBodyBothArmLLeg.png"), #Change "OpenHeadBodyBothArmLLeg" to wherever your "OpenHeadBodyBothArmLLeg" is located
        pygame.image.load("OpenFullBody.png") #Change "OpenFullBody.png" to wherever your "OpenFullBody.png" is located
    ]
    original_title_image=pygame.image.load("CloseTitleScreen.png") #Change "CloseTitleScreen.png" to wherever your "CloseTitleScreen.png" is located
    original_exit_image=pygame.image.load("Exit Screen.png") #Change "Exit Screen.png" to wherever your "Exit Screen.png" is located
    original_background_image=pygame.image.load("BG.png") #Change "BG.png" to wherever your "BG.png" is located
    original_blank_tile=pygame.image.load("dashes.png") #Change "dashes.png" to wherever your "dashes.png" is located
    original_splash_image=pygame.image.load("Splash.png") #Change "Splash.png" to wherever your "Splash.png" is located
    original_gameover_image=pygame.image.load("Game Over Screen.png") #Change "Game Over Screen.png" to wherever your "Game Over Screen.png" is located
    original_yes_button=pygame.image.load("yes_button.png") #Change "yes_button.png" to wherever your "yes_button.png" is located
    original_no_button=pygame.image.load("no_button.png") #Change "no_button.png" to wherever your "no_button.png" is located
except Exception as e:
    print(e)
    pygame.quit()
    exit()
yes_button=pygame.transform.scale(original_yes_button,(200,80))
no_button=pygame.transform.scale(original_no_button,(200,80))
background_image=pygame.transform.scale(original_background_image,(initial_width,initial_height))
hang_images=[pygame.transform.scale(img,(initial_width,initial_height)) for img in original_hang_images]
title_image=pygame.transform.scale(original_title_image,(initial_width,initial_height))
exit_image=pygame.transform.scale(original_exit_image,(initial_width,initial_height))
blank_tile=pygame.transform.scale(original_blank_tile,(84,11))
splash_image=pygame.transform.scale(original_splash_image,(initial_width,initial_height))
gameover_image=pygame.transform.scale(original_gameover_image,(initial_width,initial_height))
play_rect=pygame.Rect(993,478,338,139)
exit_rect=pygame.Rect(993,653,338,139)
yes_rect=pygame.Rect(236,653,354,152)
no_rect=pygame.Rect(899,653,354,152)
play_again_rect=pygame.Rect(400,600,200,80)
exit_game_rect=pygame.Rect(700,600,200,80)
def draw_text(text,font,color,surface,x,y,outline_colour=None,outline_width=2):
    text_obj=font.render(text,True,color)
    text_rect=text_obj.get_rect(topleft=(x,y))
    if outline_colour:
        outline_text=font.render(text,True,outline_colour)
        for dx in range(-outline_width,outline_width+1):
            for dy in range(-outline_width,outline_width+1):
                if dx!=0 or dy!=0:
                    surface.blit(outline_text,(text_rect.x+dx,text_rect.y+dy))
    surface.blit(text_obj,text_rect)
def main():
    screen=pygame.display.set_mode((initial_width,initial_height))
    pygame.display.set_caption("Henry Hangman")
    running=True
    state="title"
    topic=None
    secret_word=None
    missed_letters=[]
    correct_letters=[]
    guessed_letters=[]
    max_attempts=len(hang_images)-1
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                running=False
            if event.type==MOUSEBUTTONDOWN:
                if state=="title":
                    if play_rect.collidepoint(event.pos):
                        state="choose_topic"
                    elif exit_rect.collidepoint(event.pos):
                        state="exit_confirm"
                elif state=="exit_confirm":
                    if yes_rect.collidepoint(event.pos):
                        running=False
                    elif no_rect.collidepoint(event.pos):
                        state="title"
                elif state in ["win","lose"]:
                    if play_again_rect.collidepoint(event.pos):
                        state="choose_topic"
                    elif exit_game_rect.collidepoint(event.pos):
                        running=False
            if event.type==KEYDOWN:
                if state=="choose_topic":
                    if event.key==K_a:
                        topic="a"
                        words=load_words(topic)
                        if words:
                            secret_word=random.choice(words).lower()
                            missed_letters,correct_letters,guessed_letters=[],[],[]
                            word_length=len(secret_word)
                            max_width=336
                            initial_tile_width=blank_tile.get_width()+10
                            max_tiles_per_line=math.floor(max_width/initial_tile_width)
                            if word_length > max_tiles_per_line:
                                min_width=20
                                new_width=max(min_width,max_width/word_length-10)
                                new_height=(11.24/83.71)*new_width
                                scaled_blank_tile=pygame.transform.scale(blank_tile,(int(new_width),int(new_height)))
                            else:
                                scaled_blank_tile=blank_tile
                            state="game"
                    elif event.key==K_f:
                        topic="f"
                        words=load_words(topic)
                        if words:
                            secret_word=random.choice(words).lower()
                            missed_letters,correct_letters,guessed_letters=[],[],[]
                            word_length=len(secret_word)
                            max_width=336
                            initial_tile_width=blank_tile.get_width()+10
                            max_tiles_per_line=math.floor(max_width/initial_tile_width)
                            if word_length > max_tiles_per_line:
                                min_width=20
                                new_width=max(min_width,max_width/word_length-10)
                                new_height=(11.24/83.71)*new_width
                                scaled_blank_tile=pygame.transform.scale(blank_tile,(int(new_width),int(new_height)))
                            else:
                                scaled_blank_tile=blank_tile
                            state="game"
                elif state=="game":
                    if K_a <= event.key <= K_z:
                        guess=chr(event.key).lower()
                        if guess not in guessed_letters:
                            guessed_letters.append(guess)
                            if guess in secret_word:
                                correct_letters.append(guess)
                            else:
                                missed_letters.append(guess)
        if state in ["choose_topic","win","lose"]:
            screen.blit(background_image,(0,0))
        if state=="title":
            screen.blit(title_image,(0,0))
        elif state=="exit_confirm":
            screen.blit(exit_image,(0,0))
            draw_text("ARE YOU SURE",big_font,(248,213,123),screen,300,200)
            draw_text("You want to leave Henry hanging?",font,(248,213,123),screen,300,300)
        elif state=="choose_topic":
            screen.blit(splash_image,(0,0))
        elif state=="game":
            stage=min(len(missed_letters),max_attempts)
            screen.blit(hang_images[stage],(0,0))
            word_length=len(secret_word)
            tile_width=blank_tile.get_width()+10
            max_width=600
            max_tiles_per_line=math.floor(max_width/tile_width)
            scaled_blank_tile=blank_tile
            if word_length > max_tiles_per_line:
                new_width=max(20,max_width/word_length-10)
                new_height=(11.24/83.71)*new_width
                scaled_blank_tile=pygame.transform.scale(original_blank_tile,(int(new_width),int(new_height)))
            x_offset=200
            y_offset=300
            for i,letter in enumerate(secret_word):
                current_x=x_offset+(i % max_tiles_per_line)*(scaled_blank_tile.get_width()+5)
                current_y=y_offset+(i // max_tiles_per_line)*(scaled_blank_tile.get_height()+100)
                if letter in correct_letters:
                    draw_text(letter.upper(),font,(30,30,30),screen,current_x,current_y)
                else:
                    screen.blit(scaled_blank_tile,(current_x,current_y))
            draw_text("Missed: "+" ".join(missed_letters).upper(),font,(0,0,0),screen,x_offset,y_offset+250)
            if all(c in correct_letters for c in secret_word):
                state="win"
            elif len(missed_letters) >= max_attempts:
                state="lose"
        elif state in ["win","lose"]:
            screen.blit(gameover_image,(0,0))
            if state=="win":
                draw_text("YOU WIN!",big_font,(248,213,123),screen,350,150,outline_colour=(0,0,0),outline_width=2)
                draw_text(f"The word was: {secret_word.upper()}",font,(248,213,123),screen,550,470)
            else:
                draw_text("YOU LOSE!",big_font,(248,213,123),screen,350,150,outline_colour=(0,0,0),outline_width=2)
                draw_text(f"The word was: {secret_word.upper()}",font,(248,213,123),screen,550,470)
            screen.blit(yes_button,(play_again_rect.x,play_again_rect.y))
            screen.blit(no_button,(exit_game_rect.x,exit_game_rect.y))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if platform.system()=="Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__=="__main__":
        asyncio.run(main())
