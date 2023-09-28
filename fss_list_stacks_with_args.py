import argparse
import requests
import json
import csv
 
fname = "stacklist.csv"
csv_header = ['name','stackID','status','provider','region', "account", 'type', 'scannerStack', 'bucket']
 
f = open(fname, "w", encoding='UTF8')
writer = csv.writer(f)
writer.writerow(csv_header)

global_fss_storage_counter = 0
global_fss_scanner_counter = 0
global_fss_other_counter = 0
global_bucket_list = []

def increment(counter):
    counter = counter
    global global_fss_storage_counter
    global global_fss_scanner_counter
    global global_fss_other_counter
    if counter == 'storage':
        global_fss_storage_counter +=1
    else:
        if counter == 'scanner':
            global_fss_scanner_counter +=1
        else:
            if counter == 'account-scanner':
                global_fss_other_counter +=1

def append_bucket_list(storage):
    storage = storage
    global_bucket_list.append(storage)

def get_data(base_url, headers, payload):
    
    response = requests.request("GET", base_url, headers=headers, data=payload)
     
    if response.status_code == 200:
        print(f"HTTP response code: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"HTTP response header: {response.headers}")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Error message: {response.headers}")
    print(f"############\n")

def api_calls(c1region, api_key):
    c1region = c1region
    api_key = api_key
    payload = {}
    headers = {
    'api-version': 'v1',
    'Accept': 'application/json',
    'Authorization': 'apikey '+api_key
    }
    cursor = ""
    limit = 100 # the maximum value is 100 results per query. The default value is 25
    cursor = ""

    while True:

        if cursor != "":
            base_url = 'https://filestorage.'+c1region+'.cloudone.trendmicro.com/api/stacks?limit='+str(limit)+'&cursor='+cursor
        else:
            base_url = 'https://filestorage.'+c1region+'.cloudone.trendmicro.com/api/stacks?limit='+str(limit)
        
        output = get_data(base_url, headers, payload)
        tprint = json.dumps(output, indent=4, sort_keys=True)
        dprint = json.loads(tprint)

        if dprint:
            if 'next' in dprint.keys():
                print(f"Pagagination ['next']: {dprint['next']}")
                nxt = dprint['next']
                if nxt == cursor:
                    return False
                else:
                    cursor = dprint['next']
            else:
                #print("You got all the data.")
                for i in dprint['stacks']:

                    #print(f"\n{i}")
                    details = i['details']
                    print(f"\ndetails: {str(details)}")
                    provider_region = details.get('region')
                    print(f"\tregion: {provider_region}")
                    account = details.get('account')
                    print(f"\taccount: {account}")

                    name = str(i['name'])
                    print("\nname: "+name)
                    stackID = str(i['stackID'])
                    print("\tStackID: "+stackID)
                    status = str(i['status'])
                    print("\tstatus: "+status)
                    stype = str(i['type'])
                    print("\ttype: "+stype)
                    provider = str(i['provider'])
                    print("\tprovider: "+provider)

                    if stype == 'scanner':
                        scannerStack = ''
                        storage = ''
                        increment('scanner')
                    else:
                        scannerStack = str(i['scannerStack'])
                        storage = str(i['storage'])
                        print(f"\tstorage: {storage}")
                        append_bucket_list(storage)
                        if stype == 'storage':
                            increment('storage')
                        else:
                            if stype == 'account-scanner':
                                increment('account-scanner')
                    writer.writerow([name,stackID, status, provider, provider_region, account, stype, scannerStack, storage ])
                return False

            
            for i in dprint['stacks']:

                details = i['details']
                print(f"\ndetails: {str(details)}")
                provider_region = details.get('region')
                print(f"\tregion: {provider_region}")
                account = details.get('account')
                print(f"\taccount: {account}")

                name = str(i['name'])
                print("\tname: "+name)
                stackID = str(i['stackID'])
                print("\tStack ID: "+stackID)
                status = str(i['status'])
                print("\tstatus: "+status)
                stype = str(i['type'])
                print("\tstype: "+stype)
                provider = str(i['provider'])
                print("\tprovider: "+provider)

                if stype == 'scanner':
                    scannerStack = ''
                    storage = ''
                    increment('scanner')
                else:
                    scannerStack = str(i['scannerStack'])
                    storage = str(i['storage'])
                    print(f"\tstorage: {storage}")
                    append_bucket_list(storage)
                    if stype == 'storage':
                        increment('storage')
                    else:
                        if stype == 'account-scanner':
                            increment('account-scanner')
                writer.writerow([name,stackID, status, provider, provider_region, account, stype, scannerStack, storage ])


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--region', action='store',
                        help='Cloud One service region; e.g. us-1, de-1, etc')
    parser.add_argument('--api_key', action='store',
                        help='api key for authentication')
    args = parser.parse_args()

if args.region and args.api_key is not None:
    c1region = args.region
    api_key = args.api_key
    response = api_calls(c1region, api_key)
    output = response
    tprint = json.dumps(output, indent=4, sort_keys=True)
    print(f"\nList with all of the stacks: {fname}")
    print(f"Number of Storage Stacks: {global_fss_storage_counter}")
    print(f"Number of Scanner Stacks: {global_fss_scanner_counter}")
    print(f"Number of Account Scanner: {global_fss_other_counter}")
    print(f"Number of Buckets: {len(global_bucket_list)}")
    #print(f"Bucket List: {str(global_bucket_list)}")
else:
    print("\nError: missing region or api_key")
    print("\nusage: \npython fss_list_stacks_with_args.py -r <Cloud One region> --api_key <Cloud One API key>")
    print("\ne.g.: \npython fss_list_stacks_with_args.py -r us-1 --api_key tmc12VIiv2ek0PmNotiK3AnKV5VfHwv:5zeW14fkn8kkmVF6NMe3VFKj89uJVFKN6NMiJhVFKpyEH6NMwDkb7w3B2A5DWsYwDS")
    exit()

