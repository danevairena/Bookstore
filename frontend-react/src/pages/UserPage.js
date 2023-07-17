import { useParams } from 'react-router-dom';
import Container from 'react-bootstrap/Container';

export default function UserPage() {
  const { username } = useParams();

  return (
    <Container className="Content">
      <h1>{username}</h1>
      <p>TODO</p>
    </Container>
  );
}