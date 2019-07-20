Attribute VB_Name = "Module1"
Sub TestingMacro()
Attribute TestingMacro.VB_Description = "Testing macro"
Attribute TestingMacro.VB_ProcData.VB_Invoke_Func = "t\n14"
'
' TestinMacro Macro
' Testing macro
'
' Keyboard Shortcut: Ctrl+t
'
    Range("C10").Select
End Sub

Sub ExportToCsvMacro()
'
' Macro for exporting the selection to csv file. The selection should be a continues range
' Testing macro
'
' Keyboard Shortcut: Ctrl+e
'
    Dim Rng As Range
    Dim WorkRng As Range
    Dim xFile As Variant
    Dim xFileString As String
    On Error Resume Next
    
    xTitleId = "Export Range to CSV file"
    Set WorkRng = Application.Selection
    Set WorkRng = Application.InputBox("Range", xTitleId, WorkRng.Address, Type:=8)
    Application.ActiveSheet.Copy
    Application.ActiveSheet.Cells.Clear
    WorkRng.Copy
    Range("A1").Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
    
    Set xFile = CreateObject("Scripting.FileSystemObject")
    xFileString = Application.GetSaveAsFilename("", filefilter:="Comma Separated Text (*.csv), *.csv")
    Application.ActiveWorkbook.SaveAs Filename:=xFileString, FileFormat:=xlCSV, CreateBackup:=False
    
    Application.ActiveWorkbook.Close
    
End Sub
