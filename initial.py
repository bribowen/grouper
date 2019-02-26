class Project:
    def __init__(self, id, poster, name, ptype, description):
        self.id = id
        self.poster = poster
        self.name = name
        self.type = ptype
        self.description = description

class Profile:
    def __init__(self, id, fname, lname, persona, email, prcontact, interests, professor):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.persona = persona
        self.email = email
        self.prcontact = prcontact
        self.interests = interests
        self.professor = professor

