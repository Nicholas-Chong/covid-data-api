from api.models import Report
import api.scripts.update_data as ud
import twitter.bot as tb

def run():
    print('Starting daily update\n')
    ud.run()

    print('\nSending daily tweet')
    latest_report = Report.objects.latest('date')
    tb.main(latest_report)