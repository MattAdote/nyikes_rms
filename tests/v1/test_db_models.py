import unittest
import os
import json, pdb

from .contexts import   create_api_server, db, \
                        BaseModel, UserModel, \
                        SuperUser, superuser_schema, \
                        Member, member_schema, \
                        MembershipClass, member_class_schema

class TestDBModels(unittest.TestCase):
    """This class represents the db models test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.superuser = SuperUser
        self.member = Member
        self.MembershipClass = MembershipClass

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_model_class_db_basemodel_is_child_of_db_model(self):
        """ Test that the BaseModel in dbmodels is a child of db.Model """

        self.assertTrue(issubclass(BaseModel, db.Model), 'BaseModel is not child of SQLAlchemy db.model')
    
    def test_model_class_db_basemodel_has_core_propertes(self):
        """ Test that the BaseModel in dbmodels has core properties """
        properties =['id', 'createdOn', 'createdBy',  'lastModifiedOn', 'lastModifiedBy']

        for prop in properties:
            self.assertTrue(hasattr(BaseModel, prop), 'Missing property: {}'.format(prop))
        
    def test_model_class_db_basemodel_has_core_methods(self):
        """ Test that the BaseModel in dbmodels has core properties """
        methods =['save', 'delete']

        for method in methods:
            self.assertTrue(hasattr(BaseModel, method), 'Missing method: {}'.format(method))
    
    def test_model_class_db_usermodel_has_core_propertes(self):
        """ Test that the UserModel in dbmodels has core properties """
        properties =['public_id', 'password', 'lastLoggedIn', 'lastLoggedOut']

        for prop in properties:
            self.assertTrue(hasattr(UserModel, prop), '\nUserModel is missing property: {}'.format(prop))

    def test_model_class_superuser_is_child_of_sa_basemodel(self):
        """ Test that the class SuperUser is a child of BaseModel """

        self.assertTrue(issubclass(SuperUser, BaseModel), 'SuperUSer is not child of BaseModel')
    
    def test_model_class_superuser_has_core_propertes(self):
        """ Test that the class SuperUser has core properties """
        
        properties =['id', 'createdOn', 'createdBy',  'lastModifiedOn', 'lastModifiedBy']

        for prop in properties:
            self.assertTrue(hasattr(SuperUser, prop), 'Missing property: {}'.format(prop))
    
    def test_model_class_superuser_has_native_propertes(self):
        """ Test that the SuperUser in dbmodels has native properties """
        
        properties =['username', 'password']

        for prop in properties:
            self.assertTrue(hasattr(SuperUser, prop), 'Missing property: {}'.format(prop))
    
    def test_object_superuser_is_instance_of_its_model_class(self):
        """ Test that the SuperUser in dbmodels has native properties """
        
        superuser = SuperUser('test_username')
        self.assertTrue(isinstance(superuser, SuperUser), 'Object not instance of its class')
    
    def test_object_superuser_can_save_to_db(self):
        superuser_data = {
            'username': 'test_username',
            'password': 'test123'
        }
        with self.app.app_context():
            superuser = self.superuser(superuser_data['username'], superuser_data['password'])
            superuser.save()

            res = superuser_schema.jsonify(superuser)

            self.assertIn('id', res.json)
            self.assertTrue(
                all(item in res.json.items() for item in superuser_data.items() ),
                'Missing value in returned output. What was put in not being returned verbatim'
            )

    def test_model_class_member_is_child_of_basemodel(self):
        """ Test that the class Member is a child of BaseModel """

        self.assertTrue(issubclass(Member, BaseModel), 'Member is not child of BaseModel')

    def test_model_class_member_is_child_of_usermodel(self):
        """ Test that the class Member is a child of UserModel """

        self.assertTrue(issubclass(Member, UserModel), 'Member is not child of UserModel')
    
    def test_model_class_member_has_native_propertes(self):
        """ Test that the Member has native properties """
        
        properties = ['first_name', 'middle_name','last_name', 'email', 'phone_number', 'class_id']

        for prop in properties:
            self.assertTrue(hasattr(Member, prop), '\nClass, Member, is missing property: {}'.format(prop))

    def test_object_member_is_instance_of_its_model_class(self):
        """ Test that an instantiated Member object is indeed an instance of the class Member """

        member_properties = {
            "first_name" : "LaKwanza",
            "middle_name": "MajinaZaKati",
            "last_name": "JinaLaMwisho",
            "email": "test@nyikes.org",
            "phone_number" : "0700123456"
        }
        
        obj_member = Member(**member_properties)
        self.assertTrue(isinstance(obj_member, Member), 'Object  not instance of its class')

    def test_object_member_can_save_to_db(self):
        """ Test that the object, Member, can save to db """

        member_properties = {
            "first_name" : "LaKwanza",
            "middle_name": "MajinaZaKati",
            "last_name": "JinaLaMwisho",
            "email": "test@nyikes.org",
            "phone_number" : "0700123456"
        }
        with self.app.app_context():
            # First, create the membership class
            membershipclass_properties = {
                "class_name" : "Test Class A",
                "monthly_contribution_amount": 1000.00
            }
            membership_class = self.MembershipClass(**membershipclass_properties)
            membership_class.save()
            
            # Next, create the member and pass in the backref property (membership_class)
            member = self.member(**member_properties, member_class=membership_class)
            member.save()
            
            # Evaluate the parsed member object
            res = member_schema.jsonify(member)

            self.assertIn('id', res.json)
            self.assertTrue(
                all(item in res.json.items() for item in member_properties.items() ),
                'Missing value in returned output. What was put in not being returned verbatim \
                \nGOT {} \
                \nEXPECTED TO SEE {}'.format(res.json, member_properties)
            )

    def test_model_class_membershipclass_has_native_propertes(self):
        """ Test that the MembershipClass class has native properties """
        
        properties = ['class_name', 'monthly_contribution_amount']

        for prop in properties:
            self.assertTrue(hasattr(self.MembershipClass, prop), '\nClass, MembershipClass, is missing property: {}'.format(prop))
    
    def test_object_membershipclass_is_instance_of_its_model_class(self):
        """ Test that an instantiated MembershipClass object is indeed an instance of the class MembershipClass """

        membershipclass_properties = {
            "class_name" : "Class A",
            "monthly_contribution_amount": 1000.00
        }
        
        obj_membershipclass = MembershipClass(**membershipclass_properties)
        self.assertTrue(isinstance(obj_membershipclass, MembershipClass), 'Object  not instance of its class')
        
    def test_object_membershipclass_can_save_to_db(self):
        """
            Test that the membershipclass object can save to db
        """
        membershipclass_properties = {
            "class_name" : "Class A",
            "monthly_contribution_amount": 1000.00
        }
        with self.app.app_context():
            membershipclass = self.MembershipClass(**membershipclass_properties)
            membershipclass.save()

            res = member_class_schema.jsonify(membershipclass)

            self.assertIn('id', res.json)
            self.assertTrue(
                all(item in res.json.items() for item in membershipclass_properties.items() ),
                'Missing value in returned output. What was put in not being returned verbatim \
                \nGOT {} \
                \nEXPECTED TO SEE {}'.format(res.json, membershipclass_properties)
            )
    
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    
