from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response

import urllib
import urllib2
import urlparse
import httplib2
import json
from urlparse import parse_qsl, urlparse
from urllib import urlencode


def connect_to_service(request):
    return render_to_response('singly.html')

def singly_authorize(request):
    SINGLY_ACCESS_TOKEN_URL = 'https://api.singly.com/oauth/access_token'
    SINGLY_PROFILES = 'https://api.singly.com/v0/profiles'

    SINGLY_PHOTOS= 'https://api.singly.com/v0/types/photos'
    SINGLY_CHECKINS = 'https://api.singly.com/v0/types/checkins'
    SINGLY_STATUS = 'https://api.singly.com/v0/types/statuses'

    # Get singly access code
    code = request.GET.get("code")
    print("OAuth code is %s" % (code, ))

    post_params = {
        'client_id' : settings.SINGLY_CLIENT_ID,
        'client_secret' : settings.SINGLY_CLIENT_SECRET,
        'code': code
        }
    post_data = urllib.urlencode(post_params)

    print "Calling %s with params %s" % (SINGLY_ACCESS_TOKEN_URL, post_data)
    request2 = urllib2.Request(SINGLY_ACCESS_TOKEN_URL, post_data)
    response2 = urllib2.urlopen(request2)

    access_token_data = response2.read()
    print("Access token response data is %s" % (access_token_data, ))

    access_token_json = json.loads(access_token_data)
    access_token = access_token_json['access_token']
    print("Access token is %s" % (access_token, ))

    get_params = {
        'data' : 'true',
        'access_token' : access_token
        }

    get_data = urllib.urlencode(get_params)

    #1 Fetch Profile Data
    api_request_profiles = SINGLY_PROFILES + '?access_token=' + access_token
    api_request_photos = SINGLY_PHOTOS + '?access_token=' + access_token
    api_request_checkins = SINGLY_CHECKINS + '?access_token=' + access_token
    api_request_status = SINGLY_STATUS + '?access_token=' + access_token


    ''' PHOTOS '''
    #2 Make HTTP Requests for checkin data
    request_photos = urllib2.Request(api_request_photos)
    response_photos = urllib2.urlopen(request_photos)
    
    #3 Read checkin data from HTTP Request
    photos = response_photos.read()
    
    #4 Load checkins into json parser
    photo_json = json.loads(photos)

    '''
    [
    {
        "date": "date",
        "source": "source",
        "link": "link",
        "type": "type",
        "numb_likes": "numb_likes",
        "image_location": "image_location",
        "width": "width",
        "height": "height"
[
"oembed": {
  "type": "photo",
  "height": 720,
  "width": 720,
  "url": "https://fbcdn-photos-a.akamaihd.net/hphotos-ak-ash4/427860_3111729283648_1576860066_32083208_684623008_s.jpg",
  "provider_name": "facebook",
  "provider_url": "http://www.facebook.com/photo.php?fbid=3111729283648&set=a.3111729203646.2113918.1576860066&type=1",
  "author_name": "Beau Gunderson"
}
]
    
    '''


    print photo_json[0]['oembed']
    print photo_json[0]['at']

    photos_array = []
    count = 0
    while count < len(photo_json):
        oembed_obj = photo_json[count]['oembed']
        date_obj = photo_json[count]['at']
        
        data = {
            #'date' : date_obj,
            'source' : oembed_obj['provider_name'],
            'type' : oembed_obj['type'],
            'link' : oembed_obj['provider_url'],
            'image_location' : oembed_obj['url'],
            'height' : oembed_obj['height'],
            'width' : oembed_obj['width'],
        }
        photos_tuple = [date_obj, data]
        photos_tuple.sort()
        photos_array.append(photos_tuple)
        count += 1

    scrubbed_photo_data = json.JSONEncoder().encode(photos_array)
    #print "BEGIN JSON"
    #print scrubbed_data

    ''''

    #3 Write profile data to file
    sfile = open(settings.FILE_WRITE_PATH + 'julia-photos.json-v2', 'w')
    sfile.write(photos)
    #sfile.write(str(photo_json))
    #sfile.write(json.dumps(photos)
    sfile.close()

    #2 Make HTTP Re`14yyquests for checkin data
    request_checkins = urllib2.Request(api_request_checkins)
    response_checkins = urllib2.urlopen(request_checkins)
    
    #3 Read checkin data from HTTP Request
    checkins = response_checkins.read()
    
    #4 Load checkins into json parser
    checkin_json = json.loads(checkins)

    #3 Write profile data to file
    sfile1 = open(settings.FILE_WRITE_PATH + 'julia-checkins-v2.json', 'w')
    sfile1.write(json.dumps(checkin_json))
    sfile1.close()

    #2 Make HTTP Requests for checkin data
    request_statuses = urllib2.Request(api_request_status)
    response_statuses = urllib2.urlopen(request_statuses)
    
    #3 Read checkin data from HTTP Request
    statuses = response_statuses.read()
    
    #4 Load checkins into json parser
    statuses_json = json.loads(statuses)

    #3 Write profile data to file
    sfile2 = open(settings.FILE_WRITE_PATH + 'julia-statuses-v2.json', 'w')
    sfile2.write(json.dumps(statuses_json))
    sfile2.close()

    #2 Make HTTP Re`14yyquests for checkin data
    request_profiles = urllib2.Request(api_request_profiles)
    response_profiles = urllib2.urlopen(request_profiles)
    
    #3 Read checkin data from HTTP Request
    profiles = response_profiles.read()
    
    #4 Load checkins into json parser
    checkin_profiles = json.loads(profiles)

    #3 Write profile data to file
    sfile1 = open(settings.FILE_WRITE_PATH + 'julia-profiles-v2.json', 'w')
    sfile1.write(json.dumps(checkin_profiles))
    sfile1.close()

    '''

    #return HttpResponse('<h1>Page was found</h1>')
    return render_to_response('generic/etsy/etsy_start.html',
                              {'photo_json' : scrubbed_photo_data,})


