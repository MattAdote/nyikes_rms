from app import ma
from . dbmodels import db, BaseModel, UserModel

class Member(BaseModel, UserModel):
    """
        Model for a member
    """
    
    class_id = db.Column(db.Integer, db.ForeignKey('membership_class.id'))
    
    first_name = db.Column(db.String(75), nullable=False)
    middle_name = db.Column(db.String(75), nullable=True)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(75), unique=True, nullable=False)
    phone_number = db.Column(db.String(75), nullable=False)

    initial_attributes = set(['first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'membership_class'])

    def __init__(self, **member_properties):
        for prop in member_properties:
            if prop not in Member.initial_attributes:
                raise Exception('Received unexpected property: {}'.format(prop))
        super().__init__(**member_properties)

        # self.first_name = member_properties['first_name']
        # self.middle_name = member_properties['middle_name']
        # self.last_name = member_properties['last_name']
        # self.email = member_properties['email']
        # self.phone_number = member_properties['phone_number']
    
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
