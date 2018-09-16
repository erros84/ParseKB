import codecs
import re
import json
import copy
import functools
from pprint import pprint
from itertools import groupby
from operator import itemgetter

#ToDo: Parse Stores like strings
#Do Comparison
#expand Any's

isVerbose = False
kbProps = {}
kbLinks = [
        {"linux": "TLDE", "scancode": "29", "microsoft": "OEM_3", "caps": False, "keyman": "K_BKQUOTE", 'row': 0},
        {"linux": "AE01", "scancode": "02", "microsoft": "1", "caps": False, "keyman": "K_1", 'row': 0},
        {"linux": "AE02", "scancode": "03", "microsoft": "2", "caps": False, "keyman": "K_2", 'row': 0},
        {"linux": "AE03", "scancode": "04", "microsoft": "3", "caps": False, "keyman": "K_3", 'row': 0},
        {"linux": "AE04", "scancode": "05", "microsoft": "4", "caps": False, "keyman": "K_4", 'row': 0},
        {"linux": "AE05", "scancode": "06", "microsoft": "5", "caps": False, "keyman": "K_5", 'row': 0},
        {"linux": "AE06", "scancode": "07", "microsoft": "6", "caps": False, "keyman": "K_6", 'row': 0},
        {"linux": "AE07", "scancode": "08", "microsoft": "7", "caps": False, "keyman": "K_7", 'row': 0},
        {"linux": "AE08", "scancode": "09", "microsoft": "8", "caps": False, "keyman": "K_8", 'row': 0},
        {"linux": "AE09", "scancode": "0a", "microsoft": "9", "caps": False, "keyman": "K_9", 'row': 0},
        {"linux": "AE10", "scancode": "0b", "microsoft": "0", "caps": False, "keyman": "K_0", 'row': 0},
        {"linux": "AE11", "scancode": "0c", "microsoft": "OEM_MINUS", "caps": False, "keyman": "K_HYPHEN", 'row': 0},
        {"linux": "AE12", "scancode": "0d", "microsoft": "OEM_PLUS", "caps": False, "keyman": "K_EQUAL", 'row': 0},
        {"linux": "AD01", "scancode": "10", "microsoft": "Q", "caps": True, "keyman": "K_Q", 'row': 1},
        {"linux": "AD02", "scancode": "11", "microsoft": "W", "caps": True, "keyman": "K_W", 'row': 1},
        {"linux": "AD03", "scancode": "12", "microsoft": "E", "caps": True, "keyman": "K_E", 'row': 1},
        {"linux": "AD04", "scancode": "13", "microsoft": "R", "caps": True, "keyman": "K_R", 'row': 1},
        {"linux": "AD05", "scancode": "14", "microsoft": "T", "caps": True, "keyman": "K_T", 'row': 1},
        {"linux": "AD06", "scancode": "15", "microsoft": "Y", "caps": True, "keyman": "K_Y", 'row': 1},
        {"linux": "AD07", "scancode": "16", "microsoft": "U", "caps": True, "keyman": "K_U", 'row': 1},
        {"linux": "AD08", "scancode": "17", "microsoft": "I", "caps": True, "keyman": "K_I", 'row': 1},
        {"linux": "AD09", "scancode": "18", "microsoft": "O", "caps": True, "keyman": "K_O", 'row': 1},
        {"linux": "AD10", "scancode": "19", "microsoft": "P", "caps": True, "keyman": "K_P", 'row': 1},
        {"linux": "AD11", "scancode": "1a", "microsoft": "OEM_4", "caps": False, "keyman": "K_LBRKT", 'row': 1},
        {"linux": "AD12", "scancode": "1b", "microsoft": "OEM_6", "caps": False, "keyman": "K_RBRKT", 'row': 1},
        {"linux": "BKSL", "scancode": "2b", "microsoft": "OEM_5", "caps": False, "keyman": "K_BKSLASH", 'row': 1},
        {"linux": "AC01", "scancode": "1e", "microsoft": "A", "caps": True, "keyman": "K_A", 'row': 2},
        {"linux": "AC02", "scancode": "1f", "microsoft": "S", "caps": True, "keyman": "K_S", 'row': 2},
        {"linux": "AC03", "scancode": "20", "microsoft": "D", "caps": True, "keyman": "K_D", 'row': 2},
        {"linux": "AC04", "scancode": "21", "microsoft": "F", "caps": True, "keyman": "K_F", 'row': 2},
        {"linux": "AC05", "scancode": "22", "microsoft": "G", "caps": True, "keyman": "K_G", 'row': 2},
        {"linux": "AC06", "scancode": "23", "microsoft": "H", "caps": True, "keyman": "K_H", 'row': 2},
        {"linux": "AC07", "scancode": "24", "microsoft": "J", "caps": True, "keyman": "K_J", 'row': 2},
        {"linux": "AC08", "scancode": "25", "microsoft": "K", "caps": True, "keyman": "K_K", 'row': 2},
        {"linux": "AC09", "scancode": "26", "microsoft": "L", "caps": True, "keyman": "K_L", 'row': 2},
        {"linux": "AC10", "scancode": "27", "microsoft": "OEM_1", "caps": False, "keyman": "K_COLON", 'row': 2},
        {"linux": "AC11", "scancode": "28", "microsoft": "OEM_7", "caps": False, "keyman": "K_QUOTE", 'row': 2},
        {"linux": "K102", "scancode": "56", "microsoft": "OEM_102", "caps": False, "keyman": "K_oE2", 'row': 3},
        {"linux": "AB01", "scancode": "2c", "microsoft": "Z", "caps": True, "keyman": "K_Z", 'row': 3},
        {"linux": "AB02", "scancode": "2d", "microsoft": "X", "caps": True, "keyman": "K_X", 'row': 3},
        {"linux": "AB03", "scancode": "2e", "microsoft": "C", "caps": True, "keyman": "K_C", 'row': 3},
        {"linux": "AB04", "scancode": "2f", "microsoft": "V", "caps": True, "keyman": "K_V", 'row': 3},
        {"linux": "AB05", "scancode": "30", "microsoft": "B", "caps": True, "keyman": "K_B", 'row': 3},
        {"linux": "AB06", "scancode": "31", "microsoft": "N", "caps": True, "keyman": "K_N", 'row': 3},
        {"linux": "AB07", "scancode": "32", "microsoft": "M", "caps": True, "keyman": "K_M", 'row': 3},
        {"linux": "AB08", "scancode": "33", "microsoft": "OEM_COMMA", "caps": False, "keyman": "K_COMMA", 'row': 3},
        {"linux": "AB09", "scancode": "34", "microsoft": "OEM_PERIOD", "caps": False, "keyman": "K_PERIOD", 'row': 3},
        {"linux": "AB10", "scancode": "35", "microsoft": "OEM_2", "caps": False, "keyman": "K_SLASH", 'row': 3},
        {"linux": "SPCE", "scancode": "39", "microsoft": "SPACE", "caps": False, "keyman": "K_SPACE", 'row': 4},
        {"linux": "KPDL", "scancode": "53", "microsoft": "DECIMAL", "caps": False, "keyman": "K_NPDOT", 'row': 5},
    ]

def parseKB(passedKeyboard, filenameToParse, expand = False):
    if (filenameToParse[-4:] == ".klc"):
        passedKeyboard.setNative("MSKLC")
        parseMSK(passedKeyboard, filenameToParse)
        GenerateKMRules(passedKeyboard)
    elif (filenameToParse[-4:] == ".kmn"):
        passedKeyboard.setNative("Keyman")
        parseKeyman(passedKeyboard, filenameToParse, expand)

