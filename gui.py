import execution as ad
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import re

# Initialize all variables and objects
filename = ""
admin = ad.Administration()
headingFont = ("Calibri", 15)

# Configuration and commands of each window.
def chooseFile():
    global filename

    # Hide Main Menu
    main.withdraw()

    # Define commands
    def selectFile():
        filetypes = (("Excel File", "*.xlsx"),)
        path = fd.askopenfilename(title = "Open a File", initialdir = r"C:\Users\Harvey\OneDrive\Desktop\Harvey\Python\2025PythonClass\FinalProject", filetypes = filetypes)
        updateFileName(path)

    def shortenFilePath(path):
        result = re.findall("\w*.xlsx", path)
        return result[0]
    
    def updateFileName(path):
        global filename
        fileLabel.config(text = "Selected File: {}".format(shortenFilePath(path)))
        filename = path
        doneSelection.grid(row = 4, column = 1, pady = 3)
    
    def doneSelectingFile():
        global filename
        global admin
        if filename == "": 
            messagebox.showinfo("Field Required", "Please select a file before continue.")
            return
        fileSelection.destroy()
        main.deiconify()
        admin.openFile(filename)

    def exitSystem():
        fileSelection.destroy()
        main.destroy()

    # Initialize Window
    fileSelection = Toplevel(main)
    fileSelection.title("Data Import")

    # Assign Widget
    instruction = Label(fileSelection, wraplength = 250, text = "Select an Excel file from your device to upload membership information.")
    selectFile = Button(fileSelection, text = "Select File", command = selectFile)
    fileLabel = Label(fileSelection, text = "Selected File: None")
    doneSelection = Button(fileSelection, text = "Continue", command = doneSelectingFile)
    
    # Configure Widgets
    instruction.grid(row = 1, column = 1, padx = 10, pady = 12)
    selectFile.grid(row = 2, column = 1, pady = 5)
    fileLabel.grid(row = 3, column = 1, pady = 8)

    # Modify Protocal
    fileSelection.protocol("WM_DELETE_WINDOW", exitSystem)
    
    # Visualize the window
    fileSelection.mainloop()

def addNewMember(): 
    # Define Commands
    def confirm():
        # Check Input Validity
        if field3Entry.get() not in ["M", "F"]:
            messagebox.showinfo("Input Invalide", "The input for 'Gender' must be either 'M' or 'F'.")
            return
        if field1Entry.get() not in ["", None] and admin.checkUnique("Card ID", field1Entry.get().strip("\n")) == False:
            messagebox.showinfo("Input Invalid", "This card number already exist.")
            return

        # Analyze Attributes & Values
        text = "CardID: {}\nFull Name: {}\nGender: {}".format(field1Entry.get(), field2Entry.get(), field3Entry.get())
        response = messagebox.askokcancel("Registration Confirmation", "Are you sure to add the following member:\n" + text)
        if response == False:
            return
        attributes = []
        if field1Entry.get() not in ["", None]: attributes.append(["Card ID", field1Entry.get().strip("\n")])
        if field2Entry.get() not in ["", None]: attributes.append(["Name", field2Entry.get().strip("\n")])
        if field3Entry.get() not in ["", None]: attributes.append(["Gender", field3Entry.get().strip("\n")])

        # Add member to the sheet
        admin.addNewMember(attributes)

        # Notify user for success and reset all input
        messagebox.showinfo("Execution Complete", "User added successfully.")
        clearAll()

    def clearAll():
        allFields = [field1Entry, field2Entry, field3Entry]
        for i in allFields:
            i.delete(0, END)
        field1Entry.focus_set()
    
    def enter(block):
        if block == 1: field2Entry.focus_set()
        elif block == 2: field3Entry.focus_set()
        elif block == 3: confirm()

    # Initialize Window
    addMember = Toplevel(main)
    addMember.title("New Member Registration")

    # Assign Widgets
    heading = Label(addMember, text = "Register New Member", font = headingFont)
    field1Label = Label(addMember, text = "Card ID")
    field2Label = Label(addMember, text = "Full Name")
    field3Label = Label(addMember, text = "Gender")
    field1Entry = Entry(addMember)
    field2Entry = Entry(addMember)
    field3Entry = ttk.Combobox(addMember, values = ["M", "F"], width = 10)
    complete = Button(addMember, text = "Continue", command = confirm)
    clearInput = Button(addMember, text = "Clear All Input", command = clearAll)

    # Configure Widgets
    heading.grid(row = 1, column = 1, columnspan = 3, pady = 10)
    field1Label.grid(row = 2, column = 1, padx = 10, pady = 5)
    field2Label.grid(row = 3, column = 1, padx = 10, pady = 5)
    field3Label.grid(row = 4, column = 1, padx = 10, pady = 5)
    field1Entry.grid(row = 2, column = 2, padx = 15, columnspan = 2)
    field2Entry.grid(row = 3, column = 2, padx = 15, columnspan = 2)
    field3Entry.grid(row = 4, column = 2, padx = 15, columnspan = 2)
    complete.grid(row = 5, column = 3, pady = 20, padx = 10)
    clearInput.grid(row = 5, column = 2, padx = 10)

    # Event Binding
    field1Entry.bind("<Return>", lambda event: enter(1))
    field2Entry.bind("<Return>", lambda event: enter(2))
    field3Entry.bind("<Return>", lambda event: enter(3))

    # Visualize Window
    addMember.mainloop()

