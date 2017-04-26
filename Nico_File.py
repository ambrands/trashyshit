from psychopy import core, visual,event, logging, gui, data 
import time, glob, codecs
import csv
import os
import pandas as pd
import numpy
from numpy import random

#----------------------------------------------
# DIRECTORY, PARTICIPANT INFO (and other stuff)
#----------------------------------------------
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'Nico_File'
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
filename = _thisDir + os.sep + 'data/%s_%s_' %(expInfo['participant'], expName)

#----------------------------------------------
# DEFINING STUFF
#----------------------------------------------
expFile=pd.read_csv('stimFileAngela'+'.csv', delimiter = ';')
win = visual.Window([800,800], monitor="testMonitor",units="cm")
answerKeys = ["x","m"]
rightKey = "m"
leftKey = "x"
validResponses = ['m','x']
blockDur=6
startBlock=1
endBlock=4
startPracTrial=0
endPracTrial=16
startTrial=17
endTrial=81
blockDur=64
subNum = expInfo['participant']
nframes=list(expFile ['framerate'])
nframes= list(nframes)
trialNo=0
tarPresent=list(expFile['targetPresent'])
correctText = visual.TextStim(win,text='O', height=4, color='green',pos=[0,0])
incorrectText = visual.TextStim(win,text='X', height=4, color='red',pos=[0,0])
welcome= visual.TextStim(win, text='Hey good lookin', height=1, color='black')
instructionPrac= visual.TextStim(win, text='here are some practice trials for you', height=1, color='black')
instructionTrials= visual.TextStim(win, text='now lets get to the actual thing, so you better concentrate now', height=1, color='black')

#----------------------------------------------
# FIXATION CROSS
#----------------------------------------------
def drawFixation(win):
    # fixation cros
    fixation = visual.ShapeStim(win, 
        vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
        lineWidth= 2,
        closeShape=False,
        lineColor='White')
    fixation.draw()
    win.flip()
    # draw a waiting time between 900 and 2100 ms
    waitTime = 0.001*random.randint(400,600)
    core.wait(waitTime)
    # check for quit (the Esc key)
    if event.getKeys(keyList=["escape"]):
        core.quit()

#----------------------------------------------
# BLANK
#----------------------------------------------
def presentBlank (win):
    blank = visual.ShapeStim(win, 
        vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
        lineWidth=5,
        closeShape=False,
        lineColor='grey')
    blank.draw()
    win.flip()
    waitTime = 0.001*random.randint(200,600)
    core.wait(waitTime)

#----------------------------------------------
#CONFIDENCE SCALE
#----------------------------------------------
def presentScale(win):
    confidence = visual.TextStim(win, text='Wie sicher bist du dir bei dieser Entscheidung auf einer Skala von 0 bis 9? (Eingabe per Tastatur)', color = 'black', height=1)
    confidence.draw()
    win.flip()
    d=event.waitKeys(keyList=('0','1','2','3','4','5','6','7','8','9'), maxWait=3)
    if d:
        win.flip()
        core.wait(.5)

#psychopy tutorial (psychopy site event wait keys)

#----------------------------------------------
# PRESENT PICTURES & TEST IMAGE
#----------------------------------------------
def presentStimuli (win, aStimuli, nframes):
    pic=visual.ImageStim(win, image=str(aStimuli))
    for frame in str(nframes):
        pic.draw()
        win.flip()

def presentTestImage (win, aTest):
    testImage= visual.ImageStim(win, image=str(aTest))
    testImage.draw()
    win.flip
    core.wait(0.4)
    win.flip()
    c = event.waitKeys(maxWait = 60 , keyList = ["m","x"])
    if event.getKeys (keyList =["escape"]):
        core.quit()
    if c:
        return c[0]
    else:
        return ''
    if event.waitKeys(keyList=(rightKey,leftKey), maxWait=2):
        win.flip()
        core.wait(.5)