def parseMSK(passedKeyboard, mskFilename):
    print("Parsing MS")
    KbMetaInfo = dict()
    KBShiftStates = dict()
    KBCodes = dict()
    KBKeys = dict()
    KbKeysBool = dict()
    DeadKeys = dict()
    iDK = 0
    Mode = ""
    lineCount = 0
    currentDeadKey = ""
    infile = open(mskFilename, mode='r', encoding='utf-16')
    for line in infile:
        lineCount = lineCount + 1
        if (mskFilename[-4:] == ".klc"):
            iLevels = 0
            iKBCode = 0
            for line in infile:
                lineCount = lineCount + 1
                if (line =='\n') or (line.startswith("//")):
                    thing = 0
                else:
                    line = line[:-1]
                    if line.startswith("KBD"):
                        r = line.split("\t")
                        KbMetaInfo = {'KBID':r[1],'KBName':r[2]}
                        passedKeyboard.setVariable({'KBID':r[1]})
                        passedKeyboard.setVariable({'KBName':r[2]})                    
                    elif line.startswith("COPYRIGHT"):
                        r = line.split("\t")
                        KbMetaInfo.update({'Copyright':r[1]})
                        passedKeyboard.setVariable({'Copyright':r[1]})
                    elif line.startswith("COMPANY"):
                        r = line.split("\t")
                        KbMetaInfo.update({'Company':r[1]})
                        passedKeyboard.setVariable({'Company':r[1]})
                    elif line.startswith("LOCALENAME"):
                        r = line.split("\t")
                        KbMetaInfo.update({'Locale':r[1]})
                        passedKeyboard.setVariable({'Locale':r[1]})
                    elif line.startswith("LOCALEID"):
                        r = line.split("\t")
                        KbMetaInfo.update({'LocaleID':r[1]})
                        passedKeyboard.setVariable({'LocaleID':r[1]})
                    elif line.startswith("VERSION"):
                        r = line.split("\t")
                        KbMetaInfo.update({'Version':r[1]})
                        passedKeyboard.setVariable({'Version':r[1]})
                    elif line.startswith("//SC"):
                        r = line.split("\t")
                        for bit in r:
                            if r.index(bit) > 3:
                                passedKeyboard.addMSKIndex(bit)
                        #TODO Solve this:

                    ##Set Modes
                    elif line.startswith("DESCRIPTIONS"):
                        Mode = 'Descriptions'
                        #Add parse
                    elif line.startswith("KEYNAME"):
                        Mode = 'Keyname'
                        #Add parse
                    elif line.startswith("DEADKEY"):
                        Mode = 'DeadKey'
                        r = line.split("\t")
                        currentDeadKey = r[1]
                    elif line.startswith("SHIFTSTATE"):
                        Mode = "ShiftState" 
                    elif line.startswith("LAYOUT"):
                        Mode = "Layout"
                    elif line.startswith("LANGUAGENAMES"):
                        Mode = "LanguageNames"
                    elif line.startswith("ENDKB"):
                        Mode = "Done"
                    elif Mode == "DeadKey":
                        r = line.split("\t")
                        result = []
                        #for letter in bit:
                        #    result['Code'].append(u'%04x'%ord(letter))
                        passedKeyboard.addMSKDeadkey({'DK':currentDeadKey, "Key":r[0],"Result":r[1]})
                        iDK += 1
                        

                    elif Mode == "Keyname":
                        #Do cool stuff
                        boo = 0
                    elif Mode == "Descriptions":
                        #Do cool stuff
                        line = line.replace("\t\t","\t")
                        k = line.split("\t")
                        passedKeyboard.setVariable({"Name":k[1]})
                    elif Mode == "LanguageNames":
                        #Do cool stuff
                        line = line.replace("\t\t","\t")
                        k = line.split("\t")
                        passedKeyboard.setVariable({"WinLanguageID":k[0]})
                        passedKeyboard.setVariable({"WinLanguageName":k[1]})

                    ## Read Modes
                    elif Mode == "Layout" and not line.startswith("//SC"): #todo remove startswith
                        line = line.replace("\t\t","\t")
                        k = line.split("\t")
                        MSKLine = {}
                        index = 0
                        for bit in k:

                            if index == 0:
                                MSKLine['SC'] = bit
                            elif index == 1:
                                MSKLine['VK'] = bit
                            elif index == 2:
                                MSKLine['CAPS'] = bool(int(bit))
                            elif bit.startswith("//"):
                                MSKLine['Names'] = bit[3:].split(', ')
                            elif index > 2:
                                currentKey = {}
                                currentKey['Column'] = index+1
                                if len(bit) == 4:
                                    currentKey['Code'] = [bit]
                                    currentKey['Glyph'] = chr(int(bit,16))
                                elif len(bit) == 5:
                                    currentKey['DK'] = True
                                    #TODO Can 2 codes exist? If so, need to move this down.
                                    currentKey['Code'] = [bit[:-1]]
                                elif bit == '-1':
                                    currentKey['Code'] = ["BEEP"]
                                    #todo appears twice
                                else:
                                    currentKey['Glyph'] = bit
                                    currentKey['Code'] = []
                                    for letter in bit:
                                        currentKey['Code'].append(u'%04x'%ord(letter))
                                if 'Keys' not in MSKLine:
                                    MSKLine['Keys'] = [currentKey]
                                else:
                                    MSKLine['Keys'].append(currentKey)
                                #CurrentColumn = [c for c in passedKeyboard.MSKSShiftStateList if c['Column'] == column][0]
                            index += 1
                        #print(line)
                        passedKeyboard.addMSKLine(MSKLine)
                            
                    elif Mode == "ShiftState":
                        SSScan = re.compile(r'Column (\d+)')
                        ss = line.split("\t")
                        Column = int(SSScan.search(ss[1]).group(1))
                        ShiftRE = re.compile("Shft")
                        stateIsShifted = False
                        stateIsCtrled = False
                        stateIsAlted = False
                        if ShiftRE.search(line):
                            stateIsShifted = True
                        CtrlRE = re.compile("Ctrl")
                        if CtrlRE.search(line):
                            stateIsCtrled = True
                        AltRE = re.compile("Alt")    
                        if AltRE.search(line):
                            stateIsAlted = True

                        KBShiftStates[ss[0]] = {"SSID":ss[0],"Column":Column,"Shift":stateIsShifted,"Ctrl":stateIsCtrled,"Alt":stateIsAlted}
                        passedKeyboard.addMSKStates({"SSID":ss[0],"Column":Column,"Shift":stateIsShifted,"Ctrl":stateIsCtrled,"Alt":stateIsAlted})
                        iLevels = iLevels + 1
                       
    infile.close()
    print("ScannedMSK")

def GenerateKMRules(passedKeyboard):
    if passedKeyboard.NativeFormat == "MSKLC":
        comboNum = 1
        
        beginline = {'inputs':['begin','Unicode'],'outputs': ['USE(MAIN)'],'type': 'goTo','lineCount': comboNum}
        beginline['line'] = generateLine(beginline)
        comboNum += 1
        passedKeyboard.addCombo(beginline)

        mainline = {'inputs':['group(main) using keys'],'type': 'structural','lineCount': comboNum}
        mainline['line'] = generateLine(beginline)
        comboNum += 1
        passedKeyboard.addCombo(mainline)
        
        for line in passedKeyboard.MSKLineList:
            KeymanKeyCode = getCrossPlatformKeycode(line['SC'],'MSKLC','Keyman')
            for key in line['Keys']:
                currentCombo = {}
                currentCombo['baseKey'] = KeymanKeyCode
                if 'DK' in key:
                    currentCombo['type'] = "rule.dk"
                else:
                    currentCombo['type'] = 'rule'
                try:
                    currentColumn = [c for c in passedKeyboard.MSKStateList if c['Column'] == key['Column']][0]
                except:
                    print("Column " + str(key['Column']) + " doesn't exist!")
                currentCombo['inputs'] = ['+']
                KMKeyDef = {}
                fullKeyString = "["
                KMKeyDef["isNCAPS"] = True
                fullKeyString += "NCAPS"
                #MSK interprets CTRL+ALT instead of RALT
                if (currentColumn['Ctrl'] and currentColumn['Alt']):
                    KMKeyDef["isRALT"] = True
                    fullKeyString += " RALT"
                    KMKeyDef["isALT"] = False
                    KMKeyDef["isCTRL"] = False
                else:
                    if currentColumn['Ctrl']:
                        KMKeyDef["isCTRL"] = currentColumn['Ctrl']
                        if currentColumn['Ctrl']:
                            fullKeyString += " CTRL"
                    else:
                        KMKeyDef["isCTRL"] = False
                    if currentColumn['Alt']:
                        KMKeyDef["isALT"] = currentColumn['Alt']
                        if currentColumn['Alt']:
                            fullKeyString += " ALT"
                    else:
                        KMKeyDef["isALT"] = False
                    KMKeyDef["isRALT"] = False
                KMKeyDef["isSHIFT"] = currentColumn['Shift']
                if currentColumn['Shift']:
                    fullKeyString += " SHIFT"
                KMKeyDef["isLALT"] = False
                KMKeyDef["isRCTRL"] = False
                KMKeyDef["isLCTRL"] = False
                KMKeyDef["isCAPS"] = False
                KMKeyDef['isKey'] = KeymanKeyCode
                fullKeyString += " " + KeymanKeyCode +']'
                KMKeyDef['fullKey'] = fullKeyString
                currentCombo['inputs'].append(KMKeyDef)
                
                #Handle Outputs here
                currentCombo['outputs'] = []
                if not 'DK' in key:
                    for output in key['Code']:
                        if output == 'BEEP':
                            currentCombo['outputs'].append(output)
                            currentCombo['type'] = "rule.deadEnd"
                        else:
                            currentCombo['outputs'].append("U+" + output)

                else:
                    for output in key['Code']:
                        currentCombo['outputs'].append("DK(" + output + ")")
                        currentCombo['type'] = "rule.dk"
                currentCombo['lineCount'] = comboNum
                comboNum += 1
                currentCombo['line'] = generateLine(currentCombo)
                s = " "
                currentCombo['baseOutput'] = s.join(currentCombo['outputs'])
                passedKeyboard.addCombo(currentCombo)

                #Handle Caps Alternates, these need to be explicit in KM
                if not line['CAPS']: # is true
                    capsCurrentCombo  = copy.deepcopy(currentCombo)
                    for input in capsCurrentCombo['inputs']:
                        if 'fullKey' in input:
                            input["isCAPS"] = True
                            input["isNCAPS"] = False
                            input["fullKey"] = generateFullKey(input)
                    capsCurrentCombo['lineCount'] = comboNum
                    comboNum += 1
                    capsCurrentCombo['line'] = generateLine(capsCurrentCombo)
                    s = " "
                    capsCurrentCombo['baseOutput'] = s.join(capsCurrentCombo['outputs'])
                    passedKeyboard.addCombo(capsCurrentCombo)
                elif line['CAPS']:
                    passedKeyboard.setCapsAffectsKeyboard(True)
                    skip = False
                    capsCurrentCombo  = copy.deepcopy(currentCombo)
                    for input in capsCurrentCombo['inputs']:
                        if 'fullKey' in input:
                            if (input['isNCAPS'] == True) and (input["isCAPS"] == False) and (input["isSHIFT"] == False):
                                input['isNCAPS'] = False
                                input["isCAPS"] = True
                                input["isSHIFT"] = True
                            elif (input["isSHIFT"] == True):
                                input['isNCAPS'] = False
                                input["isCAPS"] = True
                                input["isSHIFT"] = False
                            elif (input['isNCAPS'] == True) and (input["isCAPS"] == False) and (input["isSHIFT"] == True) and (input["isRalt"] == True):
                                input['isNCAPS'] = False
                                input["isCAPS"] = True
                                input["isSHIFT"] = False
                            input["fullKey"] = generateFullKey(input)
                    capsCurrentCombo['lineCount'] = comboNum
                    comboNum += 1
                    capsCurrentCombo['line'] = generateLine(capsCurrentCombo)
                    s = " "
                    capsCurrentCombo['baseOutput'] = s.join(capsCurrentCombo['outputs'])
                    if not skip:
                        passedKeyboard.addCombo(capsCurrentCombo)
                    skip = False
        if len(passedKeyboard.MSKDeadkeyList) > 0:
            currentMatchCombo = {}
            currentMatchCombo['type'] = 'goTo'
            currentMatchCombo['inputs'] = ['match']
            currentMatchCombo['outputs'] = ['USE(deadkeys)']
            currentMatchCombo['lineCount'] = comboNum
            comboNum += 1
            currentMatchCombo['line'] = generateLine(currentMatchCombo)
            passedKeyboard.addCombo(currentMatchCombo)

            currentGroupCombo = {}
            currentGroupCombo['type'] = 'structural'
            currentGroupCombo['inputs'] = ['group(deadkeys)']
            currentGroupCombo['lineCount'] = comboNum
            comboNum += 1
            currentGroupCombo['line'] = generateLine(currentGroupCombo)
            passedKeyboard.addCombo(currentGroupCombo)

        for dk in passedKeyboard.MSKDeadkeyList:
            currentDKCombo = {}
            currentDKCombo['baseKey'] = 'dk(' + dk['DK'].upper() + ')'
            currentDKCombo['type'] = 'rule.generated'
            currentDKCombo['inputs'] = ['dk(' + dk['DK'].upper() + ')','U+' + dk['Key'].upper()]
            currentDKCombo['outputs'] = ['U+' + dk['Result'].upper()]
            currentDKCombo['lineCount'] = comboNum
            comboNum += 1
            currentDKCombo['line'] = generateLine(currentDKCombo)
            s = " "
            currentDKCombo['baseOutput'] = s.join(currentDKCombo['outputs'])
            passedKeyboard.addCombo(currentDKCombo)
            #finish
        print('Finished Dk')