def cardAssignment():
    # Define Commands
    def searchMember():
        result = admin.searchMember([[attribute.get(), inputEntry.get().strip("\n")]])
        if result == None or result == False:
            result = "Member not found."
            userLabel.config(text = result)
            inputEntry.focus_set()
            return
        userLabel.config(text = result)
        cardIDEntry.focus_set()

    def updateLabel(text):
        inputLabel.config(text = text)

    def clearSearchResult():
        userLabel.config(text = "")
        inputEntry.delete(0, END)
        inputEntry.focus_set()

    def clearCard():
        information.config(text = "")
        cardIDEntry.delete(0, END)
        cardIDEntry.focus_set()

    def assign():
        if admin.assignCard([[attribute.get(), inputEntry.get().strip("\n")]], cardIDEntry.get().strip("\n")):
            information.config(text = "Successfully link assigned card.")
            clearCard()
            clearSearchResult()
        else:
            information.config(text = "This card is occupied by other member or this member has already been assigned a card.", wrap = 300)

    def enter(n):
        cardIDEntry.focus_set()
        if n == 1: searchMember()
        else: assign()
            
    # Window Setup
    cardassignment = Toplevel(main)
    cardassignment.title("Card Assignment")

    # Assign Widget
    attribute = StringVar()
    attribute.set("Barcode")
    heading = Label(cardassignment, text = "Card Assignment", font = headingFont)
    selectAttributeLabel = Label(cardassignment, text = "Select one attribute:")
    attribute1Radio = Radiobutton(cardassignment, text = "Member ID", var = attribute, value = "Member ID", width = 8, command = lambda: updateLabel("Member ID"))
    attribute2Radio = Radiobutton(cardassignment, text = "Barcode", var = attribute, value = "Barcode", width = 6, command = lambda: updateLabel("Barcode"))
    attribute3Radio = Radiobutton(cardassignment, text = "Name", var = attribute, value = "Name", width = 5, command = lambda: updateLabel("Name"))
    inputLabel = Label(cardassignment, text = attribute.get())
    inputEntry = Entry(cardassignment, width = 30)
    searchMemberButton = Button(cardassignment, text = "Search Member", width = 15, command = searchMember)
    userLabel = Label(cardassignment, text = "", justify = "left", font = ("Consolas", 10))
    clearSearchButton = Button(cardassignment, text = "Clear Search Result", width = 15, command = clearSearchResult)
    cardIDLabel = Label(cardassignment, text = "Card ID:")
    cardIDEntry = Entry(cardassignment, width = 30)
    clearCardID = Button(cardassignment, text = "Clear Card ID", width = 15, command = clearCard)
    register = Button(cardassignment, text = "Register", width = 15, command = assign)
    information = Label(cardassignment, text = "")

    # Configure Widget
    heading.grid(row = 1, column = 1, columnspan = 3, pady = 10)
    selectAttributeLabel.grid(row = 2, column = 1, padx = 10)
    attribute1Radio.grid(row = 3, column = 1, padx = 0, pady = 5)
    attribute2Radio.grid(row = 3, column = 2, padx = 0)
    attribute3Radio.grid(row = 3, column = 3, padx = 0)
    inputLabel.grid(row = 4, column = 1, padx = 10, pady = 5)
    inputEntry.grid(row = 4, column = 2, columnspan = 2, padx = 0, sticky = "w")
    searchMemberButton.grid(row = 5, column = 3, padx = 10)
    userLabel.grid(row = 6, column = 1, columnspan = 3, pady = 10, padx = 15, sticky = "W")
    clearSearchButton.grid(row = 7, column = 3, padx = 10, pady = 10)
    cardIDLabel.grid(row = 8, column = 1, padx = 10, pady = 5)
    cardIDEntry.grid(row = 8, column = 2, columnspan = 2, padx = 0, sticky = "w")
    clearCardID.grid(row = 9, column = 2, padx = 10)
    register.grid(row = 9, column = 3, padx = 10, pady = 10)
    information.grid(row = 10, column = 1, columnspan = 3, pady = 5)
    inputEntry.focus_set()

    # Event Binding
    inputEntry.bind("<Return>", lambda event: enter(1))
    cardIDEntry.bind("<Return>", lambda event: enter(2))

    # Visualize the Window
    cardassignment.mainloop()

