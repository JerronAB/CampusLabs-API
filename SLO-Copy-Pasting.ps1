$csv = Import-Csv 'C:\Users\jboling0013\OneDrive - KCTCS\temp.csv'

function Wait-ForKey {
    Write-Host "WAITING FOR KEY"
    $read_key = $Host.UI.RawUI.ReadKey()
    if ($read_key.VirtualKeyCode -ne 16) {Wait-ForKey} #shift key
    else {$read_key = 0; Write-Host "KEY PRESSED"}
}

$members = ($csv | Get-Member)
$members | Where-Object {$_.MemberType -EQ 'NoteProperty' -and $_.Name -ne 'ContainerName'} | ForEach-Object {
    #$csv.($_.Name)
    $column_name = $_.Name
    # Load System.Windows.Forms for SendKeys
    Add-Type -AssemblyName System.Windows.Forms
    Wait-ForKey
    [System.Windows.Forms.SendKeys]::SendWait("%{TAB}") #alt+tab
    Start-Sleep -Milliseconds 500
    Write-Host "Outcome: $($_.Name)"
    [System.Windows.Forms.SendKeys]::SendWait("^{f}") #cstrl+f
    Start-Sleep -Milliseconds 500
    [System.Windows.Forms.SendKeys]::SendWait("$column_name")
    for ($i = 0; $i -lt $csv.($_.Name).Length; $i++) {
        $cell_value = $csv.($_.Name)[$i]
        $associated_course = $csv.ContainerName[$i]
        if ($cell_value -ne '' -and $column_name -ne 'ContainerName') {
            Wait-ForKey
            [System.Windows.Forms.SendKeys]::SendWait("%{TAB}")
            Start-Sleep -Milliseconds 500
            Write-Output "$associated_course - $cell_value"
            [System.Windows.Forms.SendKeys]::SendWait("^{f}")
            Start-Sleep -Milliseconds 500
            [System.Windows.Forms.SendKeys]::SendWait("$associated_course")
        }
    }
    Wait-ForKey
    [System.Windows.Forms.SendKeys]::SendWait("%{TAB}")
    Start-Sleep -Milliseconds 500
    [System.Windows.Forms.SendKeys]::SendWait("^{f}")
    [System.Windows.Forms.SendKeys]::SendWait("SAVE")
}
