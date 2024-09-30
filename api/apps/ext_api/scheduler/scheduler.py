from apscheduler.schedulers.background import BackgroundScheduler 
my_scheduler = BackgroundScheduler(daemon=True) 
my_scheduler.start()
