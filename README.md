# gmail_delete
A python-based iterative bulk gmail email deleter for stupendously large numbers of emails.

I had a gmail account pointed simultaneously to the LKML and FreeBSD developer mailing lists, and it accumulated over 1 million emails. Gmail's web interface is downright incapable when it comes to deleting more than 10,000 or so emails, and bulk deletions much larger than that over a single IMAP session will also fail. This python script handles that situation, permitting you to delete all emails in an account before a specified date.

this script has no arguments, but has mutable parameters at the top which control its behavior. A beginning date is required which specifies some date where the number of emails before that date is less than 10,000. the script then iteratively deletes emails from that date to the specified end date, while reconnecting in case of imap session error. 

This script takes a LONG time to delete 100,000s of emails, so be patient. This script is also only designed for Gmail. the process of bulk deletion via IMAP should be much simpler for other types of email accounts.
