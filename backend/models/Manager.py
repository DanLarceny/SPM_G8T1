from Employee import Employee;

class Manager(Employee):
    """_summary_

    Args:
        Employee (_type_): Manager role
    """
    
    # application will be the instance of the WFH_Application model/class
    def approve_application(self, application):
        if application.staus == "pending":
            application.approve()  # Calls the approve method of WFHApplication

    def reject_application(self, application):
        if  application.staus == "pending":
            application.reject()  # Calls the reject method of WFHApplication
    
    
    # method to get schedules for those under manager