%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
echo on
set QPT_COLOR=False
set QPT_MODE=Debug
set PROMPT=(QPT_VENV) %PROMPT%
cls
"./Python/python.exe" -c "import sys;sys.path.append('./Python');sys.path.append('./Python/Lib/site-packages');sys.path.append('./Python/Scripts');import qpt.run as run"
pause