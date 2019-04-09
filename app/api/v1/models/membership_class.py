from app import ma
from . dbmodels import db, BaseModel

class MembershipClass(BaseModel):
    """
        Model for membership class of member
    """
    
    class_name = db.Column(db.String(75), nullable=False)
    monthly_contribution_amount = db.Column(db.Float(7), nullable=False)
    members = db.relationship('Member', backref='member_class')    

    def __init__(self, class_name, monthly_contribution_amount):
        self.class_name = class_name
        self.monthly_contribution_amount = monthly_contribution_amount

    @staticmethod
    def get_all():
        return MembershipClass.query.all()
    
# MembershipClass schema
class MembershipClassSchema(ma.ModelSchema):
    class Meta:
        model = MembershipClass
        fields = ['id', 'class_name', 'monthly_contribution_amount']

# Init schema
member_class_schema = MembershipClassSchema(strict=True)
member_classes_schema = MembershipClassSchema(many=True, strict=True)
