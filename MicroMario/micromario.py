from microbit import *


#A 2 dimensional array representing our "level". 1s represent hard blocks and 0s can be walked through.
#There is one exception; a single 9 which represents the goal
terrain = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0],
[0,0,1,1,0,1,1,1,0,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0],
[0,0,1,1,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,9,0,1,0,0]
]

#Represents our position in each line of the array
pos = 0

#Boolean that is set to true only when you've reached the goal
gameComplete = False

#Boolean telling us if we can or can't jump
canJump = True

#Boolean telling us if we've in the up part of a jump
jumpUp = False

#Used to record the time that the last jump action happened. This is used to ensure the jump animation runs at a differnt speed to the main game loop
lastJumpTime = 0

#Storage for the previous "frame" of the game
lline = ["00000","00000","00000","00000","00000"]

#X and Y location for the dot presenting the player
manX = 1
manY = 1

#Maximum number of dots the player can jump
jumpHeightMax = 2

#The current height of any jump that is happening
jumpHeight = 0


#Useful method for changing the value at a given position in a String
def alterString(str, pos, value):
    chars = list(str)
    chars[pos] = value
    return "".join(chars)

#Useful method for checking for a given value at a position in a String
def checkString(str, pos, value):
    chars = list(str)
    if(chars[pos] == value):
        return True
    return False

#The main "game" loop
while True:
    
    #Break out of the loop if the game is complete
    if gameComplete:
        break

    #This array of strings represents the current frame of the game, we'll change them depending on terrain and player location
    line = ["00000","00000","00000","00000","00000"]

    #Do the following if we've pressed the A button and we are currently able to jump
    if (button_a.is_pressed() and canJump):
        canJump = False
        jumpUp = True
        jumpHeight = 0

    #If the B button is pressed...
    elif button_b.is_pressed():

        #...make sure the position to the right is clear of blocks
        if(not checkString(lline[5-manY], manX+1, "6")):
            pos = pos+1

    #Get a copy of the position in the level   
    x = pos

    #Use an offset to include all of the level current visible on the screen
    offset = 0

    #Begin iteration of all visible parts of the level
    while(offset<5):
        
        #If we're early in the level, there might be nothing of the previous level to show
        if((x-offset)<0):
            break
        
        #Get a position to draw
        offsetx = (x - offset)
        imagePos = (4 - offset)

        #Iterate each row of the terrain and examine the it
        for index in range(5):
            block = terrain[index][offsetx]

            #If the block is marked as being solid (with a 1) then we set the led to a 6 brightness
            if(block==1):
                line[index] = alterString(line[index], imagePos, "6")

            #If the player has reached the goal then complete the game
            if(block==9 and manX == imagePos):
                gameComplete = True

        #Mark the location of the player with a 9 brightness
        line[5-manY] = alterString(line[5-manY], manX, "9")

        #Increment the offset to extend one position further back in the image
        offset = offset +1
        

    #If we're jumping up and we're ready to show a bit more of the jump animation...
    if(jumpUp and ((running_time()-lastJumpTime) > 150)):

        #Check we can continue out way up
        check = checkString(line[5-manY-1],manX,"6")

        #If we can continue jumping and we've not hit the roof yet the increment the player's Y position and the current jump height
        if(manY<5 and not check):
           manY += 1
           jumpHeight += 1

        #Have we hit the roof or hit the maximum jump height? If so the up part of the jump is done
        if(manY==5 or check or (jumpHeight==jumpHeightMax)):
           jumpUp = False

        #Record the time
        lastJumpTime = running_time()

    #As long as we're not jumping up then we need to ensure "gravity" attempts to pull the player down
    elif(not jumpUp and ((running_time()-lastJumpTime) > 150)):

        #Are we standing on something?
        check = False
        if(manY > 1):
            check = checkString(line[5-manY+1], manX, "6")
        
        #If we're stood on something then we are ready to jump again
        if(manY == 1 or check):
           canJump = True
        
        #If we're in freefall then we can't jump
        else:
           canJump = False
           manY = manY - 1
        
        #All part of the jump animation so record the time
        lastJumpTime = running_time()
        
    #We're finally is a position to draw frame
    display.show(Image(line[0]+":"+line[1]+":"+line[2]+":"+line[3]+":"+line[4]))

    #Slow the loop just slightly
    sleep(50)
    
    #Reciord the last frame
    lline = line

#Game eneded then show the generic happy face 
display.show(Image.HAPPY)