def printKMN(passedKeyboard, forcedFilter = []):
    f = open("outputs/" + passedKeyboard.getKeyboardName() + '.kmn', 'w', encoding="utf-8")
    if passedKeyboard.NativeFormat == "MSKLC":
        f.write("store(&NAME) '"+ passedKeyboard.getVariable('Name') + "'"+"\n")
        f.write("store(&COPYRIGHT) '"+ passedKeyboard.getVariable('Copyright') + "'"+"\n")
        f.write("store(&KEYBOARDVERSION) '"+ passedKeyboard.getVariable('Version') + "'"+"\n\n")
        f.write("begin Unicode > use(main)\n")
        f.write("group(main) using keys\n")

        filterKeys = []
        #Testing to see if some rules can be filtered because there are no valid rules.
        needCtrl = False
        needLCtrl = False
        needRCtrl = False
        needAlt = False
        needLAlt = False
        needRAlt = False
        needShift = False
        needNCaps = False
        needCaps = False
        for line in passedKeyboard.getCombos():
            if 'inputs' in line and 'type' in line and line['type'] == "rule":
                for input in line['inputs']:
                    if "fullKey" in input:
                        if input['isCTRL']:
                            needCtrl = True
                        if input['isLCTRL']:
                            needLCtrl = True
                        if input['isRCTRL']:
                            needRCtrl = True
                        if input['isALT']:
                            needAlt = True
                        if input['isLALT']:
                            needLAlt = True
                        if input['isRALT']:
                            needRAlt = True
                        if input['isSHIFT']:
                            needShift = True
                        if input['isNCAPS']:
                            needNCaps = True
                        if input['isCAPS']:
                            needCaps = True
        if not needCtrl and 'isCTRL' not in filterKeys:
            filterKeys.append('isCTRL')
        if not needLCtrl and 'isLCTRL' not in filterKeys:
            filterKeys.append('isLCTRL')
        if not needRCtrl and 'isRCTRL' not in filterKeys:
            filterKeys.append('isRCTRL')
        if not needAlt and 'isALT' not in filterKeys:
            filterKeys.append('isALT')
        if not needLAlt and 'isLALT' not in filterKeys:
            filterKeys.append('isLALT')
        if not needRAlt and 'isRALT' not in filterKeys:
            filterKeys.append('isRALT')
        if not needShift and 'isSHIFT' not in filterKeys:
            filterKeys.append('isSHIFT')
        for filter in forcedFilter:
            filterKeys.append(filter)
        #Printing regular rules
        allCombos = passedKeyboard.getCombos()
        #sorted(keyboard, key=lambda k: ("baseKey" not in k, k.get("baseKey", None),"baseOutput" not in k, k.get("baseOutput", None)))
        regularCombos = [x for x in allCombos if (x['type'] == 'rule') or (x['type'] == 'rule.dk') or (x['type'] == 'rule.deadEnd')]
        sortedRegularCombos = sorted(regularCombos, key=lambda k: ("baseKey" not in k, k.get("baseKey", None),"baseOutput" not in k, k.get("baseOutput", None)))
        for key, group in groupby(sortedRegularCombos, key=lambda k: ("baseKey" not in k, k.get("baseKey", "*None*"))):
            f.write("c " + key[1] +"\n")
            for thing in group:
                skip = False
                for input in thing['inputs']:
                    for filter in filterKeys:
                        if filter in input and input[filter]:
                            skip = True
                if not skip:
                    f.write(thing['line'].strip()+"\n")
        f.write("match > use(deadkeys)\n")
        f.write("group(deadkeys)\n")
        generatedCombos = sorted([x for x in allCombos if 'generated' in x['type']], key=lambda k: ("baseKey" not in k, k.get("baseKey", None),"baseOutput" not in k, k.get("baseOutput", None)))
        for keys, groups in groupby(generatedCombos, key=lambda k: ("baseKey" not in k, k.get("baseKey", '*None*'))):
            f.write("c " + keys[1] +"\n")
            storeListInput = []
            storeListOutput = []
            s = " "
            for thing in groups:
                storeListInput.append(thing['inputs'][1])
                if thing['outputs'][0] == thing['inputs'][1]:
                    # MSK and Keyman handle doubled DK's differently.
                    storeListOutput.append("dk(" + thing['outputs'][0][3:-1] + ")")
                else:
                    storeListOutput.append(thing['outputs'][0]) 
            inner = "store(dkf" + keys[1][3:-1] + ") " + s.join(storeListInput)
            outer = "store(dkt" + keys[1][3:-1] + ") " + s.join(storeListOutput)
            dkrule = keys[1] + " any(dkf" + keys[1][3:-1] + ") > index(dkt" + keys[1][3:-1] + ", 2)"
            f.write(inner + "\n")
            f.write(outer + "\n")
            f.write(dkrule + "\n\n")
        f.close()
        print('KMN exported')

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def generateLine(combo):
    concatLine = ""
    for input in combo['inputs']:
        if 'fullKey' in input:
            concatLine += " " + input['fullKey']
        else:
            concatLine += " " + input
    if 'outputs' in combo:
        concatLine += " >"
        for output in combo['outputs']:
            concatLine += " " + output
        concatLine = concatLine.strip()
    return concatLine

def generateFullKey(keydef):
    fullKeyString = "["
    if keydef["isNCAPS"] == True:
        fullKeyString += "NCAPS"
    if keydef['isCAPS']:
        fullKeyString += " CAPS"
    if not (keydef['isCTRL'] and keydef['isALT']):
        if keydef['isCTRL']:
            fullKeyString += " CTRL"
        if keydef['isALT']:
            fullKeyString += " ALT"
        if keydef['isRALT']:
            fullKeyString += " RALT"
    else:
        fullKeyString += " RALT"
    if keydef['isRCTRL']:
        fullKeyString += " RCTRL"
    if keydef['isLCTRL']:
        fullKeyString += " LCTRL"
    if keydef['isLALT']:
        fullKeyString += " LALT"
    if keydef['isSHIFT']:
        fullKeyString += " SHIFT"
    fullKeyString += " " + keydef['isKey'] +']'
    fullKeyString = fullKeyString.replace('[ ','[')
    return fullKeyString


def getCrossPlatformKeycode(key,inputPlatfrom,outputPlatform):
    if inputPlatfrom == "MSKLC":
        try:
            relevantLine = [x for x in kbLinks if x['scancode'] == key][0]
        except:
            print('ScanCode Unrecognized')
        if outputPlatform == "Keyman":
            return relevantLine['keyman']
def verbose(lineNumber, inputString):
    if isVerbose:
        print(lineNumber, ": ", inputString)

def sterilizeLine(line, replaceSpaces=False):
    #remove EOL
    if line.endswith("\n"):
        line = line[:-1].strip()
    #remove BOM
    if line.startswith(u'\ufeff'):
        line = line[1:]
    #compress multiple spaces
    rex = re.compile(r'\t')
    line = rex.sub(' ', line)
    rex = re.compile(r' {2,}')
    line = rex.sub(' ', line)
    # remove comments
    rex = re.compile(r' * c .*')
    line = rex.sub('', line)

    if replaceSpaces:
        line = line.replace(u" ", u"---")
    return line

