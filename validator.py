
class Validator:
    @staticmethod
    def validate_start_evt( event: str, start_date: int, end_date: int, notif_time: int):
        
        if len(event) < 4:
            raise ValueError("Event title too short")
        elif end_date < start_date:
            raise ValueError("End date cannot be before start date")
        elif notif_time < 0 or notif_time > 23:
            raise ValueError("Invalid notification time")
        elif end_date-start_date < 24*3600  : 
            raise ValueError("Event duration is too short") 
    
    @staticmethod
    def validate_add_challenge( event_start: int, chal_start: int|None):
        if chal_start != None  :
            if chal_start < event_start and chal_start:
                raise ValueError("Challenge start date cannot be before event start date") 
                