def memberManage():
    # Define Commands
    def clearAllInput():
        # Clear all fields
        for field in [memberIDEntry, cardIDEntry, barcodeEntry, nameEntry, genderEntry]:
            field.delete(0, END)
        memberIDEntry.focus_set()
        commandStatus("disabled")

    def readAttributes():
        attributes = []
        blank = ["", None]
        if memberIDEntry.get() not in blank: attributes.append(["Member ID", memberIDEntry.get().strip("\n")])
        if cardIDEntry.get() not in blank: attributes.append(["Card ID", cardIDEntry.get().strip("\n")])
        if barcodeEntry.get() not in blank: attributes.append(["Barcode", barcodeEntry.get().strip("\n")])
        if nameEntry.get() not in blank: attributes.append(["Name", nameEntry.get().strip("\n")])
        if genderEntry.get() not in blank: attributes.append(["Gender", genderEntry.get().strip("\n")])
        return attributes

    def search():
        # Get Attributes and search member
        attributes = readAttributes()
        print(attributes)
        member = admin.searchMember(attributes)
        print(member)

        # Update Information
        if member == None or member == False or member == "" or attributes == []: 
            member = "No member found."
            commandStatus("disabled")
        else: 
            commandStatus("normal")
        memberInfo.config(text = member)

    def commandStatus(a):
        # Enable/Disable execution buttons
        if a not in ["normal", "disabled"]: return
        for i in [removeCard, deleteMember, memberStatus]:
            i.config(state = a)

    def unlinkCard():
        # Confirmation
        respond = messagebox.askokcancel("Command Confirmation", "Are you sure to remove the card from the member?")
        
        # Modify information
        if respond:
            admin.modifyUserInformation(readAttributes(), [["Card ID", None]])
            executionInfo.config(text = "Successfully removed card from the member.")
            clearAllInput()
        else:
            executionInfo.config(text = "Execution canceled.")

    def removeMember():    
        # Confirmation
        respond = messagebox.askokcancel("Command Confirmation", "Are you sure to delete the member from the list?")

        # Modify Information
        if respond:
            admin.deleteMember(readAttributes())
            executionInfo.config(text = "Successfully deleted the member from the list.")
            clearAllInput()
        else:
            executionInfo.config(text = "Execution canceled.")

    def status():
        # Confirmation
        respond = messagebox.askokcancel("Command Confirmation", "Are you sure to modify the status of the member?")

        # Modify Information
        if respond:
            if admin.returnSingleAttributeValue(readAttributes(), "Status") == "ACTIVE": s = "INACTIVE"
            else: s = "ACTIVE"
            admin.modifyUserInformation(readAttributes(), [["Status", s]])
            executionInfo.config(text = "Successfully modified the status of the member.")
        else:
            executionInfo.config(text = "Execution canceled.")

    def enter(n):
        if n == 1: cardIDEntry.focus_set()
        elif n == 2: barcodeEntry.focus_set()
        elif n == 3: nameEntry.focus_set()
        elif n == 4: genderEntry.focus_set()
        elif n == 5: search()

    # Window Setup
    memberManagement = Toplevel(main)
    memberManagement.title("Member Management")

    # Assign Widget
    heading = Label(memberManagement, text = "Member Management", font = headingFont)
    prompt = Label(memberManagement, text = "Search Member (no need to fill in all):")
    memberIDLabel = Label(memberManagement, text = "Member ID")
    cardIDLabel = Label(memberManagement, text = "Card ID")
    barcodeLabel = Label(memberManagement, text = "Barcode")
    nameLabel = Label(memberManagement, text = "Name")
    genderLabel = Label(memberManagement, text = "Gender")
    memberIDEntry = Entry(memberManagement, width = 24)
    cardIDEntry = Entry(memberManagement, width = 24)
    barcodeEntry = Entry(memberManagement, width = 24)
    nameEntry = Entry(memberManagement, width = 24)
    genderEntry = ttk.Combobox(memberManagement, values = ["M", "F"])
    clearInput = Button(memberManagement, text = "Clear All Input", width = 12, command = clearAllInput)
    searchMember = Button(memberManagement, text = "Search Member", width = 12, command = search)
    memberInfo = Label(memberManagement, text = "", justify = "left", font = ("Consolas", 10))
    removeCard = Button(memberManagement, text = "Remove Card", state = DISABLED, width = 18, command = unlinkCard)
    deleteMember = Button(memberManagement, text = "Delete Member", state = DISABLED, width = 18, command = removeMember)
    memberStatus = Button(memberManagement, text = "Deactivate/Activate Member", state = DISABLED, width = 34, command = status)
    executionInfo = Label(memberManagement, text = "")

    # Configure Widget
    heading.grid(row = 1, column = 1, columnspan = 3, pady = 10)
    prompt.grid(row = 2, column = 1, columnspan = 3, padx = 10, pady = 5, sticky = "w")
    memberIDLabel.grid(row = 3, column = 1, padx = 10, pady = 5)
    cardIDLabel.grid(row = 4, column = 1, padx = 10, pady = 5)
    barcodeLabel.grid(row = 5, column = 1, padx = 10, pady = 5)
    nameLabel.grid(row = 6, column = 1, padx = 10, pady = 5)
    genderLabel.grid(row = 7, column = 1, padx = 10, pady = 5)
    memberIDEntry.grid(row = 3, column = 2, columnspan = 2, padx = 5)
    cardIDEntry.grid(row = 4, column = 2, columnspan = 2, padx = 5)
    barcodeEntry.grid(row = 5, column = 2, columnspan = 2, padx = 5)
    nameEntry.grid(row = 6, column = 2, columnspan = 2, padx = 5)
    genderEntry.grid(row = 7, column = 2, columnspan = 2, padx = 5)
    clearInput.grid(row = 8, column = 2, padx = 10)
    searchMember.grid(row = 8, column = 3, padx = 10)
    memberInfo.grid(row = 9, column = 1, columnspan = 2, pady = 10, padx = 10, sticky = "w")
    removeCard.grid(row = 10, column = 1, columnspan = 2, pady = 5, padx = 5)
    deleteMember.grid(row = 10, column = 3, pady = 5, padx = 5)
    memberStatus.grid(row = 11, column = 1, columnspan = 3, pady = 5, padx = 5)
    executionInfo.grid(row = 12, column = 1, columnspan = 3, pady = 5, padx = 5)

    # Event Binding
    memberIDEntry.bind("<Return>", lambda event: enter(1))
    cardIDEntry.bind("<Return>", lambda event: enter(2))
    barcodeEntry.bind("<Return>", lambda event: enter(3))
    nameEntry.bind("<Return>", lambda event: enter (4))
    genderEntry.bind("<Return>", lambda event: enter(5))

    # Visualize Window
    memberManagement.mainloop()

