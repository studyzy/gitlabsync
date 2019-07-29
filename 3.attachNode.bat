@echo off

pushd node1
start cmd /c  gptn.exe attach

pushd ..\node2
start cmd /c gptn.exe attach

pushd ..\node3
start cmd /c gptn.exe attach

pushd ..\node4
start cmd /c gptn.exe attach

pushd ..\node5
start cmd /c gptn.exe attach