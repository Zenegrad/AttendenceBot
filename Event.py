import datetime

class Event():

    title = description = None

    time    : datetime = None
    accepted: set = set()
    declined: set = set()
    tenative: set = set()
    on_time : set = set()
    late    : set = set()

    def __init__(self, *args, **kwArgs) -> None:
        if(kwArgs):
            for kw in kwArgs.keys:
                match kw:
                    case 'accepted':
                        self.accepted = kwArgs[kw]
                    case 'declined':
                        self.declined = kwArgs[kw]
                    case 'tenative':
                        self.tenative = kwArgs[kw]
                    case 'on_time':
                        self.on_time = kwArgs[kw]
                    case 'late':
                        self.late = kwArgs[kw]
                    case 'time':
                        self.time = kwArgs[kw]
                    case 'title':
                        self.title = kwArgs[kw]
                    case 'description':
                        self.description = kwArgs[kw]


                    