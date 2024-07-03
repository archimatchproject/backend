import datetime


TIME_SLOT_CHOICES = [
    (datetime.time(hour=8, minute=0), "08:00"),
    (datetime.time(hour=8, minute=30), "08:30"),
    (datetime.time(hour=9, minute=0), "09:00"),
    (datetime.time(hour=9, minute=30), "09:30"),
    (datetime.time(hour=10, minute=0), "10:00"),
    (datetime.time(hour=10, minute=30), "10:30"),
    (datetime.time(hour=11, minute=0), "11:00"),
    (datetime.time(hour=11, minute=30), "11:30"),
    (datetime.time(hour=12, minute=0), "12:00"),
    (datetime.time(hour=12, minute=30), "12:30"),
    (datetime.time(hour=13, minute=0), "13:00"),
    (datetime.time(hour=13, minute=30), "13:30"),
    (datetime.time(hour=14, minute=0), "14:00"),
    (datetime.time(hour=14, minute=30), "14:30"),
    (datetime.time(hour=15, minute=0), "15:00"),
    (datetime.time(hour=15, minute=30), "15:30"),
    (datetime.time(hour=16, minute=0), "16:00"),
    (datetime.time(hour=16, minute=30), "16:30"),
    (datetime.time(hour=17, minute=0), "17:00"),
]

ARCHITECT_REQUEST_STATUS_CHOICES = [
    ("Accepted", "Accepted"),
    ("Refused", "Refused"),
    ("Awaiting Demo", "Awaiting Demo"),
    ("Awaiting Decision", "Awaiting Decision"),
]
