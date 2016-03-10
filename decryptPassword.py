from weblogic.security.internal import *
from weblogic.security.internal.encryption import *

#This will prompt you to make sure you have SerializedSystemIni.dat file under #current directory from where you are running command

raw_input("Please make sure you have SerializedSystemIni.dat inside the current directory, if yes press ENTER to continue.")


# Encryption service
encryptionService = SerializedSystemIni.getEncryptionService(".")
clearOrEncryptService = ClearOrEncryptedService(encryptionService)

# Take encrypt password from user
pwd = raw_input("Please enter encrypted password (Eg. {3DES}Bxt5E3...): ")


# Delete unnecessary escape characters
preppwd = pwd.replace("\\", "")


# Decrypt password
print "Your password is: " + clearOrEncryptService.decrypt(preppwd)
