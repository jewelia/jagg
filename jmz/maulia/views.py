from django.conf import settings
from django.shortcuts import render_to_response

import urllib
import urllib2
import json


def index(request):
    return render_to_response('singly.html',
                              { 'instagram': False,
                               'facebook' : False,
                               'linkedin' : False,
                               'foursquare' : False,
                               'twitter' : False
                               })

def connect_to_service(request):
    SINGLY_ACCESS_TOKEN_URL = 'https://api.singly.com/oauth/access_token'
    SINGLY_PROFILES = 'https://api.singly.com/v0/profiles'

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

    
    api_request_profiles = SINGLY_PROFILES + '?access_token=' + access_token
    
    request.session['REQ_TOKEN_SESSION_KEY'] = access_token
    
    all_api_calls = {'profile': api_request_profiles}

    for key in all_api_calls.keys():
        call = all_api_calls[key]

        a_request = urllib2.Request(call)
        a_response = urllib2.urlopen(a_request)
        a_data = a_response.read()

        a_json = json.loads(a_data)
        print a_json

        try:
            if a_json['twitter']:
                twitter = True
        except KeyError:
            twitter = False
        try:
            if a_json['facebook']:
                facebook = True
        except KeyError:
                facebook = False
        try:
            if a_json['linkedin']:
                linkedin = True
        except KeyError:
            linkedin = False
        try:
            if a_json['foursquare']:
                foursquare = True
        except KeyError:
            foursquare = False
        try:
            if a_json['instagram']:
                instagram = True
        except KeyError:
            instagram = False
            
        print "Instagram " + str(instagram)

    return render_to_response('singly.html',
                              { 'instagram': instagram,
                               'facebook' : facebook,
                               'linkedin' : linkedin,
                               'foursquare' : foursquare,
                               'twitter' : twitter
                               })

