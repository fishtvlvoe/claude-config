# spectra archive 垃圾清理：wrap 原生 spectra，archive 後自動偵測並清掉
# @trace injection 灌入整個 knowledge/ 快取目錄清單的異常區塊（本體大小 > 100 行判定為垃圾）。
spectra() {
  if [ "$1" = "archive" ]; then
    local marker
    marker=$(mktemp)
    command spectra "$@"
    local status=$?
    find . -name "spec.md" -newer "$marker" -print0 2>/dev/null | while IFS= read -r -d '' file; do
      _spectra_archive_clean_trace "$file"
    done
    /bin/rm -f "$marker"
    return $status
  else
    command spectra "$@"
  fi
}

_spectra_archive_clean_trace() {
  local file="$1"
  local trace_line
  trace_line=$(grep -n "^<!-- @trace" "$file" 2>/dev/null | head -1 | cut -d: -f1)
  [ -z "$trace_line" ] && return 0

  local total_lines body_lines keep
  total_lines=$(wc -l < "$file")
  body_lines=$((total_lines - trace_line))

  if [ "$body_lines" -gt 100 ]; then
    keep=$((trace_line - 1))
    /usr/bin/head -n "$keep" "$file" > "${file}.tmp"
    mv "${file}.tmp" "$file"
    echo "[spectra-archive-guard] 已清除異常 @trace 垃圾: $file ($total_lines → $(wc -l < "$file") 行)"
  fi
}
