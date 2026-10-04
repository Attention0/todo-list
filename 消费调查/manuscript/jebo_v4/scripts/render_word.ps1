$ErrorActionPreference = 'Stop'
$jeboRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    foreach ($stem in @('JEBO_manuscript_v4', 'JEBO_supplement_v4', 'JEBO_Highlights_v4')) {
        $outDir = Join-Path $jeboRoot ('qa/final/' + $stem)
        [IO.Directory]::CreateDirectory($outDir) | Out-Null
        $doc = $word.Documents.Open((Join-Path $jeboRoot ($stem + '.docx')), $false, $true)
        try {
            $doc.Repaginate()
            $doc.ExportAsFixedFormat((Join-Path $outDir ($stem + '.pdf')), 17)
            Write-Output ($stem + ': ' + $doc.ComputeStatistics(2) + ' pages')
        } finally { $doc.Close(0) }
    }
} finally {
    $word.Quit()
    [Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null
}
