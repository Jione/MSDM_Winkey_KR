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
		print("\n오류: 이 메인보드에는 Microsoft Data Management(MSDM) 정보가 없습니다.")
		os.system("Pause > nul")
		return False
	
try:	
	WindowsKey=GetWindowsKey()
	if WindowsKey==False:
		print("\n오류: 예기치 않은 오류가 발생 했습니다.")
		os.system("Pause > nul")
		sys.exit(1)
	else:
		print("\n\n    MSDM 테이블 제품 키: \n\n    " + str(WindowsKey))
		# set clipboard data
		os.system("echo " + (str(WindowsKey)) + "|clip")
		print("\n\n\n    *** 제품 키가 클립보드로 복사 되었습니다. ***")
		print("\n\n제품 키로 윈도우 인증을 시도하려면 아무 키나 누르세요.")
		os.system("Pause > nul")
		os.system("cls")
		os.system('color 1f')
		print(" * MSDM Key checker for Windows8.x & 10 (OEM KEY) *")
		print("\n\n    아래의 제품 키로 윈도우 인증을 시도합니다.")
		print("\n    제품 키: " + (str(WindowsKey)) + "\n\n")
		print("\n설치 된 윈도우가 다른 버전일 경우 정상적으로 진행되지 않습니다.")
		print("\n\n윈도우 인증을 시도하려면 아무 키나 누르세요.")
		os.system("Pause > nul")
		os.system("cls")
		print("\n                             잠시만 기다려 주세요..\n")
		os.system("sc config sppsvc start= auto > nul")
		os.system("net start sppsvc > nul")
		os.system("timeout /t 2 >nul")
		os.system("cscript //Nologo C:\Windows\system32\slmgr.vbs /ipk " + (str(WindowsKey)))
		os.system("tracert -h 1 activation-v2.sls.microsoft.com > nul")
		os.system("cscript //Nologo C:\Windows\system32\slmgr.vbs /ato")
		print("\n\n                       윈도우 인증 시도가 완료 되었습니다.")
		os.system("Pause > nul")
		os.system('exit')
except:
	print("\n오류: 예기치 않은 오류가 발생 했습니다.")
	os.system("Pause > nul")
	sys.exit(1)