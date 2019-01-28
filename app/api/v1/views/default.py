from flask import Blueprint, request, jsonify, make_response


# Define blueprint for meetup view
default_view_blueprint = Blueprint('default_view', '__name__')

@default_view_blueprint.route('/', methods=['GET'])
def default():
    """ The default view for the API Server"""
    
    response = {
        'status': 200,
        'data': 'Nyikes REST API Web server'
    }

    return make_response(jsonify(response), response['status'])
