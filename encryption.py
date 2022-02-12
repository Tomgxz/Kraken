class Encryption():
    """ Encryption module for Kraken"""

    def __init__(self,master):
        """
        Constructs a :class: 'Encryption <Encryption>'
        """

        from cryptography.fernet import Fernet
        from dotenv import load_dotenv
        import os

        self.os=os
        self.cryptor=Fernet

        self.master=master

        load_dotenv()

    def getKey(self):
        """
        Generates and returns the encryption key

        :returns: An byte-encoded string
        :rtype: str
        """

        return self.os.environ.get("KEY").encode()

    def decrypt(self,x):
        """
        Decrypts a string. The string must have been encoded by this module.

        :param x str:
            The encrypted string to decrypt.

        :returns: The decrypted string
        :rtype: str
        """

        return self.cryptor(self.getKey()).decrypt(x).decode()

    def encrypt(self,x):
        """
        Encrypts a string.

        :param x str:
            The string to encrypt.

        :returns: The encrypted byte-encoded string
        :rtype: str
        """

        return self.cryptor(self.getKey()).encrypt(x.encode())

    def usernameExists(self,usr):
        """
        See whether a username exists in the username bin file

        :param usr str:
            A decrypted username to search for

        :returns: A boolean reffering to whether the username exists
        :rtype: bool
        """

        x=self.master.execute(f"SELECT EXISTS(SELECT * FROM users WHERE username='{usr}')").fetchone()
        if x[0]==1:
            return True
        return False

    def credentialsExist(self,usr,pwd):
        """
        See whether the username and password combination inputted match in the bin files

        :param usr str:
            A decrypted username to search for
        :param pwd str:
            A decrypted password to search for

        :returns: A boolean reffering to whether the credentials match
        :rtype: bool
        """

        self.logger.info("Searching for credentials...")
        usrpos=None
        with open(self.usrFile,"rb") as usrList:
            usrs=usrList.readlines()
            itera=0
            for line in usrs:
                if usr == self.decrypt(line):
                    usrpos=itera
                    break
                itera+=1
        if usrpos is None:
            return False
        with open(self.pwdFile,"rb") as pwdList:
            pwds=pwdList.readlines()
            if pwd == self.decrypt(pwds[usrpos]):
                return True
        return False

    def store(self,usr,pwd):
        """
        Stores an encrypted username and password. Both paramaters must have been previously encrypted by this module.

        :param usr str:
            An encrypted byte-encoded string containing the username to store
        :param pwd str:
            An encrypted byte-encoded string containing the password to store

        :returns: A boolea determining whether the process was successful
        :rtype: bool
        """

        with open(self.usrFile,"ab") as usrList:
            usrList.write(usr+"\n".encode())
            usrList.close()
        with open(self.pwdFile,"ab") as pwdList:
            pwdList.write(pwd+"\n".encode())
            pwdList.close()
        return True

if __name__ == "__main__":
    raise Exception(
        "This module is to be used in conjunction with the Kraken application and not as a standalone module.")
