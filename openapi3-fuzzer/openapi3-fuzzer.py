import json
import requests
import logging
import re
import sys
import argparse
from prance import ResolvingParser
from http.client import HTTPConnection
from time import sleep

def do_post_req(ep,headers,payload):
  """
  Perform an actual POST request
  returns the response object r
  """
  try:
      # print("--- Starting POST request to {}".format(ep))
      sleep(0.05)
      r = requests.post('{}'.format(ep), data=payload, headers=headers, timeout=20, allow_redirects=False)
  except Exception as e:
      print("    Exception connecting to {} with {}".format(ep,str(e)))
      return({"status_code": -1, "content": ""})
  else:
      # print("    POST request to {} returned status {}: {}".format(ep, r.status_code, r.content))
      return r
      
def do_get_req(ep,headers):
  """
  Perform an actual GET request
  returns the response object r
  """
  try:
      # print("--- Starting GET request to {}".format(ep))
      sleep(0.05)
      r = requests.get('{}'.format(ep), headers=headers, timeout=20, allow_redirects=False)
  except Exception as e:
      print("    Exception connecting to {} with {}".format(ep,str(e)))
      return({"status_code": -1, "content": ""})
  else:
      # print("    GET request to {} returned status {}: {}".format(ep,r.status_code, r.content))
      return(r)

def generate_happy_day_url_from_pathvars(baseurl, path, pathvars):
  """
  From a given OAS3 endpoint with path parameters,
  generate 1 URL while substituting all params with happy day strings
  """ 
  url = "{}{}".format(baseurl,path)
  if pathvars is not None:
    for pathvar in pathvars:
      # happydaystring = open("fuzz-{}.txt".format(pathvar.get("name"))).readlines()[0]
      happydaystring = open("fuzz.txt").readlines()[0]
      url = url.replace("{{{}}}".format(pathvar.get("name")),happydaystring.rstrip())
  return url

def generate_urls_from_pathvars(baseurl, path, pathvars):
  """
  From a given OAS3 endpoint with path parameters,
  generate all the possible URLs to fuzz
  while only substituting 1 param with all fuzzing entries
  and using happy day strings for the other parameters
  """
  urls=set()
  for pathvar in pathvars:
    if pathvar.get('in', None) == 'path' and 'name' in pathvar.keys():
      # lines = open("fuzz-{}.txt".format(pathvar.get("name"))).readlines()
      lines = open("fuzz.txt").readlines()
      for line in lines:
        url = "{}{}".format(baseurl,path)
        url = url.replace("{{{}}}".format(pathvar.get("name")),line.rstrip())
        for otherpathvar in pathvars:
          # replacement = open("fuzz-{}.txt".format(otherpathvar.get("name"))).readlines()[0]
          replacement = open("fuzz.txt").readlines()[0]
          url = url.replace("{{{}}}".format(otherpathvar.get("name")),replacement.rstrip())
        urls.add(url)
  return urls

def generate_payloads_from_postvars(postvars):
  """
  From a given OAS3 dict of requestBody variables
  generate a list of payload dicts
  """
  payloads = []
  payload = {}

  lines = open("fuzz.txt").readlines()
  happydaystring=lines[0].rstrip()
  for jsontype in [ "int", "str", "arr", "none" ]:
    for fuzzparam in postvars.keys():
      for line in lines:
        payload={}
        for param in postvars.keys():
          if param==fuzzparam:
            if jsontype=="int":
              try:
                payload[param] = int(line.rstrip())
              except ValueError:
                payload[param] = line.rstrip()
            elif jsontype=="str":
              payload[param] = line.rstrip()
            elif jsontype=="arr":
              payload[param] = [ line.rstrip() ]
            elif jsontype=="none":
              payload[param] = None
          else:
            payload[param] = happydaystring
        payloads.append(payload)
  payloads_uniq = []
  for payload in payloads:
    if payload not in payloads_uniq:
      payloads_uniq.append(payload)
  return payloads_uniq

