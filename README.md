# PiP2Bitbake
**With this python script it is possible to pre-install Python pip (PyPI)- Packages within a final Yocto Project Linux Image.** 
In order to make this possible it will generate a Bitbake-file with all necessary informations (Version Number, Checksums,..)
to allow Bitbake to include the selected pip-package to the rootfs of the generated Linux system. 
This script support all current pip- and python-versions.

I developed this script to create [*rsYocto*](https://github.com/robseb/rsyocto) a embbeded Linux for Intel SoC-FPGAs. 

# Guide to use this script
1.  Pull this repository to your Yocto Project building machine
2.  Be sure that Python pip are installed 
    * To install that use on Ubuntu:
         ```bash
         sudo apt-get install python-pip
        ````
3. Start the python script
    ```bash
     python3 makePipRecipes.py
    ````
4. Find a Python [PyPI](https://pypi.org/)-package to include
5. Follow the instruction
    * The Script will ask for:
        1. The **pip-package** name (e.g. by `pip install pyserial` use `pyserial`)
            * Be sure that the uppercase lowercase of the string is exact
        2. For the required **Python-Version**
        3. For the **Type of Licence** (e.g. MIT) for recipe
7. The Python script will generate a *.bb-Bitbake*-file
    * Copy this file to your recipe folder
    * If you don't have a meta-layer create a new one
        * Execute following command inside your Yocto Project build Folder (`poky/build`)
            ```bash 
            bitbake-layers create-layer meta-example
            ````
        * Include the new layer to your Yocto Project by adding following line to the `poky/build/conf/bblayers.conf`-file:
            ````txt 
            /home/<user name>/poky/meta-example \
            ````
     * Copy the generated recipe file to your recipies:
       ```txt 
          meta-example
          |- conf
          | - README
          |- recipes-test
             |- test
                |-GENERATED_BITBAKAE_FILE.bb
       ```
8. Include the Python pip-package to your Yocto Build by edding following line to the `poky/build/conf/local.conf`-file
    ```txt 
    IMAGE_INSTALL_append = "pip-PIPNAME"
    ````
9. To Execute the implementation start the building process of the Yocto Project normally
   * For example with (inside `poky/build`): 
      ```bash 
      bitbake core-image-minimal
      ````
      
## Example: Embedding the Python pip-package `pyserial` to the Yocto Project

### Script Output
````txt  
      vm@ubuntu:$ python3 makePipRecipes.py 
          AUTOMATIC SCRIPT FOR GENERATING RECIPIES TO INCLUDE
          PYTHON PIP-PACKAGES TO YOUR YOCTO PROJECT 
           by Robin Sebastian (https://github.com/robseb) Vers.: 1.0

          Please type in the Name of the PiP-Package to include
          Note: Consider the exact writing! Case sensitive!
          PiP-Package Name: pyserial
          Choose the requiered Python Version:
            Python 1-2: 1,2 
            Python 3  : 3   
          Python Version:1
          Type in the used License name for the recipie (e.g.: MIT)
          License name: MIT
          Starting the generation...

          --> Downloading for test the Python PiP package
          Collecting pyserial
            Using cached https://files.pythonhosted.org/packages/cc/74/11b04703ec416717b247d789103277269d567db575d2fd88f25d9767fe3d/pyserial-3.4.tar.gz
            Saved ./mkaePiP_workingFolder/pyserial-3.4.tar.gz
          Successfully downloaded pyserial

             The Name of the downloaded file: "pyserial-3.4.tar.gz"
          --> Calculate md5 checksum of this file
              md5sum = ed6183b15519a0ae96675e9c3330c69b
          --> Calculate sha256sum checksum of this file
              sha256sum = 6e2d401fdee0eab996cf734e67773a0143b932772ca8b42451440cfed942c627
          --> Decode the current Version Code of this PiP Package
              Version: 3.4
          --> Unpackage the downloaded file to decode the included licence file
              Unpackage the downloaded package
          [sudo] password for vm: 
               Unpackaging was succsesfull
              Try to find a Licence file
              The License File was found
          --> Calculate the md5-checksum for the License file
              md5sum = d476d94926db6e0008a5b3860d1f5c0d
          --> Create the Bitbake .bb-File with the name
                pip-pyserial_3.4.bb
          --> Generate the content of this file
               Bitbake file generation was sucsessfull

          ---------------------------- Implementation Guide ----------------------------
           1. Step: Copy the recipie file: "pip-pyserial_3.4.bb"
                    to your recipie folder inside a meta layer
                    For example here:
                    meta-example
                    |- conf
                    |- recipes-test
                       |- test
                          |- pip-pyserial_3.4.bb <--

                    (this file is located here:/home/vm/Desktop/BuildingScripts )
           2. Step: Include the PiP-Package to your Yocto Project by
                    by adding follwoing line to the conf/local.conf file:
                      conf/local.conf:
                       IMAGE_INSTALL_append = "pip-pyserial"

           3. Step: Build your Yocto Project normanly with bitbake

          ----------------------------------------------------------------------------
           .. Script end..
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

### Finally on the running Yocto-Linux ....
````bash
root@cyclone5:~# pip list
Package    Version
---------- -------
pyserial   3.4.0
````
### is `pyserial`pre-installed 


# Author
* **Robin Sebastian**

*PiP2Bitbake* a project, that I have fully developed on my own. It is a academic project.
Today I'm a Master Student of electronic engineering with the major embedded systems. 