def parseKeyman(passedKeyboard, keymanFilename, generateDeadkeys = False):
    lineCount = 0
    infile = open(keymanFilename, mode='r', encoding='utf-8')
    currentGroup = {}
    for line in infile:
        if (line != "\n"):
            #line = line[:-2].strip()
            line = sterilizeLine(line)
            if (len(line) != 0):
                resultDef = {}
                upperLine = line.upper()
                lineCount = lineCount + 1
                verbose(lineCount,line)
                if (upperLine.startswith(u"STORE(&")):
                    variableSearch = re.search('store\((.*)\)', line, re.IGNORECASE)
                    variableName = "Undefined"
                    value = ""
                    if variableSearch:
                        variableName = variableSearch.group(1)

                    valueSearch = re.search(r'store\(.*?\) (.*)',line, re.IGNORECASE)
                    if valueSearch:
                        value = valueSearch.group(1).strip()[1:-1]
                    passedKeyboard.setVariable({variableName: value})
                    #TODO is this unnecessary?
                    resultDef[variableName] = value
                    tempProps = {}
                    tempProps[variableName.upper()] = value
                    resultDef['type'] = "store"
                    #if filenameToParse not in kbProps:
                    #    kbProps[filenameToParse] = {}              
                    #kbProps[filenameToParse].update(tempProps)

                elif (upperLine.startswith(u"STORE")):

                    verbose(lineCount,"It's a store")
                    storeSearch = re.search('store\((.*?)\)', line, re.IGNORECASE)
                    if storeSearch:
                        resultDef["storeName"] = storeSearch.group(1)
                    storeItemList = line.split(")",1)[1].strip()
                    resultDef['fullStore'] = storeItemList
                    resultDef['type'] = "store"
                    oldLen = len(storeItemList)
                    pattern1 = r'("[^\s]*? [^\s]*?")'
                    if re.search(pattern1,storeItemList):
                        tempbits = re.findall(pattern1,storeItemList)
                        for bit in tempbits:
                            newBit = bit.replace(" ","---")
                            storeItemList = storeItemList.replace(bit,newBit)
                    pattern2 = r"('[^\s]*? [^\s]*?')"
                    if re.search(pattern2,storeItemList):
                        tempbits = re.findall(pattern2,storeItemList)
                        for bit in tempbits:
                            newBit = bit.replace(" ","---")
                            storeItemList = storeItemList.replace(bit,newBit)
                    if len(storeItemList) != oldLen:
                        verbose(lineCount,"Space Protected")
                    storeItems = re.split("\s|\t",storeItemList)
                    if "storeItems" not in resultDef:
                        resultDef['storeItems'] = []
                    for item in storeItems:
                        item = item.replace("---"," ").strip()
                        if item.startswith("U+"):
                            resultDef['storeItems'].append(item.upper())
                        elif item.upper().startswith("DK"):
                            resultDef['storeItems'].append(item)
                        elif item.upper().startswith("NUL"):
                            resultDef['storeItems'].append(item)
                        elif item.upper().startswith("BEEP"):
                            resultDef['storeItems'].append(item)
                        if (item.startswith("'") or item.startswith('"')):
                            item = item[1:-1]
                            for char in item:
                                resultDef['storeItems'].append(u'U+%04x'%ord(char))

                elif (upperLine.startswith(u"C ")):
                    verbose(lineCount,"It's a Comment")
                    resultDef["type"] = "comment"
                elif (upperLine.startswith(u"GROUP")):
                    verbose(lineCount,"It's a Group")
                    resultDef["line"] = line
                    resultDef["lineCount"] = lineCount
                    resultDef["type"] = "structural"
                else:
                    resultDef = processKeymanRule(line,lineCount,currentGroup, passedKeyboard)
                    if resultDef is None:
                        print("This line is unparsed:", line)
                    resultDef["line"] = line
                    resultDef["lineCount"] = lineCount
                # Storing Starts Here
                resultDef["line"] = line
                resultDef["lineCount"] = lineCount
                passedKeyboard.addCombo(resultDef)
           
    #Expand
    for line in passedKeyboard.getCombos():
        #Need an iterator 
        if ("dk" in line['type']) and ("index" in line['type']):
            outputTargetStores = []
            outputTargetLists = []
            outputLines = []
            inputTargetStores = []
            inputTargetLists = []
            inputLines = []
            indexNumCounter = 0
            # counted items have parentheses
            importantInputs = [i for i in line['inputs'] if ("(" in i)]
            importantOutputs = [i for i in line['outputs'] if ("(" in i)]
            for item in importantOutputs: #from
                if item.upper().startswith("INDEX"):
                    splitIndex = re.split(r'\(|\)|,',item)
                    outputLine = item
                    outputTargetStore = splitIndex[1]
                    outputTargetList = [i['storeItems'] for i in passedKeyboard.getCombos() if ('storeName' in i) and (i['storeName'] == outputTargetStore)]
                    inputTargetStore = importantInputs[int(splitIndex[2])-1][4:-1]
                    inputLine = importantInputs[int(splitIndex[2])-1]
                    inputTargetList = [i['storeItems'] for i in passedKeyboard.getCombos() if ('storeName' in i) and (i['storeName'] == inputTargetStore)]
                    if (len(inputTargetList) < 1) or len(outputTargetList) < 1:
                        print('This group is Broken')
                    if len(inputTargetList[0]) != len(outputTargetList[0]):
                        print(inputTargetStore, " and ", outputTargetStore, " are not the same length!")
                    outputTargetStores.append(outputTargetStore)
                    outputTargetLists.append(outputTargetList[0]) #was [0]
                    inputTargetStores.append(inputTargetStore)
                    inputTargetLists.append(inputTargetList[0])
                    inputLines.append(inputLine)
                    outputLines.append(outputLine)
                   #was [0]
                    indexNumCounter = indexNumCounter + 1

            #theTable = generateCombos(line,importantInputs, inputTargetStores, inputTargetLists, inputLines, importantOutputs, outputTargetStores, outputTargetLists, outputLines)
            #Method 1 of processinglists
            if len(outputTargetLists) == 1: # This is the problem
                    storeItemCounter = 0
                    unwrappedInputTargetLists = inputTargetLists[0]
                    unwrappedOutputTargetLists = outputTargetLists[0]
                    tempDef = []
                    for i in range(0,len(unwrappedInputTargetLists)): # was -1
                        tempDef = copy.deepcopy(line)
                        inputCounter = 0
                        copyInputs = copy.deepcopy(tempDef['inputs'])
                        for tempInput in copyInputs:
                            if inputTargetStores[0].upper() in tempInput.upper():
                                copyInputs[inputCounter] = unwrappedInputTargetLists[storeItemCounter]
                                tempDef['inputs'] = copyInputs
                            inputCounter += 1
                        outputCounter = 0
                        copyOutputs = copy.deepcopy(tempDef['outputs'])
                        for tempOutput in copyOutputs:
                            if outputTargetStores[0].upper() in tempOutput.upper():
                                copyOutputs[outputCounter] = unwrappedOutputTargetLists[storeItemCounter]
                                tempDef['outputs'] = copyOutputs
                            outputCounter += 1

                        tempDef['type'] = "rule.generated"
                        tempDef['sourceLine'] = tempDef['line']
                        if isinstance(tempDef['outputs'], list):
                            outString = " ".join(i for i in tempDef['outputs'])
                        else:
                            outString = tempDef['outputs']
                        if isinstance(tempDef['inputs'], list):
                            inString = " ".join(i for i in tempDef['inputs'])
                        else:
                            inString = tempDef['inputs']
                        newLine = inString + " > " + outString
                        tempDef['line'] = newLine
                        verbose(lineCount, newLine)
                        tempDef['sourceLineCount'] = tempDef['lineCount']
                        tempDef['baseKey'] = 'Undefined'
                        if len(inString) < 16:
                            tempDef['baseKey'] = "K_" + chr(int(inString.strip().upper()[-4:], 16))
                        tempDef['lineCount'] = lineCount
                        tempDef['baseOutput'] = outString.strip().upper()
                        tempDef.pop('isExpandable',None)
                        storeItemCounter += 1
                        lineCount += 1
                        passedKeyboard.addCombo(tempDef)
                        
            else:
                print('This is too complex')
                #numRounds = len(inputTargetLists)

def processKeymanRule(line,lineCount,currentGroup, passedkeyboard):
    rule = {}
    line = line.replace('" "', '"---"')
    line = line.replace("' '", "'---'")
    put = line.split(" > ")
    if (len(put) != 2) :
       print("Unusual number of >'s")
    else:
        pattern = re.compile(u"(index\(\w+) *, +")
        if (re.search(pattern,put[1])):
            put[1] = re.sub(pattern,r'\1,',put[1])
            #print(put[1])
        pattern = re.compile(u"\[[\w -]+?\]")
        if (re.search(pattern, put[0])):
            results = re.findall(pattern, line)
            for result in results:
                beforeString = result
                result = result.replace(" ", "---")
                if (result != beforeString):
                    put[0] = put[0].replace(beforeString, result)
        inputs = put[0].split(" ")
        outputs = put[1].split(" ")
        return buildCombo(line,inputs,outputs,lineCount, passedkeyboard)


