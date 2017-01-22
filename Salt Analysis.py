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

'add <chemical name> [to <tube>]' :- adds the chemical in the specified test tube. Test tube not specified, then adds to last used test tube. Can add contents of one test tube into the other, specify test tube number rather than chemical name.

'heat [<intensity>] [<tube>] :- heats the mentioned test tube (default test tube is the last used one) with a given intensity (slight heating by default)

'flame test' :- Carries out flame test on your given salt

'guess <ion> is <name>' :- Give your guess for the specified ion ('cation' or 'anion'). If right, gain points. If wrong lose points.

'pass in <tube>' :- Pass the evolved gas in the previous reaction (if any) into a specified test tube

'introduce <chemical> [to <tube>]' :- Introduce the chemical/paper to the test tube (default test tube is last one used) at the mouth of the test tube. The chemical is not added to the test tube itself.

'create SE' :- Create the Sodium Carbonate Extract

'create WE' :- Create the Water Extract

'create OS' :- Create the Original Salt Solution

'quit' :- Quit out of Salt Analysis Emulator. Gives you the answer to the old salt, if a salt is stil being analysed.

'new tube' :- Take a new test tube

'discard <tube>' :- Remove the specified test tube

Here, test tubes also refer to boiling tubes, so don't worry about that.
Also there is no limit to the number of test tubes you can take.
If you want information as to a certain test, please refer to your lab manual :)''' 

def codeError():
    print 'ERROR! Please recheck what you have typed'

def Quit():
    if salt != [None, None]:
        ch = raw_input('Are you sure? Press y to proceed, anything else to return>>> ').lower()
        if ch == 'y':
            formula, name = saltFormula()
            print 'The salt was %s, with formula %s'%(name, formula)
        else: return
    print 'THANK YOU FOR USING THE SALT ANALYSIS EMULATOR.'
    quit()

def printtubes():
    print
    for i in range(len(tubes)):
        if not (tubes[i]['contents'] == []):
            output = 'Test Tube %d has'%(i+1)
            for chemical in tubes[i]['contents']:
                output += (' ' + str(chemical) + ',')
            output = output[:-1] + '.'
            if tubes[i]['heated']:
                output += ' It is %s hot.'%('slightly' if tubes[i]['heated'] == 1 else 'very')
            else:
                output += ' It is cool.'
            if tubes[i]['colour']:
                output += ' Its colour is %s.'%(tubes[i]['colour'].lower())
            print output
        else:
            print 'Test tube %d is empty'%(i+1)
    print 'Current Test Tube:' , currenttubeindex + 1
    
#ALL CHEMICALS LISTS
acids_list = {'Diluted Hydrochloric acid': 'dil_HCl', 'Concentrated Nitric acid': 'conc_HNO3',
              'Concentrated Sulphuric acid': 'conc_H2SO4', 'Diluted Sulphuric acid': 'dil_H2SO4',
              'Concentrated Hydrochloric acid': 'conc_HCl', 'Diluted Nitric acid': 'dil_HNO3', 'Acetic Acid': 'CH3COOH'}
misc_list = {'Moist Blue Litmus Paper': 'MBLpaper', 'Acidified Dichromate Paper': 'ADpaper', 'Moist Starch Iodide Paper': 'MSIpaper',
             'Moist Starch Paper': 'MSpaper', 'Water': 'water', 'Paper Pellets': 'paper', 'Lead Acetate paper': 'LApaper',
             'Copper turnings':'Cu_turning'}
# Add more reagents specific to certain tests for new cations/anions
reag_list = {'Calcium chloride': 'CaCl2', 'Acidified Potassium dichromate': 'K2Cr2O7', 'Ammonium chloride': 'NH4Cl',
             'Disodium hydrogen phosphate': 'Na2HPO4', 'Phenolphthalein': 'phenol', 'Magnesia mixture': 'magnesia',
             'Ammonium carbonate': '(NH4)2CO3', "Nessler's reagent": 'ness', 'Sodium nitroprusside / Na[Fe(CN)5NO]': 'SNP',
             'Sodium Hydroxide': 'NaOH', 'Barium chloride': 'BaCl2', 'Ammonium molybdate / (NH4)2MoO4': 'molybdate',
             'Magnesium sulphate': 'MgSO4', 'Ammonium acetate': 'CH3COONH4', 'Ammonium hydroxide': 'NH4OH',
             'Lead acetate': '(CH3COO)2Pb', 'Lime water / Ca(OH)2': 'lime', 'Hydrogen sulphide': 'H2S',
             'Acidified Potassium manganate':'KMnO4', 'Starch':'starch', 'Potassium iodide':'KI', 'Ferrous sulphate':'FeSO4',
             'Manganese peroxide':'MnO2', 'Silver nitrate':'AgNO3', 'Carbon tetrachloride':'CCl4', 'Chlorine water':'Cl_water',
             'Ethanol':'C2H5OH', 'Ferric chloride':'FeCl3', 'Potassium chromate':'K2CrO4', 'Potassium ferrocyanide':'K4[Fe(CN)6]',
             'Potassium ferricyanide':'K3[Fe(CN)6]', 'Blue litmus':'b_lit', 'Red litmus':'r_lit', 'Potassium thiocyanate':'KCNS',
             'Lead peroxide':'PbO2', 'Dimethylglyoxime':'DMG', 'Acetone':'(CH3)2CO', 'Ammonium sulphate':'(NH4)2SO4',
             'Ammonium oxalate':'(NH4)2C2O4'}

acids = acids_list.values()
acids.sort()
misc = misc_list.values()
misc.sort()
reagents = reag_list.values()
reagents.sort()

def List(category):
    if category == '*':
        print 'ACIDS:'
        for chemical in sorted(acids_list.keys()):
            print chemical, ' - ', acids_list[chemical] 
        print'\nREAGENTS'
        for chemical in sorted(reag_list.keys()):
            print chemical, ' - ', reag_list[chemical] 
        print '\nMISCELLANEOUS'
        for chemical in sorted(misc_list.keys()):
            print chemical, ' - ', misc_list[chemical]
    elif category == 'acids':
        for chemical in sorted(acids_list.keys()):
            print chemical, ' - ', acids_list[chemical] 
    elif category == 'misc':
        for chemical in sorted(misc_list.keys()):
            print chemical, ' - ', misc_list[chemical] 
    elif category == 'reag': 
        for chemical in sorted(reag_list.keys()):
            print chemical, ' - ', reag_list[chemical] 

def saltFormula():  #write code to return the formula as string
    name = salt[0]['name'] + ' ' + salt[1]['name']
    if salt[0]['valency'] == salt[1]['valency']:
        formula = salt[0]['formula'] + salt[1]['formula']
    elif salt[0]['formula'] == 'NH4':
        formula = '(NH4)%d%s'%(salt[1]['valency'], salt[1]['formula'])
    elif salt[0]['valency'] == 1:
        formula = '%s%d%s'%(salt[0]['formula'], salt[1]['valency'], salt[1]['formula'])
    elif len(salt[1]['formula']) > 2:
        if salt[1]['valency'] == 1:
            formula = '%s(%s)%d'%(salt[0]['formula'], salt[1]['formula'], salt[0]['valency'])
        else:
            formula = '%s%d(%s)%d'%(salt[0]['formula'], salt[1]['valency'], salt[1]['formula'], salt[0]['valency'])
    else: #len(salt 1 formula) <= 2
        if salt[1]['valency'] == 1:
            formula = '%s%s%d'%(salt[0]['formula'], salt[1]['formula'], salt[0]['valency'])
        else:
            formula = '%s%d%s%d'%(salt[0]['formula'], salt[1]['valency'], salt[1]['formula'], salt[0]['valency'])
    return formula, name 

def newSalt():
    global salt, saltflag, tubes
    if salt != [None, None]:
        ch = raw_input('Are you sure? Press y to proceed, anything else to exit>>> ').lower()
        if ch == 'y':
            formula, name = saltFormula()
            print 'The salt was %s, with formula %s'%(name, formula) 
        else: return
    salt[0] = choice(cations)
    salt[1] = choice(anions)
    for i in (0, 1): salt[i]['confirm'] = False
    print
    print 'A salt has been chosen'
    if salt[0]['colour'] != None: print 'Colour -' , salt[0]['colour']
    else: print 'No recognizable colour'
    if salt[0]['odour'] != None and salt[1]['odour'] != None: print 'Mix of smells detected'
    elif salt[0]['odour'] != None: print 'Odour -' , salt[0]['odour'], 'Smell'
    elif salt[1]['odour'] != None: print 'Odour -' , salt[1]['odour'], 'Smell'
    else: print 'No recognizable odour'
    tubes = list()
    tubes.append(new_tube())
    saltflag = [False, False]

def guess(ion, name):
    dictionary = {'cation':0, 'anion':1}
    index = dictionary[ion]
                                
    if saltflag[index] == True:
        print 'You have already guessed the %s, try to guess the other ion.'%(ion)
        return
    if not salt[index]['confirm']:
        print 'You haven\'t done a confirmatory test. Please do so before reporting an answer.'
        return
    if index == 0 and name == 'Fe':
        valence = int(raw_input('Which Fe ion? The ion with valency 2 or valency 3? '))
        if valence == salt[0]['valency'] and name == salt[0]['formula']:
            print 'CORRECT! The cation was %s, with formula %s%d+' % (salt[index]['name'], salt[index]['formula'], valence)
            saltflag[index] = True
        else:
            print 'Wrong guess :/'
    elif name == salt[index]['formula']:
        print 'CORRECT! The %s was %s, with formula %s' % (ion, salt[index]['name'], salt[index]['formula'])
        saltflag[index] = True
    else:
        print 'Wrong guess :/'
    if saltflag == [True, True]:
        print 'GREAT! YOU HAVE GUESSED THE SALT.'
        formula, name = saltFormula()
        print 'The salt was indeed %s, with formula %s.' % (name, formula)
        reset()

def reset():
    global salt, saltflag, tubes, currenttubeindex
    salt = [None, None]  #Use this as a flag to check whether new salt has been picked
    saltflag = [False, False]  #use this as a flag to check whether a salt has been guessed correctly
    tubes = list()
    tubes.append(new_tube()) 

def new_tube(chemical = None):
    global currenttubeindex
    tube = {'contents':list(), 'heated':0, 'colour':None, 'gas':None}
    #0 - not heated, 1 - slightly heated, 2 - strongly heated
    #'gas' value is to keep track of what gas is being emitted
    if chemical != None: tube['contents'].append(chemical)
    currenttubeindex = len(tubes)
    return tube

def discard(index):
    global tubes, currenttubeindex
    if tubes[index]['contents'] == []:
        del tubes[index]
        currenttubeindex = 0
    else:
        ch = raw_input('This test tube is not empty. Are you sure you want to discard this tube? Press y to continue: ').lower()
        if ch == 'y':
            del tubes[index]
            currenttubeindex = 0
    if len(tubes) == 0:
        tubes.append(new_tube())

def heat(code):
    global tubes, currenttubeindex
    if len(code) == 1:
        index = currenttubeindex
        heat = 1
    elif len(code) == 2:
        if code[1][0] == 't':
            index = int(code[1][1]) - 1
            heat = 1
        else:
            index = currenttubeindex
            heat = 2 if code[-1] == 'strongly' else 1
    elif len(code) == 3 and ((code[2][0] == 't' and code[1] in ('slightly', 'strongly')) or \
                             (code[1][0] == 't' and code[2] in ('slightly', 'strongly'))):
        index = int(code[1][1]) - 1
        heat = 2 if code[-1] == 'strongly' else 1
    else:
        codeError()
        return
    if tubes[index]['contents'] != [None]:
        tubes[index]['heated'] = heat
        currenttubeindex = index
    else:
        print 'Test Tube %d is empty. It can\'t be heated'%(index+1)

    #tests
    prelim_tests_anion()
    sulphite_confirm_tests()
    chloride_confirm_tests()
    bromide_confirm_tests()
    iodide_confirm_tests()
    nitrate_confirm_tests()
    acetate_confirm_tests()
    phosphate_confirm_tests()
    group1_confirm_tests()
    group2_confirm_tests()
    group4_confirm_tests()
    group5_confirm_tests()
    
def pass_gas(gas, index):  #Keep updating for confirmatory tests
    global tubes, currenttubeindex
    if gas == 'CO2' and tubes[index]['contents'] == ['lime']:
        print '\nSolution turned white. Becomes colourless with excess.'
        tubes[index]['colour'] = 'white'
    elif gas == 'NO' and tubes[index]['contents'] == ['FeSO4']:
        print '\nSolution turns black.'
        tubes[index]['colour'] = 'black'
    elif gas == 'CrO2Cl2' and tubes[index]['contents'] == ['NaOH']:
        tubes[index]['colour'] = 'yellow'
        print 'Very slight yellow tinge to the solution'
    currenttubeindex = index

def introduce(chemical, index = None):
    global currenttubeindex
    if index == None: index = currenttubeindex
    if tubes[index]['gas'] == 'H2S' and chemical == 'LApaper':
        print '\nLead acetate paper turns black'
    elif tubes[index]['gas'] == 'SO2' and chemical == 'ADpaper':
        print '\nAcidified dichromate paper turns green'
    elif tubes[index]['gas'] == 'HCl' and chemical == 'NH4OH':
        print '\nDense white fumes formed'
    elif tubes[index]['gas'] == 'Br2' and chemical == 'MSpaper':
        print '\nThe moist starch paper turns yellow'
    elif tubes[index]['gas'] == 'Br2' and chemical == 'MSIpaper':
        print '\nThe moist starch iodide paper turns blue'
    elif tubes[index]['gas'] == 'I2' and chemical == 'MSpaper':
        print '\nThe moist starch paper turns blue black'
    elif tubes[index]['gas'] == 'CH3COOH' and chemical == 'MBLpaper':
        print '\nMoist blue litmus paper turns red'
    elif tubes[index]['gas'] == 'NH3' and chemical == 'conc_HCl':
        print '\nDense white fumes formed'
    currenttubeindex = index

def add(chemical, index = None):
    global currenttubeindex, tubes
    if index == None: index = currenttubeindex 
    
    if chemical[0] == 't': #if adding one test tube into another
        emptiedindex = int(chemical[-1]) - 1
        if len(tubes[emptiedindex]['contents']) >= 1:
            if len(tubes[index]['contents']) >= 1 and tubes[index]['contents'][-1] == tubes[emptiedindex]['contents'][0]:
                tubes[index]['contents'].extend(tubes[emptiedindex]['contents'][1:])
            else: tubes[index]['contents'].extend(tubes[emptiedindex]['contents'])
            tubes[index]['colour'] = tubes[emptiedindex]['colour']
            tubes[index]['heated'] = tubes[emptiedindex]['heated'] 
            currenttubeindex = index
            ch = raw_input('Pour all or only some of the contents into the test tube? Press a for all and s for only little: ')
            if ch == 'a':
                tubes[emptiedindex] = new_tube()
                currenttubeindex = emptiedindex
        else:
            print 'Tube %d is empty. Cannot add an empty tube to another tube'%(emptiedindex)
    else:
        if not (chemical in reagents or chemical in acids or chemical in misc or chemical == 'salt'):
            if not chemical in ('WE', 'SE'):
                print 'Sorry. This chemical cannot be found'
        else:
            if len(tubes[index]['contents']) == 0 or not chemical == tubes[index]['contents'][-1]:
                tubes[index]['contents'].append(chemical)
            currenttubeindex = index

    #tests
    solubility_test()
    prelim_tests_anion()
    carbonate_confirm_tests()
    sulphide_confirm_tests()
    sulphite_confirm_tests()
    nitrite_confirm_tests()
    chloride_confirm_tests()
    bromide_confirm_tests()
    iodide_confirm_tests()
    nitrate_confirm_tests()
    acetate_confirm_tests()
    phosphate_confirm_tests()
    sulphate_confirm_tests()
    prelim_tests_cation()
    group0_confirm_tests()
    group1_confirm_tests()
    group2_confirm_tests()
    group3_confirm_tests()
    group4_confirm_tests()
    group5_confirm_tests()

#FUNCTIONS FOR TESTS
#These functions should be placed in the add() function (except for flame test, there's a keyword for that)
#If heating is required for some of the tests, put it under the heating function

def flame_test():
    if salt[0]['flame'] != None:
        print 'The flame is %s in colour' % (salt[0]['flame'].lower())
        salt[0]['confirm'] = True
    else:
        print 'No characteristic flame colour'

def solubility_test():
    i = currenttubeindex
    if len(tubes[i]['contents']) != 2: return
    if sorted(tubes[i]['contents']) == sorted(['salt', 'water']): #test for solubility in water
        #ammonium carbonate only soluble carbonate (for some reason). Refer to net
        if salt[1]['formula'] == 'CO3' and salt[0]['formula'] != 'NH4': print '\nSalt insoluble in water'
        else: print '\nSalt soluble in water'
    elif sorted(tubes[i]['contents']) == sorted(['salt', 'dil_HCl']): #test for solubility in dil HCl
        if salt[0]['formula'] == 'Pb':
            print '\nWhite precipitate is formed'
            tubes[i]['colour'] = 'white'
        else: print '\nSoluble in dil_HCl'

def prelim_tests_anion():
    global tubes
    i = currenttubeindex
    
    if sorted(tubes[i]['contents']) == ['dil_HCl', 'salt']: #dilute acid test
        if salt[1]['formula'] == 'CO3':
            print '\nColourless, odourless gas evolved.'
            tubes[i]['gas'] = 'CO2'
        elif tubes[i]['heated']: #only CO3 reaction takes place without heat
            if salt[1]['formula'] == 'S':
                print '\nGas with rotten egg smell evolved'
                tubes[i]['gas'] = 'H2S'
            elif salt[1]['formula'] == 'NO2':
                print '\nSlight brown fumes evolved'
                tubes[i]['gas'] = 'NO'
            elif salt[1]['formula'] == 'SO3':
                print '\nGas with burning sulphur smell evolved'
                tubes[i]['gas'] = 'SO2'
        
    if sorted(tubes[i]['contents']) == ['conc_H2SO4', 'salt']:
        if salt[1]['formula'] == 'Cl':
            print '\nColourless gas with irritating smell'
            tubes[i]['gas'] = 'HCl'
        elif tubes[i]['heated']: #only Cl reaction takes place without heat
            if salt[1]['formula'] == 'Br':
                print '\nReddish brown gas evolved'
                tubes[i]['gas'] = 'Br2'
            elif salt[1]['formula'] == 'I':
                print '\nViolet vapours evolved'
                tubes[i]['gas'] = 'I2'
            elif salt[1]['formula'] == 'CH3COO':
                print '\nGas with vinegar smell evolved'
                tubes[i]['gas'] = 'CH3COOH'
            elif salt[1]['formula'] == 'NO3':
                print '\nSlight brown fumes evolved'
                tubes[i]['gas'] = 'NO'

def carbonate_confirm_tests(): 
    #only tests not counted are for soluble carbonates, i.e ammonium carbonate
    global tubes
    i = currenttubeindex
    if not (salt[0]['formula'] == 'NH4' and salt[1]['formula'] == ['CO3']): return
    if sorted(tubes[i]['contents']) == ['MgSO4', "WE"]:
        print '\nWhite precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'white'
    elif sorted(tubes[i]['contents']) == ['CaCl2', "WE"]:
        print '\nWhite precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'white'
    elif sorted(tubes[i]['contents']) == ["WE", 'phenol']:
        print '\nSolution turns pink'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'pink'

def sulphide_confirm_tests():
    global tubes
    i = currenttubeindex
    if not (salt[0]['formula'] == 'S'): return
    if len(tubes[i]['contents']) <= 1: return
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['CH3COOH', '(CH3COO)2Pb']:
        print '\nBlack precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'black'
    elif tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['NaOH', 'SNP']:
        print '\nPurple colour obtained'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'purple'

sulphite_boilCO2_flag = False

def sulphite_confirm_tests():
    global tubes, sulphite_boilCO2_flag
    i = currenttubeindex
    if salt[1]['formula'] != 'SO3': return
    if len(tubes[i]['contents']) <= 1: return
    if tubes[i]['contents'][0] in ('SE', 'WE') and tubes[i]['contents'][1] == 'K2Cr2O7':
        print '\nSolution turns green'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'Green'
    if tubes[i]['contents'][0] in ('SE', 'WE') and tubes[i]['contents'][1:] == ['CH3COOH'] and tubes[i]['heated']:
        sulphite_boilCO2_flag = True
    if not sulphite_boilCO2_flag: return
    if tubes[i]['contents'][0] in ('SE', 'WE') and tubes[i]['contents'][1:] == ['CH3COOH', 'BaCl2'] and tubes[i]['heated']:
        print '\nWhite precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'white'
    elif tubes[i]['contents'][0] in ('SE','WE') and tubes[i]['contents'][1:] == ['CH3COOH','BaCl2','dil_HCl'] and tubes[i]['colour']:
        print '\nPrecipitate dissolves. Colourless gas with smell of burning suplhur evolved.'
        tubes[i]['colour'] = None
        salt[1]['confirm'] = True
        tubes[i]['gas'] = 'SO2'
    elif tubes[i]['contents'][0] in ('SE', 'WE') and tubes[i]['contents'][1:] == ['CH3COOH', 'BaCl2', 'KMnO4'] and tubes[i]['colour']:
        print '\nPink colour disappears'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'white'

def nitrite_confirm_tests():
    global tubes
    i = currenttubeindex
    if salt[1]['formula'] != 'NO2' : return
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['dil_H2SO4', 'KI', 'starch']:
        print '\nSolution turns blue-black'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'blue-black'
    if tubes[i]['contents'][0] in ('WE', 'SE', 'salt') and tubes[i]['contents'][1:] == ['dil_H2SO4', 'KMnO4']:
        print '\nPink colour is discharged'
        salt[1]['confirm'] = True

chromyl_chloride_test_stage = 0

def chloride_confirm_tests():
    global tubes, chromyl_chloride_test_stage
    i = currenttubeindex
    if salt[1]['formula'] != 'Cl' or len(tubes[i]['contents']) < 2: return
    if tubes[i]['contents'] == ['salt', 'MnO2', 'conc_H2SO4']:
        print '\nGreenish yellow gas evolved'
        tubes[i]['gas'] = 'Cl2'
        salt[1]['confirm'] = True
    if tubes[i]['contents'][0] in ('WE', 'SE') and 'HNO3' in tubes[i]['contents'][1] and tubes[i]['contents'][-1] == 'AgNO3':
        print '\nCurdy white precipitate formed'
        tubes[i]['colour'] = 'curdy-white'
        salt[1]['confirm'] = True
    if tubes[i]['contents'][0] in ('WE', 'SE') and 'HNO3' in tubes[i]['contents'][1] and tubes[i]['contents'][-2:] == ['AgNO3', 'NH4OH']:
        print '\nPrecipiate dissolves'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = None
    #chromyl chloride test:
    if chromyl_chloride_test_stage == 0 and tubes[i]['contents'] == ['salt', 'K2Cr2O7', 'conc_H2SO4']:
        chromyl_chloride_test_stage = 1
    elif chromyl_chloride_test_stage == 1 and tubes[i]['contents'] == ['salt', 'K2Cr2O7', 'conc_H2SO4'] and tubes[i]['heated'] == 2:
        chromyl_chloride_test_stage = 2
        print '\nRed vapours evolved'
        salt[1]['confirm'] = True
        chromyl_chloride_test_stage = 0
        tubes[i]['gas'] = 'CrO2Cl2'
    elif tubes[i]['contents'] == ['NaOH', 'CH3COOH', '(CH3COO)2Pb'] and tubes[i]['colour'] == 'yellow':
        print '\nYellow precipitate got'
        tubes[i]['colour'] = 'yellow'
        salt[1]['confirm'] = True

bromide_forheating_flag = False
def bromide_confirm_tests():
    global tubes, bromide_forheating_flag
    i = currenttubeindex
    if salt[1]['formula'] != 'Br' or len(tubes[i]['contents']) < 2: return
    if not bromide_forheating_flag and tubes[i]['contents'] == ['salt', 'MnO2', 'conc_H2SO4'] and not tubes[i]['heated']:
        bromide_forheating_flag = True
    elif bromide_forheating_flag and tubes[i]['heated']:
        bromide_forheating_flag = False
        print '\nReddish brown vapours formed'
        salt[1]['confirm'] = True
        tubes[i]['gas'] = 'Br2'
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['Cl_water', 'CCl4']:
        print '\nOrange-brown layer formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'orange'
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['dil_HNO3', 'AgNO3']:
        print '\nPale yellow precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'pale-yellow'
    elif tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['dil_HNO3', 'AgNO3', 'NH4OH']:
        print '\nPrecipiate partly dissolves'
        salt[1]['confirm'] = True

iodide_forheating_flag = False
def iodide_confirm_tests():
    global tubes, iodide_forheating_flag
    i = currenttubeindex
    if salt[1]['formula'] != 'I' or len(tubes[i]['contents']) < 2: return
    if not iodide_forheating_flag and tubes[i]['contents'] == ['salt', 'MnO2', 'conc_H2SO4'] and not tubes[i]['heated']:
        iodide_forheating_flag = True
    elif iodide_forheating_flag and tubes[i]['heated']:
        iodide_forheating_flag = False
        print '\nViolet vapours formed'
        salt[1]['confirm'] = True
        tubes[i]['gas'] = 'I2'
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['Cl_water', 'CCl4']:
        print '\nPink layer formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'pink'
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['dil_HNO3', 'AgNO3']:
        print '\nYellow precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'yellow'

nitrate_pelletstest_flag = 0
def nitrate_confirm_tests():
    global tubes, nitrate_pelletstest_flag
    i = currenttubeindex
    if salt[1]['formula'] != 'NO3' or len(tubes[i]['contents']) < 2: return
    if tubes[i]['contents'] == ['salt', 'conc_H2SO4'] and not tubes[i]['heated']: nitrate_pelletstest_flag = 1
    elif nitrate_pelletstest_flag == 1 and tubes[i]['heated']: nitrate_pelletstest_flag = 2
    elif nitrate_pelletstest_flag == 2:
        if tubes[i]['contents'][-1] == 'Cu_turning':
            print '\nSolution turns green. Profuse brown fumes evolved'
            tubes[i]['gas'] = 'NO'
            nitrate_pelletstest_flag = 0
            salt[1]['confirm'] = True
            tubes[i]['colour'] = 'green'
        elif tubes[i]['contents'][-1] == 'paper':
            print '\nProfuse brown fumes evolved'
            nitrate_pelletstest_flag = 0
            salt[1]['confirm'] = True
            tubes[i]['gas'] = 'NO'
    #Brown-ring test, must be improved
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['dil_H2SO4', 'FeSO4', 'conc_H2SO4']: 
        print 'Brown ring formed'
        tubes[i]['colour'] = 'green, with a brown ring'
        salt[1]['confirm'] = True

acetate_stages = 0
def acetate_confirm_tests():
    global tubes, acetate_stages
    i = currenttubeindex
    if salt[1]['formula'] != 'CH3COO' or len(tubes[i]['contents']) < 2: return
    if tubes[i]['contents'][0] in ('WE', 'SE') and tubes[i]['contents'][1:] == ['dil_HCl', 'FeCl3']:
        print 'Solutions turns red'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'red'
    if tubes[i]['contents'] == ['salt', 'conc_H2SO4'] and not tubes[i]['heated'] and acetate_stages == 0: acetate_stages = 1
    elif tubes[i]['contents'] == ['salt', 'conc_H2SO4'] and tubes[i]['heated'] and acetate_stages == 1: acetate_stages = 2
    elif tubes[i]['contents'] == ['salt', 'conc_H2SO4', 'C2H5OH'] and tubes[i]['heated'] and acetate_stages == 2: acetate_stages = 3
    elif tubes[i]['contents'] == ['water', 'salt', 'conc_H2SO4', 'C2H5OH'] and acetate_stages == 3:
        print 'Pleasant fruity smell got'
        salt[1]['confirm'] = True

def sulphate_confirm_tests():
    global tubes
    i = currenttubeindex
    if salt[1]['formula'] not in ('SO4', 'PO4') : return  #phosphate answers sulphate tests (for some reason)
    if tubes[i]['contents'] == ['WE', 'BaCl2'] or tubes[i]['contents'] == ['SE', 'BaCl2'] or \
       tubes[i]['contents'] == ['WE', 'dil_HCl', 'BaCl2'] or tubes[i]['contents'] == ['SE', 'dil_HCl', 'BaCl2']:
        print '\nWhite precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'white'
    elif tubes[i]['contents'] == ['WE', '(CH3COO)2Pb'] or tubes[i]['contents'] == ['SE', '(CH3COO)2Pb'] or \
         tubes[i]['contents'] == ['WE', 'CH3COOH', '(CH3COO)2Pb'] or tubes[i]['contents'] == ['SE', 'CH3COOH', '(CH3COO)2Pb']:
        print '\nWhite precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'white'
    elif (tubes[i]['contents'] == ['WE', '(CH3COO)2Pb', 'CH3COONH4'] or tubes[i]['contents'] == ['SE', '(CH3COO)2Pb', 'CH3COONH4'] or \
         tubes[i]['contents'] == ['WE', 'CH3COOH', '(CH3COO)2Pb', 'CH3COONH4'] or \
         tubes[i]['contents'] == ['SE', 'CH3COOH', '(CH3COO)2Pb', 'CH3COONH4']) and tubes[i]['colour'] == 'white':
        print '\nWhite precipitate dissolves'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = None

phosphate_molybdate_test_heated_flag = False

def phosphate_confirm_tests():
    global tubes, phosphate_molybdate_test_heated_flag
    i = currenttubeindex
    if salt[1]['formula'] != 'PO4': return
    if tubes[i]['contents'] == ['WE', 'magnesia'] or tubes[i]['contents'] == ['SE', 'magnesia'] or \
       tubes[i]['contents'] == ['WE', 'dil_HCl', 'magnesia'] or tubes[i]['contents'] == ['SE', 'dil_HCl', 'magnesia']:
        print '\nWhite precipitate formed'
        salt[1]['confirm'] = True
        tubes[i]['colour'] = 'white'
    if tubes[i]['contents'][0] in ('salt', 'WE', 'SE') and ((len(tubes[i]['contents']) == 2 and tubes[i]['contents'][1] == 'conc_HNO3') or \
         (len(tubes[i]['contents']) == 3 and tubes[i]['contents'][1] in acids and tubes[i]['contents'][2] == 'conc_HNO3')) and \
         tubes[i]['heated'] == 2:
        phosphate_molybdate_test_heated_flag = True
    elif phosphate_molybdate_test_heated_flag and tubes[i]['contents'][-1] == 'molybdate':
        print '\nCanary yellow precipitate formed'
        tubes[i]['colour'] == 'Canary yellow'  
        salt[1]['confirm'] = True     

def prelim_tests_cation():
    global tubes
    i = currenttubeindex
    colour = None
    if tubes[i]['contents'] == ['OS', 'dil_HCl'] and salt[0]['formula'] == 'Pb': colour = 'White'
    elif tubes[i]['contents'] == ['OS', 'dil_HCl', 'H2S']:
        if salt[0]['formula'] == 'Cu': colour = 'Black'
        elif salt[0]['formula'] == 'Cd': colour = 'Yellow'
    elif tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH']:
        if salt[0]['formula'] == 'Fe' and salt[0]['valency'] == 2: colour = 'Green'
        elif salt[0]['formula'] == 'Fe' and salt[0]['valency'] == 3: colour = 'Yellowish-brown'
        elif salt[0]['formula'] == 'Al': colour = 'Gelatinous white'
    elif tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', 'H2S']:
        if salt[0]['formula'] == 'Co' or salt[0]['formula'] == 'Ni': colour = 'Black'
        elif salt[0]['formula'] == 'Mn': colour = 'Off-white'
        elif salt[0]['formula'] == 'Zn': colour = 'Dirty white' 
    elif tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', '(NH4)2CO3'] and salt[0]['formula'] in ('Ca', 'Sr', 'Ba'): colour = 'White'
    elif tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', 'Na2HPO4'] and salt[0]['formula'] == 'Mg':
        colour = 'White'
        salt[0]['confirm'] = True
    if colour != None:
        print '%s precipitate formed'%(colour)
        tubes[i]['colour'] = colour

def group0_confirm_tests():
    global tubes
    if salt[0]['formula'] != 'NH4': return
    i = currenttubeindex
    if tubes[i]['contents'] == ['OS', 'NaOH']:  
        print '\nColourless gas with pungent smell evolved.'
        salt[0]['confirm'] = True
        tubes[i]['gas'] = 'NH3'
    elif tubes[i]['contents'] == ['OS', 'NaOH', 'ness']:
        print '\nRed-brown precipitate formed'
        salt[0]['confirm'] = True
        tubes[i]['colour'] = 'Red-brown'

group1_solution_flag = False
golden_spangles_flag = 0
def group1_confirm_tests():  #improve properly
    global tubes, group1_solution_flag, golden_spangles_flag, golden_spangles_turn
    if salt[0]['formula'] != 'Pb': return
    i = currenttubeindex
    if tubes[i]['contents'] == ['OS', 'dil_HCl', 'water'] and tubes[i]['heated'] == 2: group1_solution_flag = True
    if group1_solution_flag and tubes[i]['contents'] == ['OS', 'dil_HCl', 'water', 'K2CrO4']:
        print '\nYellow precipitate'
        salt[0]['confirm'] = True
        tubes[i]['colour'] = 'yellow'
    if group1_solution_flag and tubes[i]['contents'] == ['OS', 'dil_HCl', 'water', 'KI']: #make it tougher
        golden_spangles_flag = 1
        salt[0]['confirm'] = True
        print '\nYellow precipitate (golden spangles)'
        tubes[i]['colour'] = 'yellow'
    if group1_solution_flag and tubes[i]['contents'] == ['OS', 'dil_HCl', 'water', 'conc_H2SO4']:
        print '\nWhite precipitate'
        salt[0]['confirm'] = True
        tubes[i]['colour'] = 'white'
    elif group1_solution_flag and tubes[i]['contents'] == ['OS', 'dil_HCl', 'water', 'conc_H2SO4', '(CH3COO)NH4']:
        print '\nWhite precipitate'
        salt[0]['confirm'] = True
        tubes[i]['colour'] = 'white'

group2_solution_flag = 0
def group2_confirm_tests():
    global tubes, group2_solution_flag
    if salt[0]['formula'] not in ('Cd', 'Cu'): return
    i = currenttubeindex
    if group2_solution_flag == 0 and tubes[i]['contents'] == ['OS', 'dil_HCl', 'H2S', 'dil_HNO3'] and not tubes[i]['heated']:
        group2_solution_flag = 1
    elif group2_solution_flag == 1 and tubes[i]['contents'] == ['OS', 'dil_HCl', 'H2S', 'dil_HNO3'] and tubes[i]['heated']:
        group2_solution_flag = 2
    if (group2_solution_flag == 2 and tubes[i]['contents'] == ['OS', 'dil_HCl', 'H2S', 'dil_HNO3', 'NH4OH']) or \
       (tubes[i]['contents'] == ['OS', 'NH4OH']):
        if salt[0]['formula'] == 'Cu':
            print '\nBlue precipitate'
            salt[0]['confirm'] = True
            tubes[i]['colour'] = 'blue'
        elif salt[0]['formula'] == 'Cd':
            print '\nWhite precipitate'
            salt[0]['confirm'] = True
            tubes[i]['colour'] = 'white'
    if (group2_solution_flag == 2 and tubes[i]['contents'] == ['OS', 'dil_HCl', 'H2S', 'dil_HNO3', 'K4[Fe(CN)6]']) or \
       (tubes[i]['contents'] == ['OS', 'K4[Fe(CN)6]']):
        if salt[0]['formula'] == 'Cu':
            print '\nBrown precipitate'
            salt[0]['confirm'] = True
            tubes[i]['colour'] = 'brown'
        elif salt[0]['formula'] == 'Cd':
            print '\nWhite precipitate'
            salt[0]['confirm'] = True
            tubes[i]['colour'] = 'white'

def group3_confirm_tests():
    global tubes
    if salt[0]['formula'] not in ('Fe', 'Al'): return
    i = currenttubeindex
    #tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', 'dil_HCl']
    if salt[0]['formula'] == 'Al':
        if tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', 'dil_HCl', 'NaOH'] or tubes[i]['contents'] == ['OS', 'NaOH']:
            print '\nGelatinous white precipiate'
            tubes[i]['colour'] = 'white'
            salt[0]['confirm'] = True
        elif tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', 'dil_HCl', 'b_lit', 'NH4OH'] or tubes[i]['contents'] == ['OS', 'b_lit', 'NH4OH']:
            print '\nBlue lake formed'
            tubes[i]['colour'] = 'blue'
            salt[0]['confirm'] = True
    elif salt[0]['formula'] == 'Fe':
        if tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', 'dil_HCl', 'KCNS'] or tubes[i]['contents'] == ['OS', 'dil_HCl', 'KCNS']:
            salt[0]['confirm'] = True
            tubes[i]['colour'] = 'blood red' if salt[0]['valency'] == 3 else 'light red'
            print '\nSolution turns %s in colour'%(tubes[i]['colour'])
        if salt[0]['valency'] == 3 and tubes[i]['contents'] in (['OS', 'NH4Cl', 'NH4OH', 'dil_HCl', 'K4[Fe(CN)6]'], ['OS', 'K4[Fe(CN)6]']):
            print '\nDeep blue colour formed'
            salt[0]['confirm'] = True
            tubes[i]['colour'] = 'deep blue'
        if salt[0]['valency'] == 2:
            if tubes[i]['contents'] in (['OS', 'NH4Cl', 'NH4OH', 'dil_HCl', 'KMnO4'], ['OS', 'KMnO4']):
                print '\nPink colouration disappears'
                salt[0]['confirm'] = True
            elif tubes[i]['contents'] in (['OS', 'NH4Cl', 'NH4OH', 'dil_HCl', 'K3[Fe(CN)6]'], ['OS', 'dil_HCl', 'K3[Fe(CN)6]']):
                print '\nDeep blue colour formed'
                salt[0]['confirm'] = True
                tubes[i]['colour'] = 'deep blue'

group4_solution_heat_index = []  #store the indices of those tubes that still have the solution 
def group4_confirm_tests():
    global tubes, group4_solution_heat_index
    if salt[0]['formula'] not in ('Zn', 'Mn', 'Co', 'Ni'): return
    i = currenttubeindex
    #group reagent solution (different for Zn, Mn and Co,Ni)
    if salt[0]['formula'] in ('Zn', 'Mn'): solution = ['OS', 'NH4Cl', 'NH4OH', 'H2S', 'dil_HCl']
    else: solution = ['OS', 'NH4Cl', 'NH4OH', 'H2S', 'conc_HCl', 'conc_HNO3', 'water']
    
    if i not in group4_solution_heat_index and tubes[i]['contents'] == solution and \
       ((tubes[i]['heated']==2 and salt[0]['formula'] in ('Ni', 'Co')) or tubes[i]['heated']): #strongly heated in case of Ni or Co
        group4_solution_heat_index.append(i)
    
    if (i in group4_solution_heat_index and tubes[i]['contents'] == solution + ['NaOH']) or tubes[i]['contents'] == ['OS', 'NaOH']:
        if salt[0]['formula'] == 'Zn':
            print '\nWhite precipitate'
            tubes[i]['colour'] = 'white'
            salt[0]['confirm'] = True
            if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)
        elif salt[0]['formula'] == 'Mn':
            print '\nWhite precipitate, slowly turning brown'
            tubes[i]['colour'] = 'brownish white'
            salt[0]['confirm'] = True
            if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)
        elif salt[0]['formula'] == 'Ni':
            print '\nGreen precipitate'
            tubes[i]['colour'] = 'green'
            salt[0]['confirm'] = True
            if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)
            
    if salt[0]['formula'] == 'Zn' and ((i in group4_solution_heat_index and tubes[i]['contents'] == solution + ['K4[Fe(CN)6]']) or \
                                       tubes[i]['contents'] == ['OS', 'K4[Fe(CN)6]']):
        print '\nGreenish white precipitate'
        tubes[i]['colour'] = 'greenish white'
        salt[0]['confirm'] = True
        if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)
        
    if salt[0]['formula'] == 'Mn' and tubes[i]['colour'] == 'brownish white' and tubes[i]['heated'] and \
       (tubes[i]['contents'] == solution+['NaOH', 'conc_HNO3', 'PbO2'] or tubes[i]['contents'] == ['OS','NaOH', 'conc_HNO3', 'PbO2']):
        print '\nPinkish purple colour'
        tubes[i]['colour'] = 'pinkish purple'
        salt[0]['confirm'] = True
        if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)

    if salt[0]['formula'] == 'Ni' and ((i in group4_solution_heat_index and tubes[i]['contents'] == solution + ['DMG', 'NH4OH']) or \
                                       tubes[i]['contents'] == ['OS', 'DMG', 'NH4OH']):
        print '\nRed precipitate'
        tubes[i]['colour'] = 'red'
        salt[0]['confirm'] = True
        if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)
    if ((i in group4_solution_heat_index and tubes[i]['contents'] == solution + ['NH4Cl', 'NH4OH', 'K3[Fe(CN)6]']) or \
        tubes[i]['contents'] == ['OS', 'NH4Cl', 'NH4OH', 'K3[Fe(CN)6]']) and salt[0]['formula'] == 'Co':
        print '\nRed-brown precipitate'
        tubes[i]['colour'] = 'red-brown'
        salt[0]['confirm'] = True
        if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)
    if ((i in group4_solution_heat_index and tubes[i]['contents'] == solution + ['KCNS', '(CH3)2CO']) or \
        tubes[i]['contents'] == ['OS', 'KCNS', '(CH3)2CO']) and salt[0]['formula'] == 'Co':
        print '\nOrganic layer stained blue'
        tubes[i]['colour'] = 'blue'
        salt[0]['confirm'] = True
        if i in group4_solution_heat_index: group4_solution_heat_index.remove(i)

group5_solution_index = []
def group5_confirm_tests():
    global tubes, group5_solution_index
    if salt[0]['formula'] not in ('Ba', 'Ca', 'Sr'): return
    i = currenttubeindex
    solution = ['OS', 'NH4Cl', 'NH4OH', '(NH4)2CO3', 'CH3COOH']
    if i not in group5_solution_index and tubes[i]['contents'] == solution and tubes[i]['heated']:
        group5_solution_index.append(i) 
    if i not in group5_solution_index: return
    if salt[0]['formula'] == 'Ba' and tubes[i]['contents'] == solution + ['K2CrO4']:
        print '\nYellow precipitate'
        tubes[i]['colour'] = 'yellow'
        salt[0]['confirm'] = True
        group5_solution_index.remove(i)
    if salt[0]['formula'] == 'Sr' and tubes[i]['contents'] == solution + ['(NH4)2SO4']:
        print '\nWhite precipitate'
        tubes[i]['colour'] = 'white'
        salt[0]['confirm'] = True
        group5_solution_index.remove(i)
    if salt[0]['formula'] == 'Ca' and tubes[i]['contents'] == solution + ['(NH4)2C2O4']:
        print '\nWhite crystalline precipitate'
        tubes[i]['colour'] = 'white'
        salt[0]['confirm'] = True
        group5_solution_index.remove(i)
                                
#Actual loop for taking inputs-
print '''WELCOME TO SALT ANALYSIS EMULATOR!

