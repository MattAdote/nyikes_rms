
from app import ma
from . dbmodels import BaseModel, db

class SuperUser(BaseModel):
    """ This class represents the superuser table """
    
    username = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(75), nullable=False)

    
    def __init__(self, username = "", password = ""):
        """initialize with username and supplied password """
        self.username = username
        self.password = password

    @staticmethod
    def get_all():
        return SuperUser.query.all()

# SuperUser schema
class SuperUserSchema(ma.ModelSchema):
    class Meta:
        model = SuperUser
        fields = ['id', 'username', 'password']
# Init schema
superuser_schema = SuperUserSchema(strict=True)
superusers_schema = SuperUserSchema(many=True, strict=True)