def dataModification():
    # Initialize Variables
    searchAttribute = []
    updateAttribute = []

    # Define Commands
    def clearInput():
        for entry in [memberIDEntry, cardIDEntry, barcodeEntry, nameEntry, genderEntry]:
            entry.delete(0, END)

    def getAttributes():
        attributes = []
        blank = ["", None]
        if memberIDEntry.get() not in blank: 
            if admin.checkUnique("Member ID", memberIDEntry.get().strip("\n")) == False:
                    messagebox.showinfo("Invalid Input", "This Member ID has been occupied.")
                    return None
            attributes.append(["Member ID", memberIDEntry.get().strip("\n")])
        if cardIDEntry.get() not in blank: 
            if admin.checkUnique("Card ID", cardIDEntry.get().strip("\n")) == False:
                messagebox.showinfo("Invalid Input", "This Card ID has been occupied.")
                return None
            attributes.append(["Card ID", cardIDEntry.get().strip("\n")])
        if barcodeEntry.get() not in blank: 
            if admin.checkUnique("Barcode", barcodeEntry.get().strip("\n")) == False:
                messagebox.showinfo("Invalid Input", "This barcode has been occupied.")
                return None
            attributes.append(["Barcode", barcodeEntry.get().strip("\n")])
        if nameEntry.get() not in blank: attributes.append(["Name", nameEntry.get().strip("\n")])
        if genderEntry.get() not in blank: attributes.append(["Gender", genderEntry.get().strip("\n")])
        return attributes

    def search(attributes):
        return admin.searchMember(attributes)

    def updateMemberInfo():
        member = search(getAttributes())
        if member in ["", None, False]:
            updateStage(1)
            confirm.grid_remove()
            confirm.config(state = "disabled")
            member = "No User Found."
        else:
            confirm.grid(row = 4, column = 2, pady = 5)
            confirm.config(state = "normal")
            updateStage(2)
            confirm.config(text = "Confirm Member", command = confirmMember, state = "normal")
        information.config(text = member)

    def updateInformation():
        updateAttribute = getAttributes(unique = True)
        if updateAttribute == []:
            messagebox.showinfo("No fields filled", "Please fill in at least one of the data to continue.")
            return None 
        elif updateAttribute == None:
            return None
        admin.modifyUserInformation(searchAttribute, updateAttribute)
        clearInput()
        messagebox.showinfo("Modification Complete", "Modification to the data of the user is complete.")
        information.config(text = "")
        updateStage(1)
        confirm.grid_remove()
        confirm.config(state = "disabled")
    
    def confirmMember():
        searchAttribute = getAttributes()
        updateStage(2)
        clearInput()
        confirm.config(text = "Rematch Member", command = rematchMember, state = "normal")

    def rematchMember():
        confirm.grid_remove()
        searchAttribute = []
        updateStage(1)
        information.config(text = "")
        confirm.config(text = "Confirm Member", command = confirmMember, state = "normal")

    def updateStage(stage):
        if stage == 1:
            executionButton.config(text = "Search User", command = updateMemberInfo)
            prompt.config(text = "Step 1: Match a member by inputting the following fields.")
        else: 
            executionButton.config(text = "Update Information", command = updateInformation)
            prompt.config(text = "Step 2: Input new information and update it to the file. ")

    def enter(n):
        if n == 1: cardIDEntry.focus_set()
        elif n == 2: barcodeEntry.focus_set()
        elif n == 3: nameEntry.focus_set()
        elif n == 4: genderEntry.focus_set()
        elif n == 5:
            if executionButton["text"] == "Search User": updateMemberInfo()
            else: updateInformation()
            modification.focus_set()

    # Initialize Window
    modification = Toplevel(main)
    modification.title("Data Modification")

    # Assign Widgets
    heading = Label(modification, text = "Data Modification", font = headingFont)
    prompt = Label(modification, text = "Step 1: Match a member by inputting the following fields.", justify = "left")
    information = Label(modification, text = "", font = ("Consolas", 10), justify = "left")
    confirm = Button(modification, text = "Confirm Member", width = 25, state = "disabled", command = confirmMember)
    memberIDLabel = Label(modification, text = "Member ID", width = 10)
    cardIDLabel = Label(modification, text = "Card ID", width = 10)
    barcodeLabel = Label(modification, text = "Barcode", width = 10)
    nameLabel = Label(modification, text = "Name", width = 10)
    genderLabel = Label(modification, text = "Gender", width = 10)
    memberIDEntry = Entry(modification, width = 25)
    cardIDEntry = Entry(modification, width = 25)
    barcodeEntry = Entry(modification, width = 25)
    nameEntry = Entry(modification, width = 25)
    genderEntry = ttk.Combobox(modification, values = ["M", "F"], width = 21)
    clearAll = Button(modification, text = "Clear Input", width = 12, command = clearInput)
    executionButton = Button(modification, text = "Search User", width = 25, command = updateMemberInfo)

    # Configure Widgets
    heading.grid(row = 1, column = 1, columnspan = 2, pady = 10)
    prompt.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 5, sticky = "w")
    information.grid(row = 3, column = 1, columnspan = 2, padx = 10, pady = 5, sticky = "w")
    memberIDLabel.grid(row = 5, column = 1, padx = 10, pady = 5)
    cardIDLabel.grid(row = 6, column = 1, pady = 5)
    barcodeLabel.grid(row = 7, column = 1, pady = 5)
    nameLabel.grid(row = 8, column = 1, pady = 5)
    genderLabel.grid(row = 9, column = 1, pady = 5)
    memberIDEntry.grid(row = 5, column = 2, padx = 17, pady = 5)
    cardIDEntry.grid(row = 6, column = 2, pady = 5)
    barcodeEntry.grid(row = 7, column = 2, pady = 5)
    nameEntry.grid(row = 8, column = 2, pady = 5)
    genderEntry.grid(row = 9, column = 2, pady = 5)
    clearAll.grid(row = 10, column = 1, padx = 10, pady = 5)
    executionButton.grid(row = 10, column = 2, padx = 10)

    # Event Binding
    memberIDEntry.bind("<Return>", lambda event: enter(1))
    cardIDEntry.bind("<Return>", lambda event: enter(2))
    barcodeEntry.bind("<Return>", lambda event: enter(3))
    nameEntry.bind("<Return>", lambda event: enter(4))
    genderEntry.bind("<Return>", lambda event: enter(5))

    # Visualize Window
    memberIDEntry.focus_set()
    modification.mainloop()

