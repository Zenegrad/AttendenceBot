from datetime import datetime, timezone, timedelta
import re
import dateparser
from word2number import w2n

def getDatetime(time: str) -> datetime:
  time = time.lower()

  # Checks to see if usr input "in 5 hours", "in 5 minutes" etc. etc.
  if('in' in time):
    time_match = re.search('.+\s+(.*)\s+(.*)', time)
    numerical = 0

    try:
      numerical = int(time_match.group(1))

    # Failed to parse numerical delta for time as an int -- attempt str
    except ValueError:
      numerical = w2n.word_to_num(time_match.group(1))

      print("Failed to convert date delta to int.")

    period = time_match.group(2)
    current_time = datetime.now(timezone.utc)

    if 'hour' in period:
      num_match = re.search('(\w)\shour',time, flags=re.IGNORECASE)
      final_time = current_time - timedelta(hours=num_match.group(1))
        
    if 'days':
      num_match = re.search('(\w)\sday',time, flags=re.IGNORECASE)
      final_time = current_time - timedelta(days=num_match.group(1))

  final_time = dateparser.parse(time)
  

  return final_time


getDatetime('in five hours')