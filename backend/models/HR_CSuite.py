from models.Manager import Manager
from models.WFH_Schedule import WFHSchedule

class HR_CSuite(Manager):
    """_summary_

    Args:
        Employee (_type_): HR/Senior Management roles
    """
    
    
    
    # method to get all the schedules
    def get_all_schedules(self):
        """Returns all WFH schedules for all employees."""
        return WFHSchedule.query.all()