def findMember():
    # Define Commands
    def getAttributes():
        attributes = []
        blank = ["", None]
        if cardIDEntry.get() not in blank: attributes.append(["Card ID", cardIDEntry.get().strip("\n")])
        if memberIDEntry.get() not in blank: attributes.append(["Member ID", memberIDEntry.get().strip("\n")])
        if barcodeEntry.get() not in blank: attributes.append(["Barcode", barcodeEntry.get().strip("\n")])
        if nameEntry.get() not in blank: attributes.append(["Name", nameEntry.get().strip("\n")])
        if genderEntry.get() not in blank: attributes.append(["Gender", genderEntry.get().strip("\n")])
        return attributes
    
    def clearInput():
        for i in [cardIDEntry, memberIDEntry, barcodeEntry, nameEntry, genderEntry]:
            i.delete(0, END)
        information.config(text = "")
        cardIDEntry.focus_set()

    def searchMember():
        attri = getAttributes()
        r = admin.searchMember(attri)
        if r:
            information.config(text = r)
        else:
            information.config(text = "No Member Found.")

    def enter(n):
        if n == 1: memberIDEntry.focus_set()
        elif n == 2: barcodeEntry.focus_set()
        elif n == 3: nameEntry.focus_set()
        elif n == 4: genderEntry.focus_set()
        elif n == 5: searchMember()

    # Initialize Window
    search = Toplevel(main)
    search.title("Search Member")

    # Assign Widgets
    heading = Label(search, text = "Search Member", font = headingFont)
    instruction = Label(search, text = "Input the following fields to search for a member.", justify = "left")
    cardIDLabel = Label(search, text = "Card ID")
    memberIDLabel = Label(search, text = "Member ID")
    barcodeLabel = Label(search, text = "Barcode")
    nameLabel = Label(search, text = "Name")
    genderLabel = Label(search, text = "Gender")
    cardIDEntry = Entry(search, width = 20)
    memberIDEntry = Entry(search, width = 20)
    barcodeEntry = Entry(search, width = 20)
    nameEntry = Entry(search, width = 20)
    genderEntry = ttk.Combobox(search, values = ["M", "F"], width = 17)
    clearButton = Button(search, text = "Clear All Input", width = 15, command = clearInput)
    searchButton = Button(search, text = "Search Member", width = 20, command = searchMember)
    information = Label(search, text = "", font = ("Consolas", 10), justify = "left")

    # Configure Widgets
    heading.grid(row = 1, column = 1, columnspan = 2, pady = 10)
    instruction.grid(row = 2, column = 1, columnspan = 2, sticky = "w", padx = 10)
    cardIDLabel.grid(row = 3, column = 1, padx = 5, pady = 5)
    memberIDLabel.grid(row = 4, column = 1, pady = 5)
    barcodeLabel.grid(row = 5, column = 1, pady = 5)
    nameLabel.grid(row = 6, column = 1, pady = 5)
    genderLabel.grid(row = 7, column = 1, pady = 5)
    cardIDEntry.grid(row = 3, column = 2, padx = 5)
    memberIDEntry.grid(row = 4, column = 2)
    barcodeEntry.grid(row = 5, column = 2)
    nameEntry.grid(row = 6, column = 2)
    genderEntry.grid(row = 7, column = 2)
    clearButton.grid(row = 8, column = 1, sticky = "e", padx = 5, pady = 10)
    searchButton.grid(row = 8, column = 2, padx = 5)
    information.grid(row = 9, column = 1, columnspan = 2, padx = 10, pady = 10, sticky = "w")

    # Event Binding
    cardIDEntry.bind("<Return>", lambda event: enter(1))
    memberIDEntry.bind("<Return>", lambda event: enter(2))
    barcodeEntry.bind("<Return>", lambda event: enter(3))
    nameEntry.bind("<Return>", lambda event: enter(4))
    genderEntry.bind("<Return>", lambda event: enter(5))

    # Visualize Window
    search.mainloop()