def buildCombo(line,inputs,outputs, lineCount, passedKeyboard):
    thisCombo = {}
    thisCombo["type"] = "rule"
    for input in inputs:
        if 'inputs' not in thisCombo:
            thisCombo['inputs'] = []
        input = input.strip()
        inputUpper = input.upper()
        if (inputUpper.startswith(u"DK")):
            verbose(lineCount,"It's a deadkey.")
            thisCombo['inputs'].append(input)
            if "dk" not in thisCombo["type"]:
                thisCombo["type"] = thisCombo["type"] + ".dk"
        elif (inputUpper.startswith(u"BEGIN")):
            verbose(lineCount,"It's a Begin")
            thisCombo['inputs'].append(input)
        elif (inputUpper.startswith(u"UNICODE")):
            verbose(lineCount,"It's a UNICODE")
            thisCombo['inputs'].append(input)
        elif (inputUpper.startswith(u"ANY(")):
            verbose(lineCount,"It's an any.")
            thisCombo['inputs'].append(input)
        elif (inputUpper.startswith(u"GROUP")):
            verbose(lineCount,"It's a Group")
            thisCombo['inputs'].append(input)
        elif (inputUpper.startswith(u"MATCH")):
            verbose(lineCount,"It's a Match")
            thisCombo['inputs'].append(input)
        elif (inputUpper.startswith(u"NOMATCH")):
            verbose(lineCount,"It's a Match")
            thisCombo['inputs'].append(input)
        elif (inputUpper.startswith(u"PLATFORM")):
            verbose(lineCount,"It's a Platform")
            thisCombo['inputs'].append(input)
            touchPlatforms = ["TOUCH","IOS","ANDROID"]
            for platform in touchPlatforms:
                if (platform in inputUpper):
                    if "touch" not in thisCombo["type"]:
                        thisCombo["type"] = thisCombo["type"] + ".touch"
        elif (input.startswith(u"+")):
            verbose(lineCount,"It's a Plus")
            thisCombo['inputs'].append(input)
        elif (input.startswith(u"U+")):
            verbose(lineCount,"It's a Unicode ID")
            thisCombo['inputs'].append(input.upper())
        elif (input.startswith(u"[")):
            keyCombo = {"isSHIFT" : False, "isNCAPS" : False, "isCAPS" : False,
                        "isRALT" : False, "isLALT" : False, "isALT" : False,
                        "isRCTRL" : False, "isLCTRL" : False, "isCTRL" : False,
                        "isKey" : ""}
            verbose(lineCount,"It's a keypress")
            keyCombo['fullKey'] = inputUpper.replace("---", " ")
            inputUpper = inputUpper[1:-1]
            tempProps = {}
            if "SHIFT" in inputUpper:
                isSHIFT = True
                keyCombo['isSHIFT'] = True
                inputUpper = inputUpper.replace("SHIFT","").strip()
                passedKeyboard.setVariable({'containsSHIFT': True})
                tempProps['containsSHIFT'] = True
            if "NCAPS" in inputUpper:
                keyCombo['isNCAPS'] = True
                inputUpper = inputUpper.replace("NCAPS","").strip()
                passedKeyboard.setVariable({'containsNCAPS': True})
                tempProps['containsNCAPS'] = True
            if "CAPS" in inputUpper:
                keyCombo['isCAPS'] = True
                inputUpper = inputUpper.replace("CAPS","").strip()
                passedKeyboard.setVariable({'containsCAPS': True})
                tempProps['containsCAPS'] = True
            if "RALT" in inputUpper:
                keyCombo['isRALT'] = True
                inputUpper = inputUpper.replace("RALT","").strip()
                passedKeyboard.setVariable({'containsRALT': True})
                tempProps['containsRALT'] = True
            if "LALT" in inputUpper:
                keyCombo['isLALT']= True
                inputUpper = inputUpper.replace("LALT","").strip()
                passedKeyboard.setVariable({'containsLALT': True})
                tempProps['containsLALT'] = True
            if "ALT" in inputUpper:
                keyCombo['isALT'] = True
                inputUpper = inputUpper.replace("ALT","").strip()
                passedKeyboard.setVariable({'containsALT': True})
                tempProps['containsALT'] = True
            if "LCTRL" in inputUpper:
                keyCombo['isLCTRL'] = True
                inputUpper = inputUpper.replace("LCTRL","").strip()
                passedKeyboard.setVariable({'containsLCTRL': True})
                tempProps['containsLCTRL'] = True
            if "RCTRL" in inputUpper:
                keyCombo['isRCTRL'] = True
                inputUpper = inputUpper.replace("RCTRL","").strip()
                passedKeyboard.setVariable({'containsRCTRL': True})
                tempProps['containsRCTRL'] = True
            if "CTRL" in inputUpper:
                keyCombo['isCTRL'] = True
                inputUpper = inputUpper.replace("CTRL","").strip()
                passedKeyboard.setVariable({'containsCTRL': True})
                tempProps['containsCTRL'] = True
            if " " in inputUpper:
                print("I missed something", input)
            keyCombo["isKey"] = inputUpper.strip("-")
            thisCombo['baseKey'] = keyCombo["isKey"]
            if keyCombo["isKey"].startswith('T_'):
                if "touch" not in thisCombo["type"]:
                    thisCombo["type"] = thisCombo["type"] + ".touch"
            thisCombo['inputs'].append(keyCombo)

        #Split at --- and process
        elif (input.startswith("'") or input.startswith('"')):
            input = input[1:-1]
            if output == "---":
                output = " "
            for char in input:
                thisCombo['inputs'].append(u'U+%04x'%ord(char))
            print("It must be a string.")
        else:
            print("Where am I?")
    for output in outputs:
        if 'outputs' not in thisCombo:
            thisCombo['outputs'] = []
        output = output.strip()
        outputUpper = output.upper()
        if (outputUpper.startswith(u"DK")):
            verbose(lineCount,"It's a deadkey.")
            thisCombo['outputs'].append(output)
            if "dk" not in thisCombo["type"]:
                thisCombo["type"] = thisCombo["type"] + ".dk"
        elif (outputUpper.startswith(u"GROUP")):
            verbose(lineCount,"It's a Group")
            thisCombo['outputs'].append(outputUpper)
        elif (outputUpper.startswith(u"USE")):
            verbose(lineCount,"It's a Use")
            thisCombo['outputs'].append(outputUpper)
            thisCombo["type"] = "goTo"
        elif (outputUpper.startswith(u"INDEX")):
            verbose(lineCount,"It's a INDEX")
            thisCombo['outputs'].append(output)
            thisCombo['isExpandable'] = True
            if "index" not in thisCombo["type"]:
                thisCombo["type"] = thisCombo["type"] + ".index"
        elif (outputUpper.startswith(u"LAYER")):
            verbose(lineCount,"It's a Layer")
            thisCombo['outputs'].append(outputUpper)
        elif (outputUpper.startswith(u"BEEP")):
            verbose(lineCount,"It's a BEEP")
            thisCombo['outputs'].append(outputUpper)
            if "deadEnd" not in thisCombo["type"]:
                thisCombo['type'] = thisCombo["type"] + ".deadEnd"
        elif (outputUpper.startswith(u"NUL")):
            verbose(lineCount,"It's a NUL")
            thisCombo['outputs'].append(outputUpper)
            if "deadEnd" not in thisCombo["type"]:
                thisCombo['type'] = thisCombo["type"] + ".deadEnd"
        elif (outputUpper.startswith(u"CONTEXT")):
            verbose(lineCount,"It's a Context")
            thisCombo['outputs'].append(outputUpper)
            if "deadEnd" not in thisCombo["type"]:
                thisCombo['type'] = thisCombo["type"] + ".deadEnd"
        elif (output.startswith(u"U+")):
            verbose(lineCount,"It's a Unicode ID")
            thisCombo['outputs'].append(outputUpper)
            thisCombo['baseOutput'] = outputUpper
        elif (output.startswith("'") or output.startswith('"')):
            output = output[1:-1]
            if output == "---":
                output = " "
            for char in output:
                thisCombo['outputs'].append(u'U+%04x'%ord(char))
        else:
            print(output)
    return thisCombo

def prod(iterable):
    def add(x,y): return x*y
    functools.reduce(add, iterable)

class keyboardDefinition():
    def __init__(self,inFilename):
        self.idx = 0
        self.filename = inFilename
        self.keymanComboList = []
        self.idx = 0
        self.variableList = []
        self.MSKIndexList = []
        self.MSKStateList = []
        self.MSKLineList = []
        self.MSKDeadkeyList = []
        self.Format = ""
        self.NativeFormat = ""
        self.capsAffectsKeyboard = False
    def setCapsAffectsKeyboard(self, boolean):
        if boolean:
            self.capsAffectsKeyboard = True
        else:
            self.capsAffectsKeyboard = False
    def addMSKIndex(self, MSKIndex):
        self.MSKIndexList.append(MSKIndex)
    def addMSKStates(self,stateDict):
        self.MSKStateList.append(stateDict)
    def addMSKLine(self,MSKLine):
        self.MSKLineList.append(MSKLine)
    def addMSKDeadkey(self,MSKDeadkey):
        self.MSKDeadkeyList.append(MSKDeadkey)
    def setVariable(self, inVariable):
        if inVariable not in self.variableList:
            self.variableList.append(inVariable)
    def setNative(self, format):
        self.NativeFormat = format
    def getKeyboardName(self):
        return self.filename
    def addCombo(self, keyCombo):
        y = [v['inputs'] for v in self.keymanComboList if 'inputs' in v ]
        if ('inputs' in keyCombo) and (keyCombo['inputs'] in y):
            print("A combo with these inputs already exists in", self.filename)
            pprint(keyCombo['inputs'])
        else:           
            self.keymanComboList.append(keyCombo)
            self.idx = 0
            # Resetting index, because len(comboList) has changed.
            return True
    def getNextCombo(self):
        thisElem = self.keymanComboList[idx]
        self.idx = (self.idx + 1) % len(self.keymanComboList)
        return thisElem
    def getComboLen(self):
        return len(self.keymanComboList)
    def getCombo(index):
        thisElem = self.keymanComboList[index]
        return thisElem
    def getCombos(self):
        return self.keymanComboList
    def getVariable(self, varName):
        # Make this stable)
        response = [x[varName] for x in self.variableList if varName in x]
        if len(response) == 1:
            return response[0]
        else:
            return False
    def __exit__(self, exc_type, exc_value, traceback):
        self.package_obj.cleanup()
    def __del__(self):
        #del self.keymanComboList
        self.keymanComboList = []
        self.idx = 0
        #del self.variableList
        self.variableList = []
        self.filename = ""
        #print(self.filename, 'deleted')


class bumpindex:
    import itertools
    Array = []
    loopNum = 0
    cycleCounter = 0
    def __init__(repeatcount, inputTargetList, outputTargetList):
        cycleCounter = itertools.cycle(range(1,repeatCount))
        index = 0
        Array = [inputTargetList, outputTargetList]
        loopNum = repeatcount

        #TODO finish this
    def bump(group):
        if cycleCounter == 1:

            ReturnA = Array[1,index]
            totalCounter += 1
            index += 1
        else:
            ReturnA = Array[1,counter]
            counter += 1
        #in i
        return

def generateCombos(line,importantInputs, inputTargetStores, inputTargetLists, inputLists, importantOutputs, outputTargetStores, outputTargetLists, outputLists):
    #for i in inputTargetLists[0]:
    depth = 0
    loopCount = 0
    for lister in inputTargetLists[0]:
        if depth == 0:
            loopCount = len(lister)
            depth += 1
        else:
            loopCount = loopCount * len(lister)
            depth += 1
    changeArray = []

    for inputItem in inputTargetLists[0]:

        outputItem = outputTargetLists[0]
        #This won't work later
        repeatCount = int(loopCount / len(inputItem))
        for fullLoop in range(1,loopCount):
            index = 0
            for waitCount in range(0,repeatCount):
                changeArray.append([inputItem[index], outputItem[index]])
                #output is too deep
            index += 1
            #next item

            #Repeat
    

    #DeterminePairs
    #get length of each pair
def inferCaps(passedKeyboard):
    
    keyboard = passedKeyboard.getCombos()
    SortedCombosOutput = sorted(keyboard, key=lambda k: ("baseOutput" not in k, k.get("baseOutput", None),"baseKey" not in k, k.get("baseKey", None)))
    f = open("outputs/" + passedKeyboard.getKeyboardName() + '_InferredCaps.txt', 'w', encoding="utf-8")
    stringList = []
    for key, group in groupby(SortedCombosOutput, key=lambda k: ("baseOutput" not in k, k.get("baseOutput", None))):
        Booler = []
        inferCaps = CheckCondition(group)
        if inferCaps != None:
            stringList.append(str(inferCaps[0]) + " " + str(inferCaps[1]) + "\n")
    stringList = list(set(stringList))
    f.writelines(sorted(stringList))
    f.close


def CheckCondition(group):
    FoundSimple = False
    FoundCapsSimple = False
    FoundCapsShift = False
    FoundRaltSimple = False
    FoundRaltCapsSimple = False
    FoundCapsShiftRalt = False
    FoundNcapsShift = False
    for thing in group:
            if thing['type'] == 'rule':
                for input in thing['inputs']:
                    if "fullKey" in input:
                        if input['isNCAPS'] and not input['isSHIFT'] and not input['isRALT']:
                            FoundSimple = True
                        elif input['isCAPS'] and not input['isSHIFT'] and not input['isRALT']:
                            FoundCapsSimple = True
                        elif input['isCAPS'] and input['isSHIFT'] and not input['isRALT']:
                            FoundCapsShift = True
                        elif input['isNCAPS'] and input['isRALT'] and not input['isSHIFT']:
                            FoundRaltSimple = True
                        if input['isNCAPS'] and input['isSHIFT'] and not input['isRALT']:
                            FoundNcapsShift = True
                        elif input['isCAPS'] and input['isRALT'] and not input['isSHIFT']:
                            FoundRaltCapsSimple = True
                        elif input['isCAPS'] and input['isSHIFT'] and input['isRALT']:
                            FoundCapsShiftRalt = True
                            #CAPS Shift, caps

    if FoundSimple and FoundCapsSimple:
        return False, input["isKey"]
    if FoundRaltSimple and FoundRaltCapsSimple:
        return False, input["isKey"]
    if FoundSimple and FoundCapsShift:
        return True, input["isKey"]
    if FoundRaltSimple and FoundCapsShiftRalt:
        return True, input["isKey"]

