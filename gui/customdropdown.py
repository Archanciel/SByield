from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown

from gui.sbyieldgui import STATUS_BAR_ERROR_SUFFIX


class CustomDropDown(DropDown):
	saveButton = ObjectProperty(None)
	statusToRequestInputButton = ObjectProperty(None)
	
	def __init__(self, owner):
		super().__init__()
		self.owner = owner

	def showLoad(self):
		message = 'Data path ' + self.owner.dataPath + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.dataPath, message):
			self.owner.openFileLoadPopup()

	def showSave(self):
		message = 'Data path ' + self.owner.dataPath + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.dataPath, message):
			self.owner.openFileSavePopup()

	def help(self):
		self.owner.displayHelp()
	
	def copyStatusBarStrToRequestEntry(self):
		statusBarStr = self.owner.statusBarTextInput.text
		
		self.owner.requestInput.text = statusBarStr.replace(STATUS_BAR_ERROR_SUFFIX, '')
		self.owner.statusBarTextInput.text = ''
		self.statusToRequestInputButton.disabled = True
		self.owner.refocusOnRequestInput()
		self.dismiss()