#from http://travisaltman.com/password-dictionary-generator/

## TODO
# 

import subprocess
import sys
import getopt

def xselections(items, n):
    if n==0: 
        yield []
    else:
        for i in range(len(items)):
            for ss in xselections(items, n-1):
                yield [items[i]]+ss
            
def CrackGPG(inputfile,outputdecryptedfile,outputpassphrasefile):
    print("performing crack ")
    f=open(outputpassphrasefile, 'w')
    # for reference look here : http://www.asciitable.com
    # Numbers = 48 - 57
    # Capital = 65 - 90
    # Lower = 97 - 122
    majorchars = range(32,126)
    numb = range(48,58)
    cap = range(65,91)
    low = range(97,123)
    choice = 0
    while int(choice) not in range(1,9):
        choice = input('''
        1) Numbers
        2) Capital Letters
        3) Lowercase Letters
        4) Numbers + Capital Letters
        5) Numbers + Lowercase Letters
        6) Numbers + Capital Letters + Lowercase Letters
        7) Capital Letters + Lowercase Letters
        8) Major Chars from ascii(32) to ascii(126)
        : ''')

    choice = int(choice)
    poss = []
    if choice == 1:
        poss += numb
    elif choice == 2:
        poss += cap
    elif choice == 3:
        poss += low
    elif choice == 4:
        poss += numb
        poss += cap
    elif choice == 5:
        poss += numb
        poss += low
    elif choice == 6:
        poss += numb
        poss += cap
        poss += low
    elif choice == 7:
        poss += cap
        poss += low
    elif choice == 8:
        poss += majorchars



    bigList = []
    for i in poss:
        bigList.append(str(chr(i)))

    MIN = input("What is the min size of the word? ")
    MIN = int(MIN)
    MAX = input("What is the max size of the word? ")
    MAX = int(MAX)
    for i in range(MIN,MAX+1):
        for s in xselections(bigList,i):
            passphrase= ''.join(s) #join the list using '' as the joining char. so '^'.join(["a","b","c"]) => a^b^c
            cmdstring = "echo \"" + passphrase + "\" | gpg --passphrase-fd 0 -q --batch --allow-multiple-messages --no-tty --output " + outputdecryptedfile + " -d " + inputfile + ";"
            #output = subprocess.call(cmdstring,shell=True) 
            output = subprocess.Popen(cmdstring,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # check_output(cmdstring,shell=True,stderr=None)  
            #print(output)
            stderroutput=output.communicate()[1]  #must asave it off or it goes bubye
            stderroutput=stderroutput.decode('utf-8')

            if stderroutput!="gpg: decryption failed: Bad session key\n":
                f.write("stderroutput:\n"+stderroutput) #print(stderroutput)
                if (stderroutput=="gpg: handle plaintext failed: General error\ngpg: WARNING: message was not integrity protected\n"):
                    f.write("passphrase is:"+passphrase) 
                    print("The passphrase is -->"+passphrase+ "\n" + stderroutput)
                    f.close()
                    sys.exit(1) 
            exitcode=output.poll() #without calling poll or communicate the exit code will be 
            if exitcode==0:
                print("The passphrase is "+passphrase)
                exit
    f.close() #close the file if we don't find any passphrases...


### main 
decryptedfile = "/tmp/decrypted_file"
inputfile = "/path/to/input/file.gpg"
inputfile = "home/arch-nicky/BB/ConfigFiles/thinkbank.gpg"
#inputfile = "/home/arch-nicky/BB/bob.gpg"
inputfile = "home/arch-nicky/BB/ConfigFiles/testfile.gpg"
outputpassphrasefile ="crackedpassphrase.txt"

#could also just grab the filename and add .decrypted and .passphrase for the appropriate files
#print(len(sys.argv))
if len(sys.argv)==7:
    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'd:i:p:', ['--input=',
                                                                        '--outputdecryptedfile=',
                                                                        '--outputpassphrasefile=',
                                                                    ])
    except getopt.GetoptError as err:
        # print help information and exit:
        print( str(err)) # will print something like "option -a not recognized"
        #usage()
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-d', '--outputdecryptedfile'):
            outputdecryptedfile = arg
        elif opt in ('-i', '--input'):
            inputfile = arg
        elif opt in ('-p', '--outputpassphrasefile'):
            outputpassphrasefile = arg
        elif opt == '--version':
            version = arg

    print(inputfile,outputdecryptedfile,outputpassphrasefile)
    CrackGPG(inputfile,outputdecryptedfile,outputpassphrasefile)
else:
    print(" python program -d outpudecryptfile -p outputpassphrasefile -i inputgpgfiletocrack")
