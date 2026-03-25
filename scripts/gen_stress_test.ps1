$out = 'c:\Users\Administrator\CAT\catgui\examples\stress_test.cat'
$types = @('i8','i16','i32','i64','u8','u16','u32','u64','f32','f64','bool')
$instr = @('add','sub','mul','div','mod','and','orr','xor','shl','shr')
$kws   = @('local','global','const')
$dirs  = @('@inline','@static','@packed')

$sb = [System.Text.StringBuilder]::new()
$null = $sb.AppendLine('# Auto-generated stress test - valid CAT source for benchmarks')
$null = $sb.AppendLine('# Regenerate: node scripts/gen_stress_test.js OR pwsh scripts/gen_stress_test.ps1')
$null = $sb.AppendLine('')

for ($i = 0; $i -lt 1200; $i++) {
    $ty  = $types[$i % $types.Count]
    $ins = $instr[$i % $instr.Count]
    $kw  = $kws[$i % $kws.Count]
    $d   = $dirs[$i % $dirs.Count]
    $null = $sb.AppendLine("# func_$i type=$ty op=$ins")
    $null = $sb.AppendLine($d)
    $sig = 'fn func_' + $i + '(a: ' + $ty + ', b: ' + $ty + ') -> ' + $ty + ' {'
    $null = $sb.AppendLine($sig)
    $body1 = '    ' + $kw + ' result: ' + $ty + ' = 0'
    $null = $sb.AppendLine($body1)
    $body2 = '    ' + $ins + ' result, a, b'
    $null = $sb.AppendLine($body2)
    $null = $sb.AppendLine('    ret result')
    $null = $sb.AppendLine('}')
    $null = $sb.AppendLine('')
}

for ($i = 0; $i -lt 50; $i++) {
    $null = $sb.AppendLine('type Vec' + $i + ' { x: f32  y: f32  z: f32  w: f32 }')
}

$null = $sb.AppendLine('')
$null = $sb.AppendLine('fn main() -> i32 { ret 0 }')

[System.IO.File]::WriteAllText($out, $sb.ToString())

$lc = (Get-Content $out).Count
$bc = (Get-Item $out).Length
Write-Host "Generated: $out"
Write-Host "  Lines:   $lc"
Write-Host "  Bytes:   $bc"
