export default function Posts() {
    const posts = [
      {
        id: 1,
        post_title: 'Zog!',
        descriprion: 'new child book',
        price: '25',
        timestamp: 'a minute ago',
        author: {
          username: 'susan',
        },
      },
      {
        id: 2,
        post_title: 'Book2',
        descriprion: 'mommy book',
        price: '10',
        timestamp: 'an hour ago',
        author: {
          username: 'jane',
        },
      },
    ];
  
    return (
      <>
        {posts.length === 0 ?
          <p>There are no posts.</p>
        :
          posts.map(post => {
            return (
              <p key={post.id}>
                <b>{post.author.username}</b> &mdash; {post.timestamp}
                <br />
                {post.post_title}
                <br />
                {post.descriprion}
                <br />
                {post.price}
                <br />
              </p>
            );
          })
        }
      </>
    );
  }