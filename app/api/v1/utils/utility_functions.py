allowed_content_types = ['application/x-www-form-urlencoded', 'application/json', 'multipart/form-data']

def validate_request_data(request_data, required_fields_checklist):
    """
        This checks that required data is present and not empty.
        Also, non-required data is checked to see if present
        and not empty.
    """
    # request_data = [  {
    #                       "required_field_1": "datatype", 
    #                       "required_field_1": "datatype"
    #                   },
    #                   {
    #                       "other_field_1" : "datatype"
    #                   }
    #               ]
    required_fields = request_data[0]
    missing_fields = []
    empty_fields = []

    for field in required_fields_checklist:
        if field not in required_fields:
            missing_fields.append(field)

        elif request_data[0][field] == "" or request_data[0][field] == '""':
            empty_fields.append(field)

    if len(missing_fields) > 0:
        response = {
            "status": '400',
            "error": 'Required fields missing: ' + ',  '.join(missing_fields)
        }
        return response
    elif len(empty_fields) > 0:
        response = {
            "status": '400',
            "error": 'Required field(s) empty: ' + ',  '.join(empty_fields)
        }
        return response
    else:
        # process the non required fields and get those that are not empty
        # first, return if there were no non required fields
        if len(request_data) == 1:
            return request_data[0]
        elif len(request_data) == 2:
            non_empty = {}
            for field in request_data[1]:
                if request_data[1][field] != "" and request_data[1][field] != '""':
                    non_empty.update({field : request_data[1][field]})

            return {**request_data[0], **non_empty}

def validate_route_param(route_param):
    """ Checks that the supplied route parameter can be converted to an int """
    try:
        type(int(route_param)) == int
    except:
        response = {
            "status": 400,
            "error" : 'Invalid route parameter'
        }
        return response
    else:
        return int(route_param)

def invalid_param(supplied_data, valid_data):
    """Returns the invalid paramters that have been supplied in the request"""

    invalid_param = []
    response = {}

    # first, check that some data has been supplied
    data = check_is_empty(supplied_data)
    if 'error' in data:
        return data

    # some data is present, get the invalid parameters
    for field in data:
        if field not in valid_data:
            invalid_param.append(field)

        response = {
            "status": 400,
            "error": 'Invalid parameter(s): {}'.format(invalid_param)
        }
    return response


def check_is_empty(supplied_data):
    """Returns an error message if supplied data is empty, else, returns the data received"""

    if supplied_data is None or not supplied_data:
        response = {
            "status": 400,
            "error": "No data provided"
        }
        return response
    else:
        return supplied_data

def parse_request(req):
    """
    Validates the request for correct content_type.\n
    Returns error if content_type invalid else\n
    returns the data contained in the request
    
    """
    if req.content_type not in allowed_content_types:
        if allowed_content_types[2] not in req.content_type:
            response = {
                'status': 400,
                'error': 'Invalid Content_Type request header'
            }
            return response
        else:
            # we have multipart/form-data content-type
            if req.form != None and req.form != '':
                # get the form data as dict
                data = req.form.to_dict()
            else:
                # no data with request.
                data = {}
    elif req.args:
        # we're dealing with 'application/x-www-form-urlencoded'
        raw_data = req.args
        data = raw_data.to_dict()
    else:
        # content-type is ok and no url data has been set, try for json data present
        # if content-type is application/json but no data is supplied
        # then the exception will be raised otherwise if the content-type is
        # 'application/x-www-form-urlencoded' but no data is supplied
        # then the exception will not be raised
        try:
            data = req.json
        except:
            response = {
                'status': 400,
                'error': "Request data invalid! No JSON data!"
            }
            return response
    
    if data is None:
        return {
            'status': 400,
            'error': "Request invalid! No data supplied!"
        }
    else:
        # all ok, so return the data
        return data

def endpoint_error_response(request_data, processed_data):
    """ 
        Returns error response depending on whether or not
        invalid parameters were found in the request data
    """
    if 'error' in processed_data:
        # some required fields are not present or are empty
        return processed_data
    else:
        # invalid parameters present in request data
        # get the invalid parameters and return
        response = invalid_param(request_data, processed_data)

        return response
