import string
import cgi
import os
import sys
import urllib
import re
from datetime import datetime


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class AnnotationFrameWork:
    

    def __init__(self):
        current_time = str(datetime.now())

        file_input = open(sys.argv[1],'r')
        file_output = open(sys.argv[2] + current_time,'wb')
        self.id_sentence_pairs = map(lambda x: (x.split("\t")[0],x.split("\t")[1].rstrip("\n")),file_input.readlines())

        id_lookup = dict(map(lambda x: (x[1],x[0]),self.id_sentence_pairs))
        
             

        def get_next_sentences():
            return map(lambda x: x[1],self.id_sentence_pairs[0:10])
        
        def refresh_sentences():

            next_ten = self.id_sentence_pairs[0:10]
            self.id_sentence_pairs = self.id_sentence_pairs[10:]
            return map(lambda x: x[1],next_ten)



        class MyHandler(BaseHTTPRequestHandler):



            def do_GET(self):

                if (self.path == "/data"):
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    self.wfile.write("\n".join(get_next_sentences()))

                else:
                    try:
                        
                        f = open(os.curdir + os.sep + self.path)            
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.end_headers()
                    
                        self.wfile.write(f.read())
                        f.close()
                        return
                            
           
            
                    except IOError:
                        self.send_error(404,'File Not Found: %s' % self.path)
     

            def do_POST(self):
            
             #   if self.headers.has_key('content-length'):
             #       length= int( self.headers['content-length'] )
             #       print ( self.rfile.read( length ) )

             #   print self.headers
              #  print self.rfile.readline()
               
                length = int(self.headers.getheader('Content-Length'))
                raw = self.rfile.read(length)

                data = [(urllib.unquote(x.split("=")[0]),urllib.unquote(x.split("=")[1])) for x in raw.split("&")]

                output = ""
                for pair in data:
                    output += pair[0] + "\t" + pair[1]
                    output += "\n"
                output += "\n"
                file_output.write(output)
                file_output.flush()
                

                """                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                             'CONTENT_TYPE':self.headers['Content-Type'],
                     })
               


                for m in form.list:
                    print m.name + "\t" + m.value
"""


                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                
                
                refresh_sentences()
     #          
                return


        try:
            server = HTTPServer(('', 3000), MyHandler)
            print 'started httpserver...'
            server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down server'
            server.socket.close()


            
def main():
    AnnotationFrameWork()

if __name__ == '__main__':
    main()

