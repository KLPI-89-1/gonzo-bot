class Show(object):
    def __init__(self, name, dj, day, starttime, endtime):
        self.name = name
        self.dj = dj
        self.day = day
        self.starttime = starttime
        self.endtime = endtime
        self.skip = False

backup_list = [Show("Jacky J's Corner", "Jacky J", "Tuesday", "17:00", "18:00"), Show("Vaporwave", "Loquat", "Tuesday", "18:00", "19:00", Show("Mom's Basement", "Bear", "Wednesday", "13:00", "14:00"), Show("One Hot Hour", "RHCP", "Wednesday", "17:00", "18:00"), Show("New Wave Wednesday", "Boingoloid", "Wednesday", "20:00", "22:00"), Show("Sounds of the Sea", "Big Boss", "Thursday", "13:00", "14:00"), Show("Soulistic Hour", "Tee", "Thursday", "16:00", "17:00"), Show("Sounds from the Outlet", "RNG", "Thursday", "20:00", "22:00"), Show("The Cure", "Remedy", "Friday", "14:00", "15:00"), Show("Peach's Picks", "Peach", "Saturday", "10:00", "11:00")]