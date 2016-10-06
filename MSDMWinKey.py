#-*- coding: utf-8 -*-
import os
import sys
import ctypes
import ctypes.wintypes

#####################################################
#script to query windows 8.x OEM key from PC firmware
#ACPI -> table MSDM -> raw content -> byte offset 56 to end
#ck, 03-Jan-2014 (christian@korneck.de)
#####################################################

#for ref: common STR to DWORD conversions: ACPI: 1094930505 - FIRM: 1179210317 - RSMB: 1381190978 - FACP: 1178682192 - PCAF: 1346584902 - MSDM: 1297302605 - MDSM  1296323405

print(" * MSDM Key checker for Windows8.x & 10 (OEM KEY) *")
os.system('Title MSDM Key checker for Windows8.x-10')

def EnumAcpiTables():
#returns a list of the names of the ACPI tables on this system
	FirmwareTableProviderSignature=ctypes.wintypes.DWORD(1094930505)
	pFirmwareTableBuffer=ctypes.create_string_buffer(0)
	BufferSize=ctypes.wintypes.DWORD(0)
	#http://msdn.microsoft.com/en-us/library/windows/desktop/ms724259
	EnumSystemFirmwareTables=ctypes.WinDLL("Kernel32").EnumSystemFirmwareTables
	ret=EnumSystemFirmwareTables(FirmwareTableProviderSignature, pFirmwareTableBuffer, BufferSize)
	pFirmwareTableBuffer=None
	pFirmwareTableBuffer=ctypes.create_string_buffer(ret)
	BufferSize.value=ret
	ret2=EnumSystemFirmwareTables(FirmwareTableProviderSignature, pFirmwareTableBuffer, BufferSize)
	return [pFirmwareTableBuffer.value[i:i+4] for i in range(0, len(pFirmwareTableBuffer.value), 4)]

def FindAcpiTable(table):
#checks if specific ACPI table exists and returns True/False
	tables = EnumAcpiTables()
	if table in tables:
		return True
	else:
		return False

def GetAcpiTable(table,TableDwordID):
#returns raw contents of ACPI table
	#http://msdn.microsoft.com/en-us/library/windows/desktop/ms724379x
	GetSystemFirmwareTable=ctypes.WinDLL("Kernel32").GetSystemFirmwareTable
	FirmwareTableProviderSignature=ctypes.wintypes.DWORD(1094930505)
	FirmwareTableID=ctypes.wintypes.DWORD(int(TableDwordID))
	pFirmwareTableBuffer=ctypes.create_string_buffer(0)
	BufferSize=ctypes.wintypes.DWORD(0)
	ret = GetSystemFirmwareTable(FirmwareTableProviderSignature, FirmwareTableID, pFirmwareTableBuffer, BufferSize)
	pFirmwareTableBuffer=None
	pFirmwareTableBuffer=ctypes.create_string_buffer(ret)
	BufferSize.value=ret
	ret2 = GetSystemFirmwareTable(FirmwareTableProviderSignature, FirmwareTableID, pFirmwareTableBuffer, BufferSize)
	return pFirmwareTableBuffer.raw

def GetWindowsKey():
	#returns Windows Key as string
	table=b"MSDM"
	TableDwordID=1296323405
	if FindAcpiTable(table)==True:
		try:
			rawtable = GetAcpiTable(table, TableDwordID)
			#http://msdn.microsoft.com/library/windows/hardware/hh673514
			#byte offset 36 from beginning = Microsoft 'software licensing data structure' / 36 + 20 bytes offset from beginning = Win Key
			return rawtable[56:len(rawtable)].decode("utf-8")
		except:
			return False
	else:
		print("\n����: �� ���κ��忡�� Microsoft Data Management(MSDM) ������ �����ϴ�.")
		os.system("Pause > nul")
		return False
	
try:	
	WindowsKey=GetWindowsKey()
	if WindowsKey==False:
		print("\n����: ����ġ ���� ������ �߻� �߽��ϴ�.")
		os.system("Pause > nul")
		sys.exit(1)
	else:
		print("\n\n    MSDM ���̺� ��ǰ Ű: \n\n    " + str(WindowsKey))
		# set clipboard data
		os.system("echo " + (str(WindowsKey)) + "|clip")
		print("\n\n\n    *** ��ǰ Ű�� Ŭ������� ���� �Ǿ����ϴ�. ***")
		print("\n\n��ǰ Ű�� ������ ������ �õ��Ϸ��� �ƹ� Ű�� ��������.")
		os.system("Pause > nul")
		os.system("cls")
		os.system('color 1f')
		print(" * MSDM Key checker for Windows8.x & 10 (OEM KEY) *")
		print("\n\n    �Ʒ��� ��ǰ Ű�� ������ ������ �õ��մϴ�.")
		print("\n    ��ǰ Ű: " + (str(WindowsKey)) + "\n\n")
		print("\n��ġ �� �����찡 �ٸ� ������ ��� ���������� ������� �ʽ��ϴ�.")
		print("\n\n������ ������ �õ��Ϸ��� �ƹ� Ű�� ��������.")
		os.system("Pause > nul")
		os.system("cls")
		print("\n                             ��ø� ��ٷ� �ּ���..\n")
		os.system("sc config sppsvc start= auto > nul")
		os.system("net start sppsvc > nul")
		os.system("timeout /t 2 >nul")
		os.system("cscript //Nologo C:\Windows\system32\slmgr.vbs /ipk " + (str(WindowsKey)))
		os.system("tracert -h 1 activation-v2.sls.microsoft.com > nul")
		os.system("cscript //Nologo C:\Windows\system32\slmgr.vbs /ato")
		print("\n\n                       ������ ���� �õ��� �Ϸ� �Ǿ����ϴ�.")
		os.system("Pause > nul")
		os.system('exit')
except:
	print("\n����: ����ġ ���� ������ �߻� �߽��ϴ�.")
	os.system("Pause > nul")
	sys.exit(1)