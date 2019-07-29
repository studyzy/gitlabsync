
pushd node1
start cmd /c gptn.exe --noProduce --staleProduce --allowConsecutive
rem .\gptn.exe --noProduce --staleProduce --allowConsecutive

pushd ..\node2
start cmd /c gptn.exe 

pushd ..\node3
start cmd /c gptn.exe 
