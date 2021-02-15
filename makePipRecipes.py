#!/usr/bin/env python3.7
#
#            ########   ######     ##    ##  #######   ######  ########  #######                  
#            ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##           
#            ##     ## ##            ####   ##     ## ##          ##    ##     ##        
#            ########   ######        ##    ##     ## ##          ##    ##     ##       
#            ##   ##         ##       ##    ##     ## ##          ##    ##     ##      
#            ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##        
#            ##     ##  ######        ##     #######   ######     ##     #######         
#             ___          _   _      _     ___               _                 
#            | _ )  _  _  (_) | |  __| |   / __|  _  _   ___ | |_   ___   _ __  
#            | _ \ | || | | | | | / _` |   \__ \ | || | (_-< |  _| / -_) | '  \ 
#            |___/  \_,_| |_| |_| \__,_|   |___/  \_, | /__/  \__| \___| |_|_|_|
#                                                  |__/                             
#
#
# Robin Sebastian (https://github.com/robseb) 
#
# Contact: git@robseb.de
#
# Python Script to automatically create a Bitbake recipe for Python PiP Packages
# This recipe can then be used inside a meta layer for embedded Linux building with 
# the Yocto Project
#
# (2019-12-28) Vers.1.0 
#   first Version 
#
# (2020-05-23) Vers.1.1 
#  better interface
#
# (2021-02-15) Vers.1.2 
#  Allow to use packages with "-" in the name
#  Allow to use URLs as pip name to create recipes for on the 
#        build machine not supported packages 
# Information of the not supported ".whl" packages 
#
version = "1.2"

import os
import sys
import shutil
import hashlib, pathlib
import re

WORKING_FOLDER_NAME = "makePipRec_workingFolder"

#
# @brief Function to remove the working folder
# @return success 
#
def removeWorkingFolder():
    # Create a temp working directory 
    if(os.path.isdir(WORKING_FOLDER_NAME)):
        try:
            os.system('sudo rm -r '+os.getcwd()+'/'+WORKING_FOLDER_NAME)
        except PermissionError:
            print('\nERROR: Failed to delete the working Folder')
            print('Super user (root) privileges required to delate this folder!')
            print(' Please delete following folder by hand')
            print('"'+os.getcwd()+'/'+WORKING_FOLDER_NAME+'"') 
            print('and try it again')
            return False
        except Exception as ex:
            print('\nERROR: Failed to delete the working Folder')
            print(' Error Msg.: "'+str(ex)+'"')
            print(' Please delete following folder by hand')
            print('"'+os.getcwd()+'/'+WORKING_FOLDER_NAME+'"')
            print('and try it again')
            return False
    return True    

