import re
import time

# gamelog = r"C:\Users\gummy\Downloads\MoMReborn\MoMReborn\logs\game.txt" # new client
gamelog = r"C:\MoMReborn\logs\game.txt" # old client
damageraw = "damagecopy.txt"
output = "output.txt"

def getLastLine():
    initialGameLog = open(gamelog)
    lastLine = initialGameLog.readlines()[-2]
    initialGameLog.close()
    return lastLine

def getDamageTxt(startLine): # writes the content from game.txt into a new text file
    with open(gamelog) as infile, open(damageraw, "w") as outfile:
        copy = False
        for line in infile:
            if copy:
                outfile.write(line)
            elif line == startLine:
                copy = True
        infile.close()
        outfile.close() # damageraw should now contain all game text sent while program was sleeping

def calc(pname = "X"): # reads content from damagecopy.txt and outputs a dict with (first word of) name as key, then the total damage and array of all damages dealt
    dmgdict = {}

    with open(damageraw, "r") as input:
        for line in input:
            damage = ""
            lineArr = re.split("for | damage!", line)
            try:
                damage = lineArr[1]
            except IndexError:
                None

            try:
                damage = int(damage)
            except ValueError:
                None

            if isinstance(damage, int): # If the line seems compatible, add to dmgdict. Might not be perfect
                name = lineArr[0].split(" ")[2] # more like first word of name, but it's good enough for now
                if pname == "X" or pname == name:
                    if name in dmgdict:
                        dmgdict[name][0] += damage
                        dmgdict[name][1].append(damage)
                    else:
                        dmgdict[name] = [damage, [damage]]
    
    return dmgdict

    

def main():
    start = input("Enter \"s\" to start: ")

    if (start == "s"):
        firstLine = getLastLine()
        t1 = time.time()
        input("Enter anything to end ")
        
        fakeLastLine = getLastLine()

        while (True): # let logs update one more time
            if (getLastLine() != fakeLastLine):
                break

        runtime = time.time() - t1
        getDamageTxt(firstLine)
        
        dmgdict = calc()


        with open(output, "a") as finalOut:
            for name in dmgdict:
                w = f"{name:12}{dmgdict[name][0]:10}{len(dmgdict[name][1]):10}{float(int(runtime*100))/100:10}{int(dmgdict[name][0]/runtime):10}{int(dmgdict[name][0]/runtime * 60):10}\n\n"
                finalOut.write(w)
                # finalOut.write(name + "\t")
                # finalOut.write(str(dmgdict[name][0]) + "\t")
                # finalOut.write(str(len(dmgdict[name][1])) + "\t")
                # finalOut.write(str(int(runtime)) + "\t")
                # finalOut.write(str(int(dmgdict[name][0]/runtime)) + "\t")
                # finalOut.write(str(int(dmgdict[name][0]/runtime * 60)))
                # finalOut.write("\n\n")
            finalOut.close()

main()