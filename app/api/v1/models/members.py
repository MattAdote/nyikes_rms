# project imports
from marshmallow import fields

# local imports
from app import ma
from .dbmodels import db, BaseModel, UserModel

class Member(BaseModel, UserModel):
    """
        Model for a member
    """
    # username = db.Column(db.String(75), unique=True, nullable=True)

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
        
        self.class_name = '' # This is a bug workaround.

        # The bug in question is to do with the Marshmallow serializer.
        # When 'fields' property is set in class Meta, then I am unable
        # to dynamically add the class_name attribute to the MemberSchema.
        # What happens is that the attribute is totally excluded from the
        # schema.(load|dump) output.
        # When I use any of the other options as specified in the online
        # documentation at
        # (https://marshmallow.readthedocs.io/en/3.0/api_reference.html#marshmallow.Schema.Meta)
        # then ALL of the attributes of the instantiated Member class are
        # included in the output.
        # I wasted about 4 hours trying to figure this out on 
        # Fri, 12-Apr-2019 from 6:00 PM EAT || 1800 Hrs GMT +0300
        # The Aha! moment cam about when I perused the documentation at
        # (https://flask-marshmallow.readthedocs.io/en/latest/)
        # and realized that the flask-marshmallow library is probably
        # the culprit in my case in that it does not properly support the
        # native marshmallow behaviour.
        # So this workaround allows me to declare the class_name attribute
        # for the Member class and therefore make it available to the
        # schema for me to dynamically manipulate.
    
    @staticmethod
    def get_all():
        return Member.query.all()
    
# Member schema
class MemberSchema(ma.ModelSchema):
    class_name = fields.Method("set_the_class_name")
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'class_name']

    def set_the_class_name(self, obj_member):
        return  obj_member.membership_class.class_name \
                if obj_member.membership_class is not None and hasattr(obj_member, 'membership_class') \
                else 'Not Assigned'

# Init schema
member_schema = MemberSchema(strict=True)
members_schema = MemberSchema(many=True, strict=True)
