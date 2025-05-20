import fileoperation as f
from random import randint

class Administration:
    def __init__(self):
        # set the format for Member ID and Barcode
        self.ID_format = "Siiii" # "c" stands for character, "i" stands for number

        # Assign range of ascii code for ID generation
        self.number = (48, 57)
        self.letter = (65, 90)

    def openFile(self, filename):
        # Create the file operation object
        self.filename = filename
        self.fo = f.FileOperation(filename)

    def checkUnique(self, singleattribute, value):
        # Check if the value is a duplicate
        check = self.fo.findAllValues(singleattribute)
        if str(value) in check: return False
        return True

    def generateID(self):
        # Generate ID and check if valid
        while True:
            generate = ""
            for f in self.ID_format:
                if f == "c": generate += chr(randint(self.letter[0], self.letter[1]))
                elif f == "i": generate += chr(randint(self.number[0], self.number[1]))
                else: generate += f
            if self.checkUnique("Member ID", generate):
                return generate

    def modifyUserInformation(self, attributes, update):
        # Simply run the function in file operation
        self.fo.modifyUserInformation(attributes, update)

    def addNewMember(self, attributes):
        attributes.append(["Member ID", self.generateID()])
        attributes.append(["Status", "ACTIVE"])
        self.fo.addNewMember(attributes)

    def assignCard(self, attributes, cardID):
        if self.checkUnique("Card ID", cardID) and self.fo.checkIfDataIsBlank(attributes, "Card ID"):
            self.fo.modifyUserInformation(attributes, [["Card ID", cardID]])
            return True
        else:
            return False
    
    def transformResultToString(self, member, index = False):
        text = ""
        for attribute, value in member:
            if attribute == "#" and index == False: continue
            text += "{:<10}: {}".format(attribute, value)
            text += "\n"
        return text

    def displayAllMember(self):
        lst = self.fo.returnAllUserInformation()
        text = ""
        for index, member in enumerate(lst):
            text += "Member #{} ----------------\n{}\n".format(index + 1, self.transformResultToString(member))
        return text

    def searchMember(self, attributes):
        if attributes == []: return None
        member = self.fo.returnUserInformation(attributes)
        if member in ["", None]: return None
        text = self.transformResultToString(member, index = True)
        return text

    def returnSingleAttributeValue(self, attributes, singleAttribute):
        return self.fo.returnSingleValue(attributes, singleAttribute)

    def deleteMember(self, attributes):
        self.fo.deleteMember(attributes)

    def quit(self):
        self.fo.save()



