import Container from 'react-bootstrap/Container';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import ExplorePage from './pages/ExplorePage';
import LoginPage from './pages/LoginPage';
import SellPage from './pages/SellPage';
import AccountPage from './pages/AccoutPage';
import MessagesPage from './pages/MessagesPage';
import UserPage from './pages/UserPage';

export default function App() {
  return (
    <Container fluid className="App">

      {/* The BrowserRouter component adds routing support to the application. This component must be added very high 
      in the component hierarchy, as it must be a parent to all the routing logic in the application. */}
      <BrowserRouter>
        <Header />

        {/* Routes is a component that needs to be inserted in the place in the component tree where the contents 
        need to change based on the current page. */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/explore" element={<ExplorePage />} />
          <Route path="/login" element={<LoginPage />} />
          
          {/* To define a route with a dynamic section, the path attribute of the Route component uses a special syntax with a : prefix */}
          <Route path="/user/:username" element={<UserPage />} />
          <Route path="/sell" element={<SellPage />} />
          <Route path="/account" element={<AccountPage />} />
          <Route path="/messages" element={<MessagesPage />} />

          {/* Navigate is a special component that allows to redirect from one route to another. 
          The * works as a catch-all route for any URLs that are not matched by the routes declared above it. 
          The element attribute in this route uses Navigate to redirect all these unknown URLs to the root URL.*/}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </Container>
  );
}