def printKeyList(passedKeyboard, code = False, human = True, inFilter = [], deadkeyNames = []):
    w = []
    letter = ""
    category = ""
    from itertools import groupby
    from operator import itemgetter
    keyboard = passedKeyboard.getCombos()
    SortedCombosOutputs = sorted(keyboard, key=lambda k: ("outputs" not in k, k.get("outputs", None)))
    #SortedCombosOutput = sorted(keyboard, key=lambda k: ("baseOutput" not in k, k.get("baseOutput", None),"baseKey" not in k, k.get("baseKey", None)))
    #groupedCombosOutput = groupby(keyboard, key=lambda k: ("baseOutput" not in k, k.get("baseOutput", None),"baseKey" not in k, k.get("baseKey", None)))
    f = open("outputs/" + passedKeyboard.getKeyboardName() + '_Table.txt', 'w', encoding="utf-8")
    #f.write(foo.encode('utf8'))
    for key, group in groupby(SortedCombosOutputs, key=lambda k: ("outputs" not in k, k.get("outputs", None))):
        for thing in group:
            getDescrip = ""
            #Labels are only needed if both are enabled.
            if code: 
                stringtoWrite = "User:"
            else:
                stringtoWrite = ""
            if human: 
                codedString = "Code:"
            else:
                codedString = ""
            if 'inputs' in thing:
                for input in thing['inputs']:
                    if isinstance(input, dict):
                        if input['isCAPS']:
                            stringtoWrite = stringtoWrite + "\t" + "[Caps]"
                        if input['isSHIFT']:
                            stringtoWrite = stringtoWrite + "\t" + "[Shift]"
                        if input['isALT']:
                            stringtoWrite = stringtoWrite + "\t" + "[Alt]"
                        if input['isRALT']:
                            stringtoWrite = stringtoWrite + "\t" + "[AltGr]"
                        if input['isLALT']:
                            stringtoWrite = stringtoWrite + "\t" + "[Left Alt]"
                        if input['isCTRL']:
                            stringtoWrite = stringtoWrite + "\t" + "[Ctrl]"
                        if input['isRCTRL']:
                            stringtoWrite = stringtoWrite + "\t" + "[Right Control]"
                        if input['isLCTRL']:
                            stringtoWrite = stringtoWrite + "\t" + "[Left Control]"
                        stringtoWrite = stringtoWrite + "\t[" + input['isKey'] + "]"
                        codedString = codedString + "\t" + input['fullKey']
                    else:
                        if input.startswith("dk"):
                            if (input.upper() == "DK(003B)") or (input.upper() == "DK(0021)"):
                                stringtoWrite = stringtoWrite + "\t" + "[CAM Key]"
                                codedString = codedString + "\t" + input
                            else:
                                letterCode = input.strip().upper()[3:-1]
                                letter = chr(int(letterCode, 16))
                                stringtoWrite = stringtoWrite + "\t" + letter
                                codedString = codedString + "\t" + input
                        elif input.startswith("U+"):
                            letterCode = input.strip().upper()[2:]
                            letter = chr(int(letterCode, 16))
                            stringtoWrite = stringtoWrite + "\t" + letter
                            codedString = codedString + "\t" + input
                        elif input.startswith("+"):
                            x = ""
                        else:
                            stringtoWrite = stringtoWrite + "\t" + input
                            codedString = codedString + "\t" + input
            stringtoWrite = stringtoWrite + "\t➜"
            codedString = codedString + "\t➜"
            if 'outputs' in thing:
                for output in thing['outputs']:
                    if output.startswith("dk"):
                        for theKey in deadkeyNames:
                            if output.upper() == theKey[0].upper():
                                category = "Deadkey"
                        stringtoWrite = stringtoWrite + "\t" + output
                        codedString = codedString + "\t" + output
                    elif output.startswith("U+"):
                        getDescrip = output
                        letterCode = output.strip().upper()[2:]
                        letter = chr(int(letterCode, 16))
                        if output.startswith("U+030") or output.startswith("U+031") or output.startswith("U+032") or output.startswith("U+033") or output.startswith("U+034") or output.startswith("U+035") or output.startswith("U+036") or output.startswith("U+1D"):
                            stringtoWrite = stringtoWrite + "\t'" + chr(int("25CC", 16)) + letter + "'"
                            codedString = codedString + "\t" + output
                        else:
                            stringtoWrite = stringtoWrite + "\t'" + letter + "'"
                            codedString = codedString + "\t" + output
                    else:
                        stringtoWrite = stringtoWrite + "\t" + output
                        codedString = codedString + "\t" + output
            for item in inFilter:
                if (item.upper() in stringtoWrite.upper()) or (item.upper() in codedString.upper()):
                    codedString = ""
                    stringtoWrite = ""
            if ('inputs' not in thing) or ('outputs' not in thing):
                codedString = ""
                stringtoWrite = ""
            if codedString != "" and code:
                codedString = codedString + "\t" + str(thing['lineCount'])
                if getDescrip in UnicodeArchive:
                    thisOutput = UnicodeArchive[getDescrip]
                    #if category == '':
                    category = thisOutput['Category-Long']
                w.append([codedString, category, letter])
                f.write(codedString + "\n")
            if stringtoWrite != "" and human:
                if getDescrip in UnicodeArchive:
                    thisOutput = UnicodeArchive[getDescrip]
                    if thisOutput["Name"] != "":
                        stringtoWrite = stringtoWrite + "\t" + thisOutput['Name']
                    if getDescrip in UnicodeArchive:
                        thisOutput = UnicodeArchive[getDescrip]
                        #if category == '':
                        category = thisOutput['Category-Long']
                w.append([stringtoWrite, category, letter])
                f.write(stringtoWrite + "\n")
        f.write("\n")
    #combosWithoutDups = RemoveDups(w)
    #SortedCombos = sorted(combosWithoutDups, key=lambda k: (k[1], k[2]))
    SortedCombos = sorted(w, key=lambda k: (k[1], k[2]))
    
    for key, group in groupby(SortedCombos, key=lambda k: (k[1])):
        f.write("########\n" + key + "\n########\n")
        for thing in group:
            f.write(thing[0] + "\n")
    f.close()
    print("Coded")

