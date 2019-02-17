import unittest
import os
import json, pdb

from .contexts import   create_api_server, db, \
                        BaseModel, \
                        SuperUser, superuser_schema

class TestDBModels(unittest.TestCase):
    """This class represents the db models test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.superuser = SuperUser

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
    
    def test_model_class_superuser_is_child_of_sa_basemodel(self):
        """ Test that the BaseModel in dbmodels is a child of db.Model """

        self.assertTrue(issubclass(SuperUser, BaseModel), 'SuperUSer is not child of BaseModel')
    
    def test_model_class_superuser_has_core_propertes(self):
        """ Test that the BaseModel in dbmodels has core properties """
        
        properties =['id', 'createdOn', 'createdBy',  'lastModifiedOn', 'lastModifiedBy']

        for prop in properties:
            self.assertTrue(hasattr(BaseModel, prop), 'Missing property: {}'.format(prop))
    
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

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    