from random import choice

'''Salt Analysis via a code typed into the IDLE
            
Hard-coding everything
Heavy usage of dictionaries'''

#a help message
helpMsg = '''Use the given code words to do a certain task for finding out the given salt.
All chemicals should be referred to by their chemical formula.
Intensity of heating code words are listed below.

Intensity Code:-
Intensity          : Codename
Heat Very Strongly : strong
Heat Very Slightly : slight

The code is case sensitive. There should a space between every single key word. It removes any unnecessary spaces/symbols from yout input.
Note: wherever you want to add the given salt as the chemical, use the keyword salt.

All functions:
'new' :- Picks a new salt. If used while an old salt is still being analysed, it deducts a massive amount of points and gives you the answer.

'list *' :- Prints a list of all the chemicals. If u put a specific category instead of *, then it lists out all chemicals in that category
            a. 'acids' :- Lists out all acids
            b. 'reag' :- Lists out all special reagents and indicators
            c. 'misc' :- Miscellanoeus stuff like water, paper pellets, etc

'add <chemical name> [in <tube>]' :- adds the chemical in the specified test tube. Test tube not specified, then adds to last used test tube. Can add contents of one test tube into the other, specify test tube number rather than chemical name.

'heat [<tube> [<intensity>]] :- heats the mentioned test tube (default test tube is the last used one) with a given intensity (slight heating by default)

'flame test' :- Carries out flame test on your given salt

'guess <ion> is <name>' :- Give your guess for the specified ion ('cation' or 'anion'). If right, gain points. If wrong lose points.

'pass in <tube>' :- Pass the evolved gas in the previous reaction into a specified test tube

'introduce <chemical> [to <tube>]' :- Introduce the chemical to the test tube (default test tube is last one used) by a glass rod

'create SE' :- Create the Sodium Carbonate Extract

'create WE' :- Create the Water Extract

'create OS' :- Create the Original Salt Solution

'quit' :- Quit out of Salt Analysis Emulator. Gives you the answer to the old salt, if a salt is stil being analysed.

'new tube' :- Take a new test tube

Here, test tubes also refer to boiling tubes, so don't worry about that.
Also there is no limit to the number of test tubes you can take.
If you want information as to a certain test, please refer to your lab manual :)''' 

def codeError():
    print 'ERROR! Please recheck what you have typed'

def Quit():
    if salt != [None, None]:
        ch = raw_input('Are you sure? Press y to proceed, anything else to return>>> ').lower()
        if ch == 'y': print 'The salt was' , saltFormula()
        else: return
    print 'THANK YOU FOR USING THE SALT ANALYSIS EMULATOR.'
    quit()

def printtubes():
    for i in range(len(tubes)):
        if not tubes[i] == []:
            if None in tubes[i]: print 'Test Tube', i+1, ' has nothing'
            else:
                output = 'Test Tube ' + str(i+1) + ' has'
                for chemical in tubes[i]:
                     output += (' ' + str(chemical) + ',')
                if heatedflags[i]: print output[:-1] + '. It has been heated', ('slightly' if heatedflags[i] == 1 else 'strongly')
                else: print output[:-1]
    print 'Current Test Tube:' , currenttubeindex + 1
#ALL CHEMICALS LISTS
acids_list = [{'dil_HCl':'Diluted Hydrochloric acid'}, {'conc_HCl':'Concentrated Hydrochloric acid'},
              {'dil_H2SO4':'Diluted Sulphuric acid'}, {'conc_H2SO4':'Concentrated Sulphuric acid'},
              {'dil_HNO3':'Diluted Nitric acid'}, {'conc_HNO3':'Concentrated Nitric acid'}, {'CH3COOH':'Acetic Acid'}]
misc_list = [{'water':'water'}, {'paper':'Paper Pellets'}, {'LApaper':'Lead Acetate paper'}, {'ADpaper':'Acidified Dichromate Paper'},
             {'Moist Starch Paper':'MSpaper'}, {'Moist Starch Iodide Paper':'MSIpaper'}, {'Moist Blue Litmus Paper':'MBLpaper'}]
# Add more reagents specific to certain tests for new cations/anions
reag_list = [{'NH4OH':'Ammonium hydroxide'}]

acids = [acid.keys()[0] for acid in acids_list]
misc = [misc.keys()[0] for misc in misc_list]
reagents = [reag.keys()[0] for reag in reag_list]

def List(category):
    if category == '*':
        print 'ACIDS:'
        for chemical in acids:
            print chemical , ' - ', acids_list[chemical]
        print'\nREAGENTS'
        for chemical in reagents:
            print chemical , ' - ', reag_list[chemical]
        print '\nMISCELLANEOUS'
        for chemical in misc:
            print chemical , ' - ', misc_list[chemical]
    elif category == 'acids':
        for chemical in acids:
            print chemical , ' - ', acids_list[chemical]
    elif category == 'misc':
        for chemical in misc:
            print chemical , ' - ', misc_list[chemical]
    elif category == 'reag': 
        for chemical in reagents:
            print chemical , ' - ', reag_list[chemical]