def displayAllMember():
    # Define Commands
    def updateListbox():
        # Gather new information
        lst = updateInformation()

        # Upload new information
        information.delete(0, END)
        for line in lst:
            information.insert(END, line)

    def updateInformation():
        return list(admin.displayAllMember().split('\n'))

    # Initialize Window
    allMembers = Toplevel(main)
    allMembers.title("Member List")
    allMembers.geometry("250x580")
    allMembers.resizable(False, False)

    # Assign Widgets
    heading = Label(allMembers, text = "Member List", font = headingFont)
    update = Button(allMembers, text = "Update Information", command = updateListbox, width = 30)
    information = Listbox(allMembers, width = 30, height = 30, font = ("Consolas", 10))
    scroll = Scrollbar(allMembers, orient = "vertical", command = information.yview)

    # Configure Widgets
    heading.grid(row = 1, column = 1, columnspan = 2, pady = 10)
    update.grid(row = 2, column = 1, columnspan = 2, pady = 5)
    information.grid(row = 3, column = 1, pady = 5, padx = 10)
    scroll.grid(row = 3, column = 2, sticky = "ns")

    # Event Binding
    information.configure(yscrollcommand = scroll.set)

    # Visualize Window
    updateListbox()
    allMembers.mainloop()

# Main Menu Window setup
main = Tk()
main.title("Card Management System - Main Menu")

