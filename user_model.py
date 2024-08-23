class Usuario:
    def __init__(self, id: str = "", name: str="", I_time: str="", F_time: str="", user: str="", password: str="", asstec: str="", etapa: str="", workstation: str="", status: str=""):
        self.id = id
        self.name = name
        self.I_time = I_time
        self.F_time = F_time
        self.user = user
        self.password = password
        self.asstec = asstec
        self.etapa = etapa
        self.workstation = workstation
        self.status = status
        
    def to_db(self) -> list:
        return [self.id, self.name, self.I_time, self.F_time, self.user, self.password]

usuario = Usuario()