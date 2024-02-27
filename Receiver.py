from http.server import BaseHTTPRequestHandler, HTTPServer
import hashlib
import copy
import re
from collections import deque
from user_agents import user_agent_strings
class MyRequestHandler(BaseHTTPRequestHandler):
    my_dict = {}
    err = 3
    def cons(self, mess, order, length):  
        self.my_dict[order] = mess
        self.err = 5
        if mess == "0x00":
            print(self.my_dict)
            if length == len(self.my_dict):
                result_string = ''.join(self.my_dict[index] for index in sorted(self.my_dict.keys()))
                result_str = result_string[:-4]
                print("Final Message: ",result_str)
                self.err = 0
            else:
                self.err = 1
            self.my_dict.clear()
        return


    def rotate(self, d, n):
    # Get the values of the dict and put them into a deque collection that contains a rotate method
        do = deque(d.values())
        do.rotate(n)  # rotate the values by n
        do = dict(zip(d.keys(), do))  # recombine the keys and values
        return do

    def do_GET(self):
        modified_request = copy.copy(self)
        modified_request.headers = copy.copy(self.headers)
        flag = 0
        temp = str(modified_request.headers['User-Agent'])
        print("temp",temp)
        # Calculate SHA-256 hash of modified request
        request_hash = hashlib.sha256(temp.encode()).hexdigest()
        print("Calculated Hash", request_hash)
        # Check for Cookie header
        print(self.headers)
        if 'Cookie' in self.headers:
            cookies = self.headers['Cookie'].split('; ')
            #print(cookies)
            # Check for _gid value
            for cookie in cookies:
                #print(cookie)
                name, value = cookie.split('=')
                if name == '_gat':
                    if value == '27':
                        print("Covert request")
                        # Look for PHPSESSID value   
                        for cookie in cookies:
                            name, value = cookie.split('=')
                            if name == 'PHPSESSID':
                                print("Request Hash", value)
                                # Check if hash matches PHPSESSID value
                                if value == request_hash:
                                    print("HASH Matched")
                                    flag = 1
                                else:
                                    print("HASH NOT Matched")
                                    self.err = 2
                                    break
                    else:
                        print("Not a Covert request")
                        self.err = 3
                        break
                
            
            for cookie in cookies:
                name, value = cookie.split('=')
                #print(name,value)
                '''if name == '_ga' and flag == 1:
                    ga_value = value.split('.')[-2]
                    # Use the last three digits of _ga to determine the part of the covert message
                    order = int(ga_value[-3:])
                    print("Order: ",order)
                    ga_value = value.split('.')[-1]
                    # Length
                    length_1 = int(ga_value[-3:])
                    print(ga_value, length_1)
                if name == '_gid' and flag == 1:
                    gid_value = value.split('.')[-2]
                    rotation = int(gid_value[-2:])
                    print("Rotation: ",rotation)
                    gid_value = value.split('.')[-1]
                    print(gid_value)
                    # Length
                    length_2 = int(gid_value[-3:])
                    print(gid_value)'''
                if name == '_ga' and flag == 1:
                    ga_parts = value.split('.')
                    order = int(ga_parts[-2][-3:])
                    print("Order: ", order)
                    length_1 = int(ga_parts[-1][-3:])
                    print(ga_parts[-1], length_1)
                if name == '_gid' and flag == 1:
                    gid_parts = value.split('.')
                    rotation = int(gid_parts[-2][-2:])
                    print("Rotation: ", rotation)
                    length_2 = int(gid_parts[-1][-3:])
                    print(gid_parts[-1], length_2)

            if 'User-Agent' in self.headers and flag == 1 and length_1 == length_2:
                print("Total Message Length", length_1)
                cmess = self.headers['User-Agent']
                # Get the values of the dict and put them into a deque collection that contains a rotate method
                rdict = self.rotate(user_agent_strings,rotation)
                omess = rdict[cmess]
                print("original message ", omess)
                self.cons(omess, order, length_1)
    
        else:
            self.err = 4
            
        #No Cookie
        if(self.err == 4):
            self.send_response(204, "OK!!")
        #Not Covert _gat /Fake request
        elif(self.err == 3):
            self.send_response(200, "OK!!")
        #Hash Not matched
        elif(self.err == 2):
            self.send_response(418, "Error!!")
        #Message length mismatch/Full message not received/Loss in message packets
        elif(self.err == 1):
            self.send_response(510, "Error!!")
        #Full Message Received Successful
        elif(self.err == 0):
            self.send_response(201, "OK!!")
        #Part Of message received
        elif(self.err == 5):
            self.send_response(202, "OK!!")
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Starting server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
