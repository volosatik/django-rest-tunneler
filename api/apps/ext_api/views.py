from rest_framework import status, request
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import psycopg2
import os
import netifaces
from api.apps.ext_api.tunnels import tunnels
#.gitinore /env __pycache__ c korne. 
# nastroiki v ini fail 
#from api.apps.ext_api.db_querying import connect_db
#from api.apps.ext_api.scheduler import scheduler
# Ubrat' vsemoduli ne kasaushiesia REST v otdelnie faili ( nik)
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

print(settings.MY_TEST_VARIABLE)
my_scheduler = BackgroundScheduler(daemon=True)
my_scheduler.start()
my_port_list = []
for i in range(35000, 35050):
    my_port_list.append(i)

#my_scheduler.add_job(lambda: my_scheduler.print_jobs(), 'interval', seconds=5)
# Ubrat' vo vnuterennuyu hranilku django(dima)
# config parser (dima) https://cicd-git.megafon.ru/iot/projects/geo/geo-back/-/blob/develop/flask_app/app/config.py 13:

my_local_host = '0.0.0.0'
    #netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
#print(my_local_host)
#3 HERE IS DMZ HOST
my_remote_host = '10.205.28.241'

# Avtorizaciya po api po tokenu
@api_view(["POST", "GET"])
def request_selector(request):
    if request.method == "POST":
        Rawdate_dict = json.loads(json.dumps(request.data))
        if ('uspd_id' in Rawdate_dict) and ('operation' in Rawdate_dict):
            # Slovar' postavit value (Khripunov)
            if Rawdate_dict['operation'] == 'start':
                # pereispolzovat konnect
                # ubrat povtoriashiysia kod podklucheniya v querying
                print(str(Rawdate_dict['uspd_id']))
                str_uspd_id = str(Rawdate_dict['uspd_id'])
                print(type(str_uspd_id)) 
                connection = psycopg2.connect(database="ssp_tmz", user=settings.DB_USERNAME, password=settings.DB_PASSWORD, host='rc-iotp-psql.megafon.ru', port=5000)
                cursor = connection.cursor()
                #SQL_STRING = f"SELECT ip from public.uspds where uspd_id={str_uspd_id}"
                #SQL_STRING = "SELECT ip from public.uspds where uspd_id=(%s)",(str_uspd_id)
                cursor.execute("SELECT ip from public.uspds where uspd_id = (%s)",(str_uspd_id,))
                result = cursor.fetchall()
                print(result)
                device_addr = result[0][0]
                
                if 'name' in Rawdate_dict:
                    creator = Rawdate_dict['name']
                if 'epu_number' in Rawdate_dict:
                    port_number = 80 + Rawdate_dict['epu_number']
                else:
                    port_number = 80     
                to_device = tunnels.TunnelDmz(my_scheduler, settings.USERNAME, settings.PASSWORD, my_local_host, my_remote_host, device_addr, my_port_list, name=creator, private_port= port_number)
                to_device.create()
                return JsonResponse({"we got": request.data, "generated_uri": to_device.return_uri()})
            elif Rawdate_dict['operation'] == 'stop':
                connection = psycopg2.connect(database="ssp_tmz", user=settings.DB_USERNAME, password=settings.DB_PASSWORD, host='rc-iotp-psql.megafon.ru', port=5000)
                str_uspd_id = str(Rawdate_dict['uspd_id'])
                cursor = connection.cursor()
                #SQL_STRING = f"SELECT ip from public.uspds where uspd_id={str(Rawdate_dict['uspd_id'])}"
                cursor.execute("SELECT ip from public.uspds where uspd_id = (%s)",(str_uspd_id,))
                result = cursor.fetchall()
                device_addr = result[0][0]
                for item in tunnels.TunnelDmz:
                    if item.name == Rawdate_dict['name'] and item.private_host == device_addr and item.private_port == (80 + Rawdate_dict['epu_number']) if 'epu_number' in Rawdate_dict else 80:
                        item.destruct()
                        break
                for item in tunnels.TunnelDmz:
                    print(item.name, item.local_port, item.private_host)
                print('teper portov svobodno: ', len(my_port_list))
# v konce request connect zakrit
# ispolzovat' klass postgresa iz https://cicd-git.megafon.ru/iot/projects/geo/geo-back/-/blob/develop/flask_app/Database/postgres.py
# ispolzovat klass logging https://cicd-git.megafon.ru/iot/projects/geo/geo-back/-/blob/develop/flask_app/ErrorHandler/__init__.py
                return JsonResponse({"we got": request.data})
            connection.close()
            # 
        else:
            return JsonResponse({"error": "bad request"})    

# peredelat healthcheck
def healthcheck(request):
    return JsonResponse({"status": "ok"})
