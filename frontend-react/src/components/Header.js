import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { NavLink } from 'react-router-dom';


export default function Header() {
  return (
    <Navbar bg="info" sticky="top" className="Header">
        <Container>
        <Navbar.Brand href="/">BOOKSTORE</Navbar.Brand>
        <Form className="d-flex">
            <Form.Control type="search" size="sm" placeholder="Search" className="me-2" aria-label="Search"/>
            <Button variant="outline-dark" size="sm">Search</Button>
        </Form>
        <Nav variant="underline" defaultActiveKey="/"className="justify-content-end">
            {/* NavLink component from React-Router is used to generate an SPA links */}
            <Nav.Item>
                <Nav.Link as={NavLink} to="/" href="/">Home</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link as={NavLink} to="/explore" eventKey="/explore">Explore</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link as={NavLink} to="/sell" eventKey="/sell">Sell</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link as={NavLink} to="/account" eventKey="/account">Account</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link as={NavLink} to="/messages" eventKey="/messages">Messages</Nav.Link>
            </Nav.Item>
        </Nav>
      </Container>
    </Navbar>
  );
}