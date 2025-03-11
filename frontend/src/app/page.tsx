export default async function Page() {
  const res = await fetch(
    process.env.NEXT_PUBLIC_BASE_URL + "/create_quiz",
    {
      method: "POST",
    }
  );
  const payload = await res.json();
  const message = payload.message;
  // const message = 'Hello Plain Text'

  return (
    <>
      Hello World.<br></br>
      this is a message from FastAPI → {message}
    </>
  );
}