def singly_authorize(request):
    access_token = request.session['REQ_TOKEN_SESSION_KEY']
    
    SINGLY_PROFILES = 'https://api.singly.com/v0/profiles'

    SINGLY_PHOTOS= 'https://api.singly.com/v0/types/photos'
    SINGLY_CHECKINS = 'https://api.singly.com/v0/types/checkins'
    SINGLY_STATUS = 'https://api.singly.com/v0/types/statuses'
    '''
    SINGLY_ACCESS_TOKEN_URL = 'https://api.singly.com/oauth/access_token'
    FOURSQUARE = 'https://api.singly.com/v0/services/foursquare/checkins'

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
    '''

    #1 Fetch Profile Data
    api_request_profiles = SINGLY_PROFILES + '?access_token=' + access_token
    api_request_photos = SINGLY_PHOTOS + '?access_token=' + access_token
    api_request_checkins = SINGLY_CHECKINS + '?access_token=' + access_token
    api_request_status = SINGLY_STATUS + '?access_token=' + access_token
    #api_request_foursquare = FOURSQUARE + '?access_token=' + access_token

    all_api_calls = {'profile': api_request_profiles,
                     'photo' : api_request_photos,
                     'checkin': api_request_checkins,
                     'status' : api_request_status,}
                     #'foursquare' : api_request_foursquare}

    scrubbed_photo_data = []
    scrubbed_profile_data= []
    scrubbed_checkin_data = []
    scrubbed_status_data = []

    for key in all_api_calls.keys():
        call = all_api_calls[key]

        a_request = urllib2.Request(call)
        a_response = urllib2.urlopen(a_request)
        a_data = a_response.read()

        a_json = json.loads(a_data)
        json_array = []
        images_array = []
        count = 0
        if key != 'profile':

            #if key == 'checkin':
            #    print a_json

            while count < len(a_json):
                oembed_obj = a_json[count]['oembed']
                date_obj = a_json[count]['at']
                if str(date_obj).startswith('12', 0):
                    print "adjusting " + str(date_obj)
                    date_obj += 13744850000
                    #date_list = list(str(date_obj))
                    #date_list[0:1] = '13'
                    #date_obj = ''.join(date_list)
                if key == 'photo':
                    print date_obj
                if date_obj > '1341295445':
                    continue

                try:
                    if oembed_obj['provider_name']:
                        source = oembed_obj['provider_name']
                except KeyError:
                    source = ''

                try:
                    #if oembed_obj['type']:
                    #    type = oembed_obj['type']
                    if a_json[count]['idr'].find('twitter') > 0:
                        type = 'twitter'
                        lat = ''
                        lng = ''
                    elif a_json[count]['idr'].find('facebook') > 0:
                        type = 'facebook'
                        lat = a_json[count]['oembed']['lat']
                        lng = a_json[count]['oembed']['lng']
                    elif a_json[count]['idr'].find('linkedin') > 0:
                        type = 'linkedin'
                        lat = ''
                        lng = ''
                    elif a_json[count]['idr'].find('foursquare') > 0:
                        type = 'foursquare'
                        lat = ''
                        lng = ''
                    elif a_json[count]['idr'].find('instagram') > 0:
                        type = 'instagram'
                        lat = ''
                        lng = ''

                except KeyError:
                    type = ''
                    lat = ''
                    lng = ''

                try:
                    if key == 'photo':
                        if oembed_obj['provider_url']:
                            link = oembed_obj['provider_url']
                    elif key == 'status':
                        if type == 'facebook':
                            if a_json[count]['data']['actions'][0]['name']:
                                if a_json[count]['data']['actions'][0]['name'] == 'Comment':
                                    link = a_json[count]['data']['actions'][0]['link']
                        elif a_json[count]['idr'].find('twitter') > 0:
                            link = 'http://www.twitter.com/' + a_json[count]['data']['user']['screen_name'] + '/status/' + a_json[count]['data']['id_str']
                    elif key == 'checkin' or key == 'foursquare':
                        if type == 'foursquare':
                            link = 'https://foursquare.com/v/' + (a_json[count]['venue']['name']).replace(' ', '-') + "/" + a_json[count]['venue']['id']
                        if type == 'facebook':
                            link = 'https://www.facebook.com/' + a_json[count]['data']['from']['id'] + '/posts/' + a_json[count]['data']['id']

                except KeyError:
                    link = ''

                try:
                    if key == 'photo':
                        if oembed_obj['url']:
                            data = oembed_obj['url']
                            images_array.append(data)
                    elif key == 'status': 
                        if oembed_obj['text']:
                            data = oembed_obj['text']
                    elif key == 'checkin' or key == 'foursquare':
                        if oembed_obj['title']:
                            data = oembed_obj['title']

                except KeyError:
                    data = ''

                try:
                    if key == 'photo':
                        if oembed_obj['height']:
                            height = oembed_obj['height']
                except KeyError:
                    height = ''

                try:
                    if key == 'photo':
                        if oembed_obj['width']:
                            width = oembed_obj['width']
                except KeyError:
                    width = ''

                data = {
                    #'date' : date_obj,
                    'source' : source,
                    'type' : type,
                    'link' : link,
                    'data' : data,
                    'height' : height,
                    'width' : width,
                    'lat' : lat,
                    'lng' : lng,
                }
                a_tuple = [date_obj, data]
                json_array.append(a_tuple)
                count += 1
            json_array.sort()

            if key == 'photo':
                scrubbed_photo_data = json.JSONEncoder().encode(json_array)
                num_photos = str(len(json_array))
            if key == 'profile':
                scrubbed_profile_data = json.JSONEncoder().encode(json_array)
                num_profile = str(len(json_array))
            if key == 'checkin':
                scrubbed_checkin_data = json.JSONEncoder().encode(json_array)
                num_checkins= str(len(json_array))
            if key == 'status':
                scrubbed_status_data = json.JSONEncoder().encode(json_array)
                num_status = str(len(json_array))

    return render_to_response('data.html',
                              {'num_photos' : num_photos,
                               'num_status' : num_status,
                               'num_checkins' : num_checkins,
                               'photo_json' : scrubbed_photo_data,
                               'profile_json' : scrubbed_profile_data,
                               'checkin_json' : scrubbed_checkin_data,
                               'status_json' : scrubbed_status_data,
                               'images_array' : images_array}
                              )

