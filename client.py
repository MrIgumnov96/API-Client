import requests
import json

class Client:

    # Definition of the construtor
    def __init__( self, server_address, password ):
        self.__server_address = server_address
        self.__password = password

    # Function returns True if it was possible to
    # retrieve the response from the server.
    def can_connect( self ):
        try:
            req = requests.get( self.__server_address )
            if req.status_code == 200:
                print( req.text )
                return True

            return False

        except:
            print( "An exception occurred when made an attemp to send a request to a server. The server may not be running." )
    
    def print_records( self, records_raw_list ):
        records_lists = json.loads( records_raw_list )
        for records in records_lists:
            print( records )

    def print_page_options( self, records_raw_list, links_list ):
        print( "Page Options" )
        
        idx = 0
        for link in links_list[1:]:   
            for key, value in link.items():  
                idx = idx + 1
                print( "Enter digit {} to proceed to the {} page.".format( idx, key ) )

        print( "Enter digit 5 to list records." )
        print( "Enter digit 6 to return to Main Menu." )

        inpt = self.get_numeric_input()
        

        if inpt >= 1 and inpt <= 4:
            link_list = links_list[ inpt ].values()
            for link in link_list:
                if str( link ) == 'None':
                    self.main_menu()
                else:
                    self.go_to_page( link )

        if inpt == 5:
            self.print_records( records_raw_list )
            self.print_page_options( records_raw_list, links_list )

        if inpt == 6:
            self.main_menu()

    def go_to_page( self, page_address ): 
        req = requests.get(
            page_address,
            headers = { 'api_key': self.__password } )

        if req.status_code == 200:
            dict = req.json()
            print ( "We are at page: {}".format( page_address ) )
            self.print_page_options( dict[ 'records' ], dict[ 'links' ] )

        else:
            print( "It was not possible to open the page, the following error occured: {}".format( req.status_code  ) )

    def get_campaign_statistics( self ):
        self.go_to_page( self.__server_address + '/campaign_statistics' )
            
    def get_campaigns( self ):
        self.go_to_page( self.__server_address + '/campaigns' )

    def get_creatives( self ):
        self.go_to_page(  self.__server_address + '/creatives' )
        
        
    def main_menu( self ):
        print( "Main Menu" )
        print( "Enter one of the following options:" )
        print( "1 to get to campaign statistics" )
        print( "2 to get to campaigns" )
        print( "3 to get to creatives" )
        print( "4 to exit from program" )

        inpt = self.get_numeric_input()

        if inpt == 1:
            self.get_campaign_statistics()
        elif inpt == 2:
            self.get_campaigns()
        elif inpt == 3:
            self.get_creatives()
        elif inpt == 4:
            print( "Good bye" )
            exit()
        else:
            print('Option does not exist.')
            self.main_menu()
    
    def get_numeric_input( self ):
        inpt = input()
        if inpt.isnumeric():
            return int( inpt )
        
        print( "Input is not numeric. Please enter numeric value." )
        return self.get_numeric_input()
            
client = Client( "http://127.0.0.1:5000/", 'uHL6FHwsIXgk8ke3uAdNNg' )

if client.can_connect():
    client.main_menu()