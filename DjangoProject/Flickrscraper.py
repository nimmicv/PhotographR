import urllib2,json, urllib, csv

from xml.dom import minidom

#fo1 = open("new_data.json", "w")
#fo1.close()
#fo2 = open("image_data.csv", "w")
#fo2.close()


def getallphotos(tag):
    url = "http://api.flickr.com/services/rest/?method=flickr.photos.search"
    api_key = '252a5c43c2db9c7ec3b0f0aa31ce821b'

    print url

    req = urllib2.Request(url)
    data = {'api_key': api_key,
            'tags': tag,
            'format': 'json'}

    print req.get_full_url()

    try:
        conn = urllib2.urlopen(url, urllib.urlencode(data))
        try:
            response = conn.read()
        finally:
            conn.close()
    except urllib2.HTTPError as error:
            response = json.loads(error.read())

    print response

    with open('data.json', 'w') as outfile:
        json.dump(response, outfile)

    file = open('data.json')
    print type(file)
    data = json.load(file)
    print type(data)
    file.close()


    new_len = len(data)-1
    stripped_data = data[14:new_len]#this contains the first json

    with open('data.json', 'w') as outfile:
        json.dump(stripped_data, outfile)#first json  written into the file

def getExifs(tag):
    file = open('data.json')
    print type(file)
    data = json.load(file)
    print type(data)
    file.close()

    json_stripped_data = json.loads(data)
#    print(json_stripped_data['photos']['photo'])
    i = 5 #NUM of results
    new_response='{\"photos\":'
    while i > 0:
        for photo in json_stripped_data['photos']['photo']:
            print i
            if i == 0:
                break
            idd = photo['id']
            #http://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
            photo_url= "http://farm"+str(photo['farm'])+".staticflickr.com/"+str(photo['server'])+"/"+str(idd)+"_"+str(photo['secret'])+".jpg"
            print photo_url
            print idd
            new_url = "http://api.flickr.com/services/rest/?method=flickr.photos.getExif&api_key=97b05a45e3c038c3d1b520d0ef4d7594&photo_id="+idd+"&format=json&nojsoncallback=1"
            api_key = '252a5c43c2db9c7ec3b0f0aa31ce821b'

            print new_url

            new_data = {'api_key': api_key,
                        'tags': tag,
                        'format': 'json'}

            try:
                conn = urllib2.urlopen(new_url, urllib.urlencode(new_data))
                try:
                    new_response = conn.read()
                    #size = len(new_response_temp)-1
                    #new_response += new_response_temp+", "
                    print new_response
                finally:
                    conn.close()
            except urllib2.HTTPError as error:
                new_response = json.loads(error.read())

            print new_response
            json_stripped_data_1 = json.loads(new_response)
           # print json_stripped_data_1['photo']
            ISOvalue=''
            Aperture=''
            Exposure=''
            if json_stripped_data_1.get('photo'):
                for exif in json_stripped_data_1['photo']['exif']:
                        #print exif['tag']
                    if exif['tag'] == "ISO":
                        ISOvalue = exif['raw']['_content']
                        print "ISO is " + ISOvalue
                    if exif['tag'] == 'FNumber':
                        Aperture = exif['raw']['_content']
                        print "Aperture is " + Aperture
                    if exif['tag'] == 'ExposureTime':
                        Exposure = exif['raw']['_content']
                        print "Exposure is " + Exposure
                    if ISOvalue != '' and Aperture != '' and Exposure != '':
                        break
                combined = idd +","+ISOvalue+","+Aperture+","+Exposure+","+photo_url
                print combined
                with open('image_data.csv', 'a') as csvfile:
                    spamwriter = csv.writer(csvfile)
                    spamwriter.writerow((idd, ISOvalue, Aperture, Exposure, photo_url))
                csvfile.close()

                i -= 1

    #size = len(new_response)-3
    #new_response = new_response[1:size]+'}'
    with open('new_data.json', 'a') as new_outfile:
            json.dump(new_response, new_outfile)


    file.close()
    new_outfile.close()

def getSimilarPhotos(photoid, tag):
    with open('image_data.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
             print ', '.join(row)


#def getSimilarPhotos(photoid, tag):
#    #we will first get exif of the selected photo, then search in the file for similar photos
#    file = open('new_data.json')
#    print type(file)
#    #data_raw = file.readline().replace('""', '')
#    data = json.load(file)
#    #data = json.loads(data_raw)
#    print data
#    #print type(data)
#    file.close()
#
#    json_stripped_data = json.loads(data)
#    for exif in json_stripped_data['photo']['exif']:
#        print exif
#        print exif['tag']
#        if exif['tag'] == "ISO":
#            ISOvalue = exif['raw']['_content']
#            print "ISO is " + ISOvalue
#        #str = "{\"photo\": [{ \"id\": \""+id+", \"ISO\": "+iso+",\"aperture\": "+aperture+",\"exposure\": "+exposure+" },"
#        #    iso=photo[]
#
#
#
#    #xmldoc = minidom.parse(response)
#
#    #photoIDList = xmldoc.getElementsByTagName('photo id')
#
#    #for p in photoIDList :
#    #    ph = p

#CALLING HERE
#getallphotos('golden gate')
#getExifs('golden gate')
getSimilarPhotos('10479694713','golden gate')