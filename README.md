Описание АПИ v1
Принимаем json с полями
- "name": Имя того кто хочет стучаться в устройство
- "uspd_id": uspd_id в нашей базе
- "operation":"start" или "stop"
- "epu_number": номер слейва ЭПУ, при отсутствии параметра пробросит на 80 порт ( веб самого УСПД) так же как и при номере слейва 0 


Апи доступно на 9000 порту на РЦ  -- msk-iot-rgate02.megafon.ru:9000/api/
