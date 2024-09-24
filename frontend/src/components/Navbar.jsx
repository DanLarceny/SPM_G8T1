import { Button, ButtonGroup } from '@mui/material';
import { useNavigate} from 'react-router-dom';

import '../Navbar.css';

const Navbar = () => {
    const navigate = useNavigate();
    const handleHomeRedirect = () => {
        navigate('/home');
      };
    
    const handleUserRedirect = () => {
        navigate('/user');
    };

    return (
        <div className='navbar' style={{fontSize:"1px"}}>      
          <ButtonGroup size="large" variant="text" aria-label="Basic button group">
            <Button onClick={handleHomeRedirect}>Home</Button>
            <Button>Appointment</Button>
            <Button onClick={handleUserRedirect}>User</Button>
          </ButtonGroup>
        </div>

    );

}

export default Navbar;