def do_post_fuzzing(*args, **kwargs):
  baseurl=kwargs.get('baseurl', "")
  headers=kwargs.get('headers', {})
  path=kwargs.get('path', None)
  pathvars=kwargs.get('pathvars', {})
  postvars=kwargs.get('postvars', {})
  responses=kwargs.get('responses', [])

  newresponses = []
  for response in responses:
    try:
      newresponses.append(int(response))
    except ValueError:
      newresponses.append(response)
  responses = newresponses

  url = generate_happy_day_url_from_pathvars(baseurl, path, pathvars)
  payloads = generate_payloads_from_postvars(postvars)
  stats = {}

  for payload in payloads:
    r = do_post_req(url, headers, payload)
    try:
      stats[r.status_code] = stats[r.status_code] + 1
    except KeyError:
      stats[r.status_code] = 1
    if (r.status_code not in responses) and r.status_code<500:
      print("\n- Unexpected status code\n  Endpoint returned {} but expected one of {}\n  POST {}\n{}".format(r.status_code, responses, url, json.dumps(payload,  indent=4)))
    elif r.status_code>=500:
      print("\n* INTERNAL SERVER ERROR\n  Endpoint returned {} but expected one of {}\n  POST {}\n{}".format(r.status_code, responses, url, json.dumps(payload,indent=4)))
  return stats

def do_get_fuzzing(*args, **kwargs):
  """
  Perform fuzzing on a GET endpoint
  """
  baseurl=kwargs.get('baseurl', "")
  headers=kwargs.get('headers', {})
  path=kwargs.get('path', None)
  pathvars=kwargs.get('pathvars', {})
  responses=kwargs.get('responses', [])

  urls = generate_urls_from_pathvars(baseurl, path, pathvars)
  stats = {}

  newresponses = []
  for response in responses:
    try:
      newresponses.append(int(response))
    except ValueError:
      newresponses.append(response)
  responses = newresponses

  for url in urls:
    r = do_get_req(url, headers)
    try:
      stats[r.status_code] = stats[r.status_code] + 1
    except KeyError:
      stats[r.status_code] = 1
    if (r.status_code not in responses) and r.status_code<500:
      print("\n- Unexpected status code\n  Endpoint returned {} but expected one of {}\n  GET {}".format(r.status_code, responses, url))
    elif r.status_code>=500:
      print("\n* INTERNAL SERVER ERROR\n  Endpoint returned {} but expected one of {}\n  GET {}".format(r.status_code, responses, url))
  return stats

# HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('base_url', type=str, help='Base URL of the OAS3 API, e.g. https://dev.myapi.example, without trailing slash')
  parser.add_argument('oas3spec_url', type=str, help='URL to fetch the OpenAPI3 spec file from, e.g. https://dev.myapi.example/openapi.json')
  parser.add_argument('--auth', type=str, help='Authorization header field, e.g. "Bearer longbase64string", or "Basic shortb64string"')
  args = parser.parse_args()
  
  baseurl = args.base_url
  specurl = args.oas3spec_url
  headers = { "Authorization": args.auth,
              "Content-type": "application/json"}

  parser = ResolvingParser(specurl)
  spec = parser.specification  # contains fully resolved specs as a dict
  # print(json.dumps(parser.specification.get("paths").get("/employees/expenses/{expenses_id}/attachments").get("post"),indent=2))
  for path, pathvalues in spec.get("paths",{}).items():
    for method,methodvalues in pathvalues.items():
      pathvars = {}
      postvars = {}
      if method == 'get':
        if 'parameters' in methodvalues.keys():
          pathvars = methodvalues.get("parameters",{})
          responses = list(methodvalues.get("responses",{}).keys())
          print("--------------------------------------------")
          print("GET fuzzing {}".format(path))
          stats = do_get_fuzzing(baseurl=baseurl, headers=headers, path=path, pathvars=pathvars, responses=responses)
          print(json.dumps(stats,indent=2))
      if method == 'post':
        # print(json.dumps(methodvalues, indent=2)
        responses = list(methodvalues.get("responses",{}).keys())
        if 'requestBody' in methodvalues.keys() and 'parameters' in methodvalues.keys():
          pathvars = methodvalues.get("parameters")
          postvars = methodvalues.get("requestBody",{}).get("content",{}).get("application/json",{}).get("schema",{}).get("properties",{})
          print("--------------------------------------------")
          print("POST fuzzing param URL {}:".format(path))
          stats = do_post_fuzzing(baseurl=baseurl, headers=headers, path=path, pathvars=pathvars, postvars=postvars, responses=responses)
          print(json.dumps(stats,indent=2))
        elif 'requestBody' in methodvalues.keys():
          postvars = methodvalues.get("requestBody",{}).get("content",{}).get("application/json",{}).get("schema",{}).get("properties",{})
          print("--------------------------------------------")
          print("POST fuzzing non-param URL {}:".format(path))
          stats = do_post_fuzzing(baseurl=baseurl, headers=headers, path=path, postvars=postvars, responses=responses)
          print(json.dumps(stats,indent=2))
      sys.stdout.flush()


