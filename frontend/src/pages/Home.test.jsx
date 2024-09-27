import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { HomePage } from './Home';

// Mock useNavigate
const mockedUseNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUseNavigate,
}));

describe('HomePage Component', () => {
  const mockLogout = jest.fn();

  const renderHomePage = () => {
    render(
      <BrowserRouter>
        <HomePage logout={mockLogout} />
      </BrowserRouter>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders welcome message', () => {
    renderHomePage();
    expect(screen.getByText(/Welcome!/i)).toBeInTheDocument();
  });

  test('renders all navigation items', () => {
    renderHomePage();
    expect(screen.getByText('Profile')).toBeInTheDocument();
    expect(screen.getByText('Your Schedule')).toBeInTheDocument();
    expect(screen.getByText('Team Schedule')).toBeInTheDocument();
    expect(screen.getByText('Apply for Arrangements')).toBeInTheDocument();
    expect(screen.getByText('Arrangement Details')).toBeInTheDocument();
  });

  test('logout button is present and clickable', () => {
    renderHomePage();
    const logoutButton = screen.getByText('Logout');
    expect(logoutButton).toBeInTheDocument();
    fireEvent.click(logoutButton);
    expect(mockLogout).toHaveBeenCalled();
    expect(mockedUseNavigate).toHaveBeenCalledWith('/login');
  });

  test('navigation items are clickable and navigate correctly', () => {
    renderHomePage();
    const profileItem = screen.getByText('Profile');
    fireEvent.click(profileItem);
    expect(mockedUseNavigate).toHaveBeenCalledWith('/profile');

    const scheduleItem = screen.getByText('Your Schedule');
    fireEvent.click(scheduleItem);
    expect(mockedUseNavigate).toHaveBeenCalledWith('/schedule');

    const teamScheduleItem = screen.getByText('Team Schedule');
    fireEvent.click(teamScheduleItem);
    expect(mockedUseNavigate).toHaveBeenCalledWith('/team-schedule');

    const applyArrangementsItem = screen.getByText('Apply for Arrangements');
    fireEvent.click(applyArrangementsItem);
    expect(mockedUseNavigate).toHaveBeenCalledWith('/apply-arrangements');

    const arrangementDetailsItem = screen.getByText('Arrangement Details');
    fireEvent.click(arrangementDetailsItem);
    expect(mockedUseNavigate).toHaveBeenCalledWith('/arrangement-details');
    });
});