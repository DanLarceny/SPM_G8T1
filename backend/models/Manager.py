from Employee import Employee;

class Manager(Employee):
    """_summary_

    Args:
        Employee (_type_): Manager role
    """
    
    # application will be the instance of the WFH_Application model/class
    def approve_application(self, application):
        if self.role == 'Manager':
            application.approve()  # Calls the approve method of WFHApplication

    def reject_application(self, application):
        if self.role == 'Manager':
            application.reject()  # Calls the reject method of WFHApplication