if __name__ == '__main__':
    
    print('\n##############################################################################')
    print('#                                                                            #')
    print('#    ########   ######     ##    ##  #######   ######  ########  #######     #')        
    print('#    ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##    #')          
    print('#    ##     ## ##            ####   ##     ## ##          ##    ##     ##    #')    
    print('#    ########   ######        ##    ##     ## ##          ##    ##     ##    #')   
    print('#    ##   ##         ##       ##    ##     ## ##          ##    ##     ##    #')  
    print('#    ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##    #')    
    print('#    ##     ##  ######        ##     #######   ######     ##     #######     #') 
    print('#                                                                            #')
    print("#            AUTOMATIC SCRIPT FOR GENERATING RECIPES TO INCLUDE              #")
    print("#           PYTHON PIP-PACKAGES TO YOUR YOCTO-PROJECT LINUX DISTO            #")
    print('#                                                                            #')
    print("#               by Robin Sebastian (https://github.com/robseb)               #")
    print("#                        Contact: git@robseb.de                              #")
    print("#                            Vers.: "+version+"                                      #")
    print('#                                                                            #')
    print('##############################################################################\n\n')

    # Runtime environment check
    if sys.version_info[0] < 3:
        print("Use Python 3 for this script!")
        sys.exit()

    if not sys.platform =='linux':
        print("This Script can only run on Linux!")
        sys.exit()
    ############################################ READ USER INPUT (PiP Name and Version) ###########################################
    
    print('Type in the Name of the Python pip (PyPI) Package to include to your Yocto Project Linux Distro')
    print('Note: Consider the exact writing! Case sensitive!')
    print('You can find Python pip packages here: https://pypi.org/')
    PipName =input('PiP-Package Name: ')
    Pipurl = PipName

    if PipName=='q' or PipName=='Q': sys.exit()
    if PipName.endswith('.whl'):
        print('ERROR: Download URLs with ".whl" archive files are not supported!')
        print('       It is only enabled to download ".tar.gz"- and ".zip" source code files!')
        sys.exit()
    elif (PipName.endswith('.tar.gz') or PipName.endswith('.zip')) and PipName.find('http')!=-1:
        # A HTTP/HTTPS URL was used
        print('\nYou inserted a URL to a Python pip (PyPi) package ')
        print('Insert the regular pip(PyPI) Package name:')
        print('Note: Consider the exact writing! Case sensitive!')
        PipName =input('PiP-Package Name: ')
        if PipName=='q' or PipName=='Q': sys.exit()
        if (PipName.endswith('.whl') or PipName.endswith('.zip')) and PipName.find('http'):
            print('ERROR: Insert the regular Python pip name not a URL (e.g. "django")')
            sys.exit()

    selectedPythonVersion = 0
    print("Choose the requiered Python Version:")
    print("  Python 1-2: 1,2 ")
    print("  Python 3  : 3   ")

    while(True):
        temp = input("Python Version:")
        if temp=='q' or temp=='Q': sys.exit()

        try:
            selectedPythonVersion = int(temp)
        except ValueError:
            print('Your Input is not valid! Please choose a Number between 1 and 3!')
            continue

        if(selectedPythonVersion>=1 and selectedPythonVersion<=3):
            break
        else:
            print('Your Input is not valid! Please choose a Number between 1 and 3!')

    print("Type in the used License name for the recipe (e.g.: MIT)")
    licensenName = input('License name: ')

    if licensenName=='\r' or licensenName=='\n\r'or licensenName=='': licensenName='MIT'
    if PipName=='q' or PipName=='Q': sys.exit()
    print('Chosen License name: "'+licensenName+'"')
    print('Starting the generation...\n')

    ################################################ Download the PiP File ###########################################

    # Remove the old temp working directory and create a new one 
    if not removeWorkingFolder():
        sys.exit()
    os.mkdir(WORKING_FOLDER_NAME)

    # Download for testing the pip package
    print('--> Download for testing the Python PiP package')

    os.system('pip3 download --no-deps --no-binary :all: --only-binary none  -d '+WORKING_FOLDER_NAME+'/ '+Pipurl)
    


    # Reading the downloaded files and detect the file type
    targzFiles = [f for f in os.listdir(os.getcwd()+'/'+WORKING_FOLDER_NAME) if f.endswith('.tar.gz')]
    zipFiles   = [f for f in os.listdir(os.getcwd()+'/'+WORKING_FOLDER_NAME) if f.endswith('.zip')]

    detectedFiletype = 0 # 1= .tar.gz-File | 2= .zip-File
    filename = ''

    # Check if the download was successfully
    if(len(targzFiles) ==1): 
        detectedFiletype = 1
        filename = targzFiles[0]
    elif(len(zipFiles) ==1): 
        detectedFiletype = 2
        filename = zipFiles[0]
    else:
        print('\n##############################################################################')
        print('#       ERROR: Failed to download the chosen Python pip (PyPi) package!      #')
        print('#                                                                            #')
        print('#      Please read the error report of the executed "pip" command above!     #')
        print('#                                                                            #')
        print('# You can use the direct download URL (with ".tar.gz"- or ".zip"- suffix)    #')
        print('#   as pip package name                                                      #')
        print('#                                                                            #')
        print('# Note: It is only enabled incase the universal source code is available     #')
        print('#       as ".tar.gz" or ".zip" archive file (".whl"-files are not supported) #')
        print('#                                                                            #')
        print('##############################################################################\n')
        sys.exit()

    print('\n   The Name of the downloaded file: \"'+filename+'\"')

    ############################################# Calculate checksums for the file ########################################

    print('--> Calculate md5 checksum of this file')
    md5sum=hashlib.md5(pathlib.Path(os.getcwd()+'/'+WORKING_FOLDER_NAME+'/'+filename).read_bytes()).hexdigest()
    print('    md5sum = '+str(md5sum))

    print('--> Calculate sha256sum checksum of this file')
    sha256sum=hashlib.sha256(pathlib.Path(os.getcwd()+'/'+WORKING_FOLDER_NAME+'/'+filename).read_bytes()).hexdigest()
    print('    sha256sum = '+str(sha256sum))

    ######################################### Read the Version Code for this package ######################################
    print('--> Decode the current Version Code of this PiP Package')

    # PIP File name syntax: <PiP Name>-<Version No.>.<File Suffix>

    decodingversionFailed = False

    pipNamepos = filename.find(PipName)
    if pipNamepos ==-1:
        # try to replace "-" with "_"
        PipName = PipName.replace('-','_')
        pipNamepos = filename.find(PipName)
        
    if (pipNamepos >-1):
        # Find the position of the File Suffix
        if(detectedFiletype == 1 ):
            PipSufixPos = filename.find('.tar.gz')
        else: 
            PipSufixPos = filename.find('.zip')

        if(PipSufixPos >-1 ):
            PiPversionStr = filename[pipNamepos+len(PipName+'-'):PipSufixPos]
            fileFolderName = filename[:PipSufixPos]
            print('    Version: '+PiPversionStr)
        else:
            decodingversionFailed = True
    else:
        decodingversionFailed = True

    # In case of Version string encoding trigger an error message
    if decodingversionFailed:
        print('--> ERROR: Decoding downloaded file failed!')
        print('    The file name must be in following syntax:')
        print('    <PiP Name>-<Version No.>.<File Suffix>')
        sys.exit()

  
    ############################## Read in the Licence File inside the downloaded file ###################################
    print('--> Unpackage the downloaded file to decode the included licence file')

    ####### Insert the compressed rootfs to the rootfs folder
    print('    Unpackage the downloaded package')

    if(detectedFiletype == 1 ):
        os.system('sudo tar -xzpf '+WORKING_FOLDER_NAME+'/'+filename+' -C '+WORKING_FOLDER_NAME)
    else:
        os.system('unzip '+'WORKING_FOLDER_NAME/'+filename+' -d '+WORKING_FOLDER_NAME)

    # Check if the unpacking was successful
    if(os.path.isdir(WORKING_FOLDER_NAME+'/'+fileFolderName)):
        print('     Unpackaging was successful')
    else:
        print('ERROR: The unpacking of the downloaded file failed!')
        sys.exit()

    ####### Try to find the Licence file
    print('    Try to find a Licence file')
    noSufFiles = [f for f in os.listdir(os.getcwd()+'/'+WORKING_FOLDER_NAME+'/'+fileFolderName) if f.endswith('')]
    LicenseFileFoundingError = False

    LicenseFileType =0 # 1: LICENSE.txt | 2: LICENSE | 3: any other file (see LicenseFileName)
    LicenseFileName=''

    if(len(noSufFiles) >-1): 
        while(True):
            LicenseFileType = LicenseFileType +1 
            LicenseFileFoundingError =False
            # Search for the LICENCE File
            try:
                if(LicenseFileType==1):
                    LicenseFilePos =noSufFiles.index('LICENSE.txt')
                    LicenseFileName = 'LICENSE.txt'
                elif (LicenseFileType==2):
                    LicenseFilePos =noSufFiles.index('LICENSE')
                    LicenseFileName = 'LICENSE'
            except ValueError:
                LicenseFileFoundingError =True
      
            if(not LicenseFileFoundingError):
                if(LicenseFilePos >-1):
                    print('    The License File was found')
                    break
                else:
                    LicenseFileFoundingError = True

            if LicenseFileType == 2:
                # Use any other file as LICENSE-File
                print('NOTE: The LICENSE-File was not found inside the PiP-Package!')
                for it in noSufFiles: 
                    if(os.path.isfile(os.getcwd()+'/'+WORKING_FOLDER_NAME+'/'+fileFolderName+'/'+it)):
                        LicenseFileName  = it

                if(LicenseFileName ==""):
                    LicenseFileFoundingError = True
                else:
                    print('     To avoid this problem the File:\"'+LicenseFileName +'\" will be used instead')
                    LicenseFileType =3
                    LicenseFileFoundingError = False
                break
            # Try to find the LICENSE without a suffix (type =2)
    else:
        LicenseFileFoundingError = True
    
    if LicenseFileFoundingError:
        print('ERROR: No LICENSE.txt or LICENSE file inside this PiP-Package found!')
        sys.exit()

    ####### Calculate the md5sum for LICENSE.txt
    print('--> Calculate the md5-checksum for the License file')

    LicenseMd5sum=hashlib.md5(pathlib.Path(os.getcwd()+'/'+WORKING_FOLDER_NAME+'/'+fileFolderName+'/'+LicenseFileName).read_bytes()).hexdigest()
    print('    md5sum = '+str(LicenseMd5sum))

    ##########
    # At this point the user input is valide and checked 

    ############################## Giving the .bb  ###################################

    # Yocto allows only lower case numbers without numbers and others caractors

    # Check if there are only lower cases in the chosen PiP-name
    tempName=''
    for c in PipName:
        if not c.islower():
            # if not set character low
            c = c.lower()
        tempName=tempName+c
    RecipieFileName = tempName
    
    # Check if any not allowed characters are in this string and remove them
    pos =0
    tempName=''
    for c in RecipieFileName:
        if not re.match('^[0-9]*$', c): 
            tempName=tempName+c
    
    RecipieFileName = tempName 

    ############################################################################################################
    #                                                                                                          #
    #   Collected Variables for Building a recipes for embedding Python PiP-packages to the Yocto Project      #
    #                                                                                                          #
    #   PipName                       ->  PiP Package name                                                     # 
    #   selectedPythonVersion         ->  required Python Version (1,2,3)                                      #
    #   licensenName                  ->  License Type Name (e.g. MIT)                                         #     
    #   md5sum                        ->  PiP Package md5 checksum                                             #                 
    #   sha256sum                     ->  PiP Package sha256 checksum                                          # 
    #   PiPversionStr                 ->  piP Package Version String                                           #      
    #   LicenseFileName               ->  the file name of License File                                        #
    #   LicenseMd5sum                 ->  md5 checksum of the License file                                     #
    #   RecipieFileName               ->  name of the two recipe files (without suffix)                        # 
    #                                                                                                          #     
    #                                                                                                          #                         
    #                                                                                                          #         
    ############################################################################################################ 


    ############################## Create the .bb-Bitbake file ###################################

    #### Create a new blank .bb-file
    # File syntax: pip-<PiP Name>_<Version No>.<File Sufix>
    bbfilename = 'pip-'+RecipieFileName+'_'+PiPversionStr+'.bb'
    inheritPiPstr = '','inherit pypi setuptools','inherit pypi setuptools','inherit pypi setuptools3'
    print('--> Create the Bitbake .bb-File with the name')
    print('      '+bbfilename)

    if(os.path.isfile(bbfilename)):
        os.remove(bbfilename)
    
    try:
        fp = open(bbfilename)
    except IOError:
        # If not exists, create the file
        fp = open(bbfilename, 'w+')
    
    ########### Generate the conntet of the .bb-file
    bbFileContent = '# The is automatic generated Code by "makePipRecipes.py"\n' \
        '# (build by Robin Sebastian (https://github.com/robseb) (git@robseb.de) Vers.: '+version+') \n' \
        '\n' \
        'SUMMARY = "Recipie to embedded the Python PiP Package '+PipName+'"\n' \
        'HOMEPAGE ="https://pypi.org/project/'+PipName+'"\n' \
        'LICENSE = "'+licensenName+'"\n' \
        'LIC_FILES_CHKSUM = "file://'+LicenseFileName+';md5='+LicenseMd5sum+'"\n' \
        '\n' \
        +inheritPiPstr[selectedPythonVersion]+'\n' \
        'PYPI_PACKAGE = "'+PipName+'"\n' \
        'SRC_URI[md5sum] = "'+md5sum+'"\n' \
        'SRC_URI[sha256sum] = "'+sha256sum+'"\n'

    print('--> Generate the content of this file')
    with open(bbfilename, "a") as f:   
        f.write(bbFileContent)    
    
    # Download for test the pip package
    print('     Bitbake file generation was successfull')


