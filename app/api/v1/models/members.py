from app import ma
from . dbmodels import db, BaseModel, UserModel


class Member(BaseModel, UserModel):
    """
        Model for a member
    """
    
    first_name = db.Column(db.String(75), nullable=False)
    middle_name = db.Column(db.String(75), nullable=True)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(75), unique=True, nullable=False)
    phone_number = db.Column(db.String(75), nullable=False)
    

    def __init__(self, first_name, middle_name, last_name, email, phone_number):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

    @staticmethod
    def get_all():
        return Member.query.all()
    
# Member schema
class MemberSchema(ma.ModelSchema):
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number']

# Init schema
member_schema = MemberSchema(strict=True)
members_schema = MemberSchema(many=True, strict=True)
