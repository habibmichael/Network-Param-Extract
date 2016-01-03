import MySQLdb as mdb
import paramiko
import threading
import os.path
import subprocess
import datetime
import time
import sys
import se

#Coloring Module
from colorama import init,deinit,Fore,Style


#Initialize colorama
init()

#Checking number of arguments passed into the script
if len(sys.argv)==4:
	ip_file=sys.argv[1]
	user_file=sys.argv[2]
	sql_file=sys.argv[3]


	#Print in colored format
 	print Fore.BLUE + Style.BRIGHT + "\n\n* The script will be executed using files:\n"
    print Fore.BLUE + "Network IP file is: " + Fore.YELLOW + "%s" % ip_file
    print Fore.BLUE + "SSHv2 connection file is: " + Fore.YELLOW + "%s" % user_file
    print Fore.BLUE + "MySQL connection file is: " + Fore.YELLOW + "%s" % sql_file
    print Fore.BLUE + Style.BRIGHT + "\n"
    
else:
    print Fore.RED + Style.BRIGHT + "\nIncorrect number of arguments (files) passed into the script."
    print Fore.RED + "Please try again.\n"
    sys.exit()

def ip_is_valid():
    check = False
    global ip_list
	
    while True:
        #Changing exception message
        try:
            #Open user selected file for reading (IP addresses file)
            selected_ip_file = open(ip_file, 'r')
            
            #Starting from the beginning of the file
            selected_ip_file.seek(0)
            
            #Reading each line (IP address) in the file
            ip_list = selected_ip_file.readlines()
            
            #Closing the file
            selected_ip_file.close()
            
        except IOError:
            print Fore.RED + "\n* File %s does not exist! Please check and try again!\n" % ip_file
            sys.exit()
            
        #Checking octets            
        for ip in ip_list:
            octet_check = ip.split('.')
            
            if (len(octet_check) == 4) and (1 <= int(octet_check[0]) <= 223) and (int(octet_check[0]) != 127) and (int(octet_check[0]) != 169 or int(octet_check[1]) != 254) and (0 <= int(octet_check[1]) <= 255 and 0 <= int(octet_check[2]) <= 255 and 0 <= int(octet_check[3]) <= 255):
                check = True
                break
                 
            else:
                print '\n* There was an INVALID IP address! Please check and try again!\n'
                check = False
                continue
        
		#Evaluating the 'check' flag    
        if check == False:
            sys.exit()
        
        elif check == True:
            break
       #Checking IP reachability
    print "* Checking IP reachability... Please wait...\n"
    
    check2 = False
	
    while True:
        for ip in ip_list:
            ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', ip], stdout = subprocess.PIPE)
            
	    if ping_reply == 0:
                check2 = True
                continue
				
            elif ping_reply == 2:
                print Fore.RED + "\n* No response from device %s." % ip
                check2 = False
                break
				
            else:
                print Fore.RED + "\n* Ping to the following device has FAILED:", ip
                check2 = False
                break
				
        #Evaluating the 'check' flag 
        if check2 == False:
            print Fore.RED + "* Please re-check IP address list or device.\n"
            sys.exit()
			
        elif check2 == True:
            print '\n* All devices are reachable. Checking SSHv2 connection file...\n'
            break

#Checking user file validity
def user_is_valid():
    global user_file
	
    while True:
        #Changing output messages
        if os.path.isfile(user_file) == True:
            print "\n* SSHv2 connection file has been validated. Checking MySQL connection file...\n"
            break
			
        else:
            print Fore.RED + "\n* File %s does not exist! Please check and try again!\n" % user_file
            sys.exit()
            
#Checking SQL connection command file validity
def sql_is_valid():
    global sql_file
	
    while True:
        #Changing output messages
        if os.path.isfile(sql_file) == True:
            print "\n* MySQL connection file has been validated...\n"
            print "\n* Any MySQL errors will be logged to: " + Fore.YELLOW + "SQL_Error_Log.txt\n" + Fore.BLUE
            print "\n* Reading network data and writing to MySQL...\n"
            break
			
        else:
            print Fore.RED + "\n* File %s does not exist! Please check and try again!\n" % sql_file
            sys.exit()

#Change exception message
try:
    #Calling IP validity function    
    ip_is_valid()
    
except KeyboardInterrupt:
    print Fore.RED + "\n\n* Program aborted by user. Exiting...\n"
    sys.exit()

#Change exception message
try:
    #Calling user file validity function    
    user_is_valid()
    
except KeyboardInterrupt:
    print Fore.RED + "\n\n* Program aborted by user. Exiting...\n"
    sys.exit()
    
#Change exception message
try:
    #Calling MySQL file validity function
    sql_is_valid()
    
except KeyboardInterrupt:
    print Fore.RED + "\n\n* Program aborted by user. Exiting...\n"
    sys.exit()
 
