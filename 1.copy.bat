@echo off

rmdir /S /Q node1 node2 node3 node4 node5
echo delete succeed
unzip -q nodes.zip
echo unzip.exe succeed

copy /y  D:\GoProject\src\github.com\palletone\go-palletone\cmd\gptn\gptn.exe node1\.
copy /y  D:\GoProject\src\github.com\palletone\go-palletone\cmd\gptn\gptn.exe node2\.
copy /y  D:\GoProject\src\github.com\palletone\go-palletone\cmd\gptn\gptn.exe node3\.
copy /y  D:\GoProject\src\github.com\palletone\go-palletone\cmd\gptn\gptn.exe node4\.
copy /y  D:\GoProject\src\github.com\palletone\go-palletone\cmd\gptn\gptn.exe node5\.
