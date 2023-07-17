import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';


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
            <Nav.Item>
                <Nav.Link href="/">Home</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href="/explore">Explore</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href="#link">Sell</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href="#link">Account</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link href="#link">Messages</Nav.Link>
            </Nav.Item>
        </Nav>
      </Container>
    </Navbar>
  );
}