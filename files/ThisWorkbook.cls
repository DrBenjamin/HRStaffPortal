Private Sub Workbook_Open()

    ' Show Userform
    'UserForm1.Show
    
    ' Formatting columns containing date data as date in all Worksheets
    For Each ws In ActiveWorkbook.Worksheets
        With ws
            For i = 1 To 99
                If InStr(1, .Cells(1, i).Value, "DATE", vbTextCompare) > 0 Then
                    rrow = 2
                    Do While Len(Trim(.Cells(rrow, i).Value)) > 0
                        .Cells(rrow, i).NumberFormat = "dd.mm.yyyy"
                        .Cells(rrow, i).Value = .Cells(rrow, i).Value
                        rrow = rrow + 1
                    Loop
                End If
                If InStr(1, .Cells(1, i).Value, "YEAR", vbTextCompare) > 0 Then
                    rrow = 2
                    Do While Len(Trim(.Cells(rrow, i).Value)) > 0
                        .Cells(rrow, i).NumberFormat = "yyyy"
                        .Cells(rrow, i).Value = .Cells(rrow, i).Value
                        rrow = rrow + 1
                    Loop
                End If
            Next
        End With
    Next

End Sub