# Assign GUI variables
allMemberInformation = StringVar()
allMemberInformation.set("")

# Define Commands
def closeSystem():
    respond = messagebox.askokcancel("", "Are you sure to exit the system?")
    if respond:
        try:
            admin.quit()
            main.destroy()
        except:
            messagebox.showinfo("File Saving Process Error", "Please close the file during programming operation.")

# Assign Widgets
heading = Label(main, text = "Card Management System - Main Menu", font = headingFont)
newMember = Button(main, text = "Register New Member", width = 25, command = addNewMember)
cardAssign = Button(main, text = "Card Assignment", width = 25, command = cardAssignment)
management = Button(main, text = "Member Management", width = 25, command = memberManage)
modify = Button(main, text = "Data Modification", width = 25, command = dataModification)
listofMembers = Button(main, text = "Member List", width = 25, command = displayAllMember)
search = Button(main, text = "Search Member", width = 25, command = findMember)
exitSystem = Button(main, text = "Exit System", width = 25, command = closeSystem)

# Configure Widgets
heading.grid(row = 1, column = 1, padx = 5, pady = 10)
newMember.grid(row = 2, column = 1, padx = 5, pady = 5)
cardAssign.grid(row = 3, column = 1, padx = 5, pady = 5)
management.grid(row = 4, column = 1, padx = 5, pady = 5)
modify.grid(row = 5, column = 1, padx = 5, pady = 5)
listofMembers.grid(row = 6, column = 1, padx = 5, pady = 5)
search.grid(row = 7, column = 1, pady = 5)
exitSystem.grid(row = 8, column = 1, pady = 5)

# Modify Protocal
main.protocol("WM_DELETE_WINDOW", closeSystem)

# Visualize the window and prompt user to select file
chooseFile()
main.mainloop()