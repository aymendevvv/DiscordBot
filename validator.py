

def validate_new_event(title:str , startDate:int  , endDate:int):

    if endDate < startDate :
        raise ValueError("End date cannot be before start date")
    elif len(title) < 4 :
        raise ValueError("title too short")
    
def validate_add_challenge(event_start:int , chal_start:int) :
    if chal_start < event_start :
        raise ValueError(" date cannot be before start date of the event")
def validate_new_event():
    pass

    
    