def RemoveDups(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

def importUnicode():
    CodePoint = {}
    u = open('Unicode/UnicodeData.txt', 'r', encoding="utf-8")
    for line in u:
        if "\n" in line:
            line = line[:-2]
        elements = line.split(';')

        CodepointProps = {}
        if elements[1] != '':
            CodepointProps['Name'] = elements[1]
        if elements[2] != '':
            CodepointProps['Category'] = elements[2]
            cat = elements[2]
            if cat == "Lu":
                CodepointProps['Category-Long'] = "Uppercase Letter"
                CodepointProps['Category-Descrip'] = "an uppercase letter"
            if cat == "Ll":
                CodepointProps['Category-Long'] = "Lowercase Letter"
                CodepointProps['Category-Descrip'] = "a lowercase letter"
            if cat == "Lt":
                CodepointProps['Category-Long'] = "Titlecase Letter"
                CodepointProps['Category-Descrip'] = "a digraphic character, with first part uppercase"
            if cat == "Lm":
                CodepointProps['Category-Long'] = "Modifier Letter"
                CodepointProps['Category-Descrip'] = "a modifier letter"
            if cat == "Lo":
                CodepointProps['Category-Long'] = "Other Letter"
                CodepointProps['Category-Descrip'] = "other letters, including syllables and ideographs"
            if cat == "Mn":
                CodepointProps['Category-Long'] = "Nonspacing Mark"
                CodepointProps['Category-Descrip'] = "a nonspacing combining mark (zero advance width)"
            if cat == "Mc":
                CodepointProps['Category-Long'] = "Spacing Mark"
                CodepointProps['Category-Descrip'] = "a spacing combining mark (positive advance width)"
            if cat == "Me":
                CodepointProps['Category-Long'] = "Enclosing Mark"
                CodepointProps['Category-Descrip'] = "an enclosing combining mark"
            if cat == "Nd":
                CodepointProps['Category-Long'] = "Decimal Number"
                CodepointProps['Category-Descrip'] = "a decimal digit"
            if cat == "Nl":
                CodepointProps['Category-Long'] = "Letter Number"
                CodepointProps['Category-Descrip'] = "a letterlike numeric character"
            if cat == "No":
                CodepointProps['Category-Long'] = "Other Number"
                CodepointProps['Category-Descrip'] = "a numeric character of other type"
            if cat == "Pc":
                CodepointProps['Category-Long'] = "Connector Punctuation"
                CodepointProps['Category-Descrip'] = "a connecting punctuation mark, like a tie"
            if cat == "Pd":
                CodepointProps['Category-Long'] = "Dash Punctuation"
                CodepointProps['Category-Descrip'] = "a dash or hyphen punctuation mark"
            if cat == "Ps":
                CodepointProps['Category-Long'] = "Open Punctuation"
                CodepointProps['Category-Descrip'] = "an opening punctuation mark (of a pair)"
            if cat == "Pe":
                CodepointProps['Category-Long'] = "Close Punctuation"
                CodepointProps['Category-Descrip'] = "a closing punctuation mark (of a pair)"
            if cat == "Pi":
                CodepointProps['Category-Long'] = "Initial Punctuation"
                CodepointProps['Category-Descrip'] = "an initial quotation mark"
            if cat == "Pf":
                CodepointProps['Category-Long'] = "Final Punctuation"
                CodepointProps['Category-Descrip'] = "a final quotation mark"
            if cat == "Po":
                CodepointProps['Category-Long'] = "Other Punctuation"
                CodepointProps['Category-Descrip'] = "a punctuation mark of other type"
            if cat == "Sm":
                CodepointProps['Category-Long'] = "Math Symbol"
                CodepointProps['Category-Descrip'] = "a symbol of mathematical use"
            if cat == "Sc":
                CodepointProps['Category-Long'] = "Currency Symbol"
                CodepointProps['Category-Descrip'] = "a currency sign"
            if cat == "Sk":
                CodepointProps['Category-Long'] = "Modifier Symbol"
                CodepointProps['Category-Descrip'] = "a non-letterlike modifier symbol"
            if cat == "So":
                CodepointProps['Category-Long'] = "Other Symbol"
                CodepointProps['Category-Descrip'] = "a symbol of other type"
            if cat == "Zs":
                CodepointProps['Category-Long'] = "Space Separator"
                CodepointProps['Category-Descrip'] = "a space character (of various non-zero widths)"
            if cat == "Zl":
                CodepointProps['Category-Long'] = "Line Separator"
                CodepointProps['Category-Descrip'] = "U+2028 LINE SEPARATOR only"
            if cat == "Zp":
                CodepointProps['Category-Long'] = "Paragraph Separator"
                CodepointProps['Category-Descrip'] = "U+2029 PARAGRAPH SEPARATOR only"
            if cat == "Cc":
                CodepointProps['Category-Long'] = "Control"
                CodepointProps['Category-Descrip'] = "a C0 or C1 control code"
            if cat == "Cf":
                CodepointProps['Category-Long'] = "Format"
                CodepointProps['Category-Descrip'] = "a format control character"
            if cat == "Cs":
                CodepointProps['Category-Long'] = "Surrogate"
                CodepointProps['Category-Descrip'] = "a surrogate code point"
            if cat == "Co":
                CodepointProps['Category-Long'] = "Private Use"
                CodepointProps['Category-Descrip'] = "a private-use character"
        if elements[3] != '':
            CodepointProps['Combining Class'] = elements[3]
        if elements[4] != '':
            CodepointProps['Bidi Class'] = elements[4]
        if elements[5] != '':
            CodepointProps['Decomp Mapping'] = elements[5]
        if elements[6] != '':
            CodepointProps['Decimal Value'] = elements[6]
        if elements[7] != '':
            CodepointProps['Digit Value'] = elements[7]
        if elements[8] != '':
            CodepointProps['Numeric Value'] = elements[8]
        if elements[9] != '' and elements[9] != "N":
            CodepointProps['Bidi Mirrored'] = elements[9]
        if elements[10] != '' and elements[10] != "NULL":
            CodepointProps['Unicode 1 Name'] = elements[10]
        if elements[11] != '':
            CodepointProps['Comment'] = elements[11]
        if elements[12] != '':
            CodepointProps['Uppercase'] = elements[12]
        if elements[13] != '':
            CodepointProps['Lowercase'] = elements[13]
        #if (elements[14] is not Null) and (elements[14] != ''):
        #    CodepointProps['Titlecase'] = elements[14]
        codeName = "U+" + elements[0]
        CodePoint[codeName] = CodepointProps 
        #print("Yo")
    return CodePoint
    # https://github.com/jessetane/unicode-database-parser/blob/master/defs.json

def outputKeyValues(passedKeyboard):
    from itertools import groupby
    from operator import itemgetter
    keyboard = passedKeyboard.getCombos()
    SortedCombosKey = sorted(keyboard, key=lambda k: ("baseKey" not in k, k.get("baseKey", None),"baseOutput" not in k, k.get("baseOutput", None)))
    SortedCombosOutput = sorted(keyboard, key=lambda k: ("baseOutput" not in k, k.get("baseOutput", None),"baseKey" not in k, k.get("baseKey", None)))
    #groupedCombosOutput = groupby(keyboard, key=lambda k: ("baseOutput" not in k, k.get("baseOutput", None),"baseKey" not in k, k.get("baseKey", None)))
    f = open("outputs/" + passedKeyboard.getKeyboardName() + '_SortedCombos.txt', 'w', encoding="utf-8")
    #f.write(foo.encode('utf8'))
    for key, group in groupby(SortedCombosOutput, key=lambda k: ("baseOutput" not in k, k.get("baseOutput", None))):
        for thing in group:
            if 'baseOutput' in thing:
                tempBaseKey = ""
                if 'baseKey' in thing:
                    tempBaseKey = thing['baseKey']
                    spacer = " - "
                    stringtoWrite = thing['line'] + spacer + tempBaseKey
                f.write(stringtoWrite + "\n")

        f.write("\n")
    f.close()
    # https://stackoverflow.com/questions/29051573/python-filter-list-of-dictionaries-based-on-key-value

def missingCombo(passedKeyboard):
    from itertools import groupby
    from operator import itemgetter
    keyboard = passedKeyboard.getCombos()
    SortedCombosKey = sorted(keyboard, key=lambda k: ("baseKey" not in k, k.get("baseKey", None),"baseOutput" not in k, k.get("baseOutput", None)))
    f = open("outputs/" + passedKeyboard.getKeyboardName() + '_InferredCaps.txt', 'w', encoding="utf-8")
    stringList = []
    #https://help.keyman.com/DEVELOPER/language/guide/virtual-keys
    # Val   =               SHIFT    NCAPS   CAPS    RALT    LALT    ALT     RCTRL   LCTRL   CTRL
    flags0 =                [False,   False,  False,  False,  False,  False,  False,  False,  False]
    flags1_SHIFT =          [False,   False,  False,  False,  False,  False,  False,  False,  False]
    flags2_NCAPS =          [False,   True,   False,  False,  False,  False,  False,  False,  False]
    flags3_NCAPS_SHIFT =    [True,    True,   False,  False,  False,  False,  False,  False,  False]
    flags4_CAPS =           [False,   False,  True,   False,  False,  False,  False,  False,  False]
    flags5_CAPS_SHIFT =     [True,    False,  True,   False,  False,  False,  False,  False,  False]
    flags6_NCAPS_RALT =     [False,   True,   False,  True,   False,  False,  False,  False,  False]
    flags7_NCAPS_SHIFT_RALT=[True,    True,   False,  True,   False,  False,  False,  False,  False]
    flags8_RALT_CAPS =      [False,   False,  True,   True,   False,  False,  False,  False,  False]
    flags9_CAPS_SHIFT_RALT= [True,    False,  True,   True,   False,  False,  False,  False,  False]

    for key, group in groupby(SortedCombosKey, key=lambda k: ("baseKey" not in k, k.get("baseKey", None))):
        needs0 = False
        needs1 = False
        needs2 = False
        needs3 = False
        needs4 = False
        needs5 = False
        needs6 = False
        needs7 = False
        needs8 = False
        needs9 = False
        #if ("containsSHIFT" in kbProps[filenameToParse]) and ("containsNCAPS" not in kbProps[filenameToParse]) and ("containsCAPS" not in kbProps[filenameToParse]):
        if (passedKeyboard.getVariable('containsSHIFT')) and (not passedKeyboard.getVariable('containsNCAPS')) and (not passedKeyboard.getVariable('containsCAPS')):
            needs0 = True
            needs1 = True
        #elif ("containsSHIFT" in kbProps[filenameToParse]) and ("containsNCAPS" in kbProps[filenameToParse]) and ("containsCAPS" in kbProps[filenameToParse]):
        elif (passedKeyboard.getVariable('containsSHIFT')) and (passedKeyboard.getVariable('containsNCAPS')) and (passedKeyboard.getVariable('containsCAPS')):
            needs2 = True
            needs3 = True
            needs4 = True
            needs5 = True
        #if "containsRALT" in kbProps[filenameToParse]:
        if passedKeyboard.getVariable('containsRALT'):
            needs6 = True
            needs7 = True
            needs8 = True
            needs9 = True
        lastKey = ""
        for combo in group:
            testing = False
            if ("rule" in combo['type']) and ("touch" not in combo['type']):
                if "inputs" in combo:
                    for item in combo['inputs']:
                        if "fullKey" in item:
                            testing = True
                            currentFlags = [item['isSHIFT'],item['isNCAPS'],item['isCAPS'],item['isRALT'],item['isLALT'],item['isALT'],item['isRCTRL'],item['isLCTRL'],item['isCTRL']]
                            if currentFlags == flags0:
                                needs0 = False
                            if currentFlags == flags1_SHIFT:
                                needs1 = False
                            if currentFlags == flags2_NCAPS:
                                needs2 = False
                            if currentFlags == flags3_NCAPS_SHIFT:
                                needs3 = False
                            if currentFlags == flags4_CAPS:
                                needs4 = False
                            if currentFlags == flags5_CAPS_SHIFT:
                                needs5 = False
                            if currentFlags == flags6_NCAPS_RALT:
                                needs6 = False
                            if currentFlags == flags7_NCAPS_SHIFT_RALT:
                                needs7 = False
                            if currentFlags == flags8_RALT_CAPS:
                                needs8 = False
                            if currentFlags == flags9_CAPS_SHIFT_RALT:
                                needs9 = False
                            lastKey = item['isKey']

        if testing:
            if needs0 or needs1 or needs2 or needs3 or needs4 or needs5 or needs6 or needs7 or needs8 or needs9:
                print(passedKeyboard.getKeyboardName())
            if needs1:
                print("Missing [] for:" + lastKey)
            if needs1:
                print("Missing [SHIFT] for:" + lastKey)
            if needs2:
                print("Missing [NCAPS] for:" + lastKey)
            if needs3:
                print("Missing [CAPS] for:" + lastKey)
            if needs4:
                print("Missing [CAPS SHIFT] for:" + lastKey)
            if needs5:
                print("Missing [NCAPS RALT] for:" + lastKey)
            if needs6:
                print("Missing [NCAPS SHIFT] for:" + lastKey)
            if needs7:
                print("Missing [CAPS RALT] for:" + lastKey)
            if needs8:
                print("Missing [NCAPS SHIFT RALT] for:" + lastKey)
            if needs9:
                print("Missing [CAPS SHIFT RALT] for:" + lastKey)

        stringList = list(set(stringList))
        f.writelines(sorted(stringList))
        f.close

def analyzeKB(passedKeyboard, infilter, deadkeyNames):
    inferCaps(passedKeyboard)
    missingCombo(passedKeyboard)
    outputKeyValues(passedKeyboard)
    printKeyList(passedKeyboard, False, True, infilter, deadkeyNames)
    writeKeyboardGist(passedKeyboard)

def printToJson(filenameToParse):
    jsonName = filenameToParse + ".json"
    with open("outputs/" + jsonName, 'w') as fp:
        json.dump({filenameToParse : archive[filenameToParse]}, fp, indent=4)

def writeKeyboardGist(passedKeyboard, layout = 'US102'):
    #Current Supported Layouts ar US102, and AZERTY
    #thisKBProps = passedKeyboard
    header =   {
    "backcolor": "#ffffff",
    "name": passedKeyboard.getVariable('&NAME'),
    "author": passedKeyboard.getVariable('&COPYRIGHT'),
    "background": {
      "name": "Carbon fibre 5",
      "style": "background-image: url('/bg/carbonfibre/carbon_texture1876.jpg');"
    },
    "radii": "20px"
    }
    if layout == 'US102':
        row0 = rowGenerator(passedKeyboard, 0, layout) + [{ "w": 2 }, "\nBkspce"]
        row1 = [{ "w": 1.5 },"\nTab"] +  rowGenerator(passedKeyboard, 1, layout)
        row2 = [{"w": 1.75 }, "\nCaps Lock"] + rowGenerator(passedKeyboard, 2, layout) + [{"w": 2.25}, "\nEnter"]
        row3 = [{"w": 2.25},"\nShift"] + rowGenerator(passedKeyboard, 3, layout) + [{"w": 2.75},"\nShift"]
        row4 = [{"c": "#cccccc","w": 1.25},"\nCtrl",{"w": 1.25},"\nWin",{"w": 1.25},"\nAlt",{"a": 7,"w": 6.25},"",{"a": 4,"w": 1.25},"\nAlt",{"w": 1.25},"\nWin",{"w": 1.25},"\nMenu",{"w": 1.25},"\nCtrl"]
    else:
         print("I don't know that layout!")
    fullKB = [header,row0,row1,row2,row3,row4]
    jsonName = passedKeyboard.getKeyboardName() + ".kbd.json"
    with open("outputs/" + jsonName, 'w', encoding="UTF-8") as fp:
        json.dump(fullKB, fp, indent=4)

def rowGenerator(passedKeyboard, row, layout):
    expectedResult = [d for d in kbLinks if (d['row'] == row)]
    rowList = []
    # Val   =               SHIFT    NCAPS   CAPS    RALT    LALT    ALT     RCTRL   LCTRL   CTRL
    flags0_BASE =           [False,  False,  False,  False,  False,  False,  False,  False,  False]
    flags1_SHIFT =          [False,  False,  False,  False,  False,  False,  False,  False,  False]
    flags2_NCAPS =          [False,  True,   False,  False,  False,  False,  False,  False,  False]
    flags3_NCAPS_SHIFT =    [True,   True,   False,  False,  False,  False,  False,  False,  False]
    flags5_RALT =           [False,  False,  False,  True,   False,  False,  False,  False,  False]
    flags6_NCAPS_RALT =     [False,  True,   False,  True,   False,  False,  False,  False,  False]
    flags7_NCAPS_SHIFT_RALT=[True,   True,   False,  True,   False,  False,  False,  False,  False]
    for key in expectedResult:
        currentKey = {}
        currentKey['bottomLeft'] = u""
        currentKey['topLeft'] = u""
        currentKey['bottomRight'] = u""
        currentKey['topRight'] = u""
        if key['keyman'] == "K_BKSLASH":
            rowList.append({"w": 1.5})
        if 0==0:
            for combo in [a for a in passedKeyboard.getCombos() if (('baseKey' in a) and (a['baseKey'] == key['keyman']))]:
                if ("rule" in combo['type']) and ("touch" not in combo['type']) and ("deadEnd" not in combo['type']) and ("dk" not in combo['type']):
                    if "inputs" in combo:
                        for item in combo['inputs']:
                            if "fullKey" in item:
                                testing = True
                                currentFlags = [item['isSHIFT'],item['isNCAPS'],item['isCAPS'],item['isRALT'],item['isLALT'],item['isALT'],item['isRCTRL'],item['isLCTRL'],item['isCTRL']]
                                #Bottom Left
                                if (currentFlags == flags0_BASE) or (currentFlags == flags2_NCAPS):
                                    oldKey = currentKey['bottomLeft']
                                    currentKey['bottomLeft'] = u""
                                    for outItem in combo['outputs']:
                                        if "U+" in outItem:
                                            if outItem.startswith("U+030") or outItem.startswith("U+031") or outItem.startswith("U+032") or outItem.startswith("U+033") or outItem.startswith("U+034") or outItem.startswith("U+035") or outItem.startswith("U+036") or outItem.startswith("U+1D"):
                                                currentKey['bottomLeft'] = chr(int("25CC", 16))
                                                #TODO Add empty circle, do 4 times
                                            if 'bottomLeft' not in currentKey:
                                                currentKey['bottomLeft'] = chr(int(outItem.strip().upper()[-4:], 16))
                                            else:
                                                currentKey['bottomLeft'] = currentKey['bottomLeft'] + chr(int(outItem.strip().upper()[-4:], 16))
                                    if (oldKey != u"") and (oldKey != currentKey['bottomLeft']):
                                        print("These don't match:", combo['line'] )
                                #Top Left
                                if (currentFlags == flags1_SHIFT) or (currentFlags == flags3_NCAPS_SHIFT):
                                    oldKey = currentKey['topLeft']
                                    currentKey['topLeft'] = u""
                                    for outItem in combo['outputs']:
                                        if "U+" in outItem:
                                            if outItem.startswith("U+030") or outItem.startswith("U+031") or outItem.startswith("U+032") or outItem.startswith("U+033") or outItem.startswith("U+034") or outItem.startswith("U+035") or outItem.startswith("U+036") or outItem.startswith("U+1D"):
                                                #todo fix this 4 times, add U+17
                                                currentKey['topLeft'] = chr(int("25CC", 16))
                                            if 'topLeft' not in currentKey:
                                                currentKey['topLeft'] = chr(int(outItem.strip().upper()[-4:], 16))
                                            else:
                                                currentKey['topLeft'] = currentKey['topLeft'] + chr(int(outItem.strip().upper()[-4:], 16))
                                    if (oldKey != u"") and (oldKey != currentKey['topLeft']):
                                        print("These don't match:", combo['line'] )
                                #Top Right
                                if (currentFlags == flags7_NCAPS_SHIFT_RALT):
                                    oldKey = currentKey['topRight']
                                    currentKey['topRight'] = u""
                                    for outItem in combo['outputs']:
                                        if "U+" in outItem:
                                            if outItem.startswith("U+030") or outItem.startswith("U+031") or outItem.startswith("U+032") or outItem.startswith("U+033") or outItem.startswith("U+034") or outItem.startswith("U+035") or outItem.startswith("U+036") or outItem.startswith("U+1D"):
                                                currentKey['topRight'] = chr(int("25CC", 16))
                                            if 'topRight' not in currentKey:
                                                currentKey['topRight'] = chr(int(outItem.strip().upper()[-4:], 16))
                                            else:
                                                currentKey['topRight'] = currentKey['topRight'] + chr(int(outItem.strip().upper()[-4:], 16))
                                    if (oldKey != u"") and (oldKey != currentKey['topRight']):
                                        print("These don't match:", combo['line'] )
                                #Bottom Right
                                if (currentFlags == flags5_RALT) or (currentFlags == flags6_NCAPS_RALT):
                                    oldKey = currentKey['bottomRight']
                                    currentKey['bottomRight'] = u""
                                    for outItem in combo['outputs']:
                                        if "U+" in outItem:
                                            if outItem.startswith("U+030") or outItem.startswith("U+031") or outItem.startswith("U+032") or outItem.startswith("U+033") or outItem.startswith("U+034") or outItem.startswith("U+035") or outItem.startswith("U+036") or outItem.startswith("U+1D"):
                                                currentKey['bottomRight'] = chr(int("25CC", 16))
                                            if 'bottomRight' not in currentKey:
                                                currentKey['bottomRight'] = chr(int(outItem.strip().upper()[-4:], 16))
                                            else:
                                                currentKey['bottomRight'] = currentKey['bottomRight'] + chr(int(outItem.strip().upper()[-4:], 16))
                                    if (oldKey != u"") and (oldKey != currentKey['bottomRight']):
                                        print("These don't match:", combo['line'] )
            if layout == "US102" and key["keyman"] == "K_oE2":
                verbose(0,"Skipping oE2 key")
            else:
                keyString = currentKey['topLeft'] + u"\n" + currentKey['bottomLeft'] + u"\n" + currentKey['topRight'] + u"\n" + currentKey['bottomRight'] + u"\n"
                rowList.append(keyString)
    return rowList

keyboardRepo = {}
filters = ["BEEP", "ANY(", "USE(", "NUL", "CONTEXT", "T_", "[Caps]"]
deadkeyNames = [['dk(003B)', "Cam Key"],['dk(0021)', "Cam Key"]]
UnicodeArchive = importUnicode()

filenameToParse = "sil_cameroon_qwerty.kmn"
keyboardRepo[filenameToParse] = keyboardDefinition(filenameToParse)
thisKeyboard =  keyboardRepo[filenameToParse]
parseKB(thisKeyboard, filenameToParse, True)
analyzeKB(thisKeyboard, filters, deadkeyNames)
#keyboardRepo[filenameToParse] = copy.deepcopy(thisKeyboard)
#printToJson(thisKeyboard)

filenameToParse = "fr-fr.klc.kmn"
keyboardRepo[filenameToParse] = keyboardDefinition(filenameToParse)
thisKeyboard =  keyboardRepo[filenameToParse]
parseKB(thisKeyboard, filenameToParse, True)
#printKMN(thisKeyboard, ['isCTRL'])
analyzeKB(thisKeyboard, filters, deadkeyNames)
#TODO Redirect print to thisKeyboard
#printToJson(thisKeyboard)


filenameToParse = "sil_cameroon_azerty.kmn"
thisKeyboard = keyboardDefinition(filenameToParse)
thisKeyboard.keymanComboList = []
parseKB(thisKeyboard, filenameToParse, True)
analyzeKB(thisKeyboard, filters, deadkeyNames)
keyboardRepo[filenameToParse] = thisKeyboard
#printToJson(thisKeyboard)

print("Finished")