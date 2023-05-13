#############################
#### Jean Wu, 20211002
#### graphql API call with dqe call
#### based on different query
############################

from os import path
import json
from base64 import b64encode
import requests


#tpt_id_key_list = ["HA22ARG7AJPX","FD20RAP01DPR","IA22WLDDDNGX","HR21DEU500SBH1"]

def call_graphql_api(tpt_id_key, graphql_opt):

    ##client_secret = "a9~_.MGuol6UnGu5VJo357h~u_zPuJT58n"
    client_secret =  "Gb97Q~mdaup3YIgrsWa4wXaP~YZSN6CJir-Ny"
    app_id = "b4fd365f-23e4-4fb9-a2ed-1cf01d38ab17"
    url = "https://login.microsoftonline.com/fcb2b37b-5da0-466b-9b83-0014b67a7c78/oauth2/v2.0/token"

    ## get token for graphq
    def get_token(url, app_id, client_secret):
        '''
        Azure authentication
        '''        
        scope = app_id+'/.default'
        basic_auth = b64encode(f'{app_id}:{client_secret}'
                                .encode('ascii')).decode('ascii')
        headers = {'Authorization': f'Basic {basic_auth}'}
        payload = {'grant_type': 'client_credentials',
                    'scope':scope}
        try:
            resp = requests.post(url, headers=headers, data=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as ex:
            print(ex)
            return None
    ## get token
    token = get_token(url, app_id, client_secret)['access_token']

    # defining the api-endpoint  
    #API_ENDPOINT = "https://fst-graphql-api.agro.services/graphql"
    API_ENDPOINT = "https://fst-graphql-dev.agro.services/graphql"
    
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer {}'.format(token)}
    headers =  {'Authorization': 'Bearer {}'.format(token)}
    # sending post request and saving response as response 

    ## Correct graphql query based on different options/rules
    if graphql_opt == 'TD_0':
        query = """  
                query{
                    trialDescriptions(filter: [{
                tptIdKey:["%s"]
                    }]
                    ){
                    
                    tptIdKey
                    projectNumbers
                    keywords
                    siteType
                    experimentalSeason
                    numberOfReplicates
                    plannedNumberOfApplications
                    targets{
                        name
                    }
                    crops{
                        name
                    }
                    
                    protocolEditionNumber
                    guidelines
                    plotArea
                    plotAreaUnit
                    dataDeadline
                    
                    fieldResponsibles {
                        type
                        typeCode
                    }
                    
                    trialResponsibles{
                        hasName
                        siteName
                        testType
                        internalValue
                        plannedNumberOfTrials
                    }
                    
                    }}


                         """ %(tpt_id_key)


    elif graphql_opt == 'TD_1':
        query = """ 
                 query{
                trialDescriptions(filter: [{
                tptIdKey:["%s"]
                }]
                ){
                
                tptIdKey
                keywords
                guidelines
                dataDeadline
                controlField
                plannedNumberOfApplications
                protocolEditionNumber
                numberOfReplicates
                plotArea
                plotAreaUnit
                siteType
                
                plotDescription
                plotDescriptionBasis
                experimentalSeason
                targets{
                    targetName: name
                }
                
                gepCertification   
                
                        
                fieldResponsibles {
                    type
                    typeCode
                }
                
                
                plannedAssessments {
                            standardEvaluationId
                    partRated
                    ratingType
                    sampleSize
                    sampleSizeUnit
                    target{
                    name
                    }
                    crop{
                    name
                    }
                    plannedUnit : unit
                    numberOfSubSamples
                    ratingClass        
                    assessmentCode
                }
                
                treatments{
                    applications{
                    applicationCode
                    applicationTimingCode
                    products{
                        equipment{
                        method
                        placement
                        }
                    }
                    crops{
                        cropStageCode
                        
                    }
                    }
                }
                
                trialResponsibles {
                    hasName
                    internalValue
                    plannedNumberOfTrials
                    siteName
                    testType
                }
                
                crops{
                    useGroupCode
                }
                }}  
        
                      """ %(tpt_id_key)

    elif graphql_opt == 'Protocol':
        ## define query
        query = """
                 query{
                        protocols(filter: [{
                                tptIdKey:["%s"]
                        }]
                        ){
                        
                        tptIdKey
                        keywords
                        guidelines
                        dataDeadline
                        controlField
                        plannedNumberOfApplications
                        protocolEditionNumber
                        numberOfReplicates
                        plotArea
                        plotAreaUnit
                        siteType
                        
                        plotDescription
                        plotDescriptionBasis
                        experimentalSeason
                        targets{
                            targetName: name
                        }
                        
                        gepCertification
                        
                        
                        
                        fieldResponsibles {
                            type
                            typeCode
                        }
                        
                        
                        plannedAssessments
                        {
                                    standardEvaluationId
                            partRated
                            ratingType
                            sampleSize
                            sampleSizeUnit
                            target{
                            name
                            }
                            crop{
                            name
                            }
                            plannedUnit : unit
                            numberOfSubSamples
                            ratingClass        
                            assessmentCode
                        }
                        
                        treatments{
                            treatmentKey
                                    harvestDestruction
                            applications{
                            applicationCode
                            applicationTimingCode
                            products{
                                equipment{
                                method
                                placement
                                }
                            }
                            crops{
                                cropStageCode
                           
                            }
                            }
                        }
                        
                        trialResponsibles {
                            hasName
                            internalValue
                            plannedNumberOfTrials
                            siteName
                            testType
                        }
                        
                        crops{
                            useGroupCode
                            cropName: name
                        }
                        
                        projectNumbers
                        
                        location{
                            country
                        }
                        
                        }}
               
                            """ %(tpt_id_key)


    ## send post requst and get result
    try:
        r = requests.post(url = API_ENDPOINT,headers=headers,json={"query": query})
        r.raise_for_status()
        return r.json()
    except Exception as ex:
        print("Error in calling Graphql API call:, ", ex)
        return None

    # print("**** graphql result ****")
    # print(r.text)
    # print(tpt_id_key)
    # input('**** graphql result****')
    return r.json()

#######################
## call dqe api
#######################
def call_dqe(data, tpt_id_key):
    
    #client_secret = "pLfps_g-4~RfMxXiRo5md2zOV.9I5UVVCc"
    #app_id = "f2fc7c38-1d57-4925-a151-2ddd4e4d2490"
    client_secret = "iXx7Q~LsVJFYfrpcQgtX.ZsZvMrwdhQUsOkf4"
    app_id = "b4fd365f-23e4-4fb9-a2ed-1cf01d38ab17"
    url = "https://login.microsoftonline.com/fcb2b37b-5da0-466b-9b83-0014b67a7c78/oauth2/v2.0/token"


    def get_token(url, app_id, client_secret):
        '''
        Azure authentication
        '''
        
        scope = app_id+'/.default'
        basic_auth = b64encode(f'{app_id}:{client_secret}'
                                .encode('ascii')).decode('ascii')
        headers = {'Authorization': f'Basic {basic_auth}'}
        payload = {'grant_type': 'client_credentials',
                    'scope':scope}

        try:
            resp = requests.post(url, headers=headers, data=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as ex:
            print("Error in getting token fo DQE API:, ", ex)
            return None
        # resp = requests.post(url, headers=headers, data=payload)
        # resp.raise_for_status()
        # return resp
    
    try:
        token = get_token(url, app_id, client_secret)['access_token']
    except Exception as e:
        print('*** error to get token ****')
        print(e)
        token = None


    # defining the api-endpoint  
    #API_ENDPOINT = "https://fst-dqe-dev.agro.services/run"
    API_ENDPOINT = "http://10.62.152.231:10020/run"
    ## get header
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer {}'.format(token)}
    
    if token:
        headers = {'Content-type': 'application/json',  'Authorization': 'Bearer {}'.format(token)}
        #print(json.dumps(data))
        try :
            # sending post request and saving response as response object 
            res = requests.post(url = API_ENDPOINT, data=json.dumps(data), headers=headers)
            rtn = res.text
            json_rtn = json.loads(rtn)
            # print('***** DQE API call result ****')
            # print(json_rtn)
            # input('***dqe result****')
            return json_rtn
        except Exception as e1:  
            # includes simplejson.decoder.JSONDecodeError
            print("Error in calling DQE API call")
            print(e1)
            return None
    else:
        return None