A randomly generated salt is analyzed via a simple code

To find out about the syntax for the code, type help.
If you want to start analysing a salt, type new'''

#Dictionary for each cation/anion
#anions:
carbonate = {'name':'carbonate', 'type':'anion', 'formula':'CO3', 'valency':2, 'odour':None}
sulphide = {'name':'sulphide', 'type':'anion', 'formula':'S', 'valency':2, 'odour':'Rotten egg'}
nitrite = {'name':'nitrite', 'type':'anion', 'formula':'NO2', 'valency':1, 'odour':None}
sulphite = {'name':'sulphite', 'type':'anion', 'formula':'SO3', 'valency':2, 'odour':None}
chloride = {'name':'chloride', 'type':'anion', 'formula':'Cl', 'valency':1, 'odour':None}
bromide = {'name':'bromide', 'type':'anion', 'formula':'Br', 'valency':1, 'odour':None}
iodide = {'name':'iodide', 'type':'anion', 'formula':'I', 'valency':1, 'odour':None}
acetate = {'name':'acetate', 'type':'anion', 'formula':'CH3COO', 'valency':1, 'odour':'Vinegar'}
nitrate = {'name':'nitrate', 'type':'anion', 'formula':'NO3', 'valency':1, 'odour':None}
sulphate = {'name':'sulphate', 'type':'anion', 'formula':'SO4', 'valency':2, 'odour':None}
phosphate = {'name':'phosphate', 'type':'anion', 'formula':'PO4', 'valency':3, 'odour':None}
anions = [sulphide, carbonate, nitrite, sulphite, chloride, bromide, iodide, acetate, nitrate, sulphate, phosphate]

#cations
ammonium = {'name':'Ammonium', 'type':'cation', 'formula':'NH4', 'valency':1, 'odour':'Ammoniacal', 'flame':None, 'colour':None} 
lead = {'name':'Lead', 'type':'cation', 'formula':'Pb', 'valency':2, 'odour':None, 'flame':None, 'colour':None}
copper = {'name':'Copper', 'type':'cation', 'formula':'Cu', 'valency':2, 'odour':None, 'flame':'Green', 'colour':'blue-green'}
cadmium = {'name':'Cadmium', 'type':'cation', 'formula':'Cd', 'valency':2, 'odour':None, 'flame':None, 'colour':None}
ferrous = {'name':'Ferrous', 'type':'cation', 'formula':'Fe', 'valency':2, 'odour':None, 'flame':None, 'colour':'Pale green'}
ferric = {'name':'Ferric', 'type':'cation', 'formula':'Fe', 'valency':3, 'odour':None, 'flame':None, 'colour':'Yellow-brown'}
aluminium = {'name':'Aluminium', 'type':'cation', 'formula':'Al', 'valency':3, 'odour':None, 'flame':None, 'colour':None}
cobalt = {'name':'Cobalt', 'type':'cation', 'formula':'Co', 'valency':2, 'odour':None, 'flame':None, 'colour':'Deep pink'}
nickel = {'name':'Nickel', 'type':'cation', 'formula':'Ni', 'valency':2, 'odour':None, 'flame':None, 'colour':'Green'}
manganese = {'name':'Manganese', 'type':'cation', 'formula':'Mn', 'valency':2, 'odour':None, 'flame':None, 'colour':'Pale pink'}
zinc = {'name':'Zinc', 'type':'cation', 'formula':'Zn', 'valency':2, 'odour':None, 'flame':None, 'colour':None}
barium = {'name':'Barium', 'type':'cation', 'formula':'Ba', 'valency':2, 'odour':None, 'flame':'Green', 'colour':None}
strontium = {'name':'Strontium', 'type':'cation', 'formula':'Sr', 'valency':2, 'odour':None, 'flame':'Red', 'colour':None}
calcium = {'name':'Calcium', 'type':'cation', 'formula':'Ca', 'valency':2, 'odour':None, 'flame':'Red', 'colour':None}
magnesium = {'name':'Magnesium', 'type':'cation', 'formula':'Mg', 'valency':2, 'odour':None, 'flame':None, 'colour':None}
cations = [ammonium,lead,copper,cadmium,ferrous,ferric,aluminium,cobalt,nickel,manganese,zinc,barium,strontium,calcium,magnesium]

numTurns = 0

reset()

while True:
    print
    numTurns += 1
    codestring = raw_input('%d) Enter code line >>> '%(numTurns)).rstrip().lstrip()
    code = codestring.split()  #retreive individual keyword
    code = [word for word in code if word.isalnum() or word == '*' or \
            (word in reagents or word in acids or word in misc or word == 'salt')]  #remove any junk, spaces etc
    if len(code) == 0:
        codeError()
        continue

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
                tubes.append(new_tube())
        else: codeError()
        
    if salt == [None, None]: continue

    errorflag = False

    for word in code:
        if 't' == word[0] and len(word) == 2 and word[1].isdigit():
            if int(word[-1]) > len(tubes):
                codeError()
                errorflag = True
                break

    if errorflag: continue
    if code[0] == 'add':
        if len(code) == 4 and code[2] == 'to':
            errorstring = add(code[1], int(code[-1][-1]) - 1)
        elif len(code) == 2:
            errorstring = add(code[-1])
        else:
            errorstring = 'error'
        if errorstring == 'error': codeError()
    elif code[0] == 'create':
        if len(code) != 2: codeError()
        elif code[1] in ('OS', 'SE', 'WE'):
            tubes.append(new_tube(code[1]))
    elif code[0] == 'heat':
        heat(code)
    elif code == ['flame', 'test']: flame_test()
    elif code[0] == 'guess' and code[1] in ('cation', 'anion') and code[2] == 'is' and \
         (code[3] in [ion['formula'] for ion in (cations+anions)]):
        guess(code[1], code[3])
    elif len(code) == 2 and code[0] == 'discard' and code[1][0] == 't':
        discard(int(code[1][1]) - 1)
    elif len(code) == 3 and [code[0], code[1]] == ['pass', 'in'] and code[-1][0] == 't':
        gas = tubes[currenttubeindex]['gas']
        if gas != None: pass_gas(gas, int(code[-1][-1]) - 1)
        else: print 'No gas was formed in the previous reaction'
    elif code[0] == 'introduce':
        if len(code) == 2 and code[1] in (misc + reagents + acids):
            introduce(code[1])
        elif len(code) == 4 and code[1] in (misc + reagents + acids):
            introduce(code[1], int(code[-1][-1]) - 1)
        else:
            codeError()
        
    if salt != [None, None]: printtubes()







    

