# PiP2Bitbake
![GitHub](https://img.shields.io/static/v1?label=Ubuntu&message=18.04+LTS,+20.04+LTS&color=yellowgreen)
![GitHub](https://img.shields.io/static/v1?label=CentOS&message=7.0,+8.0&color=blue)
![GitHub](https://img.shields.io/static/v1?label=Python&message=3.7&color=green)
![GitHub](https://img.shields.io/github/license/robseb/PiP2Bitbake)

![Alt text](doc/concept.png?raw=true "Concept")
___
**This Python script allows to pre-install any Python** *pip* (*PyPI*) (*Python Package Index*)- **Packages within a final *Yocto Project* Linux Image.** 

In order to make this possible a Bitbake-file with all necessary information's (Version Number, Checksums,..) will be generated
to allow Bitbake to include the chosen pip-package to the *rootfs* of the generated Yocto-Project Linux Distribution. 

I developed this Python script to create [*rsYocto*](https://github.com/robseb/rsyocto) an embedded Linux for *Intel SoC-FPGAs*. 

## Features

* **Python script to automatically create Bitbake recipe files for the Yocto Project to pre-install any Python *pip* package**
* **Almost every Python pip package can implemented into a custom Linux Distribution**
    * Of cause, it is only necessary that the package is as a cross Platform version available 
* **Outputs a *".bb"*-Bitbake recipe file that can easily included to any Yocto Project *meta-layer***
* **Supported *Python Package Index Version***: 1-3
* **Supported Python pip package archive file types:** "*.tar.gz*" and "*.zip*"
* **It is enabled to use URL/Link to a specific Python package version or to a custom Server**


# Guide to use this script
1.  Pull this repository to your Yocto Project building machine
2.  Be sure that **Python pip 3** is installed on your development machine 
    * To install that use on **Ubuntu**:
         ```bash
         sudo apt-get -y install python-pip
        ````
    * To install that use on **CentOS**:
         ```bash
         sudo yum install python-pip
        ````
3. Start the python script
    ```bash
     python3 makePipRecipes.py
    ````
4. **Find a Python [PyPI](https://pypi.org/)-package to include to the Yocto Project**
5. **Follow the instruction of the Python script**
    * The script will ask for:
        1. The **pip-package** name (e.g. by `pip install pyserial` use "`pyserial`")
            * Be sure that the uppercase/lowercase of the string is exact (**Case sensitive!**)
            * **Alternatively here it is enabled to insert a URL/Link to the package**
                * Use the entire Link with the "*http*"- or "*https*"- pre-fix and with the file suffix
                * You can find the URLs to the package inside the *"Download files"* selection of the [PyPI](https://pypi.org/) package website
                * For instance "*pyserial*" it would be: "*https://files.pythonhosted.org/packages/1e/7d/ae3f0a63f41e4d2f6cb66a5b57197850f919f59e558159a4dd3a818f5082/pyserial-3.5.tar.gz*"
                * **Note:** "*.whl*" archive packages are not supported! 

        2. For the required **Python-Version**
        3. For the **Type of Licence** (e.g. MIT) for recipe
7. **The Python script will generate a *".bb"*-Bitbake-file**
    * **Copy** this file to your recipe folder
    * If you don't have a *meta-layer* create a new one
        * Execute following command inside your Yocto Project build Folder (`poky/build`)
            ```bash 
            bitbake-layers create-layer meta-example
            ````
        * Include the new layer to your Yocto Project by **adding following line** to the `poky/build/conf/bblayers.conf`-file:
            ````txt 
            /home/<user name>/poky/meta-example \
            ````
     * **Copy** the generated recipe file to your recipes:
       ```txt 
          meta-example
          |- conf
          | - README
          |- recipes-test
             |- test
                |-GENERATED_BITBAKAE_FILE.bb
       ```
8. **Include the Python pip package to your Yocto Build by adding following line to the `poky/build/conf/local.conf`-file**
    ```txt 
    IMAGE_INSTALL_append = "pip-PIPNAME"
    ````
9. **To execute the implementation start the building process of the Yocto Project normally**
   * For example with (*inside `poky/build`*): 
      ```bash 
      bitbake core-image-minimal
      ````
      
## Example: Embedding the Python pip-package `pyserial` to the Yocto Project

<details>
<summary><strong>Example output after an execution</strong></summary>
<a name="step5"></a>

````txt  
vm@ubuntu:$ python3 makePipRecipes.py 
#############################################################################
#                                                                            #
#    ########   ######     ##    ##  #######   ######  ########  #######     #
#    ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##    #
#    ##     ## ##            ####   ##     ## ##          ##    ##     ##    #
#    ########   ######        ##    ##     ## ##          ##    ##     ##    #
#    ##   ##         ##       ##    ##     ## ##          ##    ##     ##    #
#    ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##    #
#    ##     ##  ######        ##     #######   ######     ##     #######     #
#                                                                            #
#            AUTOMATIC SCRIPT FOR GENERATING RECIPES TO INCLUDE              #
#           PYTHON PIP-PACKAGES TO YOUR YOCTO-PROJECT LINUX DISTO            #
#                                                                            #
#               by Robin Sebastian (https://github.com/robseb)               #
#                        Contact: git@robseb.de                              #
#                            Vers.: 1.2                                      #
#                                                                            #
##############################################################################


Type in the Name of the Python pip (PyPI) Package to include to your Yocto Project Linux Distro
Note: Consider the exact writing! Case sensitive!
You can find Python pip packages here: https://pypi.org/
PiP-Package Name: pyserial
Choose the requiered Python Version:
Python 1-2: 1,2 
Python 3  : 3   
Python Version:3
Type in the used License name for the recipe (e.g.: MIT)
License name: 
Chosen License name: "MIT"
Starting the generation...

--> Download for testing the Python PiP package
Collecting pyserial
Downloading https://files.pythonhosted.org/packages/1e/7d/ae3f0a63f41e4d2f6cb66a5b57197850f919f59e558159a4dd3a818f5082/pyserial-3.5.tar.gz (159kB)
    100% |████████████████████████████████| 163kB 1.1MB/s 
Saved ./makePipRec_workingFolder/pyserial-3.5.tar.gz
Successfully downloaded pyserial

The Name of the downloaded file: "pyserial-3.5.tar.gz"
--> Calculate md5 checksum of this file
    md5sum = 1cf25a76da59b530dbfc2cf99392dc83
--> Calculate sha256sum checksum of this file
    sha256sum = 3c77e014170dfffbd816e6ffc205e9842efb10be9f58ec16d3e8675b4925cddb
--> Decode the current Version Code of this PiP Package
    Version: 3.5
--> Unpackage the downloaded file to decode the included licence file
    Unpackage the downloaded package
[sudo] password for vm: 
    Unpackaging was successful
    Try to find a Licence file
    The License File was found
--> Calculate the md5-checksum for the License file
    md5sum = 520e45e59fc2cf94aa53850f46b86436
--> Create the Bitbake .bb-File with the name
    pip-pyserial_3.5.bb
--> Generate the content of this file
    Bitbake file generation was successfull
--> Deleting the working Folder

################################################################################
#                                                                              #
#                          GENERATION WAS SUCCESSFUL                           #
#                                                                              #
#---------------------------- Implementation Guide ----------------------------#
# 1. Step: Copy the recipe file: "pip-pyserial_3.5.bb"                            
#          to your recipe folder inside a meta layer                           
#          For example here:                                                   
#          meta-example                                                        
#          |- conf                                                             
#          |- recipes-test                                                     
#             |- test                                                          
#                |- pip-pyserial_3.5.bb <--
                                    
#          (this file is located here:/home/vm/Desktop/PiP2Bitbake )          
# 2. Step: Include the PiP-Package to your Yocto Project by                    
#          by adding following line to the conf/local.conf file:               
#            conf/local.conf:                                                  
#             IMAGE_INSTALL_append = "pip-pyserial"
            
# 3. Step: Build your Yocto Project normanly with bitbake
                    
#------------------------------------------------------------------------------#
#                                                                              #
#                           SUPPORT THE AUTHOR                                 #
#                                                                              #
#                            ROBIN SEBASTIAN                                   #
#                     (https://github.com/robseb/)                             #
#                             git@robseb.de                                    #
#                                                                              #
#    makePipRecipes and rsYocto are projects, that I have fully                #
#        developed on my own. No companies are involved in this projects.      #
#       I am recently graduated as Master of Since of electronic engineering   #
#            Please support me for further development                         #
#                                                                              #
################################################################################
````

### Content of the generated file: `pip-pyserial_3.4.bb`
````bitbake  
# The is a automatic generated Code by "makePipRecipes.py"
# (by Robin Sebastian (https://github.com/robseb) Vers.: 1.0) 

SUMMARY = "Recipie to embedded the Python PiP Package pyserial"
HOMEPAGE ="https://pypi.org/project/pyserial"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=d476d94926db6e0008a5b3860d1f5c0d"

inherit pypi setuptools
PYPI_PACKAGE = "pyserial"
SRC_URI[md5sum] = "ed6183b15519a0ae96675e9c3330c69b"
SRC_URI[sha256sum] = "6e2d401fdee0eab996cf734e67773a0143b932772ca8b42451440cfed942c627"
````
</details>

### Finally on the running Yocto-Project Linux Distribution ....
````bash
root@cyclone5:~# pip list
Package    Version
---------- -------
pyserial   3.4.0
````
### is `pyserial`pre-installed 
<br>

   
* *rsyocto*; **Robin Sebastian,M.Sc. [(LinkedIn)](https://www.linkedin.com/in/robin-sebastian-a5080220a)**

*Pip2BitBake* and *rsyocto* are self-developed projects in which no other companies are involved. 
It is specifically designed to serve students and the Linux/FPGA open-source community with its publication on GitHub and its open-source MIT license. 
In the future, *rsyocto* will retain its open-source status and it will be further developed. 

Due to the enthusiasm of commercial users, special features for industrial, scientific and automotive applications 
were developed and ready for the implementation in a highly optimazed closed commercial version. 
Partnerships as an embedded SoC-FPGA design service to fulfil these specific commercial requirements are offered. 
It should help, besides students with the *rsyocto* open-source version, commercial users, as well.   

**For commercial users, please visit the *rsyocto* embedded service provider website:** 
[**rsyocto.com**](https://rsyocto.com/)

[![GitHub stars](https://img.shields.io/github/stars/robseb/PiP2Bitbake?style=social)](https://GitHub.com/robseb/PiP2Bitbake/stargazers/)
[![GitHub watchers](https://img.shields.io/github/watchers/robseb/PiP2Bitbake?style=social)](https://github.com/robseb/NIOSII_EclipseCompProject/watchers)
[![GitHub followers](https://img.shields.io/github/followers/robseb?style=social)](https://github.com/robseb)

