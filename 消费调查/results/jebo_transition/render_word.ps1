$ErrorActionPreference = 'Stop'
$jeboRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../manuscript/jebo_v1'))
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    foreach ($stem in @('JEBO_manuscript_v1', 'JEBO_supplement_v1')) {
        $outDir = Join-Path $jeboRoot ('qa/final/' + $stem)
        [IO.Directory]::CreateDirectory($outDir) | Out-Null
        $docPath = Join-Path $jeboRoot ($stem + '.docx')
        $pdfPath = Join-Path $outDir ($stem + '.pdf')
        $doc = $word.Documents.Open($docPath, $false, $true)
        try {
            $doc.Repaginate()
            $doc.ExportAsFixedFormat($pdfPath, 17)
            Write-Output ($stem + ': ' + $doc.ComputeStatistics(2) + ' pages')
        } finally { $doc.Close(0) }
    }
} finally {
    $word.Quit()
    [Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null
}
