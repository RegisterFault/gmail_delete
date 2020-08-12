#!/bin/python
# Author: Travis James <registerfault@gmail.com>
# pulled and heavily modified from a stack overflow answer by user radtek
# https://stackoverflow.com/a/21997753
#
# this program requires you to enable "allow less secure apps" in gmail 
# settings, is currently found at https://myaccount.google.com/lesssecureapps

from datetime import datetime, timedelta
import imaplib
import time

# Do we want to mark and expunge \Trash?
# Currently, Gmail's web interface does this better than imaplib, and Gmail
# supposedly purges every 30 days anyways, so default is False
empty_trash = False

# backoff time for reconnection, to be polite with gmail
backoff_time = 15

# datetime object representing date to begin iterative deleting with. THIS STILL
# DELETES ALL EMAILS BEFORE THIS DATE and if this date is picked poorly, might
# end up with an imap session that tries to delete too much and crashes.
from_date = datetime(2016, 6, 1)

# datetime object representing date to end iterative deleting with. by the time
# we are done, all emails before this date will be deleted.
to_date = datetime.today() - timedelta(weeks=8)

# number of days between iterations. adjust this so that on average, you are
# dealing with <10,000 emails per iteration.
iter_period = 7

# standard gmail password credentials
email = "example@gmaildomain.com"
password = "PlaceholderPassword"

from_str = from_date.strftime("%d-%b-%Y")
to_str   = to_date.strftime("%d-%b-%Y")
print "Iteratively deleting emails from before {0} to before {1}".format(from_str, to_str)
cur_date = from_date

while cur_date <= to_date:
    try:
        print "Establishing connection..."
        m = imaplib.IMAP4_SSL("imap.gmail.com")
        
        print "Logging into mailbox..."
        m.login(email, password)

        res = m.select('[Gmail]/All Mail')
        print "Selecting [Gmail]/All Mail: {0}".format(res)

        datestr = cur_date.strftime("%d-%b-%Y")
        print "Searching before {0}".format(datestr)
        typ, data = m.search(None, '(BEFORE {0})'.format(datestr))

        if data != ['']:  # if not empty list means messages exist
            num_msg = data[0].split()[-1]  # last msg id in the list
            print num_msg, "messages found"
            
            print "Removing..."
            # move to trash
            m.store("1:{0}".format(num_msg), '+X-GM-LABELS', '\\Trash')  
            print "Deleted {0} messages".format(num_msg)
            
            if empty_trash == True:
                res = m.select('[Gmail]/Trash')
                print "Entering [Gmail]/Trash: {0}".format(res)  
                print "flagging all trash as \\Deleted"
                m.store("1:*", '+FLAGS', '\\Deleted')  
                print "expunging"
                m.expunge()  # not need if auto-expunge enabled
        else:
            print "Nothing to remove."

        print("Closing mailbox...")
        m.close()
        
        print("Logging out...")
        m.logout()
        
        #iterate date
        time.sleep(backoff_time)
        if (to_date == cur_date):
            break
        cur_date += timedelta(iter_period)
        if (cur_date > to_date):
            cur_date = to_date
    # Gmail IMAP sessions like to just randomly... fail from time to time.
    # This will also happen immediately if you tell imaplib to delete too many
    # emails, usually around the 10,000-ish mark
    except imaplib.IMAP4_SSL.abort:
        print ">>>SESSION FAILED<<<"
        time.sleep(backoff_time*2)
        continue

print "All Done."
