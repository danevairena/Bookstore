import Posts from '../components/Posts';
import Container from 'react-bootstrap/Container';

export default function HomePage() {
  return (
    <Container className="Content">
        <Posts />
    </Container>    
  );
}