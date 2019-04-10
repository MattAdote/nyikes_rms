from app import ma
from . dbmodels import db, BaseModel

class MembershipClass(BaseModel):
    """
        Model for membership class of member
    """
    
    class_name = db.Column(db.String(75), nullable=False)
    monthly_contrib_amount = db.Column(db.Float(7), nullable=False)
    members = db.relationship('Member', backref='membership_class')    

    initial_attributes = set(['class_name', 'monthly_contrib_amount'])

    def __init__(self, **membership_class_properties):
        for prop in membership_class_properties:
            if prop not in MembershipClass.initial_attributes:
                raise Exception('Received unexpected property: {}'.format(prop))
        

        super().__init__(**membership_class_properties)

    @staticmethod
    def get_all():
        return MembershipClass.query.all()
    
# MembershipClass schema
class MembershipClassSchema(ma.ModelSchema):
    class Meta:
        model = MembershipClass
        fields = ['id', 'class_name', 'monthly_contrib_amount']

# Init schema
membership_class_schema = MembershipClassSchema(strict=True)
member_classes_schema = MembershipClassSchema(many=True, strict=True)