def saltFormula():  #write code to return the formula as string
    return salt[0]['name'] + ' ' + salt[1]['name'] 

def newSalt():
    global salt, saltflag, tubes
    if salt != [None, None]:
        ch = raw_input('Are you sure? Press y to proceed, anything else to exit>>> ').lower()
        if ch == 'y':
            print 'The salt was' , saltFormula()
        else: return
    salt[0] = choice(cations)
    salt[1] = choice(anions)
    print
    print 'A salt has been chosen'
    if salt[0]['colour'] != None: print 'Colour -' , salt[0]['colour'], 'Smell'
    else: print 'No recognizable colour'
    if salt[0]['odour'] != None: print 'Odour -' , salt[0]['odour'], 'Smell'
    elif salt[1]['odour'] != None: print 'Odour -' , salt[1]['odour'], 'Smell'
    else: print 'No recognizable odour'
    print
    tubes = [[None]]
    saltflag = [False, False]

def add(chemical, index = None):
    global currenttubeindex, tubes
    if index == None: index = currenttubeindex
    if chemical[0] == 't': #if adding one test tube into another
        emptiedindex = int(chemical[-1])
        tubes[index].extend(tubes[emptiedindex])
        if index > emptiedindex: currenttubeindex = index - 1
        else: currenttubeindex = index
        del tubes[emptiedindex]
        return
    if not (chemical in reagents or chemical in acids or chemical in misc or chemical == 'salt'): return 'error'
    if tubes[index] == [None]: tubes[index] = [chemical]
    else: tubes[index].append(chemical)
    currenttubeindex = index

#Actual loop for taking inputs-
print '''WELCOME TO SALT ANALYSIS EMULATOR!

A randomly generated salt is analyzed via a simple code

To find out about the syntax for the code, type help.
If you want to start analysing a salt, type new'''

#Dictionary for each cation/anion
#anions:
carbonate = {'name':'carbonate', 'type':'anion', 'formula':'CO3', 'valency':2, 'odour':None}
anions = [carbonate]
#cations
ammonium = {'name':'Ammonium', 'type':'cation', 'formula':'NH4', 'valency':1, 'odour':'Ammoniacal', 'flame':None, 'colour':None} 
cations = [ammonium]


salt = [None, None]  #Use this as a flag to check whether new salt has been picked
saltflag = [False, False]
heatedflags = [0]  #0 - Not heated, 1 - slightly heated, 2 - strongly heated
tubes = [list()]
currenttubeindex = 0

while True:
    print
    codestring = raw_input('Enter code line >>> ').rstrip().lstrip()
    code = codestring.split()  #retreive individual keyword
    code = [word for word in code if word.isalnum() or word == '*' or \
            (word in reagents or word in acids or word in misc or word == 'salt')]  #remove any junk, spaces etc
    if code[0] == 'help':
        if len(code) == 1:
            print helpMsg
        else:
            codeError()
    elif code[0] == 'quit':
        if len(code) == 1: Quit()
        else: codeError()
    elif code[0] == 'list':
        if len(code) != 2: codeError()
        else: List(code[1])
    elif code[0] == 'new':
        if len(code) == 1:newSalt()
        elif code[1] == 'tube':
            if len(code) != 2: codeError()
            else:
                tubes.append([None])
                currenttubeindex = len(tubes) - 1
                heatedflags.append(0)
        else: codeError()
        
    if salt == [None, None]: continue
    
    if code[0] == 'add':
        if len(code) == 4 and code[2] == 'in':
            errorstring = add(code[1], int(code[-1][-1]) - 1)
        elif len(code) == 2:
            errorstring = add(code[-1])
        else:
            errorstring = 'error'
        if errorstring == 'error': codeError()
    elif code[0] == 'create':
        if len(code) != 2: codeError()
        elif code[1] in ('OS', 'SE', 'WE'):
            tubes.append([code[1]])
            currenttubeindex = len(tubes) - 1
            heatedflags.append(0)
    elif code[0] == 'heat':
        flag = True
        if len(code) == 1:
            index = currenttubeindex
            heat = 1
        elif len(code) == 2 and code[1][0] == 't':
            index = int(code[1][1]) - 1
            heat = 1
        elif len(code) == 3 and code[1][0] == 't' and code[2] in ('slightly', 'strongly'):
            index = int(code[1][1]) - 1
            heat = 2 if code[-1] == 'strongly' else 1
        else:
            flag = False
            codeError()
        if flag:
            if tubes[index] != [None]:
                heatedflags[index] = heat
                currenttubeindex = index
            else:
                print 'Test Tube %d is empty. It can\'t be heated'%(index+1)
        
    printtubes()







    

