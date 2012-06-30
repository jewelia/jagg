from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response

import urllib
import urllib2
import urlparse
import httplib2
import json
import oauth2 as oauth
from urlparse import parse_qsl, urlparse
from urllib import urlencode


def connect_to_service(request):
    return render_to_response('singly.html')

def singly_authorize(request):
    SINGLY_ACCESS_TOKEN_URL = 'https://api.singly.com/oauth/access_token'
    SINGLY_PROFILES = 'https://api.singly.com/v0/profiles'

    SINGLY_PHOTOS= 'https://api.singly.com/v0/types/checkins'
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
    print photo_json

    #3 Write profile data to file
    sfile = open(settings.FILE_WRITE_PATH + 'julia-photos.json', 'w')
    sfile.write(str(photo_json))
    sfile.close()

    ''' CHECKINS '''
    #2 Make HTTP Re`14yyquests for checkin data
    request_checkins = urllib2.Request(api_request_checkins)
    response_checkins = urllib2.urlopen(request_checkins)
    
    #3 Read checkin data from HTTP Request
    checkins = response_checkins.read()
    
    #4 Load checkins into json parser
    checkin_json = json.loads(checkins)

    #3 Write profile data to file
    sfile1 = open(settings.FILE_WRITE_PATH + 'julia-checkins.json', 'w')
    sfile1.write(str(checkin_json))
    sfile1.close()

    ''' STATUS '''
    #2 Make HTTP Requests for checkin data
    request_statuses = urllib2.Request(api_request_status)
    response_statuses = urllib2.urlopen(request_statuses)
    
    #3 Read checkin data from HTTP Request
    statuses = response_statuses.read()
    
    #4 Load checkins into json parser
    statuses_json = json.loads(statuses)

    #3 Write profile data to file
    sfile2 = open(settings.FILE_WRITE_PATH + 'julia-statuses.json', 'w')
    sfile2.write(str(statuses_json))
    sfile2.close()

    ''' STATUS '''
    #2 Make HTTP Re`14yyquests for checkin data
    request_profiles = urllib2.Request(api_request_profiles)
    response_profiles = urllib2.urlopen(request_profiles)
    
    #3 Read checkin data from HTTP Request
    profiles = response_profiles.read()
    
    #4 Load checkins into json parser
    checkin_profiles = json.loads(profiles)

    #3 Write profile data to file
    sfile1 = open(settings.FILE_WRITE_PATH + 'julia-profiles.json', 'w')
    sfile1.write(str(checkin_profiles))
    sfile1.close()

    return HttpResponse('<h1>Page was found</h1>')
    #return render_to_response('generic/etsy/etsy_start.html',{'sign_in_url': })