#----------------------------------------------
# TRIALS
#----------------------------------------------
def runTrials (win,presentStimuli,presentTestImage, drawFixation, presentBlank, expFile, presentScale):
    outputFile = open(filename+'out'+'.csv','w')
    outputFile.write("time,subject,stimuli,trialNo,tarPresent,RT,response,responseCorrect,responseConfidence")
    outputFile.write("\n")
    #weitere for-loop für Blöcke 
    if blockNum=='1':
        startTrial=17
        endTrial=81
    if blockNum=='2':
        
    for i in range(startTrial,endTrial):
        global trialNo
        trialNo = trialNo + 1
        stimuli = expFile['targetPic']
        tarPresent = expFile['targetPresent']
        expFile = pd.read_csv('stimFileAngela.csv', delimiter = ';')
        pic1 =expFile['pic1']
        pic2 =expFile['pic2']
        pic3 =expFile['pic3']
        pic4 =expFile['pic4']
        pic5 =expFile['pic5']
        pic6 =expFile['pic6']
        drawFixation(win)
        before = time.time()
        presentStimuli(win,pic1[i],nframes[i])
        presentStimuli(win,pic2[i],nframes[i])
        presentStimuli(win,pic3[i],nframes[i])
        presentStimuli(win,pic4[i],nframes[i])
        presentStimuli(win,pic5[i],nframes[i])
        presentStimuli(win,pic6[i],nframes[i])
        after= time.time()
        PT = float(after - before)
        presentBlank(win)
        test = expFile['targetPic']
        trialTest= presentTestImage(win, test[i])
        presentScale(win)
        if ((tarPresent[i]==1) & (trialTest[0]=='m')):
           responseCorrect = 1
        else:
           responseCorrect = 0
        if responseCorrect== 1:
            correctText.draw()
        else:
            incorrectText.draw()
        win.flip()
        core.wait(1)
        outputFile.write("{},{},{},{},{},{},{},{},{}\n".format(int(before),subNum,stimuli[i],trialNo,tarPresent[i],"{:.3f}".format(PT),trialTest,responseCorrect,responseConfidence))
    presentBlank(win)
#----------------------------------------------
# PRACTICE TRIALS 
#----------------------------------------------
def runPracTrial (win, presentStimuli, presentTestImage, drawFixation, presentBlank, presentScale):
    for i in range (startPracTrial, endPracTrial):
        expFile = pd.read_csv('stimFileAngela.csv', delimiter = ';')
        pic1 =expFile['pic1']
        pic2 =expFile['pic2']
        pic3 =expFile['pic3']
        pic4 =expFile['pic4']
        pic5 =expFile['pic5']
        pic6 =expFile['pic6']
        drawFixation(win)
        presentStimuli(win,pic1[i],nframes[i])
        presentStimuli(win,pic2[i],nframes[i])
        presentStimuli(win,pic3[i],nframes[i])
        presentStimuli(win,pic4[i],nframes[i])
        presentStimuli(win,pic5[i],nframes[i])
        presentStimuli(win,pic6[i],nframes[i])
        presentBlank(win)
        test = expFile['targetPic']
        trialTest= presentTestImage(win, test[i])
        presentScale(win)
        if ((tarPresent[i]==1) & (trialTest[0]=='m')):
           responseCorrect = 1
        else:
           responseCorrect = 0
        if responseCorrect== 1:
            correctText.draw()
        else:
            incorrectText.draw()
        win.flip()
        core.wait(1)
    presentBlank(win)

#-------------------------------------------------------
# BLOCKS (incl. trials, practrials & writing outputfile)
#-------------------------------------------------------
def runBlocks (win, runTrials, runPracTrial):
    instructionPrac.draw()
    win.flip()
    core.wait(3)
    runPracTrial(win, presentStimuli, presentTestImage, drawFixation, presentBlank, presentScale)
    instructionTrials.draw()
    win.flip()
    core.wait(3)
    for i in range (startBlock, endBlock):
        runTrials (win,presentStimuli,presentTestImage,drawFixation, presentBlank, expFile, presentScale)

#----------------------------------------------
# DOING THE ACTUAL EXPERIMENT 
#----------------------------------------------
if (int(subNum) % 2 == 0):
    startBlock = 2
    endBlock = 4
else:
    startBlock = 1
    endBlock = 3

# Bilder laden 
runBlocks(win, runTrials, runPracTrial)

# Say Thank you!
Text = visual.TextStim(win,text='BoOOom',units='norm',height = 0.1,color="black")
Text.draw()
win.flip()
core.wait(5)

# Close the window
win.close()
core.quit()
