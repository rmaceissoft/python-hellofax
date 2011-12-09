from pyhellofax.binder import bind_api_method


class HelloFaxAPI(object):

    def __init__(self, host='www.hellofax.com',
                 api_root='/apiapp.php/v1',
                 email=None,
                 password=None,
                 guid=None):
        self.host = host
        self.api_root = api_root
        self.email = email
        self.password = password
        self.guid = guid


    #Allows send a fax
    send_fax = bind_api_method(
        path = "/Accounts/{guid}/Transmissions",
        method = "POST",
        allowed_param = ["to", 'file']
    )

    #get account details
    account_details = bind_api_method(
        path = "/Accounts/{guid}",
        method = "GET",
    )

    #update account details
    update_account_details = bind_api_method(
        path = "/Accounts/{guid}",
        method = "PUT",
        allowed_param = [] #need to access official API documentation
    )

    #get transmission of account
    transmissions = bind_api_method(
        path = "/Accounts/{guid}/Transmissions",
        method = "GET",
    )

    fax_lines = bind_api_method(
        path = "/Accounts/{guid}/FaxLines",
        method = "GET"
    )

    find_fax_numbers = bind_api_method(
        path = "/AreaCodes",
        method= "GET",
        allowed_param= ["statecode"]
    )



    



  