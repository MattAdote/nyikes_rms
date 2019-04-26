import xlsxwriter, io

from app.api.v1.models import   MembershipClass, member_classes_schema

def generate_members_file():
    """
        This generates an MS Excel file to be used to fill in
        records of members to be added to the RMS.

        Returns a dict as follows : {
            "output_file" : the_output_file (type = io.BytesIO),
            "filename" : the_output_filename (type = str),
        }
    """
    num_records = 0
    records_count = 0
    start_table_row = 2
    start_data_row = start_table_row + 1
    
    data_rows = []
    row_data = []

    # First, get the records of the membership classes that have
    # been added to the RMS.
    class_records = get_membership_class_records()
    if 'error' in class_records:
        return class_records
    
    # create workbook
    output_file = io.BytesIO()
    output_filename = 'Nyikes_RMS - Add New Member Records.xlsx'

    workbook = xlsxwriter.Workbook(output_file, {'in_memory': True})
    ws_member_info = workbook.add_worksheet('Member Info')
    ws_membership_class = workbook.add_worksheet('Class info')

    num_records = len(class_records)
    table_membershipclass_cell_range = 'A{}:C{}'.format(start_table_row, start_table_row + num_records)
    table_membershipclass_options = {
        # "data":data_rows,
        "name" : "MembershipClassData",
        "columns" : [
            {"header": "RNo."}, # A
            {"header": "Class"}, # B
            {"header": "Monthly Contribution"} # C
        ],
    }
    ws_membership_class.add_table(table_membershipclass_cell_range, options=table_membershipclass_options)
    # prepare the data to add to the table
    for item in class_records:
        records_count+=1

        row_data.append(records_count)
        row_data.append(item['class_name'])
        row_data.append(item['monthly_contrib_amount'])

        data_rows.append(row_data)

        ws_membership_class.write_row('A{}'.format(start_data_row), data=row_data)
        row_data = []
        start_data_row+=1

    # Create members info table
    member_records_limit = 5
    table_member_cell_range = 'A{}:F{}'.format(start_table_row, start_table_row + member_records_limit)
    table_member_options = {
        "name" : "MemberData",
        "columns" : [
            {"header"   :    "First Name"}, # A
            {"header"   :    "Middle Name"}, # B
            {"header"   :    "Last Name"}, # C
            {"header"   :    "Membership Class"}, # D
            {"header"   :    "Phone Number"}, # E
            {"header"   :    "Email"} # F
        ]
    }
    ws_member_info.add_table(table_member_cell_range, options=table_member_options)

    # add dropdown validation to the rows on the Membershipclass column
    col_to_validate = 'D'
    reference_column = 'B'
    start_at_row = start_data_row - records_count
    stop_at_row = start_data_row - 1
    range_start = start_table_row + 1
    range_stop = range_start + member_records_limit
    for row_num in range(range_start, range_stop):
        ws_member_info.data_validation(
            '{}{}'.format(col_to_validate, row_num), 
            {
                'validate'  :   'list',
                'source'    :   '=\'{}\'!${}${}:${}${}'.format(
                                    ws_membership_class.get_name(), 
                                    reference_column, 
                                    start_at_row,
                                    reference_column,
                                    stop_at_row
                                )
                
            }
        )

    # close the workbook    
    workbook.close()

    # rewind the buffer
    output_file.seek(0)

    return {
        "output_file": output_file,
        "filename": output_filename
    }

def get_membership_class_records():
    """ This returns the membership class records """
    try:
        membership_class = MembershipClass.query.all()
    except:
        return {
            "status":503,
            "error":"Database error encountered when looking up membership class records"
        }
    if not membership_class:
        return {
            "status":404,
            "error":"No membership class records defined"
        }
    
    # load member classes schema
    return member_classes_schema.dump(membership_class).data