############################ Remove the Working Folder ################################
    print('--> Deleting the working Folder')
    removeWorkingFolder()

############################## Implementation Guide ###################################
print('\n################################################################################')
print('#                                                                              #')
print('#                          GENERATION WAS SUCCESSFUL                           #')
print('#                                                                              #')
print('#---------------------------- Implementation Guide ----------------------------#')
print('# 1. Step: Copy the recipe file: \"'+bbfilename+'\"                            ')
print('#          to your recipe folder inside a meta layer                           ')
print('#          For example here:                                                   ')
print('#          meta-example                                                        ')
print('#          |- conf                                                             ')
print('#          |- recipes-test                                                     ')
print('#             |- test                                                          ')
print('#                |- '+bbfilename+' <--\n                                       ')
print('#          (this file is located here:'+os.getcwd()+' )          ')
print('# 2. Step: Include the PiP-Package to your Yocto Project by                    ')
print('#          by adding following line to the conf/local.conf file:               ')
print('#            conf/local.conf:                                                  ')
print('#             IMAGE_INSTALL_append = "pip-'+RecipieFileName+'"\n               ')
print('# 3. Step: Build your Yocto Project normanly with bitbake\n                    ')
print('#------------------------------------------------------------------------------#')
print('#                                                                              #')
print('#                           SUPPORT THE AUTHOR                                 #')
print('#                                                                              #')
print('#                            ROBIN SEBASTIAN                                   #')
print('#                     (https://github.com/robseb/)                             #')
print('#                             git@robseb.de                                    #')
print('#                                                                              #')
print('#    makePipRecipes and rsYocto are projects, that I have fully                #')
print('#        developed on my own. No companies are involved in this projects.      #')
print('#       I am recently graduated as Master of Since of electronic engineering   #')
print('#            Please support me for further development                         #')
print('#                                                                              #')
print('################################################################################')
# EOF