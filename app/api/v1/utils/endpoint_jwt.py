import jwt, pdb

from app.api.v1.models import SuperUser, Member

DATE_FORMAT = "{:%Y-%b-%d %H:%M:%S}"

def endpoint_validate_user_token(access_token_payload):
    """
        Validates the user's token contained in the access token

        :returns the decoded token's payload
    """
    err_response = {}
    
    # Check that supplied input is ok
    err_response = endpoint_parse_access_token_payload(access_token_payload)
    if 'headers' in err_response:
        return err_response

    # Get user from db
    try:
        if access_token_payload['super'] == "True":
            user = SuperUser.query.filter_by(username=access_token_payload['username']).first()
        else:
            user = Member.query.filter_by(username=access_token_payload['username']).first()
    except:
        err_response = {
            "status" : 500,
            "error": "Database reports problems getting the associated table. Inform System admin"
        }
        return err_response

    # Return a 400 error if the user is not found in the db
    if user is None:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="username: {} does not exist" '.format(access_token_payload['username'])
        }
        err_response.update({
            "status" : 400,
            "headers": www_authenticate_info
        })
        return err_response

    user_secret = DATE_FORMAT.format(user.lastLoggedOut)
    
    # Decode user's token
    try:
        token_payload = jwt.decode(access_token_payload['user_token'], user_secret)
    except Exception as e:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_token"; '
                                    'error_description="{}" '.format(e)
        }
        err_response = {
            "status" : 401,
            "headers": www_authenticate_info
        }
        
        return err_response
    return token_payload

def endpoint_parse_access_token_payload(access_token_payload):
    """
        Checks the access token for missing or empty values

        :param access_token_payload

        :returns Error on missing or empty values othereise
        returns the access_token_payload
    """
    err_response = {}
    if 'username' not in access_token_payload:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="username missing in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif access_token_payload['username'] == "" or access_token_payload['username'] == None:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="username missing a value in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif 'user_token' not in access_token_payload:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="user_token missing in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif access_token_payload['user_token'] == "" or access_token_payload['user_token'] == None:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="user_token missing a value in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response 
    elif 'super' not in access_token_payload:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="super missing in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif access_token_payload['super'] == "" or access_token_payload['super'] == None:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="super missing a value in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif access_token_payload['super'] not in ['True', 'False']:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="super has incorrect value" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    else:
        return access_token_payload